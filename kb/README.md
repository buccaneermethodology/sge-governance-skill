# Semx Knowledge Base

_Version: v1.34 | Status: active | Updated: 2026-07-01_

本知识库用于沉淀 Semx CLI 的当前正式设计真理，遵循 docs-system/v1 的 Doc-as-Data 约束：先写 JSON 真源，再渲染为 Markdown。

当前已覆盖 canonical、phases、strategy、evolution 四层，其中 phase 文档按 docs-system 的统一 contract 模板展开到 P00-P17。

## Current Scope

- 已建立 `semx-kb/data/` 作为 JSON 真源目录，并通过 `semx-kb/tools/render_kb.py` 生成 Markdown。
- 当前 canonical 基线采用 `Semx CLI总体架构V2.2` 作为正式架构真理。
- Phase 层已按 P00-P17 补齐，每份文档统一包含 Goal / Inputs / Outputs / Internal Logic / Constraints / Failure Modes / Upstream / Downstream。
- 已新增 `Implementation Constitution V1`，用于冻结首条正式实现线的范围、非目标、兼容策略与 change control。
- Agentic Governance V2 已收束为 canonical strategy：默认 full agentic logging 关闭，只有用户或 stage plan 明确要求时才启用 full audit logs，且 builder / validation / closure lanes 优先于默认 read-only explorer lanes。
- Tracked Session / Stage Plan 执行请求和 non-trivial governed work 现在默认激活 governed multi-agent mode：standing user authorization 已明确记录，后续 Semx non-trivial governed tasks 中用户明确授权 AI 按需使用 subagents / delegation；AI 仍需根据 Multi-Agent Activation Gate 自行决定是否启动，不需要用户额外明确要求 subagents；若降级 single-agent，必须在 closeout 记录例外，且用户没有明确要求 subagents 不是有效例外理由。
- 每个 non-trivial task 默认准备轻量 `Validation Handoff Packet`，让 Validation lane 在 full audit logging 关闭时仍能获得 claimed scope、non-goals、gates、evidence、risks 与 KB/Dashboard impact。
- 非 trivial governed task 默认用 Dashboard closeout artifact 保存 Validation Handoff、gates、non-goals、semantic no-escalation、deferred remainder 和 next candidates，而不是只依赖 final chat；所有任务 closeout artifact 和最终 closeout summary 默认使用中文，英文 lane/tool evidence 需要翻译或摘要，除非原文是必要证据。
- Validation lane 需要尽早启动并作为 final closeout / promotion 之前的真实质量 gate；等待验证结果时应优先做不重叠工作，而不是为了赶节奏催出仓促结论。
- Semantic Reviewer 已定义为独立 thread 的按需语义治理 lane，由人类请求、Stage Plan 要求或明确 semantic-risk escalation 触发；它不替代 Validation Agent，也不是每个 non-trivial task 的默认 lane。
- Builder、Validation Agent、Semantic Reviewer 与 Closure Agent 的可复用 delegation prompt templates 已写入 strategy 真源，供后续 governed batches 复用。
- CLI rollout 现在已有 first-pass `semx config-bootstrap`，可从本地 repo path 或 GitHub repository URL 生成 `semx_config_v1`；即使输入是 GitHub URL，输出仍然绑定到本地 checkout 的 `repo_path`，不把 full `semx init` 假装成已落地。
- CLI 还新增了 first-pass 本地路径 `semx extract evidence` / `m05` / `semantic-flow` facade，它们是对已维护 runtime surfaces 的 thin wrapper，而不是对完整 aspirational `extract` tree 的超前实现。
- Artifact Spec 现在已经明确 formal `history/<run_id>/`、active-run `latest/<run_id>/`、compare isolation、resume boundary 与 flat transitional out-dir 的关系，而且 formal early-phase commands 已开始 dual-write canonical run-id store。
- Legacy-to-V2 Transition Inventory 已新增为 implementation doc，用来把当前 `semx/` surfaces 分类为 keep / shim / rewrite / retire，避免未来批次重新把 demo 线与 formal line 混回一起。
- 本轮不把 `Scenario` 纳入正式语义层；如需恢复该层，必须先在 evolution 中完成角色澄清。
- P03 现在已把 guarded-flow 最小升级从纯提案推进到真实 maintained truth：repo 中已有 `semantic_flows_v1_1.schema.json`、guarded example、default contract-test coverage，以及已切到 `semx_semantic_flow_v1_1` 的 maintained runtime；旧 `v1` branching example 仍保留给当前 P03/P04 compatibility pair。
- Strategy 层现在新增了独立的 `Strategy_Acceptance_Postures` 文档，用来按 phase 持续维护 P01/P02/P03/P04 等 acceptance posture 的入口命令、blocking/advisory gate 与 regression surfaces。
- Repo-local `semx-governed-checkpoints` 现在还提供 `phase_workflow.py`，可在非 trivial phase work 开始前把当前 phase/stage 的 delivery contract、guardrails、acceptance entry surface、regression commands 与 closeout duties materialize 成可执行 runbook，并在需要时输出可复制的命令模板。
- Strategy 与 Acceptance docs 现在已经把 reviewed `semantic oracle seed` 与 downstream `executable semantic oracle` 明确分层，并补上了当 remaining drift 主要是 canonical-field ownership / exactness oscillation 时应从 `A1` prompt micro-tuning 转向 `A2` acceptance hardening 的治理规则。
- Extract / inspect surfaces 现在还有一个稳定的 review sidecar：`semx extract ...` 会在 `report_dir` 写出 `artifact_stats.json`，`semx inspect early-phase-stats <artifact>` 可以对单个 P00-P05 artifact 派生 deterministic counts 和 high-signal distributions。
- Semantic Surface Engineering 现在已作为独立 strategy truth 进入 KB：它把 S-176/S-184/S-185/S-187/S-188 中稳定的实践体系、Meaning Transformation Flow、Semantic Entropy Field、Semantic Stabilization Flow、Semantic State Transition、Semantic Memory Surface、S1-S6 taxonomy 和 L0-L6 diagnostic surfaces 提升为 Semx AI-native methodology 的 canonical 表达，同时明确 Dashboard 文章与案例仍是来源/解释材料而不是 runtime 或 capability law。S-191 已补充 S-189 promotion provenance，收窄 semantic surface eligibility，并把 oracle/runtime 中间态表述为 reviewed boundary、bounded evidence 和 promoted-only canonical truth。S-186 已把 S1-S6 / L0-L6 接入 Validation Agent、Semantic Reviewer 和 Dashboard Agent 的 reviewer guidance / prompt templates，限定为诊断词汇和 countermeasure lens，不改变 runtime/schema/gate/acceptance/product policy，也不把 Semantic Reviewer 变成每个任务的默认要求。
- SGC v1 Structural Contract 现在是 semantic-risk AI coding implementation decisions 的 active structural governance contract：它定义 claim levels、forbidden collapses、SI review questions 和 completion rule；SGC v2/v3 只作为 future layers，不改变 runtime/schema/gate/acceptance/provider/CLI 行为，也不制造 every-output scorecard 或 ledger 要求。
- `Strategy_SGC_to_P06_Contract_Evolution` 现在以 proposal 状态进入 KB：它把 SGC-to-P06 关系限定为 recommended governance review route，而不是 runtime pipeline；`contract delta` 明确定义为 non-executable、manual-review-only 的候选 P06 contract update，不会自动改变 P06 evaluator、runtime、schema、BDD 或 acceptance posture。
- M1/P05 extraction 当前新增 `Strategy_M1_Extraction_Target_B` 作为 strategy overlay：V2.2 架构仍成立，但 P05 默认目标从 pattern-promotion / maintained generalized truth 证明，转为 Java/Python repo-agnostic handling 下的 grounded M1 candidate hypotheses、diagnostic-only honesty、trust/disposition boundary 和 optional known-family enhancement；任意 Java/Python 输入应得到诚实 artifact-level result，但不保证每个 repo 都产出非空 candidate。
- `Strategy_KB_Promotion_and_Graph_Source_Policy` 现在定义 Dashboard artifacts 何时可被语义提升为 KB truth、何时只能作为 source_scope/provenance，以及 KG-L1 `R-DEPENDS-ON-DOC` advisory 和 source-set expansion 的处理规则；它不改变当前 KG-L1 approved C1 source set。
- `Strategy_BDD_Validation` 现在定义 Semx BDD validation suite 的定位：BDD 是 Given/When/Then 的人类可读行为层，legacy contract/acceptance/runtime/matrix gates 仍是 pass/fail authority；C1 BDD migration 覆盖所有 maintained non-unit gates，C2 case-level migration 覆盖当前可枚举内部 case，并保持旧 runner 不被替代。
- `Strategy_P05_Four_Bucket_Minimal_Index` 现在以 proposal 状态记录 S-263 的 P05 sidecar v2 最小索引目标：v2 sidecar 是 exact structural membership index，只允许 `member_id`、opaque `bucket`、opaque `source_ref`，且单一 invariant 是 P05 sidecar 不承载任何语义。
- `Strategy_Runtime_Orchestration_Stage1` 现在定义 Runtime Orchestration 第一阶段的可维护边界：只从 `runtime_execution_trace_v1` 确定性 replay 到 runtime execution state 和 graph skeleton；不把 global state、graph edge、provider/BDD/diagnostic/witness output 变成 KB/P06/M1 authority。
- `Strategy_Runtime_Orchestration_Stage2` 现在定义 SP-035 / S-271 批准后的 Stage 2 support-boundary truth，并记录 S-272 first emitter、S-273 read-model inspection、S-274 BDD readable cards、S-275 event/failure/next-action contract、S-276 authority boundary 和 executable no-overclaim guard 已落地。
- `Strategy_Runtime_Event_Failure_Next_Action_Contract_V1` 现在定义 Runtime Stage 2 的 stable event taxonomy、system report-only events、failure ontology、next-action mapping、input_event_refs monotonicity、witness non-mutation 和 graph endpoint 约束。
- `Strategy_Runtime_Authority_Boundary_V1` 现在定义 Runtime Stage 2 support surfaces 与 SAG truth、rollback/invalidation、repair-loop controller、P06/M1 disposition、KB truth write 的 authority split。
- `Strategy_Runtime_Kernel_V1_Target_Contract` 现在以 target-only contract 记录 SP-038 / S-280 冻结的完整 TCO Runtime Kernel v1 目标：G1-G10 全部保持 `not_implemented`，Stage 1/2 只能作为 prior support evidence，后续执行路线/status 留在 Dashboard。
- `Strategy_Runtime_Kernel_Global_State_Machine_C0_1` 现在以 target-only C0-1 contract 记录 S-281 的全局 runtime execution state machine 设计边界：runtime-owned execution coordination state、lifecycle categories、transition authority、rejection history、advisory next_action 和 truth-layer split；该文档不实现 G1，G1 仍为 `not_implemented`。
- `Strategy_Runtime_State_Contract_V1` 现在记录 S-286 维护层 state contract：transition event schema、validator、positive/negative fixtures 和 maintained fixture runner 已落地；它只支持 `maintained_schema`、`validator_landed`、`fixture_runner_landed`，不证明 `runtime_behavior_landed` 或 SP-038 完成。
- `Strategy_Runtime_Kernel_SAG_Artifact_Graph_C0_2` 现在以 target-only C0-2 contract 记录 S-282 的真正 SAG / artifact graph 设计边界：M1/Mc/Flow/Slice/Evidence graph ontology、typed edge catalog、semantic diff / contradiction boundary、invalidation model、rollback authority boundary、repair lineage / convergence proof graph model；该文档不实现 G5/G7/G8，三者仍为 `not_implemented`。
- `Strategy_Runtime_Kernel_Orchestration_Controller_C0_3` 现在以 target-only C0-3 contract 记录 S-283 的 orchestration controller 设计边界：dynamic phase router/scheduler、execution planner DAG、broad P00-P17 executor boundary、feedback loop controller、rollback/invalidation controller behavior boundary、loop-event integration、S-281/S-282 interface 和 controller authority matrix；该文档不实现 G2/G3/G4/G6/G7/G8，六者仍为 `not_implemented`。
- `Strategy_Runtime_Kernel_Execution_Posture_Cross_Cutting` 现在以 target-only cross-cutting contract 记录 S-284 的 execution posture 设计边界：cost model、parallel execution model、resource tracking、budget、retry、persistent execution context、controller daemon posture、operator console posture 和 production posture；该文档不实现 G9/G10，二者仍为 `not_implemented`。

