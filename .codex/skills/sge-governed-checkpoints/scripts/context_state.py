#!/usr/bin/env python3
"""Deterministic Validation State Snapshot and rollout-usage tooling."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


SCHEMA_VERSION = "validation-state-snapshot-v1"
SHA256_LENGTH = 64
TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)
REQUIRED_SEMANTIC_DECLARATIONS = (
    "user_instruction",
    "goal",
    "governance",
    "acceptance_criteria",
    "original_objective",
    "claim_ceiling",
    "approval_authority",
    "truth_placement",
    "dependency",
    "execution_topology",
    "threat_model",
    "semantic_risk",
    "patch_consistency",
)
SEMANTIC_REASON_CODES = {
    "user_instruction": "user_instruction_changed",
    "goal": "goal_changed",
    "governance": "governance_changed",
    "acceptance_criteria": "acceptance_criteria_changed",
    "original_objective": "original_objective_changed",
    "claim_ceiling": "claim_ceiling_changed",
    "approval_authority": "approval_authority_changed",
    "truth_placement": "truth_placement_changed",
    "dependency": "dependency_changed",
    "execution_topology": "execution_topology_changed",
    "threat_model": "threat_model_changed",
    "semantic_risk": "semantic_risk_changed",
    "patch_consistency": "patch_consistency_changed",
}
SNAPSHOT_REQUIRED_FIELDS = {
    "schema_version",
    "snapshot_id",
    "parent_snapshot",
    "baseline_revision",
    "git_observed_facts",
    "semantic_declarations",
    "generated_registry",
    "critical_file_hashes",
    "validated_scope",
    "known_blockers",
    "affected_gates",
    "last_verdict",
    "reviewer_source",
    "created_at",
    "reopen_triggers",
    "collection_issues",
}
SNAPSHOT_ERBE_FIELDS = {"erbe_baseline", "erbe_delta"}
ERBE_STATE_FIELDS = {
    "contract_revision",
    "frozen_case_identities",
    "red_identity",
    "red_status",
    "green_status",
    "mutation_status",
}
ERBE_STATUS_VALUES = {
    "not_verified",
    "verified",
    "invalid",
    "killed",
    "red_verified",
    "green_verified",
    "error",
    "not_performed",
}
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


class ContextStateError(ValueError):
    """Raised when governed context evidence cannot be parsed safely."""


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_sha256(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != SHA256_LENGTH:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _is_git_oid(value: Any) -> bool:
    if not isinstance(value, str) or len(value) not in {40, 64}:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return value == value.lower()


def _normalize_erbe_identity(value: Any, field: str) -> str | dict[str, str]:
    if isinstance(value, str) and value:
        return value
    if not isinstance(value, Mapping):
        raise ContextStateError(f"{field} must be a non-empty string or object")
    unknown = set(value) - ERBE_IDENTITY_FIELDS
    if unknown:
        raise ContextStateError(
            f"{field} has unknown fields: {', '.join(sorted(unknown))}"
        )
    frozen_identity_fields = {
        "identity_version",
        "contract_id",
        "contract_revision",
        "contract_sha256",
        "cases_sha256",
        "case_ids",
        "bundle_sha256",
    }
    if frozen_identity_fields.issubset(value):
        if any(
            not isinstance(value[name], str) or not value[name]
            for name in frozen_identity_fields - {"case_ids"}
        ):
            raise ContextStateError(f"{field} frozen identity fields must be non-empty strings")
        case_ids = value["case_ids"]
        if not isinstance(case_ids, list) or not case_ids or not all(isinstance(item, str) and item for item in case_ids):
            raise ContextStateError(f"{field}.case_ids must be a non-empty string array")
        return {name: value[name] for name in sorted(value)}
    required = {"case_identity", "failure_fingerprint"}
    if not required.issubset(value):
        raise ContextStateError(
            f"{field} must contain case_identity and failure_fingerprint"
        )
    if any(not isinstance(value[name], str) or not value[name] for name in value):
        raise ContextStateError(f"{field} fields must be non-empty strings")
    return {name: value[name] for name in sorted(value)}


def _normalize_erbe_state(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContextStateError(f"{field} must be an object")
    if set(value) != ERBE_STATE_FIELDS:
        missing = sorted(ERBE_STATE_FIELDS - set(value))
        unknown = sorted(set(value) - ERBE_STATE_FIELDS)
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if unknown:
            detail.append("unknown " + ", ".join(unknown))
        raise ContextStateError(f"{field} fields do not match ERBE state: {'; '.join(detail)}")
    if not isinstance(value["contract_revision"], str) or not value["contract_revision"]:
        raise ContextStateError(f"{field}.contract_revision must be a non-empty string")
    identities = value["frozen_case_identities"]
    if (
        not isinstance(identities, list)
        or not identities
        or not all(isinstance(item, str) and item for item in identities)
        or len(identities) != len(set(identities))
    ):
        raise ContextStateError(
            f"{field}.frozen_case_identities must be a unique non-empty string array"
        )
    normalized: dict[str, Any] = {
        "contract_revision": value["contract_revision"],
        "frozen_case_identities": sorted(identities),
        "red_identity": _normalize_erbe_identity(value["red_identity"], f"{field}.red_identity"),
    }
    for name in ("red_status", "green_status", "mutation_status"):
        status = value[name]
        if status not in ERBE_STATUS_VALUES:
            raise ContextStateError(
                f"{field}.{name} must be one of {sorted(ERBE_STATUS_VALUES)}"
            )
        normalized[name] = status
    return normalized


def _git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", b"")
        if isinstance(detail, bytes):
            detail = detail.decode("utf-8", "replace").strip()
        raise ContextStateError(f"git command failed: git {' '.join(args)}: {detail}") from exc
    if binary:
        return result.stdout
    return result.stdout.decode("utf-8", "strict").strip()


def _relative_path(repo_root: Path, value: str | os.PathLike[str]) -> str:
    path = Path(value)
    if path.is_absolute():
        try:
            path = path.resolve().relative_to(repo_root)
        except ValueError as exc:
            raise ContextStateError(f"path is outside worktree: {value}") from exc
    normalized = path.as_posix()
    if normalized in ("", ".") or normalized == ".." or normalized.startswith("../"):
        raise ContextStateError(f"invalid worktree-relative path: {value}")
    return normalized


def _path_state(repo_root: Path, path: str) -> dict[str, Any]:
    candidate = repo_root / path
    if candidate.is_file() or candidate.is_symlink():
        return {"path": path, "sha256": _sha256_file(candidate)}
    return {"path": path, "sha256": None}


def _parse_porcelain_v2(repo_root: Path, raw: bytes) -> dict[str, Any]:
    tokens = raw.split(b"\0")
    tracked: list[dict[str, Any]] = []
    untracked: list[dict[str, Any]] = []
    renamed: list[dict[str, Any]] = []
    index = 0
    while index < len(tokens):
        record = tokens[index]
        index += 1
        if not record:
            continue
        text = record.decode("utf-8", "surrogateescape")
        if text.startswith("1 "):
            fields = text.split(" ", 8)
            if len(fields) != 9:
                raise ContextStateError("unrecognized git porcelain v2 ordinary record")
            state = _path_state(repo_root, fields[8])
            state.update({"status": fields[1], "kind": "tracked"})
            tracked.append(state)
        elif text.startswith("2 "):
            fields = text.split(" ", 9)
            if len(fields) != 10 or index >= len(tokens):
                raise ContextStateError("unrecognized git porcelain v2 rename record")
            old_path = tokens[index].decode("utf-8", "surrogateescape")
            index += 1
            state = _path_state(repo_root, fields[9])
            state.update(
                {
                    "old_path": old_path,
                    "status": fields[1],
                    "score": fields[8],
                    "kind": "renamed",
                }
            )
            renamed.append(state)
        elif text.startswith("? "):
            state = _path_state(repo_root, text[2:])
            state.update({"status": "??", "kind": "untracked"})
            untracked.append(state)
        elif text.startswith("! ") or text.startswith("# "):
            continue
        else:
            raise ContextStateError(f"unrecognized git porcelain v2 record: {text[:40]}")
    tracked.sort(key=lambda item: item["path"])
    untracked.sort(key=lambda item: item["path"])
    renamed.sort(key=lambda item: (item["path"], item["old_path"]))
    return {"tracked_changed": tracked, "untracked": untracked, "renamed": renamed}


def _validate_semantic_declarations(
    declarations: Mapping[str, Any],
) -> dict[str, dict[str, str]]:
    if not isinstance(declarations, Mapping):
        raise ContextStateError("semantic declarations must be an object")
    missing = sorted(set(REQUIRED_SEMANTIC_DECLARATIONS) - set(declarations))
    if missing:
        raise ContextStateError(
            "missing required semantic declarations: " + ", ".join(missing)
        )
    normalized: dict[str, dict[str, str]] = {}
    for name, declaration in declarations.items():
        if not isinstance(name, str) or not name:
            raise ContextStateError("semantic declaration names must be non-empty strings")
        if not isinstance(declaration, Mapping):
            raise ContextStateError(f"semantic declaration {name!r} must be an object")
        expected = {"ref", "revision", "sha256"}
        if set(declaration) != expected:
            raise ContextStateError(
                f"semantic declaration {name!r} must contain exactly ref, revision, sha256"
            )
        if not all(isinstance(declaration[key], str) and declaration[key] for key in expected):
            raise ContextStateError(f"semantic declaration {name!r} has an empty field")
        if not _is_sha256(declaration["sha256"]):
            raise ContextStateError(f"semantic declaration {name!r} has invalid sha256")
        normalized[name] = {key: declaration[key] for key in sorted(expected)}
    return dict(sorted(normalized.items()))


def _normalize_generated_registry(
    repo_root: Path, registry: Mapping[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(registry, Mapping):
        raise ContextStateError("generated registry must be an object")
    required = {"registry_id", "revision", "complete", "surfaces"}
    if not required.issubset(registry):
        missing = sorted(required - set(registry))
        raise ContextStateError("generated registry missing fields: " + ", ".join(missing))
    if not isinstance(registry["registry_id"], str) or not registry["registry_id"]:
        raise ContextStateError("generated registry_id must be a non-empty string")
    if not isinstance(registry["revision"], str) or not registry["revision"]:
        raise ContextStateError("generated registry revision must be a non-empty string")
    if not isinstance(registry["complete"], bool):
        raise ContextStateError("generated registry complete must be boolean")
    if not isinstance(registry["surfaces"], list):
        raise ContextStateError("generated registry surfaces must be an array")

    issues: list[str] = []
    if not registry["complete"]:
        issues.append("generated_registry_incomplete")
    surfaces: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in registry["surfaces"]:
        if not isinstance(item, Mapping) or "path" not in item:
            raise ContextStateError("each generated surface must contain path")
        path = _relative_path(repo_root, item["path"])
        if path in seen:
            raise ContextStateError(f"duplicate generated surface: {path}")
        seen.add(path)
        state = _path_state(repo_root, path)
        declared_hash = item.get("sha256")
        if declared_hash is not None:
            if not _is_sha256(declared_hash):
                raise ContextStateError(f"generated surface {path!r} has invalid sha256")
            if state["sha256"] != declared_hash:
                issues.append(f"generated_surface_hash_mismatch:{path}")
        if state["sha256"] is None:
            issues.append(f"generated_surface_missing:{path}")
        surfaces.append(state)
    surfaces.sort(key=lambda item: item["path"])
    digest_input = {
        "registry_id": registry["registry_id"],
        "revision": registry["revision"],
        "complete": registry["complete"],
        "surfaces": surfaces,
    }
    normalized = dict(digest_input)
    normalized["registry_digest"] = _sha256_bytes(_canonical_bytes(digest_input))
    return normalized, sorted(set(issues))


def collect_snapshot(
    repo: str | os.PathLike[str],
    *,
    snapshot_id: str,
    baseline_revision: str,
    semantic_declarations: Mapping[str, Any],
    generated_registry: Mapping[str, Any],
    parent_snapshot: str | None = None,
    critical_files: Sequence[str | os.PathLike[str]] = (),
    validated_scope: Sequence[str] = (),
    known_blockers: Sequence[str] = (),
    affected_gates: Sequence[str] = (),
    last_verdict: str = "blocked",
    reviewer_source: str = "unknown",
    created_at: str | None = None,
    reopen_triggers: Sequence[str] = (),
    erbe_baseline: Mapping[str, Any] | None = None,
    erbe_delta: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Collect a snapshot from Git facts plus explicit semantic inputs."""
    if not snapshot_id or not baseline_revision:
        raise ContextStateError("snapshot_id and baseline_revision are required")
    requested_repo = Path(repo).resolve()
    worktree = Path(str(_git(requested_repo, "rev-parse", "--show-toplevel"))).resolve()
    common_dir_raw = Path(str(_git(worktree, "rev-parse", "--git-common-dir")))
    common_dir = (worktree / common_dir_raw).resolve() if not common_dir_raw.is_absolute() else common_dir_raw.resolve()
    repo_root = common_dir.parent if common_dir.name == ".git" else worktree
    baseline_commit = str(_git(worktree, "rev-parse", "HEAD"))
    raw_status = _git(
        worktree,
        "status",
        "--porcelain=v2",
        "-z",
        "--untracked-files=all",
        binary=True,
    )
    assert isinstance(raw_status, bytes)
    inventory = _parse_porcelain_v2(worktree, raw_status)
    dirty_digest = _sha256_bytes(_canonical_bytes(inventory))
    semantic = _validate_semantic_declarations(semantic_declarations)
    generated, issues = _normalize_generated_registry(worktree, generated_registry)
    normalized_erbe_baseline = (
        _normalize_erbe_state(erbe_baseline, "erbe_baseline")
        if erbe_baseline is not None
        else None
    )
    if erbe_delta is not None and normalized_erbe_baseline is None:
        raise ContextStateError("erbe_delta requires erbe_baseline")
    normalized_erbe_delta = (
        _normalize_erbe_state(erbe_delta, "erbe_delta")
        if erbe_delta is not None
        else normalized_erbe_baseline
    )

    critical_hashes: dict[str, str | None] = {}
    for raw_path in critical_files:
        path = _relative_path(worktree, raw_path)
        state = _path_state(worktree, path)
        critical_hashes[path] = state["sha256"]
        if state["sha256"] is None:
            issues.append(f"critical_file_missing:{path}")

    timestamp = created_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    git_facts = {
        "repo": str(repo_root),
        "worktree": str(worktree),
        "git_common_dir": str(common_dir),
        "baseline_commit": baseline_commit,
        "dirty_state_digest": dirty_digest,
        **inventory,
    }
    result = {
        "schema_version": SCHEMA_VERSION,
        "snapshot_id": snapshot_id,
        "parent_snapshot": parent_snapshot,
        "baseline_revision": baseline_revision,
        "git_observed_facts": git_facts,
        "semantic_declarations": semantic,
        "generated_registry": generated,
        "critical_file_hashes": dict(sorted(critical_hashes.items())),
        "validated_scope": sorted(set(validated_scope)),
        "known_blockers": list(known_blockers),
        "affected_gates": sorted(set(affected_gates)),
        "last_verdict": last_verdict,
        "reviewer_source": reviewer_source,
        "created_at": timestamp,
        "reopen_triggers": sorted(set(reopen_triggers)),
        "collection_issues": sorted(set(issues)),
    }
    if normalized_erbe_baseline is not None:
        result["erbe_baseline"] = normalized_erbe_baseline
        result["erbe_delta"] = normalized_erbe_delta
    return result


