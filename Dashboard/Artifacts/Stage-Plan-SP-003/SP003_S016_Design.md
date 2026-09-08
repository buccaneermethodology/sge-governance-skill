# S-016 设计交接：双仓合同与公共边界冻结

## 关键结论中文展开

本设计只冻结 SP-003 的最小安全切片：私有 `sge-governance-skill` 是唯一 canonical development source，公开 `bm-sge-governance` 是由 exact allowlist 产生的单向 public projection/distribution repo，用户项目仍拥有自己的执行 overlay。它不实现 exporter、installer 或 lifecycle，也不证明 candidate、公开仓、发布、GitHub 远端状态或生产就绪。

`design_handoff_status=produced_for_review` 的含义是：Builder 可以把本文件和 ERBE Contract/Cases 当作后续实现入口；它不是 Semantic Reviewer 的批准、Validation verdict 或 release authorization。

## 任务与权限边界

- Session：`SP-003/S-016`；lane：`design`；模式：`full_baseline`。
- 本次依据 [lane card](SP003_S016_DesignLaneTaskCard.json) 执行；card 的 source digest 已由 renderer 校验通过。
- 本 lane 的写范围仅为：本文件、[ERBE Contract](SP003_S016_ERBE_Contract.json)、[ERBE Cases](SP003_S016_ERBE_Cases.json)。
- 不创建或修改 exporter、installer、public repo，不执行 GitHub create/push/tag/release，不修改 Goal、KB、Dashboard registry、Session 行或远端状态。

## C0 authority 与读取清单

本设计消费的是 card 指定的当前 Goal/strategy/tool 输入；这些输入定义了目标和边界，但不把历史 candidate 证据升级为 SP-003 实现证据。

| 来源 | 本次用途 | 证据边界 |
| --- | --- | --- |
| [AGENTS.md](../../../AGENTS.md) | 仓库硬门、truth split、claim ceiling 与外部副作用边界 | 规定治理要求，不证明本设计已被独立验证 |
| [SP-003 Goal Contract](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalContract.json) | 原始 mission、MH ledger、DAG、scope delta 与最大主张 | 仍将 ODA-MH-01..12 标为 pending；本 lane 只覆盖指定子集 |
| [SP-003 Loop Goal](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_LoopGoal.md) | 连续 Loop、禁止完成措辞与后续 Session 关系 | S-016 bounded 设计不等于 SP-003 complete |
| [SP-003 Stage Plan](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_StagePlan.md) | S-016 exit criteria、S-017..S-022 依赖与 owner/lane | 后续实现/验收仍未发生 |
| [dual-repo strategy](../../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json) | 稳定双仓语义、public boundary、pipeline 与 claim ceiling | 是策略输入，不是本次 runtime/export 结果 |
| [public export manifest](../../../public_export_manifest_v1.json) | 既有 allowlist、default-deny、license/provenance 与 layer 参考 | `candidate_not_approved`；不能当作已发布 manifest |
| [public lifecycle tool](../../../tools/sge_public.py) | 现有 maintainer/end-user surface 的设计输入 | 现有代码不等于 S-017/S-018 已实现或已验收 |
| [Goal Context Bootstrap](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalContextBootstrap.json) | 确认原始意图、必需 epistemic domains、跳过远端状态的理由 | 本轮不读取或改变 GitHub 远端；不凭空补齐外部 authority |

## Plain-language objective

为后续实现提供一个可审计、可重算、不可双向漂移的双仓合同，并把维护者内部 surface 与普通终端用户 surface 分开。S-016 的成功条件是五组指定 must-have 的边界和负例被冻结：`ODA-MH-01/02/04/07/11`，以及 card 指定的 `S016-AC-01/02/03`。其余 ODA-MH-03/05/06/08/09/10/12 保留在原始 Goal 中，由后续 Session 承担。

## 范围、非目标与 claim ceiling

### 本次范围

