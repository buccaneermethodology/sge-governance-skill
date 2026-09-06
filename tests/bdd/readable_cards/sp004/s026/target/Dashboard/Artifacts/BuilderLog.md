# UAT-S001 Builder 执行日志

## 接入与实读记录

本 lane 为独立 Builder subagent；来源为经过 renderer 生成的 Builder prompt，不读取来源任务聊天。Intake execute：按冻结 Design 与五文件 write scope 实施；风险是把本地文档存在与结构检查误称独立通过。已重确认目标、authority、claim ceiling、后续独立验证依赖；ContextBuilder 的 dashboard_state=true 符合实际影响。

已全文读取：BuilderCard、Goal、Design、ContextBuilder、目标 AGENTS、profile、原 Sessions、原 Current_State。已读取已安装 Skill：首轮批读含截断，随后单独补读第 1–175 行，其后工作流与 Hard Stops/Output Expectation 已在首轮输出阅读；checklists 实读第 46–101、128–184、340–364 行；公开 companion SGC JSON 实读第 100–290 行，覆盖 claim levels、forbidden collapses、SI-1..SI-6 与 completion rule。companion 仅只读参考，不成为 target canonical truth。

未读：源仓私有资料、memory 文件、来源任务历史；公开 README/Quick Start/新手指南由主任务采集，本 lane 未重读；DesignLog 正文、旧 Context 正文、安装 manifest 正文未读，仅 inventory 采集其路径/字节摘要；其余技能源码/参考/Schema 只做 inventory，未声称全部实读。系统已注入通用仓库上下文，因此不声称完全无项目上下文。Closeout/Review/Reconciliation 尚未存在，由下游读取实际文件。

## 实际命令与结果

所有命令 cwd 为 `/tmp/sp004-s026-01a0744b/target`。

1. 初次 `lane_task_card.py validate` 手工转录 expected digest 时漏字符，退出 2：`error: --expected-card-sha256: must be a lowercase SHA-256 digest`。未开始写入。随即按 renderer 原文完整摘要重跑，退出 0：`verdict=pass`，card_id=`uat-s001-Builder`。这是入口转录错误及修复，不是 contract RED。
2. `cat Dashboard/Artifacts/BuilderCard.json`；`cat AGENTS.md kb/data/strategy/profile.json Dashboard/Artifacts/Goal.md Dashboard/Artifacts/Design.md Dashboard/Artifacts/ContextBuilder.json .codex/skills/sge-governed-checkpoints/SKILL.md Dashboard/Sessions.md Dashboard/Current_State.md`：退出 0，Skill 部分截断，按上一节补读。
3. `python3 .codex/skills/sge-governed-checkpoints/scripts/context_bootstrap.py validate Dashboard/Artifacts/ContextBuilder.json`：退出 0，输出规范化启动包，dashboard_state=true。该校验只证明包结构，不证明实读或任务质量。
4. `sed -n '1,175p' .codex/skills/sge-governed-checkpoints/SKILL.md` 与 checklist/公开 SGC 段落读取：退出 0；实读范围见上。
5. `python3 .codex/skills/sge-governed-checkpoints/scripts/workflow_contract.py --stage implement --format summary`：退出 0，输出 `SGE Workflow Contract v1` 与 `implement: 按 resolved Goal、lane card 和 design handoff 实施，不越过 claim ceiling`。
6. `rg --files --hidden -g '!.git/**'`：退出 0，获得目标实际文件目录；随后 Python pathlib/hashlib 逐文件采集下面字节基线。文件字节 SHA 与 lane card 规范化摘要算法不同，不混用。
7. 使用 Python Path.write_text 写入 PROJECT_NOTE、Handoff、BuilderLog、Sessions、Current_State 五个获授权文件；没有其他写入。

## 写入前实际文件清单

下列 JSON 是写入前全部目标文件及 SHA-256 字节摘要；这是机器比较证据，不是独立验证结论。

