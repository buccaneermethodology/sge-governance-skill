# S-018 终端用户生命周期合同

## 关键结论中文展开

本 artifact 记录 S-018 Builder 在当前本地公开 source candidate 上实现的终端用户生命周期边界。当前 verdict 为 `partial_with_bounds`：实现、中文文档和本地 clean-room 重放已形成可复核证据，但工具修改导致原 card 的 `base_context_refs` 摘要漂移，需后续 rebaseline；这不等于独立 UAT/Validation、公开仓已发布、跨平台兼容或 production readiness。

## 目标与范围

- 普通用户从当前 clone 的公开仓目录运行 `install --target <project>` 或 `upgrade --target <project>`；不需要 `--source`。
- `--source` 保留为维护者、高级诊断或测试 alternate source 入口。
- 安装只写 manifest 中 `.codex/skills/sge-governed-checkpoints/` 的 core Skill 文件和根目录 install record；target 的 `AGENTS.md`、`kb/`、`Dashboard/`、Goal、Session 与领域扩展保持由 target owner 管理。
- `doctor` 默认检查当前 source 的 manifest、allowlist、文件对象和内容 residue；它不改变 target，也不授予发布权限。
- 升级先将旧 core 移入 `.sge-backups/<timestamp>/`，保存旧文件 bytes/sha256 与 tree 摘要；复制或 install record 写入失败时恢复旧 core 和旧 record。
- 卸载要求本工具的 install record，将 core 与 record 一起移入 `.sge-trash/<timestamp>/`，因此可以人工恢复；不删除 target owner 的治理文件。

## 可观察合同

| ID | 判定 | 证据边界 |
| --- | --- | --- |
| S018-AC-01 | 默认 source 为当前公开仓目录，普通用户只需 `target`；`--source` 不是必需参数 | 本地 CLI clean-room；不证明远端公开仓存在 |
| S018-AC-02 | install record 保存 candidate、source/manifest identity、安装文件摘要、写入范围、target 与 backup provenance；升级失败恢复旧 core | 本地注入失败回放；不证明跨平台事务语义 |
| S018-AC-03 | install/upgrade/uninstall 不覆盖 target authority；卸载 core 与 record 可恢复，非本工具管理的目标拒绝猜测删除 | target fixture 与失败 fingerprint；不证明用户批准或生产运行 |

## 写入与安全边界

工具在 lifecycle 写入前检查 target layout：target 和受管理的 `.codex`、`.codex/skills`、install record、backup/trash 根路径不能通过 symlink 逃逸；升级已有 core 必须有本工具 install record；缺少 record 的卸载返回 `uninstall_requires_install_record`。install record 采用临时文件后替换，避免半写入记录。以上是本地 fail-closed 行为，不是完整操作系统权限模型。

## install record 约定

记录使用 `sge_install_record_v1`，关键字段为：

- `operation` / `status`：本次是 install 还是 upgrade；
- `source_candidate` 与 `source_identity`：source revision、manifest digest、candidate、安装 file-set/tree digest；
- `target_root` 与 `write_scope`：本地目标及唯一 core Skill 写入面；
- `files`：安装文件的相对路径、bytes、sha256；
- `backup`、`backup_files`、`backup_tree_sha256`：升级前旧 core 的可定位恢复副本及摘要；首次 install 的 backup 值为 `null`；
- `recorded_at`：UTC 记录时间。

这些字段只描述本地 candidate lifecycle provenance，不改变 candidate、validated、approved、published、Git mutation 或 production state 的分离规则。

## 文档与验证入口

- [中文新手指南](../../docs/Beginner_Guide_CN.md)：完整 install、upgrade、失败恢复和卸载路径。
- [中文快速开始](../../docs/Quick_Start_CN.md)：最小 clean-room 命令序列与边界说明。
- [生命周期实现](../../tools/sge_public.py)：默认 source、target layout、备份/记录/恢复实现。
- [Builder lane card](SP003_S018_BuilderLaneTaskCard.json)：本 lane 的唯一写范围、验收 ID 与最大主张。

## 明确非目标

本 S-018 artifact 不执行或证明 GitHub create/push/tag/release、远端 read-back、公开仓已创建/发布、license 再分发权、跨平台兼容、独立 Validation、完整 UAT、Semantic Review 或 production readiness；不修改 Goal、KB、Dashboard registry 或执行 GitHub 远端动作。
