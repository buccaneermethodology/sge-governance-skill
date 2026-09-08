# SP-001 可复用 SGE Governance 迁移与质量恢复 Loop Goal

## 文档身份

- Goal ID：`SP-001`
- Goal 类型：多 Session、连续执行的治理迁移 Loop Goal
- 当前状态：历史迁移切片已落地；质量恢复正在执行
- 当前入口：`S-012`
- 原始授权：用户要求先设计 Loop Goal，并将 Loop Goal 与已确认迁移计划放入 Dashboard；随后明确要求实施该落库计划。
- 当前 Goal Patch：[SP001_QualityRecovery_GoalPatch.md](SP001_QualityRecovery_GoalPatch.md)，新增 MH-12..MH-15 与 S-012..S-015 恢复 DAG。
- 最大主张：`本仓库的 repo-local SGE Governance 框架已完成有界迁移与质量恢复，并通过本地结构、治理、引用和工具链验收`。

## 中文任务解释

本 Goal 要把历史迁移形成的治理框架整理为独立的 `sge-governance-skill`：active authority 不依赖 Semx 或其他产品身份，canonical KB、Dashboard、引用图和验收工具链可确定性验证，并为未来独立公共候选建立前置质量。历史 audio-transcriptor/Semx 材料只保留为 provenance，不是当前仓库身份。

S-001..S-006 是历史迁移证据；本轮通过 S-012..S-015 修复审计发现的 active/public 污染、证据缺口、引用断链和工具链假绿问题。公共发布仍属于 SP-002，不能由本 Goal 推导。

## Read Manifest

### 已读

- [历史产品设计 locator](Tombstones/Removed_Audio_Transcriptor_Design.md)：迁移前唯一产品设计来源；当前仓库已删除其内容，本 Goal 只保留 provenance，不再主张当前字节存在或相等。
- [仓库硬门](../../../AGENTS.md)：当前复制自 semx-cli，迁移完成前仍包含待适配项目身份。
- [Dashboard Rules](../../Rules.md)、[Dashboard Methodology](../../Methodology.md)、[Dashboard README](../../README.md)：当前 Dashboard 表结构、Status vocabulary 和 registry 操作边界。
- semx-cli `main@19e967a782e2e95d24475770bc234d86ad7c583e` 下的 `.codex/skills/semx-governed-checkpoints/`：本轮 bootstrap checkpoint 与未来迁移来源。
- semx-cli 同一 revision 下的 `semx-kb/docs/strategy/` 全部 56 个文件表面：本轮仅完成逐文件初筛；真正迁移稳定 truth 时必须追溯对应 `semx-kb/data/strategy/*.json`，不能把 Markdown 阅读面当 canonical authority。
- 本 Goal 的 [迁移计划](SP001_SGEGovernanceMigration_Plan.md) 与 [Context Bootstrap](SP001_SGEGovernanceMigration_ContextBootstrap.json)。

### 未读或刻意跳过

- semx-cli 历史 Dashboard artifacts、provider trials、P00-P17 runtime evidence：属于被排除的 Semx 产品史，不是本 Goal 的迁移 authority。
- 全局 `transcribe` Skill：属于未来产品实现来源，本 Goal 明确不实施转写 runtime。

## Mission

将当前 Semx 空框架整理为以 `sge-governed-checkpoints` 通用核心和 audio-transcriptor 项目配置组成的、可执行、可验证、可跨仓库提取的 SGE 治理工程；删除不适用于本项目的 Semx/KYM/TCO/runtime 历史与工具，并以独立 Validation、Semantic Review、registry、KB/Dashboard 和最终 diff 证明迁移结果。该 Goal 不实现任何音频转写产品能力。

## 原始 Must-Have Ledger

