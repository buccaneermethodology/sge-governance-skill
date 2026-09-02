# sge-governance-skill

可复用的 SGE（Semantic Governance Engineering）治理 Skill 仓库。

核心入口是 [.codex/skills/sge-governed-checkpoints/SKILL.md](.codex/skills/sge-governed-checkpoints/SKILL.md)。它为非平凡任务提供 Context Bootstrap、ERBE specification-first、SGC、Goal Conformance、lane card、独立 Validation、Semantic Review、closeout-language 和 post-closeout 对账门禁。

## 最小使用

在目标项目中复制 `.codex/skills/sge-governed-checkpoints/`，然后将项目自己的 `kb/`、`Dashboard/` 和 `AGENTS.md` 作为 authority；不要复制本仓库的历史迁移记录或任何具体产品文件。

常用入口：

```bash
python3 .codex/skills/sge-governed-checkpoints/scripts/context_bootstrap.py validate <context.json>
python3 .codex/skills/sge-governed-checkpoints/scripts/lane_task_card.py validate <lane-card.json> --repo .
python3 .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode closeout-language --file <closeout.md>
```

## 边界

本仓库只维护通用治理能力，不包含音频转写或其他产品实现。`build-kym`、`build-tco-coverage` 和 Loop 编排器都是可选扩展，不会被核心 Skill 默认加载。公共发布、全局安装和跨仓库普遍适用性需要另行验证与授权。

## 目录

- `.codex/skills/sge-governed-checkpoints/`：Skill、references、schemas、确定性脚本。
- `kb/data/strategy/`：SGE canonical strategy contracts 与 generic profile。
- `Dashboard/`：执行记忆、Validation、closeout 和 provenance 记录。
