# Sessions

本文件只保留当前与近期 Session。全量定位请使用 [Session Index](Session_Index.md)，完整历史请使用 [Session Archives](Archives/Sessions/)。

Session 的 canonical identity 是 `Parent/Historical ID`。历史 ID 可能重复；例如 `SP-063/S-478` 与 `SP-064/S-478` 是两条不同记录，禁止按裸 `S-478` first-wins。

迁移前的表外执行说明完整保存在 [Legacy Execution Notes](Archives/Sessions/Legacy_Execution_Notes.md)。

| Session Key | Historical ID | Parent | Topic | Scope | Purpose | Track | Priority | Status | Historical Status Snapshot | Depends On | Deliverable | Exit Criteria | Next Step | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <a id="sp-002-s-007"></a>`SP-002/S-007` | `S-007` | SP-002 | 公共合同、license/provenance 与四层 Skill 架构冻结 | 在 SP-001 完成后冻结 public/private allowlist、license、provenance、core/companion/orchestrator/domain-extension 边界与 ERBE | 防止把 repo-local 候选未经授权包装成可公开发布的巨型 Skill | Public Contract | P0 | `To do` | `—` | SP-001 complete | Public Contract、export manifest/schema、Design 与 Semantic Review | provenance 完整、negative cases 与公共 claim ceiling 冻结 | 等待 SP-001 complete 后由用户另行启动 SP-002 | 当前不可启动；本轮只创建 tracking row |
| <a id="sp-002-s-008"></a>`SP-002/S-008` | `S-008` | SP-002 | 中文 Beginner Guide 与 bootstrap 工具 | 编写 Quick Start、傻瓜式指南、minimal project、install/doctor/bootstrap/upgrade/uninstall | 让无 Semx 背景的新手可完成最小治理循环并安全恢复 | Newcomer Enablement | P0 | `To do` | `—` | SP-002/S-007 | Beginner Guide、copyable prompts、minimal repo、工具与 fixtures | 文档命令、工具行为和错误恢复在 clean-room 一致 | S-007 closeout 后自动进入 | 指南不是 UAT verdict，也不证明普遍易用 |
| <a id="sp-002-s-009"></a>`SP-002/S-009` | `S-009` | SP-002 | 通用 Loop 编排与 optional extension 接口 | 将 run-loop-goal-cycle 去 Semx/KYM/TCO 硬编码并定义 companion/domain hooks | 提供高级自动化但保持核心 Skill 可独立安装和使用 | Optional Orchestration | P1 | `To do` | `—` | SP-002/S-008 | run-sge-loop-goal-cycle candidate、extension registry、tests | 无默认 Semx/KYM/TCO/ChatGPT project 依赖；缺扩展时核心仍通过 | S-008 closeout 后自动进入 | build-kym/build-tco-coverage 仅为 optional domain extensions |
| <a id="sp-002-s-010"></a>`SP-002/S-010` | `S-010` | SP-002 | clean-room 安装与独立小白验收 | 全新环境按 Beginner Guide 完成安装、最小 Goal/Session、Validation、closeout、故障恢复和卸载 | 用独立真实用户路径识别文档作者和 Skill 作者看不到的问题 | Independent Newcomer UAT | P0 | `To do` | `—` | SP-002/S-009 | clean-room evidence、user-acceptance-test verdict、repair loop | 独立 UAT 对真实入口给出有界通过结论且 blocking findings 清零 | S-009 closeout 后自动进入 | 一问一答；不可用作者自检替代 |
| <a id="sp-002-s-011"></a>`SP-002/S-011` | `S-011` | SP-002 | 公共发布候选、独立 Validation 与 closeout | 生成 default-deny candidate package，完成 OPCM、Semantic Review、Validation 与 post-closeout reconciliation | 形成可供人类决定是否发布的稳定候选，而不越权执行发布 | Release Candidate Closure | P0 | `To do` | `—` | SP-002/S-010 | package/manifest、Validation/Semantic、中文 closeout、release decision packet | candidate gates 全部通过；实际发布仍需具体人类授权 | S-010 通过后自动进入 | 不 push、不 release、不写全局，除非用户另行批准具体 payload |
