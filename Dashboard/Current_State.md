# Current Execution Surface

## SP-001 可复用 SGE Governance 迁移

- 当前判断：`S-001` 至 `S-006` 均已完成各自有界证据收束；SP-001 completion rule 已满足（含已批准 topology exception）。
- Stage Plan：`SP-001=Done`；`S-002=Done`、`S-003=Done`、`S-004=Done`、`S-005=Done`、`S-006=Done`。
- 已完成范围：Git seed、Final Goal、完整 Plan、S-001..S-006 Context/合同/验证/closeout；S-004 提前变更已在本 Session 重新建立证据后吸收，不回溯为早期 Session 证据。
- 权威入口：[SP-001 Final Loop Goal](Artifacts/SP001_SGEGovernanceMigration_LoopGoal.md)
- 实施边界：[SP-001 迁移计划](Artifacts/SP001_SGEGovernanceMigration_Plan.md)
- 关闭证据：[S-001 Closeout](Artifacts/S001_SGEGovernancePlanningLanding_Closeout.md) 与 [独立 Validation Review](Artifacts/S001_SGEGovernancePlanningLanding_ValidationReview.md)。
- 下一步：SP-002 仍为 `To do`，仅在用户明确启动后进入公共提取与新手可用性设计。

## SP-001 strategy 来源扩展

- 用户已批准把 semx-cli `semx-kb/docs/strategy/` 逐文件审计加入 SP-001；该扩展以 `MH-11` 和 [Goal Patch](Artifacts/SP001_StrategySourceExpansion_GoalPatch.md) 持久化。
- [Strategy Inventory](Artifacts/SP001_StrategySourceMigration_Inventory.md)已覆盖 56/56 个表面，但只是 S-002 输入，不是迁移批准或 KB truth。
- S-002 独立 Validation 已覆盖修复后合同、ERBE、closeout 与最终 diff；首轮 pre-Builder 时序作为已批准 exception/partial evidence 记录，不得被重新表述为已满足。

## SP-002 开源提取与新手可用性

- `SP-002` 已登记为 `To do`，依赖 `SP-001 complete`；当前入口 `S-007` 尚不可启动。
- 已规划 license/provenance、default-deny public export、中文 Beginner Guide、install/doctor/bootstrap、`run-sge-loop-goal-cycle` 通用化、独立 `user-acceptance-test` 与 release candidate closeout。
- 权威入口：[SP-002 Stage Plan](Artifacts/SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md)。本轮不创建、不发布或同步任何 Skill。