| ID | 原始要求 | 可观察验收判定 | Owner / Lane | 状态 |
| --- | --- | --- | --- | --- |
| MH-01 | 先建立当前目录的 Git 种子基线，保留整理前状态。 | 存在整理前 root commit，原始设计可从该 commit 读取。 | S-001 / Orchestrator | S-001 已落地，Goal 仍未终止 |
| MH-02 | 固定 semx-cli 源 revision 和所有复制 Skill 的 provenance。 | source manifest 记录 revision、路径、摘要和迁移裁决。 | S-002 / Design+Builder | 未启动 |
| MH-03 | 建立通用 `sge-governed-checkpoints` 与 audio-transcriptor project profile。 | Skill、profile schema、正反例和验证命令存在且通过。 | S-002 | 未启动 |
| MH-04 | 迁移适用的 Governance Skills、schemas、scripts 和 acceptance gates。 | 迁移清单逐项落地并通过本地 gates。 | S-003 | 未启动 |
| MH-05 | 将 `kb/`、Dashboard、AGENTS 和工具调整为新项目 truth/authority 边界。 | authority 路径自洽，KB/Dashboard 分层测试通过。 | S-004 | 未启动 |
| MH-06 | 显式删除无意义的 Semx/KYM/TCO/P00-P17/runtime 历史实践并记录理由。 | 删除清单和替代机制可定位，身份扫描通过。 | S-004 | 未启动 |
| MH-07 | 保持原始产品设计文件字节不变，不冒充产品设计冻结或 runtime 实现。 | 最终摘要等于种子基线；closeout 明确产品非目标。 | 全程 / Validation | 未启动 |
| MH-08 | 完成身份、schema、ERBE、Goal、lane、context、registry、DKG、语言门禁验收。 | 维护中的 acceptance runner 全绿且证据持久化。 | S-005 / Validation | 未启动 |
| MH-09 | 保留 Design、Builder、独立 Validation、Closure 与触发式 Semantic Reviewer 时序证据。 | lane card、task identity、Agent Log 和 verdict 可定位。 | 全程 / Orchestrator | S-001 只完成规划落库证据 |
| MH-10 | 形成中文 closeout、OPCM、Scope Delta、KB/Dashboard review 和 post-closeout reconciliation。 | S-006 最终 artifact 覆盖实际最终状态和 diff。 | S-006 / Closure+Validation | 未启动 |
| MH-11 | 逐一审计 semx-cli `semx-kb/docs/strategy/` 全部表面并追溯 canonical JSON；只迁移经去项目化改造且有 provenance 的通用策略。 | 56 个文件逐行有 `adapt_extract`、`reference_only`、`remove` 或有界 `migrate_after_refreeze` 裁决；S-002 完成 canonical mapping，S-004 排除 Semx/KYM/TCO/P00-P17/runtime 产品 truth，S-005 验证身份、链接、schema 与 forbidden collapse。 | S-002..S-006 / Design+Builder+Validation | 历史初筛和有界迁移证据已落地；S-013 对实际缺失的 semantic-governance truth 补做 canonical 复核 |
| MH-12 | 清除 active/public 表面的旧项目身份、绝对来源路径、legacy migrate 入口和 registry 漂移。 | active allowlist 扫描无未批准身份；registry check/validate 通过；历史 provenance 仍可定位。 | S-012 / Builder+Validation | Doing |
| MH-13 | 恢复 Human-AI、Semantic Surface、KB Promotion 三类通用 semantic-governance canonical truth。 | canonical JSON 存在；来源逐节裁决；Markdown 由 renderer 生成且 `--check` 通过。 | S-013 / Design+Builder+Semantic | To do |
| MH-14 | 修复缺失引用、历史 locator、KB renderer、DKG 和标准 doctor/acceptance 入口。 | 引用检查、KB check、DKG、非零测试发现、doctor 正负例通过。 | S-014 / Builder+Validation | To do |
| MH-15 | 用当前硬门重建全量 OPCM、Scope Delta、独立 Validation、Semantic Review、中文 closeout 与 post-closeout reconciliation。 | 每个原始 MH/AC 均有证据行；最终 verdict 覆盖实际 closeout、最终 Dashboard/KB 和完整 diff。 | S-015 / Validation+Semantic+Closure | To do |

## S-001 可观察验收判定