```json
{
  ".codex/skills/sge-governed-checkpoints/SKILL.md": "43691bbf4ec8c88dbc6b19308f887d180ed4ca268c13e48a430b5fcb66a0c447",
  ".codex/skills/sge-governed-checkpoints/agents/openai.yaml": "3b02bac8217fc05631972619c3963f6d024578908b90cf3e0f03fdd809a6e186",
  ".codex/skills/sge-governed-checkpoints/references/checklists.md": "24fffc584d41cc6010c887790098db033a9ded1eda78709f7ae5c249b6f4c484",
  ".codex/skills/sge-governed-checkpoints/references/context-efficient-goal-validation.md": "103d53f87816749aad8bf0b5506ddbdbb58c9996d31fe84e54af3adf08ab7863",
  ".codex/skills/sge-governed-checkpoints/schemas/goal_contract_v1.schema.json": "87ceeda6e0d53946170f401e61dbb9aa08c8d720ad7903d1f4811b2efce7d565",
  ".codex/skills/sge-governed-checkpoints/schemas/goal_patch_v1.schema.json": "01f3da80e1a604b1bf858b5a6a15537b2995ff030291a8a38de56c95e95ad23e",
  ".codex/skills/sge-governed-checkpoints/schemas/lane_prompt_audit_v1.schema.json": "9a4904c1884e2dab6f44186b53e2b649e5e67ae14c8f860b725c11092986bb26",
  ".codex/skills/sge-governed-checkpoints/schemas/lane_task_card_v1.schema.json": "086c9e47880dc295fea964fb8c9a11bb304d44e7aef59832865e8472393d120a",
  ".codex/skills/sge-governed-checkpoints/schemas/validation_state_snapshot_v1.schema.json": "7bf99314f198d3930b72603bc4f247a1cf472d0f1bdaa94f2b49ba22b27d264e",
  ".codex/skills/sge-governed-checkpoints/scripts/context_bootstrap.py": "6189a068457762ebf146e85c0233da4e41c48134381b88205e166d7bbb31ca41",
  ".codex/skills/sge-governed-checkpoints/scripts/context_efficiency_pilot.py": "78dc6a10010b155c60d7d0551bc8cb84e078da1e0de0099a71eeec753df73c20",
  ".codex/skills/sge-governed-checkpoints/scripts/context_state.py": "c002c7b5801cbecabd1a813a5e3a4b0c9c4817a438ba1ff6d43f3cd530bd3030",
  ".codex/skills/sge-governed-checkpoints/scripts/goal_patch.py": "242f3316833881f7e11a3285e4fc3c3fe81e169525bef2cdc9ded7ee5d870b36",
  ".codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py": "d67b4b7b9f22f901c2a15b5b86878f526370bee469eac27e57a7303758314a01",
  ".codex/skills/sge-governed-checkpoints/scripts/lane_task_card.py": "6a26de820a1ef2439dbae13f6e5ac2d8b5eee1c850aa4cd5342bc3cba457ed5a",
  ".codex/skills/sge-governed-checkpoints/scripts/profile_validator.py": "e6d4e4d52d6caab0909ce327b85e997d9949c9f2e79cf80e83f1133f2b75ce08",
  ".codex/skills/sge-governed-checkpoints/scripts/workflow_contract.py": "34e01d56dcc5c222d8965781410e6a5905a12d51a01f1af53c842211cf996c79",
  ".sge-governance-install.json": "792962aa5a287441234cc7a25d9afd8ee276f4894ce74b30fbb44a09d8bf588b",
  "AGENTS.md": "f18e2b2c111f9f0aab77c23606db5c5a4032bca3fb0c21efc5c28d134dd2ca84",
  "Dashboard/Artifacts/BuilderCard.json": "4b34ddb8bf0b74d1ae3cca8b92a1df39b70152544c3030afdf12aeacdde417f1",
  "Dashboard/Artifacts/BuilderPrompt.txt": "862124e605e37b3e240607ebe35dd863b3f123065c551bb8b08c785accbc194d",
  "Dashboard/Artifacts/Context.json": "805e35c5af36f47af7e91d65ea5c0541a3535430bab2a261d339d55014899c84",
  "Dashboard/Artifacts/ContextBuilder.json": "6e9678612142400fea4a0054226aa82646f2a68120e065a7a2df9ebe3aaadad6",
  "Dashboard/Artifacts/Design.md": "d69da82c143a49f86b1b125fd4bb558dad65edb4bd6417977842f724e9051968",
  "Dashboard/Artifacts/DesignCard.json": "5d33f1068b47d9f65dbf825efb863feda42b3eae8d9362b41c600143b3cda12d",
  "Dashboard/Artifacts/DesignLog.md": "9caa98c4284e51d7fd0dd6129cbabd2e26a23cf6c61f1cdeef58756f30417d91",
  "Dashboard/Artifacts/DesignPrompt.txt": "b4454f98eb720001721a5a29e65b4f822f56cea7ede0fb74ca94b5b5c5b12039",
  "Dashboard/Artifacts/Goal.md": "0c6e153142c2fc0e58b3b862b62b2a12337dc4a720fbf989a4503d8fb109892d",
  "Dashboard/Artifacts/PromptAudit.json": "b4733dc9e6c673e1d3205b5d31c0aace11e835a78f2681fd936aa109766a0659",
  "Dashboard/Current_State.md": "ae45df409efbe38da8bfe2deb69a9710b9f311eb20c3d6743f9c63519c9291f6",
  "Dashboard/Sessions.md": "bd4168292a739d074d0c02abce9b5acab060282ba649b23d93e17115cf53712d",
  "README.md": "10f578751518dc5bef9d5c5556ef071ed247d742e8720f0673da79e2ccc3b9dd",
  "kb/data/strategy/profile.json": "4df99da2635a0936723e0207b9b59c1bb12c9e72c9e93614329b187fb4e84452"
}
```

