# 仓库能力全景独立最终验证

## 任务理解

本任务要验证的是：当前 checkout 上的 JSON、Markdown、HTML、审计报告、生成器与 closeout 是否共同形成一份可重算、证据有界的仓库能力全景。它最多能证明当前本地结构与已运行门禁范围内的质量状态，不能证明公开仓已存在、权利已批准、版本已发布、跨平台兼容或 production readiness。

## Read Manifest 与证据完整性

- 已读：原始目标投影与 Context Bootstrap、AGENTS、repo checkpoint Skill 及其 Validation/SGC/context-efficiency 规则、SGC v1 canonical JSON、Design、全部 panorama 输出、Generator、Closeout、lane cards/prompts/audit、README、public manifest、Dashboard Current State/Stage Plans/Sessions、Git 最终 inventory。
- 已独立重算：Lane Task Card 摘要、JSON parse/required keys/ID uniqueness/source refs、HTML 内嵌 JSON 与离线性、Markdown links、CLI `--help`、repository doctor、27 个 unittest、public doctor、registry reconcile/validate、KB render check、closeout-language。
- 缺失/不足：最终 package 的能力清单没有显式 core Skill 条目；Generator 不是从当前 source snapshot 动态采集关键身份和质量计数，导致最终 checkout 与报告记录不一致。

## Blocking Findings

### B-01：能力清单没有实现其声称的“一个真实 core Skill”与十二类覆盖

- [Design](RepositoryCapabilityPanorama_Design.md) 的 `PAN-DESIGN-01` 要求明确“一个核心 Skill、多项能力、可选扩展非实现”，并把漏掉任一能力族列为失败条件。
- 独立解析 [Data JSON](RepositoryCapabilityPanorama_Data.json) 得到 67 个唯一 capability，但 `kind` 中没有任何 `core_skill`；实际只有 10 个 family。它列出了治理能力、工具、schema、KB、Dashboard、文档和测试，却没有把 `.codex/skills/sge-governed-checkpoints/SKILL.md` 本身作为 core Skill 条目。
- [Closeout](RepositoryCapabilityPanorama_Closeout.md) 第 21 行仍声称“1 个真实 core Skill；67 个分层能力/证据条目”且状态为 `landed`，该结论没有被 JSON/HTML 数据支撑。
- admissibility：直接违反 `PAN-DESIGN-01`、原始“列出所有 Skills 或能力”must-have 与 evidence integrity，因此阻断当前 package 的通过结论。

### B-02：最终质量快照不可按当前 checkout 重算，报告计数已经漂移

- [Audit Report](RepositoryCapabilityPanorama_Audit_Report.md) 第 13 行记录 repository doctor 为 `160 JSON / 23 Python`；本次独立重跑在同一 HEAD `55da8debbb48bd7c10ec6f37bce02b621ba6d610` 得到 `167 JSON / 24 Python`，其余 1248 refs、27 tests 和 gate verdict 仍通过。
- [Generator](RepositoryCapabilityPanorama_Generator.py) 第 185-207 行硬编码生成日期、短 HEAD、worktree 描述、source manifest、质量观察与 Dashboard entity 数量；它不会从当前 checkout 采集这些事实。因而“同一 checkout 可重算”和“当前 checkout 的最终质量状态”不能由该 Generator 建立。
- [Design](RepositoryCapabilityPanorama_Design.md) 的 `PAN-DESIGN-02` 要求实际命令证据，`PAN-DESIGN-04` 要求 Validation 可从 source snapshot 重算并绑定最终 diff；当前 package 仍引用生成中间态计数，未绑定最终 28 个 untracked panorama artifacts。
- admissibility：违反当前 AC、最终状态绑定与 SGC SI-2/SI-4/SI-5，因此阻断最终通过；这不是“还可以更严格”的未来 hardening 建议。

## Non-Blocking Findings

