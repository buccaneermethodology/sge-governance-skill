# S-025 独立验证复核

## 关键结论中文展开

本复核验证的是：当前冻结 `public_export_manifest_v1.json` 在 fresh clean staging 上能否生成 48 个文件的本地 public projection，并对声明的 17 个 core 文件和 8 个 scripts 做实际分类与入口核对。

fresh `export` 与正确参数的 `verify` 均成功，重算 tree digest 为 `d84b83cbe264e123a94422ca987bda99345ffa50b8df427e4c94635de5d0c160`，与已有 transcript 一致。17 个 allowlisted core 条目的文件存在、reference/schema 的结构检查成立；8 个脚本中 7 个是真正的 CLI，`profile_validator.py` 实际是无命令行入口的 importable library validator，应记为 CLI `N/A`，而不是 CLI 成功。由于原矩阵只持久化了 `--help` 摘要、未给出逐入口 smoke/N/A 记录，并把 `profile_validator.py` 列为 CLI，本轮唯一 Validation verdict 为 `partial`（部分通过）。

这意味着当前 checkout 支持“冻结 consumer projection 的本地结构和部分入口证据”，但不能支持 17/8 capability matrix 已完整通过、端到端能力已验证、通用 newcomer readiness、S-026 或 SP-004 完成。

## 验证交接包

本文件即为 S-025 的独立 Validation Review；本轮不是 release、rights、remote 或 production review。

### 中文 Read Manifest

| 已读文件 | 用途与实际使用 |
|---|---|
| [AGENTS.md](../../AGENTS.md) | 只读 Validation 边界、SGC v1、Goal Conformance、Dashboard/KB 分界、closeout 规则。 |
| [.codex/skills/sge-governed-checkpoints/SKILL.md](../../.codex/skills/sge-governed-checkpoints/SKILL.md) | Validation Agent、Context Bootstrap、SGC、Delta evidence 与禁止 false closure 的流程依据。 |
| [S-025 Validation Lane Task Card](SP004_S025_CapabilityMatrixValidationLaneTaskCard.json) | card identity、固定摘要、delta read set、write scope、最大主张和禁止主张。 |
| [SP-004 Loop Goal](SP004_SemxResidueOpenSourceGaps_LoopGoal.md) | 原始十项 must-have、S-025 目标/退出条件、Session DAG、claim ceiling、C2 与后续边界。 |
| [S-024 Closeout](SP004_S024_Closeout.md) | 前置 Session 的有界结论、Single-Agent Exception、S-025 入口与未完成范围。 |
| [S-025 Capability Matrix JSON](SP004_S025_CapabilityMatrix.json) | 被验证的 17/8 声明矩阵及其原始 digest。 |
| [S-025 Capability Matrix Markdown](SP004_S025_CapabilityMatrix.md) | reader-facing 分类、profile_validator 原始标记、主线程例外和边界声明。 |
| [S-025 Execution Transcript](SP004_S025_ExecutionTranscript.json) | 原始 export/verify return code、tree digest、8 个 help 摘要和主线程来源。 |
| [public export manifest](../../public_export_manifest_v1.json) | 48 个 allowlisted paths、default-deny、candidate status、identity/provenance 和排除规则。 |
| [S-023 Contract](SP004_S023_Contract.json) | GAP-MH-04 predicate、state axes、claim ceiling、forbidden collapses 和 truth/authority boundary。 |
| [S-023 Cases](SP004_S023_Cases.json) | GAP-MH-04 的 independent recompute / file-existence-or-import overclaim 边界。 |
| [S-024 Validation Review](SP004_S024_ValidationReview.md) | 前置验证的 blocker、局部 evidence ceiling 和未关闭 finding。 |
| [S-024 Validation State Snapshot](SP004_S024_ValidationStateSnapshot.json) | 前置 baseline、dirty inventory、rebaseline trigger 和既存 registry digest 问题。 |
| [S-024 Delta Validation Review](SP004_S024_DeltaValidationReview.md) | 前置 delta 的独立性、非目标和 Dashboard/KB 处理。 |
| [Dashboard Sessions](../Sessions.md)、[Session Index](../Session_Index.md)、[Stage Plans](../Stage_Plans.md)、[Current State](../Current_State.md)、[SP-004 archive](../Archives/Sessions/SP-004.md) | 最终 Dashboard 状态、S-025/S-026 顺序、SP-004 状态及历史 topology。 |
| [SGC v1 JSON](../../kb/data/strategy/strategy_sgc_structural_contract_v1.json)、[SGC v1 Markdown](../../kb/docs/strategy/Strategy_SGC_Structural_Contract_V1.md) | claim level、SI-1..SI-6、recompute validation、scope substitution 和 false closure 检查。 |

