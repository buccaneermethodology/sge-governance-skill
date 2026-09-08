# SP-004/S-028 v1.0.1 最终独立验证

## 关键结论中文展开

本次只读 Final Validation 检查 S-028 的精确 v1.0.1 远端发布、CI 与 release read-back 是否与授权 candidate 绑定一致。复核范围包括 Loop Goal、S-028 授权记录、CIRevision、S-028 execution/readback、S-027 candidate digest、最终 Dashboard registry，以及 GitHub 当前 main/tag/release/CI 和公开 release assets。

本次支持的结论仅是：精确的 `bm-sge-governance` v1.0.1 release 在指定 source commit、main/tag、48-file candidate digest、release assets 与 CI run `34003056713` 之间保持一致，并完成了独立远端读取与本地 `cmp` 复核。

本次不证明 `production_ready`（生产就绪）、所有平台适用、所有仓库或 Codex 版本适用，也不证明 `SP-004 complete`。S-029 的十项 Finding 全量终态、最终 OPCM、Semantic Review、closeout 与 post-closeout reconciliation 仍不是本文件的验证范围。

## 验证交接包

### Read Manifest

已读取：

- [AGENTS.md](../../../AGENTS.md)：中文 closeout、只读 Validation、SGC、registry 与 claim ceiling 硬门。
- [SP-004 Loop Goal](SP004_SemxResidueOpenSourceGaps_LoopGoal.md)：S-028 目标、C2 exact payload、AC-09/AC-10/AC-11、禁止把 release/read-back 折叠为 production 或 Goal complete。
- [S-028 人类授权记录](SP004_S028_AuthorizationRecord.md)：owner/repo、`main`、48-file candidate tree digest 与 exact payload 权限边界。
- [S-028 CIRevision](SP004_S028_CIRevision.json)：v1.0.1、source commit、candidate digest、CI run 与 claim ceiling。
- [S-028 execution transcript](SP004_S028_ExecutionTranscript.json)：历史 v1.0.0 执行记录及其 CI 未运行的边界；不将其冒充为 v1.0.1 当前证据。
- [S-028 RemoteReadback](SP004_S028_RemoteReadback.json) 与 [v1.0.1 RemoteReadback](SP004_S028_v1.0.1_RemoteReadback.json)：既有 durable read-back 输入，均以本次 live remote commands 重算。
- [S-027 candidate SHA256SUMS](SP004_S027_SHA256SUMS.txt)：48-file candidate 的本地 checksum witness。
- [S-027 CI workflow candidate](SP004_S027_CIWorkflowCandidate.yml)：作为历史候选 artifact；v1.0.1 workflow 的 live cmp 另绑定 source commit witness。
- [S-027 Validation Review](SP004_S027_ValidationReview.md) 与 [既有 S-028 Validation Review](SP004_S028_ValidationReview.md)：历史阻断、授权与 read-back 上下文。
- Dashboard 的 [Sessions](../../Sessions.md)、[Session Index](../../Session_Index.md)、[Current State](../../Current_State.md)、[Stage Plans](../../Stage_Plans.md) 与 [SP-004 archive](../../Archives/Sessions/SP-004.md)。
- `Dashboard/tools/session_registry.py reconcile --repo . --check` 与 `validate --repo .` 的当前只读输出。

### 未作为本次完成依据的项目

- 未修改任何既有文件，未执行 `reconcile --apply`、push、tag、release、CI mutation 或其他远端 mutation。
- 未把现有 Dashboard 行的 `S-028 Doing`、`S-029 To do` 自动改写成完成状态；registry gate 通过不等于 Session/Goal closeout 已完成。
- 未把 S-028 远端事实扩展为 S-026 clean-room UAT、十项 Finding 全覆盖或 SP-004 完成。
- Closeout language verdict：`pass`（通过；中文标题与解释要求已满足）。

## 远端复核结果

