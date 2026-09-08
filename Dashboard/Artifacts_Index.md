# Dashboard Artifact 批次定位索引

`Dashboard/Artifacts/` 现在只保留批次目录与根 README，不直接罗列 artifact 文件。每个批次按唯一 owner 收束；具体文件清单、来源和边界见对应批次 README。

| 批次 | Owner | 文件范围 | 证据边界 |
| --- | --- | --- | --- |
| [Stage-Plan-SP-001](Artifacts/Stage-Plan-SP-001/README.md) | `SP-001` | 治理迁移、质量恢复、S-001～S-006、S-012～S-015 | 不扩大产品、公共发布或生产主张 |
| [Stage-Plan-SP-002](Artifacts/Stage-Plan-SP-002/README.md) | `SP-002` | Goal/Stage Plan、S-007～S-011、公共候选与验证收束 | 保留历史有界结论与例外，不改写 release authority |
| [Stage-Plan-SP-003](Artifacts/Stage-Plan-SP-003/README.md) | `SP-003` | Goal、S-016～S-022、双仓分发、验证与 closeout | 本地/合同范围不等于公开仓或远端发布 |
| [Stage-Plan-SP-004](Artifacts/Stage-Plan-SP-004/README.md) | `SP-004` | S-023～S-029、十项 gap、候选发布、权利与 read-back | 保留 Scope Delta、例外和 `pass_with_bounds` 边界 |
| [Session-ADHOC-REPOSITORY-CAPABILITY-PANORAMA](Artifacts/Session-ADHOC-REPOSITORY-CAPABILITY-PANORAMA/README.md) | `ADHOC/REPOSITORY-CAPABILITY-PANORAMA` | 所有 `RepositoryCapabilityPanorama*` 文件 | 派生全景/审计读模型，不是 KB 真源或发布批准 |
| [Session-ADHOC-REPOSITORY-QUALITY-AUDIT](Artifacts/Session-ADHOC-REPOSITORY-QUALITY-AUDIT/README.md) | `ADHOC/REPOSITORY-QUALITY-AUDIT` | Repository Quality Panorama 审计批次 | 不证明 SP-001 或公共发布完成 |

## 关于此前根目录罗列

此前大量 `SP002_`、`SP003_`、`SP004_` 文件继续出现在根目录，是因为早先整理只迁移了部分文件；后续新增或遗漏的同 owner 文件没有再次归并。这是目录组织遗漏，不代表新的执行授权、状态变化或更强的验证结论。现在它们分别位于对应的 `Stage-Plan-SP-002/`、`Stage-Plan-SP-003/`、`Stage-Plan-SP-004/` 批次内；文件名仍保留原前缀，便于历史 provenance 和机器引用追踪。

## 组织规则

- 根目录只保留定位 README；不使用 symlink。
- Stage Plan 是 SP artifact 的最窄 owner；同一文件不复制到 Goal 或 Session 目录。
- `RepositoryCapabilityPanorama*` 按其自身 Context Bootstrap/Design 声明的 ADHOC Session 独立收束，不与 Repository Quality Panorama 混并。
- 本次不修改 Session/Goal lifecycle、Validation verdict、Scope Delta、claim ceiling 或 KB canonical truth；只修复路径、相对链接和受影响的机器摘要。
