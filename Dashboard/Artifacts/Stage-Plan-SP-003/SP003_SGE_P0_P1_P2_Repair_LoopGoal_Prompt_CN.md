/goal

请在当前仓库 `/Users/xiaomei/Documents/projects/sge-governance-skill` 中，使用 repo-local `/sge-governed-checkpoints` 启动并连续执行一个受治理的 Loop Goal，逐项设计、修复和验证下列已经确认的 P0、P1、P2 问题。

本 Goal 暂不设计、执行或要求“两个不同 Agent 的对比验收测试”。允许使用单仓库 deterministic fixtures、能力矩阵样例和独立 Validation 验证修复本身，但这些证据不得表述为真实 cross-Agent compatibility、consistency 或 UAT 已通过。

本轮显式授权 Codex 按需使用 subagents / delegation / parallel agent work；是否启用由 Multi-Agent Activation Gate 决定。Orchestrator 默认只负责 control plane。所有 non-trivial lane 在下发前必须验证 `lane_task_card_v1`，由 `lane_task_card.py render` 生成 delegation prompt，并由接收 Agent校验 expected card digest。

本 Prompt 被用户发出即构成本 Goal 在下述 repo-local scope 内的 C0 执行授权；不包含破坏性操作、外部仓库 mutation、push、tag、release、publish 或未列明的 Scope Delta。开始时检查 Git status，保留既有修改，不得擅自清理。可以按仓库规则创建 `codex/` 前缀的本地分支/工作树和本地提交。

## 0. Prompt provenance 与批准的 Scope Delta

本 Prompt 的设计依据是当前用户提供的 Agent 1/Agent 2 行为记录、前一版 P0/P1/P2 审计、上一版跨 Agent 修复 Goal Prompt、当前 `AGENTS.md`、repo-local `sge-governed-checkpoints`、`define-goal`、`pdi`、bootstrap/install/public payload、新手 first-Goal 路径和 Dashboard 当前状态。

本次用户明确批准以下 Scope Delta：

- 删除上一版 Goal 中“两个真实且不同 Agent product/runtime 的对比 UAT”及其 completion blocker；
- 不在本 Goal 内设计 cross-Agent comparison harness、identity predicate 或外部 UAT package；
- 保留单仓库 fixtures、负例、contract tests 和独立 Validation，因为它们用于证明 P0/P1/P2 修复，而不是证明跨 Agent 一致性；
- 该删除不允许进一步缩窄 P0/P1/P2 的设计、实现、验证、文档、KB/Dashboard 和防复发要求；
- 不自动建立 cross-Agent UAT 后续 Session。只有用户以后单独提出时，才重新 intake。

Prompt status：`revised_goal_prompt_ready_for_orchestrator_R0`。R0 仍必须基于当前 revision/digest 建立正式 Read Manifest、Goal artifact、独立 Goal Review、Goal Patch 和 resolved Final Goal；本聊天 Prompt 本身不冒充已落库的 Final Goal。

CG skipped: no CG input provided

## 1. Goal Mission

把以下八个问题逐一完成 PDI 闭环：原始 finding → 独立核验 → disposition → root cause → bounded design → implementation → focused verification → regression/prevention → closeout。任何问题不得只靠补一句说明、增加一个未执行 schema、生成一份自报 receipt 或移动文本位置来声称修复。

### P0

- P0-01：缺少确定性的首任务路由；空白 bootstrap 仓库没有 Goal 时，不同 Agent 会自行决定是否创建 Goal/Session、直接 Builder 或停下询问。
- P0-02：缺少机器可核验的 conformance receipt；Agent 自述“已运行/已验证”无法证明门禁、topology、最终 Validation 和 claim ceiling。
- P0-03：缺少 capability/dependency/version preflight；SGE core、全局可选 Skill、subagent、Git、Dashboard/registry tooling 的差异可能被静默消费。
- P0-04：缺少 subagent/lane 失败后的确定性 fallback；重试、缩小 card、重新派发、Orchestrator takeover、human approval 和 claim 降级边界不清楚。

