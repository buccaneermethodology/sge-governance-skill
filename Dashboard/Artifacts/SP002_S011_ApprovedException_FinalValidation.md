# SP-002 / S-011 批准例外后的独立最终验证

## 任务理解

本次验证是用户批准 `PROC-01` historical topology exception 后的独立 Final Validation。目标是重新核对原始 Goal、批准影响、最终 Closeout、Dashboard/KB、完整工作树差异和既有独立证据是否共同满足 SP-002 completion rule。

本验证为 read-mostly，只新增本文件，不修复任何 Builder 产物，不改写历史事实。批准仅吸收 `PROC-01` 的有界历史拓扑例外：S-007 独立 Design lane 未产出，主线程随后接管 Design/Builder；这不等于独立 Design/Builder 按原时序实际完成。也不批准 release、production、push、tag、全局 Skill 写入或远端发布。

## Read Manifest（读取清单）

| 读取面 | 用途与结果 |
| --- | --- |
| [Validation lane card](SP002_S011_ApprovedException_FinalValidationLaneTaskCard.json) | 已按用户指定摘要验证；`verdict=pass`，card digest 一致；完整 source refs、delta read set、write scope 与 execution command 已读取。 |
| [AGENTS.md](../../AGENTS.md) 与 [SGC Structural Contract](../../kb/docs/strategy/Strategy_SGC_Structural_Contract_V1.md) | 已读；确认必须覆盖原始目标、独立验证、SI-1..SI-6、claim ceiling、KB/Dashboard 分层和 false-closure 禁止项。 |
| [Loop Goal](SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md)、[Goal Patch](SP002_SGEOpenSourceNewcomerReadiness_GoalPatch.md) | 已读；原始 MH-01..12、PROC-01..05、Scope Delta、completion rule 与 release 非目标均已核对。 |
| [PROC-01 批准记录](SP002_PROC01_TopologyException_Approval.md) | 已读并验证摘要；确认批准只支持有界例外吸收，保留原始执行事实。 |
| [OPCM](SP002_S011_FinalClosure_OPCM.md)、[Final Closeout](SP002_S011_FinalClosure_Closeout.md) | 已读；逐项结果、claim ceiling、验证交接和当前仍待最终状态吸收的内容已核对。 |
| [旧 Final Validation](SP002_S011_FinalValidation.md)、[旧 post-closeout](SP002_S011_PostCloseoutReconciliation_Delta.md) | 已读；两者均为批准前的历史 `blocked` 记录，不能冒充批准后验证；其历史结论予以保留。 |
| [Final UAT](SP002_S010_FinalUAT.md)、[Semantic delta](SP002_S011_SemanticReview_Delta.md) | 已读；UAT 是有界 clean-room 通过，Semantic delta 是有界修复通过，均不自动证明 Goal terminal。 |
| [Current State](../Current_State.md)、[Stage Plans](../Stage_Plans.md)、[Sessions](../Sessions.md)、[Cycle Ledger](SP002_CycleLedger.json) | 已读；当前 `S-011=Doing`、`SP-002=Doing`、`cycle_complete=false`、`candidate_not_approved`、`release_authorized=false`。 |
| 当前差异面 | 已读取 `git status --short`、完整 `git diff`（188 行 tracked diff）、`git ls-files --others --exclude-standard`、`git diff --check`，并核对 card delta read set：Session index/archive、README、KB render manifest、tests、tools、docs、examples、extensions、LICENSE、NOTICE。当前存在既有 tracked/untracked 变化；`git diff --check` 无 whitespace error。 |

未读取或不推定：远端仓库、外部 release、production、push/tag 状态、凭据和 card 未列出的外部运行时；它们不能补足本次完成证据。

## 证据完整性矩阵

