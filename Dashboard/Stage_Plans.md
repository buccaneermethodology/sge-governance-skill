# Stage Plans



| ID | Topic | Scope | Purpose | Sessions | Current Entry | Required Gates | Status | Claim Ceiling | Next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SP-001 | SGE Governance Skill 历史迁移与质量恢复 | 将历史框架中的通用治理能力抽取为 SGE core，清除 active/public 污染，恢复 semantic-governance truth，并修复引用与验收工具链 | 建立可复用、可验证、与具体产品仓库隔离的治理基础设施 | S-001 → S-002 → S-003 → S-004 → S-005 → S-006；恢复链 S-012 → S-013 → S-014 → S-015 | Goal terminal at S-015 | Intake、Context、ERBE、Goal Conformance、lane cards、strategy canonical mapping、registry、KB render check、DKG、nonzero doctor、SGC、独立 Validation、Semantic Review、closeout-language、post-closeout reconciliation | Done | repo-local SP-001 只在结构、治理、引用和工具链范围内有界完成；不含公共发布、普遍跨 repo 成熟性或生产主张 | SP-002 保持 `To do`，等待用户另行明确启动；不自动进入 S-007 |
| SP-002 | SGE Governance 开源提取与新手可用性 | 在 SP-001 完成后，将 repo-local SGE 核心整理为可审计的公共候选，并用中文 Beginner Guide、安装/doctor 工具和独立小白验收验证；不在本次执行、不实际发布 | 让未来第三方新手可在 clean-room 中安装、理解、运行和卸载，并为公共发布建立 default-deny 边界 | S-007 → S-008 → S-009 → S-010 → S-011 | S-007（等待 SP-001 新 post-closeout 通过及用户另行明确启动） | License/provenance、public export allowlist、ERBE、clean-room、user-acceptance-test、独立 Validation、Semantic Review、closeout-language、release authorization | To do | 最多声明公共发布候选和新手流程已在有界 clean-room 验收；实际发布、普遍适用性和生产成熟性须另有证据与人类授权 | SP-001 最终通过后仍不自动启动；详见 [SP-002 Stage Plan](Artifacts/Stage-Plan-SP-002/SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md) |
