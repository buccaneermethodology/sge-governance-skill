# SGE Governance 仓库能力与开源质量全景

> 生成于 2026-09-05；branch `sge/sp002`，HEAD `55da8debbb48bd7c10ec6f37bce02b621ba6d610`；工作树 `tracked_changes=0; untracked_paths=33`。这是派生读模型，不是 KB/Dashboard 真源、批准或发布凭据。

## 一眼结论

- 仓库实际只有 **1 个可安装核心 Skill**：`sge-governed-checkpoints`。统一数据中有 1 个 `core_skill` 条目，并将其能力、工具和证据映射到设计冻结的 12 类能力族；它提供 23 类 checkpoint，另有 8 个 core scripts、5 个 schema、7 个公共 lifecycle 子命令。
- 可选 Loop router 只做路由，固定 `completion_evidence:false`；`build-kym` 与 `build-tco-coverage` 只是默认关闭且 `entrypoint:null` 的接口占位，不是随仓交付的 Skills。
- repo-local 质量门禁强：27/27 tests、repository doctor、public doctor、KB render、registry、clean-clone 48 文件 export/verify 均通过。
- **当前不能发布**：public identity 尚未统一到 `bm-sge-governance`；Quick Start 有可复制代码块缺陷；逐文件 rights、完整 Codex newcomer UAT、最终 release assets、CI/read-back 和人类发布授权仍缺。
- Semx 清理结论：公共候选没有 `semx-cli`、`semx-kb`、S-384/S-485、audio-transcriptor 或个人 home 路径；唯一 `semx` 是防污染 deny token。历史 Semx provenance 留在不公开的 Dashboard 层。

## 能力全清单

