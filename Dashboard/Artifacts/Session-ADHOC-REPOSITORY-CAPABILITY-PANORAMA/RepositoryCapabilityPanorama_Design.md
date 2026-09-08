# 仓库能力全景、质量审计与开源指南设计交接

> 本文是 `ADHOC/REPOSITORY-CAPABILITY-PANORAMA` 的 Design lane 产物。它冻结 Builder 的最小安全切片与验收边界，但不表示全景已生成、质量审计已完成、测试已通过或公开版本已获发布授权。

## C0 权威与任务入口

- 原始目标 authority：在当前 checkout 上生成可筛选的 Dashboard 能力全景，列出 SGE Governance 的全部 Skill 或能力，评估仓库质量、Skill 干净状态与 Semx 源仓残留，识别未来开源缺口，并提供小白使用与维护者发布指南。
- 执行启动包：[RepositoryCapabilityPanorama_ContextBootstrap.json](RepositoryCapabilityPanorama_ContextBootstrap.json)。其中限定所有产物是派生读模型，禁止修改 `kb/` canonical truth、Dashboard lifecycle 状态以及执行 commit、push、tag、release、公开仓创建或全局安装。
- 设计 lane 合同：[RepositoryCapabilityPanorama_DesignLaneTaskCard.json](RepositoryCapabilityPanorama_DesignLaneTaskCard.json)。任务卡摘要已通过 deterministic validation；该通过只证明 card 结构与绑定有效，不证明设计内容或后续实现正确。
- 前置设计参考：[../Session-ADHOC-REPOSITORY-QUALITY-AUDIT/RepositoryQualityPanorama_Audit_Design.md](../Session-ADHOC-REPOSITORY-QUALITY-AUDIT/RepositoryQualityPanorama_Audit_Design.md)。本设计继承其“先生成派生全景、再独立审计、保留冲突、不以全景代替审计”的边界，并把范围扩展为能力清单、公开候选质量与两类操作指南。
- 仓库 authority 分层来自 [AGENTS.md](../../../AGENTS.md)、[Dashboard Rules](../../Rules.md)、[Dashboard Methodology](../../Methodology.md) 与 [SGC v1 canonical contract](../../../kb/data/strategy/strategy_sgc_structural_contract_v1.json)。

## 大白话任务解释

这次要做的不是再堆一份文件目录，而是给读者一张“这个仓库有什么、哪些真的可用、证据在哪里、哪些只是候选、下一步怎样安全操作”的地图。地图需要同时服务两类人：第一次使用 Skill 的普通用户，以及准备把候选投影到未来公开仓的维护者。

全景必须把三件常被混淆的事拆开：文件存在不等于能力经过运行；本地测试通过不等于公开发布获批；Dashboard 或 HTML 中的结论不等于 `kb/` 稳定真源。任何质量结论都要带证据层级、当前 checkout 身份和不可推导边界。

## 设计范围与明确非目标

### 本次设计覆盖

1. Markdown、JSON、单文件 HTML 三个一致的全景阅读面及其 source manifest。
2. 核心 Skill、治理能力、确定性工具、schema、KB strategy、Dashboard 执行面、公共 lifecycle、可选编排器、可选扩展、文档、示例与测试的完整分类。
3. Git/目录质量、测试与 gate、文档/CLI 一致性、公共 allowlist、license/provenance、Skill 身份干净度、Semx/KYM/TCO/绝对路径残留和开源缺口的证据化审计。
4. 普通用户从候选源到最小项目的可复制路径，以及维护者从私有 canonical source 到公开 projection/release 决策点的操作指南。
5. Builder 写入边界、验收矩阵、Validation 重点与 claim ceiling。

### 本次不做

- 不修改核心 Skill、工具、schema、测试、KB、Dashboard Session/Stage Plan 或 Git 历史。
- 不修复审计发现；发现只进入本任务的审计报告与后续候选建议。
- 不创建或操作 `bm-sge-governance` 远端仓库，不 commit、push、tag、release，也不做全局 Skill 安装。
- 不把 `build-kym`、`build-tco-coverage` 描述成默认核心能力；它们目前只是默认关闭、无 entrypoint 的 optional extension interface。
- 不以文件扫描声称语义正确、普遍跨平台兼容、逐文件权利已获确认或 production readiness。