## Build Process

1. 阅读 docs-system/v1 规范，确认文档分层、字段约束和 Markdown 渲染规则。
1. 阅读 `semx-kb/bm-doc/` 中的架构、规则、协议与命名文档，提炼当前有效真理。
1. 将 canonical truth 写入 `semx-kb/data/*.json`、`semx-kb/data/strategy/*.json` 与 `semx-kb/data/evolution/*.json`。
1. 执行 `python3 semx-kb/tools/render_kb.py` 将 JSON 编译到 `semx-kb/docs/` 和顶层 `README.md`。

## Document Map

### Canonical Docs

- [Architecture](docs/Architecture.md): 定义 Semx 的定位、核心对象、分层边界和设计原则。
- [Logical Pipeline](docs/Logical_Pipeline.md): 给出 V2.2 的正式 phase 顺序、输入输出关系与 pipeline 纯度规则。
- [CLI Spec](docs/CLI_Spec.md): 定义一级命令、关键二级命令、执行模式和策略绑定方式。
- [Artifact Spec](docs/Artifact_Spec.md): 定义 `.semx/history/<run_id>/`、`.semx/latest/<run_id>/` 与 transitional flat writes 之间的正式 artifact contract。
- [Glossary](docs/Glossary.md): 统一术语定义，避免 Semantic Flow / Behavioral Flow / DRP 等概念混用。

