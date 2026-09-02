# SGE Repo Hard Gates

这些规则适用于本仓库中的所有工作。`AGENTS.md` 只保留必须执行的硬门；详细流程、模板、检查清单和解释规则放在 `.codex/skills/sge-governed-checkpoints/`、`kb/` 和 `Dashboard/`。

## 输出语言

- 所有聊天回复、最终总结、Dashboard closeout、closeout-style summary 默认使用中文。
- 外部工具、验证器、provider、代码标识、命令、schema 字段、verdict/status 等必要英文可以保留，但必须用中文解释其含义、判断影响、证据边界和下一步。
- 不发送可选闲聊；进度更新只用于必要 checkpoint、较长执行、文件编辑前说明或阻塞说明。

## Source Of Truth Split

- `kb/` 是 canonical truth：架构、contracts、strategy、terminology、evolution、稳定治理规则。
- `Dashboard/` 是 execution memory：状态、任务顺序、blocker、open decision、candidate next sessions、closeout evidence。
- 不要把 `Dashboard/` 当成 canonical truth；Dashboard artifact 中的稳定规则如需未来复用，必须通过 Contract Delta Scan 判断是否抽取到 `kb/` JSON truth。

## Dashboard Session Registry 日常硬门

- 新建、更新、关闭或归档 Session，或改动 `Dashboard/Sessions.md`、`Dashboard/Session_Index.md`、`Dashboard/Archives/Sessions/*.md`、`Dashboard/Archives/Sessions/archive_manifest.json` 任一表面时，必须运行 `python3 Dashboard/tools/session_registry.py reconcile --repo . --check` 与 `python3 Dashboard/tools/session_registry.py validate --repo .`；任一命令非零时，不得把受影响 Session 标为 `Done` 或使用等价关闭措辞。
- 只有 `reconcile --check` 报告可重建的派生漂移、且预检没有 error 时，才可显式运行 `python3 Dashboard/tools/session_registry.py reconcile --repo . --apply`；随后必须重跑相同的 `--check` 与 `validate`。identity、row、Status、unknown archive surface 或历史说明表面错误必须人工处理，不能让日常命令猜测、first-wins 或删除未知文件。
- registry check 与 validate 通过后，若本次变更影响 Dashboard KG / DKG，才以 `Dashboard/tools/generate_dashboard_kg.py` 的显式输出路径重建 DKG，并运行 focused registry gate；DKG 不是 reconcile 的副作用，也不反向成为 registry 真源。
- 本仓库不提供历史迁移命令；`reconcile --check/--apply` 只维护当前 SGE Dashboard registry，禁止隐式执行外部迁移或 locator rewrite。

## ERBE Specification-First Gate

- 对会改变终态谓词、状态机、authority routing、acceptance/promotion/write 边界或其他高语义风险的 Goal，Goal Agent 必须先给出 ERBE applicability：`required`、`proportional`、`not_applicable` 或 `blocked_oracle`。
- 适用 Goal 必须在 dominant Builder 前冻结 machine-readable Contract/Cases、state axes、predicates、invariants、counterexamples、forbidden collapses、oracle owner、write exclusions 和 claim ceiling。
- 只有 `contract_verdict=valid`、`execution_verdict=ok` 且指定行为按预期 failure fingerprint 失败，才能记录可信 RED；环境/fixture/import/path 错误只能是 `error`。
- GREEN 必须复用与 RED 相同的 frozen case identity，并由独立 Validation 从 durable inputs 重算；producer 自报 terminal status 不构成验证证据。
- Builder 不得修改 frozen Contract/Cases/expected/RED evidence/claim ceiling；修改必须走 Contract Patch + Scope Delta + re-RED。当前 `tests/bdd/readable_cards/` 仍是 projection，不是 ERBE 或 pass/fail authority。

## Task Intake Gate

- 每个用户请求默认先做 proportional Task Intake Evaluation，再执行。
- 最小检查：目标、source authority、repo/KB/Dashboard 边界、风险/缺失信息、执行/缩窄/询问/拒绝/升级路线。
- 低风险小任务可以隐式通过；涉及持久编辑、KB/Dashboard、contracts、acceptance/gates、semantic promotion、外部 artifact、approval text 或 destructive action 时，必须显式记录 intake verdict。
- 用户要求“直接执行”只跳过可见评估叙述，不跳过安全、source-of-truth、contract/KB/acceptance 和 destructive-action gate。

