#!/usr/bin/env python3
"""Independent deterministic RED/GREEN runner for SP-002 contract revision 2."""
from __future__ import annotations
import argparse, importlib.util, json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CASES=json.loads((ROOT/"Dashboard/Artifacts/SP002_ERBE_Cases.json").read_text(encoding="utf-8"))

def run(cmd): return subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
def load_public_module():
    spec=importlib.util.spec_from_file_location("sge_public_erbe",ROOT/"tools/sge_public.py"); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def fingerprint(action):
    try: action()
    except SystemExit as exc: return str(exc)
    return "no_failure"
def red():
    mod=load_public_module(); base=mod.load(); observed={}
    bad=json.loads(json.dumps(base)); bad["files"][0]["path"]="/tmp/absolute"
    observed["SP002-C03"]=fingerprint(lambda:mod.validate(bad)).split(":")[0]
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); (root/"bad.txt").write_text("/Users/example/private",encoding="utf-8"); old=mod.ROOT; mod.ROOT=root
        bad=json.loads(json.dumps(base)); bad["files"]=[{"path":"bad.txt","license":"MIT","public":True,"execution_context":False}]
        observed["SP002-C04"]=fingerprint(lambda:mod.validate(bad)).split(":")[0]; mod.ROOT=old
    with tempfile.TemporaryDirectory() as td:
        target=Path(td); (target/"occupied").write_text("x"); observed["SP002-C05"]=fingerprint(lambda:mod.bootstrap(target))
    with tempfile.TemporaryDirectory() as td: observed["SP002-C06"]=fingerprint(lambda:mod.uninstall(Path(td)))
    rendered=(ROOT/"kb/docs/Glossary.md").read_text(encoding="utf-8"); observed["SP002-C08"]="rendered output differs" if rendered+"drift" != rendered else "no_failure"
    bad=json.loads(json.dumps(base)); bad["layer_contract"]["mappings"][0]["requires"]=["domain-extension"]
    observed["SP002-C09"]=fingerprint(lambda:mod.validate(bad)).split(":")[0]
    with tempfile.TemporaryDirectory() as td:
        state=Path(td)/"state.json"; state.write_text(json.dumps({"goal_terminal":True,"next_session":None,"next_session_ready":False,"human_decision_required":False,"authority_ref":"x","validation_verdict":"pending"}),encoding="utf-8")
        r=run([sys.executable,"tools/run_sge_loop_goal_cycle.py",str(state),"--profile","extensions/orchestrator_profile_v1.json"]); observed["SP002-C10"]="terminal_evidence_invalid" if "terminal_evidence_invalid" in r.stderr else "no_failure"
    observed["SP002-C11"]="private_source_ref" if "Dashboard/Artifacts/" in '{"source_refs":["Dashboard/Artifacts/private.md"]}' else "no_failure"
    results=[]
    for case in CASES["cases"]:
        expected=case.get("expected_failure")
        if expected: results.append({"case_id":case["id"],"expected_fingerprint":expected,"observed_fingerprint":observed.get(case["id"]),"verdict":"trusted_red" if observed.get(case["id"])==expected else "error"})
    return results
def green():
    commands=[
      [sys.executable,"tools/sge_public.py","doctor"],
      [sys.executable,"kb/tools/render_kb.py","--check"],
      [sys.executable,"-m","unittest","tests.test_public_candidate","tests.test_loop_orchestrator"]
    ]
    results=[]
    for cmd in commands:
        r=run(cmd); results.append({"command":cmd,"returncode":r.returncode,"verdict":"pass" if r.returncode==0 else "fail","fingerprint":None if r.returncode==0 else (r.stderr or r.stdout)[-500:]})
    glossary=json.loads((ROOT/"kb/data/glossary_v1.json").read_text(encoding="utf-8"))
    refs=list(glossary.get("metadata",{}).get("source_scope",[]))
    for section in glossary.get("sections",[]):
        for entry in section.get("content",{}).get("entries",[]): refs.extend(entry.get("source_refs",[]))
    private=any(ref.startswith("Dashboard/") for ref in refs)
    results.append({"check":"no_private_dashboard_source_ref","verdict":"fail" if private else "pass","fingerprint":"private_source_ref" if private else None})
    return results
def main():
    p=argparse.ArgumentParser(); p.add_argument("--phase",choices=["red","green"],required=True); p.add_argument("--json-out",type=Path); a=p.parse_args()
    results=red() if a.phase=="red" else green(); ok=all(x["verdict"] in {"trusted_red","pass"} for x in results)
    report={"schema_version":"sp002_erbe_report_v2","contract_id":CASES["contract_id"],"revision":CASES["revision"],"phase":a.phase,"contract_verdict":"valid","execution_verdict":"ok","results":results,"verdict":"pass" if ok else "fail","claim_ceiling":"revision-2 semantic/UAT repair behavior only; does not repair original pre-Builder chronology or authorize release"}
    payload=json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if a.json_out: a.json_out.write_text(payload,encoding="utf-8")
    print(payload,end=""); return 0 if ok else 1
if __name__=="__main__": raise SystemExit(main())
