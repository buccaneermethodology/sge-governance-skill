# SP-001 S-015 关闭后阻断修复增量 Validation

## 任务理解与主张边界

本轮复用[第一次关闭后独立对账](SP001_S015_PostCloseoutReconciliation.md)的 B-01..B-05 作为 baseline，只验证 closeout/OPCM 动态证据、SP-002 readiness、Artifacts Index、ERBE final-evidence fail-closed、registry 单次 apply/反向链接与 SP-001 非终态回退。

Reviewer 为独立、read-mostly Validation lane；唯一写入是本报告。最大允许结论本应只到“B-01..B-05 修复后可重新执行一次受控 re-closure”，不证明 re-closure 已发生或最终 post-closeout 已通过。由于当前仍有两个读者面与回退后的非终态冲突，本轮不能授权 re-closure。

## Read Manifest（读取清单）

### 已读取与重算

- Baseline 与 authority：[blocked post-closeout reconciliation](SP001_S015_PostCloseoutReconciliation.md)、[Final Loop Goal](SP001_SGEGovernanceMigration_LoopGoal.md)、[Goal Patch](SP001_QualityRecovery_GoalPatch.md)和 frozen ERBE Contract/Cases。
- 修复后读者面：[最终 closeout](SP001_S015_FinalClosure_Closeout.md)、[OPCM/Scope Delta](SP001_S015_FinalClosure_OPCM.md)、[Current State](../../Current_State.md)、[Stage Plans](../../Stage_Plans.md)、[Sessions](../../Sessions.md)、[Session Index](../../Session_Index.md)、[Artifacts Index](../../Artifacts_Index.md)及 archive manifest。
- Conditional Read 扩展：[Big Ideas](../../Big_Ideas.md)。原因是验收项要求 SP-001 已回退非终态，而 BI-001 的 Next Step/Notes 是当前 Dashboard execution memory；发现它与 Stage Plan/Session 状态冲突后不能用 delta read set 压制扩读。
- Tooling 与 tests：`Dashboard/tools/quality_recovery_erbe.py`、`Dashboard/tools/session_registry.py`、`tests/test_session_registry.py`、[Doctor Report](SP001_S015_DoctorReport.json)与现存 [ERBE full report](SP001_QualityRecovery_ERBE_Report.json)。
- 当前工作树：完整 `git status --short`、repair diff、tracked/untracked inventory 与 `git diff --check`。
- 独立重算：lane card digest、ERBE full、`tests.test_session_registry`、registry check/validate、doctor、KB render、closeout/OPCM language gate。

### 未读或不适用

- 未操作 remote、release、global Skill、provider 或 production surface；SP-001 未授权这些动作。
- 未运行 live registry `--apply`，因为当前 `reconcile --check` 无 drift；在无 drift 时 apply 没有合法写入目的。单次 apply 与 archive→current 链接回写使用隔离临时 repo 回归验证。

## B-01..B-05 Disposition（逐项裁决）

| ID | 修复后独立观察 | Disposition | 对 re-closure 的影响 |
| --- | --- | --- | --- |
| B-01 closeout dynamic inventory | closeout 不再固定 tests 或 current/archive 数量；tests 精确值链接 Doctor Report，registry 精确拆分链接 archive manifest | `closed`，中文含义是 closeout 不再因新增验证 artifact 或状态移动立即陈旧 | 不阻止 |
| B-02 OPCM final absorption | MH-08/MH-14 已改用非零 tests + Doctor Report；S001-AC-03 已明确被 Final Validation 吸收。但 MH-15 的实际结果仍写“受控状态收束已落地”，与当前 rollback 后 SP-001=`Doing`、S-012..S-015 非终态冲突 | `partially_closed_with_blocker`，中文含义是原 B-02 的计数与 AC-03 已修复，但当前状态吸收仍不完整 | 阻止 re-closure；见 RB-01 |
| B-03 SP-002 readiness | Current State、Stage Plans 与 S-007 row 均保持 SP-002/S-007=`To do`，并区分 SP-001 final pass 与用户启动 authority；但 BI-001 Next Step 仍写“SP-001 已 Goal terminal” | `partially_closed_with_blocker`，中文含义是 SP-002 主表面已一致，但上游 Big Idea live next-step 仍错误压缩当前状态 | 阻止 re-closure；见 RB-02 |
| B-04 Artifacts Index | Final Loop Goal 行已改为历史规划入口，并明确当前终态受最新 closeout/post-closeout verdict 约束；没有改写历史 Goal 正文 | `closed` | 不阻止 |
| B-05 ERBE final evidence | GREEN 现在读取唯一 `final_evidence_verdict`，拒绝 pending、blocked、缺/重复 verdict 和缺必要 binding markers；当前 blocked reconciliation 因没有该 marker而正确返回 fail | `closed_for_current_contract`，中文含义是当前 AC 要求的 pending/blocked/content-binding fail-closed 已落地；不把 marker/schema 通过解释成语义真理 | 不阻止修复本身；re-closure 后仍须新的独立 final artifact |