## Task Context Bootstrap Gate

- 每个用户请求在 Intake 后必须按 `read_only`、`implementation` 或 `validation` profile 构造任务启动包；低风险 trivial task 可隐式满足，其他任务必须用 `context_bootstrap.py validate` 校验后再执行。
- Raw User Intent 是 authority；Intake 只是 projection，不得替换、删减或重写原始意图。启动包必须包含 boundaries、Required Read Set、Conditional Read Set、Semantic Refresh、epistemic search space、change-impact vector 和 topology。
- Context Optimization 可以减少稳定规则正文与重复读取，但不得缩小完成当前任务所必需的认知搜索空间。发现缺证据或未覆盖的 required domain 时必须扩读，无法读取时明确报告 evidence gap；profile 不是 evidence waiver。
- Conditional Read Set 必须同时支持 deterministic 与 evidence-backed agent-evaluated trigger。agent-evaluated trigger 只能基于证据扩读，不能压制 deterministic trigger。
- 即使 path/digest/revision 未变化，也必须 semantic refresh：重新确认 objective、authority、claim ceiling 和 critical dependencies；digest unchanged 不等于理解仍有效。
- Topology 必须基于 change impact，而不能仅按 artifact type。稳定规则默认只注入 path、revision/digest、applicability 与 reason；具体流程见 canonical KB 与 checkpoint skill。

## SGC Gate

- 每个 non-trivial SGE task 在 completion、validation、promotion、runtime widening、KB/Dashboard truth placement 或 semantic-risk implementation claim 前，必须运行 SGC v1 proportional check。
- Canonical truth：`kb/data/strategy/strategy_sgc_structural_contract_v1.json`；阅读面：`kb/docs/strategy/Strategy_SGC_Structural_Contract_V1.md`。
- 必检：claim level、evidence layer、forbidden collapses、SI-1..SI-6、completion rule。
- SGC v1 不启用 SGC v2/v3、numeric score、universal ledger、runtime/schema/acceptance 变更，也不替代 deterministic gates、Validation Agent、Semantic Reviewer 或 closeout evidence。

## Goal Conformance Gate

- 对 non-trivial Goal、Stage Plan、tracked Session 或 approved plan，必须保留原始目标覆盖面：Goal Scope Ledger、Scope Delta、Original Plan Coverage Matrix。
- C0/initial design 后、dominant Builder 前、closeout 前都要比较 revised target 与 original objective。
- 删除、替换、改名、降级、延期、从 must-have 改成 non-goal，或用不同 authority 验证原始要求，均属于 Scope Delta。
- 未获人类批准、未标 not-applicable、未被 blocker/termination condition 终止的原始 must-have 没有落地时，不能写 Goal/SP/Session `done` 或等价完成结论。
- Validation Handoff 必须让 Validation 同时检查 revised design 和 original objective；只检查 revised design 不能支撑完成声明。
- 原始目标中的流程要求同样属于 must-have，包括独立可见 execution task、指定 lane 时序、pre-Builder review、final review 和 post-closeout reconciliation；不得只映射功能产物而漏掉流程条款。
- OPCM 结构门：Original Plan Coverage Matrix 必须是证据矩阵，不是关键词摘要。每个原始 must-have/AC 必须逐项列出，或提供明确分组理由和可展开的子项清单；每行至少包含原始要求、可观察验收判定、精确源文件 Markdown 链接、实际结果、状态、阻断/例外、owner/lane 或时序、claim ceiling、parent/Closeout 吸收状态。缺少这些字段时只能作为索引，不能支撑 `done`、`Goal complete` 或最终 `PASS`。
- Orchestrator 接管原本要求独立 task 执行的 Builder 属于 Scope Delta。除非有明确的人类批准和可定位 reference，否则补偿测试或 `Single-Agent Exception` 只能支持 `partial/exception-recorded`，不能支持“完全按 Goal 执行”。

## Loop Continuation Gate