### Implementation Docs

- [Implementation_Constitution_V1](docs/adr/Implementation_Constitution_V1.md): 冻结首条正式实现线的范围、非目标、兼容策略、交付顺序与 change control。
- [Evidence_Relation_Enrichment_V1](docs/adr/Evidence_Relation_Enrichment_V1.md): 定义 P01 缺失关系类型该落在 canonical evidence、runtime graph view 还是 downstream artifacts。
- [Legacy_to_V2_Transition_Inventory_V1](docs/adr/Legacy_to_V2_Transition_Inventory_V1.md): 按 keep / shim / rewrite / retire 分类当前 `semx/` surfaces，给 V2 runtime 迁移一个稳定边界。
- [Semantic_Flow_Schema_Minimal_Upgrade_Proposal_V1](docs/adr/Semantic_Flow_Schema_Minimal_Upgrade_Proposal_V1.md): 为 P03 的 guarded-flow 过强分类问题提出最小、版本化、向后兼容的 `v1.1` schema 升级方案。

### Phase Docs (P00-P08)

- [Phase_00_Manifest](docs/phases/Phase_00_Manifest.md): 冻结 run context、scope、版本矩阵与 run_id。
- [Phase_01_Evidence](docs/phases/Phase_01_Evidence.md): 建立 grounded evidence 层，不直接命名 capability。
- [Phase_02_M05](docs/phases/Phase_02_M05.md): 把 evidence 转成事实描述层，稳定意图边界。
- [Phase_03_Semantic_Flow](docs/phases/Phase_03_Semantic_Flow.md): 抽取用于 M1 保护的控制语义脚手架。
- [Phase_04_Semantic_Slice](docs/phases/Phase_04_Semantic_Slice.md): 切成最小推理单元，保留完整 decision semantics。
- [Phase_05_M1_Candidate](docs/phases/Phase_05_M1_Candidate.md): 基于 Slice 与 M0.5 cluster 识别高召回 M1 候选。
- [Phase_06_M1_Validation](docs/phases/Phase_06_M1_Validation.md): 维护 P06 bounded authority surface，并把 legacy promote 解释为 eligible_for_formalization。
- [Phase_06_M1_Validation_Architecture_V2](docs/phases/Phase_06_M1_Validation_Architecture_V2.md): P06 V2 proposal：分离 assessment、validation、decision、formalization、commit 和 canonical archive。
- [Phase_06_Dedicated_Store_Stable_Contract_V1](docs/phases/Phase_06_Dedicated_Store_Stable_Contract_V1.md): 定义 S-336 Dedicated store 中可复用的稳定合同子集：manifest 边界、identity/history/current pointer、global revision、provenance、audit、transaction/readback/idempotency/conflict 和 no-production claim ceiling。
- [Phase_07_Mc](docs/phases/Phase_07_Mc.md): 由稳定 M1 组合出可执行 Mc。
- [Phase_08_Behavioral_Flow](docs/phases/Phase_08_Behavioral_Flow.md): 从 Mc 投影出正式行为层 Flow。

