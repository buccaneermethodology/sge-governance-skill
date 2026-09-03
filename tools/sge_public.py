#!/usr/bin/env python3
"""Default-deny public candidate export and reversible lifecycle checks."""
from __future__ import annotations
import argparse, datetime, hashlib, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "public_export_manifest_v1.json"

def load():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != "sge_public_export_manifest_v1" or data.get("default_deny") is not True:
        raise SystemExit("manifest_invalid")
    return data

def validate(data):
    layers=data.get("layer_contract", {})
    if layers.get("install_order") != ["core","companion","orchestrator","domain-extension"]:
        raise SystemExit("layer_contract_invalid:install_order")
    mappings=layers.get("mappings", [])
    if not mappings or mappings[-1].get("prefix") != "": raise SystemExit("layer_contract_invalid:catchall")
    allowed_layers=set(layers["install_order"])
    seen = set()
    for item in data["files"]:
        path = item["path"]
        if path in seen or Path(path).is_absolute() or ".." in Path(path).parts:
            raise SystemExit(f"manifest_path_invalid:{path}")
        seen.add(path)
        if not item.get("public") or item.get("execution_context"):
            raise SystemExit(f"manifest_policy_invalid:{path}")
        if item.get("license") != data["license"]:
            raise SystemExit(f"license_missing:{path}")
        source = ROOT / path
        if not source.is_file():
            raise SystemExit(f"source_missing:{path}")
        mapping=next((rule for rule in mappings if path.startswith(rule.get("prefix",""))),None)
        if not mapping or mapping.get("layer") not in allowed_layers: raise SystemExit(f"layer_unresolved:{path}")
        if mapping["layer"]=="core" and mapping.get("requires"): raise SystemExit(f"core_dependency_collapse:{path}")
        if any(dep not in allowed_layers for dep in mapping.get("requires",[])): raise SystemExit(f"layer_dependency_unknown:{path}")
        text = source.read_text(encoding="utf-8", errors="replace").lower()
        policy=data.get("content_policy", {})
        if policy.get("reject_absolute_home_paths") and re.search(r"/(?:users|home)/[^/\s\"']+", text):
            raise SystemExit(f"identity_or_private_residue:{path}:absolute_home_path")
        if policy.get("reject_private_execution_directories") and Path(path).parts and Path(path).parts[0] in {"Dashboard", ".git"}:
            raise SystemExit(f"private_surface_forbidden:{path}")
    registry=ROOT/"extensions/registry_v1.json"
    if registry.is_file() and "extensions/registry_v1.json" in seen:
        ext=json.loads(registry.read_text(encoding="utf-8")); ids=set()
        required={"id","kind","contract_version","enabled_by_default","entrypoint","interface_schema","core_compatibility","provenance_ref","missing_behavior","claim_ceiling"}
        if ext.get("schema_version")!="sge_extension_registry_v1" or ext.get("core_requires_extensions") is not False: raise SystemExit("extension_registry_invalid")
        for item in ext.get("extensions",[]):
            if set(item)!=required or item["id"] in ids or item["enabled_by_default"] is not False: raise SystemExit("extension_contract_invalid")
            ids.add(item["id"])
    return seen

