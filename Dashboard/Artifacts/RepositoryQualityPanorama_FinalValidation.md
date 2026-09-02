# 仓库质量全景与审计报告最终验证

## 任务理解

本验证 lane 独立检查本轮生成的仓库质量全景和审计报告是否忠实覆盖原始要求：提供离线可筛选 HTML、审计公共残留、逐项核对 SP-001 Session artifacts、识别缺失引用与其他质量问题，并把结论限制在“全景/报告交付质量”，不得借此宣称仓库质量、SP-001 completion 或 public readiness 已通过。

本轮是 read-mostly final-state reconciliation；没有修复 registry、断链、S-012 或 Builder 产物，也没有改变 `kb/` canonical truth 或 Dashboard 状态。

## Read Manifest

已读取或核验：

- [仓库硬门](../../AGENTS.md)与 [SGE governed checkpoints](../../.codex/skills/sge-governed-checkpoints/SKILL.md)，用于确认 Validation、SGC、truth split 与 claim ceiling。
- [最终 Validation Lane Task Card](RepositoryQualityPanorama_FinalValidation_LaneTaskCard.json)及 [Context Bootstrap](RepositoryQualityPanorama_FinalValidation_ContextBootstrap.json)；card 摘要校验通过，Context Bootstrap 结构校验通过。
- [审计设计交接](RepositoryQualityPanorama_Audit_Design.md)，作为原始目标、AC、边界和 maximum claim authority。
- [审计报告](RepositoryQualityPanorama_Audit_Report.md)、[全景 JSON](RepositoryQualityPanorama_Data.json)、[全景 Markdown](RepositoryQualityPanorama.md)、[全景 HTML](RepositoryQualityPanorama.html)与 [生成器](RepositoryQualityPanorama_Generator.py)。
- [Current State](../Current_State.md)、[Big Ideas](../Big_Ideas.md)、[Stage Plans](../Stage_Plans.md)、[Sessions](../Sessions.md)、[Session Index](../Session_Index.md)、SP-001 archive 与 archive manifest，用于复核 SP-001/S-012 与 registry 当前状态。
- [SGC v1 canonical JSON](../../kb/data/strategy/strategy_sgc_structural_contract_v1.json)、S-012 Context/Card 和 genericity test，用于复核 active authority 断链与 `test_bound` 边界。
- 最终 `git status --short`、`git diff --check`，以及卡片指定的 registry、S-012 card、genericity、HTML/JSON、closeout-language 检查。

缺失或未作为 passing authority 使用：

- 本任务不是 Goal/SP completion，因此没有独立的 Goal OPCM；下方按设计交接中的六项 AC 逐项建立 Evidence Completeness。未发现本任务自身 scope narrowing。
- 三条只读审计 lane 的独立结果没有单独 durable review artifact；最终报告仅在验证交接包中记录 reviewer 名称。本最终验证对关键 blocker 做了独立重算，但没有重新扩展扫描全部历史命中。

## Evidence Completeness