| ID | 能力 | 类别 | 层 | 状态 | 入口 | 证据 | 边界 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SKILL-CORE-01 | sge-governed-checkpoints | core_skill | core | active | .codex/skills/sge-governed-checkpoints/SKILL.md | test_bound | 这是本仓唯一真实可安装 Skill；其内部能力、脚本、schema 和文档不能重复冒充独立 Skills |
| CHK-intake-evaluation | 任务入口评估 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode intake-evaluation | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-context-bootstrap | 任务上下文启动包 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode context-bootstrap | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-erbe | ERBE 规格优先验收 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode erbe | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-sgc | SGC v1 结构治理 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode sgc | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-multi-agent | 多 Agent 激活 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode multi-agent | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-design | 设计交接 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode design | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-goal-conformance | 原始目标与范围一致性 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode goal-conformance | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-goal-agent | Goal Prompt 质量 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode goal-agent | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-loop-continuation | Loop 连续执行 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode loop-continuation | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-lane-task-card | Lane Task Card 门禁 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode lane-task-card | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-validation | Validation Handoff | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode validation | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-validation-agent | 独立 Validation 质量 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode validation-agent | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-context-efficiency | 增量上下文与收敛 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode context-efficiency | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-oracle | 人类 Oracle 复核 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode oracle | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-adequacy | A1 充分性 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode adequacy | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-bdd-sync | BDD 同步 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode bdd-sync | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-contract-delta | 合同增量路由 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode contract-delta | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-semantic | 语义复核 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode semantic | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-semantic-diagnostic | S1-S6/L0-L6 诊断 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode semantic-diagnostic | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-reader-explanation | 中文读者解释 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode reader-explanation | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-dashboard-agent | Dashboard 全景与候选建议 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode dashboard-agent | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-closeout | 受治理收束 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode closeout | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| CHK-closeout-language | 中文 closeout 语言门禁 | governance_capability | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py:--mode closeout-language | test_bound | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| TOOL-01 | context_bootstrap.py | tool | core | active | .codex/skills/sge-governed-checkpoints/scripts/context_bootstrap.py | test_bound | 并非完整产品运行时 |
| TOOL-02 | goal_patch.py | tool | core | active | .codex/skills/sge-governed-checkpoints/scripts/goal_patch.py | test_bound | 并非完整产品运行时 |
| TOOL-03 | context_state.py | tool | core | active | .codex/skills/sge-governed-checkpoints/scripts/context_state.py | test_bound | 并非完整产品运行时 |
| TOOL-04 | lane_task_card.py | tool | core | active | .codex/skills/sge-governed-checkpoints/scripts/lane_task_card.py | test_bound | 并非完整产品运行时 |
| TOOL-05 | guardrail_checklist.py | tool | core | active | .codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py | test_bound | 并非完整产品运行时 |
| TOOL-06 | workflow_contract.py | tool | core | active | .codex/skills/sge-governed-checkpoints/scripts/workflow_contract.py | test_bound | 并非完整产品运行时 |
| TOOL-07 | profile_validator.py | tool | core | active | .codex/skills/sge-governed-checkpoints/scripts/profile_validator.py | test_bound | 模块库，无独立 CLI 入口 |
| TOOL-08 | context_efficiency_pilot.py | tool | core | active | .codex/skills/sge-governed-checkpoints/scripts/context_efficiency_pilot.py | test_bound | 公开源码说明仍绑定 SP-041 paired rollouts，项目中立性需复核 |
| SCHEMA-01 | goal_contract_v1 | schema_contract | core | active | .codex/skills/sge-governed-checkpoints/schemas/goal_contract_v1.schema.json | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| SCHEMA-02 | goal_patch_v1 | schema_contract | core | active | .codex/skills/sge-governed-checkpoints/schemas/goal_patch_v1.schema.json | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| SCHEMA-03 | lane_prompt_audit_v1 | schema_contract | core | active | .codex/skills/sge-governed-checkpoints/schemas/lane_prompt_audit_v1.schema.json | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| SCHEMA-04 | lane_task_card_v1 | schema_contract | core | active | .codex/skills/sge-governed-checkpoints/schemas/lane_task_card_v1.schema.json | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| SCHEMA-05 | validation_state_snapshot_v1 | schema_contract | core | active | .codex/skills/sge-governed-checkpoints/schemas/validation_state_snapshot_v1.schema.json | structurally_supported | 只支持其声明范围；不自动证明语义正确或发布就绪 |
| LIFE-01 | public doctor | tool | companion | active | tools/sge_public.py:doctor | test_bound | repo-local/clean-room 证据，不证明跨平台或正式发布 |
| LIFE-02 | public export | tool | companion | active | tools/sge_public.py:export | test_bound | repo-local/clean-room 证据，不证明跨平台或正式发布 |
| LIFE-03 | public verify | tool | companion | active | tools/sge_public.py:verify | test_bound | repo-local/clean-room 证据，不证明跨平台或正式发布 |
| LIFE-04 | public bootstrap | tool | companion | active | tools/sge_public.py:bootstrap | test_bound | repo-local/clean-room 证据，不证明跨平台或正式发布 |
| LIFE-05 | public install | tool | companion | active | tools/sge_public.py:install | test_bound | repo-local/clean-room 证据，不证明跨平台或正式发布 |
| LIFE-06 | public upgrade | tool | companion | active | tools/sge_public.py:upgrade | test_bound | repo-local/clean-room 证据，不证明跨平台或正式发布 |
| LIFE-07 | public uninstall | tool | companion | active | tools/sge_public.py:uninstall | test_bound | repo-local/clean-room 证据，不证明跨平台或正式发布 |
| KB-01 | ERBE Specification-First | canonical_strategy | canonical | active | kb/data/strategy/strategy_erbe_specification_first_acceptance_v1.json | structurally_supported | JSON 是真源；Markdown 仅为派生阅读面 |
| KB-02 | Human-AI Development | canonical_strategy | canonical | active | kb/data/strategy/strategy_human_ai_development.json | structurally_supported | JSON 是真源；Markdown 仅为派生阅读面 |
| KB-03 | KB Promotion/Source Policy | canonical_strategy | canonical | active | kb/data/strategy/strategy_kb_promotion_and_source_policy.json | structurally_supported | JSON 是真源；Markdown 仅为派生阅读面 |
| KB-04 | Semantic Surface Engineering | canonical_strategy | canonical | active | kb/data/strategy/strategy_semantic_surface_engineering.json | structurally_supported | JSON 是真源；Markdown 仅为派生阅读面 |
| KB-05 | SGC Structural Contract v1 | canonical_strategy | canonical | active | kb/data/strategy/strategy_sgc_structural_contract_v1.json | structurally_supported | JSON 是真源；Markdown 仅为派生阅读面 |
| KB-06 | 双仓开源分发策略 | canonical_strategy | canonical | candidate | kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json | structurally_supported | JSON 是真源；Markdown 仅为派生阅读面 |
| DASH-01 | doctor.py | dashboard_execution_surface | private-maintainer | derived_only | Dashboard/tools/doctor.py | test_bound | 不进入公共 manifest，也不是终端用户入口 |
| DASH-02 | session_registry.py | dashboard_execution_surface | private-maintainer | derived_only | Dashboard/tools/session_registry.py | test_bound | 不进入公共 manifest，也不是终端用户入口 |
| DASH-03 | generate_dashboard_kg.py | dashboard_execution_surface | private-maintainer | derived_only | Dashboard/tools/generate_dashboard_kg.py | test_bound | 不进入公共 manifest，也不是终端用户入口 |
| DASH-04 | quality_recovery_erbe.py | dashboard_execution_surface | private-maintainer | derived_only | Dashboard/tools/quality_recovery_erbe.py | test_bound | 不进入公共 manifest，也不是终端用户入口 |
| DASH-05 | sge/s002_erbe_acceptance.py | dashboard_execution_surface | private-maintainer | derived_only | Dashboard/tools/sge/s002_erbe_acceptance.py | test_bound | 不进入公共 manifest，也不是终端用户入口 |
| ORCH-01 | profile-driven Loop router | optional_orchestrator | orchestrator | candidate | tools/run_sge_loop_goal_cycle.py | test_bound | 只做路由；completion_evidence=false，不执行 Session、不证明完成 |
| EXT-01 | build-kym | optional_extension_interface | extension | optional_disabled | extensions/registry_v1.json | structurally_supported | enabled_by_default=false 且 entrypoint=null；当前仓库没有可安装/可执行实现 |
| EXT-02 | build-tco-coverage | optional_extension_interface | extension | optional_disabled | extensions/registry_v1.json | structurally_supported | enabled_by_default=false 且 entrypoint=null；当前仓库没有可安装/可执行实现 |
| DOC-01 | 仓库入口 | documentation | companion | candidate | README.md | structurally_supported | 文档存在不等于命令全路径或 Codex 交互已验收 |
| DOC-02 | 中文新手指南 | documentation | companion | candidate | docs/Beginner_Guide_CN.md | structurally_supported | 文档存在不等于命令全路径或 Codex 交互已验收 |
| DOC-03 | 中文快速开始 | documentation | companion | candidate | docs/Quick_Start_CN.md | structurally_supported | 文档存在不等于命令全路径或 Codex 交互已验收 |
| DOC-04 | 最小消费项目示例 | documentation | companion | candidate | examples/minimal-project/README.md | structurally_supported | 文档存在不等于命令全路径或 Codex 交互已验收 |
| TEST-01 | test_loop_orchestrator.py | test_or_gate | evidence | active | tests/test_loop_orchestrator.py | test_bound | 测试通过只支撑被测试合同，不等于全部 core 能力或生产就绪 |
| TEST-02 | test_public_candidate.py | test_or_gate | evidence | active | tests/test_public_candidate.py | test_bound | 测试通过只支撑被测试合同，不等于全部 core 能力或生产就绪 |
| TEST-03 | test_public_projection.py | test_or_gate | evidence | active | tests/test_public_projection.py | test_bound | 测试通过只支撑被测试合同，不等于全部 core 能力或生产就绪 |
| TEST-04 | test_repository_quality.py | test_or_gate | evidence | active | tests/test_repository_quality.py | test_bound | 测试通过只支撑被测试合同，不等于全部 core 能力或生产就绪 |
| TEST-05 | test_session_registry.py | test_or_gate | evidence | active | tests/test_session_registry.py | test_bound | 测试通过只支撑被测试合同，不等于全部 core 能力或生产就绪 |
| TEST-06 | contract/sge_skill_generality.py | test_or_gate | evidence | active | tests/contract/sge_skill_generality.py | test_bound | 测试通过只支撑被测试合同，不等于全部 core 能力或生产就绪 |

