# SP-001 SGE Governance 迁移实施计划

## 计划摘要

- 本计划只建设可运行、可验证的 Governance 基础设施，不实现音频转写产品能力。
- 项目/Skill 身份为 `audio-transcriptor`，CLI 预留为 `audio-transcript`，仓库目录保持 `audio-transcriptor-skill`。
- 原计划要求产品设计字节不变；当前独立仓库已删除产品文件，只保留[历史 locator](Tombstones/Removed_Audio_Transcriptor_Design.md)，不再把它作为当前 authority 或 current-byte witness。
- 新建通用 repo-local Skill `sge-governed-checkpoints`，通过项目 profile 适配 audio-transcriptor。
- Semx 迁移源固定为 semx-cli `main@19e967a782e2e95d24475770bc234d86ad7c583e`；其他本机 Skill 来源也必须记录路径、revision/digest 与适配说明。
- 完成声明只覆盖治理框架的有界迁移和本地验收。

## 实施阶段

### S-001：可恢复基线与规划落库

- 初始化 Git 并提交整理前种子。
- 写入 Final Loop Goal、本计划、Context Bootstrap、Dashboard rows、closeout 和独立 Validation Review。
- 建立一次性 bootstrap exception：仓库本地 checkpoint Skill 尚不存在，使用固定 semx-cli 源脚本验证；不得把该例外外推到 S-002 之后。

### S-002：通用 SGE 核心与项目配置冻结

- 建立 source manifest，记录每个源文件的 `copy/adapt/replace/remove` 裁决。
- 逐一覆盖固定 semx-cli revision 的 `semx-kb/docs/strategy/` 56 个文件表面，并为 Markdown/JSON/图片分别记录来源摘要、阅读面角色、对应 `semx-kb/data/strategy/*.json` canonical mapping、裁决与目标 artifact；缺少 canonical source 的内容不得直接晋升为新项目稳定 truth。
- 对 `adapt_extract` 项重新冻结通用不变量；对 `reference_only` 项只保留 provenance/read-manifest；对 `remove` 项记录 Semx 产品耦合与替代机制；只有 ERBE、SGC 等接近通用合同的候选可标 `migrate_after_refreeze`，仍不得原样复制项目身份或路径。
- 从 semx-cli 迁入 checkpoint references、schemas、scripts，重构为 `.codex/skills/sge-governed-checkpoints/`。
- 新建 `kb/data/strategy/sge_project_profile_v1.json` 和 schema，固定 `project_id=audio-transcriptor`、`kb_root=kb`、`dashboard_root=Dashboard` 及各 authority 路径。
- 冻结 ERBE Contract/Cases/RED、Builder write exclusions 和本 Goal claim ceiling。

### S-003：Skills 与 deterministic tooling 迁移

- Profile 化 `guardrail_checklist.py`、`context_bootstrap.py`、`context_state.py`、`goal_patch.py`、`lane_task_card.py`。
- 将通用 ERBE/Goal Effect/governance integration 放入 Skill 自带 `lib/sge_governance/`，不进入 audio 产品 runtime。
- 以 profile + workflow registry 驱动的 `workflow_contract.py` 替代 Semx P00-P17 `phase_workflow.py`。
- 保留并适配 `contract-first-delivery`、`dashboard-governance`、`doc-system-kb-builder`、`exploration-dashboard-synthesizer`、`llm-artifact-evaluator`、`pdi`。
- 从 strategy 审计中只迁移重新冻结的通用 contract 与 read model：优先覆盖 SGC、ERBE、Human-AI、Acceptance、BDD、Goal Effect、KB Promotion、Semantic Surface，以及 authority/evidence/claim/repair-loop/change-impact 的通用不变量；禁止迁入 P00-P17、P05/M1、Runtime Kernel、SAG ontology、G1-G10、Semx Session 编号或 runner 路径。

### S-004：KB、Dashboard 与目录整理

- `kb/` 保持 canonical truth 根；新增 project profile、Dashboard contract、SGC、ERBE、Goal Effect、Human-AI、Semantic Surface、BDD 和 KB promotion 的治理真源及中文阅读面。
- `kb/docs-system/v1/` 只保留通用 Doc-as-Data、演化协议和模板；删除 Semx compiler/M1/USL/P00-P17 产品内容。
- 保留并改造 `session_registry.py`、`generate_dashboard_kg.py`；删除 legacy S-485 migrate 路径、Semx panorama、`mermaidGen.py` 和 KYM/TCO visualization/provider 数据。
- 删除 `.DS_Store`、`__pycache__` 和临时派生数据，并补 `.gitignore`。
- 按逐文件 strategy inventory 清理 Semx-specific 阅读面、产品 runtime target、旧翻译与图片；对每个删除项写明由哪个通用合同吸收其少量治理价值，避免把“删除产品实现”误写成“原文件毫无价值”。

