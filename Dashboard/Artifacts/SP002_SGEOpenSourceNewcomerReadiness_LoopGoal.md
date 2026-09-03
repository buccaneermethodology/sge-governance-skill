# SP-002 SGE Governance 公共候选与新手可用性 Loop Goal

## 文档身份

- Goal ID：`SP-002`
- Goal 类型：多 Session、连续执行的公共候选与 clean-room 新手验收 Loop Goal
- 初始状态：`To do`；实时执行状态以 `Dashboard/Stage_Plans.md` 与 `Dashboard/Sessions.md` 为 authority，本 Goal 不承载易漂移的动态状态。
- Base：[`SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md`](SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md)
- Applied Patch：[`SP002-GP-001`](SP002_SGEOpenSourceNewcomerReadiness_GoalPatch.md)
- 初始入口：`S-007`；后续入口由 Session continuation scan 和 Dashboard 实时状态决定。
- 前置条件：SP-001 的 repo-local completion 已由最终独立对账支持；用户已在 2026-09-02 明确授权启动并连续执行 SP-002。

## 关键结论中文展开

本 Goal 的目标不是把当前工作仓库原样上传到公共仓库，而是从它构建一个经过逐文件裁决的、可安装的 SGE Governance Skill 公共候选，并验证一名没有 Semx 背景的新手可以在 clean-room 项目中使用它。

本仓库同时包含两类内容：一类是未来可公开的通用 Skill、去项目化 KB 和用户文档；另一类是本仓库特定的执行面，例如 Dashboard 状态、Session/Goal、Agent Logs、closeout、历史迁移 provenance、完整测试报告和本机路径。这两类内容必须物理上和合同上分离。`public candidate pass` 只表示候选包在声明范围内通过验证，不表示已经公开发布、普遍适用或生产就绪。

## 原始用户意图与读取清单

### 原始授权

用户要求：如果 SP-002 尚无正式 Goal，则先设计；若已有设计，将 glossary 内容加入；并在 Goal 中明确本仓库是开源 Skill，而本仓库特定的执行面信息不应放入公开仓库，要求给出合适的处理方式。

### 已读

- [仓库硬门](../../AGENTS.md)：Goal、Scope Delta、SGC、Multi-Agent、Validation、closeout 和 KB/Dashboard 分层。
- [SGE governed checkpoints](../../.codex/skills/sge-governed-checkpoints/SKILL.md)：Goal handoff、lane、原始目标覆盖、独立验证和终止条件。
- [SP-001 Final Closeout](SP001_S015_FinalClosure_Closeout.md)：SP-001 的 claim ceiling 与公共发布非目标。
- [SP-001 Final OPCM](SP001_S015_FinalClosure_OPCM.md)：原始流程 must-have 和最终证据边界。
- [当前 Dashboard 状态](../Current_State.md)、[Stage Plans](../Stage_Plans.md)、[Sessions](../Sessions.md)、[Artifacts Index](../Artifacts_Index.md)：SP-002 当前为 `To do`，S-007 尚未启动。
- [现有 SP-002 Stage Plan](SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md)：原始 S-007～S-011 DAG、公共候选和新手验收目标。
- [SP-002 规划 Context](SP002_SGEOpenSourceNewcomerReadiness_ContextBootstrap.json)：既有 authority、非目标和 source-reading 边界。
- [SP-002 规划 Closeout](SP002_PlanningAndSP001StrategyExpansion_Closeout.md)：确认原规划只完成 tracking，不等于实施或发布。
- [当前 KB README](../../kb/README.md)、[KB Promotion Strategy](../../kb/docs/strategy/Strategy_KB_Promotion_and_Source_Policy.md)、[Human-AI Strategy](../../kb/docs/strategy/Strategy_Human_AI_Development.md)、[Semantic Surface Strategy](../../kb/docs/strategy/Strategy_Semantic_Surface_Engineering.md)：truth carrier、公共边界与 execution memory 分层。
- `semx-cli` 的候选来源 locator 为 `../../../../semx-cli/semx-kb/data/glossary.json` 与 `../../../../semx-cli/semx-kb/docs/Glossary.md`；它们不属于本仓库可点击证据面，其中 Semx、pipeline、runtime、产品 ontology 必须排除。

