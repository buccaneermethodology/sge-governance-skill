# S-001 SGE 治理迁移规划落库关闭记录

## 关键结论中文展开

本文件只关闭 `S-001` 的规划落库范围：保存整理前 Git 种子、将 `SP-001` Final Loop Goal、完整迁移计划、Context Bootstrap 和 Dashboard 执行入口落入仓库。首轮独立 Validation 发现三个 blocker，Builder 修复后，独立 delta Validation 给出 `pass-with-findings`，中文含义是当前合同 blocker 已关闭并允许受控状态收束；最终完成措辞仍以关闭后独立对账为准。

本文件不表示 `SP-001` 已启动或完成，不表示 SGE Governance 已迁移，不表示 audio-transcriptor 的 CLI、转写 runtime 或产品设计已实现。`BI-001` 与 `SP-001` 必须继续保持 `To do`；迁移入口虽登记为 `S-002`，但只有用户后续明确启动 `SP-001` 后才可进入。

当前允许的最大主张是：`S-001 的 Git 种子基线、Final Loop Goal、完整迁移计划、逐字 Context 和 Dashboard entry 已完成有界落库；SP-001 迁移未启动。`

## 落地范围

- 已建立可恢复的 Git seed：commit `389087ef01d1c345810367033f5d837b6361b393`，提交说明为 `chore: capture audio-transcriptor seed`。
- 已落库 [SP-001 Final Loop Goal](SP001_SGEGovernanceMigration_LoopGoal.md)、[完整迁移计划](SP001_SGEGovernanceMigration_Plan.md) 与 [Context Bootstrap](SP001_SGEGovernanceMigration_ContextBootstrap.json)。
- 已在 [Big Ideas](../../Big_Ideas.md)、[Stage Plans](../../Stage_Plans.md)、[Sessions](../../Sessions.md)、[Session Index](../../Session_Index.md)、[Current State](../../Current_State.md)、[Artifacts Index](../../Artifacts_Index.md)、[Decisions](../../Decisions.md) 和 [Exceptions](../../Exceptions.md) 建立 S-001 规划控制面。
- 已建立 6 条 Session registry 记录和 [legacy archive 说明](../../Archives/Sessions/Legacy_Execution_Notes.md)；现有派生 [archive manifest](../../Archives/Sessions/archive_manifest.json) 的 Semx/S-485 provenance 被显式限定为迁移前工具遗留，不作为 S-001 provenance 或完成证据。
- 已保留 [Design Review](S001_SGEGovernancePlanningLanding_Design.md)、Design/Builder/Closure lane card 与 prompt，供独立 Validation 核对时序与边界。

## 明确非目标

- 未启动 `S-002`，未复制、改造或声称已建立 repo-local `sge-governed-checkpoints`。
- 未改动 `kb/` canonical truth，也未清理 Semx/KYM/TCO/P00-P17/runtime 历史；这些工作仍属于 S-002 至 S-004。
- 未实现 `audio-transcript` CLI、FFmpeg、Whisper、clean transcript、metadata、cache 或真实音频测试。
- 未发布公共 Skill、未同步全局 Skills、未推送远端、未调用外部 Provider。
- registry 通过只证明当前 Dashboard Session 投影一致，不证明治理框架或音频产品可用。

## Lane 启动与 bootstrap 例外