1. 冻结 private canonical → fresh staging → deterministic public projection 的 source-of-truth 方向。
2. 冻结 `bm-sge-governance` 的 exact-allowlist、default-deny、private residue 排除面，以及 target project overlay authority。
3. 冻结 maintainer/end-user surface、六个以上 identity/state axes 与禁止互相替代的规则。
4. 冻结 ERBE machine-readable Contract/Cases；正负例共 14 个，供 S-017..S-021 使用同一 case identity 做 RED/GREEN 与独立重算。

### 明确非目标

- 不实现或修改 `tools/sge_public.py`，不写 exporter/installer/lifecycle code。
- 不创建、同步、push、tag、release 或 read back GitHub `bm-sge-governance`。
- 不把 `public_export_manifest_v1.json` 的现有候选状态改成 approved/published。
- 不把 public PR merge 当成 canonical truth，不把 target project 文件当成公共 Skill 的可覆盖面。
- 不修改 `kb/`、Goal、Stage Plan、Dashboard registry 或历史归档；本次稳定规则仍只作为本设计 handoff 的输入和 future promotion candidate。

本 lane 的最高主张是：`S-016 design/ERBE handoff 已形成并限制在设计层`。不得据此声称 exporter、installer、candidate、公开仓、发布或生产就绪。

## 当前架构读取与冻结合同

### 三个表面及其 authority

| 表面 | 角色 | 允许动作 | 不可推导 |
| --- | --- | --- | --- |
| 私有 `sge-governance-skill` | 唯一 canonical development source | 维护者开发、审查、测试、保留内部证据 | public repo 不能反向自动成为真源 |
| fresh staging / projection package | 一次 export 的可审计中间证据 | 按冻结 revision 与 allowlist 重算、扫描、比较 | staging/candidate 不是 release 或远端 mutation |
| 公开 `bm-sge-governance` | 单向 public projection/distribution repo | 仅在独立验证和人类授权后接收 projection commit/tag/release | 不是第二编辑真源，不承载 Dashboard/Goal/Session |
| target project | 用户自己的执行 overlay | 用户维护 AGENTS、Dashboard、Goal、Session、profile、domain extension | 公共安装不能夺取 target authority |

唯一维护方向是：

```text
private canonical source → frozen revision → fresh staging → exact projection
                                                   → independent validation/UAT
                                                   → human-authorized remote mutation
```

外部 PR 只能进入“公开仓输入”面；维护者必须审查并移植到私有 canonical source，然后重新 export、diff、Validation，才可能形成新的 public projection。

### Public content boundary

规则为 `default-deny`：只有逐文件 allowlist 中明确为公共、具备 license/provenance、且不含 execution context 的文件可进入 projection。允许面是通用 Skill、去项目化 KB/文档、examples、必要 tests/tools、LICENSE/NOTICE 和公共 metadata。

以下表面默认拒绝并应 fail closed：Dashboard、Sessions、Stage Plans、Agent Logs、Goal/closeout/OPCM、私有 provenance、完整本地报告、dirty worktree、绝对本机路径、credentials、未知文件、symlink/gitlink/LFS/nested repo 与路径逃逸。任何例外必须逐文件记录 source、license、provenance、public decision、execution-context decision，并有对应 negative case。

### Maintainer 与 end-user surface

| 角色 | 入口与责任 | 不应承担的知识 |
| --- | --- | --- |
| maintainer | 冻结 source/manifest/tool revision；fresh-root export；residue scan；exact tree/bytes/digest diff；独立 Validation/UAT；人类授权后的 public update/readback | 不能把验证结果直接写成发布，也不能绕过 private canonical |
| end user | clone 当前公开仓；`install --target <project>`；`doctor`；`upgrade --target <project>`；恢复性 uninstall | 不需要 export、allowlist、release、私有仓路径或 GitHub 权限知识 |
| target project owner | 保持自身 AGENTS/Dashboard/Goal/Session/profile 与领域扩展 authority | 不能被公共 Skill install/upgrade 覆盖 |

`--source` 若保留，仅是显式高级/测试/诊断入口；普通用户路径的 source 是当前 public repo，普通用户只需提供 target。