- `/goal`、Loop Goal 或多 Session Stage Plan 默认连续执行到整个 Goal 的 completion rule 满足，不以单个 Session、lane、closeout 或 post-closeout reconciliation 完成为回合终点。
- 每个 Session closeout 后必须执行 next-session scan，并记录：`goal_terminal`、`next_session`、`next_session_ready`、`human_decision_required`。当 Goal 未终止、下一 Session ready 且不需要人类决定时，Orchestrator 禁止发送 final answer，必须在同一执行回合直接进入下一 Session。
- Session 的 bounded `done/pass` 只关闭该 Session，不等于 Loop pause。不得用“安全边界”“本回合只做到当前 Session”“如果你要继续”或类似措辞把非终态 Loop 交还给用户。
- 只有以下情况允许暂停或结束 Loop：Goal completion rule 已满足；用户明确停止/暂停；存在必须由人类行使的 authority、approval 或 destructive-action 决策；达到 Goal 明示的 token/context/budget 终止阈值；网络/工具中断；同一恢复条件连续失败超过默认 3 次。
- 普通 gate failure、card/digest drift、可重建 baseline、可修复测试失败或下一 Session 尚未创建 artifacts，均不是向用户索取“继续”的理由。Orchestrator 应在原 scope 内修复、rebaseline 或创建下一 Session 入口后继续。
- 真正需要人类决定时，必须一次性说明 decision、推荐项、影响和不决策时的 blocked 状态；人类决定后自动恢复 Loop，不得再要求额外“继续”。Context compaction 或 task resume 后，先从 Goal、Dashboard 和最近 closeout 恢复 continuation state，再继续第一个未完成且 ready 的 Session。
- Loop Goal Prompt 必须包含 continuation contract 和 termination conditions。若 Goal 只允许逐 Session 人工批准，必须把相应边界明确列为 approval checkpoint；未列出的 Session boundary 默认自动跨越。

## Goal Agent Quality Gate

- 设计、review 或最终化 Goal Prompt / Task Goal Prompt / Loop Goal Prompt 时，必须把输出当成后续执行线程的 handoff contract，而不是普通摘要。
- Goal Agent 必须先建立 Read Manifest：已读线程/附件、必读 repo 文件、验收标准、相关 design/closeout、跳过项和原因。
- 输出必须包含中文任务解释、scope / non-goal / risk、must-have ledger、acceptance criteria 映射、governance workflow、Validation Handoff、Semantic Reviewer 触发条件、KB/Dashboard review、终止条件、允许/禁止 closeout wording。
- Loop Goal Prompt 还必须明确：Session closeout 不是停止点；next-session scan 显示 ready 且无需人类 decision 时必须自动进入下一 Session；只有 Loop completion 或明示 termination condition 才允许发送 final answer。
- 不得为了“尽快收束”自动缩窄范围、跳过必读证据、验收标准、Original Plan Coverage Matrix、Scope Delta audit、Validation Handoff 或 closeout-language gate。
- 如果 Orchestrator 要求立即收束但必读证据不完整，必须回复：`当前不能声明完成；缺失证据为：...；可选收束状态只能是 blocked/partial，不能是 pass/done。`
- Goal Prompt 使用三层上下文：repo governance 只引用当前 `AGENTS.md` / checkpoint skill；Loop Goal 只保存一次 mission、original-scope IDs、Session DAG 和 Loop claim ceiling；当前 Session Task Card 只注入本 Session 的 Delta Read Set、AC pointer、outputs 和 maximum claim。不得在每个 Session 重贴完整项目宪法、所有历史 Session 或 AC 正文。
- Goal 草案被 review 后默认输出 `Goal Patch`（base goal/revision、sequence、被替换 section、replacement、reason、scope impact、conflicts）；只有首次 draft 和最终可下发 artifact 输出全文。Patch 不得隐藏 must-have 删除、authority/claim/completion 改动或 Scope Delta；Builder 只能接收 base + patches 已确定性解析后的完整 Final Goal。
- Goal Agent 必须做 duplication scan：稳定规则是否重复、同一要求是否出现超过两次、是否带入非当前 Session 细节、是否复制 AC 而非引用编号、是否定义未使用角色。发现重复时先压缩引用，不得以“自包含”为由无限扩张 Prompt。
- non-trivial lane 在 delegation 前必须先创建并验证 `lane_task_card_v1`；委派提示必须由 `lane_task_card.py render` 生成，只携带 card path/digest、lane/session/role、mode、cwd 和 expected-digest 验证命令，不得手写重贴 Goal、治理正文、AC 正文或相邻 lane 背景。接收端必须执行 renderer 给出的 `--expected-card-sha256` 命令；缺少有效 card 或摘要不匹配时不得启动 Builder/Validation/Semantic lane。
- 相邻或并行 lane 下发前必须运行 lane prompt duplication audit。稳定治理/Goal/AC 的长段复制、跨 lane exact repeated block、`delta` card 缺 snapshot、source digest 漂移、Builder 无 write scope 或 `fork_context=true` 均为 blocker；近似重复只作 advisory。不得用固定字符/token 上限代替语义重复检查。

