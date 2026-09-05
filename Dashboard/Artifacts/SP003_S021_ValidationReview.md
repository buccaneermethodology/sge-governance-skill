# S-021 独立验证复核：结构性逐案重算

## 关键结论中文展开

本轮验证的是 S-021 card 允许的本地 clean-room/UAT、S-016 frozen case identity、S-019 状态/权限边界和 S-020 回流边界。固定测试命令提供了当前代码路径的本地行为证据；对 C04、C07、C08、C11、C12、C13、C14，则从 S-016 frozen cases 与 S-019/S-020 durable inputs 独立重算每案 predicate，不把未执行的代码路径写成 runtime witness。

唯一 Validation verdict：`pass-with-findings`（带非阻断发现的通过）。这表示 card 范围内的 required outputs 已完成，7 个指定 frozen cases 的结构性断言均与 expected 一致；它不表示这 7 个 case 有 runtime 行为重放，也不表示 S-021 closeout、SP-003、GitHub、release、license approval 或 production-ready 已完成。

## 验证交接包

| 字段 | 本轮内容 | 中文边界 |
| --- | --- | --- |
| claimed scope | S-021 card 指定的 local clean-room/UAT、ERBE same-case identity、14 tests、状态/权限边界，以及 C04/C07/C08/C11/C12/C13/C14 逐案结构性重算 | 只覆盖当前 card 与 durable inputs 可定位的本地/合同边界 |
| claimed semantic change | 无 | 不修改 frozen contract/cases、Goal、KB、Dashboard registry、runtime 或 acceptance posture |
| explicit non-goals | 未执行 GitHub、remote read-back、credentials、真实 PR round-trip、push/tag/release、license/right approval、production 验收 | 缺少这些外部 authority 时不得推导相应结论 |
| write scope | [本 Review](SP003_S021_ValidationReview.md)、[Validation State Snapshot](SP003_S021_ValidationStateSnapshot.json) | 只写 card 声明的两个文件 |
| Scope Delta | 无 | 未删除、替换、改名、降级或延期原始 must-have；本轮只补齐验证证据载体 |
| CG status | `CG skipped: no CG input provided` | 未提供 CG input，不产生额外结论 |

## Read Manifest

### 已读取并消费

- [S-021 Validation Lane Task Card](SP003_S021_ValidationLaneTaskCard.json)：确认 `full_baseline`、card identity、acceptance IDs、write scope、maximum claim、forbidden claims 和执行命令。
- [S-021 Validation Lane Prompt](SP003_S021_ValidationLanePrompt.txt)：确认本轮固定命令和 lane 边界。
- [SP-003 Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json)、[Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md)、[Stage Plan](SP003_OpenSourceDistributionArchitecture_StagePlan.md)：确认原始 ODA-MH-01..12、Session DAG、completion rule 和不允许的完成措辞。
- [S-016 ERBE Contract](SP003_S016_ERBE_Contract.json) 与 [S-016 ERBE Cases](SP003_S016_ERBE_Cases.json)：确认 frozen `C01–C14` identity、predicate、expected、invariant 和 forbidden collapse。
- [S-021 Clean-room/UAT](SP003_S021_CleanRoom_UAT.md)、[S-021 ERBE RED/GREEN](SP003_S021_ERBE_RED_GREEN.json)、[S-021 Semantic Review](SP003_S021_SemanticReview.md) 与 [S-021 Closeout](SP003_S021_Closeout.md)：确认已有 local witness、same-case inventory、Semantic 双 verdict、UAT claim ceiling 和 closeout 吸收边界。
- [S-017 Validation Review](SP003_S017_ValidationReview.md)、[S-018 Lifecycle Evidence](SP003_S018_LifecycleEvidence.json)、[S-019 State/Permission Matrix](SP003_S019_StatePermissionMatrix.json)、[S-020 Contribution Policy](SP003_S020_ContributionPolicy.md) 与 [S-020 PR Provenance Record](SP003_S020_PRProvenanceRecord.json)：确认相邻 Session 的本地证据、状态轴、权限合同、单向回流和 template-only 限制。
- [AGENTS.md](../../AGENTS.md)、[SGC v1 contract](../../kb/data/strategy/strategy_sgc_structural_contract_v1.json)、[SGC reading surface](../../kb/docs/strategy/Strategy_SGC_Structural_Contract_V1.md)、[双仓 KB strategy](../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)、[Current State](../Current_State.md)、[Sessions](../Sessions.md) 与 [Stage Plans](../Stage_Plans.md)：确认治理硬门、truth split、SGC claim ceiling 和当前 Dashboard 状态。
- 当前实现与测试：[sge_public.py](../../tools/sge_public.py)、[candidate tests](../../tests/test_public_candidate.py)、[projection tests](../../tests/test_public_projection.py)：确认固定命令实际覆盖的代码行为范围。

