# S-021 Clean-room 与用户验收重放

## 关键结论中文展开

本报告记录从当前私有 canonical worktree 生成 fresh projection，再从 projection 目录作为“公开仓 clone”运行 end-user lifecycle 的本地重放。`CR-*` 与 `NEG-*` 只是本地 witness 别名，不是新的 ERBE identity；唯一 frozen identity 是 S-016 的 `C01–C14`。由于工作树包含本 Loop 的未提交 Dashboard 证据，export 使用显式 `require_clean=false` 的测试入口；这保留 dirty-source 边界，不能被解释为生产发布或远端仓同步。

## Read Manifest 与边界

已读取 [Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json)、[Stage Plan](SP003_OpenSourceDistributionArchitecture_StagePlan.md)、[S-016 Design](SP003_S016_Design.md)、[S-016 ERBE Contract](SP003_S016_ERBE_Contract.json)、[S-016 ERBE Cases](SP003_S016_ERBE_Cases.json)、[S-017 Projection Contract](SP003_S017_ProjectionContract.md)、[public manifest](../../public_export_manifest_v1.json)、[projection tool](../../tools/sge_public.py)、[S-019 权限合同](SP003_S019_ReleaseGovernanceContract.md)和 [S-020 回流策略](SP003_S020_ContributionPolicy.md)。本报告只验证声明的本机路径；不验证 GitHub owner、URL、branch、权利或 remote read-back。

## S-021 验收谓词与证据入口

下表把 card 中的验收 ID 固定为可观察的 predicate、expected 和 witness。`ready_for_independent_validation` 的中文含义是证据包已修复并可交给后续独立 Validation 重算，不是独立 Validation 已通过。

| ID | 可观察 predicate | expected | witness 与当前结果 |
| --- | --- | --- | --- |
| S021-AC-01 | 从 fresh source/projection root 重放 export/verify，并以默认 source 完成 install、upgrade、recoverable uninstall；target authority 文件保持原字节 | 正例接受；projection file set/tree digest 可重算；install/upgrade/uninstall 返回声明的成功 fingerprint，且不覆盖 target authority | [S-021 ERBE RED/GREEN](SP003_S021_ERBE_RED_GREEN.json) 的 C01/C02/C09/C10 映射；本文件“实际正例”CR-01..CR-05；[candidate lifecycle test](../../tests/test_public_candidate.py) 的 `test_lifecycle_is_recoverable_and_preserves_authority`。当前为 `bounded_local_witness`，不证明远端或发布 |
| S021-AC-02 | 对 unknown/private、symlink/path escape 与 projection drift 输入执行 fail-closed 检查 | 分别达到 `unknown_path_default_deny`、`identity_or_private_residue`、`unsafe_link_or_path_escape`、`projection_digest_drift`；拒绝不能被其它正例掩盖 | [S-021 ERBE RED/GREEN](SP003_S021_ERBE_RED_GREEN.json) 的 C02/C03/C05/C06 映射；[projection tests](../../tests/test_public_projection.py) 的 `test_destination_safety_unknown_and_digest_drift_fail_closed`、`test_residue_object_and_path_safety_fail_closed`、`test_unknown_source_file_is_default_deny`。当前为 `bounded_negative_witness`，未把未重放的 C04/C08/C11/C12/C14 写成通过 |
| S021-AC-03 | RED/GREEN 的 case inventory 完全复用 S-016 frozen `C01–C14`，本地 alias 显式映射到 frozen case；测试范围、状态轴和 claim ceiling 可由 durable inputs 定位 | RED 与 GREEN 的 identity inventory 相同；本地 alias 不成为 identity；当前命令范围固定为 candidate 8 + projection 6 = 14 tests；没有 `published`、`production_ready`、remote mutation 或 approval 推导 | [S-016 ERBE Cases](SP003_S016_ERBE_Cases.json) 的 C01–C14；[S-021 ERBE RED/GREEN](SP003_S021_ERBE_RED_GREEN.json) 的 `case_identity`、`local_witness_aliases`、`acceptance_criteria`；本文件“测试范围对账”。当前为 `evidence_repaired_pending_independent_validation`，不是 GREEN 或最终 closeout |

## Frozen identity 与本地 witness alias 对账

`C01–C14` 是 S-016 冻结的唯一 identity。下表的 `CR-*`/`NEG-*` 只描述本地操作或负例 witness；空白映射表示本 lane 没有该 frozen case 的行为重放，不能填充或推断结果。