## Blocking Findings（阻断项）

### RB-01 OPCM 的 MH-15 与实际 rollback 状态冲突

[OPCM](SP001_S015_FinalClosure_OPCM.md)的 MH-15 实际结果写“active promotion、集成 reviewers 与受控状态收束已落地”，状态写 `landed pending post-closeout verdict`。第一次 closure mutation 的确发生过，但 blocked reconciliation 后已按事务规则回退；当前 [Stage Plans](../../Stage_Plans.md)为 SP-001 `Doing`，[Sessions](../../Sessions.md)中的 S-012=`Doing`、S-013..S-015=`To do`。

一行读取 MH-15 时会把“历史发生过一次后已回退的 mutation”压缩为“当前 closure 已 landed”。这违反 OPCM actual result 必须绑定当前 parent/Closeout absorption 的要求，并使 B-02 不能完整关闭。

Required repair：将 MH-15 实际结果/状态明确改为“第一次受控状态收束后因 blocked reconciliation 已回退；active promotion 与集成 reviewers 仍有效，等待修复 Validation 允许后重新收束”，并保持最终对外主张依赖新的 mutation 后 post-closeout pass。

### RB-02 BI-001 live Next Step 错写 SP-001 已 Goal terminal

[Big Ideas](../../Big_Ideas.md)的 BI-001 Next Step 仍写“SP-001 已 Goal terminal；等待用户另行决定是否启动 SP-002/S-007”。同一行 Notes 虽说明 `Doing` 是 Historical Status Snapshot，但 Next Step 是当前 execution memory，不是历史快照。

该陈述与 [Current State](../../Current_State.md)的 blocked/修复中、[Stage Plans](../../Stage_Plans.md)的 SP-001 `Doing` 以及 S-012..S-015 非终态冲突。它也会让未来 Agent误读 SP-002 的功能依赖已经满足，只剩用户授权，因而 B-03 和“SP-001 已回退非终态”验收尚未完整通过。

Required repair：将 BI-001 Next Step 改为“SP-001 已回退非终态，正在修复 B-01..B-05 并等待新 post-closeout pass；通过后仍由用户另行决定是否启动 SP-002/S-007”。Historical Status Snapshot 与 public/release 边界保持不变。

## ERBE 负例与内容绑定复核

`python3 -m unittest tests.test_session_registry -v` 执行 5/5 tests，全部通过：

- `pending` final evidence 返回 `final_evidence_verdict_pending`。
- `blocked` final evidence 返回 `final_evidence_verdict_blocked`。
- `pass` 但缺 Read Manifest/final-state markers 返回 `final_evidence_binding_incomplete`。
- 单一 `pass` verdict 且包含当前 AC 要求的 closeout/OPCM/reviewer/Dashboard/archive/git status+diff markers 才返回 `final_evidence_pass`。
- registry 单次 apply 在隔离 repo 中将 Done row 从 current 移入 archive、重写链接并稳定 manifest；再将 archive row 改为 Doing 后，一次 apply 可回写 current-relative 链接。

当前真实 [blocked reconciliation](SP001_S015_PostCloseoutReconciliation.md)没有唯一 `final_evidence_verdict` marker，因此 ERBE full 返回 `execution_verdict=blocked`、QR-GREEN-01=`fail`、`post_closeout_evidence_verdict=final_evidence_verdict_missing_or_ambiguous`。这是正确 fail-closed，不是当前 blocker。

现存 [ERBE full report](SP001_QualityRecovery_ERBE_Report.json)仍保存修复前 existence-only 的绿色结论，不能用于 re-closure 或 completion；新的受控 closure 后必须从实际新 reconciliation 重新生成 durable report。

## Registry 与非终态回退复核

- Live registry check/validate：15 records = 9 current + 6 archive，index=15，无 collision/drift。
- Session Index 将 SP-001/S-012..S-015 指向 current surface；archive manifest 同样记录 9/6。
- SP-001 Stage Plan=`Doing`；S-012=`Doing`，S-013、S-014、S-015=`To do`。核心状态 authority 已回退非终态。
- SP-002 与 S-007..S-011 均保持 `To do`，没有自动启动。
- 但 RB-01/RB-02 表明 OPCM 与 Big Idea live next-step 尚未同步吸收该回退，所以不能声明“所有最终状态面已一致”。

