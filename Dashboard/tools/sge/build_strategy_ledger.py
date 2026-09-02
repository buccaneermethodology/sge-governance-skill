#!/usr/bin/env python3
"""Build the typed, Dashboard-local strategy decision ledger from the inventory."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INVENTORY = ROOT / "Dashboard/Artifacts/SP001_StrategySourceMigration_Inventory.md"
OUTPUT = ROOT / "Dashboard/Artifacts/SP001_StrategySourceMigration_Ledger.json"
CANONICAL = {
    "Strategy_ERBE_Specification_First_Acceptance_V1.md": "kb/data/strategy/strategy_erbe_specification_first_acceptance_v1.json",
    "Strategy_SGC_Structural_Contract_V1.md": "kb/data/strategy/strategy_sgc_structural_contract_v1.json",
}

def main() -> None:
    rows = []
    for line in INVENTORY.read_text(encoding="utf-8").splitlines():
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not cells[0].isdigit():
            continue
        source, decision, reusable, excluded, target = cells[1:6]
        entry = {
            "source_doc": source,
            "decision": decision,
            "reason": excluded or reusable,
            "target_or_replacement": target,
            "claim_ceiling": "仅记录来源裁决，不证明已 promotion 或实现",
        }
        if decision == "migrate_after_refreeze":
            entry.update({"canonical_source_json": CANONICAL.get(source), "target_owner": target, "identity_scrub": True, "refreeze_evidence": "待 S-002/S-003 独立验证"})
        elif decision == "adapt_extract":
            entry.update({"invariants_extracted": reusable, "excluded_semantics": excluded, "target_owner": target, "canonical_source_or_null_reason": "来源 Markdown 无直接 canonical truth；待重新冻结"})
        elif decision == "reference_only":
            entry.update({"reference_reason": reusable, "non_promotion_boundary": "不得进入 canonical KB truth"})
        elif decision == "remove":
            entry.update({"removal_reason": excluded or reusable, "replacement_or_not_applicable": target})
        rows.append(entry)
    OUTPUT.write_text(json.dumps({"schema_version": "sge_strategy_decision_ledger_v1", "carrier": "Dashboard execution memory", "entries": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
