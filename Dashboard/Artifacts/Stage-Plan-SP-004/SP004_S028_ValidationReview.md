# S-027 独立终态 Validation Review

## 关键结论中文展开

本次只读 Validation 检查 S-027 的 durable artifacts 与当前最终 diff，确认 48 个精确公开候选文件是否仍绑定到指定 tree/payload，并检查 card、public doctor、Dashboard registry 和 source cleanliness。用户已在 [S-028 人类授权记录](SP004_S028_AuthorizationRecord.md) 中确认 48 个文件可公开再分发，并授权 `buccaneermethodology/bm-sge-governance`、`main`、`v1.0.0` 的 exact payload。

结论为：`verdict=blocked`（阻断）。候选内容的逐文件 checksum 与 tree digest 通过，但当前最终 diff 使 source checkout 仍被 export 判定为 `dirty_tree`，Dashboard registry 仍存在派生投影漂移。因此本次不能给出 `pass_with_bounds`。本 Review 不执行任何远端 mutation，也不修改既有文件；仅新增本文件作为本次独立 Validation 证据。

## 读取清单（Read Manifest）

已读取或检查：

- `AGENTS.md`、[SGE governed checkpoints skill](../../../.codex/skills/sge-governed-checkpoints/SKILL.md) 及 `validation-agent`、SGC v1 检查要求。
- [S-027 lane card](SP004_S027_ReleaseCandidatePreflightLaneTaskCard.json)，并用用户提供的 digest `8cb21ea62b0b6e9142d222ae840216615ba015fa79ae9173ec8dff19ad002ee5` 做 validate/render。
- [S-027 preflight JSON](SP004_S027_ReleaseCandidatePreflight.json) 与 [preflight 说明](SP004_S027_ReleaseCandidatePreflight.md)。
- [S-027 SHA256SUMS](SP004_S027_SHA256SUMS.txt)、[license/NOTICE 报告](SP004_S027_LicenseReport.md)、[rights 确认表](SP004_S027_RightsConfirmation.md)、[release notes](SP004_S027_ReleaseNotes.md)、[CI 候选](SP004_S027_CIWorkflowCandidate.yml)、[rollback/read-back 计划](SP004_S027_RollbackReadbackPlan.md)。
- [S-028 授权记录](SP004_S028_AuthorizationRecord.md)、[S-028 release lane card](SP004_S028_ReleaseLaneTaskCard.json)、[S-028 release notes](SP004_S028_ReleaseNotes.md)。
- [SP-004 Loop Goal](SP004_SemxResidueOpenSourceGaps_LoopGoal.md)、`Dashboard/Stage_Plans.md`、`Dashboard/Sessions.md`、`Dashboard/Session_Index.md`，以及当前工作树的 tracked/untracked diff。
- 当前最终 diff、`git diff --check`、lane card、public doctor、repository doctor、registry、manifest 文件数、tree digest 与 checksums 重算结果。

## 实际结果

| 检查项 | 实际结果 | 证据边界 |
| --- | --- | --- |
| S-027 lane card digest | `pass`（通过）；实际 digest 为 `8cb21ea62b0b6e9142d222ae840216615ba015fa79ae9173ec8dff19ad002ee5` | `lane_task_card.py validate/render` 通过；仅证明 card 结构和绑定上下文有效 |
| preflight JSON 文件数 | `48` | `candidate_file_count=48`；与指定 preflight artifact 一致 |
| candidate tree digest | `pass`（通过） | 从当前 manifest 的 48 个路径逐项重算为 `d84b83cbe264e123a94422ca987bda99345ffa50b8df427e4c94635de5d0c160` |
| SHA256SUMS | `48/48 pass`（全部匹配） | 48 行均存在且逐文件 SHA-256 与当前候选文件一致 |
| public doctor | `pass`（通过） | 输出 `public_doctor:pass`；只证明 public candidate 合同的本地检查通过 |
| repository doctor | `fail`（失败） | parse/compile、references、public identity、tests、genericity、KB、DKG 等通过；失败面为 registry check/validate 的 projection drift |
| Dashboard registry check | `blocked`（阻断） | `reconcile --check` 报告 `Dashboard/Archives/Sessions/archive_manifest.json` 与 `Dashboard/Session_Index.md` 漂移，且未写入 |
| Dashboard registry validate | `blocked`（阻断） | `validate` 返回 `projection_drift`；未写入 |
| 当前最终 diff | `blocked`（阻断） | `Dashboard/Sessions.md` 有修改；S-028 授权记录、release lane card、release notes 为 untracked；`git diff --check` 本身通过 |
| clean source export | `blocked`（阻断） | 对当前 checkout 执行 `sge_public.py export` 返回 `dirty_tree`，未生成候选目录；因此不能把当前 checkout 证明为 clean source revision |
| 用户 rights/exact payload 授权 | `pass`（通过） | 授权记录绑定 48 文件、tree、owner/repo、`main`、`v1.0.0`；这是本轮 authority evidence，不替代 registry/source-clean evidence |
| 远端 mutation | `not_run`（未运行） | 本次明确禁止 push/tag/release；没有 remote truth 或 read-back 主张 |