| 检查项 | 实际结果 | 证据边界 |
| --- | --- | --- |
| `git ls-remote` main | `9a4fc8f78c58b23f51d92e642e298395ee435c6d` | 远端 `refs/heads/main` 与 CIRevision/source commit 一致 |
| `git ls-remote` tag | `v1.0.1 -> 9a4fc8f78c58b23f51d92e642e298395ee435c6d` | tag 与 main/source commit 一致 |
| GitHub release | `v1.0.1`，非 draft、非 prerelease，target `main` | 公开 release 页面：[v1.0.1](https://github.com/buccaneermethodology/bm-sge-governance/releases/tag/v1.0.1) |
| release assets | `candidate-checks.yml`、`SHA256SUMS`、`sge-governance-v1.0.0-candidate.tar.gz` 均 uploaded | archive 文件名沿用 v1.0.0，但位于 v1.0.1 release；不据此改写为 v1.0.1 archive 文件名 |
| CI run | `34003056713`，`candidate-checks`，head SHA 同 source commit，`success` | job `deterministic-public-candidate`，doctor 与 test suite steps 均 success；[run](https://github.com/buccaneermethodology/bm-sge-governance/actions/runs/34003056713) |
| candidate tree | 48 files，digest `d84b83cbe264e123a94422ca987bda99345ffa50b8df427e4c94635de5d0c160` | 与授权记录、CIRevision、v1.0.1 read-back 一致 |
| remote SHA256SUMS asset | digest `c6fca388e2e38d8e333c56b6e9c4c1363c48e8686a94eb637d1e74fe43c9b241` | 公开 asset 下载后与本地 `SP004_S027_SHA256SUMS.txt` 执行 `cmp`，通过 |
| remote workflow asset | digest `981ca9608d2a960eeaa316140216c5bdd2ced88b73c75fc271f556279972c55d` | 公开 `candidate-checks.yml` 下载后与 source commit `9a4fc8f…` 的本地 Git witness 执行 `cmp`，通过 |
| workflow 绑定 | `.github/workflows/candidate-checks.yml` 在 source commit 存在 | 该 source-commit witness 是 v1.0.1 workflow asset 的正确本地比对对象；S-027 历史候选文件本身不是同一 payload |
| Dashboard registry | `reconcile --check` 通过；`validate` 通过；无 drift files | 当前 registry 计数：29 records、4 current、25 archive；只证明 registry 结构一致 |

## 状态轴与主张边界

- `candidate_built`：在 48-file candidate digest 范围内有证据。
- `locally_validated`：CIRevision 记录的 local doctor/unittest 与远端 CI steps 有证据；只覆盖声明的 workflow 和 candidate。
- `rights_approved` / `release_authorized`：由 S-028 人类授权记录绑定 exact payload；不扩展到未来 payload。
- `remote_mutation_succeeded`：远端 main、tag、release 和 assets 的 live read-back 支持该精确 v1.0.1 release 事实。
- `remote_readback_verified`：main/tag/source commit、release metadata、candidate digest、assets、CI 与两项 `cmp` 均一致。
- `production_ready`：未证明；没有把 CI、release 或 checksum 当作生产就绪证据。

## 非阻断发现与保留边界

1. 旧 [S-028 execution transcript](SP004_S028_ExecutionTranscript.json) 记录 v1.0.0、未包含 workflow 且 CI 未运行；它是历史执行面，不能覆盖当前 v1.0.1 live evidence。
2. [S-028 release lane card](SP004_S028_ReleaseLaneTaskCard.json) 的旧 `maximum_claim_ref` 和 execution command 仍写 v1.0.0；本次不修改它，只将其识别为历史边界，并以当前用户指定的 v1.0.1 CIRevision/远端事实作为本次 read-only validation 输入。
3. Dashboard 当前行仍将 S-028 标为 `Doing`、S-029 标为 `To do`；这是尚未执行 S-029 全量收束的状态事实，不与本次 exact release read-back 通过相矛盾。
4. Release asset 的 archive 文件名仍为 `sge-governance-v1.0.0-candidate.tar.gz`；远端 asset digest 与 v1.0.1 read-back 一致，但本记录不把文件名改称为 v1.0.1。

## 最终验证结论

verdict=pass_with_bounds

中文含义：在声明的 exact v1.0.1 release、source commit、48-file candidate、CI run、release assets、SHA256SUMS 和 workflow source-commit witness 范围内通过；主张上限是该精确 release 的远端 read-back 已复核。该结论不证明 `production_ready`、所有平台适用、所有仓库适用、所有能力端到端可用或 `SP-004 complete`。

## 收束语言验证（Closeout language verdict）

`pass`（通过）：H1/H2 使用中文；英文状态、verdict、hash、run ID 与 claim ceiling 均有中文解释和证据边界。本文件是 S-028 Final Validation evidence，不是 S-029 Goal closeout。
