# S-027 独立 Validation 记录

## 关键结论中文展开

本次 Validation 要判断 S-027 的本地 release-candidate preflight 是否满足原始退出条件，同时检查它是否越过 rights、授权和远端发布边界。当前只能确认本地候选证据已生成；不能给出 `pass`，因为独立 Validation lane 在有界等待内未落盘 durable reviewer artifact，且 C2 的人类授权尚未发生。

## 读取清单（Read Manifest）

已读取或检查：

- [SP-004 Loop Goal](SP004_SemxResidueOpenSourceGaps_LoopGoal.md)：S-027 目标、退出条件、C2 边界与 claim ceiling。
- [S-027 lane card](SP004_S027_ReleaseCandidatePreflightLaneTaskCard.json)：card schema、source refs、write scope、topology 与最大主张。
- [S-027 preflight JSON](SP004_S027_ReleaseCandidatePreflight.json) 与 [preflight 说明](SP004_S027_ReleaseCandidatePreflight.md)。
- [SHA256SUMS](SP004_S027_SHA256SUMS.txt)、[license/NOTICE 报告](SP004_S027_LicenseReport.md)、[rights 表](SP004_S027_RightsConfirmation.md)、[release notes](SP004_S027_ReleaseNotes.md)、[CI 候选](SP004_S027_CIWorkflowCandidate.yml)、[rollback/read-back 计划](SP004_S027_RollbackReadbackPlan.md)。
- `AGENTS.md`、SGE governed checkpoints skill、Dashboard Sessions/Index、S-025 final snapshot、当前最终 diff 与本地门禁输出。

## 实际观察

| 项目 | 结果 | 证据边界 |
| --- | --- | --- |
| lane card validate/render | `pass`（通过） | card digest 为 `8cb21ea62b0b6e9142d222ae840216615ba015fa79ae9173ec8dff19ad002ee5` |
| export/verify | `pass`（通过） | 48 个 allowlisted 文件；tree digest 为 `d84b83cbe264e123a94422ca987bda99345ffa50b8df427e4c94635de5d0c160` |
| SHA256SUMS | `pass`（通过） | 48/48 文件重算匹配 |
| public doctor | `pass`（通过） | 只证明本地 public candidate 合同可检查 |
| 相关 unittest | `pass`（通过） | 16 tests passed；不替代独立 Validation 或 rights |
| registry | `pass`（通过） | reconcile apply 后 check/validate 均通过 |
| closeout-language | `pass`（通过） | S-027 preflight 的中文说明与英文状态均有解释 |
| source cleanliness | `blocked`（阻断） | 当前 checkout 有未提交变更；未形成可发布 clean source revision |
| rights / owner / repo / tag | `pending_human_confirmation`（待人类确认） | 没有逐文件人类确认和具体 payload 冻结 |
| remote / CI read-back | `not_run`（未运行） | C2 前明确禁止 |

## 阻断发现

1. `P1 / validation-evidence-gap`：独立 Validation lane 未在有界等待内写入 durable review；因此本文件不是独立 reviewer 的替代品，S-027 不能获得 `pass` 或 `Done` 的无条件结论。
2. `P1 / authority-gap`：rights owner 尚未逐文件确认，owner/repo/default branch/version/tag/payload 未冻结；这直接阻断 C2 前的 S-028。
3. `P1 / source-cleanliness`：当前 source checkout dirty；候选 projection 的 digest 通过不等于发布 source revision clean。

## 非阻断观察

- checksums、manifest default-deny、license/NOTICE 结构和 rollback/read-back 计划均已形成有界本地证据。
- S-026 的独立可见 UAT 仍为 `blocked_pending_user_visible_task`，没有被 S-027 吸收或伪关闭。

## 验证结论（Verdict）

`blocked`（阻断）：本地预检证据是 `pass_with_bounds`（有界通过），但独立 Validation durable verdict 缺失、source dirty、rights/C2 未决。因此不能声明 S-027 完成、rights approved、release authorized、published、remote read-back verified 或 SP-004 Goal complete。

## Claim ceiling 与下一步

最高允许主张：`release_candidate_preflight_evidence_landed_with_blockers`，即本地候选预检材料已落盘但仍有明确阻断。下一步是先恢复一个可定位、可落盘的独立 Validation lane；其后仍必须在 C2 由人类一次性决定逐文件 rights 和 exact remote payload。C2 未通过前不得启动 S-028。

## 验证交接包

本记录的验证交接包覆盖 claimed scope、原始目标、实际 diff、状态轴、阻断发现与 durable evidence；它不是 S-027 完成授权，也不替代后续独立 post-closeout reconciliation。

Closeout language verdict: pass（通过）

本文使用中文标题和中文解释；其余英文状态仅作为精确状态，并均附中文含义和证据边界。
