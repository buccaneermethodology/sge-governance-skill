from __future__ import annotations
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"tools/run_sge_loop_goal_cycle.py"
PROFILE=ROOT/"extensions/orchestrator_profile_v1.json"
class LoopDecisionTests(unittest.TestCase):
    def run_case(self,data):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"state.json"; p.write_text(json.dumps(data),encoding="utf-8")
            return json.loads(subprocess.run([sys.executable,str(SCRIPT),str(p),"--profile",str(PROFILE)],capture_output=True,text=True,check=True).stdout)
    def state(self,**changes):
        data={"goal_terminal":False,"next_session":None,"next_session_ready":False,"human_decision_required":False,"authority_ref":"Dashboard/state","validation_verdict":"pending"}; data.update(changes); return data
    def test_continue_ready_session(self): self.assertEqual(self.run_case(self.state(next_session="S-next",next_session_ready=True))["route"],"continue_session_route")
    def test_human_authority_stops(self): self.assertEqual(self.run_case(self.state(human_decision_required=True))["route"],"human_authority_route")
    def test_terminal_routes_to_audit_not_completion_evidence(self):
        result=self.run_case(self.state(goal_terminal=True,validation_verdict="pass")); self.assertEqual(result["route"],"reported_terminal_route"); self.assertFalse(result["completion_evidence"])
    def test_terminal_without_passing_validation_fails(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"state.json"; p.write_text(json.dumps(self.state(goal_terminal=True)),encoding="utf-8")
            result=subprocess.run([sys.executable,str(SCRIPT),str(p),"--profile",str(PROFILE)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0); self.assertIn("terminal_evidence_invalid",result.stderr)
if __name__ == "__main__": unittest.main()
