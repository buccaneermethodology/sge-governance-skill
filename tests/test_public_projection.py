from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sge_public_projection", ROOT / "tools/sge_public.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)


class PublicProjectionTests(unittest.TestCase):
    def _fixture(self, *, path="README.md", content="# public\n"):
        td = tempfile.TemporaryDirectory()
        source = Path(td.name) / "source"
        source.mkdir()
        (source / "tools").mkdir()
        shutil.copy2(ROOT / "tools/sge_public.py", source / "tools/sge_public.py")
        (source / path).parent.mkdir(parents=True, exist_ok=True)
        if content is not None:
            (source / path).write_bytes(content.encode() if isinstance(content, str) else content)
        manifest = {
            "schema_version": "sge_public_export_manifest_v1",
            "candidate_id": "fixture-candidate-v1",
            "status": "candidate_not_approved",
            "license": "MIT",
            "default_deny": True,
            "files": [{"path": path, "source": "fixture", "license": "MIT", "provenance": "test fixture", "public": True, "execution_context": False}],
            "content_policy": {"reject_absolute_home_paths": True, "reject_private_execution_directories": True},
            "layer_contract": {"install_order": ["core", "companion", "orchestrator", "domain-extension"], "mappings": [{"prefix": "", "layer": "companion", "requires": []}]},
        }
        (source / "public_export_manifest_v1.json").write_text(json.dumps(manifest), encoding="utf-8")
        return td, source

    def test_fresh_exact_projection_and_identity_metadata(self):
        td, source = self._fixture()
        try:
            destination = Path(td.name) / "destination"
            MOD.export(destination, source=source, require_clean=False)
            exported = {p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file()}
            self.assertEqual(exported - {"EXPORT_METADATA.json"}, {"README.md"})
            identity = json.loads((destination / "EXPORT_METADATA.json").read_text())["identity"]
            self.assertEqual(identity["candidate_id"], "fixture-candidate-v1")
            for field in ("source_revision", "manifest_revision", "export_tool_revision", "export_run_id"):
                self.assertTrue(identity[field])
            self.assertIsNone(identity["projection_commit"])
            self.assertIsNone(identity["release_tag"])
            metadata = json.loads((destination / "EXPORT_METADATA.json").read_text())
            self.assertEqual(metadata["file_set_sha256"], MOD._file_set_digest(["README.md"]))
            self.assertEqual(metadata["tree_sha256"], MOD._tree_digest([{"path": "README.md", "sha256": MOD._sha256_bytes(b"# public\n")}]))
            self.assertEqual(MOD.verify_projection(source, destination)["files"], ["README.md"])
        finally:
            td.cleanup()

    def test_destination_safety_unknown_and_digest_drift_fail_closed(self):
        td, source = self._fixture()
        try:
            nonempty = Path(td.name) / "nonempty"
            nonempty.mkdir()
            (nonempty / "unknown.txt").write_text("x")
            with self.assertRaisesRegex(SystemExit, "destination_must_be_empty"):
                MOD.export(nonempty, source=source, require_clean=False)
            destination = Path(td.name) / "destination"
            MOD.export(destination, source=source, require_clean=False)
            (destination / "unknown.txt").write_text("x")
            with self.assertRaisesRegex(SystemExit, "unknown_path_default_deny"):
                MOD.verify_projection(source, destination)
            (destination / "unknown.txt").unlink()
            (destination / "README.md").write_text("changed\n")
            with self.assertRaisesRegex(SystemExit, "projection_digest_drift"):
                MOD.verify_projection(source, destination)
        finally:
            td.cleanup()

    def test_residue_object_and_path_safety_fail_closed(self):
        cases = [
            ("absolute", "/Users/alice/private\n", "identity_or_private_residue"),
            ("binary", "\x00binary", "unexpected_binary"),
            ("lfs", "version https://git-lfs.github.com/spec/v1\noid sha256:" + "a" * 64 + "\nsize 1\n", "lfs_pointer_forbidden"),
        ]
        for name, content, error in cases:
            with self.subTest(name=name):
                td, source = self._fixture(content=content)
                try:
                    with self.assertRaisesRegex(SystemExit, error):
                        MOD.export(Path(td.name) / "destination", source=source, require_clean=False)
                finally:
                    td.cleanup()
        td, source = self._fixture(path="docs/link.txt", content=None)
        try:
            (source / "docs/link.txt").symlink_to("../README.md")
            with self.assertRaisesRegex(SystemExit, "unsafe_link_or_path_escape"):
                MOD.export(Path(td.name) / "destination", source=source, require_clean=False)
        finally:
            td.cleanup()

    def test_nested_repo_and_dirty_tree_are_rejected(self):
        td, source = self._fixture()
        try:
            (source / "nested/.git").mkdir(parents=True)
            with self.assertRaisesRegex(SystemExit, "nested_repo_forbidden"):
                MOD.export(Path(td.name) / "destination", source=source, require_clean=False)
        finally:
            td.cleanup()

    def test_unknown_source_file_is_default_deny(self):
        td, source = self._fixture()
        try:
            (source / "unknown.txt").write_text("not in the manifest\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "unknown_path_default_deny"):
                MOD.export(Path(td.name) / "destination", source=source, require_clean=False)
        finally:
            td.cleanup()

    def test_manifest_path_escape_destination_symlink_and_gitlink_fail_closed(self):
        td, source = self._fixture()
        try:
            manifest = json.loads((source / "public_export_manifest_v1.json").read_text())
            manifest["files"][0]["path"] = "../escape.txt"
            (source / "public_export_manifest_v1.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(SystemExit, "manifest_path_invalid"):
                MOD.export(Path(td.name) / "destination", source=source, require_clean=False)
        finally:
            td.cleanup()

        td, source = self._fixture()
        try:
            parent = Path(td.name) / "redirect"
            real = Path(td.name) / "real-parent"
            real.mkdir()
            parent.symlink_to(real, target_is_directory=True)
            with self.assertRaisesRegex(SystemExit, "destination_unsafe_link"):
                MOD.export(parent / "destination", source=source, require_clean=False)
        finally:
            td.cleanup()

        td, source = self._fixture(path="unknown.txt", content="private residue")
        try:
            # An unknown source file is not silently omitted: fresh inputs
            # must fail closed under the frozen default-deny contract.
            manifest = json.loads((source / "public_export_manifest_v1.json").read_text())
            manifest["files"] = [{"path": "README.md", "source": "fixture", "license": "MIT", "provenance": "test fixture", "public": True, "execution_context": False}]
            (source / "README.md").write_text("# public\n")
            (source / "public_export_manifest_v1.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(SystemExit, "unknown_path_default_deny"):
                MOD.export(Path(td.name) / "destination", source=source, require_clean=False)
        finally:
            td.cleanup()

        td, source = self._fixture(path="docs/escape.txt", content=None)
        try:
            (source / "docs/escape.txt").symlink_to("/etc/passwd")
            with self.assertRaisesRegex(SystemExit, "unsafe_link_or_path_escape"):
                MOD.export(Path(td.name) / "destination", source=source, require_clean=False)
        finally:
            td.cleanup()

        td, source = self._fixture()
        try:
            real = Path(td.name) / "real"
            real.mkdir()
            destination = Path(td.name) / "destination"
            destination.symlink_to(real, target_is_directory=True)
            with self.assertRaisesRegex(SystemExit, "destination_unsafe_link"):
                MOD.export(destination, source=source, require_clean=False)
        finally:
            td.cleanup()

        td, source = self._fixture()
        original = MOD._gitlink_paths
        try:
            MOD._gitlink_paths = lambda _root: {"README.md"}
            with self.assertRaisesRegex(SystemExit, "gitlink_forbidden"):
                MOD.export(Path(td.name) / "destination", source=source, require_clean=False)
        finally:
            MOD._gitlink_paths = original
            td.cleanup()
        td, source = self._fixture()
        try:
            subprocess.run(["git", "-C", str(source), "init", "-q"], check=True)
            subprocess.run(["git", "-C", str(source), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(source), "config", "user.name", "Projection Test"], check=True)
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(["git", "-C", str(source), "commit", "-qm", "fixture"], check=True)
            (source / "README.md").write_text("dirty\n")
            with self.assertRaisesRegex(SystemExit, "dirty_tree"):
                MOD.export(Path(td.name) / "destination", source=source)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