| Lane | 可定位证据 | 本次作用 | 当前边界 |
| --- | --- | --- | --- |
| Design | [Design card](S001_SGEGovernancePlanningLanding_DesignLaneTaskCard.json)、[Design prompt](S001_SGEGovernancePlanningLanding_DesignLanePrompt.txt)、[Design Review](S001_SGEGovernancePlanningLanding_Design.md) | 在 Builder 关闭前检查状态词、registry provenance、anchor 和验收定义 | 设计结论为有条件通过，不是最终 Validation |
| Builder | [Builder card](S001_SGEGovernancePlanningLanding_BuilderLaneTaskCard.json)、[Builder prompt](S001_SGEGovernancePlanningLanding_BuilderLanePrompt.txt) | 补入 S001-AC-01..03、修正 Decision 状态词并限定 archive manifest 遗留含义 | 只修改 S-001 控制面，不实施迁移 |
| Closure | [Closure card](S001_SGEGovernancePlanningLanding_ClosureLaneTaskCard.json)、[Closure prompt](S001_SGEGovernancePlanningLanding_ClosureLanePrompt.txt)、[Closure Agent Log](../../Agent_Logs/2026-09-01__S-001__closure.md) | 汇总实际证据、OPCM、Scope Delta 与 Validation Handoff | 只生成关闭草案，不给独立 Validation verdict |
| Validation | [独立 Validation Review](S001_SGEGovernancePlanningLanding_ValidationReview.md) | 首轮给出 `fail` 并定位 B-01..B-03；修复后 delta round 逐项关闭 blocker，给出 `pass-with-findings` | 允许 S-001 状态收束；不替代关闭后独立对账，不支持 SP-001 完成 |
| Builder repair | [Repair card](S001_SGEGovernancePlanningLanding_RepairLaneTaskCard.json)、[Repair prompt](S001_SGEGovernancePlanningLanding_RepairLanePrompt.txt)、[Repair Agent Log](../../Agent_Logs/2026-09-01__S-001__builder-repair.md) | 逐字恢复 Raw User Intent、补齐完整计划并修正 Design Delta/语言门表述 | 只修复 B-01..B-03，保持 `S-001=Doing`，不改首轮 Validation Review |

`EX-001` 是一次性 S-001 bootstrap 例外：仓库本地 checkpoint Skill 尚未迁入，因此 Context、lane card 与 closeout-language 使用固定 semx-cli `main@19e967a782e2e95d24475770bc234d86ad7c583e` 的同源脚本。该例外不证明 repo-local Skill 已存在，也不得扩展到 S-002 Builder；S-002 必须建立项目本地入口。

现有 `Dashboard/Archives/Sessions/archive_manifest.json` 仍含 `created_by_session=S-485` 和 semx-cli 绝对源路径。当前 `session_registry.py` 会从既有 manifest 保留这些 provenance 字段；手工改写会造成派生漂移。因此 S-001 只在 [Exceptions](../../Exceptions.md) 中限制其证据含义，实际移除/替代归入 S-004。

## 设计交接

[Design Review](S001_SGEGovernancePlanningLanding_Design.md) 识别的问题已按如下边界处理：Decision 状态已使用四态词汇 `Done`；Sessions 已加入可定位 anchor；Goal 已补入 `S001-AC-01..03`；archive manifest 的遗留 provenance 已在 EX-001 中隔离；closeout 与独立 Validation 已落地。状态收束后的实际表面仍由 post-closeout reconciliation 复核。

Design Delta：`有`。Design Review 原要求人工修正 archive manifest 的 Semx/S-485 provenance；Builder 经实际 registry 行为确认，直接手改该派生表面会造成 projection drift，因此改为在 EX-001 隔离其证据含义，并把确定性移除/替代安排到 S-004。Goal Scope Delta：`无`，因为用户 Goal 本就把 Semx 污染清除、Dashboard tools 适配和删除替代审计放在 S-004；本处理没有删除、降级或延期任何 Goal must-have，也没有扩大 S-001 claim。

该 Design Delta 不需要新增人类 authority，也不触发本轮独立 Semantic Reviewer：它不改变 core/profile、KB truth、runtime/schema、acceptance strictness、Goal completion rule 或 claim ceiling；首轮独立 Validation 已裁决该分类必须如实记录，并要求后续 delta Validation 重算。S-004 的关闭条件是：新 registry/profile 能确定性重建不含 Semx/S-485 当前 provenance 的 archive manifest；`reconcile --check` 与 `validate` 通过；unknown archive/identity 负例按合同失败；身份与绝对路径扫描无未批准残留；删除与替代清单提供可点击证据。在这些条件满足前，该 manifest 只能作为受限 legacy projection，不能作为 S-001 或 Goal 完成证据。

## 验证交接包

独立 Validation 必须完整读取并重算，不得采信 producer 自报：

