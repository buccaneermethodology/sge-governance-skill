from __future__ import annotations

import importlib.util
import tempfile
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCTOR_PATH = ROOT / "Dashboard/tools/doctor.py"
SPEC = importlib.util.spec_from_file_location("sge_doctor", DOCTOR_PATH)
assert SPEC and SPEC.loader
DOCTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOCTOR)


class RepositoryQualityTests(unittest.TestCase):
    def test_empty_test_root_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = DOCTOR.discover_and_run_tests(Path(temp_dir))
        self.assertEqual(result["verdict"], "fail")
        self.assertEqual(result["fingerprint"], "zero_tests_discovered")

    def test_nonempty_test_root_executes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "test_smoke.py"
            path.write_text("import unittest\nclass Smoke(unittest.TestCase):\n    def test_ok(self): self.assertTrue(True)\n", encoding="utf-8")
            result = DOCTOR.discover_and_run_tests(Path(temp_dir))
        self.assertEqual(result["verdict"], "pass")
        self.assertEqual(result["discovered_count"], 1)
        self.assertEqual(result["executed_count"], 1)

    def test_public_identity_surface_is_clean(self) -> None:
        result = DOCTOR.check_public_identity(ROOT, DOCTOR.load_scope(ROOT))
        self.assertEqual(result, {"verdict": "pass", "checked_files": result["checked_files"], "findings": [], "fingerprint": None})

    def test_current_references_resolve(self) -> None:
        result = DOCTOR.check_markdown_references(ROOT, DOCTOR.load_scope(ROOT))
        self.assertEqual(result["verdict"], "pass", result["findings"])

    def test_public_policy_gates_pass(self) -> None:
        scope = DOCTOR.load_scope(ROOT)
        self.assertEqual(DOCTOR.check_public_provenance_locators(ROOT)["verdict"], "pass")
        self.assertEqual(DOCTOR.check_public_residue(ROOT)["verdict"], "pass")

    def _fixture_repo(self, text: str, *, deny_tokens=None):
        temp_dir = tempfile.TemporaryDirectory()
        repo = Path(temp_dir.name)
        (repo / "Dashboard/Archives").mkdir(parents=True)
        (repo / "Dashboard/Agent_Logs").mkdir(parents=True)
        (repo / "Dashboard/Artifacts").mkdir(parents=True)
        (repo / "README.md").write_text(text, encoding="utf-8")
        (repo / "Dashboard/reference_scope_v1.json").parent.mkdir(exist_ok=True)
        (ROOT / "Dashboard/reference_scope_v1.json").replace(repo / "Dashboard/reference_scope_v1.json") if False else None
        manifest = {
            "schema_version": "sge_public_export_manifest_v1", "candidate_id": "candidate",
            "identity_contract": {"private_source_id": "source", "public_project_id": "project", "skill_id": "skill", "roles_must_be_distinct": True},
            "provenance_locator_policy": {"allowed_types": ["in_package", "external", "private"], "private_prefixes": ["Dashboard/"], "relative_private_links": "forbidden", "unavailable_source_rule": "typed_private_or_external_only"},
            "residue_policy": {"deny_tokens_are_controls": deny_tokens if deny_tokens is not None else ["semx"], "forbidden_active_token_classes": ["product_cli", "product_kb", "product_audio"], "history_surfaces_are_private": list(DOCTOR.PRIVATE_LOCATOR_PREFIXES)},
            "files": [{"path": "README.md", "public": True, "execution_context": False}], "default_deny": True
        }
        (repo / "public_export_manifest_v1.json").write_text(json.dumps(manifest), encoding="utf-8")
        return temp_dir, repo

    def test_typed_locator_inventory_covers_private_surfaces_and_rejects_relative(self) -> None:
        self.assertEqual(set(DOCTOR.inventory_public_locators(ROOT)["protected_surfaces"][i]["prefix"] for i in range(3)), set(DOCTOR.PRIVATE_LOCATOR_PREFIXES))
        temp_dir, repo = self._fixture_repo("[history](Dashboard/Archives/S-1.md)\n")
        try:
            result = DOCTOR.check_public_provenance_locators(repo)
            self.assertEqual(result["verdict"], "fail")
            self.assertEqual(result["fingerprint"], "untyped_private_relative_locator")
            self.assertEqual(DOCTOR.resolve_typed_locator({"type": "private", "target": "Dashboard/Artifacts/a.md"}, repo=repo)["verdict"], "pass")
        finally:
            temp_dir.cleanup()

    def test_deny_token_presence_and_classification_fail_closed(self) -> None:
        temp_dir, repo = self._fixture_repo("semx is retained as a deny control\n")
        try:
            self.assertEqual(DOCTOR.check_public_residue(repo)["verdict"], "pass")
        finally:
            temp_dir.cleanup()
        temp_dir, repo = self._fixture_repo("public text\n", deny_tokens=[])
        try:
            result = DOCTOR.check_public_residue(repo)
            self.assertEqual(result["verdict"], "fail")
            self.assertIn(result["fingerprint"], {"deny_token_missing", "deny_token_presence_missing"})
        finally:
            temp_dir.cleanup()
        temp_dir, repo = self._fixture_repo("semx-cli is an active dependency\n")
        try:
            result = DOCTOR.check_public_residue(repo)
            self.assertEqual(result["verdict"], "fail")
            self.assertEqual(result["fingerprint"], "active_public_residue")
            self.assertTrue(any(row["class"] == "product_cli" for row in result["classifications"]))
        finally:
            temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