### P1

- P1-01：缺少 `initial_kb_bootstrap` 固定 recipe；Agent 需要自行组合 authority、Goal、lane、KB truth、验证和 closeout。
- P1-02：缺少最小可见 checkpoint 合同；一种 Agent 输出太少无法审计，另一种 Agent 大量播报术语但仍不可核验。
- P1-03：lane 生命周期与 closeout/final Validation 时序不够明确；“lane started”可能被误解为职责完成，Closure 可能过早运行，pre-closeout Validation 可能冒充 final verdict。

### P2

- P2-01：核心 Skill/default read surface 过长且规则分散，过度依赖 Agent 主动理解和组合；需要 kernel + task recipe + references 分层，并证明没有丢失 hard gates。

## 2. Source authority、必读范围与边界

R0 必须运行并保存：

- `workflow_contract.py --stage full`；
- Task Intake Evaluation；
- implementation profile Context Bootstrap 及机器校验；
- SGC v1；
- Goal Conformance；
- Goal Agent Quality Guard；
- Multi-Agent Activation Gate；
- ERBE applicability；
- Semantic Reviewer trigger scan。

正式 Read Manifest 至少覆盖：

- 本 Prompt及其八项 finding；
- `AGENTS.md`；
- `.codex/skills/sge-governed-checkpoints/SKILL.md`；
- 当前可用 `pdi` Skill 的 `SKILL.md`；若执行环境没有该 Skill，必须记录缺失，并在本 Goal 的 PDI artifact 中完整实现同等逐项闭环，不得因此跳过 finding disposition/root cause/prevention；
- `references/checklists.md`、`references/context-efficient-goal-validation.md`；
- `scripts/`、`schemas/`、`agents/openai.yaml`；
- `tools/sge_public.py`、`public_export_manifest_v1.json`；
- `docs/Agent_Setup_Prompt_CN.md`、`Beginner_Guide_CN.md`、`Quick_Start_CN.md`；
- `extensions/orchestrator_profile_v1.json`、`extensions/registry_v1.json`；
- 相关 canonical KB strategy；
- Dashboard Current State、Stage Plans、Sessions、Rules、Methodology及相关历史 artifacts/logs；
- 当前 tests、doctor、bootstrap/install/upgrade/export/verify 和现有单仓 UAT/contract fixtures。

如已有重叠 Goal/SP/Session，优先复用；需要 supersede 时必须取得人类批准。没有重叠项时，按 registry 分配新的 Parent/Session IDs，不得按裸 ID first-wins。

稳定治理 truth、状态机、receipt/fallback 语义进入 `kb/data/` canonical JSON，并确定性渲染 reader docs。Goal、Session、finding disposition、执行状态、例外、验证和 closeout 留在 Dashboard。不得把 Dashboard 或测试样例本身提升为 canonical law。

## 3. 原始 must-have ledger

Builder 前把以下 must-have 逐项写入 Goal Scope Ledger；每行必须有 source pointer、observable acceptance predicate、owner/lane、status、evidence、blocker/exception 和 claim ceiling。

- MH-01：P0-01 独立完成 disposition、root cause、设计、实现、正负测试和防复发更新。
- MH-02：P0-02 独立完成 disposition、root cause、设计、实现、正负测试和防复发更新。
- MH-03：P0-03 独立完成 disposition、root cause、设计、实现、正负测试和防复发更新。
- MH-04：P0-04 独立完成 disposition、root cause、设计、实现、正负测试和防复发更新。
- MH-05：P1-01 独立完成 disposition、root cause、设计、实现、正负测试和防复发更新。
- MH-06：P1-02 独立完成 disposition、root cause、设计、实现、正负测试和防复发更新。
- MH-07：P1-03 独立完成 disposition、root cause、设计、实现、正负测试和防复发更新。
- MH-08：P2-01 独立完成 disposition、root cause、设计、实现、measurement、regression 和防复发更新。
- MH-09：对八项修复产生的必要 bootstrap/install/docs/extensions/public-manifest/KB/Dashboard/BDD 同步做一致性收束；它是必要 contract consequence，不得扩大为公共发布或跨 Agent UAT。
- MH-10：最终独立 Validation、Semantic Review、OPCM、closeout-language、registry、public candidate/doctor/export/verify 和 post-closeout reconciliation 覆盖实际 final state/diff。

