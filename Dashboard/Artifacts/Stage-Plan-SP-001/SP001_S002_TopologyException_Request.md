# S-002 拓扑例外裁决（已批准）

## 请求事项

当前工作树在 S-002 仍为 `Doing` 时已经出现了 S-003 Design 与 S-004 清理变更。固定 DAG 是 `S-002 → S-003 → S-004`，因此这些变更不能被追溯性地吸收为 S-002 证据。

## 已批准裁决

用户已批准一个有界 `topology exception`：保留已经产生的 S-003/S-004 文件变更，但标记为提前候选，不作为 S-002 完成证据；S-002 仍需完成独立 Validation，S-003/S-004 重新建立各自 Context、lane card 与验证记录。

## 影响

- 不改变 MH-01..MH-11、产品非目标或 claim ceiling。
- 不恢复首轮 pre-Builder Semantic Review 时序；该流程 must-have 只能在 OPCM 中记录为 `exception/partial topology evidence`。
- 若不批准，必须先隔离或恢复这些后续 Session 变更，再按原 DAG 重跑 S-002。

## 人类批准

用户已明确批准：

> 允许保留已经产生的 S-003/S-004 文件变更，但必须把它们标记为提前产生的候选、不得作为 S-002 完成证据；S-002 仍需完成独立 Validation，S-003/S-004 重新建立各自 Context、lane card 与验证记录。

批准状态：`approved-bounded-topology-exception`。

该批准不改变 MH-01..MH-11、产品非目标或 claim ceiling；也不把首轮缺失的 pre-Builder 时序改写成已满足。S-002 仍须完成独立 Validation，S-003/S-004 的后续执行必须重新建立治理证据。