| ID | 可观察验收与精确证据 | 实际结果 | 状态与 claim ceiling | 阻断/例外及吸收 |
| --- | --- | --- | --- | --- |
| MH-01 | [public manifest](../../public_export_manifest_v1.json) 与 S-007 closeout | 逐文件 license/provenance/public-private 裁决存在 | 有界落地；candidate | 不证明 release；OPCM/Closeout 吸收 |
| MH-02 | [ERBE Cases](SP002_ERBE_Cases.json)、candidate tests、RED/GREEN | allowlist/default-deny 正负例通过 | test-bound；有界候选 | 不替代 Goal completion；OPCM 吸收 |
| MH-03 | S-007 Design、[extension registry](../../extensions/registry_v1.json) | core/companion/orchestrator/domain 分层可核对 | structurally-supported；bounded | 不证明通用包管理；OPCM/Closeout |
| MH-04 | [Beginner Guide](../../docs/Beginner_Guide_CN.md)、[Quick Start](../../docs/Quick_Start_CN.md)、minimal project | 文档、最小项目和受测路径已落地 | clean-room bounded | 不证明普遍新手可用；UAT/Closeout |
| MH-05 | [public lifecycle tool](../../tools/sge_public.py)、Final UAT | doctor/export/bootstrap/install/upgrade/uninstall 受测路径通过 | test-bound；当前快照 bounded | 不证明 production；UAT/Closeout |
| MH-06 | [loop helper](../../tools/run_sge_loop_goal_cycle.py)、orchestrator tests | profile/state 驱动 helper 通过 | bounded helper | 不等于 Goal terminal；OPCM/Closeout |
| MH-07 | [Final UAT](SP002_S010_FinalUAT.md) | 独立 lane 对最终快照给出限定通过 | externally-supported within declared UAT scope | 不证明 release、production 或原始时序；UAT 吸收 |
| MH-08 | extension registry、public manifest | optional extension 默认关闭，core 不依赖 | optional candidate only | 不证明领域适配或生产可用；OPCM |
| MH-09 | manifest、candidate tests、Final UAT | 身份隔离及 `/Users`、`/home` 扫描在声明范围内通过 | bounded scan | 不扩大扫描结论；UAT/Closeout |
| MH-10 | Semantic delta、旧 Final Validation、批准后本文件、Release Packet | Semantic 修复和批准后重新核对已完成；最终状态面仍未达到 terminal | blocked；最多支持批准后有界复核 | `Doing` 与 `cycle_complete=false` 阻止 Goal complete；Closeout/Current State |
| MH-11 | [Glossary JSON](../../kb/data/glossary_v1.json)、[Glossary Markdown](../../kb/docs/Glossary.md)、Semantic delta | 20 项术语、renderer 与语义边界证据一致 | bounded candidate canonical truth | 未作无条件 promotion；KB/OPCM |
| MH-12 | manifest、public tool、Final UAT | 48 文件导出并排除 Dashboard/Agent Logs 等执行面 | candidate package | 不等于 release/production；UAT/Closeout |
| PROC-01 | S-007 card/Design 历史、[批准记录](SP002_PROC01_TopologyException_Approval.md) | 独立 Design lane 未产出，主线程接管 Design/Builder；该事实未改写 | human-approved topology exception；仅有界例外 | 批准吸收例外，但不产生追溯独立时序合规；OPCM/Closeout |
| PROC-02 | [Semantic delta](SP002_S011_SemanticReview_Delta.md) | 双 verdict 对 revision-2 修复有界通过，B2 保留历史边界 | bounded semantic delta | 不倒推 pre-Builder 合规；Semantic/Closeout |
| PROC-03 | Goal、OPCM、Closeout、旧 post-closeout、本验证 | 原始 Goal 与 revised design 已检查；批准后的最终 Closeout/Dashboard/KB/diff 还未形成新的 durable post-closeout 吸收记录 | blocked；final-state evidence incomplete | 旧对账仍是批准前 `blocked` 历史，不能替代批准后最终对账 |
| PROC-04 | S-007～S-009 closeout、Dashboard 状态面 | continuation 历史已记录，当前 S-011 仍在 revalidation | partial; 不等于 Goal terminal | `S-011=Doing`、`SP-002=Doing`；不能改写为 Done |
| PROC-05 | [Release Decision Packet](SP002_ReleaseDecisionPacket.md)、Cycle Ledger | `release_authorized=false` | candidate-only | 本验证不批准 release、production、push 或 tag |

## Scope Delta

本轮没有新增删除、替换、降级或延期。既有 `SP002-GP-001` 明确新增 MH-11 与 MH-12，未删除 MH-01..10。`PROC-01` 现在是经过人类批准的 historical topology exception，而不是功能范围缩减；批准影响仅限于在 Goal conformance 中有界吸收该历史例外。原始独立 Design/Builder 未按时序实际完成这一事实仍有效。

## 批准 topology exception 的影响

批准记录满足“该例外需要人类 authority”的缺口，但不自动满足其他 completion rule。它允许 OPCM/Goal conformance 将 PROC-01 标为 `human-approved topology exception`，并解除“例外未经批准”这一单项阻断；它不把旧 `blocked` verdict 直接改写为通过，也不授权状态面写入 `Done`。当前最终状态仍显示 `S-011=Doing`、`SP-002=Doing`、`cycle_complete=false`，Closeout 仍说明批准后的最终状态需要重新验证，旧 post-closeout 仍记录批准前事实。因此批准后最终状态、Closeout、Dashboard/KB 和完整 diff 尚未由新的 durable post-closeout reconciliation 统一吸收。

## 测试与门禁

本轮执行 card execution command，退出码为 `0`：

