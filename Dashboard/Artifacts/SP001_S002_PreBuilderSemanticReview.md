# S-002 预 Builder 语义复核

## 关键结论中文展开

本复核确认，S-002 提出的总体架构方向是正确的：`sge-governed-checkpoints` 应当只承载通用治理协议，audio-transcriptor 的路径和项目身份应由 project profile 注入，来源 Semx 文件只能作为 provenance、反例或重新冻结的治理不变量，不能自动变成目标项目的 canonical truth。

此前冻结包中的五项 authority/ontology blocker 已通过 Contract Patch 与当前 Delta card 修复：derived DKG 已明确为 `not_configured`，56 文件 ledger 与 generic mapping policy 已分层，profile identity 字段已作用域化，profile validator 已参数化，且 ERBE 与 Design 的 write exclusions 已统一。用户现已批准有界 topology exception，因此后续 S-003/S-004 候选可保留但不得倒灌为 S-002 证据；首轮 pre-Builder 时序仍不可追溯，且 Skill checklist 中残留少量 Runtime/SAG 示例术语需要后续去产品化清理。

因此本复核的结论是：设计方向可以保留，但冻结状态需要 Contract Patch 后重新 RED；Builder 目前只能执行“修复合同边界的最小切片”，不得开始 S-003 的广泛 tooling/registry 迁移。本复核发生在首轮 Builder candidate 已经出现之后，只能作为下一轮修复 Builder 的前置审查，不能追溯性证明首轮实现满足 pre-Builder 时序。

## 复核身份与时序边界

- Reviewer/source：独立 Semantic Reviewer lane `strategy_runtime_audit`。
- 角色边界：read-mostly；除本文件外未修改 Skill、profile、schema、ERBE、KB、Dashboard row、测试或任何 Builder 产物。
- 时序结论：当前工作树已存在 repo-local Skill、profile、ERBE report 和首轮独立 Validation Review，所以本文件不是首轮 Builder 之前形成的历史证据。它只对下一轮 blocker-repair Builder 生效。
- 最新 Delta card：`4a8106b90c2a2c416837bcd60616621a88fed5a0cdfab83d5e25f5f0db780d76`（机器绑定证据入口）。
- 最新 topology exception：用户批准的[有界拓扑例外](SP001_S002_TopologyException_Request.md)；它允许保留提前产生的 S-003/S-004 候选，但不恢复首轮 pre-Builder 时序，也不改变原始 must-have 或 claim ceiling。
- 最大 claim ceiling：`S-002 authority/ontology Contract Patch 已完成语义复核；首轮 pre-Builder 时序仍不可追溯，且 Skill 示例术语仍有后续清理项；在独立最终 Validation 吸收前不得声明 S-002 Done、进入 S-003、SP-001 complete、公共 Skill 就绪或产品实现。`

## 已读证据清单

已完整读取或核对：

- [S-002 设计交接](SP001_S002_SGECore_Design.md)
- [ERBE Contract](SP001_S002_SGECore_ERBE_Contract.json)
- [ERBE Report](SP001_S002_SGECore_ERBE_Report.json)
- [Canonical Mapping](../../kb/data/strategy/sge_strategy_canonical_mapping_v1.json)
- [56 文件 Strategy Inventory](SP001_StrategySourceMigration_Inventory.md)
- [Strategy Source Manifest](../../kb/data/strategy/sge_strategy_source_manifest_v1.json)
- [audio-transcriptor Project Profile](../../kb/data/strategy/sge_project_profile_v1.json)
- [Project Profile Schema](../../kb/schemas/sge_project_profile_v1.schema.json)
- [SGE Workflow Registry](../../kb/data/strategy/sge_workflow_registry_v1.json)
- [repo-local SGE Skill](../../.codex/skills/sge-governed-checkpoints/SKILL.md)及其 checklist、profile validator、S-002 ERBE acceptance runner 中与本复核相关的接口
- [Delta Context Bootstrap](SP001_S002_SGECore_DeltaContextBootstrap.json)
- [Delta Validation Lane Task Card](SP001_S002_DeltaValidation_LaneTaskCard.json)
- [首轮独立 Delta Validation Review](SP001_S002_SGECore_ValidationReview.md)
- [AGENTS 硬门](../../AGENTS.md)、[Sessions](../Sessions.md)、[Stage Plans](../Stage_Plans.md)和[Current State](../Current_State.md)

本复核没有把音频产品 runtime、已删除的 Semx docs-system、S-003/S-004 Builder 设计或公共发布方案作为 S-002 设计 truth。它们不是判断当前 core/profile/ERBE freeze 是否安全的必要 authority。

## Frame-First 语义架构复核

