#!/usr/bin/env python3
"""Execute frozen SP-001 quality-recovery RED/GREEN cases by case identity."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


def load_doctor() -> Any:
    path = ROOT / "Dashboard/tools/doctor.py"
    spec = importlib.util.spec_from_file_location("sge_doctor", path)
    if not spec or not spec.loader:
        raise RuntimeError("doctor module unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True)


def red_identity(doctor: Any) -> str | None:
    with tempfile.TemporaryDirectory(prefix="sge-erbe-identity-") as temp_dir:
        repo = Path(temp_dir)
        (repo / "public.md").write_text("forbidden-source-identity\n", encoding="utf-8")
        scope = {
            "public_identity_patterns": ["public.md"],
            "forbidden_public_tokens": ["forbidden-source-identity"],
            "identity_exceptions": {},
        }
        return doctor.check_public_identity(repo, scope).get("fingerprint")


def red_registry() -> str | None:
    with tempfile.TemporaryDirectory(prefix="sge-erbe-registry-") as temp_dir:
        repo = Path(temp_dir)
        dashboard = repo / "Dashboard"
        (dashboard / "Archives").mkdir(parents=True)
        shutil.copy2(ROOT / "Dashboard/Sessions.md", dashboard / "Sessions.md")
        shutil.copy2(ROOT / "Dashboard/Session_Index.md", dashboard / "Session_Index.md")
        shutil.copytree(ROOT / "Dashboard/Archives/Sessions", dashboard / "Archives/Sessions")
        index = dashboard / "Session_Index.md"
        index.write_text(
            "\n".join(line for line in index.read_text(encoding="utf-8").splitlines() if "SP-001/S-012" not in line) + "\n",
            encoding="utf-8",
        )
        result = run([sys.executable, str(ROOT / "Dashboard/tools/session_registry.py"), "validate", "--repo", str(repo)], ROOT)
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            return None
        return payload.get("error_code")


def red_kb_render() -> str | None:
    with tempfile.TemporaryDirectory(prefix="sge-erbe-kb-") as temp_dir:
        kb = Path(temp_dir) / "kb"
        shutil.copytree(ROOT / "kb/data", kb / "data")
        shutil.copy2(ROOT / "kb/render_manifest_v1.json", kb / "render_manifest_v1.json")
        result = run(
            [sys.executable, str(ROOT / "kb/tools/render_kb.py"), "--data-dir", str(kb / "data"), "--manifest", str(kb / "render_manifest_v1.json"), "--check"],
            ROOT,
        )
        return "kb_render_mismatch" if result.returncode != 0 and "rendered output missing" in result.stderr else None


def red_reference(doctor: Any) -> str | None:
    with tempfile.TemporaryDirectory(prefix="sge-erbe-ref-") as temp_dir:
        repo = Path(temp_dir)
        (repo / "broken.md").write_text("[missing](absent.md)\n", encoding="utf-8")
        scope = {"markdown_patterns": ["broken.md"], "canonical_json_patterns": []}
        return doctor.check_markdown_references(repo, scope).get("fingerprint")


def red_zero_tests(doctor: Any) -> str | None:
    with tempfile.TemporaryDirectory(prefix="sge-erbe-tests-") as temp_dir:
        return doctor.discover_and_run_tests(Path(temp_dir)).get("fingerprint")


def red_final_evidence() -> str | None:
    card = ROOT / "Dashboard/Artifacts/Stage-Plan-SP-001/SP001_S012_Genericity_LaneTaskCard.json"
    result = run(
        [sys.executable, str(ROOT / ".codex/skills/sge-governed-checkpoints/scripts/lane_task_card.py"), "validate", str(card), "--repo", str(ROOT)],
        ROOT,
    )
    return "final_evidence_incomplete" if result.returncode != 0 else None


FINAL_EVIDENCE_REQUIRED_MARKERS = [
    "## Read Manifest",
    "## 唯一 Final Verdict",
    "SP001_S015_FinalClosure_Closeout.md",
    "SP001_S015_FinalClosure_OPCM.md",
    "SP001_S015_FinalValidationReview.md",
    "SP001_S015_SemanticReview.md",
    "Dashboard/Current_State.md",
    "Dashboard/Stage_Plans.md",
    "Dashboard/Sessions.md",
    "Dashboard/Session_Index.md",
    "archive_manifest.json",
    "git status",
    "git diff",
]


def final_evidence_status(path: Path) -> tuple[bool, str]:
    if not path.is_file() or path.is_symlink():
        return False, "final_evidence_missing"
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r"(?m)^`final_evidence_verdict`:\s*`(pass|blocked|pending)`\s*$", text)
    if len(matches) != 1:
        return False, "final_evidence_verdict_missing_or_ambiguous"
    if matches[0] != "pass":
        return False, f"final_evidence_verdict_{matches[0]}"
    missing_markers = [marker for marker in FINAL_EVIDENCE_REQUIRED_MARKERS if marker not in text]
    if missing_markers:
        return False, "final_evidence_binding_incomplete"
    return True, "final_evidence_pass"


def green_current(doctor: Any) -> tuple[str, dict[str, Any]]:
    doctor_report = doctor.run_doctor(ROOT, ROOT / "tests")
    required = [
        ROOT / "Dashboard/Artifacts/Stage-Plan-SP-001/SP001_S015_FinalValidationReview.md",
        ROOT / "Dashboard/Artifacts/Stage-Plan-SP-001/SP001_S015_SemanticReview.md",
        ROOT / "Dashboard/Artifacts/Stage-Plan-SP-001/SP001_S015_PostCloseoutReconciliation.md",
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    post_closeout_ok, post_closeout_reason = final_evidence_status(required[-1])
    verdict = "pass" if doctor_report["verdict"] == "pass" and not missing and post_closeout_ok else "fail"
    return verdict, {
        "doctor_verdict": doctor_report["verdict"],
        "missing_final_artifacts": missing,
        "post_closeout_evidence_verdict": post_closeout_reason,
    }


def execute(phase: str) -> dict[str, Any]:
    contract = json.loads((ROOT / "Dashboard/Artifacts/Stage-Plan-SP-001/SP001_QualityRecovery_ERBE_Contract.json").read_text(encoding="utf-8"))
    cases_doc = json.loads((ROOT / "Dashboard/Artifacts/Stage-Plan-SP-001/SP001_QualityRecovery_ERBE_Cases.json").read_text(encoding="utf-8"))
    expected = {case["case_id"]: case for case in cases_doc["cases"]}
    expected_ids = {f"QR-RED-0{number}" for number in range(1, 7)} | {"QR-GREEN-01"}
    contract_valid = contract.get("status") == "frozen" and set(expected) == expected_ids
    doctor = load_doctor()
    observed = {
        "QR-RED-01": red_identity(doctor),
        "QR-RED-02": red_registry(),
        "QR-RED-03": red_kb_render(),
        "QR-RED-04": red_reference(doctor),
        "QR-RED-05": red_zero_tests(doctor),
        "QR-RED-06": red_final_evidence(),
    }
    results: list[dict[str, Any]] = []
    red_ok = True
    for case_id, fingerprint in observed.items():
        expected_fingerprint = expected[case_id]["failure_fingerprint"]
        passed = fingerprint == expected_fingerprint
        red_ok = red_ok and passed
        results.append({"case_id": case_id, "expected": "fail", "expected_fingerprint": expected_fingerprint, "observed_fingerprint": fingerprint, "verdict": "trusted_red" if passed else "error"})
    green_verdict = "not_run"
    green_detail: dict[str, Any] = {}
    if phase == "full":
        green_verdict, green_detail = green_current(doctor)
        results.append({"case_id": "QR-GREEN-01", "expected": "pass", "verdict": green_verdict, "detail": green_detail})
    execution_ok = red_ok and (phase == "red" or green_verdict == "pass")
    return {
        "schema_version": "sp001_quality_recovery_erbe_report_v1",
        "contract_id": contract.get("contract_id"),
        "phase": phase,
        "contract_verdict": "valid" if contract_valid else "invalid",
        "execution_verdict": "ok" if execution_ok else "blocked",
        "case_results": results,
        "claim_ceiling": contract.get("claim_ceiling"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("red", "full"), required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    report = execute(args.phase)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["contract_verdict"] == "valid" and report["execution_verdict"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