## Identity axes 与 state axes

### Identity axes

| 轴 | 表示什么 | 明确不能替代 |
| --- | --- | --- |
| `source_revision` | 私有 canonical 输入的 revision | `manifest_revision`、candidate、projection commit、release tag |
| `manifest_revision` | allowlist/policy manifest 的 revision | source 内容、candidate approval、release |
| `export_tool_revision` | 导出工具本身的 revision | 导出结果已通过 Validation |
| `export_run_id` | 一次 fresh staging/export 执行实例 | candidate identity 或远端 commit |
| `candidate_id` | 有边界 projection 候选的身份 | approved、published、production-ready |
| `projection_commit` | 公开仓接收的具体 tree/commit 身份 | source revision、release approval |
| `release_tag` | 经授权的发布标识 | candidate、commit 内容审计、production readiness |

### State axes

这些轴可以在同一记录中并存，但不得压缩成一个 `status`：

| 轴 | 允许语义 | 禁止折叠 |
| --- | --- | --- |
| `candidate` | 是否形成有边界候选 | 候选不等于 validated/approved |
| `validated` | 指定输入由独立 Validation/UAT 重算通过 | validated 不等于 approved/published |
| `approved` | 指定 authority 对指定 artifact 作出批准 | approval 不等于 Git mutation |
| `published` | 公开仓存在已读回的公开 projection | published 不等于 production-ready |
| `production_ready` | 另有明确生产证据后的状态 | 不能由测试、tag 或 LICENSE 推出 |
| `git_mutation` | create/push/tag/release 等外部变化是否发生 | 不能由 candidate/approval 推出 |
| `license_authorized` | 逐文件再分发权已被相应 authority 确认 | MIT 文件、digest 或登录状态不能单独推出 |

## Deterministic projection pipeline contract

| 步骤 | 输入 | 输出/证据 | authority | 禁止折叠 |
| --- | --- | --- | --- | --- |
| 1. freeze | source、manifest、tool revision | 可定位 identity tuple | private maintainer contract | source revision 不等于 release tag |
| 2. stage | fresh root、exact allowlist | projection tree、residue findings | maintainer surface | fresh staging 不等于 public repo |
| 3. compare | source/staging/expected tree | exact file set、bytes/digest、render diff | deterministic gate | 结构通过不等于语义批准 |
| 4. validate | durable inputs、同一 frozen case identity | independent Validation/UAT evidence | independent Validation / UAT | producer 自报 terminal status 不算独立证据 |
| 5. authorize/mutate | 指定 repo/tree/tag/payload | 人类授权记录、远端 readback | `repo-owner` 或明确发布 authority | candidate/approved 不自动授予 push/tag/release |

S-016 只定义步骤 1 的合同、步骤 2–5 的 authority 与验收接口；步骤 2–5 的实现和运行证据属于后续 Session。

## Must-have 与 S-016 AC 覆盖

| ID | 本设计冻结内容 | 未来可观察验收 | 当前状态与 claim ceiling |
| --- | --- | --- | --- |
| ODA-MH-01 | 三表面 authority 与单向 source-of-truth | 任何 public 变更均能追溯到 private canonical revision；反向编辑被拒绝 | `covered-in-design-freeze`：只证明合同已写入 |
| ODA-MH-02 | exact allowlist、default-deny、私有 residue 排除和逐文件 provenance 要求 | 未知文件、私有表面、绝对路径、symlink/路径逃逸 fail closed | `covered-in-design-freeze`：未运行 exporter |
| ODA-MH-04 | source/manifest/tool/run/candidate/projection/tag 身份轴 | case identity 与各身份值不互相复用或伪造 | `covered-in-design-freeze`：未形成 candidate/release |
| ODA-MH-07 | maintainer、end-user、target owner surface 分离 | 普通用户只需 clone + target；不接触 export/release 内部入口 | `covered-in-design-freeze`：未做 UAT |
| ODA-MH-11 | candidate/validated/approved/published/production/Git mutation/license state 轴分离 | 任一状态变化不会自动改写其它轴 | `covered-in-design-freeze`：未做独立 validation |
| S016-AC-01 | source-of-truth 与公共边界合同可执行化 | Contract 明确方向、deny 面、target overlay 与 owner | `design-input-ready`：待 Semantic Review/Builder 使用 |
| S016-AC-02 | identity/state axes 与 forbidden collapses | Contract/Cases 对身份和状态混淆有正负例 | `design-input-ready`：待独立重算 |
| S016-AC-03 | ERBE handoff、ladder、Validation focus 与 future misuse mitigation | Builder/Validation 能按 frozen case identity 重算且不越过 scope | `design-input-ready`：handoff 形成，不是 pass |