## 当前质量状态

| 检查 | 维度 | 结果 | 实际观察 | 证据层 |
| --- | --- | --- | --- | --- |
| Q-01 | repository doctor | pass | 27 tests；170 JSON；24 Python；1248 refs；genericity/registry/KB/ERBE/DKG 均通过 | test_bound |
| Q-02 | unittest | pass | 27/27 passed | test_bound |
| Q-03 | public doctor | pass | public_doctor:pass | test_bound |
| Q-04 | registry | pass | 22 archived / 0 current / no drift or collision | test_bound |
| Q-05 | KB render | pass | render-kb: check passed 7 manifest documents | test_bound |
| Q-06 | clean clone export/verify | pass_with_bounds | 48 files；tree_sha256 dee3293a53c8dd2ff335439bd9292f5da98d83c6a6b5ebea478fdc0b540e860b | test_bound |
| Q-07 | current task worktree export | blocked_expected | dirty_tree；本任务生成物使当前工作树非 clean | execution_bound |
| Q-08 | public identity consistency | fail | bm-sge-governance contract 与公开表面 identity 未统一 | structurally_supported |
| Q-09 | full Codex newcomer UAT | not_run | 只有提示词与 CLI lifecycle 证据 | inference_only |

英文状态解释：`pass` 是声明范围内通过；`pass_with_bounds` 是有界通过；`blocked_expected` 是安全机制按预期阻断；`not_run` 表示没有证据，绝不是失败或成功。