### 未读取或不能采纳

未读取或操作 GitHub、远端 read-back、credentials、外部授权系统或 CG input。它们不属于本 card 的本地验证 authority。既有 S-021 closeout 未在本 lane 修改，因此本 Review 不把 closeout 文本的旧状态当作本轮验证结论，也不宣称 Session 已关闭。

## 原始目标覆盖

下表检查原始 ODA-MH-01..12 是否被本 lane 吸收；`partial/bounded` 是本 lane 的证据边界，不是 Goal 完成状态。

| ID | 原始要求 | 本轮可观察结果 | 状态与主张上限 | 后续吸收 |
| --- | --- | --- | --- | --- |
| ODA-MH-01 | private canonical → public projection 单向 | C11 结构性拒绝 public PR bypass；S-016/KB 合同保持单向 | `bounded`：不证明真实公开仓 | S-020/S-022 |
| ODA-MH-02 | exact allowlist/default-deny 与私有残留、未知文件、路径逃逸 fail closed | 固定 projection tests 覆盖已执行负例；C04 结构性拒绝私有执行面 | `bounded local`：C04 无 runtime witness | S-017/S-022 |
| ODA-MH-03 | export→diff→Validation→authorized update 可追溯 | 固定本地 export/verify/lifecycle 证据存在；外部 update 未执行 | `partial`：不证明完整外部 pipeline | S-022 |
| ODA-MH-04 | source/manifest/run/candidate/projection/tag 不互替 | C07 结构性确认七轴独立且 projection/tag 可为 null；C14 拒绝 handoff overclaim | `structurally_supported`：不证明真实 tag/release | S-019/S-022 |
| ODA-MH-05 | current public source + target-only install | 固定 candidate tests 的 local default-source lifecycle 通过 | `bounded local`：不证明 GitHub clone | S-018/S-022 |
| ODA-MH-06 | upgrade/backup/install record/recovery 保留 target authority | 固定 candidate tests 通过并保留本地 lifecycle claim ceiling | `bounded lifecycle`：不证明生产或跨平台 | S-018/S-022 |
| ODA-MH-07 | maintainer/end-user surface 分离 | S-016/S-018 合同与固定 lifecycle path 对齐 | `partial`：不证明普遍用户适用 | S-018/S-022 |
| ODA-MH-08 | public PR 回流 private canonical 后重新 export/validation | S-020 record 明确 template-only；C11 拒绝绕过回流 | `not landed`：不把模板当真实 round-trip | S-020/S-022 |
| ODA-MH-09 | CI 无默认 push/tag/release 权限，具体动作需授权 | S-019 permission matrix 明确 `ci_default` 无发布动作 | `bounded contract`：无实际 CI/远端动作 | S-019/S-022 |
| ODA-MH-10 | clean-room/UAT/负例由独立 authority 重算 | 固定命令通过；7 个指定 frozen cases 已逐案结构性重算 | `pass-with-findings`：7 案不含 runtime witness | S-021/S-022 |
| ODA-MH-11 | candidate/validated/approved/published/production/Git mutation 不折叠 | C08、C12、C13 分别重算状态折叠和授权边界 | `structurally_supported`：不授予发布权 | S-019/S-022 |
| ODA-MH-12 | OPCM、中文 closeout、final Validation、post-closeout reconciliation | 本 Review/Snapshot 已形成；最终 closeout/reconciliation 不属于本 write scope | `not landed`：不支持 SP-003 completion | S-022 |