- HTML renderer 会在内嵌 JSON 中补 `generated_on`、空 `stage_plans` 以及每个 session 的空兼容字段，因此与 Data JSON 不是 byte/object exact equality；核心 capability/audit/finding 数据未见实质差异。该 normalization 符合 renderer 的兼容输入行为，单独不作为 blocker，但修复后应记录允许的 projection normalization。
- Closeout 已如实把公开发布保持为 `candidate_not_approved`，并明确 rights、远端、跨平台、完整 Codex UAT 与 production readiness 未获证明；这些是正确的 claim ceiling。

## 原始目标覆盖与 Scope Delta

| 原始要求 | 当前观察 | 状态 | 完成影响 |
| --- | --- | --- | --- |
| 生成 Markdown/JSON/可筛选 HTML 全景 | 三种文件存在、可解析、链接可定位、HTML 离线；存在 renderer normalization | landed-with-finding | 不单独阻断 |
| 列出全部 Skill 或能力 | 67 个条目中没有 `core_skill`，仅 10 个 family；与“一个 core Skill/十二类”声称冲突 | blocked | 阻断 |
| 评估仓库当前质量 | 关键 gates 独立通过，但报告计数不是最终 checkout，Generator 不能动态重算 | blocked | 阻断 |
| 检查 Skill 干净度与 Semx 残留 | public/core 与历史 provenance/fixture 已分层，未见发布越权措辞 | landed-with-bounds | 支持有界结论 |
| 评估开源缺口 | P0/P1/P2、rights 与 authority gap 已列出 | landed | 不证明发布就绪 |
| 小白 Skill 使用指南 | CLI 参数与本次 `--help` 一致；完整 Codex newcomer UAT 明示未运行 | landed-with-bounds | 仅候选指南 |
| 发布操作指南 | 外部 mutation 前置人类授权，未实际执行 | landed | procedure-only |

`Scope Delta` 未见删除或批准外替换；当前问题是产物未满足原始 must-have，而不是范围变更。

## 测试与门禁充分性

- 通过：Validation Lane Task Card、Context Bootstrap、repository doctor、27/27 unittest、public doctor、registry reconcile/validate、KB render check、closeout-language、JSON/link/offline/source-ref 检查。
- 未支持通过：能力全集语义覆盖、动态 source snapshot freshness、最终 package 对最终 diff 的一致绑定。
- 最强可支持 claim：局部门禁为 `test_bound`，结构/链接检查为 `structurally_supported`；整个 panorama package 当前不能称 `validated` 或 `done`。

## SGC v1 与 truth split

- SI-1：文件/字段存在不能替代“全部能力”语义覆盖；B-01 未满足。
- SI-2：部分质量观察缺最终 snapshot grounding；B-02 未满足。
- SI-3：KB canonical truth、Dashboard execution memory、派生 HTML/JSON 的分层正确。
- SI-4：已做独立重算，但重算揭示 Generator 自身硬编码快照；当前 package 不能靠自生成输出自证。
- SI-5：Closeout 尚保持 Validation `pending`，没有把本地 gate 外推为发布；但若改成最终通过会超过证据。
- SI-6：原始能力全集与当前质量两项尚未落地，因此完整目标未覆盖。

## Required Builder / Closure Repair

1. 在统一 JSON 中增加真实 `core_skill` 条目，并按 Design 明确映射/覆盖十二类能力族；同步重生成 Markdown/HTML，修正 Closeout 的实际结果。
2. 将 branch、完整 HEAD、dirty inventory、文件计数、Dashboard entity 数量和 gate observations 改为从当前 checkout/durable evidence 采集，或显式绑定一份带 digest 的冻结 source snapshot；重生成 Audit/JSON/Markdown/HTML。
3. 修复后使用新的 lane card/digest 发起 delta Validation；最终 reviewer 必须再次读取实际 closeout、最终 Dashboard/KB 状态与最终 diff。

## Verdict

`blocked`（阻断）。这表示当前 package 的大部分门禁和阅读面可用，但两个当前合同 blocker 使它不能获得最终 `pass/done`：能力全集缺少 core Skill 条目，且质量快照不能对最终 checkout 可靠重算。正式开源发布仍另受人类 rights 与远端授权阻断。
