# S-025 消费仓核心能力矩阵

## 关键结论中文展开

当前冻结 manifest 的 17 个 core 文件和 8 个 core scripts 已逐项分类并建立本地可观察证据。clean staging 上的 public projection `export` 与 `verify` 均成功，输出 48 个 allowlisted 文件，tree digest 为 `d84b83cbe264e123a94422ca987bda99345ffa50b8df427e4c94635de5d0c160`。

## 逐项矩阵

| # | 文件 | 类型 | 入口/判定 | 实际结果 |
|---:|---|---|---|---|
| 1 | `.codex/skills/sge-governed-checkpoints/SKILL.md` | Skill interface/reference | 非可执行；可读性检查 | `pass`（通过） |
| 2 | `.codex/skills/sge-governed-checkpoints/agents/openai.yaml` | Skill metadata | 非可执行；YAML 存在 | `pass`（通过） |
| 3 | `references/checklists.md` | reference | 非可执行；可读 | `pass`（通过） |
| 4 | `references/context-efficient-goal-validation.md` | reference | 非可执行；可读 | `pass`（通过） |
| 5 | `schemas/goal_contract_v1.schema.json` | schema | JSON 加载 | `pass`（通过） |
| 6 | `schemas/goal_patch_v1.schema.json` | schema | JSON 加载 | `pass`（通过） |
| 7 | `schemas/lane_task_card_v1.schema.json` | schema | JSON 加载 | `pass`（通过） |
| 8 | `schemas/lane_prompt_audit_v1.schema.json` | schema | JSON 加载 | `pass`（通过） |
| 9 | `schemas/validation_state_snapshot_v1.schema.json` | schema | JSON 加载 | `pass`（通过） |
| 10 | `scripts/context_bootstrap.py` | CLI script | `--help` 返回码 0 | `pass`（通过） |
| 11 | `scripts/context_efficiency_pilot.py` | CLI script | `--help` 返回码 0 | `pass`（通过） |
| 12 | `scripts/context_state.py` | CLI script | `--help` 返回码 0 | `pass`（通过） |
| 13 | `scripts/goal_patch.py` | CLI script | `--help` 返回码 0 | `pass`（通过） |
| 14 | `scripts/guardrail_checklist.py` | CLI script | `--help` 返回码 0 | `pass`（通过） |
| 15 | `scripts/lane_task_card.py` | CLI script | `--help` 返回码 0 | `pass`（通过） |
| 16 | `scripts/profile_validator.py` | library validator | import 负例可观察；CLI 为 N/A | `pass_with_bounds`（有界通过） |
| 17 | `scripts/workflow_contract.py` | CLI script | `--help` 返回码 0 | `pass`（通过） |

## 原始命令与证据

完整 raw command、return code、export/verify 输出、7 个 CLI 的 help/负例 smoke 和 library N/A 记录见 [Execution Transcript](SP004_S025_ExecutionTranscript.json)。结构化逐项记录见 [Capability Matrix JSON](SP004_S025_CapabilityMatrix.json)。

## 例外、边界与后续验证

Builder lane 两次因 dirty checkout 与临时采集器错误未形成 artifact；主线程按已验证 card 补生成本矩阵，记录为 `Single-Agent Exception`，不冒充 Builder lane 已完成。必须由独立 Validation 从 durable inputs 重算，并检查每项证据是否足以支撑 capability，而不把文件存在、import 或 help 成功升级为 end-to-end capability。

本矩阵不证明所有平台/仓库、完整 UAT、rights、release、远端状态、production readiness 或 SP-004 完成。

## Claim ceiling

最高为 `declared_core_matrix_validated_on_frozen_consumer` 的候选输入；在独立 Validation 之前只能视为 `test_bound` / `structurally_supported` 的主线程证据。
