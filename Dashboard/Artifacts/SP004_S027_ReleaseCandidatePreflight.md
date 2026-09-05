# S-027 release candidate、rights 与发布包预检

## 关键结论中文展开

`release_candidate_preflight_complete_with_blockers` 的意思是：本地已从当前冻结 manifest 生成并重算 48 文件候选投影，candidate/tree/tool/manifest identity、checksums、license/NOTICE 结构报告、rights 表、release notes、CI 候选和 rollback/read-back 计划均已落盘；但 source dirty、rights 未逐文件确认、owner/repo/version/tag 未冻结，所以不能发布。

这不是 `rights_approved`、`release_authorized`、`published` 或 `production_ready`。下一步只能由人类在 C2 决定具体授权范围；在决定前不得启动 S-028。

## 落地范围

- 48 个 manifest allowlisted 文件的 clean staging projection：export 返回码 0，verify 返回码 0。
- candidate tree digest：`d84b83cbe264e123a94422ca987bda99345ffa50b8df427e4c94635de5d0c160`。
- manifest digest：`228b28ec802553421b2d590ae289ce4c3609e18afa0a4b0a29b841fc228d5ece`；export tool digest：`1852bd84facb06802476d9872e1afc1fa67f725248a64ac4410abd795bf7427f`。
- [逐文件 SHA256SUMS](SP004_S027_SHA256SUMS.txt)、[license/NOTICE 报告](SP004_S027_LicenseReport.md)、[rights 确认表](SP004_S027_RightsConfirmation.md)、[release notes](SP004_S027_ReleaseNotes.md)、[CI 候选](SP004_S027_CIWorkflowCandidate.yml)、[rollback/read-back 计划](SP004_S027_RollbackReadbackPlan.md)。

## 发布身份与 payload 提案

| 字段 | 当前值 | 证据边界 |
| --- | --- | --- |
| source identity | `sge-governance-skill` | 当前本地 source 标识，不是公开仓 identity 批准 |
| public project | `bm-sge-governance` | Loop Goal 中的 proposal，不是 owner/repo 确认 |
| owner/repo URL | `PENDING_HUMAN_CONFIRMATION` | C2 必须冻结 |
| default branch | `PENDING_HUMAN_CONFIRMATION` | C2 必须冻结 |
| version/tag | `PENDING_HUMAN_CONFIRMATION` | C2 必须冻结 |
| payload | exact 48-file manifest projection + tree digest | 仅本地候选；不得自行扩大 |

## 自动检查与阻断

| 检查 | 结果 | 含义 |
| --- | --- | --- |
| export/verify | `pass`（通过） | 仅证明当前 manifest 的本地 projection 可重算 |
| default-deny inventory | `pass_with_bounds`（有界通过） | 48 文件与 allowlist 一致，不证明 rights |
| license/NOTICE 结构 | `pass_with_bounds`（有界通过） | 结构声明可定位，不替代 owner 确认 |
| source clean | `blocked`（阻断） | 当前 checkout 有未提交变更；发布前必须得到 clean source revision |
| rights | `pending_human_confirmation`（待人类确认） | 逐文件确认缺失 |
| remote/CI/read-back | `not_run`（未运行） | C2 前禁止远端 mutation 与 read-back |

## 明确非目标

本 Session 不执行 source 修复、KB truth promotion、远端访问、push、tag、release、CI 启用、rights 签署或 production readiness 判断。S-026 仍是 `blocked_pending_user_visible_task`，其阻断未被本 Session 吸收。

## 验证交接包

- claimed scope：本地 exact candidate/release packet preflight。
- semantic change：无 runtime/schema/acceptance 改变；仅物化候选 identity 与授权边界。
- changed files：本 Session 新增的 preflight、checksums、license、rights、notes、CI、rollback artifacts；Dashboard session/index 状态说明。
- gates/tests：lane card validate/render、export、verify、registry reconcile/check、registry validate、closeout-language。
- durable evidence：本文件及其链接的 JSON、checksums、rights、license、notes、CI、rollback 文件。
- known risks：dirty source、unknown owner/repo/tag、无逐文件 rights、无 remote read-back；S-026 独立可见 task 仍缺失。
- KB/Dashboard impact：稳定 canonical truth 未改变；Dashboard 只记录执行状态与证据。
- Scope Delta：S-026 暂时 blocked 是状态记录，不删除原始 must-have；S-027 无 scope narrowing。
- 当前 state axes：candidate=true；local preflight=pass_with_bounds；approved=false；rights/release authorization=false；published=false。
- Closeout language verdict：`pass`（通过；已运行 executable `closeout-language`，本文件的中文标题/解释与英文状态说明符合门禁）。

## C2 必须一次性确认

请确认：逐文件 rights、具体 owner/repo URL/default branch、source revision、candidate tree、version/tag、assets、CI，以及是否授权 S-028 执行 push/tag/release/remote read-back。未确认时状态为 `blocked_pending_human_authority`；本 Session 不继续到 S-028。