### Authority 与 truth carrier

正确且应保留的分层是：

| 层 | 合法载体 | 可以证明 | 不可以证明 |
| --- | --- | --- | --- |
| 稳定治理 truth | `kb/data/strategy/` 中经重新冻结的通用合同 | SGE 稳定规则、ontology、authority 和 claim ceiling | Session 执行状态、来源文档本身正确、产品能力 |
| 项目适配 | project profile + schema | audio-transcriptor 的 repo-local roots、项目 identity 和适用 gates | 通用 Skill 已跨仓库成熟、public export 已批准 |
| 执行记忆 | `Dashboard/` | Session 状态、provenance audit、review、closeout 和 blocker | canonical governance truth |
| 派生投影 | 明确命名和可重建的 DKG/read model 输出文件 | 从 source truth/执行证据生成的查询或阅读面 | canonical truth、Validation verdict、human approval |
| 来源 provenance | source manifest、inventory、固定 revision | 来源文件、revision 和迁移裁决的可追溯性 | 来源项目身份成为目标 authority |

当前 profile 与 workflow registry 已将 `derived_dkg`/`derived` 明确为 `not_configured`，不再把 `Dashboard/Artifacts/` 整体冒充 DKG。未来若启用 DKG，必须指向具体、可重建且有 generator provenance 的输出文件；Design、ERBE、Validation、closeout 仍属于 Dashboard execution evidence。

### 核心 ontology

当前 S-002 至少需要稳定区分以下名词：

- `governance core`：通用协议、schema、validator 和 checkpoint，不含项目 ID、当前 Session ID 或来源 repo 路径。
- `project profile`：目标 repo 的 project identity、roots、authority pointer 和 gate applicability。
- `source provenance`：允许记录来源 repo/revision/绝对路径，但只能是不可执行的来源证据。
- `canonical mapping policy`：说明哪些来源内容可重新冻结为稳定 truth，以及对应 canonical source/null reason；不是迁移进度表。
- `migration decision ledger`：逐文件的 migrate/adapt/reference/remove 决策与目标 Session，属于 Dashboard execution memory。
- `optional extension`：默认禁用、不会成为 core authority 的外部能力标识。

最新材料已基本守住这些名词边界：KB mapping 现在只表达 generic mapping/promotion policy，56 文件 decision ledger 留在 Dashboard；profile 也改为 `forbidden_target_authority_tokens` 与 `allowed_disabled_extension_ids`，明确禁止成为目标 authority 与允许默认关闭的 extension reference 是不同作用域。

### Object responsibility 与复杂度轨迹

`sge-governed-checkpoints` 不应演化为同时包含通用治理法、audio-transcriptor profile validator、S-002 migration acceptance、来源 Semx 负例和未来 public-export 工具的 God Skill。当前 `profile_validator.py` 已改为可选 `expected_project_id` 参数驱动，S-002 专属 acceptance runner 已从 Skill root 移除；core/project/test-adapter 的边界已改善，但仍需最终 diff 与 clean-room 证据确认。

如果继续在该目录添加每个项目或 Session 的 runner，未来跨 repo 提取时将无法区分哪些是 core API、哪些是 audio-transcriptor 配置、哪些只是本轮 migration test。正确方向是：core validator 接受 profile/schema/expected project identity 作为输入；项目专属 acceptance 放在 repo test/gate 层，或由 profile-driven adapter 调用 core API。

## Blocking findings

### B-01（已关闭）：派生 DKG 与 Dashboard execution evidence 被折叠

[Project Profile](../../kb/data/strategy/sge_project_profile_v1.json) 与 [Workflow Registry](../../kb/data/strategy/sge_workflow_registry_v1.json) 现均使用 `not_configured`，不再把整个 artifacts 目录描述成派生层。

处置结果：S-002 当前满足最小语义要求；未来启用 DKG 时仍必须指向具体、可重建且有 generator provenance 的输出。

### B-02（已关闭）：Canonical Mapping 的 authority 与数据模型不足

[Canonical Mapping](../../kb/data/strategy/sge_strategy_canonical_mapping_v1.json) 现只承载 generic mapping/promotion policy；逐文件 decision ledger 由 [56 文件 Inventory](SP001_StrategySourceMigration_Inventory.md) 承载，并在 ERBE Report 中记录 Dashboard ledger carrier 与 56/56 exact coverage。

该分层关闭了原有 authority 混层；C02 仍只证明 56 个来源表面有 decision，不证明每个 `adapt_extract` 已完成 canonical extraction。

已完成的 Contract Patch 采用：

1. 56 文件 decision ledger 保留为 Dashboard artifact；
2. KB 只保存通用 mapping/promotion policy。