## 阻断发现

1. `P1 / source-cleanliness`：当前最终 diff 使 `sge_public.py export` 返回 `dirty_tree`。旧 preflight JSON 中的 `source_worktree_status=dirty_blocker` 与当前复算一致。授权 exact payload 不会自动产生可定位的 clean source revision。
2. `P1 / dashboard-registry-drift`：`reconcile --check` 与 `validate` 都失败，漂移文件为 `Dashboard/Archives/Sessions/archive_manifest.json`、`Dashboard/Session_Index.md`。依据用户“不要修改任何既有文件”的约束，本次不执行 `reconcile --apply`，所以 registry gate 仍未通过。

## 非阻断观察

- `public_doctor:pass`、manifest 48 文件、tree digest 和 SHA256SUMS 48/48 均是有效的本地候选证据。
- 用户授权已解决旧 preflight 中的 rights/owner/repo/branch/version/tag pending 状态，但授权范围只覆盖 exact payload；不能吸收 source cleanliness、Dashboard registry 或远端 read-back 缺口。
- 当前尚无远端 mutation/read-back 证据；S-028 release 是否实际完成不在本次 S-027 验证范围内。

## 主张上限（Claim ceiling）

本次最高允许主张是：

`S-027 candidate artifacts and exact authorized payload are locally checksum/tree-consistent, with source-clean and Dashboard-registry blockers`（S-027 候选 artifacts 与已授权 exact payload 在本地 checksum/tree 上一致，但 source clean 与 Dashboard registry 仍阻断）。

本次不支持：`release_authorized` 之外的远端执行结论、`published`、remote read-back verified、`SP-004 Goal complete` 或任何超出 48 文件/tree digest 的 payload 扩大。

## 明确不证明 production_ready

本 Review 明确不证明 `production_ready`（生产就绪）。`public doctor`、48/48 checksums、tree digest、授权记录和本地 registry/source 检查都不能证明跨平台兼容性、所有能力端到端可用、远端发布成功、CI 结果、运营回滚能力或生产环境安全性。

## 验证交接包

- claimed scope：S-027 durable candidate/release packet 与当前最终 diff 的只读独立验证。
- semantic change：无 runtime/schema/acceptance 修改；只判断现有候选证据、授权边界和当前状态面。
- actual outputs：本文件；不修改既有 artifact，不执行远端动作。
- gates/evidence：lane card validate/render、manifest/tree 重算、SHA256SUMS 48/48、public doctor、repository doctor、registry check/validate、`git diff --check`。
- KB/Dashboard impact：未修改 KB；未用本次验证替代 Dashboard registry 真源，也未执行 registry apply。
- required next action：在不扩大授权 payload 的前提下，形成可定位 clean source revision，并由有权限的维护流程处理 registry projection drift 后重跑 registry gates；随后才可由适用的 S-028/S-029 验证覆盖远端与最终状态。
- Closeout language verdict：`pass`（通过；本文件使用中文标题和中文解释，所有英文 verdict/status 均附中文含义与边界）。

## 验证结论（Verdict）

`blocked`（阻断）。由于 source clean export 与 Dashboard registry 两项当前最终状态证据未通过，本次不满足用户指定的“全部满足才可 `pass_with_bounds`”条件；结论仅限上述 claim ceiling。
