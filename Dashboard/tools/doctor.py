#!/usr/bin/env python3
"""Fail-closed repo-local acceptance entry for SGE Governance quality."""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Iterable


MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REPO_PATH_PREFIXES = ("AGENTS.md", "README.md", ".codex/", "kb/", "Dashboard/", "tests/")
def _run(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "verdict": "pass" if result.returncode == 0 else "fail",
    }


def _expand(repo: Path, patterns: Iterable[str]) -> list[Path]:
    paths: set[Path] = set()
    for pattern in patterns:
        paths.update(path for path in repo.glob(pattern) if path.is_file())
    return sorted(paths)


def load_scope(repo: Path) -> dict[str, Any]:
    path = repo / "Dashboard/reference_scope_v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "sge_reference_scope_v1":
        raise ValueError("unsupported reference scope schema")
    return data


def check_markdown_references(repo: Path, scope: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    checked = 0
    for path in _expand(repo, scope["markdown_patterns"]):
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for match in MARKDOWN_LINK_RE.finditer(line):
                target = match.group(1).strip().strip("<>")
                if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                    continue
                checked += 1
                target_path = target.split("#", 1)[0]
                if not target_path:
                    continue
                if target_path.startswith("/"):
                    findings.append({"file": path.relative_to(repo).as_posix(), "line": line_no, "target": target, "fingerprint": "absolute_reference_forbidden"})
                    continue
                resolved = (path.parent / target_path).resolve()
                try:
                    resolved.relative_to(repo)
                except ValueError:
                    findings.append({"file": path.relative_to(repo).as_posix(), "line": line_no, "target": target, "fingerprint": "reference_escapes_repo"})
                    continue
                if not resolved.exists():
                    findings.append({"file": path.relative_to(repo).as_posix(), "line": line_no, "target": target, "fingerprint": "reference_missing"})

    render_docs: dict[str, dict[str, Any]] = {}
    for path in _expand(repo, scope["canonical_json_patterns"]):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data.get("doc_id"), str):
            render_docs[data["doc_id"]] = data
    for doc_id, data in render_docs.items():
        source_file = next(
            path for path in _expand(repo, scope["canonical_json_patterns"])
            if json.loads(path.read_text(encoding="utf-8")).get("doc_id") == doc_id
        )
        for target in data.get("metadata", {}).get("source_scope", []):
            if not isinstance(target, str) or not target.startswith(REPO_PATH_PREFIXES):
                continue
            checked += 1
            if not (repo / target).exists():
                findings.append({"file": source_file.relative_to(repo).as_posix(), "target": target, "fingerprint": "canonical_source_missing"})
        for dependency in data.get("metadata", {}).get("depends_on_docs", []):
            checked += 1
            if dependency not in render_docs:
                findings.append({"file": source_file.relative_to(repo).as_posix(), "target": dependency, "fingerprint": "canonical_dependency_missing"})
    return {"verdict": "pass" if not findings else "fail", "checked_references": checked, "findings": findings, "fingerprint": None if not findings else "reference_missing"}


def check_public_identity(repo: Path, scope: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    exceptions = scope.get("identity_exceptions", {})
    files = _expand(repo, scope["public_identity_patterns"])
    for path in files:
        relative = path.relative_to(repo).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        allowed = set(exceptions.get(relative, []))
        for token in scope["forbidden_public_tokens"]:
            if token in allowed:
                continue
            if token.lower() in text.lower():
                findings.append({"file": relative, "token": token, "fingerprint": "active_identity_residue"})
    return {"verdict": "pass" if not findings else "fail", "checked_files": len(files), "findings": findings, "fingerprint": None if not findings else "active_identity_residue"}


def discover_and_run_tests(tests_root: Path) -> dict[str, Any]:
    suite = unittest.defaultTestLoader.discover(
        str(tests_root), pattern="test_*.py", top_level_dir=str(tests_root)
    )
    discovered = suite.countTestCases()
    if discovered == 0:
        return {"verdict": "fail", "discovered_count": 0, "executed_count": 0, "fingerprint": "zero_tests_discovered", "output": ""}
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "verdict": "pass" if result.wasSuccessful() else "fail",
        "discovered_count": discovered,
        "executed_count": result.testsRun,
        "fingerprint": None if result.wasSuccessful() else "tests_failed",
        "output": stream.getvalue(),
    }


def check_json_and_python(repo: Path) -> dict[str, Any]:
    findings: list[str] = []
    json_count = 0
    python_count = 0
    for path in repo.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        try:
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
                json_count += 1
            elif path.suffix == ".py":
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
                python_count += 1
        except Exception as exc:  # fail closed with the concrete path.
            findings.append(f"{path.relative_to(repo)}: {exc}")
    return {"verdict": "pass" if not findings else "fail", "json_count": json_count, "python_count": python_count, "findings": findings, "fingerprint": None if not findings else "parse_or_compile_failed"}


def run_doctor(repo: Path, tests_root: Path) -> dict[str, Any]:
    scope = load_scope(repo)
    gates: dict[str, Any] = {
        "parse_compile": check_json_and_python(repo),
        "references": check_markdown_references(repo, scope),
        "public_identity": check_public_identity(repo, scope),
        "tests": discover_and_run_tests(tests_root),
        "genericity": _run([sys.executable, "tests/contract/sge_skill_generality.py"], repo),
        "registry_check": _run([sys.executable, "Dashboard/tools/session_registry.py", "reconcile", "--repo", ".", "--check"], repo),
        "registry_validate": _run([sys.executable, "Dashboard/tools/session_registry.py", "validate", "--repo", "."], repo),
        "kb_render_check": _run([sys.executable, "kb/tools/render_kb.py", "--check"], repo),
        "quality_recovery_erbe_red": _run([sys.executable, "Dashboard/tools/quality_recovery_erbe.py", "--phase", "red"], repo),
    }
    with tempfile.TemporaryDirectory(prefix="sge-doctor-") as temp_dir:
        temp = Path(temp_dir)
        gates["dkg_generate"] = _run(
            [sys.executable, "Dashboard/tools/generate_dashboard_kg.py", "--repo-root", ".", "--quality-metrics", "none", "--out", str(temp / "dkg.json"), "--query-report", str(temp / "query.md"), "--created-by-session", "sge-doctor"],
            repo,
        )
    failed = [name for name, result in gates.items() if result.get("verdict") != "pass"]
    return {"schema_version": "sge_repository_doctor_v1", "verdict": "pass" if not failed else "fail", "failed_gates": failed, "gates": gates}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--tests-root", default="tests")
    parser.add_argument("--json-out")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    tests_root = (repo / args.tests_root).resolve()
    report = run_doctor(repo, tests_root)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.json_out:
        Path(args.json_out).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