仍需最终 Validation 以相同 56 个 identity 复核 C02 与 independent recompute。

### B-03（已关闭）：通用 core 与项目/Session acceptance adapter 尚未隔离

[repo-local SGE Skill](../../.codex/skills/sge-governed-checkpoints/SKILL.md) 中的 `profile_validator.py` 已参数化；S-002 专属 `s002_erbe_acceptance.py` 已移至 [Dashboard/tools/sge](../../Dashboard/tools/sge/s002_erbe_acceptance.py)，不再属于可提取 core Skill。

处置结果：core API 与项目 adapter 已分层；最终 clean-room/public export 仍留给 SP-002。

### B-04（已关闭）：identity prohibition 与 optional extension 作用域冲突

[Project Profile](../../kb/data/strategy/sge_project_profile_v1.json) 现使用 `forbidden_target_authority_tokens` 与 `allowed_disabled_extension_ids`；Workflow Registry 中的领域扩展保持默认禁用。

处置结果：profile ontology 作用域已明确；最终 Validation 仍需确认禁用扩展不会成为默认 authority。

### B-05（已关闭）：Design 与 ERBE machine contract 的 Builder write exclusions 不一致

[S-002 设计交接](SP001_S002_SGECore_Design.md) 与 [ERBE Contract](SP001_S002_SGECore_ERBE_Contract.json) 现共享 profile、source manifest、canonical mapping、ERBE contract/cases/expected/RED/claim ceiling 和产品设计的统一 exclusions。

处置结果：machine/prose write authority 已统一；后续变更仍必须走 Contract Patch、Scope Delta 判定和重新 RED。

### B-06（已批准例外，历史缺口仍存在）：首轮 pre-Builder 时序无法追溯恢复

首轮 [Validation Review](SP001_S002_SGECore_ValidationReview.md)已经证明 Builder candidate 和 ERBE report 在本文件完成前存在。当前 review 可以阻止下一轮 Builder 再次越过语义边界，但不能改写历史顺序。

处置结果：[有界拓扑例外](SP001_S002_TopologyException_Request.md)已获用户批准，允许保留提前产生的 S-003/S-004 候选并要求它们重新建立各自治理证据。该批准不恢复首轮 pre-Builder 时序；closeout/OPCM 仍必须记录 `exception/partial topology evidence`，因此它不支持无例外的 S-002 full-conformance claim，也不能由本文件倒签关闭。

## 非阻断但必须跟踪的语义风险

- `references/checklists.md` 和 `guardrail_checklist.py` 仍用 `SAG observation graph`、`Final Runtime Kernel Closeout` 作为通用示例。它们不是 executable Semx identity，但仍是来源产品 ontology residue；建议在 S-004 替换为 `evidence observation graph`、`final governed-system closeout`，当前作为 P1 follow-on，不改变 B-01..B-05 已关闭状态。
- Profile schema 把 `kb_root="kb"`、`dashboard_root="Dashboard"` 固定为 const。这对当前 repo-local claim 可以接受，但不证明跨仓库路径可配置；公共可移植性必须留给 SP-002，S-002 不得把本地 schema-valid 写成 portable。
- ERBE Contract 同时保存 expected failure fingerprint 和 `red_evidence.status`/`green_evidence.status`。expected fingerprint 属于冻结合同，实际运行状态属于 ERBE Report。建议下一次合同版本将 law 与 evidence 分离，避免未来为了吸收一次 run 修改冻结合同。
- 设计中的“该切片允许进入 S-003”在单行阅读时容易被误解为已经 ready。建议改成“仅在 B-06 例外被 OPCM 吸收、同 identity re-RED 和独立最终 Validation 通过后，才允许进入 S-003”。

## 最小安全 Builder 切片

在任何 S-003 tooling/registry 迁移前，只允许一个 `S-002 semantic-boundary repair` 切片：

1. 生成可定位的 Contract Patch，统一 truth placement、mapping carrier、identity scopes 和 Builder exclusions；若改变原 must-have 交付或 authority，记录 Scope Delta 和人类批准状态。
2. 修复 profile/schema 中 derived-DKG pointer 和 identity/extension 作用域，不修改产品设计。
3. 将通用 core validator 与 audio-transcriptor/S-002 acceptance adapter 分层；保持行为 case identity 不变。
4. 将 56 文件 ledger 与通用 canonical mapping policy 分层，或形成逐文件 typed provenance contract。
5. 用原 `S002-C01..C04` identity 重新产生 trusted RED/GREEN，C02 必须独立逐文件重算，C03 必须走真实 validator 接口。
6. 由独立 Validation 覆盖 patch 后 Design、ERBE、profile、mapping、Skill、最终 diff 与 Dashboard 状态；在此之前 S-002 保持 `Doing`。