### S-005：集成验收、独立 Validation 与 Semantic Review

- 使用冻结后的 repo-local acceptance runner 对 source provenance、project profile、Skill contracts、schema、ERBE trusted RED/GREEN、Goal/lane/context、workflow registry、Dashboard registry/DKG、身份隔离、绝对路径和 closeout-language 执行正负例验收。
- 独立 Validation 从 durable inputs 重算实际候选，不采信 producer terminal status；验证范围覆盖 S-002 至 S-004 产物、原始设计摘要、Dashboard/KB authority、完整 tracked/untracked diff 和所有未关闭 blocker。
- Semantic Reviewer 同时给出 `Design Freeze Validity` 与 `Implementation Entry Readiness`，覆盖通用核心/profile 边界、truth placement、状态词压缩误读、future-agent misuse 和跨仓库提取的 claim ceiling。
- 只有 current contract 的 blocker 清零且 registry、DKG、schema、身份与语言门禁全部通过，才可将候选交给 S-006；一般强化建议保留为 follow-on，不冒充当前 blocker。
- 验证 56/56 strategy 文件覆盖、docs→canonical JSON mapping、source digest/provenance、目标链接、身份隔离与负例；显式拒绝 observation→truth、diff→resolution、advisory→action、request→decision、recorded→approved、approved/authorized→executed 等 forbidden collapse。

### S-006：最终 closeout、覆盖审计与 post-closeout reconciliation

- 形成中文 Goal closeout、逐项 OPCM、Scope Delta audit、Evidence Completeness Matrix、KB/Dashboard review、Contract Delta Scan 和 Loop completion scan。
- 将最终 Session/Stage Plan/Big Idea 状态、Artifacts Index、KB truth 和 closeout 对齐；任何 Dashboard registry surface 变化后重跑 `reconcile --check` 与 `validate`，需要 DKG 时从显式输出路径重建并做 focused gate。
- 独立 post-closeout reconciliation 必须读取实际 closeout、最终 Dashboard/KB 状态与最终 diff，提供唯一且无冲突的 passing verdict；关闭前 Validation 不得替代该证据。
- 仅当 `MH-01..MH-11`、所有 Session exit criteria 与 Goal completion rule 全部满足时才允许写 `Goal complete`；最终主张仍受 Goal claim ceiling 限制，不包含产品实现、发布或普遍跨仓库成熟性。

## Strategy 来源迁移裁决规则

- `migrate_after_refreeze`：仅用于接近通用合同的候选；S-002 仍需追溯 canonical JSON、去 Semx 身份、冻结新 schema/claim ceiling 并 re-RED，不能原样复制。
- `adapt_extract`：只抽取稳定治理不变量并在 SGE ontology 下重写；源文档、runner、schema 和产品状态不自动迁移。
- `reference_only`：只进入 provenance、Read Manifest 或反例设计，不进入新 KB truth 或默认 Skill runtime。
- `remove`：从目标仓库排除；若含少量通用安全原则，inventory 必须指出由哪个通用合同吸收。
- 本轮逐文件初筛见 [Strategy Source Inventory](SP001_StrategySourceMigration_Inventory.md)。该 inventory 是 S-002 输入，不是迁移批准、canonical truth 或实现证据。

## 目标目录与保留/删除边界