1. 用户授权边界、[Final Loop Goal](SP001_SGEGovernanceMigration_LoopGoal.md)、[迁移计划](SP001_SGEGovernanceMigration_Plan.md) 与 [Context Bootstrap](SP001_SGEGovernanceMigration_ContextBootstrap.json)；
2. [Design Review](S001_SGEGovernancePlanningLanding_Design.md)、所有 S-001 lane cards/prompts、Closure Agent Log 和本 closeout；
3. [Big Ideas](../../Big_Ideas.md)、[Stage Plans](../../Stage_Plans.md)、[Sessions](../../Sessions.md)、[Session Index](../../Session_Index.md)、[Current State](../../Current_State.md)、[Artifacts Index](../../Artifacts_Index.md)、[Decisions](../../Decisions.md)、[Exceptions](../../Exceptions.md) 与 archive surfaces；
4. seed commit `389087ef01d1c345810367033f5d837b6361b393`、当前原始设计和 seed 中原始设计的 SHA-256，以及最终 tracked/untracked diff；
5. Context validator、registry `reconcile --check`、registry `validate`、closeout-language gate 的实际输出；
6. 逐项检查下面 OPCM、Scope Delta、`S-001` 与 parent Goal 的状态分离、DKG evidence gap 以及最终 closeout wording。

独立 Validation 结论：首轮 `fail` 后，修复后的 delta round 为 `pass-with-findings`。这允许把 `S-001` 改为 `Done`，但不支持把 `SP-001`、治理迁移或产品写成完成；关闭后的最终状态仍须由 post-closeout reconciliation 独立绑定。

`Closeout language verdict`：`pass`。已使用固定 semx-cli source 的 `guardrail_checklist.py --mode closeout-language` 对本文件执行，输出为 `Closeout language check passed`。该结果只证明当前版本的中文标题与英文状态解释符合语言门禁，仍须由独立 Validation 确认其绑定的是实际关闭版本。

## 原始计划覆盖矩阵（OPCM）

