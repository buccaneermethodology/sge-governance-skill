# Sessions

本文件只保留当前与近期 Session。全量定位请使用 [Session Index](Session_Index.md)，完整历史请使用 [Session Archives](Archives/Sessions/)。

Session 的 canonical identity 是 `Parent/Historical ID`。不同 Parent 可能复用 Historical ID，禁止按裸 Historical ID first-wins。

迁移前的表外执行说明完整保存在 [Legacy Execution Notes](Archives/Sessions/Legacy_Execution_Notes.md)。

| Session Key | Historical ID | Parent | Topic | Scope | Purpose | Track | Priority | Status | Historical Status Snapshot | Depends On | Deliverable | Exit Criteria | Next Step | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <a id="sp-004-s-026"></a>`SP-004/S-026` | `S-026` | SP-004 | 独立可见 clean-room Codex newcomer UAT | 独立 task/thread、fresh target、完整 Goal→Session→Validation→closeout | 验证真实新手交互链而非只看文件 | UAT/Validation | P1 | `Doing` | `暂时阻断：create_thread 收到无效参数；保留未关闭状态` | SP-004/S-025 | UAT card、transcript、artifact inventory、独立 Validation | GAP-MH-03 与 copy/paste path 独立通过 | S-027 | `blocked_pending_user_visible_task`；必须先取得真实用户可见 task/thread ID；不允许主线程模拟 |
| <a id="sp-004-s-027"></a>`SP-004/S-027` | `S-027` | SP-004 | release candidate、rights 与发布包预检 | exact candidate、rights 表、checksums、CI/release packet | 在无远端 mutation 下冻结待授权 payload | Release/Preflight | P1 | `Doing` | `本地预检有界证据已落盘；独立 Validation durable verdict 缺失，暂时 blocked` | SP-004/S-026 | candidate manifest、rights packet、release packet、[Validation Review](Artifacts/SP004_S027_ValidationReview.md) | 自动门禁通过且 rights 仍 pending human confirmation | C2 | `blocked_pending_validation_and_human_authority`；C2 是必须停点；不得执行远端 mutation |
| <a id="sp-004-s-028"></a>`SP-004/S-028` | `S-028` | SP-004 | 授权范围内远端发布与 read-back | 仅 exact C2 payload 的 push/tag/release/CI/read-back | 使远端事实与授权 candidate 一致 | External/Release | P1 | `To do` | `Not started` | `SP-004/S-027` + C2 | remote evidence、CI、checksum/read-back | 远端 identity 与授权 payload 一致 | S-029 | 无授权不得启动 |
| <a id="sp-004-s-029"></a>`SP-004/S-029` | `S-029` | SP-004 | 全量独立终态验证与 Goal 收束 | 十项 OPCM、最终 diff、KB/Dashboard、remote state、closeout | 只在全量证据完整且唯一无冲突时收束 | Validation/Closure | P0 | `To do` | `Not started` | SP-004/S-028 | Final Validation、Semantic Review、OPCM、closeout、reconciliation | 十项终态有证据；registry/语言/KB/remote gates 通过 | — | 未通过则保持 partial/blocked |
