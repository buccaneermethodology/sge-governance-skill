# SP-001 S-015 显式 Promotion 前独立 Validation

## 任务理解

本轮不是判断 SP-001 是否完成，而是判断三份仍标为 `reviewed_candidate` 的 repo-local strategy，是否已经满足进入一次显式 `reviewed_candidate → active` 状态变更的前置条件。`reviewed_candidate` 表示候选内容已完成当前语义复核但尚未成为 active truth；本报告即使通过，也不证明 promotion 已执行、promotion 后 diff 已验证、SP-001 已关闭、公共发布已获准或生产成熟。

Reviewer posture：独立、read-mostly Validation；唯一写入为本报告，未修改 Builder、KB、Dashboard 状态或其他证据。

## Read Manifest（读取清单）

### 已读取并重算

- Authority 与原始范围：[Final Loop Goal](SP001_SGEGovernanceMigration_LoopGoal.md)、[Goal Patch](SP001_QualityRecovery_GoalPatch.md)、[最终 OPCM 与 Scope Delta](SP001_S015_FinalClosure_OPCM.md)、[S-015 候选 closeout](SP001_S015_FinalClosure_Closeout.md)。
- Validation baseline 与 semantic delta：[首轮独立 Validation](SP001_S015_FinalValidation_Round1.md)、[首轮 Semantic Review](SP001_S015_SemanticReview_Round1.md)、[Semantic blocker delta](SP001_S015_SemanticReview_Delta.md)、[Topology reconciliation](SP001_S015_SemanticReview_TopologyReconciliation.md)。
- Session 与 topology evidence：[S-012 closeout](SP001_S012_QualityRecovery_Closeout.md)、[S-013 closeout](SP001_S013_SemanticGovernance_Closeout.md)、[S-014 closeout](SP001_S014_ToolchainQuality_Closeout.md)、[Builder Agent Log](../../Agent_Logs/2026-09-02__SP-001-S012-S014__builder.md)。
- ERBE 与工具证据：[frozen Contract](SP001_QualityRecovery_ERBE_Contract.json)、[frozen Cases](SP001_QualityRecovery_ERBE_Cases.json)、[durable RED report](SP001_QualityRecovery_ERBE_RED_Report.json)、[Doctor Report](SP001_S015_DoctorReport.json)。
- KB truth candidate 与派生阅读面：[`strategy_human_ai_development.json`](../../../kb/data/strategy/strategy_human_ai_development.json)、[`strategy_semantic_surface_engineering.json`](../../../kb/data/strategy/strategy_semantic_surface_engineering.json)、[`strategy_kb_promotion_and_source_policy.json`](../../../kb/data/strategy/strategy_kb_promotion_and_source_policy.json)及 `kb/docs/strategy/` 对应 Markdown。
- 当前控制面：`Dashboard/Current_State.md`、`Dashboard/Stage_Plans.md`、`Dashboard/Sessions.md`、`Dashboard/Session_Index.md`、`Dashboard/Archives/Sessions/archive_manifest.json`。
- 当前工作树：`git status --short`、`git diff --stat`、`git diff --name-status`、`git diff --numstat` 与 `git diff --check`；观察到 30 个 tracked modified surface 和 51 个 untracked surface。本 verdict 绑定该 inventory，不覆盖后续 promotion 写入。

### 缺失、跳过或时序上尚不存在

- `SP001_S015_FinalValidationReview.md`、`SP001_S015_SemanticReview.md`、`SP001_S015_PostCloseoutReconciliation.md` 尚不存在；它们是 promotion 后状态收束与最终关闭证据，不是本次 pre-promotion decision 的先决产物。
- 未读取或操作 remote、global Skill、release/provider/production surface；本 Goal 未授权这些动作，它们也不属于本 verdict。

## 首轮 blocker 关闭矩阵