## Context Efficiency / Delta Validation Gate

- 首轮 Validation 建立完整 baseline；后续修复轮默认使用带 `baseline_revision` 的 Validation State Snapshot 和 Delta Read Set，只重读 changed files、受影响 gates、未关闭 blocker 和最终状态面。
- 用户指令、Goal/governance/AC revision、original objective、claim ceiling、authority/truth placement、KB/Dashboard routing、依赖、执行拓扑、threat model、semantic-risk、patch consistency 或 baseline identity/inventory 发生变化时，必须 rebaseline；final diff 超出 Delta Read Set、出现未登记 untracked/renamed/generated surface 或 snapshot 不可定位时也必须 rebaseline。
- Validation Reviewer 判断当前合同是否满足；Adversarial Tester 查当前 threat scope 内的 bypass；Governance Architect 提出规则演进。未写入当前 AC、合同或人类批准 Scope Delta 的新 hardening 建议默认是 follow-on，不自动成为当前 blocker。
- 默认收敛顺序是 initial validation -> blocker-fix delta validation -> final-state reconciliation。第四轮及以后必须记录 blocker admissibility 或 rebaseline 原因；只有违反当前 AC/合同、original must-have、evidence integrity、authority boundary、claim ceiling 或造成 in-scope regression 才是 blocker。“还能继续加强”本身不是继续阻断的理由；同一根因连续两个 delta round 产生新 blocker 时应升级为 rebaseline、hardening Session 或人类 scope 决策。
- 窄、只读、无实现/语义变化的 delta reconciliation 可使用单一独立 Validation lane，不需要启动空的 Design/Builder/Closure lane；必须记录 delta-only 判定。实施、KB truth、runtime/schema、acceptance 或高语义风险变化仍按 Multi-Agent Gate 启动必要 lanes。
- 工作中间输出使用摘要级 Read Manifest 和新增 findings；完整 Read Manifest、证据矩阵和中文解释保留到正式 Validation/closeout artifact。Agent Log 记录新增事件和引用，不复制稳定背景或 closeout 全文。
- `lane_task_card.py validate/render/audit` 是 delegation 前置机器门禁；`guardrail_checklist.py` 的提示输出不能替代该门禁。首轮 full-baseline card 后，相邻 Validation/repair lane 默认消费 snapshot + Delta Read Set；需要全量重读时必须在 card 中记录 rebaseline reference。

## Validation Agent Quality Gate

- Validation Agent 是 read-mostly quality gate；除非用户明确要求修复，否则不得直接改 Builder 产物。
- Validation Agent 被调用时必须先建立 Read Manifest：指定线程/交接包、AGENTS、SGC skill、Dashboard Session/Stage Plan、Current State、验收标准、Original Plan Coverage Matrix、Scope Delta audit、相关 design/closeout、Agent Logs、KB truth、测试/gate 证据，以及未读/缺失项。
- 输出必须先用中文大白话解释任务实际在做什么、声称完成什么、不证明什么，再从用户 owner 视角识别尽可能多的执行质量问题、证据缺口、scope narrowing、overclaim、KB/Dashboard truth split 风险、测试充分性风险和后续技术债。
- Verdict 必须受证据完整性约束：缺必读证据、Validation Handoff、Original Plan Coverage Matrix、Scope Delta audit 或 closeout-language gate 时，不能给 `pass/done`；只能给 `blocked`、`partial` 或明确说明不能声明完成。
- 如果 Orchestrator 要求立即收束但必读证据不完整，必须回复：`当前不能声明完成；缺失证据为：...；可选收束状态只能是 blocked/partial，不能是 pass/done。`
- 同一任务的首轮 Validation 必须完整读取；后续轮次应先读取上一轮 Validation State Snapshot，再按 delta 验证。只有命中 rebaseline trigger 时才重新全量审计，避免每轮重新加载整个项目。
- Validation 不得把 Governance Architect 的扩展建议、当前 AC 之外的 Level 3 hardening 或一般性“还可以更严格”自动升级为 blocker；必须说明它属于 current contract、accepted Scope Delta 还是 deferred follow-on。