原始目标仍保留，未发生 Scope Delta。本 lane 的局部 verdict 不关闭 ODA-MH-12，也不改变 `goal_terminal=false`。

## Frozen case 逐案结构性断言

以下 7 行均直接引用 [S-016 frozen cases](SP003_S016_ERBE_Cases.json) 的 identity、fixture、predicate 和 expected，并用 [S-019 状态/权限矩阵](SP003_S019_StatePermissionMatrix.json) 与 [S-020 回流输入](SP003_S020_PRProvenanceRecord.json) 做必要的边界对照。`witness` 是 durable input/fixture 的结构性 witness；`runtime_witness=false` 表示本轮没有把未执行的代码路径写成行为证据。

| case | predicate | expected | witness | result |
| --- | --- | --- | --- | --- |
| C04 | `listed_in_allowlist=false` 且 `private_surface=true` 的 `Dashboard/Agent_Logs/S016.log` 必须被公共 projection 拒绝 | `reject`；fingerprint=`private_execution_surface_forbidden`；私有执行证据不进入公共 tree | S-016 C04 fixture：路径未列入 allowlist 且标为 private surface；对照 S-016 public deny boundary | `pass_structural_recompute`；predicate 成立，`runtime_witness=false` |
| C07 | 七个 identity axis 都可独立表达，且 `projection_commit`、`release_tag` 可为 null | `accept`；字段来源与未发生状态分别表达，不把 candidate 推成 projection/tag | S-016 C07 fixture 的 source/manifest/tool/run/candidate 字段齐全，projection/tag 为 null；对照 S-019 identities | `pass_structural_recompute`；predicate 成立，`runtime_witness=false` |
| C08 | `candidate=true`、`validated=true` 但 `approved/published/production_ready/git_mutation=false` 时，不能生成 published/production 结论 | `reject`；fingerprint=`candidate_state_collapse` | S-016 C08 fixture；对照 S-019 七个正交 state axes 和 forbidden collapses | `pass_structural_recompute`；拒绝折叠，`runtime_witness=false` |
| C11 | `public_pr_merged=true` 但未 port 到 private canonical、未 re-export、未 revalidate 时，不得改变 canonical/release identity | `reject`；fingerprint=`public_pr_bypasses_canonical_return_flow` | S-016 C11 fixture；S-020 direction 与 `forbidden_shortcuts=public_merge_as_canonical` 对齐 | `pass_structural_recompute`；predicate 成立，`runtime_witness=false` |
| C12 | CI check 即使通过，也不能在无 human push authorization 时因持有 token 而执行 push/tag/release | `reject`；fingerprint=`ci_publish_permission_boundary_violation` | S-016 C12 fixture：check passed、token=true、human authorization=false；对照 S-019 `ci_default` 与 `automatic_default=[]` | `pass_structural_recompute`；权限边界成立，`runtime_witness=false` |
| C13 | candidate/validated/approved 只有在具体 human authorization 绑定 repo/tree/tag/payload 时才满足外部 mutation 的授权前提 | `accept`；授权绑定具体 identity，不能推导本轮远端动作 | S-016 C13 fixture 的 `bm-sge-governance/tree-001/v1/payload-001` 与 `authorized_only`；对照 S-019 human release authority | `pass_structural_recompute`；授权前提成立，未声明 mutation 已发生，`runtime_witness=false` |
| C14 | 只有 design handoff，且 exporter/installer/independent validation/public mutation 均为 false 时，不能声明 implementation/validation/release | `reject`；fingerprint=`design_handoff_overclaim` | S-016 C14 fixture；对照 S-016 minimum safe slice 和 S-019 当前未发布状态 | `pass_structural_recompute`；predicate 成立，`runtime_witness=false` |