| ID | 原始要求 | 可观察验收判定 | 精确源文件证据 | 实际结果 | 状态 | 阻断 / 例外 | Owner / Lane / 时序 | Claim ceiling | Parent / Closeout 吸收状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MH-01 | 建立整理前 Git 种子基线 | root seed 可定位且原始设计可恢复 | [Goal Ledger](SP001_SGEGovernanceMigration_LoopGoal.md)、[历史设计 locator](Tombstones/Removed_Audio_Transcriptor_Design.md) | seed commit 已存在；当时 Validation 记录了字节一致；当前仓库已删除产品文件，不再主张 current-byte equality | S-001 landed | 通过 Git locator 恢复，不把产品内容加入当前 repo | Orchestrator / S-001，Builder 前建立 | 只证明可恢复 seed | 本 closeout 已吸收；parent Goal 仍未终止 |
| MH-02 | 固定 semx-cli revision 与复制 Skill provenance | source manifest 覆盖每个复制对象 | [迁移计划 S-002](SP001_SGEGovernanceMigration_Plan.md) | S-001 仅固定 bootstrap source revision；尚无逐文件 source manifest | Parent 未启动 | 计划内依赖 S-002 | S-002 Design+Builder | 不得声称复制来源已完整冻结 | 本 closeout保留为后续，不吸收完成 |
| MH-03 | 建立通用核心和项目 profile | Skill/profile/schema/正反例通过 | [Goal Session DAG](SP001_SGEGovernanceMigration_LoopGoal.md)、[迁移计划 S-002](SP001_SGEGovernanceMigration_Plan.md) | 未建立 repo-local core/profile | Parent 未启动 | EX-001 只解决 S-001 bootstrap，不替代实现 | S-002 | 不得声称治理核心存在 | 后续 S-002 |
| MH-04 | 迁移适用 Skills、schemas、scripts 与 gates | 迁移清单落地并验收 | [迁移计划 S-003 与取舍表](SP001_SGEGovernanceMigration_Plan.md) | 仅落库取舍和阶段计划，没有复制 Skill | Parent 未启动 | 无 | S-003 | 不得声称 Skill 已迁移 | 后续 S-003 |
| MH-05 | 调整 KB、Dashboard、AGENTS 和工具 truth/authority | authority 路径与分层测试通过 | [迁移计划 S-004](SP001_SGEGovernanceMigration_Plan.md)、[Current State](../../Current_State.md) | 只建立 Dashboard execution-memory 入口；KB/AGENTS/tools 尚未适配 | Parent 未启动 | S-001 Dashboard 不能冒充 canonical truth 迁移 | S-004 | 只证明规划控制面已落库 | 后续 S-004 |
| MH-06 | 删除无意义 Semx/KYM/TCO/P00-P17/runtime 实践并记录理由 | 删除清单、替代机制和身份扫描通过 | [迁移取舍表](SP001_SGEGovernanceMigration_Plan.md)、[DEC-004](../../Decisions.md) | 已记录取舍原则，尚未删除；legacy manifest 污染仍可见 | Parent 未启动 | EX-001 隔离 provenance；S-004 执行删除 | S-004 | 不得声称身份污染已清除 | 后续 S-004 |
| MH-07 | 原始产品设计边界，不冒充设计冻结/runtime | seed 中历史设计可定位；当前 repo 不恢复产品文件 | [历史设计 locator](Tombstones/Removed_Audio_Transcriptor_Design.md)、[Goal 非目标](SP001_SGEGovernanceMigration_LoopGoal.md) | 当时摘要记录保留；当前仓库已删除产品文件并明确非目标 | S-001 历史边界满足，Goal 全程持续 | 不以 tombstone 替代原内容 | 全程 / Validation | 不证明设计正确、冻结或产品可用 | 本 closeout已吸收边界；parent 持续检查 |
| MH-08 | 身份、schema、ERBE、Goal/lane/context、registry、DKG、语言 gates | 维护中的 acceptance runner 全绿 | [Goal Ledger](SP001_SGEGovernanceMigration_LoopGoal.md)、[计划验收](SP001_SGEGovernanceMigration_Plan.md) | S-001 context/lane bootstrap 与 registry 可运行；产品化 schema/ERBE/DKG 等未验收 | Parent 未启动 | DKG 缺 `Dashboard/Quality_Metrics.md`；归入 S-004，不作为 S-001 证据 | S-005 / Validation | 仅可引用 S-001 局部门禁 | 后续 S-002..S-005 |
| MH-09 | 保留 Design、Builder、独立 Validation、Closure 与触发式 Semantic 时序 | cards/logs/verdict 可定位 | [Design Review](S001_SGEGovernancePlanningLanding_Design.md)、[lane artifacts](../../Artifacts_Index.md)、[独立 Validation](S001_SGEGovernancePlanningLanding_ValidationReview.md) | Design→Builder→Closure→Validation→repair→delta Validation 可定位；本轮 Semantic trigger 裁决为不触发，Goal 级 Semantic 仍由后续 Session 承担 | S-001 landed，Parent 未启动 | 初始 Design/Builder 无实时 Agent Log 的非阻断 finding 保留，不伪造回填 | Orchestrator + lanes / 全程 | 只证明 S-001 有界时序 | 本 closeout 已吸收；Goal 级要求继续保留 |
| MH-10 | 中文 closeout、OPCM、Scope Delta、KB/Dashboard review 与 post-closeout reconciliation | 最终 artifact 覆盖最终状态与 diff | [Goal Ledger](SP001_SGEGovernanceMigration_LoopGoal.md)、本 closeout | S-001 已形成中文 closeout 草案、OPCM、Scope Delta 和 review；closeout-language 已通过；Goal 级最终 closeout/reconciliation 未启动 | S-001 候选，Parent 未启动 | S-001 仍需修复后的独立 delta Validation 和最终对账；语言门已通过，不再列为 pending | Closure+Validation / S-001，S-006 | 只支持 S-001 规划落库 | S-001 候选已吸收；Goal 级留给 S-006 |
| S001-AC-01 | Goal、Plan、Context 与 Dashboard entry 可定位且未启动 S-002 | 必需 artifacts/父面存在且措辞保持边界 | [Goal AC](SP001_SGEGovernanceMigration_LoopGoal.md)、[Artifacts Index](../../Artifacts_Index.md)、[Sessions](../../Sessions.md) | 三个主 artifacts 和父面均存在；Raw Intent 与完整 Plan 已由 delta Validation 复核；S-002 保持 `To do` | landed | 关闭后的文件集由 post-closeout reconciliation 再绑定 | Builder→Closure→Validation→repair→delta Validation | 只证明规划合同持久化 | 本 closeout已吸收 |
| S001-AC-02 | 四态 Status、anchor 与 registry 两命令通过 | Status 合法、链接可定位、两命令返回零 | [Dashboard Rules](../../Rules.md)、[Session Index](../../Session_Index.md)、[Sessions](../../Sessions.md) | Decision/Exception/Session 使用合法状态；6 个 anchor 存在；状态收束后 registry check/validate 重跑通过 | landed | registry 只证明 Session projection 一致 | Orchestrator→post-closeout Validation | 只证明 Session projection 一致 | 本 closeout已吸收 |
| S001-AC-03 | seed/design/lane/closeout/Validation/diff 支持有界关闭 | 历史证据与当前删除边界均可定位且无越界主张 | [Goal AC](SP001_SGEGovernanceMigration_LoopGoal.md)、本 closeout、[历史设计 locator](Tombstones/Removed_Audio_Transcriptor_Design.md)、[独立 Validation](S001_SGEGovernancePlanningLanding_ValidationReview.md) | S-001 当时的规划证据保留；当前产品文件已删除，最终状态由 S-015 重新对账 | 历史状态可定位 | 不用 tombstone 证明原内容或当前字节 | Closure→Validation→S-015 reconciliation | 只允许 S-001 历史规划结论 | 本 closeout吸收历史关闭，当前证据由 S-015 绑定 |

