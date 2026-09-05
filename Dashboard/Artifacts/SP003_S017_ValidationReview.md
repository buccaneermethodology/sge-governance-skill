# S-017 独立 delta Validation 复核

## 关键结论中文展开

本轮只复核 S-017 maintainer local deterministic projection 的 delta：card identity、当前 Builder ProjectionEvidence 的 provenance、ProjectionContract 的 S017-AC-01..03/PROC-03、实际代码/测试 diff，以及 fresh-root export/verify 行为。它不扩大到 S-018..S-022、公开仓、远端、release、生产或 SP-003 完成。

本轮唯一 Validation verdict 是：`pass-with-findings`（带非阻断发现的通过）。这表示当前 card 范围内的本地投影行为和 Validation predicate 已由独立证据支持；它不表示 Builder 自报被采纳为独立结论，也不表示 S-017 全 Session、SP-003、批准、发布或生产就绪。

关键结果：Validation lane card 的 renderer expected digest `401785639e6bed9e796e5aff2a40993899e2212103c92f71a7c5ae2dd57ff769` 校验通过；Builder card 的 renderer canonical digest 为 `2154371c200ff9c09ce2395e0448998bf0cc1b8bfb0d83e8f53b1c550e301422`，与当前 [ProjectionEvidence](SP003_S017_ProjectionEvidence.json) 记录的 `expected_card_sha256` 一致；tool digest `3810e8b695c9a9030971f1bfc19237dad438297f1c7b8cc1e932f40565815023` 也与当前实现一致。旧报告将 raw file hash 与 renderer canonical digest混为一谈，因此其 B2 阻断结论不成立。

[ProjectionContract](SP003_S017_ProjectionContract.md) 已提供可定位的 S017-AC-01、S017-AC-02、S017-AC-03 和 PROC-03 定义（第 18-24 行）。因此旧报告的 B3“定义缺失”结论也不成立。

## Read Manifest

### 本轮实际读取并消费

- [S-017 Validation Lane Task Card](SP003_S017_ValidationLaneTaskCard.json)：确认 `delta`、parent snapshot、delta read set、acceptance IDs、最大 claim、禁止动作和唯一 write scope；先执行 renderer expected-card 校验。
- [S-017 Validation Lane Prompt](SP003_S017_ValidationLanePrompt.txt)：确认 card 指定的执行顺序和命令入口。
- [SP-003 Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json)、[Stage Plan](SP003_OpenSourceDistributionArchitecture_StagePlan.md)、[Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md)：确认原始 ODA-MH-01..12、S-017 bounded scope、Session DAG、completion rule 和 claim ceiling。
- [S-016 Design](SP003_S016_Design.md)、[S-016 ERBE Contract](SP003_S016_ERBE_Contract.json)、[S-016 ERBE Cases](SP003_S016_ERBE_Cases.json) 的 C03/INV-02：确认同一 frozen case identity `unknown/private_note.txt`、预期 fingerprint `unknown_path_default_deny` 和 default-deny 约束。
- [S-016 Validation Review](SP003_S016_ValidationReview.md) 与 [S-016 Validation Snapshot](SP003_S016_ValidationStateSnapshot.json)：继承 full baseline、原始目标覆盖和 S-016 blocked 边界；没有把 S-016 的证据缺口重写为 S-017 已完成。
- changed [实现](../../tools/sge_public.py)、[candidate tests](../../tests/test_public_candidate.py)、[projection tests](../../tests/test_public_projection.py)：检查当前 export/verify、unknown source、digest drift 与负例行为。
- [ProjectionContract](SP003_S017_ProjectionContract.md)、[ProjectionEvidence](SP003_S017_ProjectionEvidence.json)、[Builder Lane Task Card](SP003_S017_BuilderLaneTaskCard.json)：检查 AC 定义和 card/tool digest provenance。
- [Dashboard Current State](../Current_State.md)、[Sessions](../Sessions.md)、[KB 双仓策略](../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)：确认状态/稳定 truth 分层；本轮不更新它们。

### 继承、跳过与证据边界

本轮按 `delta` card 复用 parent/full baseline，只扩读 changed surfaces、合同/证据、C03/INV-02、当前 card digest、git 状态和 fresh temporary roots。没有读取或操作 GitHub、remote read-back、credentials/tokens；没有启动或模拟 Builder、Design、Closure lane；没有修改非 write-scope 文件。

## 证据完整性