逐案结果为 `7/7 predicate holds`。其中 C04/C07/C08/C11/C12/C13/C14 的结果层是结构性重算，不是 runtime execution witness；它们没有被写入 S-021 UAT 的 runtime alias coverage。

## 固定命令与已有本地行为证据

实际运行 card 指定命令：

```text
python3 -m unittest tests.test_public_candidate tests.test_public_projection && python3 tools/sge_public.py doctor && python3 -m py_compile tools/sge_public.py && git diff --check
```

结果：

```text
Ran 14 tests
OK
public_doctor:pass
```

另外，测试输出包含临时 root 上的 `exported:48`、默认 source install/upgrade、可恢复 uninstall 以及 projection negative cases。该 runtime evidence 只支持当前测试实际走到的 C01/C02/C03/C05/C06/C09/C10 局部路径；不替代上表 7 案的结构性重算，也不支持远端、发布或生产结论。

## ERBE、UAT 与 Semantic Review 对账

- [S-016 cases](SP003_S016_ERBE_Cases.json) 与 [S-021 ERBE](SP003_S021_ERBE_RED_GREEN.json) 的 contract ID/revision 和 C01–C14 identity inventory 一致；`same_case_ids=true` 只表示 inventory 对齐，不表示每案都有 runtime witness。
- S-021 producer ERBE 的 `trusted_red=false`、`green.status=not_claimed_pending_independent_validation` 保持为 producer evidence 状态；本 Review 不把它们改写成自身 verdict。
- [S-021 Semantic Review](SP003_S021_SemanticReview.md) 的双 verdict 为 `Design Freeze Validity=partial`、`Implementation Entry Readiness=conditional`。其含义是边界和后续最小入口有条件成立，不是独立 Validation 通过；本 Review 不替代 Semantic Review。
- [S-021 Clean-room/UAT](SP003_S021_CleanRoom_UAT.md) 仍把 CR/NEG 限定为 local witness alias；本轮新增的 7 案是结构性断言，不创建新的 frozen identity，也不把 alias 改成 runtime evidence。

## 状态/权限与回流边界

[S-019 matrix](SP003_S019_StatePermissionMatrix.json) 的七个状态轴仍独立：`candidate`、`validated`、`approved`、`published`、`production_ready`、`git_mutation`、`license_authorized`。其 `push/tag/release` 均为 `not_authorized`，`read_back=not_requested`；C08/C12/C13 的结构性结果与此边界一致。

[S-020 policy](SP003_S020_ContributionPolicy.md) 和 [PR provenance record](SP003_S020_PRProvenanceRecord.json) 仍是 public PR input → private canonical review/port → fresh projection → independent validation → separately authorized public update；record 状态为 template-only，不是真实远端 PR。C11 的拒绝结果只验证不允许绕过这条回流顺序。

## Validation 角色分段

### Validation Reviewer

当前合同和 card required outputs 已满足；7 个指定案的 predicate/expected/witness/result 均可定位，且 evidence layer 没有把结构性重算升级成 runtime witness。因此给出唯一 `pass-with-findings`。

### Adversarial Tester

在本 card 的 Level 1 contract boundary 与 Level 2 semantic abuse 范围内，C04/C08/C11/C12/C14 分别覆盖私有面、状态折叠、回流绕过、CI 权限和 design overclaim；没有发现需要阻断本 lane 的 predicate mismatch。未执行 Level 3 远端/credential 攻击测试，因为它们不在本 card authority 和 threat scope 内。

### Governance Architect

非阻断建议：后续若要把这些结构性 case 转成可运行的 maintained gate，必须另行定义执行入口、failure fingerprint 和 BDD/contract 同步；本轮不把该建议升级为当前 blocker。