## Read Manifest 与当前架构读取

| 证据域 | 已读入口 | 对本设计的约束 |
| --- | --- | --- |
| 仓库治理与 claim ceiling | [AGENTS.md](../../../AGENTS.md)、[SGE checkpoint Skill](../../../.codex/skills/sge-governed-checkpoints/SKILL.md)、[SGC v1](../../../kb/data/strategy/strategy_sgc_structural_contract_v1.json) | 派生视图不升格为 truth；结构证据不能替代语义/运行证据；完成措辞必须弱于或等于证据。 |
| Dashboard authority | [Rules](../../Rules.md)、[Methodology](../../Methodology.md)、[Current State](../../Current_State.md)、[Stage Plans](../../Stage_Plans.md)、[Sessions](../../Sessions.md) | `Dashboard/` 是执行记忆；状态冲突必须保留，不能 first-wins；本任务不改 registry 表面。 |
| 公共入口与用户路径 | [README](../../../README.md)、[中文新手指南](../../../docs/Beginner_Guide_CN.md)、[快速开始](../../../docs/Quick_Start_CN.md) | 用户指南只能引用实际 CLI 参数、预期输出和恢复边界。 |
| 公共文件与发布边界 | [public export manifest](../../../public_export_manifest_v1.json)、[双仓分发策略](../../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)、[sge_public.py](../../../tools/sge_public.py) | 公共投影必须 default-deny；candidate、approval、projection commit、tag、release 是不同身份轴。 |
| 能力实现表面 | [核心 Skill 目录](../../../.codex/skills/sge-governed-checkpoints/)、[tools](../../../tools/)、[extensions](../../../extensions/)、[tests](../../../tests/) | 一个核心 Skill 内含多项治理能力；脚本、schema、测试分别是执行器、合同和证据，不应全部冒充 Skill。 |
| 全景渲染方法 | `exploration-dashboard-synthesizer` Skill 及其 HTML renderer contract | JSON 用于丰富关系与来源字段；HTML 必须离线、可筛选、有详情抽屉，并明确只是 derived read model。 |

当前架构可概括为四层：`sge-governed-checkpoints` 是默认核心；公共文档、KB 阅读面与 lifecycle utility 是 companion；`run_sge_loop_goal_cycle.py` 与 orchestrator profile 是可选编排层；extension registry 中的 domain extension 默认关闭。目标项目始终拥有自己的 `AGENTS.md`、`kb/`、`Dashboard/`、Goal 与 Session authority。

## 全景信息架构

### 输出集合与责任

| 产物 | 责任 | 不承担的责任 |
| --- | --- | --- |
| `RepositoryCapabilityPanorama_Data.json` | 当前 checkout 的机器可读派生快照；保存来源、能力、证据、审计发现、指南步骤与冲突 | 不成为 KB 或 Dashboard registry 真源 |
| `RepositoryCapabilityPanorama.md` | 中文长文阅读面；完整列出能力、质量解释、残留分类、缺口和指南 | 不代替 JSON 的结构校验或独立 Validation |
| `RepositoryCapabilityPanorama.html` | 单文件离线交互视图；从同一 JSON 渲染 | 不发起网络请求、不修改仓库、不成为批准凭据 |
| `RepositoryCapabilityPanorama_Audit_Report.md` | 记录实际命令、verdict、finding、证据层级与 claim boundary | 不自动修复 finding，不授予 release authority |
| `RepositoryCapabilityPanorama_Generator.py` | 确定性采集与渲染入口；同一 checkout 可重算 | 不自行决定语义 truth、权利批准或远端状态 |

所有人类阅读面都要链接到精确源文件；digest、tree identity 和命令输出保存在 JSON/审计证据中。HTML 页首固定展示生成日期、branch、HEAD、worktree dirty/clean 状态、source manifest revision 与 claim boundary，避免截图脱离身份后被误用。

### 页面与导航

HTML 使用一个数据源、六个视图：