## Semantic Reviewer Quality Gate

- Semantic Reviewer 不是只检查 no-overclaim 的 gatekeeper；被触发时必须同时做 Boundary Review 和 Evolution / Implementation-Entry Review。
- 必须输出两个 verdict：`Design Freeze Validity` 判断边界、truth placement、scope delta 和 overclaim；`Implementation Entry Readiness` 判断 Builder 是否能从该 artifact 安全开始最小实现。
- 对大型设计对象必须检查 minimum safe slice、implementation ladder、next-session map、输入/输出/验收证据、明确非目标和 future-agent misuse scenario；缺少这些时，即使 design freeze 可通过，也应至少给 P1 follow-up。
- 必须做状态词压缩误读测试：`done`、`landed`、`active`、`covered`、`integration`、`complete`、`support`、`foundation` 等词若出现在 row/title/status/closeout headline，需确认未来 Agent 只看到一行时不会误读。
- Goal 若同时要求 pre-Builder Semantic Review 和 final Semantic Review，必须分别保留可定位的时序证据。Builder 后的 landed-package review 不能倒推或冒充 pre-Builder review。
- 如果 Orchestrator 要求立即收束但必读证据、验收标准、Original Plan Coverage Matrix、Scope Delta audit、Validation Handoff 或 closeout-language gate 不完整，Semantic Reviewer 也必须回复：`当前不能声明完成；缺失证据为：...；可选收束状态只能是 blocked/partial，不能是 pass/done。`

## Multi-Agent Gate

- tracked Session、Stage Plan、Goal 或 non-trivial governed work 默认运行 Multi-Agent Activation Gate。
- 当任务会改变 KB truth、Dashboard state、acceptance posture、fixtures/tests、runtime/schema behavior，或需要 design handoff、validation handoff、closeout artifact 时，默认启动 Design、Builder、Validation、Closure lanes；Semantic Reviewer 和 Dashboard Agent 由各自触发条件决定。
- 用户已授权 Codex 按需使用 subagents / delegation / parallel agent work；当前工具若还要求本轮显式授权，则在执行模板中写明：`本轮显式授权 Codex 按需使用 subagents / delegation / parallel agent work；是否启用由 Multi-Agent Activation Gate 决定。`
- 如果默认 lane 未启动，closeout 必须记录 `Single-Agent Exception`：原因、风险、补偿检查，以及是否缺少独立 Design 或 Validation verdict。用户沉默不是有效例外。
- 经 intake 明确分类为 `delta-only read-only reconciliation`、且不含 Builder、KB truth、runtime/schema、acceptance 或 semantic widening 的任务，可以只启动独立 Validation lane；未启动本来就无工作的 lanes 记录为 `not applicable for delta-only review`，不算 Single-Agent Exception。
- Goal / Stage Plan 若明确要求 Builder 使用独立、用户可见 execution task，closeout 必须记录 task/thread ID、worktree（如有）和 Builder 实际所在 task。仅创建 task 但由 Orchestrator 主线程完成 Builder，不算满足该要求。
- 主线程接管明确要求独立 task 的 Builder 时，必须先取得人类批准的 topology exception，并记录批准 reference、影响和补偿检查。事后补写 `Single-Agent Exception` 或补跑测试不能追溯性地恢复完整 Goal conformance。

## Closeout / Validation Gate