八个 finding 必须各自有唯一 PDI disposition：`accept / accept_with_revision / reject / needs_evidence`，以及终态：`resolved / resolved_with_bounds / rejected / blocked`。共享根因可以复用证据，但不得把多个 finding 合并成一行“整体已修复”。

任何删除、合并、降级、延期、改名、换 authority 验证或改成 non-goal 都是新的 Scope Delta，需要人类批准或明确 blocker/termination。

## 4. ERBE specification-first gate

本 Goal 会改变首任务路由、lane/fallback 状态机、receipt schema、acceptance predicate 和 closeout 时序，因此 ERBE applicability=`required`。

R0/R1 dominant Builder 前必须冻结 machine-readable Contract/Cases，包括：state axes、predicates、invariants、counterexamples、forbidden collapses、oracle owner、write exclusions 和 claim ceiling。至少覆盖：

- `goal_presence`、`task_class`、`route`；
- `core_candidate_identity`、`optional_dependency_state`、`agent_capability_state`；
- `lane_state`、`fallback_state`、`actual_builder_topology`；
- `evidence_state`、`receipt_verdict`；
- `closeout_phase`、`validation_binding_state`；
- `context_baseline`、`conditional_reread`、`coverage_state`。

最低负例：

- 无 Goal 的 bootstrap 仓库静默创建 Session 并开始 Builder；
- 静默使用未随 core 安装的全局 Skill；
- 只输出“context bootstrap completed”但没有有效 packet；
- 只说“多 Agent 已启动”但没有 card/actual topology/lane state；
- Builder subagent 无输出后 Orchestrator 静默接管；
- receipt 仅凭自然语言、自报 verdict、handoff 或绿色单测通过；
- Validation 在实际 closeout/final diff 前完成，却用于最终 `done`；
- 通过移动或压缩文本达到 size 指标，但 trigger/coverage 下降或 conditional reread 反弹；
- 单仓 fixtures 通过后声称 cross-Agent validated。

可信 RED 必须在未修复实现上以预期 failure fingerprint 失败；import/path/fixture 错误只能记 `error`。GREEN 必须复用相同 frozen case identity，并由独立 Validation 从 durable inputs 重算。Builder 不得修改 frozen Contract/Cases/expected/RED/claim ceiling；变化必须走 Contract Patch、Scope Delta 和 re-RED。

## 5. Session DAG：逐问题闭环

由 Orchestrator 映射为合法 Dashboard IDs；逻辑顺序固定如下：

1. R0 — Goal landing 与 full baseline：Read Manifest、重复工作审计、PDI issue queue、Scope Ledger、Context Bootstrap、ERBE applicability、Goal Review/Patch/resolved Final Goal。
2. R1 — P0-01 首任务 classifier 与 Goal-missing router。
3. R2 — P0-03 capability/dependency/version preflight。
4. R3 — P0-04 subagent/lane failure fallback 与 actual-topology evidence。
5. R4 — P0-02 conformance receipt schema、producer、validator 与 fail-closed cases；必须消费 R1-R3 的稳定接口。
6. R5 — P1-01 core `initial_kb_bootstrap` recipe；不得依赖外部辅助 Skill，optional Skill 只能作为显式 adapter。
7. R6 — P1-03 lane lifecycle/readiness barriers 与两阶段 closeout/final reconciliation。
8. R7 — P1-02 五个最小可见 checkpoint，并绑定 R4 receipt 与 R6 lifecycle，不以固定聊天文案替代结构证据。
9. R8 — P2-01 kernel + task recipe + references 分层、default read surface 压缩和 hard-gate coverage regression。
10. R9 — 必要 surfaces 一致性收束、完整 Validation/Semantic/OPCM/closeout/post-closeout reconciliation。

