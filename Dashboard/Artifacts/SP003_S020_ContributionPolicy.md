# S-020 External PR 单向回流策略

## 关键结论中文展开

公开仓 PR 是输入，不是 canonical truth。维护者必须在私有 `sge-governance-skill` 中审查、移植、补充 provenance，再重新生成 projection、重新执行独立 Validation，之后才有资格进入未来的授权公开更新。没有 remote read-back 或人类授权时，流程停在 candidate/validated 边界。

## 回流流程

1. 记录 PR 编号、作者、提交树摘要、文件清单、许可证声明和审查意见；不把 PR merge 当成批准。
2. 将可接受变更移植到私有 canonical source，并记录 source revision 与变更映射；拒绝直接把 public repo 反向复制为真源。
3. 从新的私有 source revision 按 exact allowlist 生成 fresh projection，执行 residue/object/path/tree/digest 检查。
4. 由独立 Validation/UAT 重算相关正负例，形成新 candidate identity；失败则停止，不更新公开仓。
5. 只有后续人类对具体 repo/tree/payload 的授权存在时，才可执行 public update；该 mutation 和 remote read-back 独立记录。

## 禁止情形

禁止 public PR 直接写回私有 Dashboard/KB truth；禁止 public merge、CI green、作者声明或 GitHub 登录状态替代 canonical review、权利确认、Validation 或 release authorization。PR provenance、source revision、candidate id、projection commit 和 release tag 必须可分别重算。