## Semx 残留与开源缺口

| Finding | 级别 | 分类 | 证据 | 影响 | 建议 |
| --- | --- | --- | --- | --- | --- |
| F-P0-IDENTITY | P0 | active/public | 双仓合同指定 bm-sge-governance；README 标题和 candidate_id 仍使用 sge-governance-skill，公开树中 bm-sge-governance 命中为 0 | 公开仓、项目、候选身份不一致，现有 doctor 未阻断 | 裁决 source provenance 与 public identity，新增一致性 gate |
| F-P1-QUICKSTART | P1 | active/public | 中文说明位于 bash fenced block 内 | 整段复制会把中文说明作为 shell 命令执行 | 把说明移出代码块并增加 copy/paste 测试 |
| F-P1-CODEX-UAT | P1 | evidence_gap | Goal/Session/Validation 仅给提示词，未给 Codex 入口、Skill discovery、预期文件与完整交互验收 | 不能声称完整新手体验已验证 | 做独立可见 clean-room Codex UAT |
| F-P1-CORE-COVERAGE | P1 | evidence_gap | 17 个 core 文件可安装；代表性入口已执行，但所有核心脚本未在消费仓逐项端到端运行 | 不能声称全部 core 能力可运行 | 补消费仓 capability matrix 与逐入口 smoke/UAT |
| F-P1-RIGHTS | P1 | authority_gap | manifest 每项有 MIT/source/provenance 字段，但 rights owner 尚未对具体 candidate 作人类确认 | 结构字段不能替代再分发权批准 | 对最终 candidate 做逐文件权利签署 |
| F-P1-RELEASE-ASSETS | P1 | evidence_gap | 无已冻结 owner/URL/default branch/version/tag、公开 CI、SHA256SUMS、最终 license report/release notes/remote read-back | 没有可审计正式发布包 | 完成 release packet、CI/read-back 与具体授权 |
| F-P2-PROVENANCE-LINKS | P2 | active/public | 若干 allowlisted KB JSON/Markdown source refs 指向未随公共包发布的 Dashboard/Artifacts 历史文件 | 不会加载 Semx 代码，但公共文档 provenance 入口不可独立解析 | 生成 public provenance projection 或明确 external/private source locator policy |
| F-P2-PILOT-ID | P2 | active/public | 公开 core 说明硬编码 SP-041 paired rollouts | 带有内部 Session 耦合，削弱项目中立叙述 | 改为通用名称并保留历史 provenance 于私有层 |
| F-INFO-SEMX | INFO | fixture/example | 公开候选仅有 semx 作为 forbidden_target_authority_tokens；没有 semx-cli、semx-kb、S-384/S-485、audio-transcriptor 或个人 home 路径 | 这是防污染规则，不是 Semx 产品依赖 | 保留负例意图并在发布审查中说明 |
| F-INFO-HISTORY | INFO | historical provenance | 历史迁移记录保留 Semx 来源与审计线索，manifest 明确排除 Dashboard/Agent Logs/closeout | 可恢复 provenance，不进入公开包或默认 core | 继续保持 default-deny 隔离 |

## 小白使用指南

把 `<PUBLIC_CLONE>` 替换成你拿到的公开候选 clone，把 `<TARGET_PROJECT>` 替换成一个**不存在或为空**的新目录。

```bash
cd <PUBLIC_CLONE>
python3 tools/sge_public.py doctor
python3 tools/sge_public.py bootstrap <TARGET_PROJECT>
python3 tools/sge_public.py install --target <TARGET_PROJECT>
python3 <TARGET_PROJECT>/.codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode intake-evaluation
```

