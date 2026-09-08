from pathlib import Path
import json,subprocess,hashlib,datetime,tarfile,io
REPO=Path('/Users/xiaomei/.codex/worktrees/d441/sge-governance-skill')
BASE=Path('/tmp/sp004-s026-01a0744b')
OUT=REPO/'Dashboard/Artifacts/Stage-Plan-SP-004/SP004_S026_UATTranscript.json'
def inv(p):
 return [{'path':str(f.relative_to(p)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in sorted(p.rglob('*')) if f.is_file()] if p.exists() else []
def run(label,cmd,cwd,expected,watch=None):
 before=inv(watch) if watch else []
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
 step={'label':label,'input_origin':'独立 UAT task 实际执行；非人类手工键入','command':cmd,'cwd':str(cwd),'expected':expected,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'before_inventory':before,'after_inventory':inv(watch) if watch else []}
 d=json.loads(OUT.read_text());d['steps'].append(step);OUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(label,r.returncode,r.stdout[:500],r.stderr[:500]);return r
if __name__=='__main__':
 assert not BASE.exists(), 'fresh base must not exist'
 BASE.mkdir();source=BASE/'source';source.mkdir()
 blob=subprocess.run(['git','archive','HEAD'],cwd=REPO,check=True,capture_output=True).stdout
 with tarfile.open(fileobj=io.BytesIO(blob)) as t:t.extractall(source,filter='data')
 card=json.loads((REPO/'Dashboard/Artifacts/Stage-Plan-SP-004/SP004_S026_CleanRoomUATLaneTaskCard.json').read_text())
 d={'schema_version':'sp004_s026_uat_transcript_v1','status':'running','task_id':'01a0744b-2796-7183-b10a-4c5d5b4cb3a6','source_task_id':'01a07029-0b7d-7723-b1d1-abcb5169d5ec','worktree':str(REPO),'source_head':'35747db7b769a1f6c25bec57263257100d1fb445','source_preparation':'git archive HEAD to fresh source; no product edits, no commit or remote','source_archive_sha256':hashlib.sha256(blob).hexdigest(),'fresh_base':str(BASE),'candidate':str(BASE/'candidate'),'target':str(BASE/'target'),'context_limit':'未继承来源任务对话；系统注入源仓 AGENTS/skill catalog/memory，预检读取源仓 contract/closeout；不称完全零项目背景。','card_digest_algorithm':'canonical JSON SHA-256; distinct from raw file SHA-256','card_digest':hashlib.sha256(json.dumps(card,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'rendered_prompt':Path('/tmp/sp004-s026-rendered.txt').read_text(),'preflight_findings':[{'code':'pending_topology','observed':'renderer rejected user_visible=false','resolution':'来源任务明确授权更新实际 task topology 后 validate/render 通过'},{'code':'raw_vs_canonical_digest','observed':'首次将 raw file hash 传给 expected-card-sha256 被拒','resolution':'读取 renderer canonical JSON digest 后验证通过'}],'steps':[]}
 OUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 run('doctor',['python3','tools/sge_public.py','doctor'],source,'exit 0/public_doctor:pass')
 run('export',['python3','tools/sge_public.py','export',str(BASE/'candidate')],source,'exit 0/exported:48；manifest 48 个文件加 metadata',BASE/'candidate')
 run('bootstrap',['python3','tools/sge_public.py','bootstrap',str(BASE/'target')],BASE/'candidate','exit 0；五个目标项目文件',BASE/'target')
 run('install',['python3','tools/sge_public.py','install','--target',str(BASE/'target')],BASE/'candidate','exit 0/installed:17；core 17 文件及 install record',BASE/'target')
 run('bootstrap_negative',['python3','tools/sge_public.py','bootstrap',str(BASE/'target')],BASE/'candidate','nonzero/destination_must_be_empty；文件不变',BASE/'target')
 run('install_negative',['python3','tools/sge_public.py','install','--target',str(BASE/'target')],BASE/'candidate','nonzero/already_installed；文件不变',BASE/'target')
 run('intake_entry',['python3','.codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py','--mode','intake-evaluation'],BASE/'target','exit 0；打印清单，不是验收 verdict')
