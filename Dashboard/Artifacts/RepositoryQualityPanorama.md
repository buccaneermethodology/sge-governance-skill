# SGE Governance Skill 仓库质量 Dashboard 全景

> 这是 2026-09-02 当前工作树的派生读模型，不是 `kb/` 真源、Dashboard 状态 authority、批准凭据或完成证明。

## Big Idea: 可复用 SGE 语义治理工程与质量状态
- Big Idea Length: Unknown
- Coverage: Unknown
- Key Points:
  - SP-001 当前父状态为 `Doing`，当前入口 S-012 也是 `Doing`；旧 S-006 closeout 不覆盖新发现的 active legacy。
  - 当前全景覆盖 Dashboard 控制面、Stage Plans、Sessions、Decisions、Risks、Exceptions、Artifacts、Agent Logs、KB、Skill、tests 与 Git。
- Next Suggestions:
  - 优先完成 S-012、修复 active/public legacy 与 registry 派生漂移，再进入 SP-002 公共候选工作。

### Sessions
| Session ID | Session Type | Topic | Scope | Purpose | Length (minutes) | Key Points |
|------------|--------------|-------|-------|---------|-------------------|------------|
| SP-001/S-001 | Exploration | Git 种子基线、Loop Goal 与迁移计划落库 | 建立整理前 Git seed，落库 Final Loop Goal、迁移计划、Context 与 Dashboard entry；不启动 S-002 | 让后续迁移拥有可恢复基线和 durable handoff contract | Unknown | seed commit、Goal、Plan、Context、Dashboard rows、closeout、独立 Validation Review；registry 与语言门禁通过；独立 Validation 覆盖实际 diff；S-001 closeout 明确不等于 SP-001 完成 |
| SP-001/S-002 | Exploration | 来源、project profile、ERBE 与通用 SGE 核心冻结 | 固定全部 Skill 与 strategy provenance；完成 56 个 docs 表面到 canonical JSON mapping；建立 profile 并冻结 Contract/Cases/RED/write exclusions | 为迁移建立不可偷换的机器合同、最小通用核心边界与策略来源 authority | Unknown | source manifest、typed ledger、profile/schema、ERBE bundle、Design、Semantic Review、S-002 closeout、最终 Validation；C01-C04 同 identity 重算通过；closeout-language、registry、最终 diff 与 topology exception 均有证据 |
| SP-001/S-003 | Exploration | Governance Skills、strategy contracts 与 deterministic tooling 迁移 | 迁移适用 Skills、通用 strategy truth/read models、schemas、scripts 和 workflow registry | 使 repo-local checkpoints 可执行并为后续抽取做准备 | Unknown | tooling、schemas、workflow registry、closeout、独立 Validation、post-closeout reconciliation；结构/接口/身份/registry/语言门禁通过；S-004 提前删除不作为本 Session 证据 |
| SP-001/S-004 | Exploration | KB、AGENTS、Dashboard tools 整理及身份污染清除 | 删除无意义 Semx/KYM/TCO/P00–P17/runtime 历史，修正 audio-transcriptor truth/authority 入口并记录替代机制 | 形成新项目自洽且低污染的治理目录 | Unknown | 清理记录、适配后的 AGENTS/Dashboard/KB、独立 Validation、中文 closeout；身份、truth split、替代机制、registry、diff 与原始设计字节检查通过；不证明产品实现 |
| SP-001/S-005 | Exploration | 集成验收、独立 Validation 与 Semantic Review | 对最终候选执行完整本地 gates、56/56 strategy coverage、原目标审计和语义架构复核 | 阻止工具自报、阅读面/canonical 折叠、局部测试或保守措辞冒充整体迁移完成 | Unknown | 集成 Validation Review、Semantic Review、Context、lane card；11 项 MH 有 evidence mapping；最终结论有界，可进入 S-006 |
| SP-001/S-006 | Exploration | Goal closeout 与最终对账 | 形成中文 closeout、MH-01..MH-11 OPCM、Scope Delta、KB/Dashboard review 和 post-closeout reconciliation | 给 Goal completion 提供唯一、无冲突、覆盖最终状态的证据 | Unknown | [S-006 Closeout](../../Artifacts/SP001_S006_GoalClosure_Closeout.md)、[OPCM](../../Artifacts/SP001_S006_GoalClosure_OPCM.md)、[Post-closeout](../../Artifacts/SP001_S006_GoalClosure_PostCloseoutReconciliation.md)；MH-01..MH-11 逐项证据、closeout-language、registry、最终 diff 与 claim ceiling 对齐 |
| SP-002/S-007 | Proposed | 公共合同、license/provenance 与四层 Skill 架构冻结 | 在 SP-001 完成后冻结 public/private allowlist、license、provenance、core/companion/orchestrator/domain-extension 边界与 ERBE | 防止把 repo-local 候选未经授权包装成可公开发布的巨型 Skill | N/A | Public Contract、export manifest/schema、Design 与 Semantic Review；provenance 完整、negative cases 与公共 claim ceiling 冻结 |
| SP-002/S-008 | Proposed | 中文 Beginner Guide 与 bootstrap 工具 | 编写 Quick Start、傻瓜式指南、minimal project、install/doctor/bootstrap/upgrade/uninstall | 让无 Semx 背景的新手可完成最小治理循环并安全恢复 | N/A | Beginner Guide、copyable prompts、minimal repo、工具与 fixtures；文档命令、工具行为和错误恢复在 clean-room 一致 |
| SP-002/S-009 | Proposed | 通用 Loop 编排与 optional extension 接口 | 将 run-loop-goal-cycle 去 Semx/KYM/TCO 硬编码并定义 companion/domain hooks | 提供高级自动化但保持核心 Skill 可独立安装和使用 | N/A | run-sge-loop-goal-cycle candidate、extension registry、tests；无默认 Semx/KYM/TCO/ChatGPT project 依赖；缺扩展时核心仍通过 |
| SP-002/S-010 | Proposed | clean-room 安装与独立小白验收 | 全新环境按 Beginner Guide 完成安装、最小 Goal/Session、Validation、closeout、故障恢复和卸载 | 用独立真实用户路径识别文档作者和 Skill 作者看不到的问题 | N/A | clean-room evidence、user-acceptance-test verdict、repair loop；独立 UAT 对真实入口给出有界通过结论且 blocking findings 清零 |
| SP-002/S-011 | Proposed | 公共发布候选、独立 Validation 与 closeout | 生成 default-deny candidate package，完成 OPCM、Semantic Review、Validation 与 post-closeout reconciliation | 形成可供人类决定是否发布的稳定候选，而不越权执行发布 | N/A | package/manifest、Validation/Semantic、中文 closeout、release decision packet；candidate gates 全部通过；实际发布仍需具体人类授权 |
| SP-001/S-012 | Exploration | Active legacy 清理与 Skill 通用性验收 | 清理 S-485/legacy migrate、Semx 全景工具、绝对源路径和非通用 Dashboard 表面；建立 generic clean-room portability test | 使 SGE Governance Skill 不再依赖迁移项目历史，并以可重复测试证明可被不同项目 profile 使用 | Unknown | 清理后的 Rules/Methodology/registry/tools、通用 profile、portability test、独立 Validation、中文 closeout、post-closeout reconciliation；active surface 无 legacy authority；通用性测试通过；registry、closeout-language、最终 diff 与独立 Validation 通过 |
| BQ-K1 | Knowledge | Dashboard 控制面 | 10 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A | Dashboard/Current_State.md；Dashboard/Big_Ideas.md；Dashboard/Stage_Plans.md；Dashboard/Sessions.md；Dashboard/Session_Index.md；Dashboard/Decisions.md；Dashboard/Risks.md；Dashboard/Exceptions.md；Dashboard/Rules.md；Dashboard/Methodology.md |
| BQ-K2 | Knowledge | Dashboard artifacts | 89 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A | Dashboard/Artifacts/RepositoryQualityPanorama.html；Dashboard/Artifacts/RepositoryQualityPanorama.md；Dashboard/Artifacts/RepositoryQualityPanorama_Audit_Design.md；Dashboard/Artifacts/RepositoryQualityPanorama_Audit_Report.md；Dashboard/Artifacts/RepositoryQualityPanorama_ContextBootstrap.json；Dashboard/Artifacts/RepositoryQualityPanorama_Data.json；Dashboard/Artifacts/RepositoryQualityPanorama_FinalValidation.md；Dashboard/Artifacts/RepositoryQualityPanorama_FinalValidation_ContextBootstrap.json；Dashboard/Artifacts/RepositoryQualityPanorama_FinalValidation_Delta.md；Dashboard/Artifacts/RepositoryQualityPanorama_FinalValidation_Delta_LanePrompt.txt；Dashboard/Artifacts/RepositoryQualityPanorama_FinalValidation_Delta_LaneTaskCard.json；Dashboard/Artifacts/RepositoryQualityPanorama_FinalValidation_LanePrompt.txt |
| BQ-K3 | Knowledge | Agent Logs | 4 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A | Dashboard/Agent_Logs/2026-09-01__S-001__builder-repair.md；Dashboard/Agent_Logs/2026-09-01__S-001__closure.md；Dashboard/Agent_Logs/2026-09-01__S-001__post-closeout-validation.md；Dashboard/Agent_Logs/2026-09-01__S-001__validation.md |
| BQ-K4 | Knowledge | KB canonical JSON | 6 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A | kb/data/strategy/sge_project_profile_v1.json；kb/data/strategy/sge_strategy_canonical_mapping_v1.json；kb/data/strategy/sge_strategy_source_manifest_v1.json；kb/data/strategy/sge_workflow_registry_v1.json；kb/data/strategy/strategy_erbe_specification_first_acceptance_v1.json；kb/data/strategy/strategy_sgc_structural_contract_v1.json |
| BQ-K5 | Knowledge | KB reader Markdown | 2 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A | kb/docs/strategy/Strategy_ERBE_Specification_First_Acceptance_V1.md；kb/docs/strategy/Strategy_SGC_Structural_Contract_V1.md |
| BQ-K6 | Knowledge | Repo-local Skill 与治理工具 | 17 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A | .codex/skills/sge-governed-checkpoints/SKILL.md；.codex/skills/sge-governed-checkpoints/agents/openai.yaml；.codex/skills/sge-governed-checkpoints/references/checklists.md；.codex/skills/sge-governed-checkpoints/references/context-efficient-goal-validation.md；.codex/skills/sge-governed-checkpoints/schemas/goal_contract_v1.schema.json；.codex/skills/sge-governed-checkpoints/schemas/goal_patch_v1.schema.json；.codex/skills/sge-governed-checkpoints/schemas/lane_prompt_audit_v1.schema.json；.codex/skills/sge-governed-checkpoints/schemas/lane_task_card_v1.schema.json；.codex/skills/sge-governed-checkpoints/schemas/validation_state_snapshot_v1.schema.json；.codex/skills/sge-governed-checkpoints/scripts/context_bootstrap.py；.codex/skills/sge-governed-checkpoints/scripts/context_efficiency_pilot.py；.codex/skills/sge-governed-checkpoints/scripts/context_state.py |
| BQ-K7 | Knowledge | Tests 与验证表面 | 2 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A | tests/contract/__pycache__/sge_skill_generality.cpython-310.pyc；tests/contract/sge_skill_generality.py |
| BQ-K8 | Knowledge | Decisions | 5 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A | DEC-001: 本轮能力边界 [Done]；DEC-002: 仓库与 Skill 命名 [Done]；DEC-003: Governance Skill 架构 [Done]；DEC-004: 历史来源处理 [Done]；DEC-005: SGE Skill 分层与未来发布边界 [Done] |
| BQ-K9 | Knowledge | Risks | 0 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A |  |
| BQ-K10 | Knowledge | Exceptions | 2 个当前工作树表面 | 提供全仓导航与质量审计入口 | N/A | EX-001: S-001 checkpoint bootstrap [Done]；EX-002: SP-001 strategy 扩展与 SP-002 规划 bootstrap [Done] |

### Assumptions
- `Coverage` 没有可靠量化依据，因此保持 `Unknown`。
- 历史 `Done` 只表示对应有界 Session 的旧终态，不自动覆盖后续新增 S-012。

### Unresolved Questions
- S-012 尚无 closeout/独立 Validation/post-closeout evidence 时，SP-001 不可声明完成。
- 是否公开发布属于未来 SP-002 和人类授权事项，本全景不作决定。

## 可见冲突

- `BI-001=Done` 与 `SP-001=Doing`、`S-012=Doing` 不一致。
- `archive_manifest.json` 仍含 `S-485`、Semx 绝对路径和旧计数，需以 registry check 结果判断漂移。

## Source Manifest

- Dashboard artifacts: 89
- Agent Logs: 4
- KB JSON: 6；KB reader Markdown: 2
- Skill/tool files: 17；tests: 2
- Git HEAD: `1001510992911d2018c6ee1384af88c8cfe8519f`；branch: `main`
- 详细路径、Stage Plan 字段、状态、source metadata 与冲突见同名 JSON 和 HTML 详情抽屉。
