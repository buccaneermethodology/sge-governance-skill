#!/usr/bin/env python3
"""Create reproducible source/target file inventory for the copied Skill."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path('/Users/xiaomei/Documents/projects/semx-cli/.codex/skills/semx-governed-checkpoints')
TARGET = ROOT / '.codex/skills/sge-governed-checkpoints'
OUT = ROOT / 'Dashboard/Artifacts/SP001_SGEGovernanceSkill_ProvenanceInventory.json'

def files(root: Path):
    out=[]
    if not root.exists(): return out
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel=p.relative_to(root).as_posix()
        out.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    return out

OUT.write_text(json.dumps({'schema_version':'sge_skill_provenance_inventory_v1','algorithm':'sha256(file bytes), paths sorted lexicographically','source_root':str(SOURCE),'target_root':'.codex/skills/sge-governed-checkpoints','source_files':files(SOURCE),'target_files':files(TARGET)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