## 写入清单与证据边界

新增 PROJECT_NOTE.md、Dashboard/Artifacts/Handoff.md、Dashboard/Artifacts/BuilderLog.md；更新 Dashboard/Sessions.md、Dashboard/Current_State.md。全部属于已校验 card 的 write_scope。正文差异是新增三标题说明、完整交接和日志，以及把设计待执行/执行中状态推进为待独立验证。没有写独立 Review、Closeout 或最终状态。

## 写入后实际复核

真实运行 `cat AGENTS.md`、`python3 -m json.tool kb/data/strategy/profile.json` 及 `cat Dashboard/Artifacts/Goal.md Dashboard/Sessions.md Dashboard/Current_State.md`，全部退出 0。AGENTS 显示稳定 truth 与执行记忆分工；profile 输出 project_id=target、canonical_truth=kb/data/、execution_memory=Dashboard/、claim_ceiling=repo-local governance skeleton only；最终两状态面均显示待独立验证、M4/M5 未满足。批量 cat 覆盖说明中三个单独 cat 的相同文件内容。

实际执行以下 Python 自检（通过命令行 heredoc 运行，没有创建测试脚本），退出 0；其结果仅为 Builder 自检：

```python
from pathlib import Path
import json,re,hashlib
r=Path('.')
log=r/'Dashboard/Artifacts/BuilderLog.md'
before=json.loads(re.search(r'```json\n(.*?)\n```',log.read_text(),re.S).group(1))
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(r.rglob('*')) if p.is_file() and '.git' not in p.parts}
new=sorted(set(after)-set(before))
changed=sorted(p for p in before if p in after and before[p]!=after[p])
missing=sorted(set(before)-set(after))
assert new==['Dashboard/Artifacts/BuilderLog.md','Dashboard/Artifacts/Handoff.md','PROJECT_NOTE.md'],new
assert changed==['Dashboard/Current_State.md','Dashboard/Sessions.md'],changed
assert missing==[],missing
s=(r/'PROJECT_NOTE.md').read_text()
assert re.findall(r'^## (.+)$',s,re.M)==['项目目的','使用步骤','边界']
links=re.findall(r'\]\(([^)]+)\)',s)
assert all((r/p).is_file() for p in links)
assert json.loads((r/'kb/data/strategy/profile.json').read_text())['authority']=={'canonical_truth':'kb/data/','execution_memory':'Dashboard/'}
print(json.dumps({'producer_selfcheck':'pass','new':new,'changed':changed,'deleted':missing,'file_count':len(after),'project_note_links':links,'protected_files_unchanged':len(before)-len(changed)},ensure_ascii=False,indent=2))
```

实际输出摘要：producer_selfcheck=pass（上述存在性、路径与写入范围检查通过）；new 为 BuilderLog、Handoff、PROJECT_NOTE 三文件；changed 为 Current_State、Sessions 两文件；deleted=[]；file_count=36；project_note_links 五个均存在；protected_files_unchanged=31。写入后完整 inventory 是上方 33 文件基线加新增三文件，未删除文件。

最后仅追加本节日志，仍在同一五文件 write scope 内。未运行负例、独立 Review、语言门或 reconciliation；这些由下游实际执行并落盘，不能借本日志推断通过。
