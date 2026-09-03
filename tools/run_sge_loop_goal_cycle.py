#!/usr/bin/env python3
"""Generic, profile-and-hook-driven Loop Goal routing helper."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("state", type=Path); p.add_argument("--profile", type=Path, required=True); a=p.parse_args()
    data=json.loads(a.state.read_text(encoding="utf-8"))
    profile=json.loads(a.profile.read_text(encoding="utf-8"))
    if profile.get("schema_version")!="sge_orchestrator_profile_v1" or profile.get("project_binding") is not None: raise SystemExit("profile_contract_invalid")
    hooks=profile.get("decision_hooks", {})
    required={"goal_terminal","next_session","next_session_ready","human_decision_required","authority_ref","validation_verdict"}
    if set(data) != required: raise SystemExit("state_contract_invalid")
    if data["goal_terminal"]:
        if not data["authority_ref"] or data["validation_verdict"]!="pass": raise SystemExit("terminal_evidence_invalid")
        route="reported_terminal_route"
    elif data["human_decision_required"]: route="human_authority_route"
    elif data["next_session_ready"] and data["next_session"]: route="continue_session_route"
    else: route="not_ready_route"
    if route not in hooks: raise SystemExit("hook_missing")
    print(json.dumps({"route":route,"hook":hooks[route],"next_session":data["next_session"],"completion_evidence":False}, ensure_ascii=False))
    return 0
if __name__ == "__main__": raise SystemExit(main())
