from __future__ import annotations
import importlib.util, json, re, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("sge_public", ROOT/"tools/sge_public.py")
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

class PublicCandidateTests(unittest.TestCase):
    def test_public_manifest_carries_no_concrete_private_identity(self):
        text=(ROOT/"public_export_manifest_v1.json").read_text(encoding="utf-8").lower()
        for token in ("/users/xiaomei","semx-cli","semx-kb","s-384","s-485","audio-transcriptor"):
            self.assertNotIn(token,text)

    def test_newcomer_docs_cover_full_lifecycle(self):
        docs=((ROOT/"docs/Beginner_Guide_CN.md").read_text(encoding="utf-8")+"\n"+(ROOT/"docs/Quick_Start_CN.md").read_text(encoding="utf-8"))
        for command in ("doctor","export","bootstrap","install","upgrade","uninstall"):
            self.assertIn(f"sge_public.py {command}", docs)
        self.assertIn(".sge-backups", docs)
        self.assertIn(".sge-trash", docs)

    def test_manifest_and_export_are_default_deny(self):
        data=MOD.load(); allowed=MOD.validate(data)
        self.assertTrue(data["default_deny"]); self.assertNotIn("Dashboard/Sessions.md", allowed)
        with tempfile.TemporaryDirectory() as td:
            dest=Path(td); MOD.export(dest, require_clean=False)
            exported={p.relative_to(dest).as_posix() for p in dest.rglob("*") if p.is_file()}
            self.assertEqual(exported-{"EXPORT_METADATA.json"}, allowed)

    def test_identity_locator_and_residue_policy_is_explicit(self):
        data = MOD.load()
        identity = data["identity_contract"]
        self.assertTrue(identity["roles_must_be_distinct"])
        self.assertEqual(len({identity["private_source_id"], identity["public_project_id"], identity["skill_id"], data["candidate_id"]}), 4)
        self.assertEqual(data["provenance_locator_policy"]["relative_private_links"], "forbidden")
        self.assertIn("semx", data["residue_policy"]["deny_tokens_are_controls"])

    def test_quick_start_bash_fences_are_shell_only(self):
        text = (ROOT / "docs/Quick_Start_CN.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```bash\n(.*?)```", text, flags=re.S)
        self.assertTrue(blocks)
        for block in blocks:
            shell_prefixes = ("python3 ", "find ", "cd ", "#")
            self.assertFalse(any(line.strip() and not line.lstrip().startswith(shell_prefixes) for line in block.splitlines()))

    def test_four_layer_contract_blocks_core_dependency_collapse(self):
        data=json.loads(json.dumps(MOD.load()))
        data["layer_contract"]["mappings"][0]["requires"]=["domain-extension"]
        with self.assertRaises(SystemExit) as cm: MOD.validate(data)
        self.assertIn("core_dependency_collapse",str(cm.exception))

    def test_extension_contract_is_explicit_and_optional(self):
        registry=json.loads((ROOT/"extensions/registry_v1.json").read_text(encoding="utf-8"))
        self.assertFalse(registry["core_requires_extensions"])
        for item in registry["extensions"]:
            self.assertFalse(item["enabled_by_default"]); self.assertIn("provenance_ref",item); self.assertIn("missing_behavior",item)

    def test_absolute_path_and_private_residue_fail(self):
        data=MOD.load(); bad=json.loads(json.dumps(data)); bad["files"][0]["path"]="/tmp/no"
        with self.assertRaises(SystemExit) as cm: MOD.validate(bad)
        self.assertIn("manifest_path_invalid", str(cm.exception))
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/"bad.txt").write_text("/Users/alice/private", encoding="utf-8")
            old=MOD.ROOT; MOD.ROOT=root
            try:
                case=json.loads(json.dumps(MOD.load())); case["files"]=[{"path":"bad.txt","source":"fixture","license":"MIT","provenance":"test fixture","public":True,"execution_context":False}]
                with self.assertRaises(SystemExit) as cm2: MOD.validate(case)
                self.assertIn("private", str(cm2.exception))
            finally: MOD.ROOT=old

    def test_lifecycle_is_recoverable_and_preserves_authority(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/"consumer"; MOD.bootstrap(target)
            original=(target/"AGENTS.md").read_text(encoding="utf-8")
            MOD.install(ROOT,target); self.assertTrue((target/".codex/skills/sge-governed-checkpoints/SKILL.md").is_file())
            MOD.install(ROOT,target,upgrade=True); self.assertTrue(any((target/".sge-backups").rglob("SKILL.md")))
            MOD.uninstall(target); self.assertFalse((target/".codex/skills/sge-governed-checkpoints").exists())
            self.assertTrue(any((target/".sge-trash").rglob("SKILL.md")))
            self.assertEqual((target/"AGENTS.md").read_text(encoding="utf-8"), original)

    def test_nonempty_bootstrap_and_unmanaged_uninstall_fail(self):
        with tempfile.TemporaryDirectory() as td:
            target=Path(td); (target/"keep").write_text("x")
            with self.assertRaises(SystemExit) as cm: MOD.bootstrap(target)
            self.assertEqual(str(cm.exception),"destination_must_be_empty")
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(SystemExit) as cm: MOD.uninstall(Path(td))
            self.assertEqual(str(cm.exception),"uninstall_requires_install_record")

if __name__ == "__main__": unittest.main()
