# S-007 公共合同与术语设计交接

## 关键结论中文展开

本设计把可公开候选与本仓库执行记忆分成物理目录和合同边界。它只授权后续 Builder 生成候选与可重跑检查，不授权发布、推送、全局安装或生产声明。

## 公共四层与依赖

| 层 | 内容 | 依赖 | claim ceiling |
| --- | --- | --- | --- |
| core | `.codex/skills/sge-governed-checkpoints/`、公共 schema/script | 无 | 通用治理门禁在声明范围内可复制 |
| companion | README、Beginner Guide、Quick Start、LICENSE/NOTICE | core | 新手可按文档重放，不证明普遍易用 |
| orchestrator | `tools/run_sge_loop_goal_cycle.py` 与 profile/hooks | core；可选 companion | 仅证明无扩展时的有界编排 |
| domain extension | `extensions/` 下显式注册的领域适配器 | core；按注册项 | 不安装时 core 不得依赖；不证明领域正确性 |

安装顺序为 core → companion → 可选 orchestrator → 可选 domain extension。每一层都必须在 manifest 中逐文件列出；缺失可选层不能阻塞 core。

## Glossary v1 合同

canonical 真源是 `kb/data/glossary_v1.json`，`kb/docs/Glossary.md` 是 renderer 生成的投影。条目必须包含 term、definition、scope、authority、boundary、claim_ceiling、forbidden_overreads、related_concepts、source_refs；只定义稳定 SGE 治理语义。

纳入：Canonical Truth、KB / Dashboard Truth Split、Doc as Data、Evidence、Candidate、Claim Ceiling、Scope Delta、Promotion、Session、Stage Plan、Lane Task Card、Validation Handoff、Semantic Reviewer、Closeout、Design Freeze Validity、Implementation Entry Readiness、Minimum Safe Slice、Future-agent Misuse Scenario、SGC、ERBE。

排除：任何具体产品、产品 phase/runtime、provider、历史 Session/Goal、KYM/TCO 专属语义和本机绝对路径。

## Default-deny 与 provenance

`public_export_manifest_v1.json` 是显式 allowlist；构建器拒绝未列文件、路径穿越、绝对路径、Dashboard/Agent_Logs、历史 provenance、dirty worktree 和 forbidden identity token。每个 allowlisted 文件记录 source、license、provenance、public、execution_context。

## ERBE 设计

- predicate：导出结果集合必须等于 allowlist 的闭包；任何 unknown、absolute、private-surface 输入必须失败。
- invariant：manifest 不可由工作树 glob 隐式扩大；KB JSON 与 Markdown 必须确定性一致；可选扩展缺失时 core 命令仍可运行。
- negative cases：未知文件、绝对路径、Dashboard 文件、私有路径 token、重复条目、缺 license、glossary 缺 source_refs、Markdown 漂移。

## 实施梯子与非目标

先落地 manifest/validator 和 glossary，再落地文档与生命周期工具，再落地可选编排器，最后执行 clean-room/UAT 与最终候选验证。非目标是发布、远端 push、全局 Skill 写入、任何具体产品迁移和生产就绪。

## 入口与验证

Builder 只可修改本 Session 的公共候选文件；Validation 从 manifest、JSON、renderer 输出和 clean-room 临时目录独立重算。当前设计不证明这些产物已经实现。