依赖为：`R0 → R1 → R2 → R3 → R4 → R5 → R6 → R7 → R8 → R9`。每个问题必须先形成独立 Design/PDI artifact 和验收案例，再开始对应 Builder。相邻 Session 可复用 frozen baseline/snapshot，但不得合并八项 finding 的独立 verdict。

每个 Session closeout 后必须记录：`goal_terminal`、`next_session`、`next_session_ready`、`human_decision_required`。当 Goal 未终止、下一 Session ready 且无需人类决定时，禁止发送 final answer或询问“是否继续”，必须自动进入下一 Session。

## 6. Acceptance Criteria

- AC-01 / P0-01：classifier 对 frozen first-task cases 输出 schema-valid 的 task class、goal state、route、required gates/lanes、semantic posture、maximum claim 和 reason；Goal missing、existing、conflict 均有正负例。
- AC-02 / P0-02：machine-readable receipt 记录 task/context/lane/topology/must-have/Scope Delta/gates/Validation/closeout/registry/KB-Dashboard/claim/evidence gap；每个 mandatory evidence 缺失都有独立 fail-closed 负例。
- AC-03 / P0-03：preflight 输出 core candidate digest/version、可选 Skill identity、subagent/Git/shell/filesystem/Dashboard tooling capability、required/optional 分类、fallback 和 claim impact；未安装能力不得被描述为 core capability。
- AC-04 / P0-04：subagent unavailable、无输出、card drift、execution failure、重试耗尽和 Orchestrator takeover 均有状态转移、重试上限、human trigger、exception evidence 和 claim impact；补偿 Validation 不得抹去实际 topology。
- AC-05 / P1-01：`initial_kb_bootstrap` recipe 在无外部辅助 Skill的 clean bootstrap fixture 上可运行；明确 authority classification、Goal route、最小交付、optional adapter、required lanes、验证、closeout 和产品实现/发布非目标。
- AC-06 / P1-02：用户可见层只要求五类 checkpoint：intake/class/claim、Goal/Session/lane plan、pre-Builder frozen handoff、independent Validation binding、final receipt/non-goals；每类可定位，且无需把完整日志复制到聊天。
- AC-07 / P1-03：lane 至少具有 `registered / ready / running / completed / evidence_bound / failed` 状态及合法转换；Design→Builder→Validation→Closure readiness barrier 和 closeout draft→Validation→repair→final closeout→post-closeout reconciliation 可由负例验证。
- AC-08 / P2-01：R0 冻结代表性 first-task fixtures、baseline、重复测量方法和 materiality predicate；同时测 mandatory injected bytes/可用 token estimate、实际 reads/conditional expansion、跨 lane 重复稳定块和 trigger/hard-gate coverage。所有 fixture 必须呈正向改善、改善下界超过测量噪声、不得被 conditional reread 反弹抵消；50% reduction 仅是 stretch target，不是 completion blocker。
- AC-09：所有既有 hard gates 和 deterministic/agent-evaluated triggers 有逐项 coverage mapping 和 regression；压缩不得通过删除规则、降低 applicability、隐藏 evidence gap 或把内容搬到默认仍全量读取的文件实现。
- AC-10：bootstrap 产物、install record、core payload、optional extension declaration、新手文档和真实命令入口一致；不存在 core 未安装却被 recipe 默认要求的工具。
- AC-11：所有相关 focused/contract/schema/negative tests、public candidate/projection tests、KB render check、Git diff check、export/verify 通过；有效 candidate 的 doctor exit code=0，无效 candidate 按 frozen fingerprint 非零失败。Dashboard surface 有变化时 registry reconcile --check 与 validate 必须通过。
- AC-12：八项 finding 分别具有 disposition、root cause、Design、implementation、verification、prevention、residual risk 和独立终态；没有“整体 closeout”代替逐项证据。
- AC-13：独立 Validation 同时检查本 Prompt、resolved Goal、MH-01..MH-10、AC-01..AC-15、实际实现、closeout、最终 KB/Dashboard 和完整 diff。
- AC-14：Semantic Reviewer 给出 `Design Freeze Validity` 与 `Implementation Entry Readiness`，并检查 classifier/receipt 是否演化为 God Object、半 schema DSL、治理膨胀或 misplaced truth carrier。
- AC-15：最终 OPCM 对 MH-01..MH-10 与 AC-01..AC-15 逐项列出原始要求、observable predicate、精确源文件链接、实际结果、状态、blocker/exception、owner/timing、claim ceiling 和 parent/Closeout absorption。