1. **总览**：仓库身份、核心/可选能力数量、quality gate 摘要、公开候选 posture、阻断项、证据新鲜度。
2. **能力地图**：按能力族分组，展示“用户能做什么—入口—状态—证据—限制—依赖”。
3. **质量与残留**：按 quality dimension 和 residue class 展示发现、严重度、source/public 可见性、修复建议。
4. **Dashboard/KB 导航**：Big Ideas、Stage Plans、Sessions、Decisions、Risks、Exceptions、Artifacts、Agent Logs、KB、tests 与 Git source manifest；保留所有互相冲突的记录。
5. **小白指南**：可复制命令、需要替换的值、成功输出、常见失败与恢复。
6. **开源发布指南**：maintainer-only 的 candidate→review→authorization→projection→release→read-back 序列及每一步 authority gate。

共同交互包括关键词搜索、能力族/层级/状态/证据级别/严重度/残留类别/是否 public allowlisted 筛选、排序、分页、URL hash 状态、重置和详情抽屉。详情抽屉必须保留 source links、检查命令、观察结果、不可推导结论和 next action。

### JSON 最小数据合同

顶层至少包含：

```text
schema_version, title, subtitle, generated_at, source_identity,
claim_boundary, source_manifest, capability_groups, capabilities,
quality_dimensions, audit_checks, residue_findings, release_gaps,
dashboard_entities, visible_conflicts, beginner_guide, maintainer_release_guide,
recommendations
```

每个 `capability` 至少包含：`id`、`name_cn`、`kind`、`family`、`layer`、`user_outcome`、`entrypoints`、`status`、`default_enabled`、`dependencies`、`source_refs`、`evidence_level`、`tested_scope`、`limitations`、`public_disposition`。其中：

- `kind` 只允许区分 `core_skill`、`governance_capability`、`tool`、`schema_contract`、`canonical_strategy`、`dashboard_execution_surface`、`optional_orchestrator`、`optional_extension_interface`、`documentation`、`example`、`test_or_gate`；避免“每个文件一个 Skill”。
- `status` 至少区分 `active`、`candidate`、`optional_disabled`、`derived_only`、`historical_provenance`、`evidence_gap`，且每个英文值在阅读面都有中文解释。
- `evidence_level` 使用 SGC v1 的 `execution_bound`、`test_bound`、`structurally_supported`、`externally_supported`、`inference_only` 或 `ungrounded`，不得从较弱层级推导更强结论。

每个 `audit_check` 至少包含：`check_id`、`dimension`、`command_or_method`、`expected`、`observed`、`verdict`、`evidence_level`、`source_refs`、`limitations`、`freshness`。每个 finding 至少包含：`finding_id`、`category`、`severity`、`surface`、`public_reachability`、`classification`、`evidence`、`impact`、`recommended_action`、`blocking_for`、`claim_ceiling`。

## 完整能力分类

Builder 必须按下列能力族逐项枚举，不能只列目录计数。若审计 lane 发现新增或缺失能力，可补充条目，但改变分类法或把 optional 提升为 core 属于 Design Delta。