| AC | 可观察判定 | 实际结果 | 状态 | Claim ceiling |
| --- | --- | --- | --- | --- |
| `PANORAMA-HTML` | HTML 离线、内嵌 JSON 可解析，关键词/字段筛选、视图、分页、详情可用 | HTML 与内嵌 JSON可解析；视图、关键词、排序、分页和详情代码存在。但 Session 数据的 `stage_plan`、`surface` 均为空，导致 Stage Plan 与当前/归档筛选不能产生预期结果；HTML 内嵌模型也不等于同名 JSON | `blocked`，需 Builder 修复 | 不能声明完整的“字段可筛选 HTML 已通过” |
| `AUDIT-PUBLIC` | 公共残留按 active/public 与历史 provenance 分级并限制发布结论 | 报告列出 LICENSE/NOTICE、default-deny/export contract 缺失、绝对路径与 active registry residue，并把 public candidate 判为 blocked | `landed` | 仅支持审计 finding，不支持 public-ready |
| `AUDIT-SP001` | S-001..S-012 逐项给出状态、artifact、差距与最大结论 | 报告逐项覆盖 S-001..S-006、S-012，并与 Stage Plan/Sessions 的 `Doing` 状态一致；registry 与 S-012 card 失败已重算 | `landed` | SP-001 保持 `Doing/blocked` |
| `AUDIT-REFERENCES` | 断链给出精确文件/缺失目标 | 报告列出 active canonical、S-005/S-006、S-002、历史 design 与 KB README 断链；active SGC/Human-AI strategy 缺失已抽查复核 | `landed-with-evidence-limit` | 支持报告所列有界 finding；不是全仓零遗漏证明 |
| `AUDIT-OTHER-QUALITY` | 识别 registry、renderer/DKG、测试入口等其他质量问题 | registry drift、S-012 invalid card、genericity pass、零测试假绿等结论与重跑结果一致；未将失败修成通过 | `landed` | 支持当前审计状态，不支持仓库质量 pass |
| `CLAIM-BOUNDARY` | 不把全景/历史 closeout/test 通过折叠成 SP-001 或公共发布完成 | 报告明确使用 `repository_consistency=fail`、`public_candidate=blocked`、`test_bound` 与 `structurally_supported`，边界与 SGC SI-5/SI-6 相符 | `landed` | 最多确认报告的大部分审计结论忠实 |

## Blocking Findings

### P1：HTML 的关键字段筛选是空功能，未满足 `PANORAMA-HTML`

[HTML](RepositoryQualityPanorama.html)提供 Stage Plan 和“当前/归档”筛选控件，但内嵌 Session 项目的 `stage_plan` 与 `surface` 都是空字符串；筛选逻辑却要求这两个字段精确匹配。因此选择 SP-001/SP-002 或 current/archive 时，合法 Session 会被全部过滤掉，而不是得到相应子集。

这违反 [设计交接](RepositoryQualityPanorama_Audit_Design.md)第 22 行要求的“关键词/字段筛选”可用性，也使 [审计报告](RepositoryQualityPanorama_Audit_Report.md)第 11 行对“关键词/字段筛选”的无保留表述超过实际证据。必须由 Builder 在生成数据时提供稳定的 `stage_plan`/`surface`，或删除/降级不能工作的控件与主张，并重生 HTML 后复测。

### P1：HTML 内嵌数据不是同名 JSON 的忠实嵌入，Source view 丢失 manifest 值

独立解析显示 [HTML](RepositoryQualityPanorama.html)的 embedded JSON 可解析，但与 [全景 JSON](RepositoryQualityPanorama_Data.json)不相等。尤其 `source_manifest` 在 JSON 中是带计数、Git 和 archive snapshot 的对象，进入 HTML 后变成字段名数组；HTML Source view 因而只能展示键名，不能展示报告所称的详细 source metadata。该差异还掩盖了 HTML 数据中新增的空 `stage_plan`/`surface` 字段。

设计 AC 只明确要求 embedded JSON“可解析”，所以“字节相等”本身不是独立 hard gate；但当前差异已经造成可观察功能和证据入口损失，因此与上一项共同阻断 HTML 完整交付。Builder 应冻结 renderer 输入/输出 contract，至少验证关键字段和值的语义等价，而不只是 JSON parse。

## Non-blocking Findings

- [全景 JSON](RepositoryQualityPanorama_Data.json)生成时记录 82 个 Dashboard artifacts；最终验证开始时为 85 个。新增差异来自 final-validation 控制面文件，说明全景是生成时快照，不是随工作树自动更新的实时索引。报告已用 `generated_at` 与派生读模型边界限制其含义，因此该时间差不单独阻断审计报告，但最终交付应避免称其为毫无时点限定的“当前全部文件”。
- 三条审计 lane 的结果没有各自 durable review artifact，降低 provenance 的可复核性。由于本轮 final Validation 已独立重跑关键 blocker，当前可将其作为后续治理改进，不把它升级为全部报告 findings 的 blocker；未来同类审计应保存每条 lane 的 Read Manifest 与 finding artifact。
- HTML 的 JSON parse、关键词、排序、分页、视图和详情代码结构存在；本 verdict 不否定这些已工作的部分，只否定“所有字段筛选与 Source detail 均可用”的完整主张。

