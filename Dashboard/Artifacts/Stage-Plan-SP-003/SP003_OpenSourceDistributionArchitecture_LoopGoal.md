# SP-003 实现 Open-source Distribution Architecture Loop Goal

## Goal 身份与当前结论

- Goal ID：`SP-003`；类型：多 Session、连续执行的双仓公开分发架构 Goal。
- 当前状态：`To do`（待启动）。本文件与机器合同/Stage Plan 的落库只证明设计入口已建立，不证明实现、candidate、远端仓库或 release。
- 公开 GitHub repo 固定命名：`bm-sge-governance`；owner、URL、default branch、tag、release payload 和权限由后续人类 authority 在具体发布点确认。
- 唯一 canonical development source：私有 `sge-governance-skill`。
- 唯一允许的维护方向：`sge-governance-skill → fresh staging → bm-sge-governance`；禁止 public repo 与 private repo 双向并行编辑同一稳定内容。
- 机器可读合同：[Goal Contract](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalContract.json)；稳定策略：[Open-source Dual-repo Distribution KB](../../../kb/docs/strategy/Open_Source_Dual_Repo_Distribution.md)；实现阶梯：[Goal Patch](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalPatch.md)。

## 关键结论中文展开

本 Goal 解决的是“谁是真源、什么能公开、谁负责导出/发布、普通用户怎么安装升级、公开仓修改如何回流”的产品边界问题。维护者看到的是私有开发仓、allowlist、provenance、fresh-root export、diff、Validation 和 release authority；普通用户看到的是公开 `bm-sge-governance` 的 clone、以当前公开仓为默认 source 的 install/doctor/upgrade，以及自己的 target project overlay。普通用户不需要先 export 一个候选包，也不需要理解私有开发仓路径。

## 原始目标与 Must-have Ledger

完整 ODA-MH-01..12 见 [Stage Plan](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_StagePlan.md) 与 [Goal Contract](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalContract.json)。这些要求在设计时全部保留为 pending implementation，不得由单个 Session 或工具 PASS 关闭。

## 架构合同

### 双仓 source-of-truth

- 私有 `sge-governance-skill`：唯一 canonical development source，承载完整开发、治理、Dashboard、内部证据和待发布内容。
- 公开 `bm-sge-governance`：从冻结 source revision 按 exact allowlist 生成的单向 projection/distribution repo；公开仓不是第二编辑真源。
- target project：用户自己的执行 overlay；安装不得覆盖 target 的 AGENTS、Dashboard、Goal、Session、profile 或领域扩展 authority。

### Public content boundary

允许公开：逐文件裁决为 public distribution required 的通用 Skill、去项目化文档/KB、示例、必要 tests/tools、LICENSE/NOTICE 与公共 metadata。默认拒绝：Dashboard、Sessions、Stage Plans、Agent Logs、Goal/closeout/OPCM、内部 provenance、私有 fixture、完整本地报告、dirty worktree、绝对本机路径、credentials、symlink/gitlink/LFS/nested repo、未知文件和路径逃逸。任何例外必须逐文件记录 source/license/provenance/public decision/execution-context decision，并有 negative case。

### Maintainer 与 end-user surface

维护者路径：冻结 source/manifest/tool revision → fresh-root exact-allowlist export → residue scan → exact file-set/bytes/digest diff → independent Validation/UAT → 人类决定 → 授权后更新公开仓 → remote read-back。终端用户路径：`git clone` 公开 `bm-sge-governance` → `python3 tools/sge_public.py install --target <project>` → `doctor` → 后续 `upgrade --target <project>`；`--source` 若保留，只用于明确的高级/测试/诊断场景。

### Identity、upgrade 与贡献回流

`source_revision`、`manifest_revision`、`export_run_id`、`candidate_id`、`projection_commit`、`release_tag` 互不替代。install record 记录 source identity、target、安装文件集/digest、时间和 backup provenance；upgrade 先生成可恢复备份，失败可 rollback，且不夺取 target project authority。外部 PR 只是 public repo 输入，维护者审查后回流私有 canonical source，重新 export、diff、Validation，才可形成新的公开 projection。

### GitHub 权限与 release 边界

CI 默认只读/check/build candidate，不持有 push/tag/release 权限。GitHub repo 创建、push、tag、release 需要对具体 repository、commit/tree、tag、payload 作出人类授权；candidate/validated/approved/published/production-ready/Git mutation 不得合并成一个状态。license、copyright、NOTICE 与逐文件再分发权不能由测试通过、LICENSE 文件、GitHub 登录或 source digest 单独证明。

## 设计验收与实现序列

1. `S-016` 冻结双仓合同、内容边界、状态轴、身份轴和 ERBE 负例；这是 minimum safe slice。
2. `S-017` 建立维护者 deterministic projection；不得把 fresh staging 或 candidate 写成 public release。
3. `S-018` 建立普通用户生命周期；默认 source 是当前公开仓，target project authority 保持不变。
4. `S-019` 冻结版本、candidate、权限、license 和 release read-back 规则。
5. `S-020` 建立 external PR 单向回流与 provenance。
6. `S-021` 由 clean-room、UAT、ERBE、独立 Validation 和 Semantic Review 重算关键正负例。
7. `S-022` 用 OPCM、中文 closeout、final Validation 与 post-closeout reconciliation 判断是否达到 Goal completion rule。

每次 Session closeout 后必须记录 `goal_terminal`、`next_session`、`next_session_ready`、`human_decision_required`；Goal 未终止、下一 Session ready 且无需人类决定时，继续进入下一 Session。单个 Session `Done` 不得终止本 Loop Goal。

## 非目标、Scope Delta 与允许主张

- 本 Goal 不把现有 SP-002 candidate 改写为双仓已发布实现；SP-002 只作为边界输入。
- 不在本轮创建或修改 Skill，不创建 GitHub `bm-sge-governance`，不 push/tag/release，不写全局目录。
- 无 approved Scope Delta。删除、改名、延迟、权限变化、把 public repo 变为第二真源，均需新 Goal Patch、Scope Delta 与必要的人类批准。
- 在完整 completion rule 满足前，允许的当前主张只有“SP-003 设计与执行边界已落库”；不允许写 `SP-003 complete`、`published`、`production-ready` 或“公开仓已建立”。

## Completion Rule 与终止条件

只有 ODA-MH-01..12 逐项有 durable evidence，deterministic projection、end-user lifecycle、external PR return、permission/license boundary、clean-room/UAT、independent Validation、Semantic Review、中文 closeout、OPCM 和 post-closeout reconciliation 全部通过，且 candidate/release/GitHub/production 状态保持分离，才允许写 `SP-003 complete`。允许提前停止的条件只有用户明确暂停、需要人类作出未提供的外部/权利/破坏性决定、关键工具中断或同一恢复条件连续失败超过三次；普通未完成不是停止理由。

## Validation Handoff 与 truth placement

最终交接必须覆盖原始 ODA-MH-01..12、Stage Plan/Goal/Goal Patch、实际 changed files、Scope Delta、负例、candidate/release identity、UAT/ERBE/independent Validation、最终 diff、Dashboard/KB 状态和 closeout-language。Validation Handoff 只是输入，不是 Validation verdict。稳定双仓规则进入 `kb/data/` 并由 renderer 生成 `kb/docs/`；Session、blocker、candidate、decision、evidence 和 closeout 进入 `Dashboard/`。