- non-trivial governed work 若改变 tracked session、Stage Plan、KB truth、acceptance posture、fixture/test pack 或 substantive Dashboard state，必须创建或更新 Dashboard closeout artifact，并让相关 Dashboard row 引用它。
- closeout artifact 必须使用中文标题和中文解释。推荐标题：`关键结论中文展开`、`落地范围`、`明确非目标`、`Lane 启动与例外`、`设计交接`、`验证交接包`、`验证结论`、`证据`、`运行的门禁`、`语义复核`、`延后范围`、`KB/Dashboard 复核`、`后续候选`。
- 面向人类的证据引用规则：Closeout、final summary、Dashboard parent/row prose 以及 `验证交接包` 的解释性正文，必须给出可点击的 Markdown 源文件链接，不得把裸 SHA-256/hash/digest 数字当作证据入口。机器门禁所需的摘要继续保留在 lane card、manifest、snapshot、JSON 或验证报告等机器证据中；Closeout 只链接对应源文件，并用中文说明它证明什么、不能证明什么。历史不可变 artifact 可以保留原有摘要，不要求为此改写历史记录。
- closeout 前必须运行 closeout-language gate：检查 closeout 的 H1/H2 是否为中文、英文 verdict/status 是否有中文解释。未通过时不能声明最终完成。
- Validation Handoff 必须包含 `Closeout language verdict`。该 verdict 未通过或缺失时，不能写最终完成。
- Validation Agent verdict 是 final closeout gate；没有独立 Validation 时必须记录例外，不能把 Validation Handoff Packet 或 Orchestrator 自检冒充 Validation verdict。
- non-trivial governed closeout 进入最终完成态时，无论是否主动写出 `Independent Validation passed`，都必须存在并显式链接可定位的 durable Validation Review / post-closeout reconciliation artifact，包含唯一且无冲突的 passing verdict、唯一 reviewer/source、Read Manifest、实际 closeout、最终 Dashboard/KB 状态和最终 diff。省略 verdict、重复冲突记录、Validation Handoff、Semantic Review、测试通过或 Orchestrator 摘要均不能绕过该证据门禁。
- Final Validation / Semantic verdict 必须覆盖实际用于关闭任务的 closeout、Dashboard/KB 最终状态和最终 diff。发生在这些文件写入之前、仍记录 closure blocker 的 verdict，只能证明当时已读 package；除非 reviewer 明确读过 closeout draft 且最终内容无实质变化，或补做独立 post-closeout reconciliation，否则不能支撑 `done`。
- 多 Session final audit 必须提供 Evidence Completeness Matrix，逐项覆盖每个 Session 的技术 must-have、流程 must-have、task topology、Validation/Semantic 时序、closeout、最终父面和 Scope Delta。矩阵不能只是把 MH/AC 合并成“检查过”的关键词索引；每个原始 must-have/AC 必须有独立行，或有明确的分组理由和组内逐项清单，并至少列出验收判定、精确源文件链接、实际结果、状态、阻断/例外、时序/拓扑、claim ceiling 与最终 parent/Closeout 吸收情况。漏审流程 must-have 时不得写 `Scope Delta: 无` 或 audit complete。
- closeout 若声明 BDD readable cards 已落地，必须把 cards 写入并保留在 `tests/bdd/readable_cards/<gate>/`（或等价受版本控制路径）；仅写入 `.sge/reports/`、`/tmp` 或其他临时 report-dir 不算 durable readable-card evidence。

## KB / Dashboard Review Gate

- 每个 non-trivial task 结束前必须明确判断是否更新 `kb/` 和 `Dashboard/`。
- 更新 `kb/`：稳定 truth、implementation scope、contract、terminology、rollout policy、artifact semantics 或 future-agent policy 发生变化。
- 更新 `Dashboard/`：task state、priority、blocker、decision、active work、completion state、closeout evidence 或 concrete next candidate 发生变化。
- Contract Delta Scan：approved proposal、closeout、reviewed seed、baseline、matrix、contract 或 gate artifact 含稳定规则时，必须分类为 `promote-to-KB`、`Dashboard-only`、`gate-docs later`、`runtime/tests later` 或 `deferred session`。
- 如果出现 concrete follow-on、deferred remainder 或 later candidate，必须在同一任务中写入或更新 `Dashboard/Sessions.md`；不要只留在聊天或 closeout prose。

## Repo Checkpoint Entry

- 非平凡 SGE 工作必须使用 `.codex/skills/sge-governed-checkpoints/SKILL.md`。
- 常用命令：
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode intake-evaluation`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode context-bootstrap`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/context_bootstrap.py validate <packet.json>`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode sgc`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode goal-conformance`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode goal-agent`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode loop-continuation`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode validation-agent`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode semantic`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode closeout`
  - `python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode closeout-language --file <closeout.md>`

## Detailed Rule Locations

- Workflow/checklists/scripts：`.codex/skills/sge-governed-checkpoints/`
- Human-AI governance strategy：`kb/data/strategy/strategy_human_ai_development.json`（如已迁移）
- SGC v1 canonical contract：`kb/data/strategy/strategy_sgc_structural_contract_v1.json`
- Dashboard method/rules：`Dashboard/Methodology.md`、`Dashboard/Rules.md`
- Agent Logs policy/templates：`Dashboard/Agent_Logs/`
