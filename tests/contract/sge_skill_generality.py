#!/usr/bin/env python3
"""Bounded clean-room portability checks for the SGE Governance Skill."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".codex/skills/sge-governed-checkpoints"
PROFILE = ROOT / "kb/data/strategy/sge_project_profile_v1.json"


def main() -> int:
    required = [SKILL / "SKILL.md", SKILL / "scripts/context_bootstrap.py", SKILL / "scripts/profile_validator.py"]
    assert all(path.is_file() for path in required), "core skill surface missing"
    metadata = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert metadata.startswith("---\n") and "name: sge-governed-checkpoints" in metadata
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    assert profile["project_id"] == "sge-governance-skill"

    with tempfile.TemporaryDirectory(prefix="sge-genericity-") as tmp:
        target = Path(tmp) / "consumer"
        (target / ".codex/skills").mkdir(parents=True)
        shutil.copytree(SKILL, target / ".codex/skills/sge-governed-checkpoints")
        (target / "kb/data/strategy").mkdir(parents=True)
        (target / "Dashboard").mkdir()
        consumer_profile = dict(profile)
        consumer_profile["project_id"] = "demo-consumer"
        consumer_profile["profile_id"] = "demo-consumer-sge-v1"
        consumer_profile["identity"] = dict(profile["identity"], project_name="demo-consumer", cli_name="demo-consumer")
        (target / "kb/data/strategy/profile.json").write_text(json.dumps(consumer_profile), encoding="utf-8")
        validator = target / ".codex/skills/sge-governed-checkpoints/scripts/profile_validator.py"
        probe = "from pathlib import Path; import json; from profile_validator import validate_path; print(validate_path(Path('kb/data/strategy/profile.json'), expected_project_id='demo-consumer', repo_root=Path('.')));"
        result = subprocess.run(["python3", "-c", probe], cwd=target, env={"PYTHONPATH": str(validator.parent)}, capture_output=True, text=True, check=True)
        assert "(True, 'ok')" in result.stdout, result.stdout + result.stderr

    print("Sge genericity portability: PASS (core copied to an independent demo-consumer profile)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
