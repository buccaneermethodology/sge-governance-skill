# Stage Plans



| ID | Topic | Scope | Purpose | Sessions | Current Entry | Required Gates | Status | Claim Ceiling | Next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SP-001 | audio-transcriptor SGE Governance 迁移 | 把 Semx 空框架迁移为通用 SGE core + audio-transcriptor profile；逐一审计 strategy 56 个表面并只迁移经重新冻结的通用 truth；删除项目污染；不实现转写产品 | 建立可运行、可验证并可在未来抽取到其他 repo 的治理基础设施 | S-001 → S-002 → S-003 → S-004 → S-005 → S-006 | — | Intake、Context、ERBE、Goal Conformance、lane cards、strategy provenance/canonical mapping、registry、SGC、独立 Validation、Semantic Review、closeout-language、post-closeout reconciliation | Done | 仅能声明本仓库 repo-local SGE Governance 框架已完成有界迁移与本地结构/治理验收（含已批准 topology exception），不含产品实现、发布或普遍跨 repo 成熟性 | Final closeout、OPCM 与 post-closeout reconciliation 已通过；SP-002 仍为 To do |
| SP-002 | SGE Governance 开源提取与新手可用性 | 在 SP-001 完成后，将 repo-local SGE 核心整理为可审计的公共候选，并用中文 Beginner Guide、安装/doctor 工具和独立小白验收验证；不在本次执行、不实际发布 | 让未来第三方新手可在 clean-room 中安装、理解、运行和卸载，并为公共发布建立 default-deny 边界 | S-007 → S-008 → S-009 → S-010 → S-011 | S-007（依赖 SP-001 complete，当前不可启动） | License/provenance、public export allowlist、ERBE、clean-room、user-acceptance-test、独立 Validation、Semantic Review、closeout-language、release authorization | To do | 最多声明公共发布候选和新手流程已在有界 clean-room 验收；实际发布、普遍适用性和生产成熟性须另有证据与人类授权 | SP-001 完成后另行明确启动；详见 [SP-002 Stage Plan](Artifacts/SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md) |
