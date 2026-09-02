# Current Execution Surface

## SGE Governance Skill 当前状态

- 当前判断：`SP-001` 已在 B-01..B-05、RB-01/RB-02 修复通过后重新执行受控状态收束；最终有界结论只由新的[关闭后独立对账](Artifacts/SP001_S015_PostCloseoutReconciliation.md)与 ERBE GREEN 共同支持。
- 当前仓库身份：`sge-governance-skill`；不包含任何具体产品设计或产品源代码。
- 权威入口：[SGE Governance Skill](../.codex/skills/sge-governed-checkpoints/SKILL.md)、[SGE profile](../kb/data/strategy/sge_project_profile_v1.json)。
- 执行记忆：[Dashboard README](README.md)；稳定治理 truth 位于 `kb/`。
- 下一步：SP-001 已达到 repo-local Goal terminal；SP-002 仍保持 `To do`，S-007 入口已具备但等待用户另行明确启动，不自动进入执行。

## 历史迁移 provenance（只读）

- 原 SP-001 strategy 来源审计和迁移记录保留在 Dashboard Artifacts，仅用于 provenance 和可恢复性，不是当前 Skill 配置。
- [Strategy Inventory](Artifacts/SP001_StrategySourceMigration_Inventory.md)已覆盖 56/56 个表面，但只是 S-002 输入，不是迁移批准或 KB truth。
- S-002 独立 Validation 已覆盖修复后合同、ERBE、closeout 与最终 diff；首轮 pre-Builder 时序作为已批准 exception/partial evidence 记录，不得被重新表述为已满足。

## SP-002 开源提取与新手可用性

- `SP-002` 已登记为 `To do`；SP-001 功能依赖已满足，但仍须用户另行明确启动，当前入口 `S-007` 没有自动进入 `Doing`。
- 已规划 license/provenance、default-deny public export、中文 Beginner Guide、install/doctor/bootstrap、`run-sge-loop-goal-cycle` 通用化、独立 `user-acceptance-test` 与 release candidate closeout。
- 权威入口：[SP-002 Loop Goal](Artifacts/SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md)、[Goal 设计收束](Artifacts/SP002_SGEOpenSourceNewcomerReadiness_GoalDesign_Closeout.md) 与 [SP-002 Stage Plan](Artifacts/SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md)。本轮只设计 Goal，不创建、不发布或同步任何 Skill。
