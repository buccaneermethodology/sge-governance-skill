# UAT-S001 最小文档示例设计

## 任务解释与接入判断

本例让 Builder 在 fresh target 写一份能看懂、能按真实路径操作的中文项目说明，并保留 Design → Builder → Closure draft → 独立 Validation → Closure final → 独立 reconciliation 的证据。它不实现产品，也不判断外层 S-026 是否通过。

Intake verdict：execute（按既定范围执行设计）。任务来源为[原始 Goal](Goal.md)及[Design lane card](DesignCard.json)，目标项目的[AGENTS](../../AGENTS.md)和[profile](../../kb/data/strategy/profile.json)提供 authority。Design 只写本文件与[设计日志](DesignLog.md)。风险是把文档存在、门禁结构通过或本例完成，误写成完整 UAT 或发布完成。未新增审批要求；未收到外部 CG 输入，`CG skipped: no CG input provided`。

[Context](Context.json) 已通过结构校验。但其 `change_impact.dashboard_state=false` 与 M3/M5 的实际 Dashboard 写入影响不一致：Orchestrator 须在 Builder 下发前修正为真实影响、重校验并重建受影响卡摘要。本设计记录该入口问题，不修改冻结 Goal 或卡引用源。

## 已读与未读清单

| 来源 | 读取状态与用途 |
| --- | --- |
| [Goal](Goal.md)、[DesignCard](DesignCard.json)、[Context](Context.json) | 已读全文；保存 M1–M5、写入边界、拓扑与完成条件。卡摘要校验通过。 |
| [目标 AGENTS](../../AGENTS.md)、[profile](../../kb/data/strategy/profile.json) | 已读全文；实际项目为 `target`，canonical truth 是 `kb/data/`，execution memory 是 `Dashboard/`；profile 只允许本仓治理骨架主张。 |
| [已安装 Skill](../../.codex/skills/sge-governed-checkpoints/SKILL.md) | 已读；输出曾截断，随后分段补读相关工作流。未把摘要校验等同于语义验证。 |
| [checklists](../../.codex/skills/sge-governed-checkpoints/references/checklists.md) | 已读 SGC、Intake、Context、Design、Goal Conformance、Validation Handoff 相关段；其余段不属于本次设计的额外必读。 |
| [Sessions](../Sessions.md)、[Current State](../Current_State.md) | 已读；UAT-S001 当前执行中，设计待执行。 |
| [公开 companion SGC JSON](/tmp/sp004-s026-01a0744b/candidate/kb/data/strategy/strategy_sgc_structural_contract_v1.json) | 目标未安装此 KB；仅作为公开只读参考，读取 claim levels、forbidden collapses、SI-1..SI-6、completion rule 及适用边界。未将 candidate KB 提升为目标项目 truth。 |
| 公开 README、Quick Start、新手指南 | 本 Design lane 未重新读取；公开入口与 lifecycle 实验由主任务并行采集，不把主任务阅读声称为本人阅读。 |
| 源仓 Dashboard、私有历史、memory 文件、来源任务聊天 | 未读取，非本 lane 的证据输入。系统注入上下文可能含仓库规则，因此不声称完全无项目上下文。 |
| PROJECT_NOTE、Builder Handoff、Closeout、独立 Review 与 Reconciliation | 设计时尚未产生；必须由下游读取实际文件，不能以本设计代替验证。 |

## 最小内容与实现边界

`PROJECT_NOTE.md` 至少有三个中文二级标题：`项目目的`、`使用步骤`、`边界`。项目目的说明本目录是 repo-local governance skeleton 的本地说明示例。使用步骤给出从 target 根目录执行的实际命令，至少读取 `AGENTS.md` 与 `kb/data/strategy/profile.json`，解释预期看到的 canonical truth / execution memory 分工；可指向当前 Goal 和 Session。文档中用可点击链接指向目标 AGENTS 与 profile，不能换成源仓路径或虚构入口。边界明确本例没有产品实现、provider、release、远端或 semantic promotion；本地文档验收与外层 UAT 结论独立。

