# S-027 rollback、撤销与 read-back 计划

本计划只描述授权后 S-028 的操作顺序，不执行远端动作。

1. C2 先冻结 owner/repo URL、default branch、source revision、candidate/tree digest、version/tag、assets、CI 与授权有效期。
2. 授权后仅按 exact payload 执行 push/tag/release；每步记录命令、返回码和授权 reference。
3. 立即独立 read-back commit/tree/tag/assets/checksum/release notes/CI，并与 [SHA256SUMS](SP004_S027_SHA256SUMS.txt) 和 candidate digest 比对。
4. 任一 identity drift、checksum mismatch、CI failure 或部分 mutation 都标记 `partial_remote_mutation` / `blocked`；停止后续写入。
5. 撤销按 C2 预先批准的路径执行：撤下/标记错误 release、发布修复版本或恢复到授权前已知 identity；不擅自删除远端历史。

当前没有 owner/repo/tag/授权 reference，因此 rollback/read-back 只能是计划，不能形成 remote evidence。
