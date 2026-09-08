# Current Execution Surface

## SGE Governance Skill 当前状态

- 当前判断：`SP-001` 已在 B-01..B-05、RB-01/RB-02 修复通过后重新执行受控状态收束；最终有界结论只由新的[关闭后独立对账](Artifacts/Stage-Plan-SP-001/SP001_S015_PostCloseoutReconciliation.md)与 ERBE GREEN 共同支持。
- 当前仓库身份：`sge-governance-skill`；不包含任何具体产品设计或产品源代码。
- 权威入口：[SGE Governance Skill](../.codex/skills/sge-governed-checkpoints/SKILL.md)、[SGE profile](../kb/data/strategy/sge_project_profile_v1.json)。
- 执行记忆：[Dashboard README](README.md)；稳定治理 truth 位于 `kb/`。
- 下一步：SP-001 与 SP-002 均达到各自 repo-local Goal terminal；SP-002 仅在声明范围内支持有界 public candidate，实际 release、push、tag、production 与全局写入仍未授权。

## 历史迁移 provenance（只读）

- 原 SP-001 strategy 来源审计和迁移记录保留在 Dashboard Artifacts，仅用于 provenance 和可恢复性，不是当前 Skill 配置。
- [Strategy Inventory](Artifacts/Stage-Plan-SP-001/SP001_StrategySourceMigration_Inventory.md)已覆盖 56/56 个表面，但只是 S-002 输入，不是迁移批准或 KB truth。
- S-002 独立 Validation 已覆盖修复后合同、ERBE、closeout 与最终 diff；首轮 pre-Builder 时序作为已批准 exception/partial evidence 记录，不得被重新表述为已满足。

## SP-002 开源提取与新手可用性

<<<<<<< HEAD
- `SP-002` 当前技术状态为 `candidate_goal_terminal_with_approved_proc01_exception`；批准前 blocked verdict、批准后 Final Validation 与批准后 post-closeout reconciliation 均保留，最终状态已由最新对账吸收。
- 已落地 license/provenance、default-deny public export、中文 Beginner Guide、install/doctor/bootstrap/upgrade/recoverable uninstall、profile/hooks 编排候选与 optional extension contract；仍不得解释为发布或生产就绪。
- 权威入口：[SP-002 Loop Goal](Artifacts/Stage-Plan-SP-002/SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md)、[Execution Context](Artifacts/Stage-Plan-SP-002/SP002_Execution_ContextBootstrap.json)、[S-010 UAT](Artifacts/Stage-Plan-SP-002/SP002_S010_NewcomerUAT.md)、[Semantic Review](Artifacts/Stage-Plan-SP-002/SP002_S011_SemanticReview.md) 与 [SP-002 Stage Plan](Artifacts/Stage-Plan-SP-002/SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md)。

## SP-003 Open-source Distribution Architecture

- `BI-002` 与 `SP-003` 已在声明的本地/合同范围内 `Done`（有界完成）；S-022 的 Final Validation 与 post-closeout reconciliation 均为 `pass_with_bounds`，MH-08 policy/provenance 和 MH-09 权限合同按本地架构要求落地。不能由本地 evidence 推导公开仓、发布或生产就绪。
- 稳定架构合同已进入 [KB strategy](../kb/docs/strategy/Open_Source_Dual_Repo_Distribution.md)：私有 `sge-governance-skill` 是唯一 canonical development source，公开 `bm-sge-governance` 是 exact-allowlist deterministic one-way projection/distribution repo，禁止双向真源。
- Maintainer surface 包含 allowlist/provenance、fresh-root export、diff、Validation 与 release authority；end-user surface 默认是公开仓 clone 后只带 target 的 install/upgrade，`--source` 仅高级/测试参数。
- SP-003 当前已完成 S-016..S-022 的有界本地实现/合同与 evidence；S-016 的 `blocked`/`partial` 历史 verdict 保留，S-017 独立 Validation 为 `pass-with-findings`，S-021 独立 Validation 为 `pass-with-findings`（7 案为 structural_recompute，非 runtime witness），S-021 Semantic 为 `partial/conditional`。S-022 已由 Final Validation 与独立 post-closeout reconciliation 在声明范围内共同收束，`goal_terminal=true`。公开仓名称已修订为 `bm-sge-governance`，详见[名称修订收束](Artifacts/Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_NameRevision_Closeout.md)。不证明公开 GitHub 仓库、push、tag、release、逐文件权利批准或 production readiness；外部动作仍需具体人类授权。

## SP-004 Semx 残留与开源缺口闭环

- SP-004 已在用户批准的 Scope Delta 与例外范围内 `Done（pass_with_bounds）`。S-026 完整 newcomer flow 暂时记为 `not_applicable`，历史 task/UAT partial 保留；S-023 以 [Final Review](Artifacts/Stage-Plan-SP-004/SP004_S023_FinalReview.md) 登记有界通过。README 已修复，v1.0.2 48-file exact candidate、CI、Release 与 remote read-back 见 [v1.0.2 read-back](Artifacts/Stage-Plan-SP-004/SP004_S029_v1.0.2_RemoteReadback.json)。最终收束见 [S-029 Final Closeout](Artifacts/Stage-Plan-SP-004/SP004_S029_FinalCloseout.md) 与 [post-closeout reconciliation](Artifacts/Stage-Plan-SP-004/SP004_S029_PostCloseoutReconciliation_v2.md)。
- 当前 Git branch 仍为 `sge/sp002`，新分支创建因 `.git` 写权限失败；这是 Git provenance/最终 handoff 风险，不是授权远端发布。
- S-028 的 CI workflow 修订、v1.0.1 exact payload 与远端 read-back，及后续 v1.0.2 README 修订 payload 均按人类授权完成。SP-004 当前 `goal_terminal=true`，但 claim ceiling 仍是批准例外下的 `pass_with_bounds`；不表示完整 newcomer readiness、无条件独立 Validation 或 production readiness。
=======
- `SP-002` 已登记为 `To do`；SP-001 功能依赖已满足，但仍须用户另行明确启动，当前入口 `S-007` 没有自动进入 `Doing`。
- 已规划 license/provenance、default-deny public export、中文 Beginner Guide、install/doctor/bootstrap、`run-sge-loop-goal-cycle` 通用化、独立 `user-acceptance-test` 与 release candidate closeout。
- 权威入口：[SP-002 Stage Plan](Artifacts/Stage-Plan-SP-002/SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md)。本轮不创建、不发布或同步任何 Skill。
>>>>>>> codex/sp001-quality-recovery