| 能力族 | 必须覆盖的能力 | 主要入口/证据 |
| --- | --- | --- |
| 1. 任务入口与上下文控制 | proportional Task Intake、Context Bootstrap、semantic refresh、required/conditional read set、epistemic search space、change-impact topology | `AGENTS.md`、`context_bootstrap.py`、context schema/packet evidence |
| 2. 规格优先与结构治理 | ERBE applicability、Contract/Cases、trusted RED、same-identity GREEN、write exclusions、SGC claim/evidence matching、SI-1..SI-6、forbidden collapses | ERBE/SGC canonical strategy、checkpoint Skill、相关 gate |
| 3. Goal 与范围完整性 | Goal contract、Goal Patch/resolve、duplication audit、must-have ledger、Scope Delta、OPCM、Goal Conformance、Loop continuation | `goal_patch.py`、goal schemas、Dashboard/closeout rules |
| 4. 多 lane 协作合同 | workflow contract、Multi-Agent Activation、Design/Builder/Validation/Closure 分工、lane task card validate/render、prompt duplication audit、topology exception | `workflow_contract.py`、`lane_task_card.py`、lane schemas |
| 5. Validation 与收敛 | Validation Handoff、独立 read-mostly review、baseline snapshot、Delta Read Set、rebaseline triggers、delta compare、adversarial/current-contract 分离、post-closeout reconciliation | `context_state.py`、validation snapshot schema、checklists |
| 6. 语义、证据与 truth placement | Semantic Architecture/Frame-First review、S1-S6/L0-L6 diagnostic、KB/Dashboard split、Contract Delta Scan、BDD sync、reader explanation、closeout-language | canonical strategy、Skill/checklists、`guardrail_checklist.py` |
| 7. Dashboard 生命周期 | Big Idea/Stage Plan/Session/Decision 等 TSP、session registry reconcile/validate、archive/index、DKG 派生边界、closeout 与 Agent Log | `Dashboard/` rules/methodology/tools；属于执行记忆而非核心安装内容 |
| 8. 公共候选 lifecycle | public `doctor`、default-deny `export`、source/destination `verify`、minimal `bootstrap`、core `install`、recoverable `upgrade`、recoverable `uninstall` | `tools/sge_public.py`、manifest、public tests、docs |
| 9. 可选 Loop 编排 | profile-driven Loop Goal cycle、continuation/termination、项目 owner profile/hook boundary | `tools/run_sge_loop_goal_cycle.py`、`extensions/orchestrator_profile_v1.json`；默认非 core |
| 10. 可选领域扩展接口 | `build-kym`、`build-tco-coverage` 的注册、缺失时 fail-closed、core continues | `extensions/registry_v1.json`；无 entrypoint，不能声称能力实现已随仓库提供 |
| 11. 数据合同与 canonical strategy | 五个公开 schema、project profile、strategy mapping/source manifest/workflow registry、ERBE/Human-AI/KB promotion/semantic surface/SGC/dual-repo strategy | `.codex/.../schemas/`、`kb/data/strategy/`、rendered Markdown |
| 12. 用户教育与验证证据 | README、Beginner Guide、Quick Start、minimal project、unit/contract/public projection/repository quality/session registry/loop orchestrator tests | `docs/`、`examples/`、`tests/`；测试只支撑其实际覆盖范围 |

能力条目必须额外给出 `public_disposition`：`allowlisted`、`private_execution_only`、`maintainer_validation_only`、`not_shipped_interface` 或 `historical_only`。Dashboard 工具和执行历史即使有用，也不能因为全景列出就进入公共包。

## 质量审计设计

### 质量维度

| 维度 | 检查方法 | 合格判定 | 证据边界 |
| --- | --- | --- | --- |
| Checkout 与可重复性 | 记录 branch、HEAD、tracked/untracked/renamed/generated inventory；生成前后比较 diff | 所有本任务写入均在允许前缀，未覆盖他人文件；身份可定位 | dirty worktree 不是自动失败，但必须逐项显示归属与影响 |
| 核心 Skill 完整性 | manifest 与实际 core 文件集比对；运行 repo-local doctor/profile/genericity 相关 gate | 缺文件、未知 public 文件、项目身份依赖均 fail closed | 本地 structural/test pass 不证明任意项目可用 |
| 公共候选干净度 | `public_export_manifest_v1.json` 结构、allowlist exactness、private token/residue scan、fresh destination export/verify | 公共候选只含 allowlist，未知/私有残留为阻断 | 只证明当前候选，不证明 rights approval 或远端状态 |
| 测试与门禁 | 非零 test discovery；运行维护中的 repository/public/session/loop/contract gates | 命令退出码为零，测试数非零，失败原文保留 | 每项只支撑其测试合同，不把 test pass 当语义全真 |
| KB 与派生阅读面 | KB renderer `--check`、manifest/源文件/输出一致性 | canonical JSON 与 rendered docs 无 drift | rendered Markdown 不是可写 authority |
| Dashboard registry | `reconcile --check` 与 `validate`；本任务不 apply | 两项均为零且不含 identity/row/unknown archive error | registry pass 不证明 Session 语义完成 |
| 引用与文档 | Markdown source link 存在性、README/Beginner/Quick Start 命令与实际 `--help` 对照 | 无断链；参数、默认值、成功输出和限制与实现一致 | 文档正确不证明命令已在所有平台运行 |
| 生命周期恢复性 | fresh-root bootstrap/install/upgrade/uninstall 的既有测试与必要临时演练 | 不覆盖 target authority；备份/回滚/trash/record 行为可观察 | 临时本机演练不是跨平台或 production evidence |
| License/provenance | 每个 allowlisted file 有 license、source、provenance、public、execution_context 分类；未知权利 fail closed | 机器字段完整；发布前另有 human rights confirmation | MIT 文件与字段本身不等于所有上游权利已获确认 |