## SGC v1 复核

最强 claim level：`structurally_supported`（结构上有支持）。固定测试属于 `test_bound` 的局部输入；7 个指定 case 的本轮结果属于 `structural_recompute`，不是 execution-bound runtime witness。

| 不变量 | 结论 |
| --- | --- |
| SI-1 Truth is not structure | 不把 card、schema、digest、alias、状态字段或本 Review 的结果字段当作行为真相；law、witness、evaluation、governance decision 分层。 |
| SI-2 Grounding completeness | 7 个指定 case 都有 frozen identity、predicate、expected、fixture witness 和结果；未把外部动作缺口填成通过。 |
| SI-3 Decision surface validity | S-019/S-020 规则仍由其合同/矩阵承载；本 Review 只承载本轮 evaluation result，不做 KB promotion。 |
| SI-4 Non-tautological validation | predicate 是从输入字段独立重算，不读取 producer 的 `same_case_ids` 或 pending 状态来伪造结果。 |
| SI-5 Authority-execution coupling | C13 只接受具体授权前提，不宣称 mutation 已发生；C08/C12 继续分离状态和权限。 |
| SI-6 Original objective coverage | ODA-MH-01..12 全部保留；本 lane 只局部覆盖 S-021，不关闭 ODA-MH-12 或 SP-003。 |

## 发现、边界与后续

### 阻断发现

本 lane 无阻断发现。7 个指定 frozen cases 的结构性要求已完成，且没有把未执行路径写成 runtime witness。

### 非阻断发现

1. C04/C07/C08/C11/C12/C13/C14 的证据层是 `structural_recompute`；如未来要求行为级 gate，需另设实现/BDD/acceptance 任务。
2. [S-021 Closeout](SP003_S021_Closeout.md) 不在本 card write scope，本轮未修改；因此该文件尚未吸收本 Review，不能据此宣称 S-021 Session 已关闭。
3. S-020 仍为 template-only；S-019 仍无具体 repo/tree/tag/payload 的本轮远端授权和 read-back；这些是边界保留，不是本 lane 的验证失败。

### 下一状态

- `goal_terminal=false`：原始 Goal completion rule 尚未满足。
- `next_session=S-022`：沿既定 Session DAG 的下一入口。
- `next_session_ready=true`：本 lane 没有需要人类决定的外部动作；S-022 仍须复核完整 OPCM、closeout 和 post-closeout reconciliation。
- `human_decision_required=false`：本轮没有请求或执行外部/权利/破坏性操作。

### KB/Dashboard 复核

- `kb/`：不更新。稳定双仓规则已存在于 [KB JSON](../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)，本轮没有新的已批准稳定 truth。
- `Dashboard/`：只写本 card 指定的 [Validation Review](SP003_S021_ValidationReview.md) 与 [Validation State Snapshot](SP003_S021_ValidationStateSnapshot.json)；不改 Goal、frozen cases、UAT、ERBE、Semantic Review、Sessions、Session registry 或代码。
- 外部动作：未执行 GitHub、网络、remote read-back、credentials、commit、stage、push、tag、release。

## Closeout language verdict

已运行 `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode closeout-language --file Dashboard/Artifacts/SP003_S021_Closeout.md`，结果为 `pass`（通过）。这只证明现有 closeout 的中文标题/解释满足语言门禁，不解除本 Review 的 claim ceiling，也不证明 closeout 已吸收本轮结果。

## 唯一 Validation verdict

`pass-with-findings`（带非阻断发现的通过）：S-021 card 范围内的固定验证和 7 个指定 frozen case 结构性重算均通过；7 案均明确 `runtime_witness=false`。主张上限仍为有界本地 clean-room/UAT、结构性 case 证据和状态/权限边界；不支持 S-021 complete、SP-003 complete、published、production-ready、license approval 或 GitHub mutation。
