from __future__ import annotations

import importlib.util
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