审计报告同时记录“已运行”“仅静态检查”“未运行/缺证据”。禁止把未运行能力写成 passed，也禁止让 generator 自报结果替代独立 Validation。

### Semx 与源仓残留分类

扫描至少分四个互不折叠的集合：当前 tracked active source、manifest allowlisted public candidate、tests/examples/fixtures、Dashboard/Archives 与 immutable provenance。匹配 token 至少包含大小写变体的 `semx`、`semx-cli`、`semx-kb`、KYM/TCO、`S-384`、`S-485`、`audio-transcriptor`、本机用户名与绝对 home path；还要扫描 symlink、文件名、JSON 值和 CLI/help 输出，而不仅是正文 grep。

| 分类 | 定义 | 默认影响 |
| --- | --- | --- |
| `active/public`（当前活跃或公开可达） | 命中位于默认加载的 core、公共 allowlist、用户文档、安装产物或运行路径，并可能把旧项目身份带给用户 | public candidate 阻断；给精确文件/行或结构路径和修复建议 |
| `historical provenance`（历史来源证据） | 命中只在明确标记的 Dashboard archive、closeout、迁移记录中，且不进入公共导出/默认加载 | 可保留但必须解释隔离依据；若被 allowlist 或 runtime 引用则升级为阻断 |
| `fixture/example`（测试或示例） | 命中用于 negative case、拒绝规则或清楚标注的示例，运行时预期是识别/拒绝它 | 非自动问题；必须显示测试意图与是否 public 可见，避免误判为 active dependency |
| `false positive`（非身份残留） | 子串命中但上下文与旧项目无关，或是受控术语说明 | 记录裁决理由，不计缺陷 |

每个命中必须包含 `surface`、`tracked`、`allowlisted`、`default_loaded`、`context_excerpt`、`classification`、`rationale` 和 `reviewer_confidence`。全景显示分类后的 finding 数量，但不得用 grep 数量直接形成质量 verdict。

## 小白 Skill 使用指南结构

指南面向“已拿到当前公共候选 clone、不会维护私有源仓”的用户。每一步固定包含：所在目录、完整命令、需替换值、预期成功输出、失败时不要做什么、恢复方法、该步证明/不证明什么。

1. **准备**：要求 Python 与一个当前候选 clone；用占位符 `<PUBLIC_CLONE>`、`<TARGET_PROJECT>`，解释二者不能是同一路径。
2. **检查候选**：在 `<PUBLIC_CLONE>` 运行 `python3 tools/sge_public.py doctor`；预期 `public_doctor:pass`，并解释这只是 repo-local manifest/残留/门禁检查。
3. **可选的干净 staging**：维护/评估场景运行 `python3 tools/sge_public.py export <EMPTY_STAGING>`；目标必须不存在或为空；普通终端用户无需先 export 已公开 clone。
4. **建立最小项目**：运行 `python3 tools/sge_public.py bootstrap <TARGET_PROJECT>`；说明拒绝非空目录是保护行为。
5. **安装 core**：从 `<PUBLIC_CLONE>` 运行 `python3 tools/sge_public.py install --target <TARGET_PROJECT>`；`--source` 只作为高级/测试 alternate source。
6. **验证最小治理入口**：在 target 中验证 Skill 文件存在，使用 repo 自己的 `AGENTS.md`、KB/Dashboard authority 跑最小 Goal；禁止复制本源仓的历史 Dashboard。
7. **升级与恢复**：运行 `upgrade --target`，检查 `.sge-backups/`；说明失败自动恢复与手工恢复边界。
8. **可恢复卸载**：从 source 调用 `uninstall --target`，检查 `.sge-trash/` 与 install record；禁止手工猜测批量删除。
9. **限制**：candidate、单机 clean-room、跨平台、license rights、远端发布、production readiness 分别说明。

Builder 必须以 `python3 tools/sge_public.py <subcommand> --help` 和实际实现校正参数，不能复制过时文档；如文档与实现冲突，要保留确切差异并把它列为 docs defect，而不是责怪用户。

## 维护者开源发布指南结构

