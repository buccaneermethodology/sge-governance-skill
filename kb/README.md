# SGE Governance 知识库

本目录是 SGE Governance Skill 的 canonical truth（稳定治理合同、术语与来源规则）。JSON 位于 `kb/data/`，Markdown 位于 `kb/docs/`；Markdown 是可读投影，不是独立真源。

## 当前范围

- `sge_project_profile_v1.json` 定义通用 Skill 身份、根目录与 authority 路由。
- `sge_strategy_source_manifest_v1.json` 固定来源 revision、provenance 与 56 个 strategy 表面的审计入口。
- `sge_strategy_canonical_mapping_v1.json` 定义通用治理规则的抽取、排除与 promotion policy。
- SGC、ERBE 与 workflow registry 提供结构治理、合同验收和可执行阶段入口。

## 权威边界

稳定 truth 写入 `kb/data/`；执行状态、Session、阻断和 closeout 写入 `Dashboard/`。Dashboard DKG 与 Markdown 均为执行记忆投影，不替代本目录的 canonical truth。

本仓库只提供可复用的 repo-local SGE Governance 框架，不实现任何具体产品、provider 或公共发布。KYM/TCO、历史 phase/runtime 和高级 Loop 编排均不属于默认核心；如未来需要，必须作为独立、明确授权的扩展重新设计。

## 工具

- `.codex/skills/sge-governed-checkpoints/`：治理 checkpoint、schema 与确定性脚本。
- `kb/tools/render_kb.py`：从 JSON 生成 Markdown 投影。
- `kb/tools/glossary_v21_validator.py`：验证术语 JSON 的结构和边界。
