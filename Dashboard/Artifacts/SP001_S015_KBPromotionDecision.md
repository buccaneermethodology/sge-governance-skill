# SP-001 S-015 KB 显式 Promotion 决定

## 决定

批准将以下三份 repo-local strategy 的 `status` 从 `reviewed_candidate` 提升为 `active`：

- [Human-AI Development](../../kb/data/strategy/strategy_human_ai_development.json)
- [Semantic Surface Engineering](../../kb/data/strategy/strategy_semantic_surface_engineering.json)
- [KB Promotion and Source Policy](../../kb/data/strategy/strategy_kb_promotion_and_source_policy.json)

`active` 的中文含义是这些经来源裁决、独立 Semantic Review 和 pre-promotion Validation 检查的稳定规则，成为本仓库当前可用的 canonical strategy truth。它不表示公共发布、外部适用性、runtime/schema/acceptance 扩大、生产成熟或 SP-001 完成。

## Authority 与前置证据

- 用户原始质量恢复要求及 [Goal Patch](SP001_QualityRecovery_GoalPatch.md)授权修复 canonical 缺失与 active 引用断链。
- [来源逐节裁决](SP001_S013_SourceAdjudication.md)限制了 migrate/adapt/reject 边界。
- [Semantic blocker delta](SP001_S015_SemanticReview_Delta.md)关闭 taxonomy、candidate-state 与 Graph ontology 问题；[topology reconciliation](SP001_S015_SemanticReview_TopologyReconciliation.md)以有界例外关闭 Builder topology 阻断。
- [pre-promotion 独立 Validation](SP001_S015_PrePromotionValidation.md)给出 `pass-for-explicit-promotion-step-only`，只授权本次三项状态变更、重新渲染与 promotion 后独立 delta Validation。

## 写入边界

- 本步骤只修改三份 JSON 的 `status`，不改变 sections、owner、dependencies、non-goals、claim ceiling、runtime、schema、BDD、acceptance、public packaging 或 release scope。
- `kb/docs` 必须由 renderer 重建，不手工编辑。
- promotion 后实际 JSON、Markdown、Dashboard evidence 与完整 diff 必须接受新的独立 delta Validation；在该 verdict 通过前，不得写 `active promotion completed` 或关闭 SP-001。

## KB / Dashboard 路由

- KB：三份 JSON 承载 active canonical truth，Markdown 只作确定性阅读面。
- Dashboard：本决定、来源裁决、review、doctor、OPCM 与 closeout 继续承载 execution/decision evidence，不反向成为 canonical law。

## 验证交接包

- Required gates：renderer 重建与 `--check`、doctor、registry check/validate、`git diff --check`、promotion 后独立 delta Validation。
- 最大 claim：已作出并写入有界 KB promotion 决定，等待 promotion 后独立验证。
- `Closeout language verdict`：`pass`，中文含义是本决定对 `active`、批准边界、不可推导事项与下一步均有明确中文解释；语言通过不替代技术或独立验证。
