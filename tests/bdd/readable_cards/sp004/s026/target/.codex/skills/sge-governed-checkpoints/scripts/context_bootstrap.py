#!/usr/bin/env python3
"""Validate and render profile-specific task bootstrap packets."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping, NoReturn


class ContextBootstrapError(ValueError):
    """Raised when a context bootstrap packet violates the frozen contract."""


PROFILES = {"read_only", "implementation", "validation"}
TRIGGER_MODES = {"deterministic", "evidence_backed_agent_evaluated"}
SEMANTIC_ANCHORS = {"objective", "authority", "claim_ceiling", "critical_dependencies"}
VALIDATION_SURFACES = {"original objective", "acceptance criteria", "actual diff", "final state"}
CHANGE_IMPACT_FIELDS = {
    "kb_truth",
    "dashboard_state",
    "contract_or_acceptance",
    "runtime_or_schema",
    "external_side_effect",
    "semantic_risk",
    "write_conflict",
}


def fail(code: str, detail: str = "") -> NoReturn:
    suffix = f": {detail}" if detail else ""
    raise ContextBootstrapError(f"{code}{suffix}")


def require_mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        fail("invalid_packet_shape", f"{field} must be an object")
    return value


def require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail("invalid_packet_shape", f"{field} must be a non-empty string")
    return value


def require_list(value: Any, field: str, *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list) or (nonempty and not value):
        qualifier = "non-empty " if nonempty else ""
        fail("invalid_packet_shape", f"{field} must be a {qualifier}array")
    return value


def validate_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    packet = require_mapping(packet, "packet")
    required = {
        "schema_version",
        "task_id",
        "task_profile",
        "raw_user_intent",
        "intake_projection",
        "boundaries",
        "required_read_set",
        "conditional_read_set",
        "semantic_refresh",
        "epistemic_search_space",
        "change_impact",
        "topology",
        "skipped_reads",
        "validation_evidence_surfaces",
    }
    missing = sorted(required - set(packet))
    if missing:
        fail("missing_required_field", ", ".join(missing))
    if packet["schema_version"] != "context_bootstrap_v1":
        fail("unsupported_schema_version")
    require_string(packet["task_id"], "task_id")
    profile = require_string(packet["task_profile"], "task_profile")
    if profile not in PROFILES:
        fail("invalid_task_profile", profile)

    raw_intent = require_mapping(packet["raw_user_intent"], "raw_user_intent")
    intake = require_mapping(packet["intake_projection"], "intake_projection")
    require_string(raw_intent.get("text"), "raw_user_intent.text")
    require_string(intake.get("summary"), "intake_projection.summary")
    if raw_intent.get("authority_role") != "authority" or intake.get("authority_role") != "projection":
        fail("raw_intent_authority_violation")
    require_list(intake.get("assumptions"), "intake_projection.assumptions")

    boundaries = require_mapping(packet["boundaries"], "boundaries")
    write_scope = require_list(boundaries.get("write_scope"), "boundaries.write_scope")
    require_list(boundaries.get("forbidden_actions"), "boundaries.forbidden_actions")
    require_string(boundaries.get("maximum_claim"), "boundaries.maximum_claim")
    if profile == "implementation" and not write_scope:
        fail("implementation_write_scope_missing")

    reads = require_list(packet["required_read_set"], "required_read_set", nonempty=True)
    covered_domains: set[str] = set()
    for index, raw_read in enumerate(reads):
        read = require_mapping(raw_read, f"required_read_set[{index}]")
        for field in ("path", "revision", "applicability", "reason"):
            require_string(read.get(field), f"required_read_set[{index}].{field}")
        domains = require_list(read.get("domains"), f"required_read_set[{index}].domains", nonempty=True)
        for domain in domains:
            covered_domains.add(require_string(domain, f"required_read_set[{index}].domains"))

    triggers = require_list(packet["conditional_read_set"], "conditional_read_set", nonempty=True)
    trigger_modes: set[str] = set()
    for index, raw_trigger in enumerate(triggers):
        trigger = require_mapping(raw_trigger, f"conditional_read_set[{index}]")
        for field in ("trigger_id", "condition", "action"):
            require_string(trigger.get(field), f"conditional_read_set[{index}].{field}")
        mode = require_string(trigger.get("mode"), f"conditional_read_set[{index}].mode")
        if mode not in TRIGGER_MODES:
            fail("invalid_trigger_mode", mode)
        trigger_modes.add(mode)
        if trigger.get("can_suppress_deterministic") is not False:
            fail("deterministic_trigger_suppressed")
    if trigger_modes != TRIGGER_MODES:
        fail("trigger_mode_missing")

    refresh = require_mapping(packet["semantic_refresh"], "semantic_refresh")
    anchors = require_list(refresh.get("anchors"), "semantic_refresh.anchors", nonempty=True)
    if refresh.get("required_when_digest_unchanged") is not True or not SEMANTIC_ANCHORS.issubset(anchors):
        fail("semantic_refresh_missing")

    search_space = require_mapping(packet["epistemic_search_space"], "epistemic_search_space")
    required_domains = {
        require_string(value, "epistemic_search_space.required_domains")
        for value in require_list(search_space.get("required_domains"), "epistemic_search_space.required_domains", nonempty=True)
    }
    require_string(search_space.get("preservation_statement"), "epistemic_search_space.preservation_statement")
    if search_space.get("missing_evidence_action") != "expand_or_report_evidence_gap":
        fail("epistemic_search_space_narrowed")
    skipped_domains = {
        require_string(require_mapping(item, "skipped_reads[]").get("domain"), "skipped_reads[].domain")
        for item in require_list(packet["skipped_reads"], "skipped_reads")
    }
    if required_domains - covered_domains or required_domains & skipped_domains:
        fail("epistemic_search_space_narrowed")

    impact = require_mapping(packet["change_impact"], "change_impact")
    if set(impact) != CHANGE_IMPACT_FIELDS:
        fail("invalid_change_impact", "fields must match the v1 vector")
    for field in CHANGE_IMPACT_FIELDS - {"semantic_risk"}:
        if not isinstance(impact[field], bool):
            fail("invalid_change_impact", f"{field} must be boolean")
    if impact["semantic_risk"] not in {"low", "medium", "high"}:
        fail("invalid_change_impact", "semantic_risk")
    topology = require_mapping(packet["topology"], "topology")
    if topology.get("basis") != "change_impact":
        fail("topology_not_change_impact_based")
    require_string(topology.get("route"), "topology.route")
    require_string(topology.get("reason"), "topology.reason")

    surfaces = {
        require_string(value, "validation_evidence_surfaces")
        for value in require_list(packet["validation_evidence_surfaces"], "validation_evidence_surfaces")
    }
    if profile == "validation" and not VALIDATION_SURFACES.issubset(surfaces):
        fail("validation_evidence_surface_missing")
    return deepcopy(dict(packet))


def render_packet(packet: Mapping[str, Any]) -> str:
    packet = validate_packet(packet)
    boundaries = packet["boundaries"]
    lines = [
        f"# Context Bootstrap: {packet['task_id']}",
        "",
        f"Task profile: {packet['task_profile']}",
        f"Raw intent authority: {packet['raw_user_intent']['text']}",
        f"Intake projection: {packet['intake_projection']['summary']}",
        f"Maximum claim: {boundaries['maximum_claim']}",
    ]
    if boundaries["write_scope"]:
        lines.append("Write scope: " + ", ".join(boundaries["write_scope"]))
    lines.extend(["", "## Required Read Set"])
    for read in packet["required_read_set"]:
        lines.append(
            f"- {read['path']}@{read['revision']} — {read['applicability']}; {read['reason']}"
        )
    lines.extend(["", "## Conditional Read Set"])
    for trigger in packet["conditional_read_set"]:
        lines.append(
            f"- {trigger['trigger_id']} [{trigger['mode']}]: {trigger['condition']} -> {trigger['action']}"
        )
    refresh = packet["semantic_refresh"]
    lines.extend(
        [
            "",
            "## Semantic Refresh",
            "- Required even when digest is unchanged: yes",
            "- Anchors: " + ", ".join(refresh["anchors"]),
            "",
            "## Epistemic Search Space",
            "- Required domains: " + ", ".join(packet["epistemic_search_space"]["required_domains"]),
            "- Missing evidence: expand reads or report an evidence gap",
            "",
            "## Topology",
            f"- {packet['topology']['route']} (basis=change_impact): {packet['topology']['reason']}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "render"))
    parser.add_argument("packet", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = validate_packet(packet) if args.command == "validate" else render_packet(packet)
    except (OSError, json.JSONDecodeError, ContextBootstrapError) as exc:
        parser.exit(2, f"context-bootstrap: {exc}\n")
    text = (
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        if isinstance(result, dict)
        else result
    )
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