## 7. 设计与实施约束

- 优先修改 authoritative source；不得手改生成 Markdown 代替 JSON/source 修复。
- 开始每个 finding 前先核验并给 disposition；若 `reject`，只有取得人类批准并记为 `not applicable with reason` 后才可不实施；若 `needs_evidence`，终态只能是 `blocked`，不得写 `resolved` 或用其他 finding 的实现代替。不能为了满足任务数量强行实现，也不能由 Orchestrator 单方面缩小分母。
- 先审计现有 `workflow_contract.py`、`context_bootstrap.py`、`lane_task_card.py`、profile/extension contract，再决定扩展或新增入口；不得无审计再造平行 orchestrator。
- receipt 只能是 evidence index/verdict carrier，不得混合 semantic law、runtime truth、Validation result 和 governance approval。
- classifier 不得硬编码 Agent 品牌、模型或具体产品；本 Goal 不验证不同 Agent 的真实一致性。
- core recipe 不得静默使用 `doc-system-kb-builder` 等全局 Skill；可选能力必须由 preflight 声明，并保持 required governance contract 不变。
- 不用固定聊天措辞替代结构 contract；五个 checkpoint 规定最小信息，不规定逐字输出。
- 新 schema 首次落地可用 `v1`，但必须记录版本理由；既有 schema/CLI 改动需要 compatibility、migration 和 rollback 判断。
- 若改变 maintained non-unit gate、validator 或 enumerable case，执行 BDD Sync；reader-facing cards 必须保存在受版本控制路径。
- 只同步完成八项修复所必需的 bootstrap/install/docs/extensions/public manifest；不得把 Goal 扩大为公共发布、完整 distribution architecture 或其他产品能力。

## 8. Lane、Validation 与 Semantic Review

默认启动 Design、Builder、Validation、Closure；涉及 routing/state machine/schema/claim/closeout 语义的 Session 必须运行 Semantic trigger scan，并在 R0/R9 启动 Semantic Reviewer。若默认 lane 未启动，closeout 记录 `Single-Agent Exception`、原因、风险、补偿检查和 claim impact。

Validation Agent 给 verdict 前必须运行：

`python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode validation-agent`

并应用固定 read-mostly prompt。Validation Handoff 必须包含 claimed scope、semantic change、non-goals、changed files、gates/tests、evidence、known risks、KB/Dashboard impact 和 Closeout language verdict。

最终 passing verdict 必须来自唯一、可定位、无冲突的独立 reviewer/source，并覆盖实际 closeout、最终 KB/Dashboard、完整 final diff 和原始八项 finding。Builder/Orchestrator 自报、handoff、Semantic Review 或绿色 tests 均不能替代它。

## 9. 明确非目标