- lane card 摘要验证：`pass`，中文含义是任务卡身份与摘要一致。
- Session registry reconcile/validate：`pass`，15 records、1 current、14 archived、无 drift/collision；只证明 registry projection 一致。
- Final Closeout `closeout-language`：`pass`；只证明中文标题、状态解释和证据边界表达合规，不证明技术完成。
- `unittest discover -s tests -p 'test_*.py'`：21 tests，`OK`；只证明测试覆盖的行为。
- repository doctor、public doctor、KB renderer：均 `pass`；分别只支撑各自结构/公共候选自检/JSON→Markdown projection 边界。
- ERBE RED：revision-2、`contract_verdict=valid`、`execution_verdict=ok`，8 个 frozen fingerprints 为可信 RED。
- ERBE GREEN：revision-2、`contract_verdict=valid`、`execution_verdict=ok`、报告 `pass`；claim ceiling 明确不修复原始 chronology、不授权 release。
- `git diff --check`：通过，无 whitespace error；不证明语义完成、提交、发布或 production。

这些局部门禁没有出现失败，但不能合并成一个超出证据的总体通过结论。

## SGC v1 复核

- 最强可支持 claim level：`externally_supported` 仅限既有独立 UAT 的声明范围；对本轮 Goal completion 最多是 `structurally_supported` 加上批准后的 authority 证据，不能提升为无条件完成。
- SI-1：结构、字段、doctor 和 renderer 不等于完整语义或 Goal 完成。
- SI-2：每项结论绑定了对应 UAT、ERBE、OPCM、Dashboard 或批准证据；最终状态缺少批准后 durable reconciliation。
- SI-3：稳定 glossary 继续由 `kb/` JSON 承载，状态/例外/closeout/Validation 继续由 `Dashboard/` 承载；本文件不提升 truth layer。
- SI-4：本轮独立读取并重算 card 指定门禁，不把 producer 自报或旧 handoff 当作本轮 verdict。
- SI-5：批准 authority 已与 PROC-01 例外匹配，但 `Doing`/`cycle_complete=false` 与 completion claim 不匹配。
- SI-6：MH-01..12 与 PROC-01..05 逐项覆盖；未把批准的单项例外替换成“原始流程全部完成”。

## KB/Dashboard 分层

本次只新增本 Dashboard Validation artifact，属于 execution memory；没有修改 `kb/`、Dashboard 状态表、OPCM、Closeout、Session 或候选实现。稳定 glossary 与治理规则仍以 `kb/data/` 为 canonical truth，当前候选状态、批准例外、测试结果和验证结论留在 `Dashboard/`。由于用户明确禁止修改其他文件，批准后的最终状态吸收和任何 concrete follow-on 不在本文件之外落地；这也是当前 completion evidence 不完整的原因之一。

## 阻断与非阻断发现

### 阻断发现

1. [Final Closeout](SP002_S011_FinalClosure_Closeout.md) 仍是批准后重新验证的收束草案，未吸收本轮最终 verdict；它自身写明最终状态更新尚未执行。
2. [旧 post-closeout reconciliation](SP002_S011_PostCloseoutReconciliation_Delta.md) 是批准前记录，仍把 PROC-01 写成未获批准；它保留历史价值，但不能证明批准后的最终 Dashboard/KB、Closeout 与完整 diff 已完成对账。
3. [Current State](../Current_State.md)、[Stage Plans](../Stage_Plans.md)、[Sessions](../Sessions.md) 与 [Cycle Ledger](SP002_CycleLedger.json) 仍显示 S-011/SP-002 未达 terminal，且 `cycle_complete=false`。本验证无权替它们改写为 `Done`。

### 非阻断发现

- 既有 tracked/untracked 变化规模较大；本轮已读取完整 tracked diff 并执行 `diff --check`，但未把工作树变化解释为已提交或已发布。
- 各局部门禁均通过，且其 claim ceiling 清楚；这些不是阻断本轮验证执行的失败，而是不能合并为 Goal completion 的边界。

## 验证交接包

- 角色：批准后独立、read-mostly Final Validation Agent。
- 输入：card 全部 source refs、AGENTS、SGC skill、Goal/Patch、OPCM/Closeout、批准记录、Final UAT、Semantic delta、旧 Validation、旧 post-closeout、当前 Dashboard/KB 和完整 diff。
- 写入：仅本文件；未修改 Builder 产物、KB、Dashboard 状态、测试、合同、manifest 或 release packet。
- Closeout language verdict：`pass`；中文含义是已执行的 Closeout 语言门禁通过，但它不是技术完成 verdict。
- 主要缺口：批准后的 durable final-state reconciliation 尚未由现有文件吸收，状态面仍未达到 Goal terminal。

## 唯一最终 Verdict

`blocked`（阻断；唯一总体结论）

当前不能声明 `pass`、`done`、`SP-002 complete` 或 `Goal complete`。PROC-01 的人类批准已正确解除“未经批准”这一局部缺口，并保留历史事实；但批准后的所有原始完成条件和最终状态尚未被一组无冲突、durable、可定位的最终对账证据完整支持。现有本地门禁和独立 UAT/Semantic 证据只能支持有界 candidate/结构结论。不得批准 release、production、push、tag 或任何发布动作。
