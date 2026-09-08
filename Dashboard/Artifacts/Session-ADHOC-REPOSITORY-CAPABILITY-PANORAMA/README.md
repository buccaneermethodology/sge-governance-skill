# Repository Capability Panorama Artifact 批次

## Owner 与范围

- Owner：`ADHOC/REPOSITORY-CAPABILITY-PANORAMA`，对应已有 Context Bootstrap 的 `task_id=repository-capability-panorama-2026-09-04`。
- Scope：能力全景的设计、确定性生成器、JSON/Markdown/HTML 派生读模型、质量与 Semx 残留审计、各 lane card/prompt、独立 Validation、closeout 与 post-closeout reconciliation。
- Non-goal：不把派生全景图、结构扫描或本地验证升级为 KB canonical truth、公开仓、逐文件权利批准、release 或 production readiness。

## Provenance

所有 `RepositoryCapabilityPanorama*` 文件从 `Dashboard/Artifacts/` 根目录迁入本批次。目录变化只改善 discoverability；不改变文件原有的证据层级、历史冲突、claim ceiling 或远端权限边界。

## Artifact 索引

- 设计与入口：`RepositoryCapabilityPanorama_ContextBootstrap.json`、`RepositoryCapabilityPanorama_Design.md`。
- 派生输出：`RepositoryCapabilityPanorama_Data.json`、`RepositoryCapabilityPanorama.md`、`RepositoryCapabilityPanorama.html`、`RepositoryCapabilityPanorama_Generator.py`。
- 审计与收束：`RepositoryCapabilityPanorama_Audit_Report.md`、`RepositoryCapabilityPanorama_ValidationReview.md`、`RepositoryCapabilityPanorama_Closeout.md`、`RepositoryCapabilityPanorama_PostCloseoutReconciliation.md`。
- 其余 `RepositoryCapabilityPanorama_*LanePrompt*`、`*LaneTaskCard*`、`*StateSnapshot*` 与审计报告为对应协作和验证证据。
