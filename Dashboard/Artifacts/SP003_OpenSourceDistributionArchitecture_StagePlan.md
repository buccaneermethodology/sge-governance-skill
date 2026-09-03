# SP-003 实现 Open-source Distribution Architecture Stage Plan

## 当前状态

- Status：`To do`（待启动）；本轮只落库设计，不表示实现、candidate、公开仓或 release 已存在。
- Parent Big Idea：[BI-002](../Big_Ideas.md)；与已收束的 SP-002 并列，SP-002 的候选证据不被改写为本阶段实现证据。
- 公开仓逻辑名称：`bm-sge-governance`；owner、URL、default branch、GitHub 权限和 release 具体身份均需在后续授权点由人类确认。
- 私有 canonical source：`sge-governance-skill`；公开仓只能由其 exact-allowlist projection 生成，禁止双向真源。
- 正式 Goal：[SP-003 Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md)；机器合同：[Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json)。

## 目标

把当前私有 `sge-governance-skill` 建立为唯一 canonical development source，把公开 `bm-sge-governance` 建立为可重算、可审计、exact-allowlist、default-deny 的单向 public projection/distribution repo；同时把维护者的 export/review/release surface 与普通用户 clone/install/upgrade surface 分离。

## Must-have Ledger

| ID | Must-have | 可观察验收 | 设计入口 | 实现状态 |
| --- | --- | --- | --- | --- |
| ODA-MH-01 | 双仓 source-of-truth contract | 明确 private canonical → public projection 单向关系与禁止双向编辑 | S-016 | 待实现 |
| ODA-MH-02 | public content boundary | exact allowlist、default-deny、private residue/unknown/absolute path/symlink 等 fail closed | S-016/S-017 | 待实现 |
| ODA-MH-03 | deterministic projection pipeline | export→diff→validation→authorized public update 每步可重算、可追溯 | S-016/S-017 | 待实现 |
| ODA-MH-04 | version/revision/candidate identity | source、manifest、candidate、projection commit、tag/release 互不替代 | S-016/S-019 | 待实现 |
| ODA-MH-05 | end-user clone/install path | clone `bm-sge-governance` 后默认 current public source，只需 target；`--source` 仅高级/测试 | S-018 | 待实现 |
| ODA-MH-06 | upgrade/backup/install provenance | install record、backup、rollback、target authority 保留可重算 | S-018 | 待实现 |
| ODA-MH-07 | maintainer/end-user separation | 普通用户不需要 export/allowlist/release 内部 surface | S-016/S-018 | 待实现 |
| ODA-MH-08 | external PR return flow | public PR 先回流 private canonical，再重新 export/validation | S-020 | 待实现 |
| ODA-MH-09 | GitHub permission boundary | push/tag/release 明确权限，CI 默认无发布权，逐次人类授权 | S-019 | 待实现 |
| ODA-MH-10 | clean-room/UAT/independent validation | maintainer、end-user、负例和回流路径均由独立证据覆盖 | S-021 | 待实现 |
| ODA-MH-11 | state-axis separation | candidate/validated/approved/published/production/Git mutation 不折叠 | S-019/S-021 | 待实现 |
| ODA-MH-12 | final governed closeout | OPCM、Scope Delta、中文 closeout、final Validation、post-closeout reconciliation | S-022 | 待实现 |

## Session DAG

| Session | Topic | Scope | Deliverable | Exit Criteria |
| --- | --- | --- | --- | --- |
| S-016 | 双仓合同与公共边界冻结 | source-of-truth、public/private surface、allowlist boundary、identity axes、negative cases | Design Contract、KB strategy、Goal/AC handoff、ERBE contract/cases draft | 所有 ODA-MH-01/02/04/07/11 的边界、禁止折叠和最小安全切片冻结 |
| S-017 | Maintainer deterministic projection | fresh-root export、allowlist、residue scan、exact tree/diff、projection manifest | exporter/manifest contract、validation fixtures、projection evidence | 不明文件、路径逃逸、私有残留和 tree drift fail closed；只生成 candidate，不更新远端 |
| S-018 | End-user lifecycle surface | clone/install/doctor/upgrade/backup/install record/recoverable uninstall | user docs、lifecycle implementation、record schema、clean-room replay | 普通用户只需 clone + target；升级保留 target authority 且可恢复 |
| S-019 | Identity、release 与 GitHub 权限 | revision/candidate/projection/tag/release identity、rights/license、permission/authorization | release governance contract、permission matrix、readback checklist | candidate、approval、push、tag、release、production 状态分离且无默认发布权 |
| S-020 | External PR 回流维护 | public PR provenance、review、canonical port、re-export、validation | contribution policy、PR provenance record、round-trip evidence | 公开仓修改不直接成为真源；回流后 projection 可重算 |
| S-021 | Clean-room 与独立验收 | maintainer/end-user UAT、ERBE RED/GREEN、independent Validation、Semantic Review | UAT/Validation/Semantic artifacts、final evidence matrix | 关键正负例由独立 authority 重算；不把测试通过升格为 release |
| S-022 | Final closure 与 reconciliation | OPCM、Scope Delta、中文 closeout、最终状态、post-closeout 对账 | final closeout、Validation、reconciliation、release decision packet | 只在完整 Goal completion rule 满足时关闭；否则保持 To do/Doing 并记录下一步 |

固定依赖为 `S-016 → S-017 → S-018 → S-019 → S-020 → S-021 → S-022`。每个 Session 的 `Done` 只关闭该 Session 的有界范围；Session closeout 后必须扫描下一 Session，不得把 S-016 设计完成当作 SP-003 完成。

## 必需门禁与 authority

- 入口：Task Intake、Context Bootstrap、SGC v1、Goal Conformance/Scope Delta、Goal Contract/Goal Patch。
- 设计与实现：pre-Builder Semantic Review、digest-bound lane card、ERBE specification-first、license/provenance 与 default-deny。
- 验证：clean-room、独立 `user-acceptance-test`、independent Validation、必要时 Semantic Review 与最终 post-closeout reconciliation。
- 稳定规则写入 `kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json`，阅读面由 renderer 生成；状态、blocker、candidate、decision 与 evidence 留在 `Dashboard/`。
- GitHub create/push/tag/release、远端 read-back 与权利确认均是外部 authority；本轮不执行。

## 非目标与 claim ceiling

- 不在本轮创建/修改 Skill、exporter、installer 或 public repo。
- 不执行 GitHub repo 创建、push、tag、release，不写全局 Skill，不作生产就绪声明。
- 不把公开仓视作第二编辑真源，不把外部 PR merge 视作 canonical truth。
- 本 Stage Plan 的最大当前主张仅是：SP-003 的完整实现边界、Sessions、验收、authority 和 claim ceiling 已落库；实现和公开发布尚未发生。
