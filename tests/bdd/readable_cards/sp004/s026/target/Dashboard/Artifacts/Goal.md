# 最小 Goal：项目说明示例

这是独立 Codex UAT 在公开新手指南第 6 步选择的最小文档任务。目标是在 fresh target 创建一份中文项目说明 `PROJECT_NOTE.md`，完成一个 Session `UAT-S001` 的 Design、Builder、独立 Validation 与中文 closeout。

## 原始范围与验收

| ID | 原始 must-have | 可观察验收 | owner/时序 |
| --- | --- | --- | --- |
| M1 | 项目说明文档 | PROJECT_NOTE.md 含项目目的、使用步骤、边界三个中文标题；步骤引用真实 target AGENTS 与 profile；不声称产品或发布完成 | Builder 在 Design 后 |
| M2 | 冻结设计与范围 | 独立 Design 保存设计、明确写入范围与预期文件 | Design 在 Builder 前 |
| M3 | 一个 Session 及验证交接 | Sessions 有 UAT-S001；Builder 保存 Handoff，列出 actual files、变化与验证要求 | Builder 后 |
| M4 | 独立验证 | 新上下文 Validation 从 Goal、Design、文件、Handoff 与实际 closeout 重算；正例存在、负例说明不会把文件缺失判通过 | Validation 独立于 Builder |
| M5 | 中文收束与最终状态 | 中文 Closeout 引用独立 Review；language gate 通过；最终 Dashboard/KB 状态由独立 reconciliation 覆盖 | Closure 后 Validation |

## 任务边界

目标 authority 为 [AGENTS](../../AGENTS.md) 与 [profile](../../kb/data/strategy/profile.json)。只创建本地示例文档与执行证据；不修改 core、profile、源仓规则；无 provider、release、远端、产品实现、semantic promotion。ERBE applicability=not_applicable：示例说明文档不改变状态机、acceptance 或 runtime；既有 SGC 与验证原则保持不变。最大主张是本地示例文档完成；UAT 是否满足外层 S-026 由外层独立审核另判。

## 执行与终止

Read Manifest：公开 README、Quick Start、新手指南；已安装 core Skill/checklists；target AGENTS、profile；无来源任务聊天。Scope Delta 初始为无；每条 M1..M5 必须逐项对账。流程为 Intake/Context → Design → Builder → Closure draft → 独立 Validation → Closure final → 独立 reconciliation。各 lane 使用 render 生成提示与 digest 校验，fork_context=false。允许使用 subagents；主任务仅协调与证据采集。

Validation Handoff 须含原始 Goal、Design、实际文件、closeout、最终状态、diff/inventory、语言门与 claim ceiling。Semantic Reviewer 本例不触发：无 truth、authority、acceptance 或 runtime 变化；如出现扩宽则重新评估。KB 无稳定规则变更，Dashboard 记录 UAT-S001 执行；例子不自创 Session registry 工具。

只有 M1..M5 全满足且独立最终审核覆盖最终文件时，示例 Goal 才能完成；否则记 partial/blocked 并保留未满足项。Session closeout 不是自动终止点；无待办 Session 且全部验收满足才结束。禁止将此例的成功写成完整 S-026 UAT、通用 newcomer readiness、发布或生产就绪。