### 未读或刻意跳过

- 未把 `semx-cli` glossary 的 schema、validator、fixtures 或整套条目当作当前 Goal 的 canonical truth。
- 未读取 provider、产品 runtime、远端 release 或任何凭据；这些不属于当前设计授权。

## 使命

在 SP-001 的 repo-local SGE core 基础上，冻结并验证一个可审计的公共候选：它具有清晰的 license/provenance、default-deny export、去项目化 SGE glossary、四层 Skill 分层、中文 Beginner Guide、可恢复的 install/doctor/bootstrap/upgrade/uninstall 路径、可选 domain extensions，以及独立 clean-room user acceptance。

## Public / Private Execution-Surface Contract

### 公共候选允许进入的表面

| 层 | 允许内容 | 必须满足 |
| --- | --- | --- |
| Public core | `.codex/skills/sge-governed-checkpoints/` 的通用 Skill 与必要 schema/script | 无项目 ID、无本机路径、无私有 Session/Goal、license/provenance 已裁决 |
| Public governance docs | 去项目化 README、Beginner Guide、Quick Start、安装/卸载说明、故障恢复说明 | 面向陌生用户，可复制，可从 clean-room 验证 |
| Public canonical KB | 去项目化的稳定治理 JSON 及其 Markdown projection，包括 SGE glossary v1 | JSON 是真源；source scope 不暴露私有绝对路径；renderer/check 通过 |
| Public tests/examples | 通用 contract、negative cases、最小 demo-consumer fixture | 不包含本仓库历史、私有数据、Semx 产品路径或未批准执行证据 |
| Public metadata | LICENSE、NOTICE、public export manifest、版本和 release candidate metadata | 每个文件有来源/许可证/是否 public 的明确裁决 |

### 默认留在私有执行面的表面

| 层 | 不应公开的内容 | 处理方式 |
| --- | --- | --- |
| Private execution memory | 本仓库 `Dashboard/` 的 Goal、Stage Plan、Sessions、状态、blocker、closeout、OPCM、Big Ideas、Decisions | 留在 target repo 或内部治理仓库；不作为公共 Skill 安装输入 |
| Private agent trace | `Dashboard/Agent_Logs/`、lane prompts、task cards、reviewer thread identity、完整工作树 diff | 只保留内部审计；如需公开，必须另做最小化、去身份的示例并重新裁决 |
| Private provenance | 原始 `semx-cli`/其他仓库的本机绝对路径、私有 revision locator、迁移 inventory、历史产品设计 locator | 使用逻辑 provenance/tombstone；公共 manifest 只保留必要的可公开来源信息 |
| Private evidence | 本仓库特定的 doctor 快照、完整测试日志、当前 Session 数量、未提交文件和内部 acceptance 记录 | 作为发布前内部证据，不进入 public export；公共包只提供可重跑的通用检查 |
| Target-project overlay | 使用者自己的 `AGENTS.md`、`Dashboard/`、project profile、Session、Goal、source registry 和产品扩展 | 安装 Skill 后在目标项目生成或维护；公共 Skill 不携带本仓库的执行状态 |

### 物理处理规则

1. public export 从干净 staging directory 构建，不从当前工作树直接复制。
2. `public_export_manifest_v1.json` 使用显式 allowlist/default-deny；未知文件、绝对路径、内部 Session、历史 evidence 和未裁决 provenance 一律拒绝。
3. public 包与执行 overlay 使用不同根目录、不同 manifest 和不同 validation profile；不能用 `.gitignore`、目录命名或“历史文件不会被看到”作为边界。
4. 公共包中的稳定治理规则进入 `kb/data/`；本仓库当前执行状态继续留在 Dashboard，不反向提升为公共 canonical truth。
5. public candidate、release authorization、Git、remote push 和 production readiness 分轴记录。

## Glossary 目标

S-007 必须设计并冻结 `SGE Governance Glossary v1`，而不是复制 Semx glossary v2.x。

### 应纳入的通用术语族

- `Canonical Truth`、`KB / Dashboard Truth Split`、`Doc as Data`
- `Evidence`、`Candidate`、`Claim Ceiling`、`Scope Delta`、`Promotion`
- `Session`、`Stage Plan`、`Lane Task Card`、`Validation Handoff`
- `Semantic Reviewer`、`Closeout / Governance Memory`
- `Design Freeze Validity`、`Implementation Entry Readiness`、`Minimum Safe Slice`
- `Future-agent Misuse Scenario`、`SGC`、`ERBE`