def _inventory_index(snapshot: Mapping[str, Any]) -> dict[str, tuple[Any, ...]]:
    facts = snapshot.get("git_observed_facts", {})
    if not isinstance(facts, Mapping):
        raise ContextStateError("snapshot git_observed_facts must be an object")
    result: dict[str, tuple[Any, ...]] = {}
    for category in ("tracked_changed", "untracked", "renamed"):
        items = facts.get(category)
        if not isinstance(items, list):
            raise ContextStateError(f"snapshot {category} must be an array")
        for item in items:
            if not isinstance(item, Mapping) or not isinstance(item.get("path"), str):
                raise ContextStateError(f"snapshot {category} contains an invalid item")
            result[item["path"]] = (
                category,
                item.get("old_path"),
                item.get("status"),
                item.get("sha256"),
            )
    return result


def _snapshot_structure_errors(snapshot: Any) -> list[str]:
    """Validate the complete v1 comparison boundary without external packages."""
    errors: list[str] = []
    if not isinstance(snapshot, Mapping):
        return ["snapshot must be an object"]
    missing = SNAPSHOT_REQUIRED_FIELDS - set(snapshot)
    extra = set(snapshot) - SNAPSHOT_REQUIRED_FIELDS - SNAPSHOT_ERBE_FIELDS
    if missing:
        errors.append("missing fields: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("unknown fields: " + ", ".join(sorted(extra)))
    erbe_present = SNAPSHOT_ERBE_FIELDS & set(snapshot)
    if erbe_present and erbe_present != SNAPSHOT_ERBE_FIELDS:
        errors.append("ERBE snapshot requires both erbe_baseline and erbe_delta")
    if erbe_present == SNAPSHOT_ERBE_FIELDS:
        try:
            _normalize_erbe_state(snapshot.get("erbe_baseline"), "erbe_baseline")
            _normalize_erbe_state(snapshot.get("erbe_delta"), "erbe_delta")
        except ContextStateError as exc:
            errors.append(str(exc))
    if snapshot.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version is not validation-state-snapshot-v1")
    for field in ("snapshot_id", "baseline_revision", "last_verdict", "reviewer_source"):
        if not isinstance(snapshot.get(field), str) or not snapshot.get(field):
            errors.append(f"{field} must be a non-empty string")
    parent = snapshot.get("parent_snapshot")
    if parent is not None and (not isinstance(parent, str) or not parent):
        errors.append("parent_snapshot must be null or a non-empty string")
    created_at = snapshot.get("created_at")
    if not isinstance(created_at, str):
        errors.append("created_at must be a date-time string")
    else:
        try:
            datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append("created_at must be a valid date-time string")

    for field in (
        "validated_scope",
        "known_blockers",
        "affected_gates",
        "reopen_triggers",
        "collection_issues",
    ):
        value = snapshot.get(field)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"{field} must be an array of strings")
        elif len(value) != len(set(value)):
            errors.append(f"{field} must contain unique strings")

    facts = snapshot.get("git_observed_facts")
    git_fields = {
        "repo",
        "worktree",
        "git_common_dir",
        "baseline_commit",
        "dirty_state_digest",
        "tracked_changed",
        "untracked",
        "renamed",
    }
    if not isinstance(facts, Mapping):
        errors.append("git_observed_facts must be an object")
    else:
        if set(facts) != git_fields:
            errors.append("git_observed_facts fields do not match the v1 contract")
        for field in ("repo", "worktree", "git_common_dir"):
            if not isinstance(facts.get(field), str) or not facts.get(field):
                errors.append(f"git_observed_facts.{field} must be a non-empty string")
        if not _is_git_oid(facts.get("baseline_commit")):
            errors.append("git_observed_facts.baseline_commit must be a Git object id")
        if not _is_sha256(facts.get("dirty_state_digest")):
            errors.append("git_observed_facts.dirty_state_digest must be sha256")
        for category in ("tracked_changed", "untracked", "renamed"):
            items = facts.get(category)
            if not isinstance(items, list):
                errors.append(f"git_observed_facts.{category} must be an array")
                continue
            for index, item in enumerate(items):
                prefix = f"git_observed_facts.{category}[{index}]"
                required = {"path", "sha256", "status", "kind"}
                if category == "renamed":
                    required |= {"old_path", "score"}
                if not isinstance(item, Mapping) or set(item) != required:
                    errors.append(f"{prefix} fields do not match the v1 contract")
                    continue
                for field in required - {"sha256"}:
                    if not isinstance(item.get(field), str) or not item.get(field):
                        errors.append(f"{prefix}.{field} must be a non-empty string")
                expected_kind = "renamed" if category == "renamed" else (
                    "tracked" if category == "tracked_changed" else "untracked"
                )
                if item.get("kind") != expected_kind:
                    errors.append(f"{prefix}.kind is inconsistent with its inventory")
                if item.get("sha256") is not None and not _is_sha256(item.get("sha256")):
                    errors.append(f"{prefix}.sha256 must be null or sha256")

    try:
        _validate_semantic_declarations(snapshot.get("semantic_declarations"))
    except ContextStateError as exc:
        errors.append(str(exc))

    registry = snapshot.get("generated_registry")
    registry_fields = {
        "registry_id",
        "revision",
        "complete",
        "surfaces",
        "registry_digest",
    }
    if not isinstance(registry, Mapping):
        errors.append("generated_registry must be an object")
    else:
        if set(registry) != registry_fields:
            errors.append("generated_registry fields do not match the v1 contract")
        for field in ("registry_id", "revision"):
            if not isinstance(registry.get(field), str) or not registry.get(field):
                errors.append(f"generated_registry.{field} must be a non-empty string")
        if not isinstance(registry.get("complete"), bool):
            errors.append("generated_registry.complete must be boolean")
        surfaces = registry.get("surfaces")
        if not isinstance(surfaces, list):
            errors.append("generated_registry.surfaces must be an array")
        else:
            seen: set[str] = set()
            for index, item in enumerate(surfaces):
                prefix = f"generated_registry.surfaces[{index}]"
                if not isinstance(item, Mapping) or set(item) != {"path", "sha256"}:
                    errors.append(f"{prefix} fields do not match the v1 contract")
                    continue
                path = item.get("path")
                if not isinstance(path, str) or not path:
                    errors.append(f"{prefix}.path must be a non-empty string")
                elif path in seen:
                    errors.append(f"{prefix}.path is duplicated")
                else:
                    seen.add(path)
                if item.get("sha256") is not None and not _is_sha256(item.get("sha256")):
                    errors.append(f"{prefix}.sha256 must be null or sha256")
        digest = registry.get("registry_digest")
        if not _is_sha256(digest):
            errors.append("generated_registry.registry_digest must be sha256")
        elif set(registry) == registry_fields:
            digest_input = {key: registry[key] for key in registry_fields - {"registry_digest"}}
            if digest != _sha256_bytes(_canonical_bytes(digest_input)):
                errors.append("generated_registry.registry_digest does not match its content")

    critical_hashes = snapshot.get("critical_file_hashes")
    if not isinstance(critical_hashes, Mapping):
        errors.append("critical_file_hashes must be an object")
    else:
        for path, digest in critical_hashes.items():
            if not isinstance(path, str) or not path:
                errors.append("critical_file_hashes keys must be non-empty strings")
            if digest is not None and not _is_sha256(digest):
                errors.append(f"critical_file_hashes[{path!r}] must be null or sha256")
    return sorted(set(errors))


