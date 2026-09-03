# SGE Governance Skill 中文新手指南

本指南帮助一个没有既有项目背景的新仓库建立最小治理循环。完成这些步骤，只能说明该仓库已经拥有可运行的治理骨架；不能说明产品正确、已经发布或生产就绪。

## 1. 先检查候选包

在候选仓库根目录运行：

```bash
python3 tools/sge_public.py doctor
```

看到 `public_doctor:pass` 表示 manifest 中每个公开文件都存在、许可证字段完整且没有命中的私有身份残留。

## 2. 导出干净公共候选

在候选仓库根目录运行，目标目录必须不存在或为空：

```bash
python3 tools/sge_public.py export /tmp/sge-public-candidate
```

成功输出形如 `exported:<文件数>:/tmp/sge-public-candidate`；文件数以当前 manifest 为准。后续安装和升级均以这个 staging 目录作为 `--source`，不直接从包含 Dashboard 的工作树复制。

## 3. 建立最小项目

```bash
python3 tools/sge_public.py bootstrap /tmp/my-sge-project
```

该命令只写入新的空目录，生成 `AGENTS.md`、项目 profile、Dashboard 最小表面和 README。若目录非空，命令会失败，避免覆盖已有项目。

## 4. 安装 core Skill

```bash
python3 /tmp/sge-public-candidate/tools/sge_public.py install \
  --source /tmp/sge-public-candidate \
  --target /tmp/my-sge-project
```

成功输出形如 `installed:17:/tmp/my-sge-project`。安装只复制 manifest 允许的 `.codex/skills/sge-governed-checkpoints/` 文件，并写入安装记录。目标项目自己的 `AGENTS.md`、`kb/` 和 `Dashboard/` 仍是该项目的 authority。

## 5. 升级并确认可恢复备份

当 staging 中出现经过审查的新候选时运行：

```bash
python3 /tmp/sge-public-candidate/tools/sge_public.py upgrade \
  --source /tmp/sge-public-candidate \
  --target /tmp/my-sge-project
find /tmp/my-sge-project/.sge-backups -name SKILL.md -print
```

成功输出形如 `upgraded:17:/tmp/my-sge-project`，随后 `find` 应至少显示一个旧 core 的 `SKILL.md`。若新版本有问题，从打印出的 `.sge-backups/<timestamp>/...` 路径恢复。

## 6. 跑一个最小 Goal

可复制提示：

```text
/goal 请在当前仓库建立一个最小、可验证的 Goal。先读取 AGENTS.md 与项目 profile，明确原始目标、非目标、claim ceiling、一个 Session、Validation Handoff 和终止条件；不要把计划落库表述为实现完成。
```

Session 执行提示：

```text
执行当前 Goal 的第一个 ready Session。先做 Task Intake 和 Context Bootstrap；若是非平凡改动，按 lane card 启动 Design、Builder、Validation、Closure，并在 closeout 中说明做了什么、不证明什么。
```

独立验证提示：

```text
作为独立 Validation lane，从 durable inputs 重算结果；同时检查原始 Goal 与当前设计，列出已读/未读证据、blocking findings、claim ceiling、KB/Dashboard truth split 和最终 verdict。不要修改 Builder 产物。
```

## 7. 故障恢复

- `destination_must_be_empty`：换一个空目录，或先人工检查现有目录；工具不会覆盖。
- `identity_or_private_residue`：定位 manifest 报告的文件和 token，移出公共候选或给出经审查的公开裁决。
- `uninstall_requires_install_record`：目标不是由本工具安装，工具拒绝猜测删除范围。
- 升级失败：工具会在目标项目 `.sge-backups/` 保存旧 core，再写新版本；运行 `find /tmp/my-sge-project/.sge-backups -name SKILL.md -print` 定位可恢复副本。

## 8. 卸载

```bash
python3 /tmp/sge-public-candidate/tools/sge_public.py uninstall --target /tmp/my-sge-project
```

卸载把已安装 core 移到目标项目 `.sge-trash/`，不删除项目自己的 KB、Dashboard 或 AGENTS.md。需要时可手工移回。