| 证据项 | 结果 | 说明和边界 |
| --- | --- | --- |
| Validation card renderer | `pass` | card canonical digest 与用户给定 expected digest 一致；只证明 card 结构、引用和 write scope |
| Builder card provenance | `pass` | renderer 输出 `2154371c200ff9c09ce2395e0448998bf0cc1b8bfb0d83e8f53b1c550e301422`，匹配 ProjectionEvidence 的 expected card digest |
| Tool provenance | `pass` | ProjectionEvidence 记录的 tool digest 与当前 `tools/sge_public.py` 一致 |
| ProjectionContract AC | `pass` | S017-AC-01..03/PROC-03 在当前合同第 18-24 行可定位 |
| Focused tests | `14/14` | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_public_candidate tests.test_public_projection` 返回 `Ran 14 tests`、`OK` |
| Doctor | `pass` | `PYTHONDONTWRITEBYTECODE=1 python3 tools/sge_public.py doctor` 返回 `public_doctor:pass` |
| Fresh unknown negative | `pass` | fresh source 的 `unknown/private_note.txt` 命中 `unknown_path_default_deny`，失败前 destination 未创建 |
| Fresh projection replay | `pass` | 48/48 allowlisted files；file-set `26c39a883ca02cd6e0fea87ede6a0ab36989dacd6ce8c07f1074cf6cda1544d`、tree `dee3293a53c8dd2ff335439bd9292f5da98d83c6a6b5ebea478fdc0b540e860b` 均经独立 `hashlib` 重算并由 `verify` 匹配 |
| ProjectionEvidence test count | `pass` | 当前 evidence 已记录 `tests_run=14`，与本轮独立 `14/14` 一致；不把 Builder 自报单独当作 Validation verdict |
| Verify negatives | `pass` | destination 新文件命中 `unknown_path_default_deny`；篡改 `README.md` 命中 `projection_digest_drift` |
| Syntax/diff check | `pass` | 使用不写入 bytecode 的 source compile 检查；`git diff --check` 无输出 |
| Closeout language gate | `not_run` | card write scope 不包含 closeout；因此本报告不支持最终 closeout 或 Done 结论 |

## S-017 AC 与 PROC-03 对照

| ID | 可定位定义 | 本轮独立结果 | 状态与主张上限 |
| --- | --- | --- | --- |
| S017-AC-01 | [ProjectionContract 第 20 行](SP003_S017_ProjectionContract.md:20) | fresh source unknown case 返回 `unknown_path_default_deny`，destination 未创建；fresh positive 完整复制 48 个 allowlisted files | `pass`：只支持本地 projection slice |
| S017-AC-02 | [ProjectionContract 第 21 行](SP003_S017_ProjectionContract.md:21) | `verify` 重新计算 file set、逐文件 digest 和 tree；新增文件/篡改文件分别命中预期 fingerprint | `pass`：不支持批准、发布或远端状态 |
| S017-AC-03 | [ProjectionContract 第 22 行](SP003_S017_ProjectionContract.md:22) | 14 tests 覆盖 symlink/path escape、private/absolute residue、binary/LFS/gitlink/nested repo、dirty tree、destination safety 等负例 | `pass`：仍是当前 threat scope 的本地行为证据 |
| PROC-03 | [ProjectionContract 第 24 行](SP003_S017_ProjectionContract.md:24) | 已读取原始 Goal 与本合同；以 C03 同一 identity 重算；记录 changed files/final diff；本文件与 snapshot 提供唯一 Validation verdict witness | `pass-with-findings`：不把 card/schema/test pass 当作独立 verdict |

## Blocking Findings

无。B2 provenance 阻断不成立：当前 Builder card renderer digest 与 ProjectionEvidence 一致，tool digest 也一致。B3 acceptance grounding 阻断不成立：S017-AC-01..03 与 PROC-03 已在当前 ProjectionContract 中明确定义并可定位。

## Non-Blocking Findings

1. gitlink 覆盖仍是测试 seam（monkeypatched `_gitlink_paths`），不是可提交的真实 gitlink object fixture；当前合同/测试要求已覆盖该 failure fingerprint，但真实对象 hardening 可作为后续工作，不阻断本 card 的既定范围。

## 原始目标覆盖与范围检查

本轮没有删除、替换、降级或延期 ODA-MH-01..12，也没有创建 Scope Delta。局部结果如下：

| 原始要求 | 本轮结果 | 主张上限 |
| --- | --- | --- |
| ODA-MH-01 source-of-truth | 依赖 S-016 设计/策略；本地 projection 不改变方向 | 设计/局部行为边界，不是双仓完成 |
| ODA-MH-02 public boundary | exact allowlist、default-deny、residue/path/object safety 独立通过 | 受限 local projection |
| ODA-MH-03 deterministic pipeline | local export/verify 独立通过；authorized public update/read-back 未执行 | local pipeline partial |
| ODA-MH-04 identity | candidate metadata/file-set/tree identity 可重算 | 不含 projection commit/tag/release |
| ODA-MH-05/06 end-user lifecycle | 未落地，留给 S-018 | 不得由本轮吸收 |
| ODA-MH-07 maintainer/end-user separation | 仅 maintainer side 证据 | 不含 end-user/UAT |
| ODA-MH-08/09 PR、权限与 release | 未落地，留给 S-019/S-020 | 不含 GitHub 或授权 |
| ODA-MH-10 clean-room/UAT/final independent validation | 本轮提供 S-017 local independent Validation；完整 UAT/ERBE 留给后续 | 不含完整 Goal 验收 |
| ODA-MH-11 state-axis separation | metadata 保持 candidate/validated/approved/published/production/Git mutation 分轴 | 不授予任何批准状态 |
| ODA-MH-12 final governed closeout | 未落地，留给 S-022；本轮未运行 closeout-language | 不支持 SP-003 completion |

### Scope narrowing / overclaim 检查

没有未批准 Scope Delta。`pass-with-findings` 仅覆盖 S-017 maintainer local deterministic projection 的 card 范围；禁止解释为 `S-017 Done`、`candidate approved`、`public repository/release completed`、`production-ready` 或 `SP-003 complete`。

## SGC v1 与语义风险

- claim level：focused command 结果为 `test_bound`；fresh-root 独立重算对 local projection slice 提供有界 `structurally_supported` evidence。
- SI-1：不把 card、metadata 或 Builder self-report 当行为真相；行为以本轮 fresh-root/verify 重算为准。
- SI-2：当前 AC、C03 identity 和负例 witness 足够支持本 card；ProjectionEvidence 的 14 tests 记录与本轮独立结果一致。
- SI-3：稳定双仓规则仍在 `kb/`，执行 evidence 仍在 `Dashboard/`；本轮没有 truth promotion。
- SI-4：独立 `hashlib` 与 `verify` 重新计算 file-set/tree 和逐文件 digest，没有用 test pass 掩盖 unknown negative。
- SI-5：candidate、validated、approved、published、production 和 Git mutation 保持分轴；没有远端动作。
- SI-6：ODA-MH-01..12 及 S-018..S-022 remainder 保留，没有把局部结果写成 Goal 完成。

本轮是 read-mostly delta Validation，没有修改 contract、authority、KB 或 acceptance posture，因此不启动 Semantic Reviewer；若后续修改 ProjectionEvidence provenance 或改变 AC/PROC-03 的 authority，应重新评估语义升级并 rebaseline。

## 验证交接包

| 字段 | 当前值 | 中文说明 |
| --- | --- | --- |
| claimed scope | S-017 maintainer local deterministic projection delta | 仅 fresh source/export/verify/negative 行为和 Validation predicate |
| claimed semantic change | 无 | 本轮不修改合同、状态轴、authority 或 promotion policy |
| explicit non-goals | lifecycle、license approval、public repo、GitHub、remote read-back、release、production、SP-003 completion | 均未执行或未被本轮证明 |
| changed artifacts | 仅 [Validation Review](SP003_S017_ValidationReview.md) 与 [Validation Snapshot](SP003_S017_ValidationStateSnapshot.json) | Builder/Contract/tests/KB/Dashboard registry 未由本轮修改 |
| gates/tests | card renderer、SGC、validation-agent、14 tests、doctor、fresh negative、projection verify、source compile、diff check | 各命令的证据边界见上表 |
| known risks | gitlink 为 seam fixture；完整 closeout/UAT/remote evidence 未在本 card | 均不扩大当前主张 |
| KB/Dashboard impact | `kb/` 和 Dashboard registry/session surfaces 不更新 | 本轮只写 card 指定的两个 execution evidence 文件 |
| Closeout language verdict | `not_run`（未运行） | card write scope 不包含 closeout；不能支撑最终 completion wording |

## 写入范围与继续状态

- 本轮只写入 card 指定的 [Validation Review](SP003_S017_ValidationReview.md) 与 [Validation State Snapshot](SP003_S017_ValidationStateSnapshot.json)；未回滚或清理既有工作树变更，未执行远端动作。
- `goal_terminal=false`：SP-003 原始 Goal completion rule 未满足。
- `next_session=S-018`：S-017 局部 Validation evidence 可交接给后续 lifecycle Session；若要改变本地 evidence provenance，应先修复 Builder evidence 并重新做 S-017 delta reconciliation。
- `next_session_ready=true`：在“不扩大到远端/release/生产”的前提下，S-018 入口已由 Stage Plan 定义；这不表示本 Goal terminal。
- `human_decision_required=false`：本轮没有需要人类决定的外部动作；任何 GitHub、权利、权限或 release 决定仍需后续具体 authority。
- `CG skipped: no CG input provided`：本轮没有 CG input，不产生额外结论。

允许的收束措辞是：`S-017 maintainer local deterministic projection 的独立 delta Validation 以 pass-with-findings 通过；14/14 tests、doctor、fresh unknown negative、projection verify 和 S017-AC-01..03/PROC-03 均有本轮证据，gitlink seam 仅是非阻断 hardening 发现，且不支持远端、release、production 或 SP-003 完成。`