## Scope Delta 审计

- 原始 must-have 删除：无。
- 原始 must-have 降级、替换或延期：无未批准变更；MH-02..MH-10 的 parent Goal 工作仍按固定 Session DAG 保留，S-001 只记录其计划状态。
- 新增但不缩窄原范围：Goal 中补入 `S001-AC-01..03`，用于把 S-001 的落库关闭条件变成可观察判定。
- 证据边界修正：未手工改写 registry 派生 manifest 的 Semx/S-485 provenance，而是在 EX-001 中声明其 legacy 含义并把工具适配纳入 S-004。这不是接受身份污染为 Goal 完成，而是避免在 S-001 伪造 registry provenance。
- Design Delta：`有`，即把 Design Review 的“本轮人工修正 manifest”替换为“EX-001 隔离证据含义并由 S-004 确定性移除/替代”；Goal Scope Delta：`无`，因为清除该污染及工具适配仍由原 DAG 的 S-004 完整承担。首轮独立 Validation 要求如实记录此分类；本轮无需新增人类批准或 Semantic Reviewer verdict。
- 执行拓扑：Design、Builder、Closure 使用独立 lane cards；独立 Validation 仍是硬门。没有用主线程自检替换独立 Validation 的批准 Scope Delta。

Scope Delta verdict：`无未批准 Scope Delta；S-001 只按规划落库范围关闭，parent Goal 保持未启动。`

## 证据

- 任务合同：[Final Loop Goal](SP001_SGEGovernanceMigration_LoopGoal.md)、[迁移计划](SP001_SGEGovernanceMigration_Plan.md)、[Context Bootstrap](SP001_SGEGovernanceMigration_ContextBootstrap.json)。
- 设计与 lane：[Design Review](S001_SGEGovernancePlanningLanding_Design.md)、[Design card](S001_SGEGovernancePlanningLanding_DesignLaneTaskCard.json)、[Builder card](S001_SGEGovernancePlanningLanding_BuilderLaneTaskCard.json)、[Closure card](S001_SGEGovernancePlanningLanding_ClosureLaneTaskCard.json)。
- Dashboard 状态：[Big Ideas](../../Big_Ideas.md)、[Stage Plans](../../Stage_Plans.md)、[Sessions](../../Sessions.md)、[Session Index](../../Session_Index.md)、[Current State](../../Current_State.md)、[Artifacts Index](../../Artifacts_Index.md)、[Decisions](../../Decisions.md)、[Exceptions](../../Exceptions.md)。
- 产品设计边界：[历史设计 locator](Tombstones/Removed_Audio_Transcriptor_Design.md)记录 seed 中原路径与历史摘要；当前仓库已删除产品文件，不再主张 seed 与 current SHA-256 相等。
- 机器证据入口：registry 的派生 [Session Index](../../Session_Index.md) 与 [archive manifest](../../Archives/Sessions/archive_manifest.json)；具体命令输出须由独立 Validation 从工作树重算。

## 运行的门禁