本例不增加模块、API、schema、测试框架或运行时。Builder 的最小切片为：读取设计与 authority → 写说明 → 检查路径和内容 → 记录真实命令与 actual files → 保存 Handoff。新维护性测试/BDD 卡不适用，因为没有修改已有行为门禁；负例是本例验收证据，不能称 ERBE 可信 RED。

| Owner / 时序 | 预期文件与职责 |
| --- | --- |
| Design；Builder 前 | `Dashboard/Artifacts/Design.md`、`DesignLog.md`。设计保存完成后可供 Builder 消费；入口 Context 修正仍须先完成。 |
| Builder；Design 后 | `PROJECT_NOTE.md`、`Dashboard/Artifacts/Handoff.md`、Builder 实际日志（建议 `BuilderLog.md`）；更新 `Dashboard/Sessions.md`、`Current_State.md` 为待独立验证并引用证据。具体写入以已校验 Builder card 为准。 |
| Closure；Builder 后 | `Dashboard/Artifacts/Closeout.md` 草稿与最终稿；实际 lane 日志；Sessions/Current_State 引用最终 closeout。 |
| 独立 Validation；草稿后 | `Dashboard/Artifacts/Review.md`，保存 reviewer/source、Read Manifest、正负例、逐项 M1–M5 结果与语言门。 |
| 独立 reconciliation；最终状态后 | `Dashboard/Artifacts/Reconciliation.md`，读取实际最终 Closeout、Dashboard、KB 及 diff/inventory，给唯一无冲突 verdict。 |

Builder write exclusions：不得改 `Goal.md`、`Design.md`、`DesignLog.md`、任何既有卡/冻结 expected、`AGENTS.md`、`kb/`、`.codex/skills/`、公开 candidate 或源仓；不得伪造独立 Review、Closure 与 reconciliation 的作者或结论。需要修正这些输入时退回对应 owner 并保存 Design Delta 或 Scope Delta。禁止移除、替换、延期 M1–M5 来获得完成措辞。

## 原始范围与验收表

本表是 pre-Builder 验收映射，实际结果保持未完成；最终 Closeout 必须逐项补实际源链接、结果、阻断/例外、时序、claim ceiling 和父面吸收状态，不得把计划表当完成矩阵。