### 必须排除或重新命名的来源术语

- `Semx`、SCKS、M0.5、P02–P08、M1/Mc/Flow/DRP；
- Runtime Kernel、SAG、RCP、USL 及其产品运行时语义；
- Semx 专属 source refs、产品 phase、P00–P17、KYM/TCO 和当前产品 Session IDs。

### Glossary 验收

- 真源为 `kb/data/glossary_v1.json`，可读面为 `kb/docs/Glossary.md`。
- 每个条目至少有 term、definition、scope、authority、boundary、claim ceiling、forbidden overreads、related concepts 和 source refs。
- `source_refs` 只指向当前公开或明确可审计的 SGE source；不暴露本机绝对路径。
- renderer 生成与 `--check` 通过；未知字段、重复 term、重复 section、缺 source ref 和错误类型应有 negative cases。
- glossary 定义稳定术语，不承载当前 Session status、候选 verdict、发布批准或产品能力。

## Original Must-Have Ledger

| ID | 原始要求 | 可观察验收 | Owner / 时序 | 状态 |
| --- | --- | --- | --- | --- |
| SP002-MH-01 | 冻结 license、第三方 provenance 与 public/private 边界 | 每个候选文件有 license/source/public 裁决；私有执行面有排除清单 | S-007 | pending |
| SP002-MH-02 | public export 使用 allowlist/default-deny | clean staging export 只含 manifest 允许文件；未知/绝对路径/历史 evidence 被拒绝 | S-007 | pending |
| SP002-MH-03 | 明确 core、companion、orchestrator、domain extension 四层 | 安装顺序、依赖图、optional contract 和 claim ceiling 可核对 | S-007 | pending |
| SP002-MH-04 | 提供中文 Beginner Guide、Quick Start、minimal project 和可复制 prompts | 无 Semx 背景的新手可执行 bootstrap→Goal→Session→Validation→closeout | S-008 | pending |
| SP002-MH-05 | 提供 install/doctor/bootstrap/upgrade/uninstall | clean-room 正反例通过，失败可恢复 | S-008 | pending |
| SP002-MH-06 | 将 loop 编排去产品硬编码并改为可选扩展 | profile/hooks 驱动；核心不要求固定项目、KYM/TCO 或产品 project | S-009 | pending |
| SP002-MH-07 | 独立 user-acceptance-test 验证新手路径 | 一问一答、可读性、错误恢复和 claim 边界由独立 lane 验收 | S-010 | pending |
| SP002-MH-08 | KYM/TCO 保持 optional domain extensions | 未安装时 core/Quick Start 通过；安装时有显式接口和 provenance | S-009 | pending |
| SP002-MH-09 | clean-room 身份隔离与无绝对路径验收 | 新 repo 安装、doctor、示例、卸载无私有路径/产品身份残留 | S-010 | pending |
| SP002-MH-10 | 独立 Validation、Semantic Review、closeout 与发布授权边界 | final candidate 覆盖实际 diff；实际发布仍需具体人类批准 | S-011 | pending |
| SP002-MH-11 | 建立去项目化 SGE Governance Glossary v1 | canonical JSON/Markdown、source refs、negative cases 和 renderer check 通过 | S-007→S-011 | pending |
| SP002-MH-12 | 将公共 Skill 与本仓库特定执行面物理/合同隔离 | default-deny staging export 排除 Dashboard/Agent Logs/历史 provenance/内部 evidence；target overlay 可独立运行 | S-007→S-011 | pending |

## Process Must-Haves

| ID | 流程要求 | 验收证据 |
| --- | --- | --- |
| PROC-01 | C0、Design、Builder、Validation、Closure 按适用时序运行 | lane cards、Agent Logs、Design/Validation Handoff、closeout |
| PROC-02 | Semantic Reviewer 在公共边界、glossary、通用化或 promotion 风险出现时运行 | Design Freeze Validity + Implementation Entry Readiness |
| PROC-03 | Validation 同时检查本 Goal 和 revised design；最终 review 覆盖 closeout、Dashboard/KB 和完整 diff | durable Validation Review / post-closeout reconciliation |
| PROC-04 | 每个 Session closeout 后运行 continuation scan；ready 且无需人类决定时自动进入下一 Session | `goal_terminal`、`next_session`、`next_session_ready`、`human_decision_required` |
| PROC-05 | public release 是独立人类授权 checkpoint | release decision packet；无自动 push/release |