| 目标路径 | 处理 | 所属 Session | 计划内容与边界 |
| --- | --- | --- | --- |
| `.codex/skills/sge-governed-checkpoints/` | 新建通用核心 | S-002/S-003 | 放置 `SKILL.md`、references、schemas、scripts 与 Skill 自带通用 library；不得含 audio 产品 runtime 或 Semx P00-P17 事实。 |
| `.codex/skills/sge-governed-checkpoints/config/` | 新建项目配置入口 | S-002 | 保存 audio-transcriptor profile 的可执行绑定或其 canonical pointer；不得复制 KB truth 形成第二真源。 |
| `kb/data/strategy/` | 保留并新增 canonical JSON | S-002/S-004 | 保存 project profile、Dashboard contract、SGC、ERBE、Goal Effect、Human-AI、Semantic Surface、BDD 与 KB promotion 稳定真源。 |
| `kb/docs/strategy/` | 新增中文阅读面 | S-004 | 从 canonical JSON 生成或可追溯维护；不得反向成为机器 authority。 |
| `kb/docs-system/v1/` | 保留通用部分、删除项目污染 | S-004 | 仅保留通用 Doc-as-Data、演化协议和模板；移除 Semx compiler/M1/USL/P00-P17 产品内容。 |
| `kb/bm-doc/audio-transcriptor-skill_design_v1.0.md` | 字节保留 | 全程 | 唯一产品设计 authority；治理迁移不得修改、冻结或实现它。 |
| `Dashboard/` | 保留 execution memory 并适配 | S-001/S-004/S-006 | 保留 BI/SP/Session/Decision/closeout 表面和中文 evidence links；不得提升为 canonical truth。 |
| `Dashboard/tools/session_registry.py` | 保留并去项目化 | S-004 | 保留日常 check/validate/reconcile；移除 S-485 legacy bootstrap/migrate 专用路径，不允许 reconcile 猜测 identity。 |
| `Dashboard/tools/generate_dashboard_kg.py` | 保留并适配 | S-004/S-005 | 使用明确输入和显式输出路径生成 DKG projection；不得把 DKG 反向作为 registry 或 KB 真源。 |
| `Dashboard/tools/visualization/`、Semx panorama、KYM/TCO/provider 样例 | 删除或由通用入口替代 | S-004 | 逐项记录删除理由与替代机制，不作为本项目样例库保留。 |
| `tests/governance/` 或冻结合同指定的等价受版本控制路径 | 新建治理验收面 | S-002/S-003/S-005 | 保存 Contract/Cases、正负 fixtures、durable readable cards 与 acceptance runner；临时 report 不算完成证据。 |
| `.gitignore` | 补充 | S-004 | 排除 `.DS_Store`、`__pycache__` 与明确的临时派生数据，不得忽略 canonical evidence。 |

上述目标路径是迁移合同，不表示 S-001 已创建这些目录；实际精确路径若在 S-002 Design Freeze 中调整，必须通过 Contract Patch、Scope Delta 判定和 re-RED 后更新本计划。

## 接口变化合同

| 源接口 / 当前行为 | 目标接口 / 行为 | 变化语义 | Session | 验收证据 |
| --- | --- | --- | --- | --- |
| `.codex/skills/semx-governed-checkpoints/` 与 Semx 项目事实绑定 | `.codex/skills/sge-governed-checkpoints/` 通用核心 + audio-transcriptor profile | `adapt/replace`；稳定治理机制保留，项目身份和产品事实外置 | S-002/S-003 | source manifest、profile schema 正反例、全模式 checklist 与身份扫描 |
| 脚本内硬编码 `semx-kb/`、Semx Dashboard/phase 路径 | profile 提供 `kb_root=kb`、`dashboard_root=Dashboard` 和 authority pointers | `replace`；缺字段、错误 repo 或越界路径必须 fail closed | S-002/S-003 | profile Contract/Cases、negative fixtures、context/lane validator 输出 |
| `phase_workflow.py --phase P00..P17` | `workflow_contract.py` + 通用 workflow registry | `replace/remove`；保留阶段合同机制，不兼容保留 Semx phase facts | S-003 | registry schema、合法/未知 workflow 正负例、无 P00-P17 identity 扫描 |
| Semx repo package 中的 ERBE/Goal Effect/governance integration | Skill 自带 `lib/sge_governance/` | `move/adapt`；只服务治理工具，不进入 audio 产品 runtime | S-003 | import isolation、trusted RED/GREEN、Goal Effect 与 clean-room tests |
| `context_bootstrap.py`、`context_state.py`、`goal_patch.py`、`lane_task_card.py` 的 Semx 路径假设 | 同名通用 CLI，由 profile/显式 repo 参数解析 authority | `adapt`；尽量保持 CLI 形状，语义不兼容项必须在 S-002 冻结 | S-002/S-003 | validate/render/audit/resolve 正负例、expected digest 与路径逃逸失败指纹 |
| registry 的 S-485 `migrate` 与 Semx archive provenance | 仅保留日常 check/validate/reconcile 和受控 locator migration（若合同批准） | `remove`；S-485 bootstrap 不提供兼容入口，archive manifest 必须由新工具确定性重建 | S-004 | 6-record bootstrap 后的新 profile fixtures、unknown archive/identity negative tests、无 legacy provenance 扫描 |
| Dashboard KG 对 Semx `Quality_Metrics.md` 和旧 panorama 的隐式依赖 | profile/contract 明示输入的通用 DKG 生成 | `replace`；缺输入时给稳定 failure fingerprint，不生成虚假 PASS | S-004/S-005 | 显式路径生成、缺输入负例、focused registry/DKG gate 与 durable output |
| `AGENTS.md` 的 Semx 名称、KB 根和固定 phase 命令 | audio-transcriptor repo hard gates + `sge-governed-checkpoints` 入口 | `replace`；保留治理强度与 truth split，删除项目无关事实 | S-004 | hard-gate audit、命令可执行性、身份/绝对路径扫描、中文说明检查 |
| Dashboard closeout/Validation 仅引用内部摘要或裸 digest | 人类正文使用可点击源文件链接，机器摘要留在 card/manifest/report | `adapt`；链接与 digest 分工明确 | S-004/S-006 | link checker、closeout-language、最终 Evidence Completeness Matrix |

