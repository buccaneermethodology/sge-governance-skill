#!/usr/bin/env python3
"""Adjudicate SP-041 paired rollouts and report measured token deltas."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[4]
CONTEXT_STATE_PATH = Path(__file__).with_name("context_state.py")


class PilotError(ValueError):
    pass


def _load_context_state():
    spec = importlib.util.spec_from_file_location("context_state", CONTEXT_STATE_PATH)
    if spec is None or spec.loader is None:
        raise PilotError("cannot load context_state.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _prompt_payload_sha256(text: str) -> str:
    encoded = text.encode("utf-8")
    framed = len(encoded).to_bytes(8, "big") + encoded
    return hashlib.sha256(framed).hexdigest()


def _extract_last_message(rollout: Path) -> Mapping[str, Any]:
    complete = []
    for raw in rollout.read_text(encoding="utf-8").splitlines():
        event = json.loads(raw)
        if event.get("type") == "event_msg" and event.get("payload", {}).get("type") == "task_complete":
            complete.append(event["payload"])
    if len(complete) != 1 or not isinstance(complete[0].get("last_agent_message"), str):
        raise PilotError(f"{rollout}: expected one task_complete with last_agent_message")
    try:
        value = json.loads(complete[0]["last_agent_message"])
    except json.JSONDecodeError as exc:
        raise PilotError(f"{rollout}: reviewer output is not strict JSON") from exc
    if not isinstance(value, dict):
        raise PilotError(f"{rollout}: reviewer output must be an object")
    return value


def adjudicate(output: Mapping[str, Any], oracle: Mapping[str, Any], arm: str) -> dict[str, Any]:
    expected_keys = {"arm_contract", "blockers", "non_blockers", "coverage", "verdict"}
    errors: list[str] = []
    if set(output) != expected_keys:
        errors.append("output_shape_mismatch")
    expected_arm = f"{arm}-v1"
    if output.get("arm_contract") != expected_arm:
        errors.append("arm_contract_mismatch")

    def index_findings(field: str) -> dict[str, Mapping[str, Any]]:
        raw = output.get(field)
        if not isinstance(raw, list):
            errors.append(f"{field}_not_array")
            return {}
        indexed: dict[str, Mapping[str, Any]] = {}
        for item in raw:
            if not isinstance(item, Mapping) or set(item) != {"category", "severity", "citation"}:
                errors.append(f"{field}_finding_shape")
                continue
            finding_id = item.get("category")
            if not isinstance(finding_id, str) or finding_id in indexed:
                errors.append(f"{field}_finding_id")
                continue
            indexed[finding_id] = item
        return indexed

    blockers = index_findings("blockers")
    non_blockers = index_findings("non_blockers")
    for field, actual in (("expected_blockers", blockers), ("expected_non_blockers", non_blockers)):
        expected = {item["category"]: item for item in oracle[field]}
        if set(actual) != set(expected):
            errors.append(f"{field}_id_mismatch")
        for finding_id in set(actual) & set(expected):
            if actual[finding_id].get("severity") != expected[finding_id]["severity"]:
                errors.append(f"{finding_id}_severity_mismatch")
            if actual[finding_id].get("citation") != expected[finding_id]["citation"]:
                errors.append(f"{finding_id}_citation_mismatch")

    coverage = output.get("coverage")
    if not isinstance(coverage, list) or set(coverage) != set(oracle["required_coverage"]):
        errors.append("coverage_mismatch")
    if output.get("verdict") != oracle["expected_verdict"]:
        errors.append("verdict_mismatch")
    return {"passed": not errors, "errors": sorted(set(errors))}


def _median(records: Sequence[Mapping[str, Any]], field: str) -> float:
    return float(statistics.median(record["usage"]["model_reported_usage"][field] for record in records))


def _saving(full: float, delta: float) -> float:
    if full <= 0:
        raise PilotError("full-arm metric must be positive")
    return round((full - delta) / full * 100.0, 3)


def summarize(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    full = [record for record in records if record["arm"] == "full"]
    delta = [record for record in records if record["arm"] == "delta"]
    if len(full) < 2 or len(delta) < 2:
        raise PilotError("at least two full and two delta arms are required")
    if any(not record["quality"]["passed"] for record in records):
        classification = "quality_failed"
    else:
        full_total_input = _median(full, "input_tokens")
        delta_total_input = _median(delta, "input_tokens")
        full_uncached = _median(full, "uncached_input_tokens")
        delta_uncached = _median(delta, "uncached_input_tokens")
        total_improved = delta_total_input < full_total_input
        uncached_improved = delta_uncached < full_uncached
        if total_improved and uncached_improved:
            classification = "validated_positive"
        elif not total_improved and not uncached_improved:
            classification = "negative"
        else:
            classification = "mixed"

    metrics = {}
    for field in ("input_tokens", "cached_input_tokens", "uncached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens"):
        full_value = _median(full, field)
        delta_value = _median(delta, field)
        metrics[field] = {
            "full_median": full_value,
            "delta_median": delta_value,
            "saving_percent": _saving(full_value, delta_value) if full_value else None,
        }
    return {"classification": classification, "metrics": metrics}


def evaluate_convergence_trace(trace: Mapping[str, Any]) -> dict[str, Any]:
    """Validate blocker admissibility, repeated-root escalation, and rebaseline."""
    if trace.get("schema_version") != "sge-convergence-pilot-v1":
        raise PilotError("unsupported convergence trace schema")
    scenarios = trace.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise PilotError("convergence trace must contain scenarios")
    admissible_bases = {
        "acceptance_criteria",
        "original_must_have",
        "evidence_integrity",
        "authority_boundary",
        "claim_ceiling",
        "in_scope_regression",
    }
    escalation_actions = {"rebaseline_required", "hardening_session", "human_scope_decision"}
    rebaseline_triggers = {
        "user_instruction_changed",
        "goal_revision_changed",
        "governance_revision_changed",
        "acceptance_criteria_changed",
        "original_objective_changed",
        "claim_ceiling_changed",
        "authority_boundary_changed",
        "truth_placement_changed",
        "dependency_changed",
        "execution_topology_changed",
        "threat_model_changed",
        "semantic_risk_changed",
        "patch_consistency_changed",
        "snapshot_identity_changed",
        "final_diff_outside_delta_read_set",
    }
    seen_ids: set[str] = set()
    repeated_root_seen = False
    rebaseline_seen = False
    summaries: list[dict[str, Any]] = []
    for scenario in scenarios:
        if not isinstance(scenario, Mapping):
            raise PilotError("convergence scenario must be an object")
        scenario_id = scenario.get("scenario_id")
        if not isinstance(scenario_id, str) or not scenario_id or scenario_id in seen_ids:
            raise PilotError("convergence scenario_id must be unique")
        seen_ids.add(scenario_id)
        rounds = scenario.get("rounds")
        if not isinstance(rounds, list) or not rounds:
            raise PilotError(f"convergence scenario {scenario_id} has no rounds")
        for index, round_entry in enumerate(rounds, start=1):
            if not isinstance(round_entry, Mapping):
                raise PilotError(f"convergence scenario {scenario_id} has malformed round")
            if round_entry.get("round") != index:
                raise PilotError(f"convergence scenario {scenario_id} round sequence is not contiguous")
            if round_entry.get("admissible_basis") not in admissible_bases:
                raise PilotError(f"convergence scenario {scenario_id} uses inadmissible blocker basis")
            if round_entry.get("outcome") != "blocked":
                raise PilotError(f"convergence scenario {scenario_id} weakens an open blocker")
            for field in ("mode", "root_cause_id", "finding_category"):
                if not isinstance(round_entry.get(field), str) or not round_entry[field]:
                    raise PilotError(f"convergence scenario {scenario_id} has empty {field}")
        kind = scenario.get("kind")
        action = scenario.get("expected_action")
        if kind == "repeated_root":
            repeated_root_seen = True
            expected_modes = [
                "initial_validation",
                "blocker_fix_delta_validation",
                "final_state_reconciliation",
            ]
            if len(rounds) < 3 or [item.get("mode") for item in rounds[:3]] != expected_modes:
                raise PilotError("repeated-root scenario lacks the required convergence rounds")
            roots = {item.get("root_cause_id") for item in rounds}
            if len(roots) != 1 or action not in escalation_actions:
                raise PilotError("repeated-root scenario does not escalate the same root cause")
        elif kind == "rebaseline_trigger":
            rebaseline_seen = True
            if scenario.get("trigger") not in rebaseline_triggers or action != "rebaseline_required":
                raise PilotError("rebaseline trigger does not stop delta validation")
        else:
            raise PilotError(f"unknown convergence scenario kind: {kind}")
        summaries.append({"scenario_id": scenario_id, "kind": kind, "round_count": len(rounds), "action": action})
    if not repeated_root_seen or not rebaseline_seen:
        raise PilotError("convergence trace must cover repeated-root escalation and rebaseline")
    return {"passed": True, "scenarios": summaries}


def evaluate_manifest(manifest_path: Path, oracle_path: Path) -> dict[str, Any]:
    manifest = _read_json(manifest_path)
    oracle = _read_json(oracle_path)
    if manifest.get("schema_version") != "sge-pilot-manifest-v1":
        raise PilotError("unsupported manifest schema")
    required_paths = {
        "baseline_snapshot_path",
        "post_snapshot_path",
        "snapshot_comparison_path",
        "convergence_trace_path",
    }
    if not required_paths.issubset(manifest):
        raise PilotError("manifest is missing durable snapshot bindings")
    baseline_path = Path(manifest["baseline_snapshot_path"])
    post_path = Path(manifest["post_snapshot_path"])
    comparison_path = Path(manifest["snapshot_comparison_path"])
    convergence_path = Path(manifest["convergence_trace_path"])
    baseline = _read_json(baseline_path)
    post = _read_json(post_path)
    comparison = _read_json(comparison_path)
    convergence = evaluate_convergence_trace(_read_json(convergence_path))
    if comparison.get("status") != "delta_safe" or comparison.get("reason_codes"):
        raise PilotError("durable pre/post snapshot comparison is not delta_safe")
    if post.get("parent_snapshot") != baseline.get("snapshot_id"):
        raise PilotError("post snapshot does not bind baseline snapshot")
    pairs = manifest.get("pairs")
    if not isinstance(pairs, list) or len(pairs) < 2:
        raise PilotError("at least two pairs are required")
    context_state = _load_context_state()
    records: list[dict[str, Any]] = []
    expected_orders = (("full", "delta"), ("delta", "full"))
    seen_rollouts: set[str] = set()
    for pair_index, pair in enumerate(pairs):
        arms = pair.get("arms") if isinstance(pair, Mapping) else None
        if not isinstance(arms, list) or tuple(arm.get("arm") for arm in arms) != expected_orders[pair_index % 2]:
            raise PilotError(f"pair {pair_index + 1} violates AB/BA order")
        pair_records = []
        for arm_entry in arms:
            rollout = (ROOT / arm_entry["rollout_path"]).resolve() if not Path(arm_entry["rollout_path"]).is_absolute() else Path(arm_entry["rollout_path"])
            rollout_key = str(rollout)
            if rollout_key in seen_rollouts:
                raise PilotError("rollout reused across arms")
            seen_rollouts.add(rollout_key)
            usage = context_state.extract_rollout_usage(rollout, expected_sha256=arm_entry["source_sha256"])
            prompt_path = Path(arm_entry["prompt_path"])
            prompt_text = prompt_path.read_text(encoding="utf-8").strip()
            if _sha256(prompt_path) != arm_entry["prompt_file_sha256"]:
                raise PilotError(f"pair {pair['pair_id']} prompt file digest mismatch")
            expected_prompt_payload = _prompt_payload_sha256(prompt_text)
            if expected_prompt_payload != arm_entry["prompt_payload_sha256_aggregate"]:
                raise PilotError(f"pair {pair['pair_id']} prompt manifest payload digest mismatch")
            if usage["prompt_payload"]["sha256_aggregate"] != expected_prompt_payload:
                raise PilotError(f"pair {pair['pair_id']} rollout prompt does not match prompt artifact")
            output = _extract_last_message(rollout)
            quality = adjudicate(output, oracle, arm_entry["arm"])
            record = {"pair_id": pair["pair_id"], "arm": arm_entry["arm"], "usage": usage, "quality": quality, "reviewer_output": output, "environment": arm_entry["environment"]}
            records.append(record)
            pair_records.append(record)
        invariants = ("model", "reasoning_effort", "cli_version", "base_instructions_sha256")
        for invariant in invariants:
            if pair_records[0]["usage"].get(invariant) != pair_records[1]["usage"].get(invariant):
                raise PilotError(f"pair {pair['pair_id']} {invariant} mismatch")
        if pair_records[0]["environment"] != pair_records[1]["environment"]:
            raise PilotError(f"pair {pair['pair_id']} environment mismatch")
    environments = [record["environment"] for record in records]
    if any(environment != environments[0] for environment in environments[1:]):
        raise PilotError("environment mismatch across paired arms")
    invariants = ("model", "reasoning_effort", "cli_version", "base_instructions_sha256")
    for invariant in invariants:
        values = {record["usage"].get(invariant) for record in records}
        if len(values) != 1:
            raise PilotError(f"usage {invariant} mismatch across pairs")
    frozen = environments[0]
    facts = baseline.get("git_observed_facts", {})
    if frozen.get("snapshot_id") != baseline.get("snapshot_id"):
        raise PilotError("environment snapshot id is not bound to durable baseline")
    if frozen.get("baseline_commit") != facts.get("baseline_commit"):
        raise PilotError("environment commit is not bound to durable baseline")
    if frozen.get("dirty_state_digest") != facts.get("dirty_state_digest"):
        raise PilotError("environment dirty digest is not bound to durable baseline")
    if post.get("git_observed_facts", {}).get("dirty_state_digest") != facts.get("dirty_state_digest"):
        raise PilotError("post snapshot dirty digest differs from baseline")
    result = summarize(records)
    return {"schema_version": "sge-pilot-report-v1", "manifest": str(manifest_path), "oracle": str(oracle_path), "convergence": convergence, "records": records, **result}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        result = evaluate_manifest(args.manifest, args.oracle)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, PilotError, ValueError) as exc:
        print(f"context-efficiency-pilot: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["classification"] != "quality_failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