### Phase Docs (P09-P17)

- [Phase_09_DRP](docs/phases/Phase_09_DRP.md): 从稳定语义层归纳可复用 DRP。
- [Phase_10_Alignment](docs/phases/Phase_10_Alignment.md): 建立 Mc→M1 与 Flow→DRP 的正式映射。
- [Phase_11_UCS](docs/phases/Phase_11_UCS.md): 装配符合 UCS V1.1 的统一正式 schema。
- [Phase_12_USL_Lint](docs/phases/Phase_12_USL_Lint.md): 执行结构与语义双维 USL 校验。
- [Phase_13_Issue_Graph](docs/phases/Phase_13_Issue_Graph.md): 把平面 issues 提升为依赖与冲突图。
- [Phase_14_Repair_Plan](docs/phases/Phase_14_Repair_Plan.md): 把 issues 规划为最小、低冲突 repair plan。
- [Phase_15_Repair_Apply](docs/phases/Phase_15_Repair_Apply.md): 执行局部 patch，输出 repair report 和 repaired schema。
- [Phase_16_Post_Lint](docs/phases/Phase_16_Post_Lint.md): 对 repaired schema 重新执行 lint。
- [Phase_17_Convergence](docs/phases/Phase_17_Convergence.md): 判断是否收敛、继续下一轮或升级人工审查。