未读或不执行的外部面：remote owner/repo/CI/tag/release/assets、rights confirmation、credential、Git handoff、S-026 clean-room UAT、S-027/C2 和 S-028 remote mutation；这些不是本 card 的 authority，也未被本 verdict 吸收。

## 范围与非目标

范围仅为当前 manifest 的 48 个 allowlisted 文件、其中 9 个非可执行 core 条目和 8 个 scripts 的本地 consumer projection 及入口证据。明确不做：代码修复、manifest/matrix/Contract/Cases 修改、Sessions/KB 更新、远端访问或写入、rights/release 判断、S-026 UAT、SP-004/Goal terminal 判断。

## Card 与独立重算证据

| 检查 | 实际证据 | 结论边界 |
|---|---|---|
| card 摘要校验 | `python3 .codex/skills/sge-governed-checkpoints/scripts/lane_task_card.py validate Dashboard/Artifacts/SP004_S025_CapabilityMatrixValidationLaneTaskCard.json --repo . --expected-card-sha256 448060f5880bbfa5deb8517fb763a8215da9386e4270a1afb62e885fc05e7335`，`returncode=0`，card digest 与期望一致。 | 只证明 lane card 可用，不证明产物质量。 |
| clean staging | 从 manifest `.files[].path` 复制 48 条 allowlist；检查无 `.git/`、`Dashboard/`、绝对路径或 `..` escape。 | source staging 是本轮新建的 `/private/tmp` 临时输入，不是 public release。 |
| export | `python3 tools/sge_public.py export <fresh-destination> --source <clean-staging>`，`returncode=0`，输出 `exported:48`。 | 只证明本地 projection 执行成功。 |
| verify | `python3 tools/sge_public.py verify --source <clean-staging> --destination <fresh-destination>`，`returncode=0`；文件集合 48 条，tree digest 为 `d84b83cbe264e123a94422ca987bda99345ffa50b8df427e4c94635de5d0c160`。 | 是本地重算证据，不是远端、rights 或 release 证据。 |
| public doctor | fresh destination 上 `python3 tools/sge_public.py doctor`，`public_doctor:pass`。 | 仅为工具自身的静态/本地检查。 |
| destination 附加物 | export 生成 `EXPORT_METADATA.json`；allowlist payload 无 missing，附加物不是 manifest payload。此前手工 import 曾在另一临时 destination 产生 `__pycache__`，不纳入最终 fresh replay。 | `verify` 只核对 expected allowlist；不能把 generated metadata 当作 48 项能力。 |

## 17 个 core 条目逐项判断

以下是从最终 fresh destination 独立读取/分类的结果；`pass` 只表示该条目的结构或加载检查，不表示端到端能力。