预期依次看到 `public_doctor:pass`、`bootstrapped:<TARGET_PROJECT>`、`installed:17:<TARGET_PROJECT>` 和 Task Intake checklist。若看到 `destination_must_be_empty`，请换空目录；不要强行覆盖。`--source` 仅用于维护者/测试 alternate source，普通用户不需要。

安装后，在 Codex 中打开 `<TARGET_PROJECT>`，确认项目自己的 `AGENTS.md`、`kb/` 与 `Dashboard/` 仍是 authority，再输入：

```text
/goal 请在当前仓库建立一个最小、可验证的 Goal。先读取 AGENTS.md 与项目 profile，明确原始目标、非目标、claim ceiling、一个 Session、Validation Handoff 和终止条件；不要把计划落库表述为实现完成。
```

当前证据只验证了 lifecycle 与代表性入口；尚未完成一条可见的 Codex `/goal → Session → Validation → closeout` clean-room 验收，所以请把这一步视作待验收指南，而非保证。

升级与恢复：

```bash
cd <PUBLIC_CLONE>
python3 tools/sge_public.py upgrade --target <TARGET_PROJECT>
find <TARGET_PROJECT>/.sge-backups -name SKILL.md -print
python3 tools/sge_public.py uninstall --target <TARGET_PROJECT>
```

upgrade 成功会显示 `upgraded:17:<TARGET_PROJECT>` 并留下备份；uninstall 会显示 `uninstalled_recoverable:...`，把 core 移入 `.sge-trash/`，不会删除项目自己的 KB、Dashboard 或 AGENTS。

## 维护者开源发布操作指南

以下只是授权后的操作合同，不是本任务的 GitHub 写入授权。

1. 冻结 `<SOURCE_COMMIT>`、manifest digest、tool digest、`<PUBLIC_REPO>`、`<BRANCH>`、`<VERSION>` 与 `<TAG>`。
2. 确认 canonical source clean；`dirty_tree` 是安全阻断，不能绕过。
3. 由 rights owner 对 48 个 allowlisted 文件逐项确认 source/license/provenance/public/execution-context。
4. 导出并重算：

```bash
cd <PRIVATE_CANONICAL_CLONE>
python3 tools/sge_public.py export <EMPTY_STAGING>
python3 tools/sge_public.py verify --source <PRIVATE_CANONICAL_CLONE> --destination <EMPTY_STAGING>
cd <EMPTY_STAGING>
python3 tools/sge_public.py doctor
```

5. 从 staging 新建 clean-room target，重放 bootstrap/install/Goal/upgrade/uninstall，并由独立 reviewer 绑定最终 candidate fingerprint。
6. 在继续前修复 public identity、Quick Start code fence、公共 provenance 断开的 source refs，并生成 exact manifest、SHA256SUMS、rights report、release notes。
7. **人类授权 checkpoint**：对具体 repo/tree/branch/tag/release payload 授权；没有授权时停在 `candidate_not_approved`。
8. 授权后才可 commit/push/tag/release。公开 PR 必须先移植回私有 canonical source，再重新 export/verify，不能让公开仓成为第二真源。
9. 发布后 read back 远端 commit/tree/tag/assets/checksums；本地成功不能替代远端验证。发布后回滚应发修复版本或标记/撤下受影响 release，不能声称删除已被复制的公开副本。

## 三条后续路线

- 质量/稳定 P0：统一 public identity，并让 doctor/测试 fail closed。
- 速度/进展 P1：修复 Quick Start，补一条真实可见 Codex newcomer UAT 与所有 core 入口 capability matrix。
- 蓝天 P1：做默认只读的 release-candidate pipeline，自动产出 rights report、checksums、release notes 与 remote read-back 计划；所有外部 mutation 继续需要人类授权。

## 证据入口

- [核心 Skill](../../../.codex/skills/sge-governed-checkpoints/SKILL.md)
- [公共 manifest](../../../public_export_manifest_v1.json)
- [双仓策略](../../../kb/docs/strategy/Open_Source_Dual_Repo_Distribution.md)
- [新手指南](../../../docs/Beginner_Guide_CN.md)
- [快速开始](../../../docs/Quick_Start_CN.md)
- [设计交接](RepositoryCapabilityPanorama_Design.md)
- [详细审计报告](../Session-ADHOC-REPOSITORY-CAPABILITY-PANORAMA/RepositoryCapabilityPanorama_Audit_Report.md)
