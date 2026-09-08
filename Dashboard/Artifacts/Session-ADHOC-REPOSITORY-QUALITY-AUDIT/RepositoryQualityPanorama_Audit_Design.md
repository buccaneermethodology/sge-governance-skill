# 仓库质量全景与审计设计交接

## 任务目标

基于当前工作树生成一份可筛选的 Dashboard 全景派生读模型，并独立审计：公共开源候选中的 Semx 残留、SP-001 每个 Session 的实际落地产物、缺失引用，以及其他不一致与质量风险。

## Source authority 与边界

- 当前 `kb/` 是稳定治理真源；当前 `Dashboard/` 是执行记忆；Git、测试和门禁输出是可重算证据。
- 全景 Markdown、JSON、HTML 只是派生读模型，不修改或替代 Dashboard 状态，也不是批准或完成凭据。
- 本任务允许新增本审计的设计、启动包、lane card、全景和验证报告；不修复发现的仓库问题，不关闭 SP-001/S-012，不发布、不推送、不写全局 Skill。

## 最小安全切片

1. 对当前 Dashboard、KB、Skill、tests、Git 表面建立 source manifest。
2. 生成 JSON 全景真值快照和 Markdown 阅读面，再用 `exploration-dashboard-synthesizer` 自带 renderer 生成单文件 HTML。
3. 三条只读审计 lane 分别检查：公共身份残留；SP-001 Session/artifact 完整性；断链与其他一致性。
4. 主线程汇总时保留冲突，不以首条记录覆盖其他证据；最终再做独立 Validation。

## 验收判定

- HTML 可离线打开，具备关键词/字段筛选、视图切换和详情抽屉；JSON 可解析，HTML 内嵌数据可解析。
- 全景覆盖 Big Ideas、Stage Plans、Sessions、Decisions、Risks、Exceptions、Artifacts、Agent Logs、KB、Skill、tests、Git 状态和 source manifest。
- 对 SP-001/S-001..S-012 逐项给出：登记状态、声明的 deliverables、实际存在的 artifacts、关键门禁/验证、差距与最大可支持结论。
- 残留与断链发现必须给出文件/行号或明确的缺失目标；历史 provenance 与 active/public surface 分开分级。
- 最终结论不得把 SP-001 既有 `Done` 子 Session、历史 closeout 或生成全景等同于 SP-001 整体完成。

## 最大主张

本次最多声明：当前工作树的 Dashboard 全景已生成并通过结构检查，仓库质量审计发现已按现有证据分级；不证明仓库已具备公共发布条件，也不证明 SP-001 已完成。

## Lane 与写范围

- 主线程 Builder：仅写 `Dashboard/Artifacts/Session-ADHOC-REPOSITORY-QUALITY-AUDIT/RepositoryQualityPanorama_*`。
- 三条审计 lane：read-only，不修改文件。
- 最终 Validation：read-only，覆盖实际全景文件、审计报告和最终 diff。

## ERBE / Semantic / BDD

- ERBE：`not_applicable`，本任务不改变状态机、终态谓词或 promotion/write contract。
- Semantic Reviewer：不单独启动；本任务是现有语义与证据的审计，不批准新稳定语义。若发现 S1-S6 风险，在报告中分类。
- BDD：不修改 maintained gate/runtime/schema，因此无需更新 BDD 文件；只运行与当前审计相称的既有门禁。