| Round 1 blocker | 独立重算证据 | 当前 disposition | 对 promotion 的影响 |
| --- | --- | --- | --- |
| `VAL-B01 final semantic artifact` | [Semantic delta](SP001_S015_SemanticReview_Delta.md)关闭 B01-B03；[Topology reconciliation](SP001_S015_SemanticReview_TopologyReconciliation.md)将 B04 判为 `closed-with-bounded-exception`，并给出两个可定位 verdict | `closed`，中文含义是 taxonomy、candidate state、Graph ontology 与 topology disposition 都已有 durable 独立复核 | 不再阻止显式 promotion |
| `VAL-B02 OPCM closeout language` | 对 OPCM 与候选 closeout 分别运行 closeout-language gate，均 exit 0 | `closed`；英文 status/verdict 已有中文含义和边界 | 不再阻止显式 promotion |
| `VAL-B03 topology disposition` | [Builder Agent Log](../../Agent_Logs/2026-09-02__SP-001-S012-S014__builder.md)、三份 Session closeout、OPCM 与候选 closeout一致记录 task=`/root`、缺失独立 Builder lane/card、原因、风险、补偿和 claim ceiling | `closed-with-bounded-exception`；整体 multi-agent 不等于独立 Builder conformance，且原 Goal 未要求独立 user-visible Builder task，所以不是需追溯人类批准的 topology Scope Delta | 例外必须继续保留，但不阻止 promotion |
| `VAL-B04 durable ERBE RED evidence` | frozen Contract/Cases 与 [durable RED report](SP001_QualityRecovery_ERBE_RED_Report.json)使用同一 `contract_id=sp001-quality-recovery-v1` 和 `QR-RED-01..06`；本轮 `--phase red` 重算得到 `contract_verdict=valid`、`execution_verdict=ok`、六项 `trusted_red` | `closed`；环境/路径错误未被冒充 RED | 不再阻止显式 promotion |
| `VAL-B05 tombstone claim boundary` | [design tombstone](Tombstones/Removed_Audio_Transcriptor_Design.md)只提供 Git locator；OPCM 的 MH-07、S001-AC-03、SD-03 明确不再主张 current-byte equality | `closed`；历史字节 witness 与当前内容存在性已经分离 | 不再阻止显式 promotion |
| `VAL-B06 dynamic reference evidence` | 本轮 doctor 动态重算 `checked_references=530` 且 `pass`；候选 closeout 不再固定陈旧 reference count | `closed` | 不再阻止显式 promotion |
| post-closeout 未执行 | `quality_recovery_erbe.py --phase full` 当前以 `QR-GREEN-01=fail` 精确列出三个终态 artifact 尚缺；候选 closeout 也保持 `goal_terminal=false` | `expected downstream blocker`，中文含义是 SP-001 终态仍被正确阻断；若把它提前要求为 promotion 前置条件，会形成“先完成才能 promotion”的循环 | 不阻止本次 promotion，但继续阻止任何 Done/complete 主张 |

## 原始 Goal、OPCM 与 Scope Delta 覆盖

- MH-01..MH-15、S001-AC-01..03、PROC-01..02 在 OPCM 中均有独立行，包含可观察判定、精确源文件、实际结果、状态、例外、owner/时序、claim ceiling 与 parent/Closeout 吸收状态；本轮没有只验证三份 revised candidate。
- SD-01..03 均有来源、原因、影响与批准边界；未发现新的未登记 scope deletion、replacement、降级或 authority substitution。
- MH-09 的 Builder topology 不是完整独立 Builder conformance；其有界 `Single-Agent Exception` 仍是事实，不因本 verdict 消失。
- MH-10、MH-15 和 PROC-02 仍处于 final/promotion 后证据未吸收状态。因此本 verdict 不能被解释为 Goal/SP complete。

## Tests 与 gates

| 命令 | 结果 | 证据边界 |
| --- | --- | --- |
| `python3 kb/tools/render_kb.py --check` | exit 0；5/5 manifest documents | 证明 candidate JSON 与派生 Markdown 一致，不单独证明 semantic correctness |
| `python3 Dashboard/tools/doctor.py --repo .` | exit 0；总 verdict `pass`；4/4 tests；530 references；39 public-identity files；registry、KB、DKG、genericity、trusted RED 均 pass | 证明当前定义的 repo-local test/structural gates，不证明 promotion 已执行或 SP-001 complete |
| `python3 Dashboard/tools/session_registry.py reconcile --repo . --check` | exit 0；15=9 current+6 archive，无 drift | 证明 registry projection 一致，不证明 Session/Goal completion |
| `python3 Dashboard/tools/session_registry.py validate --repo .` | exit 0 | 同上 |
| `python3 Dashboard/tools/quality_recovery_erbe.py --phase red` | exit 0；6/6 `trusted_red` | 证明冻结 negative cases 以预期 fingerprint 失败 |
| `python3 Dashboard/tools/quality_recovery_erbe.py --phase full` | exit 2；`execution_verdict=blocked`，QR-GREEN-01 因三个终态 artifact 缺失而 fail | 正确阻止最终关闭；不是 pre-promotion failure |
| 两个 closeout-language gate | exit 0 | 证明当前 OPCM/closeout 的中文可读性，不替代技术 verdict |
| `git diff --check` | exit 0 | 仅证明 diff whitespace 基线通过 |