def _path_declared(path: str, delta_read_set: Sequence[str]) -> bool:
    for pattern in delta_read_set:
        if pattern.endswith("/") and path.startswith(pattern):
            return True
        if path == pattern or fnmatch.fnmatchcase(path, pattern):
            return True
    return False


def compare_snapshots(
    baseline: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    delta_read_set: Sequence[str] = (),
) -> dict[str, Any]:
    """Compare snapshots and fail closed on semantic or unregistered drift."""
    reasons: set[str] = set()
    details: list[dict[str, Any]] = []

    def add(code: str, **detail: Any) -> None:
        reasons.add(code)
        details.append({"reason_code": code, **detail})

    baseline_errors = _snapshot_structure_errors(baseline)
    current_errors = _snapshot_structure_errors(current)
    if baseline_errors:
        add("snapshot_structure_invalid", snapshot="baseline", errors=baseline_errors)
    if current_errors:
        add("snapshot_structure_invalid", snapshot="current", errors=current_errors)

    if baseline_errors or current_errors:
        return {
            "status": "rebaseline_required",
            "reason_codes": sorted(reasons),
            "drift_paths": [],
            "delta_read_set": sorted(set(delta_read_set)),
            "details": sorted(details, key=lambda item: _canonical_bytes(item)),
        }

    if baseline.get("schema_version") != SCHEMA_VERSION or current.get("schema_version") != SCHEMA_VERSION:
        add("snapshot_schema_unknown")
    if current.get("parent_snapshot") != baseline.get("snapshot_id"):
        add("snapshot_parent_mismatch")
    if current.get("baseline_revision") != baseline.get("baseline_revision"):
        add("snapshot_identity_changed", field="baseline_revision")

    old_facts = baseline.get("git_observed_facts", {})
    new_facts = current.get("git_observed_facts", {})
    for field, code in (
        ("repo", "repo_changed"),
        ("worktree", "worktree_changed"),
        ("git_common_dir", "repo_changed"),
        ("baseline_commit", "baseline_commit_changed"),
    ):
        if old_facts.get(field) != new_facts.get(field):
            add(code, field=field)

    old_semantic = baseline.get("semantic_declarations")
    new_semantic = current.get("semantic_declarations")
    if not isinstance(old_semantic, Mapping) or not isinstance(new_semantic, Mapping):
        add("semantic_declarations_missing")
    else:
        all_names = set(old_semantic) | set(new_semantic) | set(REQUIRED_SEMANTIC_DECLARATIONS)
        for name in sorted(all_names):
            if old_semantic.get(name) != new_semantic.get(name):
                add(
                    SEMANTIC_REASON_CODES.get(name, "unknown_semantic_declaration_changed"),
                    declaration=name,
                )

    old_erbe = baseline.get("erbe_baseline")
    new_erbe = current.get("erbe_baseline")
    old_delta = baseline.get("erbe_delta")
    new_delta = current.get("erbe_delta")
    erbe_changed_fields: list[str] = []
    if (old_erbe is None) != (new_erbe is None):
        add("erbe_state_missing")
    elif old_erbe is not None and old_erbe != new_erbe:
        add("erbe_baseline_changed")
        erbe_changed_fields.extend(
            name for name in sorted(ERBE_STATE_FIELDS) if old_erbe.get(name) != new_erbe.get(name)
        )
    if old_delta is not None and new_delta is not None:
        for name in sorted(ERBE_STATE_FIELDS):
            if old_delta.get(name) != new_delta.get(name):
                erbe_changed_fields.append(f"delta.{name}")
        if old_delta.get("contract_revision") != new_delta.get("contract_revision"):
            add("erbe_contract_revision_changed")
        if old_delta.get("frozen_case_identities") != new_delta.get("frozen_case_identities"):
            add("erbe_case_identity_changed")
        if old_delta.get("red_identity") != new_delta.get("red_identity"):
            add("erbe_red_identity_changed")
    elif (old_delta is None) != (new_delta is None):
        add("erbe_delta_missing")
    if old_erbe is not None and new_delta is not None:
        for name, code in (
            ("contract_revision", "erbe_contract_revision_changed"),
            ("frozen_case_identities", "erbe_case_identity_changed"),
            ("red_identity", "erbe_red_identity_changed"),
        ):
            if old_erbe.get(name) != new_delta.get(name):
                add(code)

    old_registry = baseline.get("generated_registry")
    new_registry = current.get("generated_registry")
    if not isinstance(new_registry, Mapping) or not new_registry.get("complete"):
        add("generated_registry_incomplete")
    if old_registry != new_registry:
        add("generated_registry_changed")

    if baseline.get("critical_file_hashes") != current.get("critical_file_hashes"):
        add("critical_file_hash_changed")
    for issue in current.get("collection_issues", ["collection_issues_missing"]):
        add("collection_issue", issue=issue)

    try:
        old_inventory = _inventory_index(baseline)
        new_inventory = _inventory_index(current)
    except ContextStateError as exc:
        add("snapshot_structure_invalid", error=str(exc))
        old_inventory = {}
        new_inventory = {}
    drift_paths = sorted(
        path
        for path in set(old_inventory) | set(new_inventory)
        if old_inventory.get(path) != new_inventory.get(path)
    )
    outside_delta = [path for path in drift_paths if not _path_declared(path, delta_read_set)]
    if outside_delta:
        add("final_diff_outside_delta_read_set", paths=outside_delta)
        add("unknown_drift", paths=outside_delta)
    for path in drift_paths:
        category = new_inventory.get(path, old_inventory.get(path, (None,)))[0]
        if category == "untracked" and path not in old_inventory and not _path_declared(path, delta_read_set):
            add("unregistered_untracked_surface", path=path)
        if category == "renamed" and old_inventory.get(path) != new_inventory.get(path) and not _path_declared(path, delta_read_set):
            add("unregistered_renamed_surface", path=path)

    if drift_paths and not current.get("affected_gates"):
        add("affected_gates_indeterminate")

    ordered_details = sorted(details, key=lambda item: _canonical_bytes(item))
    return {
        "status": "rebaseline_required" if reasons else "delta_safe",
        "reason_codes": sorted(reasons),
        "drift_paths": drift_paths,
        "delta_read_set": sorted(set(delta_read_set)),
        "erbe_delta": {
            "changed_fields": sorted(set(erbe_changed_fields)),
            "rebaseline_required": bool(reasons & {
                "erbe_state_missing",
                "erbe_delta_missing",
                "erbe_baseline_changed",
                "erbe_contract_revision_changed",
                "erbe_case_identity_changed",
                "erbe_red_identity_changed",
            }),
        },
        "details": ordered_details,
    }


