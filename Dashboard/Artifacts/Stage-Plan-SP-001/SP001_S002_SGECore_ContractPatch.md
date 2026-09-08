# S-002 合同边界修复补丁

## 补丁目的

修复独立 Semantic Review 发现的三项合同边界冲突；不改变原始产品设计，也不扩大 S-002 的产品或发布范围。

## 变更

1. [项目 Profile](../../../kb/data/strategy/sge_project_profile_v1.json) 与 [Workflow Registry](../../../kb/data/strategy/sge_workflow_registry_v1.json) 的派生 DKG 指针改为 `not_configured`。`Dashboard/Artifacts/` 是执行证据目录，包含 Design、ERBE、Validation 与 closeout，不得整体标记为可重建 DKG。
2. [Profile schema](../../../kb/schemas/sge_project_profile_v1.schema.json) 与 [Profile validator](../../../.codex/skills/sge-governed-checkpoints/scripts/profile_validator.py) 将身份禁止字段明确为 `forbidden_target_authority_tokens`，将可保留但默认关闭的领域扩展明确为 `allowed_disabled_extension_ids`。禁止规则只作用于 target authority；因此 `build-kym`、`build-tco-coverage` 的禁用扩展登记不再与目标身份规则冲突。
3. [S-002 Design](SP001_S002_SGECore_Design.md) 与 [ERBE Contract](SP001_S002_SGECore_ERBE_Contract.json) 统一 Builder write exclusions，覆盖 profile、source manifest、canonical mapping、ERBE contract/cases/expected、RED evidence、claim ceiling 与原始产品设计。

## 验证边界

- `s002_erbe_acceptance.py`：C01/C02/C04 为 `pass`，C03 按预期返回 `red`，失败指纹为 `forbidden_source_identity_or_absolute_authority`。
- Profile 正例通过；含相对 `semx-kb` authority 的负例被拒绝；仅在 extensions 中登记禁用 `build-kym`/`build-tco-coverage` 的候选通过。
- 原始产品设计文件未修改，SHA-256 仍为 `3ca2d5f98991b05612b06647e25e65319c0850d6909a14e760aa095f433d17f4`。

## Scope Delta

无。该补丁只是落实 S-002 已记录的 blocker 修复，不删除或降级原始 must-have；独立 Validation 与 Semantic Review 仍是关闭门禁。
