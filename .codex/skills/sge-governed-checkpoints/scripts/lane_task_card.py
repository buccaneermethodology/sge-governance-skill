#!/usr/bin/env python3
"""Validate and render Lane Task Cards, and audit delegated prompts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional


REPO_ROOT = Path(__file__).resolve().parents[4]
CARD_VERSION = "lane_task_card_v1"
AUDIT_VERSION = "lane_prompt_audit_v1"
ROLES = {"design", "builder", "validation", "semantic", "closure"}
MODES = {"full_baseline", "delta"}
SOURCE_TYPES = {"prompt_artifact", "codex_rollout_user_messages"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MIN_LONG_BLOCK = 160
NEAR_DUPLICATE_RATIO = 0.80
RECOMMENDED_PLUGINS_ENVELOPE = re.compile(r"^\s*<recommended_plugins>")


class LaneTaskCardError(ValueError):
    pass


def fail(path: str, message: str) -> None:
    raise LaneTaskCardError(f"{path}: {message}")


def exact_keys(value: Mapping[str, Any], required: Iterable[str], path: str) -> None:
    required = set(required)
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - required)
    if missing:
        fail(path, f"missing required fields: {', '.join(missing)}")
    if unknown:
        fail(path, f"unknown fields: {', '.join(unknown)}")


def obj(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(path, "must be an object")
    return value


def text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(path, "must be a non-empty string")
    return value


def array(value: Any, path: str, *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list) or (nonempty and not value):
        fail(path, "must be a non-empty array" if nonempty else "must be an array")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_path(
    raw: Any, field: str, *, repo_root: Path = REPO_ROOT, file_required: bool = True
) -> Path:
    value = text(raw, field)
    candidate = Path(value)
    if candidate.is_absolute():
        fail(field, "must be repo-relative")
    root = repo_root.resolve()
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        fail(field, "path escapes the worktree")
    if file_required and not resolved.is_file():
        fail(field, "referenced file does not exist")
    return resolved


def validate_ref(raw: Any, field: str, *, repo_root: Path = REPO_ROOT) -> Path:
    value = obj(raw, field)
    exact_keys(value, {"path", "sha256"}, field)
    path = repo_path(value["path"], f"{field}.path", repo_root=repo_root)
    digest = text(value["sha256"], f"{field}.sha256")
    if not HEX64.fullmatch(digest):
        fail(f"{field}.sha256", "must be a lowercase SHA-256 digest")
    actual = sha256(path)
    if digest != actual:
        fail(f"{field}.sha256", f"digest drift; rebaseline required (actual {actual})")
    return path


def validate_rollout_ref(raw: Any, field: str, *, repo_root: Path) -> Path:
    value = obj(raw, field)
    exact_keys(value, {"path", "sha256"}, field)
    raw_path = Path(text(value["path"], f"{field}.path"))
    path = raw_path.resolve() if raw_path.is_absolute() else repo_path(
        value["path"], f"{field}.path", repo_root=repo_root
    )
    if not path.is_file():
        fail(f"{field}.path", "referenced rollout file does not exist")
    digest = text(value["sha256"], f"{field}.sha256")
    if not HEX64.fullmatch(digest):
        fail(f"{field}.sha256", "must be a lowercase SHA-256 digest")
    actual = sha256(path)
    if digest != actual:
        fail(f"{field}.sha256", f"digest drift; rebaseline required (actual {actual})")
    return path


def validate_string_array(raw: Any, field: str, *, nonempty: bool = False) -> list[str]:
    values = array(raw, field, nonempty=nonempty)
    for index, value in enumerate(values):
        text(value, f"{field}[{index}]")
    if len(values) != len(set(values)):
        fail(field, "items must be unique")
    return values


CARD_FIELDS = {
    "schema_version", "card_id", "session_id", "lane", "role", "source_goal",
    "base_context_refs", "mode", "snapshot", "delta_read_set",
    "acceptance_criteria_ids", "write_scope", "required_outputs",
    "maximum_claim_ref", "forbidden_claims_ref", "topology", "rebaseline_ref",
    "working_directory", "execution_command", "erbe_contract_ref",
    "erbe_case_refs", "red_evidence_ref", "frozen_inputs",
    "builder_write_exclusions", "red_identity",
}
ERBE_CARD_FIELDS = {
    "erbe_contract_ref",
    "erbe_case_refs",
    "red_evidence_ref",
    "frozen_inputs",
    "builder_write_exclusions",
    "red_identity",
}
REQUIRED_CARD_FIELDS = CARD_FIELDS - ERBE_CARD_FIELDS
ERBE_CARD_REQUIRED_FIELDS = ERBE_CARD_FIELDS
ERBE_IDENTITY_FIELDS = {
    "case_identity",
    "failure_fingerprint",
    "expected_failure_code",
    "contract_revision",
    "identity_version",
    "contract_id",
    "contract_sha256",
    "cases_sha256",
    "case_ids",
    "bundle_sha256",
}
ERBE_EXCLUSION_TOKENS = {"contract", "cases", "red", "claim_ceiling", "frozen_inputs"}


def validate_red_identity(raw: Any, field: str) -> set[str]:
    """Validate the stable identity of a RED result.

    A string is accepted for compact legacy-compatible cards.  Structured
    identities must carry the case and observed failure fingerprint so a
    status label alone cannot stand in for RED evidence.
    """
    if isinstance(raw, str):
        text(raw, field)
        return set()
    identity = obj(raw, field)
    unknown = set(identity) - ERBE_IDENTITY_FIELDS
    if unknown:
        fail(field, f"unknown fields: {', '.join(sorted(unknown))}")
    if {"identity_version", "contract_id", "contract_revision", "contract_sha256", "cases_sha256", "case_ids", "bundle_sha256"}.issubset(identity):
        for name in set(identity) - {"case_ids"}:
            text(identity[name], f"{field}.{name}")
        case_ids = identity["case_ids"]
        if not isinstance(case_ids, list) or not case_ids or not all(isinstance(item, str) and item for item in case_ids):
            fail(f"{field}.case_ids", "must be a non-empty string array")
        return set(identity)
    required = {"case_identity", "failure_fingerprint"}
    exact_keys(identity, required | (set(identity) & ERBE_IDENTITY_FIELDS), field)
    for name in required | (set(identity) & ERBE_IDENTITY_FIELDS):
        text(identity[name], f"{field}.{name}")
    return set(identity)


def validate_erbe_card(card: Mapping[str, Any], *, role: str, repo_root: Path) -> None:
    present = ERBE_CARD_FIELDS & set(card)
    if not present:
        return
    missing = sorted(ERBE_CARD_REQUIRED_FIELDS - present)
    if missing:
        fail(
            "card",
            "ERBE fields must be supplied as a complete set; missing: "
            + ", ".join(missing),
        )

    protected_paths: set[str] = set()
    for field in ("erbe_contract_ref", "red_evidence_ref"):
        protected_paths.add(
            validate_ref(card[field], f"card.{field}", repo_root=repo_root).relative_to(repo_root.resolve()).as_posix()
        )
    case_refs = array(card["erbe_case_refs"], "card.erbe_case_refs", nonempty=True)
    for index, ref in enumerate(case_refs):
        protected_paths.add(
            validate_ref(ref, f"card.erbe_case_refs[{index}]", repo_root=repo_root)
            .relative_to(repo_root.resolve())
            .as_posix()
        )
    frozen_inputs = array(card["frozen_inputs"], "card.frozen_inputs", nonempty=True)
    for index, ref in enumerate(frozen_inputs):
        protected_paths.add(
            validate_ref(ref, f"card.frozen_inputs[{index}]", repo_root=repo_root)
            .relative_to(repo_root.resolve())
            .as_posix()
        )
    validate_red_identity(card["red_identity"], "card.red_identity")

    exclusions = validate_string_array(
        card["builder_write_exclusions"],
        "card.builder_write_exclusions",
        nonempty=True,
    )
    for index, raw_path in enumerate(exclusions):
        if raw_path not in ERBE_EXCLUSION_TOKENS:
            repo_path(
                raw_path,
                f"card.builder_write_exclusions[{index}]",
                repo_root=repo_root,
                file_required=False,
            )
    symbolic_protected = set()
    if "contract" in exclusions:
        symbolic_protected.add("erbe_contract_ref")
    if "cases" in exclusions:
        symbolic_protected.add("erbe_case_refs")
    if "red" in exclusions:
        symbolic_protected.update({"red_evidence_ref", "red_identity"})
    if "frozen_inputs" in exclusions:
        symbolic_protected.add("frozen_inputs")
    path_protected = set(exclusions) & protected_paths
    if symbolic_protected:
        missing_exclusions = sorted(
            {"contract", "cases", "red", "claim_ceiling"} - set(exclusions)
        )
        if missing_exclusions:
            fail(
                "card.builder_write_exclusions",
                "symbolic exclusions must include: " + ", ".join(missing_exclusions),
            )
        missing_exclusions = []
    else:
        missing_exclusions = sorted(protected_paths - path_protected)
    if missing_exclusions:
        fail(
            "card.builder_write_exclusions",
            "must exclude every frozen ERBE input: " + ", ".join(missing_exclusions),
        )

    write_scope = set(card["write_scope"])
    overlap = sorted(write_scope & set(exclusions))
    if overlap:
        fail(
            "card.write_scope",
            "overlaps ERBE builder write exclusions: " + ", ".join(overlap),
        )
    if role == "builder" and not exclusions:
        fail("card.builder_write_exclusions", "builder requires non-empty exclusions")


def validate_card(card: Any, *, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    card = obj(card, "card")
    unknown_fields = set(card) - CARD_FIELDS
    if unknown_fields:
        fail("card", f"unknown fields: {', '.join(sorted(unknown_fields))}")
    missing_required = REQUIRED_CARD_FIELDS - set(card)
    if missing_required:
        fail("card", f"missing required fields: {', '.join(sorted(missing_required))}")
    if card["schema_version"] != CARD_VERSION:
        fail("card.schema_version", f"must be {CARD_VERSION}")
    for field in ("card_id", "session_id", "lane", "forbidden_claims_ref", "rebaseline_ref", "execution_command"):
        text(card[field], f"card.{field}")
    role = text(card["role"], "card.role")
    if role not in ROLES:
        fail("card.role", f"must be one of {sorted(ROLES)}")
    validate_ref(card["source_goal"], "card.source_goal", repo_root=repo_root)
    refs = array(card["base_context_refs"], "card.base_context_refs", nonempty=True)
    for index, ref in enumerate(refs):
        validate_ref(ref, f"card.base_context_refs[{index}]", repo_root=repo_root)
    mode = text(card["mode"], "card.mode")
    if mode not in MODES:
        fail("card.mode", f"must be one of {sorted(MODES)}")
    snapshot = obj(card["snapshot"], "card.snapshot")
    exact_keys(snapshot, {"snapshot_id", "parent_snapshot_ref"}, "card.snapshot")
    text(snapshot["snapshot_id"], "card.snapshot.snapshot_id")
    parent = snapshot["parent_snapshot_ref"]
    if parent is not None:
        repo_path(parent, "card.snapshot.parent_snapshot_ref", repo_root=repo_root)
    if mode == "delta" and parent is None:
        fail("card.snapshot.parent_snapshot_ref", "delta mode requires a parent snapshot")
    if mode == "full_baseline" and parent is not None:
        fail("card.snapshot.parent_snapshot_ref", "full_baseline must not bind a parent snapshot")
    validate_string_array(card["delta_read_set"], "card.delta_read_set", nonempty=mode == "delta")
    validate_string_array(card["acceptance_criteria_ids"], "card.acceptance_criteria_ids", nonempty=True)
    write_scope = validate_string_array(card["write_scope"], "card.write_scope")
    if role == "builder" and not write_scope:
        fail("card.write_scope", "builder requires a non-empty write scope")
    for index, raw in enumerate(write_scope):
        repo_path(raw, f"card.write_scope[{index}]", repo_root=repo_root, file_required=False)
    validate_string_array(card["required_outputs"], "card.required_outputs", nonempty=True)
    validate_erbe_card(card, role=role, repo_root=repo_root)
    claim = obj(card["maximum_claim_ref"], "card.maximum_claim_ref")
    exact_keys(claim, {"summary", "authority_ref"}, "card.maximum_claim_ref")
    text(claim["summary"], "card.maximum_claim_ref.summary")
    repo_path(claim["authority_ref"], "card.maximum_claim_ref.authority_ref", repo_root=repo_root)
    repo_path(card["forbidden_claims_ref"], "card.forbidden_claims_ref", repo_root=repo_root)
    repo_path(card["rebaseline_ref"], "card.rebaseline_ref", repo_root=repo_root)
    topology = obj(card["topology"], "card.topology")
    exact_keys(
        topology,
        {"fork_context", "user_visible_required", "user_visible", "task_id", "worktree"},
        "card.topology",
    )
    if topology["fork_context"] is not False:
        fail("card.topology.fork_context", "must be false")
    if not isinstance(topology["user_visible_required"], bool):
        fail("card.topology.user_visible_required", "must be a boolean")
    if not isinstance(topology["user_visible"], bool):
        fail("card.topology.user_visible", "must be a boolean")
    if topology["user_visible_required"] and not topology["user_visible"]:
        fail("card.topology.user_visible", "must be true when user_visible_required is true")
    text(topology["task_id"], "card.topology.task_id")
    worktree = repo_path(topology["worktree"], "card.topology.worktree", repo_root=repo_root, file_required=False)
    working = repo_path(card["working_directory"], "card.working_directory", repo_root=repo_root, file_required=False)
    if worktree != repo_root.resolve() or working != repo_root.resolve():
        fail("card.topology", "worktree and working_directory must equal the current repo root")
    return card


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LaneTaskCardError(f"{path}: invalid JSON: {exc}") from exc


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def card_digest(card: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(card)).hexdigest()


def verify_expected_card_digest(card: Mapping[str, Any], expected: Optional[str]) -> str:
    actual = card_digest(card)
    if expected is None:
        return actual
    if not HEX64.fullmatch(expected):
        fail("--expected-card-sha256", "must be a lowercase SHA-256 digest")
    if expected != actual:
        fail(
            "--expected-card-sha256",
            f"card digest mismatch (expected {expected}, actual {actual})",
        )
    return actual


def render_card(
    card_path: Path, card: Mapping[str, Any], *, repo_root: Path = REPO_ROOT
) -> str:
    digest = card_digest(card)
    relative = card_path.resolve().relative_to(repo_root.resolve()).as_posix()
    tool_relative = Path(__file__).resolve().relative_to(repo_root.resolve()).as_posix()
    erbe_line = ""
    if "erbe_contract_ref" in card:
        red_identity = card["red_identity"]
        red_label = (
            red_identity
            if isinstance(red_identity, str)
            else red_identity.get("case_identity", "structured")
        )
        erbe_line = (
            f"ERBE: contract={card['erbe_contract_ref']['path']} | "
            f"cases={len(card['erbe_case_refs'])} | "
            f"frozen_inputs={len(card['frozen_inputs'])} | RED={red_label}\n"
        )
    return (
        f"Lane Task Card: {relative}\n"
        f"Card SHA-256: {digest}\n"
        f"Verify: python3 {tool_relative} validate {relative} --repo . "
        f"--expected-card-sha256 {digest}\n"
        f"Lane: {card['lane']} | Session: {card['session_id']} | Role: {card['role']}\n"
        f"Mode: {card['mode']}\n"
        f"{erbe_line}"
        f"Working directory: {card['working_directory']}\n"
        f"Execute: {card['execution_command']}\n"
    )


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(value.split())


def blocks(value: str) -> list[str]:
    return [normalize(part) for part in re.split(r"\n\s*\n+", value) if len(normalize(part)) >= MIN_LONG_BLOCK]


def rollout_user_messages(path: Path) -> str:
    messages: list[str] = []

    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"rollout:{path}:{line_no}", f"invalid JSONL: {exc}")
        payload = event.get("payload", event)
        if payload.get("role") != "user":
            continue
        content = payload.get("content", "")
        if isinstance(content, str):
            event_messages = [content]
        elif isinstance(content, list):
            event_messages = [
                item["text"]
                for item in content
                if isinstance(item, dict)
                and item.get("type") in {"input_text", "text"}
                and isinstance(item.get("text"), str)
            ]
        else:
            event_messages = []
        if event_messages and RECOMMENDED_PLUGINS_ENVELOPE.match(event_messages[0]):
            continue
        messages.extend(event_messages)
    if not messages:
        fail(f"rollout:{path}", "contains no user messages")
    return "\n\n".join(messages)


def audit_manifest(manifest: Any, *, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    manifest = obj(manifest, "manifest")
    exact_keys(manifest, {"schema_version", "stable_sources", "prompts", "allowed_boilerplate"}, "manifest")
    if manifest["schema_version"] != AUDIT_VERSION:
        fail("manifest.schema_version", f"must be {AUDIT_VERSION}")
    stable: list[tuple[str, str]] = []
    for index, raw in enumerate(array(manifest["stable_sources"], "manifest.stable_sources")):
        path = validate_ref(raw, f"manifest.stable_sources[{index}]", repo_root=repo_root)
        stable.append((raw["path"], path.read_text(encoding="utf-8")))
    prompts: list[dict[str, str]] = []
    for index, raw in enumerate(array(manifest["prompts"], "manifest.prompts", nonempty=True)):
        field = f"manifest.prompts[{index}]"
        item = obj(raw, field)
        exact_keys(item, {"lane", "source_type", "path", "sha256"}, field)
        lane = text(item["lane"], f"{field}.lane")
        source_type = text(item["source_type"], f"{field}.source_type")
        if source_type not in SOURCE_TYPES:
            fail(f"{field}.source_type", f"must be one of {sorted(SOURCE_TYPES)}")
        ref = {"path": item["path"], "sha256": item["sha256"]}
        path = (
            validate_rollout_ref(ref, field, repo_root=repo_root)
            if source_type == "codex_rollout_user_messages"
            else validate_ref(ref, field, repo_root=repo_root)
        )
        prompt = path.read_text(encoding="utf-8") if source_type == "prompt_artifact" else rollout_user_messages(path)
        prompts.append({"lane": lane, "source": item["path"], "text": prompt})
    allowed = {normalize(v) for v in validate_string_array(manifest["allowed_boilerplate"], "manifest.allowed_boilerplate")}
    findings: list[dict[str, Any]] = []
    duplicate_chars = 0
    for prompt in prompts:
        prompt_norm = normalize(prompt["text"])
        for stable_path, stable_text in stable:
            stable_norm = normalize(stable_text)
            match = SequenceMatcher(
                None, stable_norm, prompt_norm, autojunk=False
            ).find_longest_match()
            matched_text = stable_norm[match.a : match.a + match.size]
            if match.size >= MIN_LONG_BLOCK and matched_text not in allowed:
                duplicate_chars += match.size
                findings.append({"severity": "blocking", "code": "stable_source_copy", "lane": prompt["lane"], "source": prompt["source"], "other_source": stable_path, "characters": match.size})
    prompt_blocks = [blocks(prompt["text"]) for prompt in prompts]
    for left in range(len(prompts)):
        for right in range(left + 1, len(prompts)):
            for a in prompt_blocks[left]:
                for b in prompt_blocks[right]:
                    if a == b and a not in allowed:
                        duplicate_chars += len(a)
                        findings.append({"severity": "blocking", "code": "cross_lane_exact_duplicate", "lane": prompts[left]["lane"], "source": prompts[left]["source"], "other_lane": prompts[right]["lane"], "other_source": prompts[right]["source"], "characters": len(a)})
                    else:
                        similarity = SequenceMatcher(None, a, b, autojunk=False).ratio()
                        if min(len(a), len(b)) >= MIN_LONG_BLOCK and similarity >= NEAR_DUPLICATE_RATIO:
                            findings.append({"severity": "advisory", "code": "cross_lane_near_duplicate", "lane": prompts[left]["lane"], "source": prompts[left]["source"], "other_lane": prompts[right]["lane"], "other_source": prompts[right]["source"], "similarity": round(similarity, 3)})
    # De-duplicate findings caused by a repeated source block while retaining location evidence.
    unique = list({json.dumps(finding, sort_keys=True): finding for finding in findings}.values())
    blocking = [finding for finding in unique if finding["severity"] == "blocking"]
    advisory = [finding for finding in unique if finding["severity"] == "advisory"]
    return {"schema_version": AUDIT_VERSION, "verdict": "fail" if blocking else "pass", "prompt_bytes": [{"lane": p["lane"], "source": p["source"], "bytes": len(p["text"].encode("utf-8"))} for p in prompts], "duplicate_blocks": len(blocking), "estimated_duplicate_characters": duplicate_chars, "blocking_findings": blocking, "advisory_findings": advisory}


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("validate", "render", "audit"):
        command = commands.add_parser(name)
        command.add_argument("path", type=Path)
        command.add_argument("--repo", type=Path, default=REPO_ROOT)
        command.add_argument("--output", type=Path)
        if name in {"validate", "render"}:
            command.add_argument("--expected-card-sha256")
    return root


def emit_result(result: str, output: Optional[Path], *, repo_root: Path) -> None:
    if output is None:
        print(result, end="" if result.endswith("\n") else "\n")
        return
    destination = repo_path(str(output), "--output", repo_root=repo_root, file_required=False)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(result, encoding="utf-8")


def main() -> int:
    args = parser().parse_args()
    try:
        repo_root = args.repo.resolve()
        if not repo_root.is_dir():
            fail("--repo", "must be an existing directory")
        path = args.path.resolve() if args.path.is_absolute() else (repo_root / args.path).resolve()
        path.relative_to(repo_root)
        payload = load_json(path)
        if args.command == "audit":
            report = audit_manifest(payload, repo_root=repo_root)
            emit_result(
                json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                args.output,
                repo_root=repo_root,
            )
            return 1 if report["blocking_findings"] else 0
        card = validate_card(payload, repo_root=repo_root)
        digest = verify_expected_card_digest(card, args.expected_card_sha256)
        if args.command == "validate":
            result = json.dumps(
                {"schema_version": CARD_VERSION, "verdict": "pass", "card_id": card["card_id"], "card_sha256": digest},
                sort_keys=True,
            ) + "\n"
        else:
            result = render_card(path, card, repo_root=repo_root)
        emit_result(result, args.output, repo_root=repo_root)
        return 0
    except (LaneTaskCardError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