### Strategy Docs

- [Strategy_M1_Extraction](docs/strategy/Strategy_M1_Extraction.md): 说明 M0.5 + Semantic Flow + Semantic Slice 驱动的 M1 抽取策略。
- [Strategy_M1_Extraction_Target_B](docs/strategy/Strategy_M1_Extraction_Target_B.md): 定义当前 target-B M1/P05 strategy overlay：Java/Python repo-agnostic handling 和 grounded candidate hypotheses 为主线，known-family enhancement 和 maintained generalized truth 为 side-lane。
- [Strategy_USL](docs/strategy/Strategy_USL.md): 说明 USL 的结构/语义双维校验策略与输出契约。
- [Strategy_Repair](docs/strategy/Strategy_Repair.md): 说明 issue-driven repair 的动作映射、顺序和边界。
- [Strategy_Convergence](docs/strategy/Strategy_Convergence.md): 说明 planner 排序、收敛判定、震荡检测与人工升级条件。
- [Strategy_Human_AI_Development](docs/strategy/Strategy_Human_AI_Development.md): 总结 Semx 会话中形成的人-AI开发范式、默认多 Agent 激活、可复用 skills、phase workflow automation、语义治理 reviewer lane、S1-S6 / L0-L6 reviewer guidance 和跨项目自动化边界。
- [Strategy_Acceptance_Postures](docs/strategy/Strategy_Acceptance_Postures.md): 按 phase 维护 acceptance posture 的入口命令、blocking/advisory gate 与 regression surface，当前覆盖 P01/P02/P03/P04/P05。
- [Strategy_Semantic_Surface_Engineering](docs/strategy/Strategy_Semantic_Surface_Engineering.md): 定义 Semx 的 Semantic Surface Engineering 方法：Meaning Transformation Flow、Semantic Entropy Field、Semantic Stabilization Flow、Semantic State Transition、S1-S6 语义不一致分类、L0-L6 diagnostic surfaces、semantic surface eligibility、19 个实践 registry 与 P19 的 8 个子实践。
- [Strategy_SGC_Structural_Contract_V1](docs/strategy/Strategy_SGC_Structural_Contract_V1.md): 定义 SGC v1 Structural Contract：semantic-risk AI coding implementation decisions 的适用范围、claim levels、forbidden collapses、SI review questions、completion rule、non-promises，以及 v2/v3 future-layer 边界。
- [Strategy_SGC_to_P06_Contract_Evolution](docs/strategy/Strategy_SGC_to_P06_Contract_Evolution.md): 以 proposal 状态定义 SGC-derived reasoning-validity pressure 如何通过 recommended contract evolution path 进入人工审查的 P06 contract update；明确 contract delta 非执行、P06 保持唯一 disposition authority、Runtime commit-only、M1 canonical truth。
- [Strategy_KB_Promotion_and_Graph_Source_Policy](docs/strategy/Strategy_KB_Promotion_and_Graph_Source_Policy.md): 定义 Dashboard artifact 到 semx-kb 的语义提升规则、source_scope/provenance-only 边界、KG-L1 `R-DEPENDS-ON-DOC` advisory 处理，以及 reviewed source-set expansion protocol。
- [Strategy_BDD_Validation](docs/strategy/Strategy_BDD_Validation.md): 定义 Semx BDD validation suite 的行为分层、四个迁移批次、legacy gate authority 兼容规则、C1 gate-level 与 C2 case-level coverage/no-duplicate-truth 约束和 authoring checklist。
- [Strategy_P05_Four_Bucket_Minimal_Index](docs/strategy/Strategy_P05_Four_Bucket_Minimal_Index.md): 以 proposal 状态记录 S-263 的 P05 sidecar v2 最小索引合同、sidecar 消费边界、P05/P06 三层不重叠模型，以及 v1 payload mirror 到 v2 opaque structural index 的收敛方向。
- [Strategy_Runtime_Orchestration_Stage1](docs/strategy/Strategy_Runtime_Orchestration_Stage1.md): 定义 Runtime Orchestration Stage 1 的 deterministic replay、event governance、witness-only graph skeleton、CLI exit-code contract，以及不越权成为 KB/P06/M1 authority 的边界。
- [Strategy_Runtime_Orchestration_Stage2](docs/strategy/Strategy_Runtime_Orchestration_Stage2.md): 定义 Runtime Orchestration Stage 2 的 approved support-boundary：真实 maintained trace emission、graph/read-model inspection、BDD readable cards、event/failure/next-action contract、SAG/rollback/repair authority split，以及 no-overclaim gates。
- [Strategy_Runtime_Event_Failure_Next_Action_Contract_V1](docs/strategy/Strategy_Runtime_Event_Failure_Next_Action_Contract_V1.md): 定义 Runtime replay support 的 event taxonomy、failure ontology、next-action mapping、monotonicity 和 witness/system-event 边界。
- [Strategy_Runtime_Authority_Boundary_V1](docs/strategy/Strategy_Runtime_Authority_Boundary_V1.md): 定义 Runtime Stage 2 support surfaces 与 SAG truth、rollback/invalidation、repair-loop controller、P06/M1 disposition、KB truth write 的边界，并要求 executable no-overclaim guard。
- [Strategy_Runtime_Kernel_V1_Target_Contract](docs/strategy/Strategy_Runtime_Kernel_V1_Target_Contract.md): 以 target-only contract 冻结 SP-038 / Runtime Kernel v1 的 G1-G10 完整缺口 ledger、claim ceiling、truth carrier split、Scope Delta 禁止规则和完成边界；不实现任何 Runtime Kernel 行为。
- [Strategy_Runtime_Kernel_Global_State_Machine_C0_1](docs/strategy/Strategy_Runtime_Kernel_Global_State_Machine_C0_1.md): 以 target-only C0-1 contract 冻结 S-281 全局 runtime execution state machine 的 lifecycle、state ownership、transition authority、candidate DSL shape、invariants 和 no-truth-collapse 边界；不实现 G1。
- [Strategy_Runtime_State_Contract_V1](docs/strategy/Strategy_Runtime_State_Contract_V1.md): 记录 S-286 维护层 Runtime state contract / schema / validator / fixtures / fixture runner；只支持 validator 层声明，不证明 Runtime Kernel runtime behavior landed。
- [Strategy_Runtime_Kernel_SAG_Artifact_Graph_C0_2](docs/strategy/Strategy_Runtime_Kernel_SAG_Artifact_Graph_C0_2.md): 以 target-only C0-2 contract 冻结 S-282 真正 SAG / artifact graph 的 ontology、typed edges、semantic diff、contradiction、invalidation、rollback、repair lineage 和 convergence proof graph 边界；不实现 G5/G7/G8。
- [Strategy_Runtime_Kernel_Orchestration_Controller_C0_3](docs/strategy/Strategy_Runtime_Kernel_Orchestration_Controller_C0_3.md): 以 target-only C0-3 contract 冻结 S-283 orchestration controller 的 router/scheduler、planner DAG、P00-P17 executor boundary、feedback loop、rollback/invalidation behavior boundary、loop-event integration 和 authority matrix；不实现 G2/G3/G4/G6/G7/G8。
- [Strategy_Runtime_Kernel_Execution_Posture_Cross_Cutting](docs/strategy/Strategy_Runtime_Kernel_Execution_Posture_Cross_Cutting.md): 以 target-only cross-cutting contract 冻结 S-284 execution posture 的 cost、parallel、resource、budget、retry、persistent context、daemon、operator console 和 production readiness 边界；不实现 G9/G10。