指南遵循“私有 `sge-governance-skill` 是唯一 canonical development source；公开 `bm-sge-governance` 是 exact-allowlist 单向 projection”的架构。以下步骤是操作设计，不是本任务授权：

1. **冻结身份**：记录 private source branch/commit/tree、manifest revision、export tool revision、目标 public repo、候选版本与预期 tag；这些身份不可互相替代。
2. **确认 source 工作树**：审查 tracked/untracked 差异并确定哪些变化进入候选；是否要求完全 clean 必须依发布合同决定，不能静默丢弃文件。
3. **逐文件 license/provenance review**：核对 allowlisted 文件的 source、license、provenance、public 与 execution-context 分类；人类 rights owner 对具体 candidate 作确认，未知项 fail closed。
4. **fresh-root default-deny export**：导出到不存在或空的 staging；保留 export metadata、candidate fingerprint、exact file set 与 digests。
5. **deterministic verify 与 residue scan**：用 `verify --source <PRIVATE_SOURCE> --destination <STAGING>`、public doctor、引用/身份/绝对路径检查验证 staging；未知文件或 private residue 阻断。
6. **clean-room 用户路径**：从 staging bootstrap 新 target，执行 install、最小入口、upgrade/backup、失败恢复与 uninstall/trash；记录环境和实际输出。
7. **独立 Validation/UAT**：reviewer 从 durable inputs 重算 candidate；producer 的 doctor/verify 自报不等价于独立 verdict。
8. **人类授权 checkpoint**：授权人绑定具体 source/candidate/public target/commit payload/tag/release payload；没有该授权时停止在 `candidate_not_approved`。
9. **单向投影更新**：只有获授权后才允许把 exact projection 写入公开仓；公开 PR 必须先人工审查并回流私有 canonical source，再重新导出，禁止公开仓成为第二真源。
10. **tag/release 与 read-back**：commit、push、tag、release 分别需要适用权限；发布后重新读取远端 commit/tree/tag/assets、checksums、release notes 与 license/provenance report，不能用本地成功推导远端成功。
11. **维护与回滚**：source release 或安全修复都重新走 export/diff/Validation；发布前可 abort，发布后通过显式修复或撤下/标记受影响 release 处理，不能声称删除已被复制的公开副本。

指南中的 Git/GitHub 命令只能以“授权后示例”呈现，必须使用 `<PUBLIC_REPO>`、`<BRANCH>`、`<VERSION>` 等占位符，并在每个外部 mutation 前标注 authority gate。不得在本次 Builder 或 Validation 中实际运行这些命令。

## Builder 实施切片与写入边界

### 实施顺序

1. **B1 Source snapshot**：读取当前 checkout、两条只读 audit lane 返回结果和已列 authority；冻结 source manifest、Git identity、生成时间与未读/缺失证据。
2. **B2 Data model/generator**：实现确定性采集、分类和 JSON 输出；所有状态/证据/残留 finding 都从 source refs 或 audit evidence 构造，不能从旧全景复制为当前事实。
3. **B3 Reader projections**：从同一 JSON 生成 Markdown 和单文件 HTML；不得让 Markdown、HTML 各自维护第二份事实。
4. **B4 Audit report/guides**：写入实际命令、观察值、质量 verdict、缺口和两类指南；未运行项明确为 evidence gap。
5. **B5 Self-check and handoff**：验证 JSON/HTML 内嵌数据、筛选/详情、链接、source identity、写范围与 claim language，准备独立 Validation handoff。

### Builder 允许写入

Builder 仅可写 `Dashboard/Artifacts/Session-ADHOC-REPOSITORY-CAPABILITY-PANORAMA/RepositoryCapabilityPanorama_*`，建议具体为本设计列出的 Data JSON、Markdown、HTML、Audit Report、Generator 与后续 lane/validation 证据。现有由其他 lane 拥有的 card、prompt、validation 文件不得被无依据覆盖。

### Builder 禁止写入

- `AGENTS.md`、`README.md`、`docs/`、`kb/`、`tools/`、`extensions/`、`tests/`、`public_export_manifest_v1.json`。
- `Dashboard/Current_State.md`、`Stage_Plans.md`、`Sessions.md`、registry/index/archive、Decisions/Risks/Exceptions 或历史 closeout。
- `.git/`、全局 Skills、外部 repo、远端 provider/GitHub 表面。
- 审计发现涉及上述路径时，只记录 finding 与建议，不顺手修复。

