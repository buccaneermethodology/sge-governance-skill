# S-027 逐文件 rights 确认表

本表绑定候选 `sge-governance-public-candidate-v1`、48 个 allowlisted 文件及候选 tree digest `d84b83cbe264e123a94422ca987bda99345ffa50b8df427e4c94635de5d0c160`。manifest 中的 `MIT` 字段、LICENSE、NOTICE、测试、登录状态或 CI token 都不是人类 rights 确认。

| 文件 | source/license/provenance | source owner 确认 | 再分发确认 | public/execution context | 状态 |
| --- | --- | --- | --- | --- | --- |
| manifest allowlist 中的 48 个精确路径（逐项见 [SHA256SUMS](SP004_S027_SHA256SUMS.txt)） | 均为 repository / MIT / repo-local public candidate 或 SGE core provenance | 待填写姓名/角色/日期/签名引用 | 待逐文件确认 | public=true；execution_context=false | `pending_human_confirmation` |

## 逐项确认要求

在 C2 前不得把上述聚合行改成通过。人类必须针对每个 manifest path 记录：文件路径、实际 source owner、license 与 NOTICE 依据、provenance、是否允许 public redistribution、确认人/角色、确认时间、绑定 candidate/tree digest、撤销条件。任何 unknown、冲突、缺签或 digest drift 都保持 `blocked`。

当前结论：rights 未批准；不得 push、tag、release 或声称 published。