def _text_payloads(value: Any, *, strict_tool_output: bool = False) -> list[str]:
    if isinstance(value, str):
        return [value]
    if not isinstance(value, list):
        if strict_tool_output:
            raise ContextStateError("unrecognized structured tool output carrier")
        return []
    texts: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            if strict_tool_output:
                raise ContextStateError(f"unrecognized tool output item at index {index}")
            continue
        kind = item.get("type")
        if kind in {"input_text", "output_text", "text"}:
            if not isinstance(item.get("text"), str):
                if strict_tool_output:
                    raise ContextStateError(
                        f"tool output text item at index {index} has no text"
                    )
                continue
            texts.append(item["text"])
        elif kind not in {"image", "image_url"} and strict_tool_output:
            raise ContextStateError(
                f"unrecognized structured tool output type at index {index}: {kind!r}"
            )
    return texts


def _require_matching_event_turn(
    event: Mapping[str, Any], expected_turn_id: str, event_kind: str
) -> None:
    payload = event.get("payload")
    if not isinstance(payload, Mapping):
        raise ContextStateError(f"{event_kind} payload must be an object")
    explicit_ids: list[Any] = []
    if "turn_id" in event:
        explicit_ids.append(event["turn_id"])
    if "turn_id" in payload:
        explicit_ids.append(payload["turn_id"])
    info = payload.get("info")
    if isinstance(info, Mapping) and "turn_id" in info:
        explicit_ids.append(info["turn_id"])
    metadata = payload.get("internal_chat_message_metadata_passthrough")
    if isinstance(metadata, Mapping) and "turn_id" in metadata:
        explicit_ids.append(metadata["turn_id"])
    if any(turn_id != expected_turn_id for turn_id in explicit_ids):
        raise ContextStateError(f"{event_kind} turn_id does not match turn_context")


