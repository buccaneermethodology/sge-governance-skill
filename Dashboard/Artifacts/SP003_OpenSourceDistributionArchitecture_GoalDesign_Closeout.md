# SP-003 Goal 设计落库收束

## 关键结论中文展开

本轮已设计并落库新的 `SP-003 实现 Open-source Distribution Architecture` Goal、BI-002、Stage Plan 与 S-016..S-022。当前只完成“设计和执行边界落库”：SP-003、所有新 Session 均保持 `To do`（待启动），没有实现 exporter/installer，没有创建 `bm-sge-governance` GitHub 仓库，也没有执行 push、tag、release。

核心架构已经明确：私有 `sge-governance-skill` 是唯一 canonical development source；公开 `bm-sge-governance` 只能由 exact-allowlist、default-deny、deterministic projection 产生；公开仓外部 PR 必须回流私有真源后再重新导出和验证；普通用户直接从公开仓 clone/install/upgrade，`--source` 只保留为高级/测试入口。

## 落地范围

- 新增 [BI-002](../Big_Ideas.md)、[SP-003](../Stage_Plans.md) 与 `S-016..S-022`。
- 新增 [SP-003 Stage Plan](SP003_OpenSourceDistributionArchitecture_StagePlan.md)、[Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md)、[Goal Patch](SP003_OpenSourceDistributionArchitecture_GoalPatch.md) 和机器 [Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json)。
- 新增 [Context Bootstrap](SP003_OpenSourceDistributionArchitecture_GoalContextBootstrap.json)，保留用户原始目标、Required Read Set、Conditional Read Set、语义刷新、影响面和本轮不执行远端动作的边界。
- 新增 [canonical dual-repo strategy JSON](../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)，并由 renderer 生成对应阅读面。
- 更新 Dashboard 的 Big Ideas、Stage Plans、Sessions、Current State、Decisions、Risks 与 Artifacts Index；Session Index/archive manifest 由 registry projection 生成。

## 原始目标覆盖矩阵

| 原始要求 | 可观察验收判定 | 精确证据 | 实际结果 | 状态 | 阻断/例外 | Owner/时序 | Claim ceiling | Parent/Closeout 吸收 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 私有仓是唯一 canonical source | Goal/KB 明确单向 source-of-truth，禁止双向真源 | [Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md)、[KB strategy](../../kb/docs/strategy/Open_Source_Dual_Repo_Distribution.md) | 已写入设计合同 | 设计覆盖；实现待启动 | 无 | S-016→S-017 | 设计层，不证明同步实现 | 本 closeout/SP-003 |
| 公开仓固定命名为 bm-sge-governance | Goal、Stage Plan、KB machine contract 使用同一逻辑名称 | [Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json) | 名称已冻结；owner/URL/default branch 未确认 | 设计覆盖 | 后续需人类确认远端身份 | S-019 | 不证明 GitHub 仓存在 | 本 closeout/SP-003 |
| public content boundary | exact allowlist、default-deny、private residue 排除面及 negative cases 被列出 | [Stage Plan](SP003_OpenSourceDistributionArchitecture_StagePlan.md)、[KB strategy](../../kb/docs/strategy/Open_Source_Dual_Repo_Distribution.md) | 已冻结设计；未实现扫描器 | 设计覆盖；实现待启动 | 无 | S-016/S-017 | 不证明当前工作树已可公开 | 本 closeout/SP-003 |
| deterministic export→diff→validation→public update | 五步 pipeline 有 authority、输入输出和写入边界 | [Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md) | 已冻结设计；未执行 pipeline | 设计覆盖；实现待启动 | GitHub update 需外部授权 | S-017/S-019/S-022 | 不证明 candidate/release | 本 closeout/SP-003 |
| version/revision/candidate identity | source、manifest、candidate、projection commit、tag/release 独立建模 | [Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json) | 已列出 identity axes | 设计覆盖；实现待启动 | 无 | S-016/S-019 | 不证明任何版本发布 | 本 closeout/SP-003 |
| end-user clone/install/upgrade | 默认公开仓 source、只需 target、--source 高级/测试；备份与 install record 有合同 | [Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md) | 已冻结用户路径；未实现/重放 | 设计覆盖；实现待启动 | 无 | S-018 | 不证明普通用户可用 | 本 closeout/SP-003 |
| external PR 回流 canonical | public PR 只作输入，回流 private source 后重新 export/validation | [KB strategy](../../kb/docs/strategy/Open_Source_Dual_Repo_Distribution.md) | 已冻结回流规则；未实现 | 设计覆盖；实现待启动 | 无 | S-020 | 不证明贡献流程已运行 | 本 closeout/SP-003 |
| GitHub permission/release boundary | push/tag/release、CI 与人类授权分离 | [Stage Plan](SP003_OpenSourceDistributionArchitecture_StagePlan.md) | 已冻结权限边界；未执行外部动作 | 设计覆盖 | 本轮明确禁止外部 mutation | S-019 | 不证明远端权限或 release | 本 closeout/SP-003 |
| clean-room/UAT/independent validation | 正负例、UAT、ERBE、独立 Validation 和 Semantic Review 被纳入 DAG | [Stage Plan](SP003_OpenSourceDistributionArchitecture_StagePlan.md) | 已建立验证计划；未运行 | 设计覆盖；验证待启动 | 无 | S-021 | 不证明验证通过 | 本 closeout/SP-003 |
| candidate/release/production 分离 | 状态轴与 forbidden claims 明确 | [Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md)、[Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json) | 已冻结边界 | 设计覆盖 | 无 | 全阶段 | 设计层，不证明状态事实 | 本 closeout/SP-003 |
| final coverage/closeout/reconciliation | S-022 明确 OPCM、中文 closeout、final Validation 与 post-closeout | [Stage Plan](SP003_OpenSourceDistributionArchitecture_StagePlan.md) | 已建立终态合同；未执行 | 设计覆盖；实现待启动 | Goal 不得因计划落库而关闭 | S-022 | 不证明 Goal complete | 本 closeout/SP-003 |

