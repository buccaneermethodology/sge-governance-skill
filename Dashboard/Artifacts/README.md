# Dashboard Artifact 批次索引

`Dashboard/Artifacts/` 是持久证据的定位面，不直接存放 artifact 文件。每个批次按唯一 owner 收束；批次内文件不重复复制，文件中的仓库相对引用已按新位置重算。

| 批次 | Owner / 身份 | 范围与边界 |
| --- | --- | --- |
| [Stage-Plan-SP-001](Stage-Plan-SP-001/README.md) | `SP-001` | SGE Governance 历史迁移、质量恢复、S-001～S-006、S-012～S-015 及其 provenance/tombstones；不扩大产品、公共发布或生产主张 |
| [Stage-Plan-SP-002](Stage-Plan-SP-002/README.md) | `SP-002` | SP-002 跟踪合同、planning-intake、S-007～S-011 与公共候选证据；不改变其历史有界结论 |
| [Stage-Plan-SP-003](Stage-Plan-SP-003/README.md) | `SP-003` | SP-003 Goal、S-016～S-022、验证、语义复核与收束证据；不把本地/合同范围升级为远端发布 |
| [Stage-Plan-SP-004](Stage-Plan-SP-004/README.md) | `SP-004` | SP-004 S-023～S-029、十项 gap、候选发布、权利、read-back 与有界收束证据；不改变其 Scope Delta/例外边界 |
| [Session-ADHOC-REPOSITORY-CAPABILITY-PANORAMA](Session-ADHOC-REPOSITORY-CAPABILITY-PANORAMA/README.md) | `ADHOC/REPOSITORY-CAPABILITY-PANORAMA` | Repository Capability Panorama 的设计、生成、审计、验证与 closeout；派生读模型，不是 KB 真源或发布批准 |
| [Session-ADHOC-REPOSITORY-QUALITY-AUDIT](Session-ADHOC-REPOSITORY-QUALITY-AUDIT/README.md) | `ADHOC/REPOSITORY-QUALITY-AUDIT` | Repository Quality Panorama 审计、派生 HTML/JSON、审计 lane 与 final validation；不证明 SP-001 或公共发布完成 |

## 组织规则

- 根目录只保留本索引和 owner 批次目录，不使用 symlink。
- `Stage-Plan-SP-001`～`Stage-Plan-SP-004` 使用 Stage Plan 作为最窄稳定 owner；同一 artifact 不再同时放入 Goal 或 Session 副本。
- `RepositoryCapabilityPanorama_*` 使用其自身声明的 ADHOC Session owner；不与 Repository Quality Panorama 混并。
- Session registry 的 authority 仍是 `Dashboard/Sessions.md` 与归档面；本目录只改变 artifact discoverability，不改变生命周期、验证 verdict 或 claim ceiling。
