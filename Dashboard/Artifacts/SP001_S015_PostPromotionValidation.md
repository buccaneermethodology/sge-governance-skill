# SP-001 S-015 Promotion 后独立增量验证

## 任务理解与主张边界

本轮验证三份 repo-local semantic-governance strategy 的显式 `reviewed_candidate → active` promotion 是否按批准边界写入、正确渲染且没有 semantic/scope widening。`active` 只表示当前仓库内可用的 canonical strategy truth；不表示 SP-001 完成、公共发布、普遍跨仓库适用或生产成熟。

Reviewer 为独立、read-mostly Validation；唯一写入是本报告，没有修改 Builder、KB、Dashboard state 或其他 evidence。

## Read Manifest（读取清单）

已读取并重算：

- [Pre-promotion Validation](SP001_S015_PrePromotionValidation.md)与[显式 Promotion Decision](SP001_S015_KBPromotionDecision.md)。
- 三份 promoted JSON：Human-AI、Semantic Surface、KB Promotion and Source Policy，以及三份对应 Markdown projection。
- [最终 OPCM](SP001_S015_FinalClosure_OPCM.md)、[候选 closeout](SP001_S015_FinalClosure_Closeout.md)、[Doctor Report](SP001_S015_DoctorReport.json)。
- Builder topology exception 的 [Agent Log](../Agent_Logs/2026-09-02__SP-001-S012-S014__builder.md)与 Semantic topology reconciliation。
- 当前 Dashboard parent/session surfaces、`git status`、tracked/untracked inventory、完整 tracked diff 与 `git diff --check`。
- 独立重跑 doctor、registry check/validate 和 `render_kb.py --check`。

未将 remote、release、global Skill 或 production surface 作为证据；这些不在本 Goal 授权范围。当前三个 promoted JSON/Markdown 是 untracked candidate surface，因此 tracked `git diff` 本身不能展示它们的 pre/post 字节差；本轮使用 pre-promotion Semantic card 固定的三个候选摘要做同 identity 虚拟还原比较，避免把“看见 active”当作无扩大证明。

## Promotion AC 重算

| AC | 独立观察 | Verdict | 证据边界 |
| --- | --- | --- | --- |
| `PROMO-01` | 三份目标 JSON 均为 `status=active`；对应 Markdown metadata 也均为 `Status: active` | `pass`，中文含义是批准的三项状态写入存在 | 不关闭 SP-001 |
| `PROMO-02` | `render_kb.py --check` 对 5/5 manifest documents 通过；三份 JSON/Markdown status 一致 | `pass` | 只证明确定性 projection parity |
| `PROMO-03` | 将当前三个 JSON 的第一处 `status: active` 虚拟还原为 `reviewed_candidate` 后，SHA-256 分别精确等于 Semantic delta 固定摘要 `b7ee95...`、`907f2a...`、`8ce14a...` | `pass` | 证明 promotion 只改变三处 status，没有 sections、owner、dependency、non-goal 或 claim ceiling widening |
| `PROMO-04` | Promotion Decision 明确 authority、三项目标、状态含义、write exclusions、KB/Dashboard routing 和 post-promotion Validation requirement | `pass` | Decision 是 promotion evidence，不替代 KB truth 或 final Goal verdict |
| `PROMO-05` | 当前 doctor 总 verdict=`pass`；4/4 tests、registry、KB、DKG、genericity、references、identity 与 ERBE trusted RED 均通过 | `pass` | test/structural evidence，不证明 release/production |
| `PROMO-06` | OPCM 与 closeout 均刷新为 public identity `39 files`；当前 doctor 同样重算为 39 | `pass` | 只覆盖定义的 public identity scope |
| `PROMO-07` | Agent Log、OPCM 和 closeout 继续保留有界 `Single-Agent Exception`、风险、补偿和“不证明独立 Builder conformance”的 claim ceiling | `pass` | promotion 没有抹除实际 topology exception |

## Promotion diff 与无扩大判定

Promotion Decision 只授权三份 JSON status 变化、renderer 重建和 reader-facing count 刷新。独立检查结果：

- 三份 JSON 除 status 外与固定 `reviewed_candidate` 候选逐字节一致。
- 三份 Markdown 由当前 JSON 确定性生成，未见手工 projection drift。
- OPCM/closeout 的 39-file refresh 与当前 doctor 一致。
- promotion 没有新增 runtime、schema、BDD、acceptance、provider、CLI、public packaging 或 release 行为。
- Dashboard 的 SP-001/S-012..S-015 parent/session state 仍未被提前收束为 Done。

