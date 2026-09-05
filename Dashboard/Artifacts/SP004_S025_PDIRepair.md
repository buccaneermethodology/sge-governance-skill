# S-025 能力矩阵 PDI 修复

## 问题与处置

本 PDI 处理独立 Validation 指出的三个问题：

1. `profile_validator.py` 被误标为 CLI；已改为 library validator，CLI 判定为 `N/A`，并保留 import 负例证据。
2. 原 transcript 只有 help 摘要；已补充 7 个 CLI 的成功/预期 fail-closed smoke、library N/A 调用、命令、返回码和 raw output。
3. 历史 S-024 snapshot 的 registry digest 不一致；不修改历史 snapshot，不把 `rebaseline_required` 当通过；本轮 transcript 明确该边界，未来 Validation 以当前 S-025 matrix/transcript 为新 baseline。

## Verification

重新读取 [Capability Matrix JSON](SP004_S025_CapabilityMatrix.json)、[Markdown](SP004_S025_CapabilityMatrix.md) 与 [Execution Transcript](SP004_S025_ExecutionTranscript.json)，确认 17 个 core 条目、8 个 scripts、fresh projection tree digest 和修复 revision 一致。独立 Validation 必须再次从这些 durable inputs 重算，才能决定是否解除 `partial`。

## 复发预防

今后 capability matrix 每个入口必须同时记录类别、命令、返回码、raw output 和 `N/A` 理由；library 不得因文件位于 scripts 目录而自动分类为 CLI。Validation card 的 forbidden claims 继续禁止把 file existence/import/help 直接升级为 end-to-end capability。

## Claim ceiling

本 PDI 不提升 verdict，不支持 S-025 Done、S-026、rights、release、远端、production 或 SP-004 complete。
