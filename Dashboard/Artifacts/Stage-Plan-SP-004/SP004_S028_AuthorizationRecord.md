# S-028 人类授权记录

## 授权内容

2026-09-05，用户明确确认：48 个 allowlisted 文件均可公开再分发，并授权按 exact payload 执行。

绑定 payload：

- owner/repo URL：[https://github.com/buccaneermethodology/bm-sge-governance.git](https://github.com/buccaneermethodology/bm-sge-governance.git)
- default branch：`main`
- source revision/branch：`main`
- version/tag：`v1.0.0`
- release assets：48-file candidate tree digest `d84b83cbe264e123a94422ca987bda99345ffa50b8df427e4c94635de5d0c160`
- candidate：`sge-governance-public-candidate-v1`

## 权限边界

本授权覆盖按上述 exact payload 执行 push、tag、release、CI/read-back 所需的远端 mutation 与读取。不得扩大文件集合、改变 source branch、改写版本/tag、替换仓库，或将结果解释为 production readiness。

## 撤销与偏差

任一 checksum、tree、identity、CI 或远端 read-back 偏差都必须停止并记录为 `partial_remote_mutation` 或 `blocked`；不得伪写成功。该记录是本次 C2 authority reference，不是普遍未来发布授权。