| 门禁 | 当前结果 | 证明范围 | 不证明范围 |
| --- | --- | --- | --- |
| Context Bootstrap validate | `pass`（固定 semx-cli source validator；repair 后重跑） | S-001 implementation packet 结构有效，且 Raw User Intent 已恢复为逐字 authority | validator 的结构 PASS 本身不证明逐字保真，也不证明 repo-local checkpoint 已迁移 |
| Closure lane card validate | `pass`，card SHA-256=`3af2d5c151b47eed233613400e5f3dd5d63fcce01db474a2ee8c9d3ed25cc5ea` | 本 lane 输入和 write scope 未漂移 | closeout 内容正确或独立验收通过 |
| Session registry reconcile check | `pass`，6 records，无 drift | Sessions/Index/archive 当前可确定性对账 | SGE/产品功能正确 |
| Session registry validate | `pass`，6 records | 当前 registry 结构与 identity 一致 | archive manifest 的 legacy provenance 已适配 |
| 原始设计摘要对比 | `pass` | 当前设计字节与 seed 中设计字节相同 | 产品设计已冻结或实现 |
| Dashboard DKG | `not_generated` | 生成器存在，但当前缺少其输入 `Dashboard/Quality_Metrics.md` | 不能作为 S-001 完成证据；由 S-004 工具适配处理 |
| Closeout language | `pass`（固定 semx-cli source 同一门禁） | 当前版本的中文标题和英文状态解释符合语言门禁 | 不替代独立 Validation，也不自动关闭 S-001 |
| Independent Validation | 首轮 `fail`；修复后 delta Validation `pass-with-findings` | B-01..B-03 已关闭并授权状态收束；中文含义是当前合同通过但仍保留非阻断 findings | 不替代关闭后独立对账，不支持 SP-001/Goal 完成 |

## 语义复核

S-001 没有改变通用 SGE core、project profile、KB truth placement、runtime/schema 或 gate strictness；这些高语义风险对象尚未进入实现。因此本 Session 不产生 Goal 级 Semantic Reviewer 通过结论。archive manifest 处理属于 Design Delta 但不是 Goal Scope Delta；首轮独立 Validation 已裁决本轮只需准确记录并由 delta Validation 重算，不需要单独 Semantic Reviewer。后续 S-002 对 core/profile/ERBE 冻结时必须触发 pre-Builder Semantic Review，S-005/S-006 还必须覆盖实际最终候选与 closeout。

状态词压缩测试：如果未来 Agent 只看到“S-001 Done”，它仍可能误读为迁移完成，因此任何最终状态面必须同时保留“仅规划落库；SP-001 迁移未启动”。本 closeout 标题和结论均维持该限制。

## KB / Dashboard 复核

- KB 判断：本次不更新 `kb/`。稳定治理 truth 尚未冻结；原始产品设计保持唯一产品来源且字节不变。未来稳定 profile、SGC、ERBE、Goal Effect 等规则按 S-002/S-004 的 Contract Delta Scan 进入 `kb/data/`。
- Dashboard 判断：本次必须更新，因为 Goal、Stage Plan、Session、状态、决策、例外和 closeout evidence 都属于 execution memory；当前已写入相应父面。
- Contract Delta Scan：Final Loop Goal 与迁移计划中的稳定候选规则当前分类为 `deferred session`，由 S-002 冻结、S-003 实现、S-004 决定 promote-to-KB；不能从本 Dashboard artifact 直接冒充 canonical truth。
- DKG 判断：本次变更影响 Dashboard KG，但复制框架缺少 `Dashboard/Quality_Metrics.md`，现有生成器无法完成 projection。该 evidence gap 已明确归入 S-004；在 S-001 不生成虚假的 DKG 输出，也不因此声称 Goal 级 DKG 验收通过。

## 验证结论

S-001 关闭结论：独立 delta Validation 为 `pass-with-findings`，中文含义是 B-01..B-03 已关闭、允许有界状态收束，现有非阻断 finding 不改变 S-001 当前合同。关闭后的实际状态与完整 diff 由 [Post-closeout 独立对账](S001_SGEGovernancePlanningLanding_PostCloseoutReconciliation.md) 给出最终 verdict；该 artifact 是最终关闭证据，不能由 Closure 自检或本段摘要替代。

当前只允许写“`S-001 Done` 表示规划落库完成；`SP-001` 迁移未启动”。仍禁止写 `Goal complete`、`SP-001 完成`、`治理迁移完成` 或 `audio-transcriptor 可用`。`BI-001` 与 `SP-001` 继续保持 `To do`。

## 后续候选与 Loop continuation scan

- `goal_terminal=false`
- `next_session=S-002`
- `next_session_ready=false`
- `human_decision_required=true`

这里的 `human_decision_required=true` 不是要求用户再次批准 S-001 closeout，而是遵循本次明确授权边界：只有用户后续明确启动 `SP-001`，S-002 才 ready。S-001 状态已收束；post-closeout reconciliation 通过后停在“已落库、迁移未启动”。
