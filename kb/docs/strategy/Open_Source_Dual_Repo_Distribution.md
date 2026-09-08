# Strategy Open-source Dual-repository Distribution

_Owner: sge-governance-skill | Version: v1.0 | Status: candidate | Updated: 2026-09-03_

## 双仓 Source-of-truth Contract

| 表面 | 角色 | 允许写入 | 不可推导 |
| --- | --- | --- | --- |
| 私有 sge-governance-skill | 唯一 canonical development source | 维护者在私有仓开发、审查、测试和保留执行证据 | 不能由公开仓反向自动成为真源 |
| 公开 bm-sge-governance | exact-allowlist deterministic public projection/distribution repo | 经授权的 projection commit、tag、release | 不能承载私有 Dashboard/Goal/Session 或独立产品真源 |
| target project | 用户自己的执行 overlay | 用户维护 AGENTS、Dashboard、Goal、Session、profile 与领域扩展 | 不能被公共 Skill 安装覆盖其 authority |

## Public Content Boundary

- [ ] 采用 default-deny exact allowlist；未知文件、符号链接、路径逃逸、绝对本机路径、凭据和私有身份残留 fail closed。
- [ ] 公开内容只包含通用 Skill、去项目化 KB/文档、示例、必要测试/工具、许可证与公共 metadata。
- [ ] Dashboard、Sessions、Stage Plans、Agent Logs、closeout、OPCM、历史 provenance、完整本地报告、dirty worktree 和私有 fixture 默认不公开。
- [ ] 任何例外必须逐文件记录 source、license、provenance、public decision、execution-context decision，并有 negative case。

## Deterministic Projection Pipeline

| 顺序 | 动作 | 权威与输出 |
| --- | --- | --- |
| 1 | 冻结 source revision、manifest revision 与 export tool revision | 私有仓库合同；生成可定位 projection identity |
| 2 | 从 fresh root 按 allowlist 导出并扫描 residue | 维护者 surface；未知文件与私有残留拒绝 |
| 3 | 比较 exact file set、bytes/digest 与 rendered outputs | deterministic evidence；不等于语义批准 |
| 4 | 由独立 Validation/UAT 重算并保留 candidate identity | Validation evidence；不等于发布授权 |
| 5 | 取得人类 GitHub push/tag/release authority 后更新公开仓并 read back | 外部 mutation；必须与 candidate、approved、published、production 状态分离 |

## Identity and Lifecycle

source_revision、manifest_revision、export_run_id、candidate_id、projection_commit、release_tag 是不同身份轴，任何一个都不能替代另一个。

终端用户默认从当前公开仓根目录安装，只需要 target；--source 如保留，只用于高级/测试或诊断，不是普通用户必须理解的 export 输入。

install record 必须记录 source identity、target、installed file set/digests、时间和备份 provenance；upgrade 先生成可恢复备份并保留 target project authority，失败时可回滚。

## Contribution and Permission Boundary

| 参与者 | 允许动作 | 禁止折叠 |
| --- | --- | --- |
| 外部贡献者 | 向公开仓提交 PR 作为候选输入 | PR merge 不等于 canonical truth 或 release approval |
| 维护者 | 审查/移植 PR 到私有 canonical source，重新 export、diff、Validation | 不能直接把公开仓独立修改反向当作真源 |
| 发布授权人 | 对具体 repo、commit/tree、tag、release payload 作出显式授权 | 候选通过不等于 GitHub 写入授权 |
| CI/自动化 | 默认只做 read/check/build candidate | 默认不持有 push/tag/release 权限 |

## Validation and Claim Ceiling

clean-room、维护者回归、终端用户 UAT、ERBE 与 independent Validation 必须覆盖双仓架构的正负例，包括未知文件、私有残留、source/target 混淆、错误 install record、升级备份失败、外部 PR 直写和权限越界。

本策略最多支撑有界架构规则与验证设计。它不支撑 public repo 已创建、已同步、已发布、普遍跨团队适用、生产就绪或任何 GitHub 远端状态声明。

## Source Scope

- `AGENTS.md`
- `Dashboard/Artifacts/Stage-Plan-SP-002/SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md`
- `Dashboard/Artifacts/Stage-Plan-SP-002/SP002_S011_FinalClosure_OPCM.md`
- `Dashboard/Artifacts/Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalContract_Base.json`
- `public_export_manifest_v1.json`
- `tools/sge_public.py`

## Related Docs

- `sge-strategy-kb-promotion-and-source-policy`
- `sge-strategy-human-ai-development`