## Session DAG

| Session | 主题 | 主要输出 | 退出条件 |
| --- | --- | --- | --- |
| S-007 | 公共合同、四层分层、glossary 与执行面隔离冻结 | Public Contract、public/private matrix、manifest/schema、Glossary Design、ERBE/Semantic Review | provenance、边界、glossary scope 和 negative cases 冻结 |
| S-008 | Beginner Guide 与 bootstrap 工具 | Guide、Quick Start、minimal repo、install/doctor/bootstrap/upgrade/uninstall | 文档命令与 clean-room 行为一致 |
| S-009 | 高级编排与 optional extensions | `run-sge-loop-goal-cycle` 通用候选、extension registry、KYM/TCO companion contract | 核心无产品依赖，optional interface 有 provenance |
| S-010 | clean-room 新手验收 | 独立 UAT evidence、修复记录、身份/路径扫描 | 独立 UAT 对真实入口给出有界通过 |
| S-011 | 公共候选最终收束 | package manifest、OPCM、Validation/Semantic、post-closeout、release decision packet | candidate gates 全部通过；发布仍等待人类授权 |

固定依赖为 `S-007 → S-008 → S-009 → S-010 → S-011`。Session closeout 不是 Goal 停止点。

## Governance Workflow

- Task Intake：确认用户目标是设计/修订 SP-002 Goal，而不是启动或发布。
- ERBE applicability：`required`，因为本 Goal 冻结 public/private authority、export predicates、glossary contract 和 release boundary。
- SGC v1：检查 claim level、evidence layer、SI-1..SI-6、false closure 和 public/release/production forbidden collapses。
- Multi-Agent：C0 后默认启动 Design、Builder、Validation、Closure；glossary、genericization、truth placement 和 public boundary 触发 Semantic Reviewer。
- Lane delegation：每个 lane 先验证并渲染 `lane_task_card_v1`；接收端必须运行 expected digest 校验。
- Builder：只修改当前 Session card 声明的 public candidate/contract surface；不得修改 frozen Goal、Glossary contract、allowlist 或 private/public boundary 而不走 Contract Patch + Scope Delta。
- Validation：read-mostly，必须从 durable inputs 重算实际 candidate、public manifest、glossary render、clean-room 和最终 diff。
- Closure：建立中文 closeout、Original Plan Coverage Matrix、Scope Delta、KB/Dashboard review、closeout-language 和 post-closeout reconciliation。

## Validation Handoff

Validation 必须读取：本 Goal、base Stage Plan、Goal Patch、SP-001 final closeout/OPCM、当前 Dashboard/KB、实际 public staging diff、license/provenance manifest、Glossary JSON/Markdown、ERBE Contract/Cases、clean-room test、S-007～S-011 closeout、Semantic Review 和完整 tracked/untracked diff。

验证必须分别报告：

- public candidate 与 private execution overlay 是否分离；
- glossary 是否只承载稳定 SGE terminology；
- license/provenance/allowlist 是否逐文件闭合；
- core/companion/orchestrator/domain extension 是否发生依赖折叠；
- tests/doctor/UAT 是否只支撑声明的边界；
- 是否存在把 candidate、active、published、production 或 Dashboard `Done` 混成同一状态的 overclaim。

## Semantic Reviewer 触发条件与双 verdict

以下任一情况必须启动 Semantic Reviewer：

- 新增或 promotion glossary term；
- 改变 public/private authority、export manifest 或 license/provenance 规则；
- 将现有 Semx 内容去项目化为 SGE 通用规则；
- 修改 core/companion/orchestrator/domain extension 边界；
- 引入新 acceptance posture、release candidate 或 clean-room claim。

Semantic Reviewer 必须给出：

1. `Design Freeze Validity`：authority、ontology、truth placement、scope delta 和 claim ceiling 是否有效。
2. `Implementation Entry Readiness`：Builder 能否从最小公共切片安全开始，且有明确输入、输出、negative cases、implementation ladder 和 next-session map。

