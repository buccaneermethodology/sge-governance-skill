# SP-001 Artifact 批次

## Owner 与范围

- Owner：`SP-001`，对应 [Stage Plan](../../Stage_Plans.md)。
- Scope：SGE Governance Skill 历史迁移、质量恢复、S-001～S-006 与 S-012～S-015 的 Goal、设计、合同、lane、Validation、Semantic Review、closeout、对账及历史 provenance。
- Non-goal：本批次不改变 `SP-001` 的生命周期状态，不把历史 evidence、registry/test 通过或 artifact 整理解释为产品、公共发布或生产完成。

## Provenance

文件从旧的 `Dashboard/Artifacts/` 直放位置迁入本批次；内容语义不因归档而提升。仓库内引用、lane card 的机器路径和 Markdown 相对链接已按新位置更新；SHA-256 字段仍只在其所属证据语境中有效，不能由路径整理重新获得验证权威。

## Artifact 索引

- Goal 与计划：[Final Loop Goal](SP001_SGEGovernanceMigration_LoopGoal.md)、[迁移计划](SP001_SGEGovernanceMigration_Plan.md)、[Strategy Expansion Goal Patch](SP001_StrategySourceExpansion_GoalPatch.md)。
- 质量恢复合同与设计：[Quality Recovery Design](SP001_QualityRecovery_Design.md)、[ERBE Contract](SP001_QualityRecovery_ERBE_Contract.json)、[ERBE Cases](SP001_QualityRecovery_ERBE_Cases.json)、[Context Bootstrap](SP001_QualityRecovery_ContextBootstrap.json)。
- S-001 规划落库：所有 `S001_SGEGovernancePlanningLanding_*` 文件，包括 closeout、Validation、lane cards/prompts 与 post-closeout reconciliation。
- S-002～S-006：对应 `SP001_S002_*`、`SP001_S003_*`、`SP001_S004_*`、`SP001_S005_*`、`SP001_S006_*` 文件。
- S-012～S-015：对应 `SP001_S012_*`、`SP001_S013_*`、`SP001_S014_*`、`SP001_S015_*` 文件；最终入口为 [S-015 Final Closure](SP001_S015_FinalClosure_Closeout.md)、[OPCM](SP001_S015_FinalClosure_OPCM.md) 与 [Post-closeout Reconciliation](SP001_S015_PostCloseoutReconciliation.md)。
- 其他历史 provenance：[仓库整理收束](SGEGovernanceRepositoryExtraction_Closeout.md)、[Strategy Inventory](SP001_StrategySourceMigration_Inventory.md)、[Strategy Ledger](SP001_StrategySourceMigration_Ledger.json)、[Skill Provenance Inventory](SP001_SGEGovernanceSkill_ProvenanceInventory.json)、[Tombstones](Tombstones/)。
