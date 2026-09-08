# Dashboard Artifact 批次索引

`Dashboard/Artifacts/` 是持久证据的定位面，不直接存放 artifact 文件。每个批次按唯一 owner 收束；批次内文件不重复复制，文件中的仓库相对引用已按新位置重算。

| 批次 | Owner / 身份 | 范围与边界 |
| --- | --- | --- |
| [Stage-Plan-SP-001](Stage-Plan-SP-001/README.md) | `SP-001` | SGE Governance 历史迁移、质量恢复、S-001～S-006、S-012～S-015 及其 provenance/tombstones；不扩大产品、公共发布或生产主张 |
| [Stage-Plan-SP-002](Stage-Plan-SP-002/README.md) | `SP-002` | SP-002 跟踪合同与 planning-intake / strategy 来源扩展证据；当前不代表 SP-002 已启动 |
| [Stage-Plan-SP-003](Stage-Plan-SP-003/README.md) | `SP-003`（未登记候选） | 当前工作树已有的未跟踪 Loop Goal prompt；仅保留定位与身份边界，不推断 Dashboard 已登记或执行 |
| [Session-ADHOC-REPOSITORY-QUALITY-AUDIT](Session-ADHOC-REPOSITORY-QUALITY-AUDIT/README.md) | `ADHOC/REPOSITORY-QUALITY-AUDIT` | Repository Quality Panorama 审计、派生 HTML/JSON、审计 lane 与 final validation；不证明 SP-001 或公共发布完成 |

## 组织规则

- 根目录只保留本索引和 owner 批次目录，不使用 symlink。
- `Stage-Plan-SP-001` 与 `Stage-Plan-SP-002` 使用 Stage Plan 作为最窄稳定 owner；同一 artifact 不再同时放入 Goal 或 Session 副本。
- `SP-003` 当前没有对应的 `Dashboard/Stage_Plans.md` 行，故其目录 README 明确标为未登记候选。
- Session registry 的 authority 仍是 `Dashboard/Sessions.md` 与归档面；本目录只改变 artifact discoverability，不改变生命周期、验证 verdict 或 claim ceiling。
