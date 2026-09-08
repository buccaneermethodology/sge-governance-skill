# S-019 身份、许可证、发布与权限合同

## 关键结论中文展开

本 Session 把“版本是什么”“谁能写 GitHub”“候选是否批准”“是否已发布”拆成独立状态轴。当前本地实现只可生成 candidate evidence；本轮没有 GitHub remote、owner、URL、default branch、逐文件再分发权或 mutation 授权，因此这些字段保持 `needs_human_confirmation`，不能由测试或登录状态推断。

## 身份轴

| 身份 | 载体 | 可证明 | 不可替代 |
| --- | --- | --- | --- |
| `source_revision` | 私有仓 HEAD/受控 revision | 开发真源输入 | 不等于 candidate/release |
| `manifest_revision` | allowlist manifest digest | 内容裁决版本 | 不等于 source revision |
| `export_run_id` | 单次本地导出 metadata | 本次运行 | 不等于 commit/tag |
| `candidate_id` | manifest/metadata | 候选身份 | 不等于 validated/approved |
| `projection_commit` | 公开仓 commit | 外部 mutation 后的树身份 | 当前为 null |
| `release_tag` | 具体 tag/release | 外部发布资产身份 | 当前为 null |

## 状态轴与权限

`candidate`、`validated`、`approved`、`published`、`production_ready`、`git_mutation`、`license_authorized` 分别记录；任何状态变化需要自己的 witness。CI 默认只能 read/check/build candidate，不持有 push/tag/release 权限。对具体仓库、commit/tree、tag、release payload 和逐文件权利的授权由人类逐次确认。

## 许可证与发布门

LICENSE/NOTICE、manifest 中的 license 字段和测试通过只是结构证据；不能单独证明逐文件再分发权。发布前必须有人类确认权利、仓库身份、目标分支、payload、回滚策略和 remote read-back 计划。本 Loop 的 no-external-side-effect 边界禁止执行这些动作。

## 可接受主张

允许：“本地 candidate 的身份字段与状态轴可重算”“权限矩阵已冻结为默认无发布权”。不允许：“GitHub 已发布”“candidate 已获批准”“production-ready”“CI 可以安全发布”。