## 原目标覆盖与 overclaim 检查

- Scope narrowing：未发现。报告覆盖了公共残留、SP-001 逐 Session、断链和其他质量问题四个原始审计面。
- Overclaim：仓库/SP-001/public-ready 层面没有 overclaim；报告明确保持 `fail/blocked/test_bound`。交付层面存在局部 overclaim：HTML 被描述为具备字段筛选和 source metadata，但两个关键筛选字段为空，Source view 丢失值。
- SGC v1：全景 JSON 的结构主张最多为 `structurally_supported`；genericity 仅为 `test_bound`；SP-001 completion 与 public readiness 仍为 `blocked`。本验证不得把报告本身的可用性 verdict 折叠成仓库质量 verdict。

## Test / Gate 充分性

| 检查 | 结果 | 含义 |
| --- | --- | --- |
| Final Validation lane card digest | `pass` | 委派合同与预期摘要一致 |
| Context Bootstrap validate | `pass` | 启动包结构有效；不等于审计正确 |
| 全景 JSON parse / HTML embedded JSON parse | `pass` | 两者可解析；但语义模型不相等 |
| HTML embedded JSON 与同名 JSON 等价 | `fail` | Source manifest 值和关键字段语义发生变化 |
| `session_registry reconcile --check` | `drift` | archive manifest 与 Session Index 漂移，未执行 apply |
| `session_registry validate` | `projection_drift` | registry 当前不能支持 clean completion |
| S-012 Lane Task Card validate | `fail` | `base_context_refs[0].sha256=PENDING` 不是合法摘要 |
| genericity direct test | `pass` | 只支持有界 portability `test_bound` |
| 审计报告 closeout-language | `pass` | 中文标题、英文 verdict 解释和 reader evidence 入口满足语言门；不改变 findings |
| `git diff --check` | `pass` | 未发现已跟踪 diff 的空白错误；当前交付文件仍是 untracked，不等于已提交或发布 |

这些门禁足以确认报告对主要仓库 blocker 的描述与边界大体可信，也足以定位 HTML 交付 blocker；它们不支持仓库、SP-001 或 public readiness 通过。

## KB / Dashboard Truth Split

- `kb/`：本任务没有批准稳定 contract、terminology、runtime 或 promotion policy 变化，不应更新 canonical truth。
- `Dashboard/`：全景、审计报告和本 Validation Review 属执行记忆/派生证据，放在 `Dashboard/Artifacts/` 正确；它们不得覆盖 Sessions/Stage Plans 的 authority。
- 后续工作：报告已列出的 S-012、registry、active canonical 断链和 public contract 均已有 Dashboard 跟踪面；本 Validation 没有创造新的仓库治理 Session。HTML 修复属于当前交付的 Builder repair，不应伪装为 KB promotion。

## Required Builder Repair

1. 给每个 Session 派生明确的 `stage_plan` 与 `surface=current/archive`，重生 JSON/HTML，并对 SP 与 current/archive 筛选做可观察验证。
2. 修复 renderer contract，使 HTML Source view保留 `source_manifest` 的路径、计数、Git 状态与 archive snapshot 值；增加 embedded model 与源 JSON 的关键字段语义等价检查。
3. 收窄或更新审计报告中“字段筛选”和“HTML source metadata”的表述，使其与修复后的实际行为一致。
4. 修复后必须做 delta validation；不得以 JSON 可解析或代码中存在控件替代交互语义验证。

## Verdict

`partial`（部分通过，交付尚未完整通过）。

中文含义：审计报告对 SP-001 未完成、registry 漂移、S-012 card 无效、active authority 断链与 public candidate blocked 的主要判断及 claim boundary 大体忠实；公共残留、SP-001、引用与其他质量审计四个面均有实际覆盖。但原始要求中的“可筛选 HTML”存在可复现的字段筛选与 Source view 数据缺失，当前不能声明全景/审计交付整体 `pass/done`。

这不支持仓库质量通过、SP-001 完成、S-012 完成、公共候选就绪、已提交或已发布。Builder 完成上述 HTML/data contract 修复并通过独立 delta validation 后，才可重新评估本交付是否 `pass`。
