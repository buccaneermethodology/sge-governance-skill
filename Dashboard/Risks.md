# Risks

| ID | Topic | Scope | Purpose | Trigger Signal | Mitigation | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | 双向真源与 public drift | SP-003 private/public repository boundary | 防止公开仓独立修改后与私有 canonical source 漂移 | public PR/commit 未绑定 source revision 或 manifest digest mismatch | public PR 只作输入；回流私有 source 后重新 export/diff/Validation；drift fail closed | Open | 由 S-016/S-017/S-020 处理；不以当前 SP-002 candidate 证据关闭 |
| RISK-002 | 用户承担维护者 export 认知 | SP-003 end-user install/upgrade surface | 防止把 maintainer workflow 暴露给普通用户 | Beginner path 需要手工 export、source 或 private path | 默认 source=current public repo；用户只提供 target；--source 仅高级/测试；S-018 clean-room/UAT 验证 | Open | 由 S-018/S-021 处理；当前只完成设计 |
| RISK-003 | candidate/release/GitHub authority 折叠 | SP-003 release governance | 防止测试或 candidate manifest 被解释为已发布 | CI 自动 push、tag、release 或把 GitHub 登录当授权 | CI 默认 read/check/build candidate；具体 repo/tree/tag/payload 逐次人类授权；S-019/S-022 对账 | Open | 本轮明确不执行任何远端动作 |
