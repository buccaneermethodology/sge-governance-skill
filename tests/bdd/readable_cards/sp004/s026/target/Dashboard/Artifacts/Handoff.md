# UAT-S001 Builder 验证交接包

## 实际任务与范围

Builder 已按[冻结设计](Design.md)创建[项目说明](../../PROJECT_NOTE.md)，并保存本交接、[执行日志](BuilderLog.md)、[Session 表](../Sessions.md)和[当前状态](../Current_State.md)。五个文件构成本 lane 的实际写入范围。Intake verdict=`execute`（目标与 authority 一致，按已列五文件范围执行）；依赖为[Goal](Goal.md)、[目标 AGENTS](../../AGENTS.md)、[profile](../../kb/data/strategy/profile.json)、[Builder card](BuilderCard.json)及[修正 Context](ContextBuilder.json)。

ContextBuilder 已由主任务在本 lane 前把 Dashboard 影响纠正为 true，并保留旧 Context 历史；Builder 校验通过且没有改写它。来源 authority 不变，最大主张仍为本地文档示例。没有修改 core、profile、KB、设计、Goal、冻结卡、公开 companion 或源仓。未新增 schema、测试框架、BDD gate、provider、release、远端或产品实现。

## 实读清单与命令证据

完整实际输入范围、读取截断补读、未读项、入口失败与修复、命令及执行结果见[Builder 日志](BuilderLog.md)。说明中的读取命令由本 lane 实际运行；路径/三个中文标题只做生产者自检，不能冒充独立验证。actual inventory 与受保护文件的核对证据同样保存在日志。

## 原始目标逐项交接

各项原始来源均为 [Goal 原始范围](Goal.md#原始范围与验收)，不得只检查 revised Design。

| ID / 原始要求 | 可观察验收与精确证据 | 本 lane 实际结果 / 状态 | Owner / 时序 | 阻断或例外 / 主张上限 / Closeout 吸收 |
| --- | --- | --- | --- | --- |
| M1 项目说明文档 | [说明](../../PROJECT_NOTE.md)具有项目目的、使用步骤、边界三个中文二级标题；命令引用真实 AGENTS/profile；正文无产品/发布完成主张 | 已写入并自检；待独立内容复核 | Builder 在 [Design](Design.md)之后 | 无范围例外；仅文档示例；Closeout 待吸收 |
| M2 冻结设计与范围 | [Design](Design.md)及[DesignLog](DesignLog.md)应证明独立设计先于 Builder，核对 card 的冻结源与排除范围 | 设计在 Builder 开始前已存在；本 lane 读取 Design，未读取 DesignLog 正文，独立时序待 reviewer 核验 | 独立 Design → Builder | 不由 Builder 自证独立设计通过；Closeout 待吸收 |
| M3 一个 Session 及验证交接 | [Sessions](../Sessions.md)有 UAT-S001；本 Handoff 列出 actual files、变化、命令和验证要求 | 已写入交接；状态为待独立验证 | Builder 后交 Closure/Validation | 交接不等于 verdict；Closeout 待吸收 |
| M4 独立验证 | 新上下文 reviewer 读取 Goal、Design、实际说明、Handoff、实际 Closeout；正例和缺文件负例实际执行并记录 | 本 lane 未执行独立验证或缺文件负例；未满足 | Closure 草稿后，独立 Validation | 当前禁止最终通过；只支持已写入；Closeout 待吸收 |
| M5 中文收束与最终状态 | 实际 [Closeout](Closeout.md)链接独立 [Review](Review.md)；语言门通过；最终 Dashboard/KB/diff 由 [Reconciliation](Reconciliation.md)覆盖 | 三个链接为下游预期路径，本 lane 时不存在；未满足 | Closure final → 独立 reconciliation | 不预报最终 verdict；最终父面待吸收 |

Scope Delta / Design Delta：本 lane 未删除、替代、缩小或延期 M1–M5；把待独立验证如实记录为未满足项。Context 投影修正不是原始范围变化。任何后续调整必须由对应 owner 记录，不得以此交接包视为批准。

## 最终验证要求与未覆盖项

Validation 需重新阅读实际文件，检查说明链接可达、命令可复制、预期输出符合目标 authority，并审查正文含义与边界。使用同一存在性检查，在正式 target 做正例，在隔离临时目录构造缺失 PROJECT_NOTE 的负例，记录非零或明确拒绝；不得删除正式文件，不得把负例称为 ERBE 可信 RED。

Closure 必须创建实际中文 Closeout，引用本交接并补齐逐项原始覆盖矩阵、语言门与独立 Review。当前 `Closeout language verdict=not-run`（尚无本 lane 可检查的实际 Closeout，不能宣布最终完成）。下游须运行：

```sh
python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode closeout-language --file Dashboard/Artifacts/Closeout.md
```

最终独立 reconciliation 必须读取最终 Closeout、Review、Sessions、Current_State、KB 与完整 diff/inventory，检查保护输入未改与未登记生成文件，并保存唯一 reviewer/source、实读清单和唯一无冲突 verdict。目标没有 Session registry 工具；不引入或借入源仓 registry，改由 reviewer 核对实际表面一致性。M4/M5 仍为后续必要工作，不能只凭 Builder 自检或交接包宣布 Goal 完成。

## 语义与治理检查

SGC strongest claim=`execution_bound`（真实命令与写入的观察）和 `structurally_supported`（文档形状及路径自检）；只覆盖本 lane 操作，不代表独立语义验证。SI-1 形状不等于含义；SI-2 文件和命令可定位；SI-3 稳定规则仍在既有 authority，执行状态写 Dashboard；SI-4 Builder 不写独立 verdict；SI-5 M4/M5 未满足，状态保持待验证；SI-6 完整交接五项原要求。拒绝 schema substitution、recompute validation、profile/routing collapse、deterministic masking、mock grounding、false closure、scope substitution。

ERBE=`not_applicable`（仅文档，不改终态谓词、状态机、acceptance 或 runtime）；Semantic Reviewer 不触发，没有 authority/truth/能力扩宽。BDD 不适用，没有修改行为门禁或枚举 case。Contract Delta Scan=`Dashboard-only`（本例执行证据），KB 无稳定规则变化；Dashboard 已更新待验证状态。同一 Session 内继续 Closure/Validation，无新增域外 follow-on。