## Tests / Gates 充分性

| Gate | 独立结果 | 证据边界 |
| --- | --- | --- |
| Repair lane card expected digest | `pass`，中文含义是本 lane 输入未发生摘要漂移 | 不证明修复内容正确 |
| ERBE full | exit 1；contract valid、6/6 trusted RED、QR-GREEN-01 fail、execution blocked | 正确拒绝旧 blocked reconciliation；不预证明新 reconciliation |
| `tests.test_session_registry` | 5/5 pass | 覆盖 pending/blocked/content marker 负例和双向 registry apply |
| doctor | `pass`；9/9 tests，registry/KB/DKG/genericity/references/public identity/trusted RED 均通过 | repo-local technical gates；不消除 Dashboard reader-surface 冲突 |
| registry check/validate | 均 `pass`；15=9+6 | 当前 machine projection 一致 |
| KB render | 5/5 pass | canonical JSON 与 Markdown projection 一致 |
| closeout/OPCM language | 均 pass | 表达形式通过，不等于事实一致 |
| `git diff --check` | pass | tracked whitespace gate 通过 |

## Scope、Truth Split 与 SGC v1

- 未发现新的 Scope Delta；公共 packaging/license/release 仍属于 SP-002，且 SP-002 未启动。
- KB truth 未被本修复改变；B-01..B-04 是 Dashboard execution/final-evidence 修复，B-05 是当前 ERBE deterministic decision surface 修复。
- SGC strongest claim level：`test_bound + structurally_supported_for_repair_only`，中文含义是工具与大部分 reader surfaces 已修复，但不能越过 RB-01/RB-02 声称状态一致或允许 re-closure。
- SI-3 decision surface validity 与 SI-6 original objective/final absorption 仍被 RB-01/RB-02 阻断。language/registry pass 不能替代 OPCM/Big Idea 的实际状态一致性。
- 有界 Builder `Single-Agent Exception` 继续保留；本轮不要求或声称独立 Builder conformance。

## Required Builder / Closure Repair（必须修复）

1. 修复 OPCM MH-15，使其明确第一次 closure 已回退、当前仍为非终态，等待新的受控收束与 post-closeout。
2. 修复 BI-001 Next Step，使其与 blocked reconciliation、SP-001=`Doing` 和 SP-002 未满足最终功能依赖保持一致。
3. 更新后重跑 closeout/OPCM language、doctor、registry check/validate、ERBE full、`git diff --check`；ERBE 此时仍应因旧 blocked reconciliation fail closed。
4. 创建新的 digest-bound read-only delta Validation；只有 RB-01/RB-02 关闭后，才允许重新执行受控 re-closure。
5. re-closure 后必须生成新的独立 post-closeout reconciliation，加入唯一 `final_evidence_verdict`，并真实覆盖 actual closeout、OPCM、Dashboard/KB、registry、完整 final diff 和 topology exception；随后重新生成 durable Doctor/ERBE report。

本 Validation Agent 不执行上述 Builder/Closure 修复。

## 验证交接包

- Claimed scope：B-01..B-05 repair delta、ERBE negative regressions、registry apply/reverse-link 与 rollback state。
- Blocking findings：RB-01、RB-02，均属于当前 evidence integrity/state consistency，不是 future hardening。
- 已关闭：B-01、B-04、B-05；B-02/B-03 为部分关闭。
- 不证明：受控 re-closure 已获准、SP-001 complete、post-closeout passed、public/release/production 或独立 Builder conformance。
- KB/Dashboard impact：本报告只新增 Dashboard Validation evidence；未修改 Builder、KB 或其他 Dashboard state。
- `Closeout language verdict`：`pass`，中文含义是本报告的中文标题、英文 verdict/status、阻断影响、证据边界和下一步可独立理解；写入后仍需 executable gate 重算。
- 语言检查通过不改变本轮技术阻断裁决。

## Verdict 与允许措辞

`blocked-for-controlled-reclosure`，中文含义是“当前仍不允许重新执行受控状态收束”。

允许的最强措辞：

> B-01、B-04、B-05 与 registry 双向 apply 已通过增量复核；B-02/B-03 仍因 OPCM MH-15 和 BI-001 live Next Step 未吸收非终态回退而阻断 re-closure。修复并重新独立验证前，SP-001 保持非终态。

禁止措辞：`controlled re-closure allowed`、`SP-001 complete`、`Goal complete`、`post-closeout passed`、`ERBE GREEN proves completion`、`public-ready`、`released` 或 `production-ready`。