## 验收判定矩阵

| AC | 可观察验收判定 | 必需证据 | 失败条件 |
| --- | --- | --- | --- |
| `PAN-DESIGN-01` | 信息架构覆盖六个页面视图、三种派生输出、source identity/manifest、共同筛选与详情模型；完整能力分类明确“一个核心 Skill、多项能力、可选扩展非实现” | 本设计的“全景信息架构”“完整能力分类”及 Builder 产出的统一 JSON | 只列文件、漏掉任一能力族、HTML/Markdown 使用不同事实源，或把 derived view 当 authority |
| `PAN-DESIGN-02` | 质量审计覆盖 checkout、Skill、public candidate、tests、KB、registry、references/docs、lifecycle recovery、license/provenance；残留逐命中归入四类且给上下文证据 | Audit Report、命令输出、source links、residue finding records | 以 grep 数量下 verdict、混合 active 与 historical、缺少 evidence level，或 producer 自报代替独立验证 |
| `PAN-DESIGN-03` | 小白指南与维护者指南均给真实入口、完整命令、占位符、预期输出、恢复/限制；发布指南逐步标注 authority checkpoint | `--help` 对照、当前 docs/implementation 引用、两份阅读面 | 使用不存在的参数、把 `--source` 设为普通用户必需、执行外部 mutation，或把 candidate 写成 released |
| `PAN-DESIGN-04` | Builder 只写允许前缀；JSON/Markdown/HTML 可解析且一致；Validation 可从 source snapshot 重算；最终措辞不超过当前 checkout 有界证据 | 最终 diff、解析/链接/交互检查、独立 Validation artifact | 越界写入、source identity 缺失、generated output 自验即通过、或声称 rights/release/cross-platform/production ready |

## 测试与门禁计划

Builder 先检查每条命令的存在性与 `--help`，再运行。具体测试清单由当前 checkout 与 audit lane 收敛，但至少包括：

- `python3 tools/sge_public.py doctor`；只支撑当前 repo-local public candidate gate。
- fresh 临时目录上的 `export` 与 `verify`，并核对 exact manifest file set；不得写入已存在的用户目录。
- 当前维护的 unittest/contract tests，确认 discovery 非零；报告测试数量、环境和失败原文。
- `python3 Dashboard/tools/session_registry.py reconcile --repo . --check` 与 `python3 Dashboard/tools/session_registry.py validate --repo .`；本任务不运行 `--apply`。
- KB renderer/check 的当前实际入口；若实现/文档入口不一致，记录 evidence gap，不猜参数。
- JSON parse、Markdown links、HTML 内嵌 JSON parse、HTML 离线加载、关键词/字段 filter、URL hash、详情抽屉、reset。
- 生成前后 `git status --short` 与 final diff inventory，确认只有 `RepositoryCapabilityPanorama_*` 发生本 lane 授权写入；并保留其他并行 lane 的文件归属。
- closeout 与 final validation 由主线程/后续 lane 执行；本 Design lane 不生成通过 verdict。

## Validation 重点

独立 Validation 必须从实际 source snapshot 复核，而不是只读生成器摘要：

1. 逐项抽查所有能力族是否有真实 source entry，尤其 optional extension 是否被误写为 shipped capability。
2. 对 manifest allowlist 和 active core 分别重跑残留扫描；抽查 historical/fixture/false-positive 裁决上下文。
3. 将 Audit Report 的每个 `passed` 对照实际命令、退出码、范围和 evidence level；未运行项不能被聚合 UI 掩盖。
4. 验证 Markdown/HTML 与 JSON 同源，source links 可定位，冲突未被 first-wins 合并。
5. 按 CLI `--help` 和实现验证两套指南，检查参数、默认 source、目标目录保护、预期输出、备份/恢复/卸载语义。
6. 检查 final diff 的 write scope、并行文件归属和未登记生成物；若基线身份或 final diff 超出 Delta Read Set，必须 rebaseline。
7. 用 SGC v1 检查 SI-1..SI-6、false closure、recompute validation、mock grounding 与 scope substitution。

## 风险与升级触发器

