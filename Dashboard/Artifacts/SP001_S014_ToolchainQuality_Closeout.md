# S-014 引用、KB/DKG 与 Doctor 工具链修复 Closeout

## 关键结论中文展开

S-014 已建立单一 fail-closed doctor 入口，并修复 KB renderer、DKG 可选输入和当前/SP-001 evidence 链接。`unittest discover` 现在发现并执行 4 个测试；空 tests root 以 `zero_tests_discovered` 失败，不再允许 0 tests 假绿。

## 落地范围

- [KB renderer](../../kb/tools/render_kb.py)与[render manifest](../../kb/render_manifest_v1.json)：配置 JSON 不再被猜测为文档；普通 render 与 `--check` 共用 adapter。
- [DKG generator](../tools/generate_dashboard_kg.py)：`--repo-root` 和 `--quality-metrics PATH|none` 必须显式提供；`none` 在 metadata 记录 `explicit_none`。
- [doctor](../tools/doctor.py)：JSON parse、Python compile、非零 tests、genericity、registry、KB、references、public identity 与临时 DKG 全部进入总 verdict。
- [repository quality tests](../../tests/test_repository_quality.py)：覆盖空/非空 discovery、public identity 和 reference gates。
- [reference scope](../reference_scope_v1.json)及两个[tombstone](Tombstones/)：历史缺失内容只提供 locator，不伪造正文。
- 修复 S-003 archive anchor、S-005/S-006 source manifest 相对路径和 S-002 runner locator。

## 明确非目标

- Tombstone 不是原内容或当前执行证据，不恢复已删除产品/runner。
- DKG 是 Dashboard read model，不成为 registry/KB/acceptance authority。
- doctor pass 只证明列出的 repo-local gate，不证明公共发布、普遍适用性或生产成熟性。

## Lane 启动与例外

- 工具链 Design lane 使用 [digest-bound card](SP001_S014_ToolchainDesign_LaneTaskCard.json)，先复现 QR-RED-03/04/05，再给出 render manifest、显式 DKG、tombstone 和 fail-on-zero-tests 设计。
- Builder 采用显式 adapter，而不是对 `sections` 做隐式启发式分类。
- 历史 Markdown 的链接修改只改变 locator；原 verdict、摘要和时序不改写。
- Builder 由 Orchestrator 在共享工作树集中执行；缺少独立 Builder lane/task/card 已在 [Builder Agent Log](../Agent_Logs/2026-09-02__SP-001-S012-S014__builder.md)记录为有界 `Single-Agent Exception`。其补偿门禁包括独立工具链 Design、最终 Validation/Semantic、ERBE、doctor 与完整 diff 复核。

## 验证交接包

- 当前 doctor：`pass`；全部 gate（含 ERBE trusted RED）通过，tests `discovered_count=4`、`executed_count=4`。
- Required negative evidence：空 tests root=`zero_tests_discovered`；缺 manifest source/输出、缺显式 quality input、broken active link 和 public identity residue 均 fail closed。
- `Closeout language verdict`：`pass`，中文含义是本文 H1/H2 与英文 verdict/status 均有中文解释；独立 reviewer 仍须对实际最终版本重算。
- 最大 claim：S-014 Builder 候选通过当前 doctor；最终状态仍由 S-015 独立 Validation 绑定。

## KB / Dashboard 复核

- KB：renderer manifest 与阅读面属于 canonical projection contract，已更新。
- Dashboard：doctor、reference scope、DKG 和历史 locator 属 execution/tooling evidence，已更新。
- Contract Delta Scan：public packaging/license 属 `deferred SP-002`；不因 doctor pass提前进入 public claim。

## 终止扫描

- `goal_terminal=false`
- `next_session=SP-001/S-015`
- `next_session_ready=true`
- `human_decision_required=false`