并至少列出三类 future-agent misuse scenario，例如：

- 把 public package 中的 Dashboard 状态当成公共 Skill 的 canonical truth；
- 把 glossary 中的 `active`/`validated` 术语当成当前 release approval；
- 复制一个可选 domain extension 后误以为 core 依赖该产品领域。

## KB / Dashboard Truth Placement

- 稳定 glossary 术语、public/private contract、export policy 中可复用的规则：经 Contract Delta Scan 后进入 `kb/data/`；Markdown 由 renderer 生成。
- 当前候选状态、文件级 license 裁决、blocker、Session、closeout、UAT 结果和 release decision：留在 `Dashboard/`。
- public manifest 是候选/发布证据，不是 KB truth；必须同时保留 provenance 与 claim ceiling。
- 本次 Goal 设计本身只新增 Dashboard Goal/Stage Plan 交接，不提前 promotion glossary 或 public contract truth。

## Scope Delta 审计

本次 `SP002-GP-001` 的变化是显式新增 `SP002-MH-11` 和 `SP002-MH-12`，并明确 S-007 的最小入口。没有删除、替换、降级原 `SP002-MH-01..10`；也没有把公共发布授权、生产成熟性或任意 repo 支持加入当前 Goal。

## Loop Continuation Contract

本 Goal 默认连续执行整个 Session DAG。任意单一 Session、lane、closeout 或 post-closeout pass 都不是停止条件。每次 Session closeout 后必须记录 `goal_terminal`、`next_session`、`next_session_ready`、`human_decision_required`；当 Goal 未终止、下一 Session ready 且无需人类决定时，Orchestrator 必须在同一执行回合进入下一 Session。

允许暂停或结束的情况只有：Goal completion rule 满足；用户明确暂停；需要人类作出未提供的 public release、license、destructive 或 Scope Delta 决定；关键工具/网络中断；同一恢复条件连续失败超过三次。

## Completion Rule

只有以下条件全部满足，才允许写 `SP-002 complete` 或“公共候选完成”：

1. SP002-MH-01..12 和 PROC-01..05 均有逐项证据；
2. `public_export_manifest_v1.json` 在干净 staging 中 default-deny 通过，且未知文件/绝对路径/历史执行面 negative cases 失败；
3. `kb/data/glossary_v1.json` 与 `kb/docs/Glossary.md` 确定性一致，Glossary source refs、边界和 negative cases 通过；
4. core、companion、orchestrator、domain extension 四层依赖与安装顺序通过独立 Validation；
5. Beginner Guide、Quick Start、install/doctor/bootstrap/upgrade/uninstall 在 clean-room 中可重放；
6. 独立 user-acceptance-test、Validation、Semantic Review、中文 closeout 和 post-closeout reconciliation 覆盖实际最终 diff、public manifest、KB/Dashboard 和原始目标；
7. license/provenance 和 public/private execution-surface matrix 无未裁决文件；
8. `public candidate`、`release authorized`、Git、push、production 等状态保持分离；实际发布仍需单独人类授权。

## Termination Conditions

- `complete`：Completion Rule 全部满足，仅支持有界 public candidate claim。
- `paused_by_user`：用户明确暂停或停止。
- `human_authority_required`：缺少 license、release、destructive action 或 Scope Delta 决定。
- `tool_interruption`：关键工具/环境中断且无法恢复。
- `recovery_ceiling`：同一恢复条件连续失败超过默认三次。

## 允许与禁止的 Closeout 用语

允许：

- “SGE 公共候选在声明的 clean-room 范围内通过结构与独立可用性验收。”
- “public export manifest 通过；实际公开发布仍等待人类授权。”
- “本仓库执行面未进入 public export，留在 target project/internal governance overlay。”

禁止：

- “仓库已经公开发布”或“release 已完成”，除非有具体人类授权与外部证据；
- “任意 repo 都适用”或“生产就绪”；
- “Dashboard/Agent Logs/历史 provenance 随 Skill 一起公开”；
- 以 glossary、doctor、schema 或 clean-room 单项通过替代完整 Goal completion。

## CG 状态

`CG skipped: no CG input provided`