| ID | 可观察判定 | 验收证据 | 不通过条件 |
| --- | --- | --- | --- |
| S001-AC-01 | S-001 的规划合同已持久化：Final Loop Goal、迁移计划、Context Bootstrap 与 Dashboard entry 均可从仓库内定位，并明确本次只落库规划、不启动 S-002。 | [Final Loop Goal](SP001_SGEGovernanceMigration_LoopGoal.md)、[迁移计划](SP001_SGEGovernanceMigration_Plan.md)、[Context Bootstrap](SP001_SGEGovernanceMigration_ContextBootstrap.json) 及 `Dashboard/` 父面与 Session entry。 | 任一必需 artifact 缺失、链接不可定位，或文本把 S-001 落库写成 S-002/治理迁移已经启动。 |
| S001-AC-02 | Dashboard 控制面使用规定四态 Status vocabulary，`SP-001/S-001..S-006` 的 index 定位链接均能解析到 `Sessions.md` 中同名 anchor，且 registry `reconcile --check` 与 `validate` 均返回零。 | [Dashboard Rules](../../Rules.md)、[Session Index](../../Session_Index.md)、[Sessions](../../Sessions.md) 与两项 registry 命令输出。 | 出现四态之外的 Status、缺失或错配 anchor、identity/row/unknown archive 错误，或任一 registry 命令非零。 |
| S001-AC-03 | S-001 关闭证据保持边界：整理前 Git seed 可恢复，原始产品设计字节不变，Design/Builder/独立 Validation/Closure 时序可定位，中文 closeout 与最终 diff 只支持“S-001 规划落库完成；SP-001 迁移未启动”。 | Git seed、原始设计摘要、lane card/Agent Log、S-001 closeout、独立 Validation Review、closeout-language 结果及最终 tracked/untracked diff。 | 原始设计摘要变化、缺少独立 Validation 或 closeout-language 通过证据、证据未覆盖最终 diff，或出现产品实现、S-002 Builder、Goal complete 等越界主张。 |

## 非目标

- 不实现 `audio-transcript` CLI、FFmpeg、Whisper、clean transcript、metadata、cache 或真实音频测试。
- 不发布公共 Skill，不同步到全局 Skills，不推送远端。
- 不复制 Semx Dashboard 历史、provider evidence、P00-P17 产品合同或 KYM/TCO 数据作为样例库。
- 不声称治理框架通过测试就证明 audio-transcriptor 产品可用。

## Session DAG

| Session | 主题 | 依赖 | 主要输出 | 退出条件 |
| --- | --- | --- | --- | --- |
| S-001 | Git 种子基线、Loop Goal 与迁移计划落库 | 无 | Goal、Plan、Context、Dashboard entry、S-001 closeout/validation | 只证明规划落库，registry 与独立 Validation 通过 |
| S-002 | 来源清单、project profile、ERBE 合同与通用 SGE 核心冻结 | S-001 | 全量 source manifest、56 个 strategy docs→canonical JSON mapping、profile、frozen contract/cases/RED | 同 identity contract gates 通过，且每个 strategy 表面的 authority/canonical mapping 已冻结 |
| S-003 | Governance Skills、schemas、scripts、通用 strategy contracts/read models 和 workflow registry 迁移 | S-002 | repo-local Skills、经重新冻结的通用 strategy truth/read models 与 deterministic tooling | Skill/interface/strategy provenance acceptance 通过 |
| S-004 | KB、AGENTS、Dashboard tools 整理及污染清除 | S-003 | 新项目 authority surfaces、Semx/runtime strategy 删除与替代清单 | 身份、路径、KB/Dashboard gates 通过，排除项不残留为 authority |
| S-005 | 集成验收、独立 Validation 与 Semantic Review | S-004 | acceptance evidence、56 文件覆盖复核、Validation、Semantic Review | blocker 清零或明确终止；docs/read-model 与 canonical JSON authority 未折叠 |
| S-006 | closeout、覆盖审计与最终对账 | S-005 | Closeout、MH-11 OPCM、Scope Delta、post-closeout reconciliation | Goal completion rule 全部满足 |
| S-012 | active/public 身份与 registry 修复 | S-006 | 有效执行合同、registry 修复、active identity 清理与独立 Validation | MH-12 predicates 通过；不伪造历史时序 |
| S-013 | semantic-governance canonical 恢复 | S-012 | 三类 canonical JSON、来源裁决、派生 Markdown 与 Semantic Review | MH-13 predicates 与 renderer check 通过 |
| S-014 | 引用与验收工具链修复 | S-013 | locator 修复、KB/DKG、doctor 与正负例 | MH-14 predicates 通过且测试发现非零 |
| S-015 | SP-001 最终集成与关闭 | S-014 | OPCM、Scope Delta、Validation、Semantic、closeout、post-closeout | MH-01..MH-15 completion rule 全部满足 |