不提供对 Semx 专用命令、P00-P17、KYM/TCO 数据或 S-485 migrate 的兼容承诺；需要保留的通用 CLI 形状由 S-002 frozen Contract/Cases 决定，Builder 不得自行扩大。

## Skill 与实践迁移裁决

| 处理 | 对象 | 原因 |
| --- | --- | --- |
| 保留并适配 | contract-first、dashboard-governance、doc-system-kb-builder、exploration-dashboard-synthesizer、llm-artifact-evaluator、pdi | 对合同、KB、Dashboard、结构化 artifact 和缺陷固化有直接价值。 |
| 建立通用核心 | sge-governed-checkpoints | 承载 Intake、Context、SGC、ERBE、Goal、lane、Validation、Semantic、closeout、continuation。 |
| 不迁入 | build-kym、build-tco-coverage、kym-tco-governed-checkpoints | 属于 KYM/TCO 产品域，无本项目 authority 或验收需求。 |
| 本 Goal 不迁入 | 全局 transcribe Skill | 属于未来产品实现，避免污染治理迁移范围。 |
| 替换 | Semx phase runner / phase acceptance posture | 机制保留，Semx phase facts 由通用 workflow registry 替代。 |
| 删除 | Semx panorama、KYM/TCO visualization、provider trial 样例、legacy migrate | 固定 Semx 历史，迁入会制造身份污染或危险入口。 |

## 验证与验收

- 来源：源 revision 干净；manifest 中每个复制文件有路径、摘要、裁决；原始设计摘要不变。
- 身份：可执行、schema、AGENTS、KB、Dashboard authority 表面无未批准的 Semx/KYM/TCO/P00-P17/runtime 身份。
- Skill：profile 正反例、所有 checklist modes、context validate/render、Goal patch/resolve、lane validate/render/audit、ERBE trusted RED/GREEN、Goal Effect、closeout-language 均通过。
- Dashboard：registry check/validate 通过；DKG 用显式路径重建并保持 execution-memory claim ceiling。
- KB：治理 JSON 通过 schema；Markdown 可从 JSON 重建；source design、canonical truth、Dashboard memory 不混淆。
- 仓库：治理 acceptance runner、负例、绝对路径检查、漂移检查和最终 Git diff 审计通过；不调用网络、Provider 或真实音频。
- 独立复核：Design、Builder、Validation、Closure lanes 均有 card/log；Semantic Reviewer 覆盖通用化和 truth placement。

### 逐项验收矩阵

