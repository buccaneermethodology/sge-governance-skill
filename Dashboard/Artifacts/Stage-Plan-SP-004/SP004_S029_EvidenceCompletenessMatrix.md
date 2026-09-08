# SP-004/S-029 原始目标证据完整性矩阵

## 关键结论中文展开

本矩阵逐项覆盖 SP-004 的十个原始 must-have。它证明最终审计已保留原始分母，并没有把 S-026 的 `partial` 或 S-028 的 exact release 事实折叠成 Goal 完成。由于 S-026 仍未满足完整 clean-room 交互链，整体只能是 `blocked/partial`。

| 原始要求 | 可观察验收与精确证据 | 实际结果 | 状态 | 阻断/例外 | 时序/拓扑 | Claim ceiling | Parent/Closeout 吸收 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GAP-MH-01 Identity | [S-024 Closeout](SP004_S024_Closeout.md) 的 identity 正负门禁；[S-028 read-back](SP004_S028_v1.0.1_RemoteReadback.json) 的公开仓身份 | 本地修复与 exact remote identity 均有证据 | 有界满足 | 需由最终独立 reviewer 重算，不推广通用身份能力 | S-024 → S-028 | exact surfaces only | S-029；不单独支撑 Goal |
| GAP-MH-02 Quick Start | [S-024 Validation](SP004_S024_ValidationReview.md)；[S-026 UAT Review](SP004_S026_UATReview.md) 与 transcript | Quick Start/指南通过；README 第一 bash fence 占位符原样执行失败 | partial | copy/paste 入口仍有公开缺口 | S-024 → 独立 S-026 task | one observed candidate flow | S-026 parent 保持 Doing |
| GAP-MH-03 Codex UAT | [S-026 UAT Review](SP004_S026_UATReview.md)、[target Review](../../../tests/bdd/readable_cards/sp004/s026/target/Dashboard/Artifacts/Review.md) | 真实 task/fresh target 已取得；系统注入上下文，M5 closeout/reconciliation 未完成 | blocked/partial | 严格 clean-room 与完整 Goal→Session→Validation→closeout 未通过 | task `01a0744b-2796-7183-b10a-4c5d5b4cb3a6` | one partial observed flow | 当前 Goal blocker |
| GAP-MH-04 Core coverage | [S-025 Closeout](SP004_S025_Closeout.md)、[S-025 Final Validation](SP004_S025_FinalValidationReview.md) | 48-file candidate、17 core、8 scripts 有界矩阵；保留 topology exception | pass_with_bounds | 非独立完整 capability pass | S-025 main-thread compensation | frozen consumer only | S-025 archive；不吸收 S-026 |
| GAP-MH-05 Rights | [S-028 Authorization](SP004_S028_AuthorizationRecord.md) | 48 个 allowlisted 文件 exact payload 获人类授权 | authorized exact payload | 不扩大到未来 payload/生产权利 | C2 → S-028 | exact authorized files | S-027/S-028 |
| GAP-MH-06 Release assets | [S-028 Closeout](SP004_S028_Closeout.md)、[Final Validation](SP004_S028_FinalValidationReview.md) | v1.0.1、CI、checksum、assets、remote read-back 一致 | pass_with_bounds | 仅 exact release 事实 | S-027 → S-028 | published/read-back exact release | S-028；不等于 Goal |
| GAP-MH-07 Provenance links | [S-024 Closeout](SP004_S024_Closeout.md)、candidate manifest 与 remote read-back | typed locator/default-deny 证据存在 | bounded | 仍须按 public/private 类型逐项复核 | S-023/S-024/S-029 | declared locator policy | S-029 pending final absorption |
| GAP-MH-08 Pilot ID | [S-024 Validation](SP004_S024_ValidationReview.md) | 公共接口已中立化，历史 provenance 保留隔离 | bounded | 不证明所有下游仓库 | S-024 | declared project-neutral repair | S-029 pending final absorption |
| GAP-MH-09 Semx residue | [S-023 Contract/Cases](SP004_S023_Contract.json)、[S-024 Closeout](SP004_S024_Closeout.md) | deny token/fixture 与 product dependency 分离 | preserve-and-prove | 不能用 grep 零命中替代语义分类 | S-023 → S-029 | contextual residue evidence | S-029 pending final absorption |
| GAP-MH-10 History provenance | [S-024 Closeout](SP004_S024_Closeout.md)、candidate manifest、[S-028 read-back](SP004_S028_v1.0.1_RemoteReadback.json) | public default-deny 排除私有 Dashboard/history；私有 provenance 保留 | preserve-and-prove | 需最终对账确认无 public/private 污染 | S-023/S-024/S-029 | exact public/private boundary | S-029 pending final absorption |

## Scope Delta 审计

未发现已批准的删除、合并或降级。S-025 topology exception、S-026 `partial/blocked` 和 S-028 CI/v1.0.1 修订均被保留为状态/例外，而不是 Scope Delta 后完成。S-028 只改变了用户明确授权的 exact release payload；不改变原始十项分母。

## 结论

`goal_terminal=false`；`next_session=S-026 repair or human-approved resolution`；`next_session_ready=false`；`human_decision_required=true`（若要以新 candidate 修复 README 并重新发布，需新的 exact payload/rights/remote authorization）。本矩阵不支持 `SP-004 Goal complete`。
