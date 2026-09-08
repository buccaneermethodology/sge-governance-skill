# SP-002 / S-010 最终独立 UAT

## 关键结论中文展开

本次独立 UAT 对最终当前快照的 clean-room newcomer lifecycle 给出**限定通过**结论：指定 lane card 的摘要绑定有效；在全新临时目录中，以正确的 bootstrap-to-install target 拓扑重放了 `doctor`、`export`、`bootstrap`、`install`、`upgrade` 与 `uninstall`；导出物未检出本机绝对 `/Users` 或 `/home` 路径；ERBE GREEN 通过。

这表示该受测生命周期在本次本地快照和上述命令范围内可用。它不表示 release 已批准、production 已验证，也不追溯补足原始 pre-Builder chronology。

## lane card 摘要校验

命令：

```bash
python3 .codex/skills/sge-governed-checkpoints/scripts/lane_task_card.py validate \
  Dashboard/Artifacts/Stage-Plan-SP-002/SP002_S010_FinalUATLaneTaskCard.json \
  --expected-card-sha256 503ed2cf7ec98f4db82aac7d2ea1a5c70948129e30a8e195b18e50f797ab9f39
```

结果：退出码 `0`；`verdict=pass`；返回的 `card_sha256` 与要求值一致。受测 card 见 [SP002_S010_FinalUATLaneTaskCard.json](SP002_S010_FinalUATLaneTaskCard.json)。

## 新临时目录 lifecycle 重放

最终成功重放使用新目录 `/tmp/s010-final-uat-retry.dpjpkV`。命令和结果如下：

| 命令 | 结果 | 中文判断 |
| --- | --- | --- |
| `python3 tools/sge_public.py doctor` | `public_doctor:pass`，退出码 `0` | 源仓库公开候选自检通过。 |
| `python3 tools/sge_public.py export /tmp/s010-final-uat-retry.dpjpkV/exported` | `exported:48`，退出码 `0` | 导出目录生成 48 项。 |
| `python3 tools/sge_public.py bootstrap /tmp/s010-final-uat-retry.dpjpkV/installed` | `bootstrapped`，退出码 `0` | 安装 target 已完成 bootstrap。 |
| `python3 tools/sge_public.py install --source /tmp/s010-final-uat-retry.dpjpkV/exported --target /tmp/s010-final-uat-retry.dpjpkV/installed` | `installed:17`，退出码 `0` | 安装成功，共 17 项。 |
| `python3 tools/sge_public.py upgrade --source /tmp/s010-final-uat-retry.dpjpkV/exported --target /tmp/s010-final-uat-retry.dpjpkV/installed` | `upgraded:17`，退出码 `0` | 升级路径成功，共 17 项。 |
| `python3 tools/sge_public.py uninstall --target /tmp/s010-final-uat-retry.dpjpkV/installed` | `uninstalled_recoverable`，退出码 `0` | 卸载成功，结果进入 target 内的可恢复 `.sge-trash`。 |

首轮新目录重放把 `bootstrap` 和 `install` 放在两个不同 target，导致 `install` 与 `upgrade` 返回 `target_not_bootstrapped`、`uninstall` 返回 `uninstall_requires_install_record`。该结果说明 lifecycle 的必要拓扑是：必须对将要 `install` 的同一 target 先运行 `bootstrap`；它不构成最终成功重放的失败掩盖。

## 导出物绝对路径检查

命令：

```bash
rg -n --hidden --glob '!*\\.pyc' '/Users|/home' /tmp/s010-final-uat-retry.dpjpkV/exported
```

结果：退出码 `1` 且无输出，表示 `rg` 未找到匹配项；导出目录未检出 `/Users` 或 `/home` 绝对路径。

## ERBE GREEN

命令：

```bash
python3 Dashboard/tools/sge/s002_erbe_acceptance.py --phase green
```

结果：退出码 `0`；`contract_verdict=valid`、`execution_verdict=ok`、总 `verdict=pass`。该门禁还报告 `doctor`、`kb/tools/render_kb.py --check`、`tests.test_public_candidate tests.test_loop_orchestrator` 与 `no_private_dashboard_source_ref` 均通过。

## 独立 verdict 与 claim ceiling

**独立 verdict：通过（仅限最终当前快照的本地 clean-room newcomer UAT）。** 证据由本次独立命令重放和 [SP002_S010_FinalUATLaneTaskCard.json](SP002_S010_FinalUATLaneTaskCard.json) 的 digest-bound 任务边界共同支撑。

**Claim ceiling：** 最多确认最终当前快照的 clean-room newcomer path 有界通过；不批准 release、不声明 production 成功、不声明 SP-002 最终关闭，也不修复或重写原始 pre-Builder chronology。
