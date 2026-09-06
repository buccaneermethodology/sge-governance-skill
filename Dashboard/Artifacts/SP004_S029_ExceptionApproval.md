# SP-004/S-029 人类批准例外登记

## 批准内容

用户于 2026-09-06 明确批准：

1. 暂时取消 S-026 完整 newcomer flow，不把它计为本轮 Goal completion blocker；历史 S-026 partial 证据继续保留。
2. 允许 S-029 以人工批准例外登记 `pass_with_bounds`，不能伪写成无条件独立 Validation pass。
3. 允许在 S-023 无法达到无条件 pass 时登记 `pass_with_bounds`。
4. 授权修复 README 后重新冻结 48-file candidate，并执行新的 rights、CI、push、tag、release 与 remote read-back。

## 边界

这是明确的人类 Scope/Topology/Claim 例外，不是把历史失败改写成成功，也不改变 `candidate`、`published`、`production_ready` 等状态轴。新的 public payload 仅绑定 v1.0.2 exact candidate 和其 read-back。

## 依据

- [S-026 UAT Review](SP004_S026_UATReview.md)
- [S-029 原始 Final Validation](SP004_S029_FinalValidationReview.md)
- [v1.0.2 授权记录](SP004_S029_v1.0.2_AuthorizationRecord.md)
