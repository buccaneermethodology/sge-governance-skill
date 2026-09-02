# Dashboard Artifacts Index


| Artifact | Role | 当前判断 |
| --- | --- | --- |
| [SP001_SGEGovernanceMigration_LoopGoal.md](Artifacts/SP001_SGEGovernanceMigration_LoopGoal.md) | SP-001 Final Loop Goal / durable execution contract | Final Goal 已落库；迁移尚未启动 |
| [SP001_SGEGovernanceMigration_Plan.md](Artifacts/SP001_SGEGovernanceMigration_Plan.md) | 经用户确认的完整迁移实施计划 | 作为 S-002..S-006 的范围、取舍与验收 authority |
| [SP001_SGEGovernanceMigration_ContextBootstrap.json](Artifacts/SP001_SGEGovernanceMigration_ContextBootstrap.json) | S-001 implementation profile 启动包 | 保留 Raw User Intent authority、边界、Read Set、影响面和 topology |
| [S001_SGEGovernancePlanningLanding_Closeout.md](Artifacts/S001_SGEGovernancePlanningLanding_Closeout.md) | S-001 中文 closeout | 只关闭规划落库；明确不关闭 SP-001，不证明治理迁移或产品实现 |
| [S001_SGEGovernancePlanningLanding_ValidationReview.md](Artifacts/S001_SGEGovernancePlanningLanding_ValidationReview.md) | S-001 独立 Validation Review | 首轮 fail 后修复；delta verdict 为 `pass-with-findings`，中文含义是允许 S-001 状态收束但仍需关闭后独立对账 |
| [S001_SGEGovernancePlanningLanding_PostCloseoutReconciliation.md](Artifacts/S001_SGEGovernancePlanningLanding_PostCloseoutReconciliation.md) | S-001 关闭后独立对账 | 最终关闭 verdict authority；其正文必须覆盖实际 closeout、Dashboard/KB 状态和完整 diff，不能由本索引代替 |
| [SP001_StrategySourceMigration_Inventory.md](Artifacts/SP001_StrategySourceMigration_Inventory.md) | SP-001 strategy 56 文件逐项初筛 | S-002 provenance/canonical mapping 输入；不是迁移批准或 canonical truth |
| [SP001_StrategySourceMigration_Ledger.json](Artifacts/SP001_StrategySourceMigration_Ledger.json) | 56 文件 typed decision ledger | Dashboard execution memory；逐文件字段与 mapping policy 分层 |
| [SP001_S002_SGECore_ContractPatch.md](Artifacts/SP001_S002_SGECore_ContractPatch.md) | S-002 合同边界修复记录 | 记录 truth placement、identity scope、adapter 与 write exclusions 修复 |
| [SP001_SGEGovernanceSkill_ProvenanceInventory.json](Artifacts/SP001_SGEGovernanceSkill_ProvenanceInventory.json) | copied Skill source/target file provenance | 逐文件路径、字节数与 SHA-256；不等于公共发布批准 |
| [SP001_S002_TopologyException_Request.md](Artifacts/SP001_S002_TopologyException_Request.md) | S-002 拓扑例外请求 | 已获有界批准；不支持追溯性恢复 pre-Builder 时序 |
| [SP001_S002_SGECore_Closeout.md](Artifacts/SP001_S002_SGECore_Closeout.md) | S-002 阶段性收束草案 | 等待独立 Validation 覆盖后，才可按批准例外关闭 S-002 |
| [SP001_StrategySourceExpansion_GoalPatch.md](Artifacts/SP001_StrategySourceExpansion_GoalPatch.md) | 经用户批准的 SP-001 Scope Expansion | 新增 MH-11 并把 strategy 审计分配到 S-002..S-006；不启动迁移 |
| [SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md](Artifacts/SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md) | SP-002 durable tracking contract | 规划未来 public candidate 与 newcomer readiness；依赖 SP-001 complete，当前未启动 |
| [SP002_SGEOpenSourceNewcomerReadiness_ContextBootstrap.json](Artifacts/SP002_SGEOpenSourceNewcomerReadiness_ContextBootstrap.json) | 本轮 implementation Context Bootstrap | 保留用户原文、56-file 边界、禁止复制/发布和 final Validation surfaces |
| [SP002_PlanningAndSP001StrategyExpansion_Closeout.md](Artifacts/SP002_PlanningAndSP001StrategyExpansion_Closeout.md) | 本轮中文 closeout | 只关闭规划/来源裁决落库；不关闭 SP-001 或 SP-002 |
| [SP002_PlanningAndSP001StrategyExpansion_ValidationReview.md](Artifacts/SP002_PlanningAndSP001StrategyExpansion_ValidationReview.md) | 本轮独立 full-baseline + delta Validation | 保留首轮 blocked 与修复后 pass；最终 Dashboard/closeout 状态仍由 post-closeout reconciliation 覆盖 |
| [SP002_PlanningAndSP001StrategyExpansion_PostCloseoutReconciliation.md](Artifacts/SP002_PlanningAndSP001StrategyExpansion_PostCloseoutReconciliation.md) | 本轮 final-state 独立对账 | 唯一最终状态 verdict；覆盖实际 closeout、EX-002=Done、Dashboard/KB 和最终 diff |
| [SP002_PlanningAndSP001StrategyExpansion_ValidationLaneTaskCard.json](Artifacts/SP002_PlanningAndSP001StrategyExpansion_ValidationLaneTaskCard.json) | 首轮 full-baseline Validation lane card | Digest-bound 输入；首轮 verdict 为 blocked，不能冒充 final pass |
| [SP002_PlanningAndSP001StrategyExpansion_DeltaValidationLaneTaskCard.json](Artifacts/SP002_PlanningAndSP001StrategyExpansion_DeltaValidationLaneTaskCard.json) | B-01..B-03 修复后的 delta Validation card | 绑定首轮 blocked Review 与修复后文件摘要；只验证 delta 与 final diff |
| [SP002_PlanningAndSP001StrategyExpansion_PostCloseoutValidationLaneTaskCard.json](Artifacts/SP002_PlanningAndSP001StrategyExpansion_PostCloseoutValidationLaneTaskCard.json) | final-state post-closeout lane card | 绑定 EX-002=Done、实际 closeout/Review 与最终 Dashboard；输出唯一 final-state verdict |
| [SP001_S003_GovernanceTooling_ContextBootstrap.json](Artifacts/SP001_S003_GovernanceTooling_ContextBootstrap.json) | S-003 Context Bootstrap | S-003 tooling 迁移的独立启动包 |
| [SP001_S003_GovernanceTooling_LaneTaskCard.json](Artifacts/SP001_S003_GovernanceTooling_LaneTaskCard.json) | S-003 full-baseline lane card | digest-bound tooling write scope |
| [SP001_S003_GovernanceTooling_Closeout.md](Artifacts/SP001_S003_GovernanceTooling_Closeout.md) | S-003 中文 closeout | 仅关闭治理 tooling 技术切片 |
| [SP001_S003_GovernanceTooling_PostCloseoutReconciliation.md](Artifacts/SP001_S003_GovernanceTooling_PostCloseoutReconciliation.md) | S-003 事后对账 | 独立最终状态核对 |
| [SP001_S004_SemanticCleanup_ContextBootstrap.json](Artifacts/SP001_S004_SemanticCleanup_ContextBootstrap.json) | S-004 Context Bootstrap | 语义清理独立启动包 |
| [SP001_S004_SemanticCleanup_LaneTaskCard.json](Artifacts/SP001_S004_SemanticCleanup_LaneTaskCard.json) | S-004 lane card | 清理与替代机制 write scope |
| [SP001_S004_SemanticCleanup_ValidationReview.md](Artifacts/SP001_S004_SemanticCleanup_ValidationReview.md) | S-004 独立 Validation | 身份、真源路由与历史清理验收 |
| [SP001_S004_SemanticCleanup_Closeout.md](Artifacts/SP001_S004_SemanticCleanup_Closeout.md) | S-004 中文 closeout | 提前删除在本 Session 吸收，不回溯为 S-002/S-003 证据 |
| [SP001_S005_IntegrationValidation_ContextBootstrap.json](Artifacts/SP001_S005_IntegrationValidation_ContextBootstrap.json) | S-005 Validation Context | 最终候选集成验收启动包 |
| [SP001_S005_IntegrationValidation_LaneTaskCard.json](Artifacts/SP001_S005_IntegrationValidation_LaneTaskCard.json) | S-005 validation lane card | MH-01..MH-11 full-baseline 读取面 |
| [SP001_S005_IntegrationValidation_ValidationReview.md](Artifacts/SP001_S005_IntegrationValidation_ValidationReview.md) | S-005 独立 Validation | 最终候选 evidence completeness matrix |
| [SP001_S005_IntegrationValidation_SemanticReview.md](Artifacts/SP001_S005_IntegrationValidation_SemanticReview.md) | S-005 Semantic Review | 边界与实现入口复核 |
| [SP001_S006_GoalClosure_ContextBootstrap.json](Artifacts/SP001_S006_GoalClosure_ContextBootstrap.json) | S-006 closeout Context | 最终 Goal 收束启动包 |
| [SP001_S006_GoalClosure_LaneTaskCard.json](Artifacts/SP001_S006_GoalClosure_LaneTaskCard.json) | S-006 closure lane card | OPCM、Scope Delta 与对账 write scope |
| [SP001_S006_GoalClosure_OPCM.md](Artifacts/SP001_S006_GoalClosure_OPCM.md) | SP-001 OPCM/Scope Delta | MH-01..MH-11 逐项覆盖与唯一例外 |
| [SP001_S006_GoalClosure_Closeout.md](Artifacts/SP001_S006_GoalClosure_Closeout.md) | SP-001 最终中文 closeout | 允许的 repo-local SGE 有界完成主张 |
| [SP001_S006_GoalClosure_PostCloseoutReconciliation.md](Artifacts/SP001_S006_GoalClosure_PostCloseoutReconciliation.md) | SP-001 最终事后对账 | 唯一最终状态 verdict |
| [SGEGovernanceRepositoryExtraction_Closeout.md](Artifacts/SGEGovernanceRepositoryExtraction_Closeout.md) | SGE Governance 专用仓库整理收束 | 删除 audio-transcriptor 产品源文件，保留通用 Skill；quick_validate 因缺少 PyYAML 待补跑 |