`promotion_diff_verdict=pass_for_three_status_changes_and_derived_projection_only`，中文含义是只确认批准的三项 active 状态及其派生阅读面，不把整个工作树或 Goal 判为完成。

## Doctor、registry 与 reader-facing evidence

- 当前独立 doctor：`pass`；references=562、public identity files=39、tests=4/4。
- Durable Doctor Report：`pass`（通过）；中文含义是报告记录的全部 repo-local gates 无失败项，references=562、public identity files=39、tests=4/4。
- Registry check/validate：均为 `pass`；15 records = 9 current + 6 archive，无 drift/collision。
- KB render：5/5 check passed（检查通过）；中文含义是 manifest 内五份阅读面与 canonical JSON 的当前渲染结果一致。
- ERBE RED：QR-RED-01..06 均为同 contract identity 的 `trusted_red`，`contract_verdict=valid`、`execution_verdict=ok`。
- `git diff --check`：通过。

Doctor Report 与当前重算的关键计数和 verdict 一致；临时 DKG 输出路径不同不构成 semantic drift。

## Truth placement 与 SGC v1

- 三份 `active` JSON 位于 `kb/data`，承载当前 canonical strategy truth；Markdown 是 derived reading surface。
- Promotion Decision、OPCM、closeout、Agent Log、doctor 与本报告位于 Dashboard execution/decision/evidence 层，没有反向成为 semantic law。
- Strongest claim level：`test_bound + structurally_supported`，只支持当前 repo-local promotion 写入与 projection 一致性。
- Forbidden collapse 保持分离：active truth 不等于 public release；render/doctor 不等于普遍 semantic correctness；promotion pass 不等于 Goal complete；有界 topology exception 不等于独立 Builder conformance。
- SI-1..SI-6 在本 promotion delta 内满足：truth carrier、grounding、decision surface、独立重算、authority/write coupling 与原始 Goal 边界均可定位。最终 completion 仍须后续证据。

## Blocking 与 non-blocking findings

本 promotion scope 内没有 blocking finding，也没有需要 Builder 修复的 promotion defect。

非阻断边界：当前完整工作树仍包含大量 tracked/untracked Goal artifacts；本报告只绑定 card 指定的 promotion delta 和当前 inventory，不把其余历史/实现面重新判为全部完成。

## 最终状态关闭前的剩余阻断项

Promotion 验证通过后，SP-001 仍不能关闭。至少仍需：

1. durable final integrated Validation 与 Semantic evidence 覆盖 promoted KB、实际 closeout/OPCM、最终 Dashboard 和完整 diff；本 post-promotion delta 不替代这些终态 artifacts。
2. 按 completion workflow 执行 S-012..S-015、SP-001 与 BI-001 的受控状态收束，并重跑 registry、doctor、语言门和 ERBE GREEN。
3. 状态/closeout/Artifacts Index 最终化后，执行独立 post-closeout reconciliation；其 verdict 必须覆盖 mutation 后实际文件，不能复用本 mutation 前 verdict。
4. QR-GREEN-01 只有在 final Validation、Semantic 与 post-closeout artifacts 实际存在且内容一致时才能通过。

## Builder 必需修复

无需修复本次 promotion 写入。下一步仅允许按 frozen completion workflow 生成终态证据与受控状态 mutation；若后续修改三份 active strategy 内容或 promotion boundary，必须重新触发 Semantic Review 和 rebaseline，不能复用本 verdict。

## 验证交接包

- Claimed scope：三份 strategy active promotion、三份 Markdown projection、decision evidence、39-file refresh 与 topology exception retention。
- 不证明：SP-001/S-012..S-015/BI-001 Done、release、public-ready、production-ready 或独立 Builder conformance。
- 当前 verdict：`pass-for-post-promotion-delta-only`。
- `Closeout language verdict`：`pass`，中文含义是本文对 active、promotion pass、Goal completion 与后续状态 mutation 的差异提供了中文解释；语言通过不替代最终集成 Validation 或 post-closeout reconciliation。

## Verdict 与允许措辞

`pass-for-post-promotion-delta-only`，中文含义是：三份 strategy 的显式 active promotion、派生 Markdown、promotion decision、39-file count、doctor/registry 与 topology exception retention 均通过独立复核；没有发现 promotion scope 内的 semantic 或 authority widening。

当前允许措辞：

> 三份 repo-local semantic-governance strategy 的 active promotion 已按批准边界写入，并通过 promotion 后独立 delta Validation；SP-001 最终状态仍等待集成 Validation、受控状态收束和 post-closeout reconciliation。

当前禁止措辞：`SP-001 Done`、`Goal complete`、`public-ready`、`released`、`production-ready`、普遍跨 repo 适用或“完整独立 Builder conformance”。