| ID / 原始要求来源 | 可观察判定 | Owner / 时序与证据位置 | 当前实际结果 / 状态 | 阻断或例外 / 主张上限 / 父面吸收 |
| --- | --- | --- | --- | --- |
| M1：[Goal 原始范围](Goal.md#原始范围与验收)，项目说明文档 | 三个指定中文标题存在；步骤命令真实引用 target AGENTS/profile；人工检查未夸大能力。 | Builder；Design 后；`PROJECT_NOTE.md` 与 Handoff。 | 尚未实施，待验证。 | 无范围例外；仅文档示例；Closeout 待吸收。 |
| M2：[Goal 原始范围](Goal.md#原始范围与验收)，冻结设计与范围 | 独立 Design 在 Builder 前保存最小内容、文件、排除范围及交接；验证实际 lane 时序。 | 本 Design lane；[Design](Design.md)、[DesignLog](DesignLog.md)。 | 设计已保存，待独立验证；Context 投影修正待主任务。 | 设计存在不等于实现通过；Closeout 待吸收。 |
| M3：[Goal 原始范围](Goal.md#原始范围与验收)，一个 Session 及验证交接 | UAT-S001 行存在；Handoff 列 actual files、变化、真实命令及验证要求。 | Builder 后；[Sessions](../Sessions.md)、Handoff。 | Session 行已存在；Handoff 尚未产生。 | 不能把交接包当 verdict；Closeout 待吸收。 |
| M4：[Goal 原始范围](Goal.md#原始范围与验收)，独立验证 | 新上下文 reviewer 同时读取 Goal、Design、实际文件、Handoff、实际 Closeout；正例通过；缺文件负例不能通过。 | 独立 Validation；Builder 与 Closure draft 后；Review 与 lane 证据。 | 尚未验证。 | 正负例都需真实观察；仅当前文档合同；Closeout 待吸收。 |
| M5：[Goal 原始范围](Goal.md#原始范围与验收)，中文收束与最终状态 | 中文 Closeout 链接独立 Review；language gate 通过；最终 Dashboard/KB/diff 由独立 reconciliation 覆盖。 | Closure final 后独立 Validation；Closeout、Reconciliation、Sessions/Current_State。 | 尚未发生。 | 前置 Review 不能覆盖未见过的最终修改；仅本例闭合；最终父面待吸收。 |

Scope Delta：本设计未删除、替代、缩小任何 M1–M5；Context 影响标记修正是投影纠错，不改变原始 Goal denominator。若后续产生设计偏离，记录原要求、原因、替换内容、影响、审批需求/依据、延期或阻断状态，验证必须检查原 Goal。

## 验证交接要求与检查计划

Builder Handoff 必须用中文列 claimed scope、实际文件与变化、真实命令/输出、已知风险、明确非目标、KB/Dashboard 影响，并链接 Goal、Design、logs、实际 Closeout 和最终状态。Closure 的 `验证交接包` 应引用该 Handoff，补最终 diff/inventory、原始范围覆盖矩阵与 Scope Delta、独立 reviewer 入口。

Validation 必须独立读回实际文档，检查中文标题、真实链接、复制命令预期与实际 authority 吻合。负例推荐在隔离临时目录构造缺失 `PROJECT_NOTE.md` 的输入，用同一存在性检查获得非零/明确拒绝；记录命令、输入与结果。不可先删除正式产物或凭文字承诺声称负例已执行。存在性正例只证明文件存在，正文语义与边界仍需独立人工式审阅。

需要运行实际命令：`python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode closeout-language --file Dashboard/Artifacts/Closeout.md`。`Closeout language verdict` 应保留在交接包；未运行或未通过时不允许最终完成。不存在本例自带 Session registry，不自创或借入源仓 registry；最终 reviewer 应核对目标 Sessions/Current_State 的实际一致性。

最后一次 reconciliation 应重读所有最终变更面、对保护输入核对未变，覆盖未跟踪/生成文件，记录唯一 reviewer/source 与唯一 passing verdict（通过仅限 M1–M5）。若仍有缺项，保留 partial/blocked 中文解释；不能回填不曾发生的时序。无待办 Session 且 M1–M5 全满足才能结束本例。

## 语义与 SGC 比例检查

ERBE applicability=`not_applicable`（不适用）：本例仅说明文档和执行证据，不改变终态谓词、状态机、acceptance、authority routing 或 runtime。Semantic Reviewer 本例不触发：不做能力泛化、truth promotion、oracle freeze 或规则修订；若出现这些变化，应重评估并在越界实施前转交主任务。

SGC strongest claim=`structurally_supported`（设计与输入结构相符）；已执行校验另属 `test_bound` 的卡/包结构证据。证据层只支持本 lane 设计已保存，不能证明实现质量或外层 UAT。

- SI-1：中文标题/文件形状不证明正文正确，Validation 须读实际内容。
- SI-2：每项观察链接实际文件或记录真实命令；未产生证据明确待验证。
- SI-3：原规则留在目标 authority；Design、日志与 Session 状态属于 Dashboard 执行记忆。
- SI-4：Builder 不写独立 verdict；Review 与最终 reconciliation 从实际输入重算。
- SI-5：只有独立最终证据满足 M1–M5 才允许本例完成措辞。
- SI-6：完整保留 M1–M5 的技术、时序和最终核对要求。

Forbidden collapses：不以 schema/字段代替语义，不以生成 expected 代替验证，不把 profile 路由变成能力批准，不用标签掩盖不确定性，不以空来源 ID 伪造 grounding，不从本例文件齐全推出外层完成，不替换原始范围。

## KB 与 Dashboard 复核

Contract Delta Scan：`Dashboard-only`（只记录本例执行设计），没有新增稳定规则；本设计引用现有 authority，不修改 `kb/`。Dashboard 由相应 lane 保存状态、证据与最终 closeout。当前入口修正在本 Session 内处理，无新增域外 concrete follow-on。该判断须在最终状态再复核，不预告最终完成。
