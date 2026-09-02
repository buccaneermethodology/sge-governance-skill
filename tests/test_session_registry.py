from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "Dashboard/tools/session_registry.py"
SPEC = importlib.util.spec_from_file_location("sge_session_registry", REGISTRY_PATH)
assert SPEC and SPEC.loader
REGISTRY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = REGISTRY
SPEC.loader.exec_module(REGISTRY)

ERBE_PATH = ROOT / "Dashboard/tools/quality_recovery_erbe.py"
ERBE_SPEC = importlib.util.spec_from_file_location("sge_quality_recovery_erbe", ERBE_PATH)
assert ERBE_SPEC and ERBE_SPEC.loader
ERBE = importlib.util.module_from_spec(ERBE_SPEC)
sys.modules[ERBE_SPEC.name] = ERBE
ERBE_SPEC.loader.exec_module(ERBE)


def record(parent: str, historical_id: str, status: str, deliverable: str) -> object:
    return REGISTRY.SessionRecord(
        session_key=f"{parent}/{historical_id}",
        historical_id=historical_id,
        parent=parent,
        topic="topic",
        scope="scope",
        purpose="purpose",
        track="track",
        priority="P0",
        status=status,
        historical_status="—",
        depends_on="—",
        deliverable=deliverable,
        exit_criteria="exit",
        next_step="next",
        notes="notes",
        source_line=1,
    )


class SessionRegistryReconcileTests(unittest.TestCase):
    def test_single_apply_moves_done_record_and_stabilizes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            dashboard = repo / "Dashboard"
            archive_root = dashboard / "Archives/Sessions"
            archive_root.mkdir(parents=True)
            (archive_root / "Legacy_Execution_Notes.md").write_text("# Notes\n", encoding="utf-8")

            closing = record("SP-001", "S-012", "Doing", "[closeout](Artifacts/closeout.md)")
            remaining = record("SP-002", "S-007", "To do", "[plan](Artifacts/plan.md)")
            records = [closing, remaining]
            expected = REGISTRY.build_expected_projection(repo, records)
            for relative, content in expected.items():
                path = repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            done = replace(closing, status="Done")
            (dashboard / "Sessions.md").write_text(
                REGISTRY.render_current([done, remaining]), encoding="utf-8"
            )

            result = REGISTRY.reconcile(repo, "apply")

            self.assertEqual(result["verdict"], "pass")
            self.assertTrue(result["write_performed"])
            self.assertEqual(REGISTRY.reconcile(repo, "check")["verdict"], "pass")
            self.assertEqual(REGISTRY.validate(repo)["verdict"], "pass")
            manifest = json.loads((archive_root / "archive_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["current_count"], 1)
            self.assertEqual(manifest["archive_count"], 1)
            self.assertIn("(../../Artifacts/closeout.md)", (archive_root / "SP-001.md").read_text(encoding="utf-8"))

            reopened = replace(done, status="Doing", deliverable="[closeout](../../Artifacts/closeout.md)")
            (archive_root / "SP-001.md").write_text(
                REGISTRY.render_archive([reopened], "SP-001.md"), encoding="utf-8"
            )
            result = REGISTRY.reconcile(repo, "apply")

            self.assertEqual(result["verdict"], "pass")
            self.assertEqual(REGISTRY.reconcile(repo, "check")["verdict"], "pass")
            current_text = (dashboard / "Sessions.md").read_text(encoding="utf-8")
            self.assertIn("(Artifacts/closeout.md)", current_text)
            self.assertNotIn("(../../Artifacts/closeout.md)", current_text)


class FinalEvidenceTests(unittest.TestCase):
    def evidence(self, verdict: str) -> str:
        markers = "\n".join(ERBE.FINAL_EVIDENCE_REQUIRED_MARKERS)
        return f"# 对账\n\n## Read Manifest\n\n{markers}\n\n## 唯一 Final Verdict\n\n`final_evidence_verdict`: `{verdict}`\n"

    def test_pending_final_evidence_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "reconciliation.md"
            path.write_text(self.evidence("pending"), encoding="utf-8")
            self.assertEqual(ERBE.final_evidence_status(path), (False, "final_evidence_verdict_pending"))

    def test_blocked_final_evidence_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "reconciliation.md"
            path.write_text(self.evidence("blocked"), encoding="utf-8")
            self.assertEqual(ERBE.final_evidence_status(path), (False, "final_evidence_verdict_blocked"))

    def test_passing_final_evidence_requires_complete_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "reconciliation.md"
            path.write_text("## Read Manifest\n\n## 唯一 Final Verdict\n\n`final_evidence_verdict`: `pass`\n", encoding="utf-8")
            self.assertEqual(ERBE.final_evidence_status(path), (False, "final_evidence_binding_incomplete"))

    def test_passing_final_evidence_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "reconciliation.md"
            path.write_text(self.evidence("pass"), encoding="utf-8")
            self.assertEqual(ERBE.final_evidence_status(path), (True, "final_evidence_pass"))


if __name__ == "__main__":
    unittest.main()