| 风险 | 默认处理 | 必须升级的条件 |
| --- | --- | --- |
| 并行 lane/dirty worktree 写冲突 | 只编辑任务卡授权文件，记录基线与 owner；不覆盖不属于本 lane 的 untracked artifacts | 同一目标文件被并行修改，或无法判定 artifact owner |
| 能力清单膨胀为营销声明 | 每项绑定 kind、status、source、evidence、tested scope、limitation | 需要把 candidate/optional interface 提升为 active/core |
| 残留误报或漏报 | 四集合扫描并逐上下文裁决 | active/public 命中涉及 source authority、license 或默认运行依赖 |
| 发布指南被误当授权 | 每个 mutation step 标注 authority gate；本轮不执行 | 需要创建公开仓、push、tag、release 或确认逐文件权利 |
| 设计产生稳定合同变化 | 保持 Dashboard-only design evidence | 需要修改 public lifecycle、truth placement、status vocabulary、acceptance posture 或 canonical strategy 时，先走 Contract Delta/KB promotion 与 Semantic Review |
| 历史全景与当前事实冲突 | 以当前 checkout 为主，历史只作 provenance；显式保留冲突 | 当前 authority 自身互相冲突且无法通过 source hierarchy 裁决 |

Semantic Reviewer 不因本设计默认启动：当前只组织现有能力和证据，不批准新稳定语义。若 Builder 改变核心/可选边界、公共生命周期、release authority、acceptance/gate strictness，或把本分类提升为 canonical contract，则触发 Semantic Architecture + Frame-First 双 verdict 复核。

## SGC、ERBE 与 BDD 边界

- SGC strongest claim level：本 Design lane 为 `structurally_supported`（结构支持）。它只支撑设计交接可供 Builder 使用，不支撑审计通过、运行正确或发布就绪。
- SI-1/SI-2：能力文件存在与 JSON shape 只算结构证据；运行和测试结论必须绑定实际 evidence layer。
- SI-3：稳定 truth 留在 `kb/`，执行状态留在 Dashboard，测试/报告是 evidence，HTML 是派生阅读面。
- SI-4：generator 不能验证自己；后续独立 Validation 必须重算关键结论。
- SI-5/SI-6：最终 claim 不得超过当前 checkout 证据，并逐项覆盖原始目标的全景、能力、质量/残留、开源缺口与两套指南。
- ERBE applicability：`not_applicable`（不适用），因为本任务不改变终态谓词、状态机、promotion/write contract 或 maintained acceptance posture。
- BDD sync：本设计与预期 Builder 只新增派生 artifacts，不改变 maintained runtime/gate/schema；无需修改 BDD。若 Builder 后续改变 `sge_public.py` 或 maintained gate，则必须重新评估。

## Design Delta 规则与 Builder handoff

Builder 可以在不改变语义的前提下调整字段命名、展示布局和采集实现，但必须保持：统一 JSON 事实源、十二类能力族、四类残留裁决、六个视图、两套指南、evidence level、source identity、write exclusions 和 claim ceiling。

以下变化必须在 closeout 中记录 Design Delta，并说明 rationale、影响、是否需要人类/Validation/Semantic Review：删除能力族或原始目标项；把 optional/candidate 提升为 core/active；改变 public/private 边界；更改 release authority；省略证据层级或残留上下文；修改写入范围；用不同 authority 验证原要求；从三种派生输出中删除一种。

Builder 接收本设计后，应先吸收两条只读审计 lane 的证据化结果，再实施 B1→B5。没有审计结果时可以搭建 schema/renderer，但不得填入 `passed`、`clean` 或发布准备结论。任何缺证据项必须显示为 `evidence_gap`，而不是由旧全景或推断补齐。

## Artifact path 与最大主张

- Design artifact：`Dashboard/Artifacts/Session-ADHOC-REPOSITORY-CAPABILITY-PANORAMA/RepositoryCapabilityPanorama_Design.md`
- 最大主张：已形成当前能力全景任务的结构化设计交接，明确了信息架构、能力分类、审计方法、两套指南、Builder 边界与验收判定。
- 明确不能主张：能力全景已经生成、整个仓库质量已验证、Skill 已确认完全干净、Semx 残留已清零、公开仓已存在、逐文件权利已批准、版本已发布、跨平台兼容或 production readiness。