| Frozen case | 本地 alias | alias 的局部含义 | 本 lane 状态 |
| --- | --- | --- | --- |
| C01 | CR-01 | private canonical → fresh projection | 有局部 witness |
| C02 | CR-02；NEG-digest | allowlist/verify 正例；digest drift 是 verify 的局部负例扩展 | 有局部 witness |
| C03 | NEG-unknown | unknown path default-deny | 有局部 witness |
| C04 | — | private execution surface forbidden | 未在本 lane 重放 |
| C05 | NEG-private | allowlisted 内容中的 absolute/private residue | 有局部 witness |
| C06 | NEG-symlink | unsafe link/path escape | 有局部 witness |
| C07 | — | 七个 identity axis 独立记录 | 未在本 lane 重放 |
| C08 | — | candidate 不折叠为 published/production-ready | 未在本 lane 重放 |
| C09 | CR-03；CR-05 | default-source install；recoverable uninstall 的 end-user lifecycle 局部扩展 | 有局部 witness |
| C10 | CR-04 | upgrade 与 target authority 保留 | 有局部 witness |
| C11 | — | public PR 不绕过 canonical return flow | 未在本 lane 重放 |
| C12 | — | CI 不取得 push/tag/release 权限 | 未在本 lane 重放 |
| C13 | — | 具体 human authorization 后才允许 external mutation | 未在本 lane 重放 |
| C14 | — | design handoff 不冒充 execution/release | 未在本 lane 重放 |

## 实际正例

| Local witness alias | Frozen case | 操作 | 观察结果 | 边界 |
| --- | --- | --- | --- | --- |
| CR-01 | C01 | 从私有 source 生成 fresh projection | `exported:48`；metadata tree/file-set identity 可由 verify 重算 | 仅是本机 candidate |
| CR-02 | C02 | `verify` 重新计算 source/destination file set 与 digest | 48 个 allowlisted 文件，verify tree digest 一致 | 不等于独立批准 |
| CR-03 | C09 | 从 projection 根目录运行 `install --target` | `installed:17`，默认 source 生效 | target 需已有 AGENTS.md |
| CR-04 | C10 | 运行 `upgrade --target` | `upgraded:17`，备份目录保留 25 个条目 | 不覆盖 target authority |
| CR-05 | C09 | 运行 `uninstall --target` | `uninstalled_recoverable`，skill 移入 `.sge-trash` | 可恢复删除，不是 destructive purge |

## 负例与测试范围对账

当前 card 的固定命令实际收集两个测试模块：`tests.test_public_candidate` 8 个 test method，加上 `tests.test_public_projection` 6 个 test method，共 `14/14`。这 14 个 method 的完整名称和断言位于 [candidate tests](../../tests/test_public_candidate.py) 与 [projection tests](../../tests/test_public_projection.py)；本 lane 运行命令为：

```text
python3 -m unittest tests.test_public_candidate tests.test_public_projection
```

旧 UAT/历史报告中的 `13/13` 仅保留为旧范围的计数声明，不能与当前 14 个 method 合并成一个结果；当前 S-021 采用可定位的 `8 + 6 = 14` inventory，且没有用总数替代 C01–C14 的 case-level 对账。当前负例 witness 包含 unknown path、absolute/private residue、symlink/path escape、unexpected binary、LFS pointer、nested repo、gitlink、dirty tree、非空/符号链接 destination、unmanaged uninstall 和 projection digest drift；它们分别由测试 method 和上述 alias 映射定位。无 install record 的卸载返回 `uninstall_requires_install_record`，说明用户 target 不会被无记录删除。

## Verdict 与 Claim Ceiling

本 evidence package：`evidence_repaired_pending_independent_validation`，中文含义是 S-021 的 identity、范围和验收入口已修复，局部行为可由后续独立 Validation 从 durable inputs 重算；不代表独立 Validation 已通过。远端动作列表为空；候选、validated、approved、published、production-ready 和 Git mutation 仍分轴记录。

本地 clean-room/UAT witness 只支持声明的输入、版本和机器环境下的有界路径。它不代表公开仓已存在、GitHub 已写入、许可证权利已批准、跨平台支持或 production-ready。

## Card 绑定复核

本次写入前，`SP003_S021_EvidenceRepairLaneTaskCard.json` 的 expected card digest `75d7928fa1fa1213c022aa42890614b6f15369314a6dc143672e582ef8422a8c` 校验通过。写入严格限制在 card 的两个 `write_scope` 文件；因此它们的内容摘要发生合法变化：本文件当前为 `a1748f1c189249f631fa1fc81995a7f9a3db9649facc5bf7c0a93b02772a3d01`，ERBE 文件当前为 `f6eea27f9670eb4db116666a657f8b9ed0ae42d995a3c47a80e7ed180cd40a74`。末次 card 校验按 `digest drift; rebaseline required` 阻断；本 lane 不修改 card，故当前 evidence package 不能称为 digest-stable lane completion，需由有权流程重新绑定 card 后再做独立 Validation。
