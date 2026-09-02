#!/usr/bin/env python3
"""Render the repo-local SGE workflow contract without project phase ontology."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Render generic SGE workflow stages")
    parser.add_argument("--stage", choices=["intake", "design", "implement", "validate", "closeout", "full"], default="full")
    parser.add_argument("--format", choices=["summary", "json"], default="summary")
    args = parser.parse_args()
    stages = {
        "intake": "确认 Raw User Intent、authority、边界、风险和执行路线",
        "design": "冻结最小安全切片、合同、验收、不变量和 Builder write exclusions",
        "implement": "按 resolved Goal、lane card 和 design handoff 实施，不越过 claim ceiling",
        "validate": "独立从 durable inputs 重算证据，检查原始目标、forbidden collapses 和最终 diff",
        "closeout": "运行 registry、closeout-language、KB/Dashboard review、OPCM 与 post-closeout reconciliation",
    }
    selected = list(stages) if args.stage == "full" else [args.stage]
    payload = {"schema_version": "sge_workflow_contract_v1", "stage": args.stage, "steps": [{"id": s, "instruction": stages[s]} for s in selected]}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("SGE Workflow Contract v1")
        for item in payload["steps"]:
            print(f"- {item['id']}: {item['instruction']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
