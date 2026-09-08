# SP-003 公开仓名称修订收束

## 关键结论中文展开

公开仓逻辑名称已从 `sge-governance` 统一修订为 `bm-sge-governance`。私有仓 `sge-governance-skill` 仍是唯一 canonical development source；公开仓仍只是 exact-allowlist、default-deny、deterministic 的单向 projection/distribution repo。

现在不需要先在 GitHub 创建空白公开仓。本次只修订本地 Goal、合同、KB 和 Dashboard 的名称身份，没有执行 GitHub 创建、push、tag、release 或 remote read-back。未来真正进入发布前预检时，仍需人类确认 owner、URL、default branch、逐文件再分发权、具体 source/tree/tag/payload 与写入权限。

## 落地范围

- 更新 [SP-003 Loop Goal](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_LoopGoal.md)、[Stage Plan](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_StagePlan.md)、[Goal Contract Base](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalContract_Base.json) 与解析后的 [Goal Contract](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalContract.json)。
- 重新绑定 [SP003-GP-001 Goal Patch](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalPatch.json)：基础合同 revision 为 `2`，`Scope Delta=none`，ODA-MH-01..12 与 Session DAG 不变。
- 更新 [BI-002、SP-003 与 Session registry](../../Big_Ideas.md)、[Current State](../../Current_State.md)、[Decision/Risk](../../Decisions.md)、[Artifacts Index](../../Artifacts_Index.md) 及双仓 [KB strategy](../../../kb/docs/strategy/Open_Source_Dual_Repo_Distribution.md)。

## 原始目标覆盖与边界

本次是名称身份修订，不是 SP-003 实现。原始 ODA-MH-01..12、维护者/终端用户表面、export→diff→validation→authorized update、版本/候选身份、install/upgrade provenance、外部 PR 回流、GitHub 权限、clean-room/UAT/独立 Validation 与最终 OPCM 仍全部保持待实现。现有 [Goal Design Closeout](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalDesign_Closeout.md) 与本文件共同提供设计阶段定位；本文件只证明名称修订已进入当前设计面。

## 运行与验证交接

已重新计算 Goal Contract Base digest，并对 Base、Goal Patch 和 resolved Goal 执行结构验证；Context Bootstrap、KB render、Dashboard registry、repository doctor、`git diff --check` 与本文件的 closeout-language gate 均已通过。`doctor` 发现并执行 21/21 测试，引用检查 1248 条，registry 为 22 条记录且无 identity collision。机器校验只证明结构、引用和派生面一致，不能证明语义实现、license 权利、远端仓库存在或发布成功。

本次没有独立 Builder、独立 Validation 或 Semantic Review verdict；它们仍是后续 S-016 及实现阶段的必需拓扑。不得把本次主线程检查写成 independent Validation passed，也不得把名称修订写成 SP-003 complete。

## KB 与 Dashboard 复核

- KB：公开仓名称是稳定双仓合同的一部分，已更新 canonical JSON 并重新生成 Markdown；`candidate`/`candidate_not_approved` 状态与权利、发布边界保持不变。
- Dashboard：当前 BI/SP/Session 状态继续为 `To do`；名称修订、下一步与外部授权边界已写入当前执行面。历史 SP-001/SP-002 归档不作为本次修改目标。
- Contract Delta Scan：名称身份更新归入当前双仓 KB 合同；实现、UAT、独立 Validation、发布和远端 read-back 仍归入 S-016..S-022 的 deferred session。

## 非目标与后续候选

不创建 GitHub `bm-sge-governance`，不执行任何远端写入，不实现 exporter/installer，不改变现有 `tools/sge_public.py`，不授予 license、GitHub 或 production authority。

下一候选仍是 `S-016`：冻结双仓合同、public content boundary、身份轴和负例；不得以本次名称修订绕过 pre-Builder Review、ERBE 或独立 Validation。

## 收束语言判定

`Closeout language verdict: pass`（通过）。本文件使用中文标题并对必要的英文状态、门禁和 claim ceiling 给出中文解释；该 verdict 只证明语言门通过，不证明 Goal 完成。