| # | 实际文件 | 实际类别 | 独立检查 | 判断 |
|---:|---|---|---|---|
| 1 | `.codex/skills/sge-governed-checkpoints/SKILL.md` | reference/interface | 非空、可读 | 结构证据成立 |
| 2 | `.codex/skills/sge-governed-checkpoints/agents/openai.yaml` | metadata | 非空 YAML 文本 | 结构证据成立 |
| 3 | `references/checklists.md` | reference | 非空、可读 | 结构证据成立 |
| 4 | `references/context-efficient-goal-validation.md` | reference | 非空、可读 | 结构证据成立 |
| 5 | `schemas/goal_contract_v1.schema.json` | schema | `json.loads` 成功 | 加载证据成立 |
| 6 | `schemas/goal_patch_v1.schema.json` | schema | `json.loads` 成功 | 加载证据成立 |
| 7 | `schemas/lane_task_card_v1.schema.json` | schema | `json.loads` 成功 | 加载证据成立 |
| 8 | `schemas/lane_prompt_audit_v1.schema.json` | schema | `json.loads` 成功 | 加载证据成立 |
| 9 | `schemas/validation_state_snapshot_v1.schema.json` | schema | `json.loads` 成功 | 加载证据成立 |
| 10 | `scripts/context_bootstrap.py` | CLI | AST 有 parser/main/guard；`--help` 为 0；真实 packet `validate` 为 0 | 有界入口证据 |
| 11 | `scripts/context_efficiency_pilot.py` | CLI | AST 有 parser/main/guard；`--help` 为 0；空输入按预期报 JSON parse error、`returncode=2` | 仅 fail-closed 入口证据 |
| 12 | `scripts/context_state.py` | CLI | AST 有 parser/main/guard；`--help` 为 0；同 snapshot compare 返回 `status=rebaseline_required` | 能运行；输入 snapshot 结构问题未被当作通过 |
| 13 | `scripts/goal_patch.py` | CLI | AST 有 parser/main/guard；`--help` 为 0；提案型 Loop Goal parse 按预期拒绝，`missing fixed canonical Goal payload`、`returncode=2` | 仅输入边界证据 |
| 14 | `scripts/guardrail_checklist.py` | CLI | AST 有 parser/main/guard；`--help` 和 `--mode validation-agent` 均为 0 | 有界 checklist 入口证据 |
| 15 | `scripts/lane_task_card.py` | CLI | AST 有 parser/main/guard；`--help` 为 0；固定 S-025 card validate 为 0 | 有界 card-validator 入口证据 |
| 16 | `scripts/profile_validator.py` | library validator；非 CLI | AST 无 parser、无 `main`、无 `__main__` guard；直接 import 后负例返回 `(False, 'project_identity_missing')`；`--help` 无输出且 0 | CLI 入口应为 `N/A`，不能写 CLI pass |
| 17 | `scripts/workflow_contract.py` | CLI | AST 有 parser/main/guard；`--help` 和 `--stage validate` 均为 0 | 有界 workflow-renderer 入口证据 |

## 8 scripts 的覆盖判断

实际覆盖是 `7 个 CLI + 1 个 library/N/A`，不是 `8 个 CLI`。7 个 CLI 都有 fresh projection 中的 `--help` evidence；其中 `context_bootstrap`、`guardrail_checklist`、`lane_task_card`、`workflow_contract` 有成功 smoke，`context_efficiency_pilot`、`goal_patch` 有预期 fail-closed smoke，`context_state` 有可运行但暴露旧 snapshot registry digest mismatch 的 smoke。`profile_validator` 的 import 负例证明了 library validator 的边界，不证明命令行能力。

因此 GAP-MH-04 的“17 个条目有 observable capability 或 justified N/A”得到部分独立支持：9 个 reference/schema 的结构证据、7 个 CLI 的入口证据和 1 个 library 的 N/A 分类均可观察；但原始 durable matrix 尚未把这些实际分类、smoke 输出和 N/A 逐项吸收，且 row 16 的 `CLI script` 标签与真实实现冲突。不能将其升级为完整 17/8 capability pass。

## 阻断发现