| ID | Session / 对象 | 正例与负例 / gate | 命令或 authority | 预期结果 | Durable evidence | Claim ceiling |
| --- | --- | --- | --- | --- | --- | --- |
| MH-01 | S-001 Git seed | seed 中原始设计可通过 Git locator 恢复；当前 repo 不恢复产品文件 | Git seed、[历史设计 locator](Tombstones/Removed_Audio_Transcriptor_Design.md) | seed 可恢复；当时摘要记录保留，当前不主张字节相等 | S-001 Validation/closeout 与 S-015 修正说明 | 只证明整理前状态可恢复 |
| MH-02 | S-002 source provenance | 每个复制对象均有 source path、revision/digest、裁决；脏源或缺裁决失败 | source manifest schema + frozen source revision | manifest 全量、源干净、无未登记复制 | 受版本控制 source manifest、Validation Review | 不证明目标实现正确 |
| MH-03 | S-002 core/profile | 合法 profile 通过；缺 root、错 project_id、路径逃逸和 Semx identity 失败 | frozen ERBE Contract/Cases、profile schema validator | trusted RED/GREEN 使用同一 case identity，profile fail closed | Contract/Cases、RED/GREEN report、pre-Builder Semantic Review | 只证明设计冻结与最小入口可实现 |
| MH-04 | S-003 Skills/scripts/gates | 所有 checklist modes、context、Goal、lane、workflow 正例通过；未知 mode/digest drift/非法路径失败 | repo-local Skill 命令与治理 acceptance runner | 目标接口通过，删除接口无静默 fallback | tests、readable cards、runner report、Builder/Validation logs | 只证明 repo-local 治理工具合同 |
| MH-05 | S-004 truth/authority | KB JSON/schema/阅读面、Dashboard memory、AGENTS/tool paths 对齐；跨层冒充失败 | KB schemas、AGENTS、Dashboard Rules/registry | truth placement 唯一且路径可执行 | KB validation、truth-placement review、final diff | 不证明产品设计或 runtime |
| MH-06 | S-004 污染清除 | Semx/KYM/TCO/P00-P17/runtime/绝对源路径扫描；每个删除项有理由/替代 | source manifest、删除与替代清单、身份扫描 gate | 未批准身份零残留；legacy migrate 不可调用 | 删除清单、扫描报告、registry negative tests | 只证明已定义扫描面的身份隔离 |
| MH-07 | 全程产品边界 | seed/current 摘要一致；治理 runner 不导入 audio runtime | 原始设计 authority、Git diff、import isolation tests | 原始设计不变且无产品实现面 | 每轮 Validation 与最终 reconciliation | 不证明设计冻结、产品可用或质量 |
| MH-08 | S-005 集成验收 | schema、ERBE、Goal/lane/context、registry、DKG、语言、绝对路径的正负例全部通过 | 维护中的治理 acceptance runner；registry `reconcile --check`/`validate` | runner 绿色且指定负例按 frozen fingerprint 失败 | 受版本控制 reports/readable cards、registry/DKG outputs | 本地结构与治理验收，不含外部成熟性 |
| MH-09 | 全程 lane 时序 | 每个 non-trivial lane 有有效 card/digest/log；Builder 不写 frozen contract；独立 reviewer 重算 | lane card validate/render/audit、Agent Logs、Semantic verdict | Design→Builder→Validation→Closure 时序可定位，无 producer 自批 | cards、prompts、logs、Validation/Semantic artifacts | 只证明记录到的执行拓扑 |
| MH-10 | S-006 closeout/reconciliation | OPCM 逐项覆盖 MH/AC；Scope Delta、links、语言、最终状态/diff 一致；缺证据不得完成 | Goal completion rule、closeout-language、registry、final diff | 唯一 passing post-closeout verdict 且无未吸收 must-have | 中文 closeout、Evidence Completeness Matrix、post-closeout reconciliation | 最多为 Goal 的 repo-local bounded claim |
| IF-01 | core/profile 与路径接口 | 对接口变化表逐行建立兼容/替代/删除 case；旧 Semx 专用入口不得静默成功 | S-002 Contract/Cases + S-005 runner | 每行结果与变化语义一致 | interface acceptance report 与 source links | 不承诺未列出的向后兼容 |
| IF-02 | registry/DKG 接口 | 新 profile 下 check/validate/generate 通过；S-485 migrate、缺 DKG 输入、unknown archive 按合同失败 | Dashboard tools + frozen failure fingerprints | 无 identity 猜测、无虚假 projection | registry/DKG reports、negative fixtures | 只证明 Dashboard 投影工具 |
| IF-03 | final authority/closeout 接口 | 人类证据链接可点击、machine digest 可重算；最终状态先后顺序无冲突 | link checker、closeout-language、post-closeout Validation | closeout、KB/Dashboard 与 final diff 同步 | final closeout 和 reconciliation | 不扩展到发布或产品能力 |

## 固定边界

- 不发布、不写全局、不推送远端。
- 不保留 Semx 历史样例库；通用 fixture 必须重新去项目化。
- 后续产品合同、CLI 和转写 runtime 必须另开受治理 Goal/Session。