### Evolution Docs

- [Evolution_Log](docs/evolution/Evolution_Log.md): 记录 V1.0 → V2.0 → V2.2 → Target-B M1 Extraction Overlay 的保留、删除、替换项，以及当前待校正冲突。

## Source Notes

- `docs-system/v1/` 提供文档系统方法论和 JSON 文档模型，但不直接提供 Semx KB 成品内容。
- `semx-kb/bm-doc/` 是当前主要语义来源，其中 `TCO/4. Semx CLI总体架构V2.2.md` 是最关键的 canonical 基线。
- `KYM/2. KYProd (What)/2.4 Unified Capability Schema V1.1.md` 已补齐，现作为 UCS 的正式文本来源；`semx/schemas/ucs_v1_1.schema.json` 作为当前实现参考。
- 当 bm-doc 与当前代码实现不一致时，本知识库优先记录最新设计真理，并在 evolution 中显式标出实现差距。
- S-176/S-184/S-185/S-187/S-188 是 Semantic Surface Engineering 的主要 Dashboard 来源；S-189 只提升其中稳定、可复用、边界明确的 methodology subset，未提升长篇叙事、案例本身、runtime generalization 或产品能力 claim；S-191 将 S-189 closeout 纳入 source scope，并明确 taxonomy 是 canonical vocabulary / diagnostic lens；S-186 将该 lens 接入 reviewer guidance 和 reusable prompts，但仍不把它升级成 numeric scorecard、universal science claim、runtime/schema/gate/acceptance policy 或每个任务的 mandatory Semantic Reviewer trigger。
- `Strategy_M1_Extraction_Target_B` 吸收了待删除分支 `4d262b8` 中 generic candidate synthesis 的正确方向，但修正了该分支的 overclaim：Current P05 Board 不属于 KB truth，TBC/ECCN/Co-Sight 旧证据只支撑 candidate surface evidence，provider-backed path 仍是待设计的 calibration/runtime 选择而不是已维护默认；2026-06-17 的路线更新进一步明确 Java/Python repo-agnostic handling 不等于每个 repo 都必须产出非空 candidate，P02 是 target-B coverage frontier，真实泛化证据由 support matrix 与 diagnostic matrix 共同承载。
- S-212 将 S206-S210 KG Dashboard artifacts 作为 promotion/source-set policy 的 source material，而不是将这些 artifacts 原样提升为 KB truth；S207 contract、S209 validation report、S210 projection/issue report 仍保持 Dashboard/projection/evidence authority。
- `Strategy_P05_Four_Bucket_Minimal_Index` 来自用户提供的 P05 sidecar 消费边界图和 P05 Phase / P05 Sidecar / P06 Authority 三层不重叠模型；该文档只冻结 S-263 proposal-level 最小索引方向，不表示 `p05_four_bucket_output_v2` 已实现。
- `Strategy_Runtime_Orchestration_Stage1` 来自 Runtime Orchestration TCO、SP-034 C0 设计和 Stage 1 acceptance suite；该文档只提升 deterministic replay / event-governance / non-authority boundary 的稳定子集，不提升 full semantic compiler kernel、自动 repair loop、rollback authority 或 broad P00-P17 runtime。
- `Strategy_Runtime_Orchestration_Stage2` 来自 SP-035 / S-271 C0 approval、C0 design、C0 closeout 和 S-272..S-276 implementation evidence；该文档记录已落地的 support surfaces，但不表示 SAG truth、rollback/invalidation controller、repair-loop controller 或 broad Runtime authority 已实现。
- `Strategy_Runtime_Event_Failure_Next_Action_Contract_V1` 来自 S-275 contract implementation；该文档是 runtime replay support contract，不是 P06/M1 authority、rollback authority、repair-loop authority、provider authority 或 KB write authority。
- `Strategy_Runtime_Authority_Boundary_V1` 来自 S-276 boundary implementation；该文档定义 support-vs-authority split 和 no-overclaim guard，不批准未来 SAG/rollback/repair-loop controller 实现。
- `Strategy_Runtime_Kernel_V1_Target_Contract` 来自 SP-038 / S-280 C0 design、指定 Semantic Reviewer Thread 问题澄清与 review、指定 Validation Agent 验收矩阵反馈、TCO/12 原始 Runtime Kernel 文档和用户给出的 10-gap 主口径；该文档只提升稳定 target-only ledger 和 overclaim 禁令，不提升 Dashboard session route/status，也不表示任何 G1-G10 已实现。
- `Strategy_Runtime_Kernel_Global_State_Machine_C0_1` 来自 S-281 Goal、S-281 验收基线、SP-038 target contract、Stage 1/2 Runtime Orchestration contracts 与 S-281 设计工件；该文档只提升稳定 C0-1 state-machine boundary，不提升 candidate DSL 为 maintained schema/gate，也不表示 global runtime state machine behavior 已实现。
- `Strategy_Runtime_State_Contract_V1` 来自 S-286 implementation-entry、S-281 C0-1 target-only contract、maintained validator、transition event schema、fixtures 和 acceptance suite；该文档只提升 maintained schema/validator/fixture-runner 层，不表示 scheduler/planner/executor、feedback loop、rollback execution、SAG truth、Runtime Kernel behavior 或 SP-038 closeout 已完成。
- `Strategy_Runtime_Kernel_SAG_Artifact_Graph_C0_2` 来自 S-282 Goal、S-282 验收基线、SP-038 target contract、S-281 runtime state boundary、S-282 设计工件与 closeout；该文档只提升稳定 C0-2 SAG/artifact graph target boundary，不提升 candidate graph DSL 为 maintained schema/gate，也不表示 SAG truth、rollback/invalidation controller、repair loop、G5/G7/G8 implementation 或 Runtime Kernel behavior 已实现。
- `Strategy_Runtime_Kernel_Orchestration_Controller_C0_3` 来自 S-283 Goal、S-283 验收基线、SP-038 target contract、S-281 runtime state boundary、S-282 SAG/artifact graph boundary、S-283 设计工件与 closeout；该文档只提升稳定 C0-3 controller target boundary，不提升 candidate route event、DAG、adapter 或 loop-event shape 为 maintained schema/gate，也不表示 router/scheduler/planner/executor、automatic repair loop、rollback/invalidation execution、G2/G3/G4/G6/G7/G8 implementation 或 Runtime Kernel behavior 已实现。
- `Strategy_Runtime_Kernel_Execution_Posture_Cross_Cutting` 来自 S-284 Goal、S-284 验收基线、SP-038 target contract、S-281 runtime state boundary、S-282 SAG/artifact graph boundary、S-283 orchestration controller boundary、S-284 设计工件与 closeout；该文档只提升稳定 execution posture target boundary，不提升 cost/budget/retry/persistence/daemon/console/production posture candidate shape 为 maintained schema/gate/runtime，也不表示 G9/G10 implementation、production readiness、budget enforcement、parallel scheduler、persistent runtime store、retry engine、controller daemon、operator console 或 Runtime Kernel behavior 已实现。

## Open Questions

- CLI 命令与 artifact 编号仍存在 staged rollout 的剩余差距；当前已落地 `config-bootstrap`、formal runtime commands、`inspect early-phase`，以及本地路径 `extract evidence/m05/semantic-flow`，但更宽的 `extract` breadth 与其他命令族仍待后续批次补齐，详见 `docs/evolution/Evolution_Log.md`。
- 是否需要把 `semx-kb/` 迁移为 docs-system 推荐的 `semx/kb/` 内嵌布局，尚未决定。
- Target-B P05 仍需后续同步 `m1_candidates` trust/disposition schema、P05 acceptance posture、provider-backed role decision、Current P05 Board 和 open Dashboard session reconciliation。
- KG-L1 approved source set 仍是 S207/S209 维护的窄 C1 source set；若未来要纳入 Architecture、Artifact Spec、Human-AI strategy、Semantic Surface Engineering、P06-P17 phase specs 或新的 promotion policy doc，应先执行 reviewed source-set expansion，而不是自动追随 `depends_on_docs`。