- 不运行、设计或要求两个不同 Agent 的 comparison UAT。
- 不声明任何真实 cross-Agent compatibility、consistency、portability 或 production readiness。
- 不要求不同 Agent 生成相同业务 KB 内容。
- 不实现 audio-transcriptor 或其他产品 KB/运行时。
- 不新增跨 Agent UAT follow-on Session，除非用户以后单独授权。
- 不执行外部 push、tag、release、publish 或远端 mutation。
- 不借修复名义启用 SGC v2/v3、通用数值评分或无关 schema/runtime 改造。

## 10. Claim ceiling 与禁止措辞

本 Goal 的最大声明为：

`P0-01..P0-04、P1-01..P1-03、P2-01 已在本仓库完成逐项设计、实现、deterministic/contract 验证和独立 final-state Validation；未进行两个不同 Agent 的对比验收，因此不证明真实 cross-Agent 一致性或兼容性。`

若只有部分 finding 完成，必须逐项列出 `resolved / resolved_with_bounds / rejected / blocked`，不得写“P0/P1/P2 已整体完成”。

禁止：

- 仅凭 schema/file existence 写 `validated`；
- 仅凭单 Agent fixtures 写 `cross-Agent proven`；
- 仅凭 Skill 文本缩短写“认知负担已降低”；
- 仅凭 public export 写 `released`；
- 仅凭单个 Session closeout 写 `Goal complete`。

## 11. Human authority checkpoints 与终止条件

仅在以下情况暂停并一次性请求人类决定：

- 需要删除、替换、合并或降级八项 finding、MH-01..MH-10 或 AC-01..AC-15；
- 发现必须扩展到 cross-Agent UAT、外部 provider/Agent runtime 或用户明确排除的范围；此时只报告建议，不得扩 scope；
- 需要破坏性操作、外部仓库写入、发布、许可证/权利决定；
- 已有 active Goal 无法安全复用，需要 supersede；
- 同一恢复条件连续失败超过三次；
- 用户明确暂停。

普通测试失败、可修复 card/digest drift、可重建 baseline、缺少尚未创建的 Session artifact 或 subagent 首次无输出，不是要求用户回复“继续”的理由。

## 12. Completion rule

只有同时满足以下条件才允许 `goal_terminal=true`：

1. 八项 finding 均有独立 PDI disposition 和终态；所有 accepted finding 均有 Design、implementation、verification 和 prevention evidence；
2. MH-01..MH-10 与 AC-01..AC-15 全部 landed，或有明确 human-approved deferral、not-applicable 或 blocker termination；
3. ERBE Contract/Cases 有可信 RED、same-identity GREEN 和独立 Validation；
4. P0/P1/P2 修复及必要 contract consequence 已进入正确 authority layer，generated projection 无 drift；
5. focused tests、contract/schema/negative tests、KB render、BDD（如触发）、public doctor/export/verify、Dashboard registry 和 Git diff gates 全部通过；
6. 独立 Final Validation 与 Semantic Review 覆盖实际 closeout、最终 KB/Dashboard 和完整 diff；
7. closeout-language gate 通过；
8. post-closeout reconciliation 给出唯一、无冲突的 bounded passing verdict；
9. OPCM 没有漏项、未批准 Scope Delta 或未吸收例外；
10. next-session scan 没有本 Goal 内未完成且 ready 的 Session。

两个 Agent 的对比验收不在 completion rule 中，不得因为未运行该测试而阻断本 Goal；同样不得据此给出 cross-Agent claim。

如果 mandatory evidence 不完整，必须使用：

`当前不能声明完成；缺失证据为：...；可选收束状态只能是 blocked/partial，不能是 pass/done。`

启动后请先输出中文任务解释、Read Manifest 摘要、intake verdict、批准的 Scope Delta、ERBE applicability、resolved Goal/Session DAG、八项 finding ledger 和 maximum claim，然后自动进入 R0。不要只回复计划，也不要在单个 Session closeout 后把控制权交回用户。