该最小切片的允许输出是修复后的合同和验证候选；禁止输出 `S-002 Done`、S-003 implementation、公共包、全局 Skill、音频 CLI 或 runtime。

## Implementation ladder 与下一 Session map

```text
Contract Patch / authority placement decision
  -> same-identity re-RED
  -> project profile + schema
  -> generic profile validator + repo-specific acceptance adapter
  -> per-file mapping/provenance validator
  -> independent S-002 GREEN and four-axis Validation
  -> S-002 closeout/reconciliation
  -> S-003 generic tooling and workflow registry migration
  -> S-004 identity/history cleanup
  -> S-005 integrated Validation + final Semantic Review
```

- 当前 next session：仍是 `S-002 blocker repair`，不是 S-003。
- S-003 ready 条件：B-01..B-05 关闭，B-06 被诚实吸收到 Scope/OPCM，ERBE 使用相同 case identity 重新验证，独立 Validation 不再 blocked。
- SP-002 public/newcomer work 不属于本复核实施入口，不得提前吸收。

## Future-agent 误用场景

| 误用场景 | 影响 | 缓解机制 |
| --- | --- | --- |
| 未来 Agent 看到 `Dashboard/Artifacts/` 被称为 derived，删除或重建其中的 closeout/Validation | 丢失不可替代的执行证据 | profile 只指向具体可重建 DKG；execution evidence 保持独立层 |
| 未来 Agent 把 56 文件 mapping 放在 KB 就理解为 26 个 `adapt_extract` 已成为 canonical truth | Markdown/迁移裁决冒充稳定治理法 | 逐文件 canonical source/null reason；ledger 留 Dashboard；promotion 需独立 contract |
| 新项目复制 Skill 后，运行硬编码 audio-transcriptor/S-002 validator | 通用 Skill 表面存在，实际不可移植 | core API 参数化；项目 acceptance adapter 与 export allowlist 分离 |
| Agent 按 `forbidden_identities` 删除 optional extension provenance，或反过来让 KYM/TCO 成为默认 authority | provenance 丢失或领域耦合重新进入 core | 给禁止 token 和允许 extension 明确作用域；默认禁用并由 profile opt-in |
| Closeout 把本复核称为首轮 pre-Builder pass | 流程 must-have 被追溯性伪造 | 明确 next-repair-only 时序；OPCM 记录 exception/partial topology evidence |

## 状态词压缩测试

- `核心冻结`：当前只能写“核心冻结候选”；单独写“已冻结”会掩盖 B-01..B-05。
- `identity isolated`：当前不能使用；provenance 允许出现 Semx，但 active core/project ontology 仍需分层。
- `mapping complete`：只能表示 56/56 有 decision；不能表示 26 个 adapt 项已完成 canonical extraction。
- `ready for S-003`：当前为 false；只有最小修复、re-RED 和独立 Validation 通过后才能改变。
- `pre-Builder review complete`：只能表示下一轮 repair Builder 的 review 已完成，不能表示首轮时序合规。

## 双 Verdict

### Design Freeze Validity：`pass-with-findings`

中文含义：B-01..B-05 的 authority/ontology 冲突已关闭，“通用 core + project profile + provenance-only source”方向成立；B-06 已有用户批准的有界 topology exception，但首轮 pre-Builder 时序仍是不可追溯的历史缺口，且 Skill 示例术语有 P1 follow-on。因此设计边界本身可作为下一轮实现输入，但不能据此宣称无例外的完整流程 conformance。

该 verdict 不否定 56/56 typed ledger、C01-C04 deterministic evidence 或用户批准的 topology exception；它说明证据支持“设计边界有效且可继续”，不支持历史时序被修复或产品/公共发布完成。

### Implementation Entry Readiness：`ready-for-S-003-after-final-validation`

中文含义：S-002 合同边界的最小修复已具备进入 S-003 的输入条件，但必须先完成本轮独立最终 Validation，并将 B-06 作为批准的 exception/partial topology evidence 吸收到 OPCM/closeout。S-003/S-004 必须重新建立各自 Context、lane card 与验证记录，不得把提前候选当作 S-002 evidence。

## 最终裁决

当前不能声明 S-002 完成；剩余必需证据为：B-06 已批准例外的 OPCM/closeout 吸收、同 identity re-RED、覆盖最新 Skill/profile/mapping/ERBE/最终 diff 的独立最终 Validation，以及对 Runtime/SAG 示例术语 follow-on 的明确路由。B-01..B-05 已关闭；当前可选收束状态为 `partial/exception-recorded`，不能写无例外的 `pass/done`。