## KB / Dashboard truth split 与 SGC v1

- 三份稳定策略的候选内容位于 `kb/data` JSON，`kb/docs` 是确定性 projection；来源裁决、Agent Log、doctor、OPCM、closeout 与本报告留在 Dashboard execution/evidence 层，未见 Dashboard 反向替代 KB truth。
- SGC strongest claim level：`structurally_supported`，中文含义是当前 repo-local contract、truth placement、独立 semantic/validation evidence 与 deterministic gates 足以支持“允许一次显式 promotion step”；不支持外部适用性、release 或 production claim。
- Forbidden collapses 均保持分离：schema/render 不等于 semantic correctness，doctor 不等于 independent Validation，candidate eligibility 不等于 active/approved/released，pre-promotion pass 不等于 promotion 后 diff pass，Session evidence 不等于 SP-001 complete。
- SI-1..SI-6：truth carrier、grounding、decision surface、非同义反复验证、authority/write coupling 与 original objective coverage 在本次有界 decision 中均可定位；最终 completion 仍由 QR-GREEN-01 和后续独立对账 fail closed。

## 非阻断 finding

候选 closeout 和 OPCM 仍写 `38 files`，而本轮 doctor 与 durable Doctor Report 均为 `public_identity.checked_files=39`。这不是 semantic promotion criterion，也不改变扫描 verdict，因此不阻止一次显式 promotion；但它是 reader-facing final inventory drift，Builder 必须在 promotion 后最终证据刷新中改为动态表述或当前计数，并让 post-promotion Validation 读取修复后的实际文件。不得用本 finding 扩大为新的未来 hardening scope。

## Required Builder next step（Builder 下一步）

只允许以下有界步骤：

1. 将三份已复核 JSON 的 `status` 从 `reviewed_candidate` 显式改为 `active`：Human-AI、Semantic Surface、KB Promotion and Source Policy；不得同时扩大内容、runtime、schema、acceptance、public 或 release scope。
2. 通过 `kb/tools/render_kb.py` 重新生成三份阅读面，并重跑 `render_kb.py --check`、doctor、registry check/validate 与 `git diff --check`。
3. 刷新 reader-facing final evidence 中已经漂移的 public identity count，但不得借此改写历史 verdict 或隐藏 Builder topology 例外。
4. 创建新的 digest-bound、read-only promotion 后 delta Validation，使独立 reviewer 覆盖状态写入、派生 Markdown、当前 Dashboard/KB、完整 post-promotion diff；只有该 verdict 通过后，才能继续状态收束与 post-closeout reconciliation。

本报告不授权直接写 SP-001、S-012..S-015 或 BI-001 为 `Done`。

## 验证交接包

- Claimed scope：只判断三份 `reviewed_candidate` 是否允许进入显式 promotion step；不执行 promotion，不关闭 SP-001。
- Evidence：原始 Goal/OPCM、Round 1 blocker closure、Semantic delta/topology reconciliation、三份 candidate KB、ERBE、doctor、registry、语言门和完整工作树 inventory。
- Known risk：public identity reader-facing count 为 38，而动态重算为 39；该 drift 必须在 promotion 后证据刷新中修复。
- KB/Dashboard impact：本 Validation 只新增 Dashboard evidence；没有修改 KB truth 或 Dashboard state。
- `Closeout language verdict`：`pass`，中文含义是本报告的中文标题、英文状态词、判断影响、证据边界和下一步均可独立理解；该语言判定将在写入后由 executable gate 重算，且不替代技术 verdict。

## Verdict 与主张上限

`pass-for-explicit-promotion-step-only`，中文含义是“只允许进入一次显式 promotion 步骤”，不表示 promotion 已执行或 SP-001 已完成。

中文含义：Round 1 中与 promotion eligibility 直接相关的 blocker 已由 durable evidence 关闭；当前三份 `reviewed_candidate` 允许进入一次明确、窄范围的 `active` promotion 写入。该 verdict 不等于 promotion 已完成，也不等于 promotion 后状态已验证。

仍然禁止的主张：`SP-001 Done`、`Goal complete`、`active promotion completed`（在写入与 post-promotion Validation 前）、独立 Builder conformance、public-ready、released、production-ready 或普遍跨 repo 适用。

Promotion 后若新增内容变化、truth placement 变化、未登记文件或 diff 超出上述窄范围，必须 rebaseline；不得复用本 pre-promotion verdict 覆盖新的工作树。
