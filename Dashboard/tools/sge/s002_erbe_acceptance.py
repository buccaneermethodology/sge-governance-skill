#!/usr/bin/env python3
"""Deterministic S-002 ERBE acceptance for the audio-transcriptor SGE core."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".codex/skills/sge-governed-checkpoints/scripts"))
from profile_validator import validate_profile

DESIGN = ROOT / "kb/bm-doc/audio-transcriptor-skill_design_v1.0.md"
INVENTORY = ROOT / "Dashboard/Artifacts/SP001_StrategySourceMigration_Inventory.md"
LEDGER = ROOT / "Dashboard/Artifacts/SP001_StrategySourceMigration_Ledger.json"


def inventory_entries() -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in INVENTORY.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[0].isdigit():
            entries.append((cells[1].strip("`"), cells[2].strip("`")))
    return entries


def reject_forbidden_authority() -> str:
    candidate = {"identity": {"project_name": "audio-transcriptor", "forbidden_target_authority_tokens": ["semx", "kym", "tco"]}, "roots": {"kb_root": "kb", "dashboard_root": "Dashboard", "skill_root": ".codex/skills/sge-governed-checkpoints"}, "authority": {"canonical_truth": "semx-kb/data/strategy", "skill": "/Users/xiaomei/Documents/projects/semx-cli/.codex/skills/semx-governed-checkpoints"}}
    accepted, reason = validate_profile(candidate, expected_project_id="audio-transcriptor", repo_root=ROOT)
    if not accepted:
        return reason
    raise AssertionError("negative case unexpectedly accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    mapping = json.loads((ROOT / "kb/data/strategy/sge_strategy_canonical_mapping_v1.json").read_text())
    profile = json.loads((ROOT / "kb/data/strategy/sge_project_profile_v1.json").read_text())
    policy_decisions = list(mapping["decision_vocabulary"])
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    entries = [(e["source_doc"], e["decision"]) for e in ledger["entries"]]
    names = [name for name, _ in entries]
    decisions = [decision for _, decision in entries]
    required_ok = all(e.get("source_doc") and e.get("decision") and e.get("reason") and e.get("target_or_replacement") and e.get("claim_ceiling") for e in ledger["entries"])
    decision_fields_ok = all((e.get("canonical_source_json") and (ROOT / e["canonical_source_json"]).exists()) if e["decision"] == "migrate_after_refreeze" else True for e in ledger["entries"])
    inventory_counts = {decision: decisions.count(decision) for decision in ("migrate_after_refreeze", "adapt_extract", "reference_only", "remove")}
    mapping_matches = (
        len(entries) == 56
        and len(set(names)) == len(names)
        and all(decision in policy_decisions for decision in decisions)
        and all(name and decision for name, decision in entries)
        and required_ok and decision_fields_ok
    )
    design_hash = hashlib.sha256(DESIGN.read_bytes()).hexdigest()
    negatives = []
    for bad in (
        {**profile, "roots": {**profile["roots"], "kb_root": "missing-root"}},
        {**profile, "project_id": "wrong-project"},
        {**profile, "roots": {**profile["roots"], "kb_root": "../outside"}},
    ):
        ok, reason = validate_profile(bad, expected_project_id=profile["project_id"], repo_root=ROOT)
        negatives.append({"accepted": ok, "reason": reason})
    c01_ok = all(not item["accepted"] for item in negatives)
    results = [
        {"case_id": "S002-C01", "verdict": "pass" if c01_ok else "fail", "evidence": {"roots": profile["roots"], "negative_cases": negatives}},
        {"case_id": "S002-C02", "verdict": "pass" if mapping_matches and sum(inventory_counts.values()) == 56 else "fail", "evidence": {"policy_decisions": policy_decisions, "inventory_files": len(entries), "unique_files": len(set(names)), "inventory_counts": inventory_counts, "exact_coverage": f"{len(entries)}/56", "ledger_carrier": "Dashboard/Artifacts/SP001_StrategySourceMigration_Ledger.json", "required_fields": required_ok, "decision_fields": decision_fields_ok, "kb_role": "generic mapping policy only"}},
        {"case_id": "S002-C03", "verdict": "red", "failure_fingerprint": reject_forbidden_authority()},
        {"case_id": "S002-C04", "verdict": "pass" if design_hash == "3ca2d5f98991b05612b06647e25e65319c0850d6909a14e760aa095f433d17f4" else "fail", "sha256": design_hash},
    ]
    report = {"schema_version": "sge_erbe_acceptance_report_v1", "contract_id": "sp001-s002-sge-core", "case_identity": [r["case_id"] for r in results], "results": results, "execution_verdict": "ok", "claim_ceiling": "仅证明 S-002 合同切片的本地结构与负例拒绝，不证明产品或公共发布。"}
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