历史依赖为 `S-001 → S-002 → S-003 → S-004 → S-005 → S-006`；当前恢复依赖为 `S-012 → S-013 → S-014 → S-015`。Builder 不得修改冻结的 Contract/Cases/RED/claim ceiling；需要变更时走 Contract Patch、Scope Delta 与 re-RED。

## Governance Workflow

- ERBE applicability：`required`，因为本 Goal 改变治理终态、authority routing、acceptance 和 write boundaries。
- Multi-Agent：默认启用 Design、Builder、Validation、Closure；通用化和语义治理边界触发 Semantic Reviewer。
- 所有 delegation 必须消费验证通过的 `lane_task_card_v1`，`fork_context=false`。
- Validation 必须同时检查实际实现和本 Ledger，不得只检查修订后的局部设计。
- Dashboard 记录执行记忆；稳定治理 truth 迁入 `kb/data/`；派生 DKG/HTML 不成为 authority。

## Loop Continuation Contract

- S-001 落库不启动迁移；落库后 `SP-001=To do`，`Current Entry=S-002`。
- 用户后续明确启动 `SP-001` 后，Session closeout 不是停止点。每次 closeout 必须记录 `goal_terminal`、`next_session`、`next_session_ready`、`human_decision_required`。
- 当 `goal_terminal=false`、下一 Session ready 且不需要人类决定时，Orchestrator 必须在同一执行回合进入下一 Session。
- 只允许因 Goal completion、用户暂停、真正的人类 authority、未批准 Scope Delta、外部发布/全局写入、工具中断或同一恢复条件连续失败三次而暂停。
- 删除 must-have、降低验收标准或加入产品实现，必须先取得人类批准并记录 Scope Delta。

## Completion Rule

只有同时满足以下条件才允许写 `Goal complete`：

1. MH-01..MH-15 均有逐项、可点击且与最终 diff 对齐的证据；
2. 所有相关 Session registry check/validate 通过；
3. 原始设计摘要与种子基线一致；
4. 无未批准的 Semx 项目身份或绝对源路径残留；
5. SGE profile、Skill contracts、ERBE、Goal/lane/context 工具、KB renderer、引用检查、非零测试 doctor 和 Dashboard DKG 验收通过；
6. 独立 Validation 与 Semantic Review 覆盖实际 closeout、最终 KB/Dashboard 和最终 diff；
7. closeout-language gate 明确通过；
8. 没有未落地且未经批准延期的原始 must-have；S-004/S-005 历史证据缺口已由当前 final-state reconciliation 明确吸收；
9. 公共候选、验证、批准、Git、发布和生产状态未发生 forbidden collapse。

## Termination Conditions

- `complete`：Completion Rule 全部满足。
- `paused_by_user`：用户明确暂停或停止。
- `human_authority_required`：需要未提供的 Scope Delta、外部发布、全局写入或 destructive decision。
- `tool_interruption`：关键工具或环境中断且不能在 scope 内恢复。
- `recovery_ceiling`：同一恢复条件连续失败三次。

## Validation Handoff 要求

Validation 必须读取用户原始请求、本 Goal、迁移计划、context packet、所有 Session closeout、最终 KB/Dashboard、最终 tracked/untracked diff、测试和 gate 证据；必须分别列出 blocking、non-blocking、Scope Delta、原始目标覆盖与 verdict。

## Semantic Reviewer 触发与输出

通用 SGE core、project profile、truth placement、gate strictness 或跨 repo 可移植性发生变化时触发。必须给出：

- `Design Freeze Validity`：设计冻结是否保持 authority、非目标和 claim ceiling。
- `Implementation Entry Readiness`：下一个 Builder 是否能从当前 artifact 安全开始最小实现。

## CG 状态

`CG skipped: no CG input provided`

## 允许与禁止的 Closeout 用语

允许：

- “S-001 规划落库完成；SP-001 迁移未启动。”
- “治理迁移在本地结构与治理验收范围内完成。”（仅 Completion Rule 全部满足后）

禁止：

- “audio-transcriptor 已实现/可用/生产就绪。”
- “完整 SGE 已被普遍证明可跨任意 repo 使用。”
- 用单个 Session `Done` 代替 `Goal complete`。
