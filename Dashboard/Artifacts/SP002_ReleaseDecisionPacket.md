# SP-002 公共发布决定包

## 当前决定

`release_authorized=false`：尚未取得针对具体 Git remote、tag、release notes 和 public payload 的人类发布授权。因此当前只形成 `candidate_not_approved`（待批准候选），不会自动 push、创建 tag 或 GitHub Release。

## 待人类批准的具体动作

候选完成独立验证后，人类可另行决定是否：确认最终 public manifest payload、选择版本号、提交并推送当前分支、合并主分支、创建远端 tag/release。每项都是独立权限动作。

## 当前证据入口

- [公共 manifest](../../public_export_manifest_v1.json)
- [中文新手指南](../../docs/Beginner_Guide_CN.md)
- [S-010 独立 UAT](SP002_S010_NewcomerUAT.md)
- [最终 Closeout](SP002_S011_FinalClosure_Closeout.md)

## Claim ceiling

即使候选门禁通过，也只支持“在声明的 clean-room 范围内形成可复核候选”；不支持“已发布”“生产就绪”或“任意仓库普遍适用”。