1. 原 [Capability Matrix JSON](SP004_S025_CapabilityMatrix.json) 与 [Capability Matrix Markdown](SP004_S025_CapabilityMatrix.md) 将 `profile_validator.py` 标成 `CLI script`，但独立 AST 和 import 检查显示它没有 CLI parser、main 或 main guard；这应改成 library validator / CLI `N/A`，但本轮按用户边界不修改 matrix。
2. 原 [Execution Transcript](SP004_S025_ExecutionTranscript.json) 只保存 8 个 help 摘要和带占位符的 staging 命令，没有逐入口 smoke/N/A raw output；存在文件、可 import、`--help` 成功均不足以支撑 end-to-end capability。
3. `context_state.py compare` 对既有 S-024 snapshot 返回 `status=rebaseline_required`，原因是 `generated_registry.registry_digest does not match its content`；这是旧 snapshot 的证据质量问题，不能伪装为 S-025 full baseline 通过。

以上问题阻断“完整 capability matrix 已验证”的强主张，但不阻断记录本地 projection、结构检查和有界入口证据。

## Single-Agent Exception 与时序

S-025 Builder lane 没有落盘 Builder artifact：既有记录说明两次尝试分别受 dirty checkout 与临时采集器错误影响，随后由主线程生成 matrix/transcript。该 topology 例外已在 [Capability Matrix Markdown](SP004_S025_CapabilityMatrix.md) 明示；本 Review 不把主线程补产物改写为 Builder lane 已完成，也不把 Validation 变成 Builder 修复。

S-025 card 没有要求 user-visible independent task，因此本 lane 不新增 user-visible task exception；当前独立性来自本 Review 对 durable inputs 的重新读取、fresh staging 重算和入口重跑，而不是来自 Builder 产物自报。

## SGC v1 与 claim ceiling

最高只到 `execution_bound`、`structurally_supported` 与 `test_bound` 的组合：支持当前 checkout / frozen consumer projection 的本地执行、结构和测试边界证据。没有 `externally_supported` 证据。已检查并保持分离：manifest/schema 不是 rights approval，local verify 不是 remote success，candidate 不是 release，Dashboard artifact 不是 KB canonical truth，结构/入口 evidence 不是 end-to-end capability。

## 最终 diff、registry、Dashboard 与 KB 复核

- 写入前观察到 baseline commit 为 `f93e82c87df36a33f5fe4b74beae85a45a02f03a`；既存 worktree 已有大量 tracked modifications 和 untracked SP-004 artifacts，本轮不归因、不清理。
- 写入前 `python3 Dashboard/tools/session_registry.py reconcile --repo . --check` 与 `validate --repo .` 均为 `pass`，record count 为 29，drift files 为空；本轮只新增 Dashboard/Artifacts 下两个 validation artifacts，不改 Sessions、Index、archive、Stage Plan 或 Current State，因此不触发 registry 内容更新。
- Dashboard 当前仍为：S-025 `Doing`、S-026 `To do`、SP-004 `Doing`。KB 不更新；本轮只写 Dashboard execution evidence。
- 未运行 Git handoff、branch、commit、push、tag、release、remote read-back、rights confirmation 或 production readiness。

## 延后范围与明确禁止的收束

S-026 的独立可见 clean-room Codex newcomer UAT 未执行、未验证、未被本 Review 支持。SP-004 的十项 Finding、rights、release、remote、production readiness 和 Goal completion 均未由本 Review 支持。不得把本 `partial` verdict 改写为 `pass`、`done`、`S-026 complete`、`SP-004 complete` 或 Goal terminal。

## 唯一 Validation verdict

`partial`：fresh public projection 的 export/verify、tree digest、9 个非可执行 core 条目、7 个 CLI 的有界入口证据和 `profile_validator.py` 的 library/N/A 边界已独立观察；但 durable matrix 的逐入口 evidence 不完整，且 row 16 的 CLI 分类错误，另有旧 snapshot registry digest mismatch。因此不能声明 GAP-MH-04 完整通过，也不能支持 S-026 或 SP-004 完成。