## ERBE applicability 与 oracle ownership

- `erbe_applicability=required`：本任务改变 source-of-truth、authority routing、write/promotion boundary 和多个终态状态轴。
- `contract_verdict` 与 `execution_verdict` 在本 lane 不宣称通过；这里冻结合同与 expected outcomes，不执行 RED/GREEN。
- `oracle_owner`：`repo-owner` 负责对 authority、公共边界、状态/身份语义作最终人类 oracle 决策；这不等于本次已批准。
- `validation_owner`：后续独立 Validation lane 从 durable inputs 重算，同一 frozen case identity 复用 RED/GREEN；不得接受 producer 自报状态。
- `semantic_reviewer`：因高语义风险、oracle/contract 冻结和未来漂移触发，后续独立 Semantic Reviewer 必须分别给出 `Design Freeze Validity` 与 `Implementation Entry Readiness`；本设计不冒充该 verdict。
- `CG skipped: no CG input provided`

机器可读的完整字段、invariants、forbidden collapses、oracle owner、write exclusions 与 cases 见 [ERBE Contract](SP003_S016_ERBE_Contract.json) 和 [ERBE Cases](SP003_S016_ERBE_Cases.json)。

## Implementation ladder 与 ownership

| Session | 最小实现切片 | owner/lane | 依赖与入口证据 | 不得提前声称 |
| --- | --- | --- | --- | --- |
| S-017 | fresh-root exact-allowlist export、residue scan、exact tree/diff、projection manifest | Builder；随后独立 Validation | 本设计 + ERBE C01–C07/C14 | 不得声称公开仓或 release |
| S-018 | clone/install/doctor/upgrade/backup/install-record/recoverable-uninstall | Builder；end-user UAT | 本设计 surface contract + target overlay cases | 不得让普通用户承担 maintainer surface |
| S-019 | identity、license/provenance、GitHub permission/authorization 与 readback contract | Design/Builder + repo-owner oracle | 本设计 C08/C12/C13/C14 | 不得把 candidate/approval 变成 mutation |
| S-020 | external PR provenance、private canonical port、re-export、validation 回流 | Builder；maintainer review | 本设计 C01/C08/C11 | 不得把 public PR/merge 变成 canonical truth |
| S-021 | clean-room maintainer/end-user UAT、ERBE RED/GREEN、独立 Validation、Semantic Review | UAT/Validation/Semantic lanes | 全部 frozen cases | 不得把测试通过升格为 release/production |
| S-022 | OPCM、中文 closeout、release decision boundary、post-closeout reconciliation | Closure + independent Validation | 原始 Goal MH-01..12 与最终 diff | 不得由 S-016 bounded closeout 关闭 SP-003 |

固定 DAG：`S-016 → S-017 → S-018 → S-019 → S-020 → S-021 → S-022`。S-016 的 ready 只表示下一个实现切片可从该 handoff 开始；不表示 Goal terminal。

## Validation focus 与 evidence handoff

后续 Validation 必须逐项重算 ODA-MH-01/02/04/07/11 以及 S016-AC-01/02/03，并覆盖原始 Goal 的未落地项不可被本设计吞并。重点是：

