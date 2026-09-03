# SP-002 SGE Governance 开源提取与新手可用性 Stage Plan

## 当前状态

- Initial Status：`To do`；实时状态以 `Dashboard/Stage_Plans.md` 与 `Dashboard/Sessions.md` 为 authority。
- 依赖：`SP-001 complete`
- 初始入口：`S-007`；依赖已满足，用户已于 2026-09-02 明确启动，后续入口由 continuation scan 决定。
- 正式 Goal：[SP-002 Loop Goal](SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md)。
- 本阶段计划冻结执行边界；实际实现与验证记录在各 Session closeout。仍不自动发布、不 push、不写全局 Skills。

## 目标

在 SP-001 完成 repo-local 有界迁移后，把 `sge-governed-checkpoints` 整理为可审计、可安装、可卸载的公共发布候选，并让第一次接触 SGE 的中文新手能按傻瓜式指南在 clean-room 项目中完成最小治理循环，再由独立 `user-acceptance-test` 验证说明书与真实行为一致。

## Must-have Ledger

| ID | Must-have | 可观察验收 |
| --- | --- | --- |
| SP002-MH-01 | 冻结 license、第三方 provenance 与 public/private 边界 | 每个分发文件有来源/许可证裁决，无未授权 Semx 私有内容 |
| SP002-MH-02 | public export 使用 allowlist/default-deny | clean export 只含 manifest 允许文件，未知/绝对路径/历史 evidence 被拒绝 |
| SP002-MH-03 | 明确 core、companion、orchestrator、domain extension 四层 | 依赖图、安装顺序、optional contract 和 claim ceiling 可机器/人工核对 |
| SP002-MH-04 | 提供中文 Beginner Guide、Quick Start、minimal project 和完整可复制 prompts | 新手无需 Semx 背景可完成 bootstrap→Goal→Session→Validation→closeout |
| SP002-MH-05 | 提供 install/doctor/bootstrap/upgrade/uninstall | clean-room 正反例通过且操作可恢复 |
| SP002-MH-06 | 将 `run-loop-goal-cycle` 去 Semx/KYM/TCO 硬编码为可选 `run-sge-loop-goal-cycle` | profile/hooks 驱动；不要求 ChatGPT Semx project、KYM/TCO 或固定两轮 refresh |
| SP002-MH-07 | `user-acceptance-test` 独立验证新手路径 | 一问一答、可读性、错误恢复、证据/claim 边界由独立 lane 验收 |
| SP002-MH-08 | KYM/TCO 保持 optional domain extensions | 未安装时核心与 Quick Start 仍通过；安装时有显式接口与 provenance |
| SP002-MH-09 | clean-room 身份隔离与无绝对路径验收 | 新 repo 安装、doctor、示例、卸载均无 Semx/audio-transcriptor 私有路径残留 |
| SP002-MH-10 | 独立 Validation、Semantic Review、closeout 与发布授权边界 | final candidate 覆盖实际 diff；实际公开发布仍需单独人类批准 |
| SP002-MH-11 | 建立去项目化 SGE Governance Glossary v1 | canonical JSON/Markdown、source refs、negative cases 和 renderer check 通过 |
| SP002-MH-12 | 将公共 Skill 与本仓库特定执行面物理/合同隔离 | default-deny staging export 排除 Dashboard、Agent Logs、历史 provenance 和内部 evidence |

## Session DAG

| Session | Topic | Scope | Deliverable | Exit Criteria |
| --- | --- | --- | --- | --- |
| S-007 | 公共合同、glossary 与分层冻结 | license/provenance、public export、SGE glossary、四层架构、执行面隔离、ERBE | Public Contract、manifest/schema、Glossary Design、Design/Semantic Review | provenance、glossary scope、边界/negative cases 冻结 |
| S-008 | 新手指南与 bootstrap 工具 | Beginner Guide、Quick Start、示例、install/doctor/bootstrap/upgrade/uninstall | docs、minimal repo、工具与 fixtures | 文档命令与 clean-room 行为一致 |
| S-009 | 高级编排与扩展接口 | `run-sge-loop-goal-cycle`、companion hooks、KYM/TCO optional interface | orchestrator Skill candidate、extension registry | 无 Semx/KYM/TCO 默认依赖，核心独立通过 |
| S-010 | clean-room 小白验收 | 全新环境安装、按指南执行、故障恢复、卸载 | 独立 UAT evidence 与修复闭环 | `user-acceptance-test` 对真实入口给出有界通过结论 |
| S-011 | 公共候选 closeout | package manifest、独立 Validation/Semantic、OPCM、final reconciliation | release candidate 与中文 closeout | candidate gates 全部通过；发布仍 pending human authority |

固定依赖为 `S-007 → S-008 → S-009 → S-010 → S-011`。Session closeout 不是 Goal 停止点；启动 SP-002 后，下一 Session ready 且无需人类决定时自动继续。

## 公共包与执行面分层

- Public candidate 只从干净 staging 目录按 default-deny manifest 生成；允许 core Skill、去项目化 KB/glossary、Beginner Guide、必要 tests/examples、LICENSE/NOTICE 和公共 metadata。
- 本仓库的 Dashboard、Sessions、Stage Plans、Agent Logs、OPCM、closeout、完整 doctor/Validation 报告、历史迁移 provenance、绝对路径和 dirty worktree 属于 private execution/provenance surface，默认不进入公共包。
- 使用者的 `AGENTS.md`、Dashboard、Goal、Session、project profile 和领域扩展属于 target-project overlay；安装公共 Skill 后在目标项目维护，不从本仓库复制执行状态。
- 任何例外必须逐文件写入 manifest、license/provenance 裁决，并由 clean-room negative case 验证；目录名或 `.gitignore` 不能代替边界。

## Skill 分层

1. 通用核心：`sge-governed-checkpoints`。
2. 独立方法型配套：`dashboard-governance`、`contract-first-delivery`、`doc-system-kb-builder`、`llm-artifact-evaluator`、`pdi`、`user-acceptance-test`。
3. 高级编排：可选 `run-sge-loop-goal-cycle`。
4. 领域扩展：可选 `build-kym`、`build-tco-coverage`。

Beginner Guide 是用户操作文档；`user-acceptance-test` 是独立验收 Skill，不能用文档作者自检替代。KYM/TCO 不是默认治理前置，因为它们建模特定业务 artifact；只有采用该领域方法的项目才安装。

## 非目标与 Claim Ceiling

- 不在本轮创建或修改任何 Skill。
- 不实际开源发布、不 push、不写全局 Skills、不创建 GitHub release。
- 不证明任意 repo、任意团队或生产环境普遍适用。
- 最大主张：`SGE Governance 公共发布候选及新手流程已在规定 clean-room 范围内通过结构、安装与独立可用性验收`。

实际发布属于外部状态变更，必须在 S-011 后由用户针对具体 repository、tag、license 和 payload 单独授权。
