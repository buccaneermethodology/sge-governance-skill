# Current Execution Surface

## SGE Governance Skill 当前状态

- 当前判断：通用 `sge-governed-checkpoints` Skill 已完成 repo-local 有界验收；原 audio-transcriptor 迁移记录仅作为历史 provenance。
- 当前仓库身份：`sge-governance-skill`；不包含任何具体产品设计或产品源代码。
- 权威入口：[SGE Governance Skill](../.codex/skills/sge-governed-checkpoints/SKILL.md)、[SGE profile](../kb/data/strategy/sge_project_profile_v1.json)。
- 执行记忆：[Dashboard README](README.md)；稳定治理 truth 位于 `kb/`。
- 下一步：公共提取、新手指南和发布候选仍需另行启动与验证，不在本次变更内。

## 历史迁移 provenance（只读）

- 原 SP-001 strategy 来源审计和迁移记录保留在 Dashboard Artifacts，仅用于 provenance 和可恢复性，不是当前 Skill 配置。
- [Strategy Inventory](Artifacts/SP001_StrategySourceMigration_Inventory.md)已覆盖 56/56 个表面，但只是 S-002 输入，不是迁移批准或 KB truth。
- S-002 独立 Validation 已覆盖修复后合同、ERBE、closeout 与最终 diff；首轮 pre-Builder 时序作为已批准 exception/partial evidence 记录，不得被重新表述为已满足。

## SP-002 开源提取与新手可用性

- `SP-002` 已登记为 `To do`，依赖 `SP-001 complete`；当前入口 `S-007` 尚不可启动。
- 已规划 license/provenance、default-deny public export、中文 Beginner Guide、install/doctor/bootstrap、`run-sge-loop-goal-cycle` 通用化、独立 `user-acceptance-test` 与 release candidate closeout。
- 权威入口：[SP-002 Stage Plan](Artifacts/SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md)。本轮不创建、不发布或同步任何 Skill。