def export(destination: Path):
    data = load(); paths = validate(data)
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit("destination_must_be_empty")
    destination.mkdir(parents=True, exist_ok=True)
    for path in paths:
        out = destination / path; out.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(ROOT / path, out)
    (destination / "EXPORT_METADATA.json").write_text(json.dumps({"candidate_id":data["candidate_id"],"status":data["status"],"files":sorted(paths),"sha256":{p:hashlib.sha256((destination/p).read_bytes()).hexdigest() for p in paths}}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"exported:{len(paths)}:{destination}")

def ensure_empty(destination: Path):
    if destination.exists() and any(destination.iterdir()): raise SystemExit("destination_must_be_empty")
    destination.mkdir(parents=True, exist_ok=True)

def bootstrap(destination: Path):
    ensure_empty(destination)
    files = {
      "README.md": "# Minimal SGE Project\n\n项目 authority 位于 AGENTS.md、kb/data/ 和 Dashboard/。\n",
      "AGENTS.md": "# Project Governance\n\n- 稳定 truth 写入 kb/data/；执行记忆写入 Dashboard/。\n- 候选、验证、批准和发布分轴记录。\n",
      "kb/data/strategy/profile.json": json.dumps({"schema_version":"sge_project_profile_v1","project_id":destination.name,"authority":{"canonical_truth":"kb/data/","execution_memory":"Dashboard/"},"claim_ceiling":"repo-local governance skeleton only"}, ensure_ascii=False, indent=2)+"\n",
      "Dashboard/Sessions.md": "# Sessions\n\n| Session | Status | Evidence |\n| --- | --- | --- |\n",
      "Dashboard/Current_State.md": "# Current State\n\n尚未创建 Goal。\n"
    }
    for rel, body in files.items():
        out=destination/rel; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(body, encoding="utf-8")
    print(f"bootstrapped:{destination}")

def install(source: Path, target: Path, *, upgrade: bool=False):
    source=source.resolve(); target=target.resolve(); manifest=json.loads((source/"public_export_manifest_v1.json").read_text(encoding="utf-8"))
    skill_prefix=".codex/skills/sge-governed-checkpoints/"; files=[i["path"] for i in manifest["files"] if i["path"].startswith(skill_prefix)]
    if not (target/"AGENTS.md").is_file(): raise SystemExit("target_not_bootstrapped")
    skill_dir=target/skill_prefix.rstrip("/")
    marker=target/".sge-governance-install.json"
    if skill_dir.exists():
        if not upgrade: raise SystemExit("already_installed")
        stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup=target/".sge-backups"/stamp/skill_prefix.rstrip("/"); backup.parent.mkdir(parents=True, exist_ok=True); shutil.move(str(skill_dir), str(backup))
    for rel in files:
        out=target/rel; out.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source/rel, out)
    marker.write_text(json.dumps({"schema_version":"sge_install_record_v1","source_candidate":manifest["candidate_id"],"files":sorted(files),"status":"installed"}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"{'upgraded' if upgrade else 'installed'}:{len(files)}:{target}")

def uninstall(target: Path):
    target=target.resolve(); marker=target/".sge-governance-install.json"
    if not marker.is_file(): raise SystemExit("uninstall_requires_install_record")
    data=json.loads(marker.read_text(encoding="utf-8")); skill=target/".codex/skills/sge-governed-checkpoints"
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    trash=target/".sge-trash"/stamp/"sge-governed-checkpoints"; trash.parent.mkdir(parents=True, exist_ok=True)
    if skill.exists(): shutil.move(str(skill), str(trash))
    marker.rename(target/".sge-trash"/stamp/"install-record.json")
    print(f"uninstalled_recoverable:{trash}")

def main():
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor"); exp = sub.add_parser("export"); exp.add_argument("destination", type=Path)
    boot = sub.add_parser("bootstrap"); boot.add_argument("destination", type=Path)
    ins=sub.add_parser("install"); ins.add_argument("--source", type=Path, required=True); ins.add_argument("--target", type=Path, required=True)
    up=sub.add_parser("upgrade"); up.add_argument("--source", type=Path, required=True); up.add_argument("--target", type=Path, required=True)
    rem = sub.add_parser("uninstall"); rem.add_argument("--target", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "doctor": validate(load()); print("public_doctor:pass")
    elif args.command == "export": export(args.destination)
    elif args.command == "bootstrap": bootstrap(args.destination)
    elif args.command == "install": install(args.source, args.target)
    elif args.command == "upgrade": install(args.source, args.target, upgrade=True)
    elif args.command == "uninstall": uninstall(args.target)
if __name__ == "__main__": main()
