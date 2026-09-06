# UAT-S001 初轮独立验证

## 关键结论中文展开

本任务是在 target 写一份能依实际路径操作的中文项目说明，并保留原 Goal 的五项流程证据。本轮唯一 verdict 为 **partial（初轮部分满足，不能声明 Goal 完成）**：M1–M4 在本地文档合同范围内已获得独立证据，M5 仍待最终 Closeout、两父面吸收与独立后置对账。未发现需要 Builder 修改说明的当前合同问题。

Reviewer/source：`/root/uat_validation`，独立于 Builder 的本轮 subagent；唯一正式来源为本文件。证据绑定于[写前快照](ValidationSnapshot.json)记录的实际输入，真实命令及输出见[ValidationLog](ValidationLog.md)。本轮读的是[实际 Closeout 草稿](Closeout.md)，未声称读过尚未产生的最终稿或 Reconciliation。本结果不判断外层 S-026 UAT、新手普遍可用、发布或生产就绪。

## 接入与已读证据

Intake verdict：execute（允许按已校验卡在三个证据文件内写入，保持 read-mostly）。采用 validation profile 启动包，经 `context_bootstrap.py validate /dev/stdin` 实际退出 0；启动包原文保存在[日志](ValidationLog.md#实际启动包)。重新确认目标、authority、主张限制与最终对账依赖，未把结构通过当语义通过。

| 输入 | 实读状态与用途 |
| --- | --- |
| [ValidationCard](ValidationCard.json)、[原 Goal](Goal.md) | 全文已读；原卡摘要校验退出 0，保持 M1–M5 分母与三文件 write scope。 |
| [目标 AGENTS](../../AGENTS.md)、[profile](../../kb/data/strategy/profile.json)、[旧 Context](Context.json)、[修正 Context](ContextBuilder.json) | 全文已读；目标分工、claim ceiling 与两个 Context 的实际差异均核对。 |
| [Design](Design.md)、[DesignLog](DesignLog.md)、[DesignCard](DesignCard.json)、[BuilderCard](BuilderCard.json) | 全文已读；Design 与 Builder 卡重新校验退出 0；Builder 卡绑定现存 Design，日志交叉支持先设计后 Builder。不是外层 task 时间线审计。 |
| [PROJECT_NOTE](../../PROJECT_NOTE.md)、[Handoff](Handoff.md)、[BuilderLog](BuilderLog.md) | 全文已读；独立执行说明实际命令，并读正文、链接与边界；不复用生产者自报 verdict。 |
| [Closeout](Closeout.md)、[ClosureLog](ClosureLog.md)、[Sessions](../Sessions.md)、[Current State](../Current_State.md) | 全文已读；逐项 OPCM、Scope Delta 文字、验证交接、实际草稿及当前父面均纳入。Current State 的下一步骤仍停在创建草稿，属于最终 Closure 应更新的既定状态面。 |
| [已安装 Skill](../../.codex/skills/sge-governed-checkpoints/SKILL.md) | 首批输出截断，随后分段补读工作流、Validation、Context、SGC、closeout、Hard Stops 与 Output Expectation；没有把截断段算作自动已读。 |
| [checklists](../../.codex/skills/sge-governed-checkpoints/references/checklists.md)、[上下文协议](../../.codex/skills/sge-governed-checkpoints/references/context-efficient-goal-validation.md) | 实读 Validation 固定提示/交接段和 snapshot/rebaseline 段；其余未相关段不纳入本次已读声明。 |
| [公开 SGC JSON](/tmp/sp004-s026-01a0744b/candidate/kb/data/strategy/strategy_sgc_structural_contract_v1.json) | 实读 100–290 行，含 claim levels、forbidden collapses、SI-1..SI-6、completion；仅公开只读参考，不替代 target truth。 |
| [PromptAudit](PromptAudit.json)与全文件扫描 | Audit JSON 全文已读；其余安装源码/schema/prompts仅采集路径和字节摘要，未声称逐文件语义审核。 |
| 尚未产生的最终稿与 Reconciliation | 缺失且明确未读，由 M5 后续独立对账处理。 |
| 公开 README/Quick Start/新手指南、来源聊天、源仓私有 Dashboard、memory 文件 | 本 lane 未重读公开入口，也未读取来源聊天/私有历史/memory 文件；公开 UAT 步骤由主任务另行采证。系统注入规则与 memory 摘要仍存在，因此不能声称完全无项目上下文。 |

## 原始目标覆盖矩阵

每条原要求及验收来源均为[Goal 原始范围](Goal.md#原始范围与验收)。以下结果只覆盖此次实际输入，所有行主张上限均为本地文档示例。

| ID / 原始要求 | 可观察验收与精确来源 | 实际结果 / 状态 | owner / 时序 | 阻断或例外 | 父面与 Closeout 吸收 |
| --- | --- | --- | --- | --- | --- |
| M1 项目说明文档 | [说明](../../PROJECT_NOTE.md)须有三指定中文标题，真实 target AGENTS/profile 操作，无产品/发布完成声称 | 已满足：独立读正文，三标题准确；五链接存在；读取命令实际退出 0，预期输出与 authority 一致 | Builder 在冻结 Design 后；本 Validation 重算 | 无当前 Builder 修复；文件存在检查另有语义人工审阅补足 | 两父面已有说明入口；草稿已吸收 M1，待最终稿吸收本 Review |
| M2 冻结设计与范围 | 独立 [Design](Design.md)/[DesignLog](DesignLog.md)明确最小内容、输出、write exclusions；[BuilderCard](BuilderCard.json)冻结同一 Design | 已满足本地文档合同：Design 文件摘要与 Builder 卡一致，BuilderLog 记录先读 Design，再按五文件写入，DesignLog 记录 PROJECT_NOTE 尚不存在 | Design → Builder；独立 lanes 的现存日志及卡 | 支持 target 内已记录时序；不证明外层 visible-task/clean-room 全部条件 | 草稿逐项保存设计交接与时序边界；最终稿应引用本 Review |
| M3 一个 Session 及验证交接 | [Sessions](../Sessions.md)有 UAT-S001；[Handoff](Handoff.md)列 actual files、变化、真实命令与独立验证要求 | 已满足：单一 UAT-S001 行，五文件清单正确；完整扫描未见未解释的产品/KB/core 写入 | Builder 写入后交 Closure/Validation | 两父面目前仍是待验证，符合初轮时点；最终更新属于 M5 | 两父面已链接 Handoff，草稿已吸收 |
| M4 独立验证 | 本 reviewer 从 Goal/Design/说明/Handoff/实际草稿重算；同一存在检查有真实正例及隔离缺文件负例 | 已满足此次 M4：正例 PRESENT/0，缺文件负例 MISSING_PROJECT_NOTE/1；本 Review 和[命令日志](ValidationLog.md)保存独立结果 | 当前 `/root/uat_validation`，Builder 与 Closure 草稿之后 | 不依赖 Builder verdict；当前三文件本身须由后置 reconciliation 纳入最终清单 | 原父面/草稿仍称 M4 未满足，最终 Closure 必须吸收本轮新增证据 |
| M5 中文收束与最终状态 | 最终 [Closeout](Closeout.md)引用 Review，language gate 通过；最终两父面/KB/diff 由 Reconciliation 覆盖 | 未满足：草稿语言门已实际通过，但最终稿、最终状态与独立后置对账尚未发生 | Closure final → 独立 reconciliation | 唯一当前 completion blocker；既定流程待完成，无新增 hardening | 当前仍不能使用最终完成措辞；须最终 Closeout 与两父面吸收本 Review 和最终对账 |

## 问题与范围复核

**阻断最终完成的事项：** M5 尚待 final/reconciliation。执行顺序应继续最终 Closure，再由新 digest-bound delta card 读取实际最终稿、两父面、KB、完整 inventory/diff 及保护输入；在此之前不能以本 Review 声称 Goal 完成。这是原合同要求，不是新增验收。

**非阻断观察：** Current State 的下一步骤仍停在创建 Closure 草稿；Handoff 与 Closeout 草稿保留当时 M4 未满足的历史口径。最终 Closure 应将当前状态更新为已得到初轮验证、待最终对账，并保留历史证据时间含义。

旧 [Context](Context.json) 与 [ContextBuilder](ContextBuilder.json) 的差异不仅是 dashboard_state=false→true，Raw User Intent 文本也从外层 S-026 UAT 改写为 M1–M5 子实验。故不能把该修正描述为“只改影响标记”，或用 ContextBuilder 证明外层 Scope Delta 为无。此次审查依据始终是同一[原 Goal](Goal.md)的五项要求：未观察到 M1–M5 被删除、替换或缩小；外层完整目标覆盖及 clean-room provenance 另由外层审核。本观察不引入本例新增 Builder 修复。

**Required Builder repair：无。** 文档内容、命令和链接满足当前 M1；剩余动作由既定 Closure/reconciliation 承接。没有新增域外 deferred follow-on 或新的待办 Session。

## 实际命令、负例与完整清单

[日志](ValidationLog.md)保存 14 条真实 subprocess 命令的 argv、cwd、退出码、stdout、stderr，以及验证启动包。说明中的 `cd` 对应每条命令实际 cwd；`cat AGENTS.md`、`python3 -m json.tool ...`、三个状态读取命令均退出 0。AGENTS/profile 实际内容与说明预期一致，claim ceiling 仍为 repo-local governance skeleton only。

同一 `python3 -c` 存在性检查在 target 得 PRESENT/0；在隔离空临时目录得 MISSING_PROJECT_NOTE/1。没有删除正式产物；负例之后正式文件仍在。该负例只证明缺文件会被拒绝，语义判定另由本轮正文阅读支撑；它不是 ERBE RED、恶意输入通用保证或产品能力验证。

写前全目录扫描共 42 文件；与 BuilderLog 的 pre-Builder 基线独立比较：新增 9 个文档/协调证据；改动 Sessions、Current_State 与 PromptAudit；无删除。PromptAudit 新增 Closure/Validation prompt 记录，变化与本轮 lane 序列一致。26 个保护输入（core、profile、AGENTS、README、install manifest、Goal、Design/DesignLog、两 Context）字节全部保持原样。详细 inventory、差异列表与保护输入见[快照](ValidationSnapshot.json)。

实际 `git status` 退出 128，因为 target 无 Git；此为环境事实，不能伪造 commit/diff。采用完整文件系统基线与生成物扫描，快照显式记录 `baseline_revision`、全部输入摘要、未关闭项和 rebaseline triggers；该观察快照不声称通过需要 Git 字段的通用 snapshot schema。没有 Session registry，按本 Goal 检查实际父面，不借入源仓工具。

## 验证交接包

Claimed scope 是本地 M1–M4 初轮独立证据。实际读了原始范围、设计、说明、交接、草稿、两父面和目标 KB；无 runtime/schema、acceptance、authority 或 core 修改。原始五项、完整 diff/inventory、scope 差异观察与全部未覆盖项均已列出。

Closeout language verdict: pass（对本轮实际 Closeout 草稿运行语言门退出 0，输出 Closeout language check passed；只证明中文标题与状态解释检查通过，不证明 M5 最终对账）。最终稿必须重跑相同语言门，并由独立 reconciliation 对最终文件与父面给唯一结论。

后续 delta 应至少覆盖最终 Closeout、Closure final 日志、Sessions、Current_State、Review、ValidationLog、ValidationSnapshot，以及新增的 final/reconciliation 卡/提示/audit；重新扫描整个目标目录，任何未登记变化须解释并决定是否 rebaseline。本轮快照不自引用输出摘要，三个 Validation 新文件须由后置对账纳入。

## 语义与资料归属复核

SGC 最强证据为 execution_bound（实际命令）与 test_bound（当前存在性和语言门），正文含义由独立源阅读支持。SI-1 不以三标题代替语义；SI-2 逐项绑定真实文件和命令；SI-3 stable truth 仍在目标 authority、Review 是 Dashboard 执行证据；SI-4 当前 reviewer 不创建 Builder 文档；SI-5 M5 未满足所以保持 partial；SI-6 完整保留五项技术和流程要求。已检查并拒绝结构替代语义、重造预期充当验证、profile/route 充当能力批准、标签掩盖未知、空来源 grounding、虚假完成和范围替换。

ERBE not_applicable（文档示例不改行为合同）；无 Semantic Reviewer 新触发；BDD 不适用，未修改维护门禁或案例。Contract Delta Scan 为 Dashboard-only（本例执行观察），未产生应提升到 KB 的新稳定规则。Dashboard 必须吸收当前初轮结果和最终对账；本 lane 只写获授权三文件，由 Closure 更新父面。

## 后续状态

goal_terminal=false（M5 尚待完成）；next_session=UAT-S001（继续同一例子的最终收束）；next_session_ready=true；human_decision_required=false。主任务应按既定流程继续，不能将本轮 partial 误读为请求用户批准或停止 Loop。