def _payload_metric(texts: Iterable[str], extraction_rule: str) -> dict[str, Any]:
    encoded = [text.encode("utf-8") for text in texts]
    framed = b"".join(len(item).to_bytes(8, "big") + item for item in encoded)
    return {
        "bytes": sum(len(item) for item in encoded),
        "item_count": len(encoded),
        "sha256_aggregate": _sha256_bytes(framed),
        "extraction_rule": extraction_rule,
    }


def extract_rollout_usage(
    rollout_path: str | os.PathLike[str], *, expected_sha256: str | None = None
) -> dict[str, Any]:
    """Extract final model-reported usage from one fresh, completed turn."""
    path = Path(rollout_path)
    source = path.read_bytes()
    source_sha256 = _sha256_bytes(source)
    if expected_sha256 is not None:
        if not _is_sha256(expected_sha256) or source_sha256 != expected_sha256.lower():
            raise ContextStateError("rollout source sha256 mismatch")

    events: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(source.splitlines(), 1):
        if not raw_line.strip():
            continue
        try:
            event = json.loads(raw_line)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ContextStateError(f"invalid rollout JSON at line {line_number}") from exc
        if not isinstance(event, dict):
            raise ContextStateError(f"rollout line {line_number} is not an object")
        events.append(event)

    session_events = [event for event in events if event.get("type") == "session_meta"]
    turn_events = [event for event in events if event.get("type") == "turn_context"]
    complete_events = [
        event
        for event in events
        if event.get("type") == "event_msg"
        and event.get("payload", {}).get("type") == "task_complete"
    ]
    if len(session_events) != 1:
        raise ContextStateError("rollout must contain exactly one session_meta")
    if len(turn_events) != 1:
        raise ContextStateError("rollout must contain exactly one turn_context")
    if len(complete_events) != 1:
        raise ContextStateError("rollout must contain exactly one task_complete")

    session = session_events[0].get("payload", {})
    turn = turn_events[0].get("payload", {})
    complete = complete_events[0].get("payload", {})
    turn_id = turn.get("turn_id")
    if not isinstance(turn_id, str) or not turn_id:
        raise ContextStateError("turn_context is missing turn_id")
    if complete.get("turn_id") != turn_id:
        raise ContextStateError("task_complete does not match turn_context")

    complete_index = events.index(complete_events[0])
    if any(
        event.get("type") in {"turn_context", "response_item", "event_msg"}
        for event in events[complete_index + 1 :]
    ):
        raise ContextStateError("task_complete is not terminal")

    turn_index = events.index(turn_events[0])
    if turn_index >= complete_index:
        raise ContextStateError("turn_context occurs after task_complete")
    user_messages: list[dict[str, Any]] = []
    for event in events[turn_index + 1 : complete_index]:
        payload = event.get("payload", {})
        if event.get("type") != "response_item" or payload.get("type") != "message" or payload.get("role") != "user":
            continue
        metadata = payload.get("internal_chat_message_metadata_passthrough", {})
        if metadata.get("turn_id") == turn_id:
            user_messages.append(payload)
    if len(user_messages) != 1:
        raise ContextStateError("rollout must contain exactly one user message for the turn")
    prompt_texts = _text_payloads(user_messages[0].get("content"))
    if not prompt_texts:
        raise ContextStateError("turn user message has no textual prompt payload")

    token_events: list[dict[str, int]] = []
    tool_texts: list[str] = []
    for event in events[turn_index + 1 : complete_index]:
        payload = event.get("payload", {})
        if event.get("type") == "event_msg" and payload.get("type") == "token_count":
            _require_matching_event_turn(event, turn_id, "token_count")
            info = payload.get("info")
            if not isinstance(info, Mapping):
                raise ContextStateError("token_count is missing usage info")
            usage = info.get("total_token_usage")
            if not isinstance(usage, Mapping):
                raise ContextStateError("token_count is missing cumulative total_token_usage")
            normalized: dict[str, int] = {}
            for field in TOKEN_FIELDS:
                value = usage.get(field)
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    raise ContextStateError(f"token_count has invalid {field}")
                normalized[field] = value
            if normalized["cached_input_tokens"] > normalized["input_tokens"]:
                raise ContextStateError("cached input tokens exceed input tokens")
            if normalized["reasoning_output_tokens"] > normalized["output_tokens"]:
                raise ContextStateError("reasoning output tokens exceed output tokens")
            if normalized["total_tokens"] != normalized["input_tokens"] + normalized["output_tokens"]:
                raise ContextStateError("model total_tokens is inconsistent with input plus output")
            if token_events and any(normalized[field] < token_events[-1][field] for field in TOKEN_FIELDS):
                raise ContextStateError("token_count events are not monotonic")
            token_events.append(normalized)
        if event.get("type") == "response_item" and payload.get("type") in {
            "custom_tool_call_output",
            "function_call_output",
        }:
            _require_matching_event_turn(event, turn_id, "tool output")
            tool_texts.extend(
                _text_payloads(payload.get("output"), strict_tool_output=True)
            )
    if not token_events:
        raise ContextStateError("rollout has no token_count before task_complete")

    if not all(isinstance(session.get(field), str) and session.get(field) for field in ("id", "cli_version")):
        raise ContextStateError("session_meta is missing id or cli_version")
    if not all(isinstance(turn.get(field), str) and turn.get(field) for field in ("model", "effort")):
        raise ContextStateError("turn_context is missing model or effort")

    final_usage = dict(token_events[-1])
    final_usage["uncached_input_tokens"] = (
        final_usage["input_tokens"] - final_usage["cached_input_tokens"]
    )
    base_instructions = session.get("base_instructions", {}).get("text")
    base_digest = _sha256_bytes(base_instructions.encode("utf-8")) if isinstance(base_instructions, str) else None
    return {
        "source_path": str(path.resolve()),
        "source_sha256": source_sha256,
        "session_id": session["id"],
        "parent_session_id": session.get("session_id"),
        "turn_id": turn_id,
        "model": turn["model"],
        "reasoning_effort": turn["effort"],
        "cli_version": session["cli_version"],
        "model_provider": session.get("model_provider"),
        "originator": session.get("originator"),
        "thread_source": session.get("thread_source"),
        "base_instructions_sha256": base_digest,
        "terminal_status": "task_complete",
        "completed_at": complete.get("completed_at"),
        "token_event_count": len(token_events),
        "model_reported_usage": final_usage,
        "prompt_payload": _payload_metric(
            prompt_texts,
            "UTF-8 bytes of input_text items in the single matching user message",
        ),
        "tool_output_payload": _payload_metric(
            tool_texts,
            "UTF-8 bytes of textual items in tool output response_items before task_complete",
        ),
    }