## 范围变更复核

- Goal Conformance：原始用户要求全部保留；没有删除、替换、降级、延期或把实现要求改写成 non-goal。
- Scope Delta：`none`。`SP003-GP-001` 仅把 Stage Plan 解析为实现阶梯，不改变 must-have、authority 或 completion rule。
- 与 SP-002 的关系：SP-002 的 candidate、UAT、Validation 与 release boundary 作为输入复用；不把 SP-002 历史证据倒推为 SP-003 证据。

## Lane 启动与例外

- 本轮是新 Goal/Stage Plan/Session 的设计落库，不执行 Builder；因此没有启动实现 Builder lane。
- 本轮没有 Builder lane，因为用户只要求设计和落库；已尝试启动只读独立 Validation 与 Semantic Review lane，但两者均因执行流断开而 `errored`，没有产生可采纳 verdict。记录有界 `Single-Agent Exception`：补偿措施为完整 Required Read Set、参考策略比对、Goal Contract/Goal Patch 机器校验、Context Bootstrap、SGC/Goal Conformance/Goal Agent checklist、KB renderer、repository doctor、registry 与 closeout-language gates。该例外不支撑实现完成或 Goal complete。
- 后续 S-016 启动时必须按 Multi-Agent Gate 重新评估并提供独立 Design、Builder、Validation、Closure；高语义边界变化必须触发 Semantic Review。

## 设计交接

S-016 的 minimum safe slice 是冻结双仓 source-of-truth、public content boundary、maintainer/end-user surface、identity axes 与 negative cases；不得从创建 GitHub 仓或直接导出当前工作树开始。后续 Session 只接受完整 [Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md)、机器 [Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json) 和 [Goal Patch](SP003_OpenSourceDistributionArchitecture_GoalPatch.json) 的确定性结果。

## 验证交接包

- Original objective coverage：见上方逐项矩阵；ODA-MH-01..12 均为设计覆盖、实现 pending。
- Scope Delta：`none`；任何改变 public repo identity、authority、release 或完成规则的变更必须新建 Goal Patch 并请求人类批准。
- Changed files：BI/SP/Session registry、SP-003 artifacts、KB strategy JSON/Markdown、render manifest。
- Required gates：Context Bootstrap、Goal Contract、Goal Patch、SGC、Goal Conformance、registry/reconcile/validate、KB render、链接、closeout-language、最终 diff。
- Evidence ceiling：只证明设计合同与执行入口已落库；不证明实现、候选、远端仓、发布、生产或权利确认。
- KB/Dashboard impact：稳定双仓规则进入 KB；状态与证据进入 Dashboard；不改 SP-002 历史归档。
- Closeout language verdict：`pass`（通过）；命令输出为 `Closeout language check passed`。这只证明本 closeout 的标题/状态解释满足语言门，不证明 Goal 完成。

## 验证结论

本轮不是实现 closeout。只有在上述设计文件、registry projection、KB render 和 closeout-language 通过后，才可声明“Goal 设计已落库”；不能声明 `SP-003 complete`、`bm-sge-governance published` 或 GitHub mutation 完成。

## 明确非目标

不创建 GitHub 仓库，不 push/tag/release，不修改全局 Skill，不实现 exporter/installer，不运行 clean-room/UAT，不做远端 read-back，不授予 license、GitHub 或 production authority。

## 运行的门禁与语义复核

必须运行：Goal Contract/Goal Patch、Context Bootstrap、SGC、Goal Conformance、Goal Agent、registry `reconcile --check`/`validate`、必要时 `reconcile --apply` 后重跑、KB renderer `--check`、链接检查、`git diff --check` 与 closeout-language。由于本轮改变稳定双仓策略与 authority boundary，后续实现前必须有 Semantic Reviewer 的 `Design Freeze Validity` 与 `Implementation Entry Readiness` 双 verdict。

## 延后范围

S-016..S-022 的实现、验证与最终 closeout全部延后到 SP-003 启动；GitHub repo 创建、push/tag/release 永远是单独人类授权面，不因 SP-003 candidate 或 Goal complete 自动获得授权。

## KB/Dashboard 复核

- KB：已新增候选 canonical strategy JSON，并更新 render manifest；Markdown 由 renderer 生成。其 status 保持 `candidate`/`candidate_not_approved`，不作为发布批准。
- Dashboard：已新增 BI-002/SP-003/S-016..S-022 与 Current State、Decision、Risk、Artifacts 索引；Session registry projection 由工具重建。
- Contract Delta Scan：双仓稳定规则分类为 `promote-to-KB`；当前实现细节、UAT、release evidence 分类为 `deferred session`；执行状态分类为 `Dashboard-only`。

## 后续候选

- `S-016`（P0）：先冻结双仓合同、allowlist 和负例；它是后续所有 exporter/lifecycle/release 工作的 authority 基础，因此优先于直接改工具或创建远端仓库。
- `S-017`（P0，依赖 S-016）：建立维护者 deterministic projection，先解决“可重算且不泄露”再谈公开仓更新。
- `S-018`（P0，依赖 S-017）：建立普通用户 clone/install/upgrade 路径，消除用户承担 export 认知的风险。

## 收束语言判定

本文件的 `Closeout language verdict` 已由 `guardrail_checklist.py --mode closeout-language` 确认通过；当前文档不作 Goal complete、published 或 production-ready 声明。