- fresh staging 中 exact file set、bytes/digests、私有残留、unknown/symlink/path escape 的 fail-closed 行为；
- 普通用户默认 current public source + target，以及 target authority 未被覆盖；
- identity tuple 的字段来源、唯一性和非替代关系；
- candidate、validated、approved、published、production-ready、Git mutation、license authorization 的独立状态变化；
- public PR 只能作为输入，必须回到 private canonical 后再 export/validate；
- RED 与 GREEN 使用完全相同的 frozen case identity；环境/fixture/import/path 错误只能记为 `error`，不能记为可信 RED；
- final diff、Dashboard/KB 状态、Scope Delta 和最终 closeout 若要支撑任何更高 claim，必须另有 durable independent review。

本次没有修改行为 gate 或 BDD readable cards：S-016 只新增设计合同与 ERBE 输入，尚未改变 maintained non-unit validator 的实现或枚举案例；后续若 S-017..S-021 改变此类 gate，必须按仓库 BDD 规则同步。

## Future-agent misuse scenarios

| 场景 | 可能误读 | 缓解 |
| --- | --- | --- |
| 1 | 看到 `design-input-ready` 或 `covered-in-design-freeze` 就写成 exporter/installer 已落地 | 任何状态词都附中文 claim ceiling；Contract 将设计、执行、验证、发布分轴，S-016 只允许 handoff claim |
| 2 | 把公开 PR merge 或公开仓现有内容当成 private canonical truth | 强制 C01/C08/C11 的单向回流规则；public PR 是 input，必须 port 到 private 后 re-export |
| 3 | 把 `candidate_id`、`validated=true` 或 `release_tag` 当作已发布/生产就绪 | C07/C09/C10/C12/C13/C14 逐轴负例；要求独立 Validation、人类授权和 remote readback |
| 4 | 为方便安装，让公共工具覆盖 target 的 AGENTS/Dashboard/Goal/Session | C10 冻结 target overlay authority；S-018 必须以 UAT 证明仅写受控 Skill surface |
| 5 | 为“完整”而将 Dashboard/Agent Logs/本机路径加入 allowlist | C03–C06/C14 default-deny；例外必须逐文件 provenance/license/decision，未知输入 fail closed |

## Design Delta policy、风险与后续 review

- Builder 不得直接修改本设计冻结的 Contract/Cases、expected、RED evidence、claim ceiling；任何变更都要形成 Contract Patch + Scope Delta，并重新 RED。
- 若 Builder 修改 public boundary、authority、state/identity axes、写入/发布边界或将 `--source` 改成普通用户必需入口，必须触发 rebaseline，并由 repo-owner/Validation/Semantic Reviewer 按影响复核。
- 若只是实现细节且不改变冻结谓词、输入输出、authority 或 claim ceiling，可在后续 closeout 记录 Design Delta；不能用实现便利隐式缩小原始 must-have。
- 主要风险：现有 `public_export_manifest_v1.json` 仍是候选状态且现有工具已有生命周期入口，未来 agent 可能把“已有代码/manifest”误读成架构已验收；本 handoff 明确把它们作为输入，不是 S-016 运行证据。
- 本 lane 未提供 external CG；保留精确记录 `CG skipped: no CG input provided`。

## Artifact path 与允许结论

- 设计交接：[Dashboard/Artifacts/Stage-Plan-SP-003/SP003_S016_Design.md](SP003_S016_Design.md)
- ERBE Contract：[Dashboard/Artifacts/Stage-Plan-SP-003/SP003_S016_ERBE_Contract.json](SP003_S016_ERBE_Contract.json)
- ERBE Cases：[Dashboard/Artifacts/Stage-Plan-SP-003/SP003_S016_ERBE_Cases.json](SP003_S016_ERBE_Cases.json)

允许的本 lane 结论是“**S-016 设计交接与 ERBE 冻结输入已形成，等待后续 review/实现/独立验证**”。不允许写 `SP-003 complete`、`published`、`production-ready`、“公开仓已建立”或“本设计已通过独立验证”。