def _read_json(path: str | os.PathLike[str]) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContextStateError(f"cannot read JSON from {path}: {exc}") from exc


def _write_result(value: Any, output: str | None) -> None:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if output:
        Path(output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect = subparsers.add_parser("collect", help="collect a Validation State Snapshot")
    collect.add_argument("--repo", default=".")
    collect.add_argument("--snapshot-id", required=True)
    collect.add_argument("--baseline-revision", required=True)
    collect.add_argument("--parent-snapshot")
    collect.add_argument("--semantic-declarations", required=True)
    collect.add_argument("--generated-registry", required=True)
    collect.add_argument("--metadata", help="optional validation metadata JSON")
    collect.add_argument("--critical-file", action="append", default=[])
    collect.add_argument("--output")

    compare = subparsers.add_parser("compare", help="compare snapshots")
    compare.add_argument("baseline")
    compare.add_argument("current")
    compare.add_argument("--delta-read-set", help="JSON array of paths/patterns")
    compare.add_argument("--output")

    usage = subparsers.add_parser("usage", help="extract fresh single-turn rollout usage")
    usage.add_argument("rollout")
    usage.add_argument("--expected-sha256")
    usage.add_argument("--output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "collect":
            metadata = _read_json(args.metadata) if args.metadata else {}
            if not isinstance(metadata, dict):
                raise ContextStateError("metadata must be a JSON object")
            result = collect_snapshot(
                args.repo,
                snapshot_id=args.snapshot_id,
                baseline_revision=args.baseline_revision,
                parent_snapshot=args.parent_snapshot,
                semantic_declarations=_read_json(args.semantic_declarations),
                generated_registry=_read_json(args.generated_registry),
                critical_files=args.critical_file,
                **metadata,
            )
            output = args.output
        elif args.command == "compare":
            delta_read_set = _read_json(args.delta_read_set) if args.delta_read_set else []
            if not isinstance(delta_read_set, list) or not all(isinstance(item, str) for item in delta_read_set):
                raise ContextStateError("delta read set must be a JSON array of strings")
            result = compare_snapshots(
                _read_json(args.baseline),
                _read_json(args.current),
                delta_read_set=delta_read_set,
            )
            output = args.output
        else:
            result = extract_rollout_usage(args.rollout, expected_sha256=args.expected_sha256)
            output = args.output
        _write_result(result, output)
    except ContextStateError as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
