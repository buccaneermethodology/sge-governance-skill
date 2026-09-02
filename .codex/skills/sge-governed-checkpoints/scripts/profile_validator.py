#!/usr/bin/env python3
"""Fail-closed validator for project profile identity and authority paths."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def validate_profile(payload: dict[str, Any], *, expected_project_id: str | None = None, repo_root: Path | None = None) -> tuple[bool, str]:
    identity = payload.get("identity", {})
    project = str(identity.get("project_name", "")).lower()
    if not project:
        return False, "project_identity_missing"
    declared_id = str(payload.get("project_id", "")).lower()
    if declared_id and declared_id != project:
        return False, "project_id_mismatch"
    if expected_project_id is not None and project != expected_project_id.lower():
        return False, "project_identity_mismatch"
    roots = payload.get("roots", {})
    for key in ("kb_root", "dashboard_root", "skill_root"):
        value = roots.get(key)
        if not isinstance(value, str) or not value or Path(value).is_absolute():
            return False, "invalid_root_path"
        if ".." in Path(value).parts:
            return False, "root_path_escape"
        if repo_root is not None and not (repo_root / value).exists():
            return False, "root_missing"
    if any(".." in Path(text).parts for text in _strings(payload.get("authority", {}))):
        return False, "authority_path_escape"
    roots = payload.get("roots", {})
    for key in ("kb_root", "dashboard_root", "skill_root"):
        value = roots.get(key)
        if not isinstance(value, str) or not value or Path(value).is_absolute():
            return False, "invalid_root_path"
    authority = payload.get("authority", {})
    forbidden = {str(x).lower() for x in identity.get("forbidden_target_authority_tokens", [])}
    for text in _strings(authority):
        lowered = text.lower()
        if any(token in lowered for token in forbidden) or text.startswith("/"):
            return False, "forbidden_source_identity_or_absolute_authority"
        if ".." in Path(text).parts:
            return False, "authority_path_escape"
    return True, "ok"


def validate_path(path: Path, *, expected_project_id: str | None = None, repo_root: Path | None = None) -> tuple[bool, str]:
    return validate_profile(json.loads(path.read_text(encoding="utf-8")), expected_project_id=expected_project_id, repo_root=repo_root)
