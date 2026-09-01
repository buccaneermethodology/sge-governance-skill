# Sessions

本文件只保留当前与近期 Session。全量定位请使用 [Session Index](Session_Index.md)，完整历史请使用 [Session Archives](Archives/Sessions/)。

Session 的 canonical identity 是 `Parent/Historical ID`。历史 ID 可能重复；例如 `SP-063/S-478` 与 `SP-064/S-478` 是两条不同记录，禁止按裸 `S-478` first-wins。

迁移前的表外执行说明完整保存在 [Legacy Execution Notes](Archives/Sessions/Legacy_Execution_Notes.md)。

| Session Key | Historical ID | Parent | Topic | Scope | Purpose | Track | Priority | Status | Historical Status Snapshot | Depends On | Deliverable | Exit Criteria | Next Step | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <a id="sp-001-s-002"></a>`SP-001/S-002` | `S-002` | SP-001 | 来源、project profile、ERBE 与通用 SGE 核心冻结 | 固定源 provenance，建立 project profile，冻结 Contract/Cases/RED/write exclusions | 为迁移建立不可偷换的机器合同与最小通用核心边界 | Governance Contract | P0 | `To do` | `—` | SP-001/S-001 | source manifest、profile/schema、ERBE bundle、Design artifact | frozen identity 和 trusted RED 通过，Builder write scope 明确 | 用户启动 SP-001 后进入 S-002 intake | 不在本次 S-001 授权内执行 |
| <a id="sp-001-s-003"></a>`SP-001/S-003` | `S-003` | SP-001 | Governance Skills 与 deterministic tooling 迁移 | 迁移适用 Skills、schemas、scripts 和通用 workflow registry | 使 repo-local checkpoints 可在 audio-transcriptor 中执行并为跨 repo 抽取做准备 | Governance Implementation | P0 | `To do` | `—` | SP-001/S-002 | sge-governed-checkpoints、portable Skills、tooling tests | Skill/interface acceptance 全部通过，无 Semx product path hardcode | S-002 closeout 后自动进入 | 不含产品 runtime |
| <a id="sp-001-s-004"></a>`SP-001/S-004` | `S-004` | SP-001 | KB、AGENTS、Dashboard tools 整理及身份污染清除 | 适配 truth/authority surfaces，删除无意义的 Semx/KYM/TCO/runtime 历史实践 | 形成新项目自洽且低污染的治理目录 | Governance Truth Placement | P0 | `To do` | `—` | SP-001/S-003 | KB governance truth、适配后的 AGENTS/Dashboard、删除与替代清单 | 身份、绝对路径、KB/Dashboard、registry/DKG gates 通过 | S-003 closeout 后自动进入 | 原始产品设计必须保持字节不变 |
| <a id="sp-001-s-005"></a>`SP-001/S-005` | `S-005` | SP-001 | 集成验收、独立 Validation 与 Semantic Review | 对最终候选执行完整本地 gates、原目标审计和语义架构复核 | 阻止工具自报、局部测试或保守措辞冒充整体迁移完成 | Governance Validation | P0 | `To do` | `—` | SP-001/S-004 | acceptance evidence、Validation Review、Semantic Review | blocking findings 清零或触发合法终止条件 | S-004 closeout 后自动进入 | 必须覆盖 actual final candidate diff |
| <a id="sp-001-s-006"></a>`SP-001/S-006` | `S-006` | SP-001 | Goal closeout 与最终对账 | 形成中文 closeout、OPCM、Scope Delta、KB/Dashboard review 和 post-closeout reconciliation | 给 Goal completion 提供唯一、无冲突、覆盖最终状态的证据 | Governance Closure | P0 | `To do` | `—` | SP-001/S-005 | final closeout、coverage matrix、post-closeout validation | SP-001 completion rule 全部满足，否则保持 partial/blocked | S-005 通过后自动进入 | 单个 Session Done 不等于 Goal complete |
