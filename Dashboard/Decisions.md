# Decisions

| ID | Decision | Status | Options | Recommended | Why | Resolution Trigger | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 本轮能力边界 | Done | 仅治理框架 / 治理加产品 KB / 同轮产品实现 | 仅治理框架 | 用户希望后续形成可跨 repo 复用的 SGE Skill，产品实现会污染迁移 claim ceiling | 用户后续另开产品 Goal | 本决策明确排除 CLI、Whisper、FFmpeg 和真实音频 |
| DEC-002 | 仓库与 Skill 命名 | Done | 分层命名 / 项目专用 / 通用治理 | 仓库与 Skill=`sge-governance-skill`；核心入口=`sge-governed-checkpoints` | 将治理能力与未来具体产品仓库彻底隔离 | 公共合同冻结时复核 package metadata | 原 audio-transcriptor 命名仅保留在历史 provenance |
| DEC-003 | Governance Skill 架构 | Done | 通用核心+项目配置 / 项目专用 fork / 保留历史名称 | 通用 `sge-governed-checkpoints` + generic SGE profile | 直接服务未来跨 repo 抽取，避免绑定任何产品仓库 | S-002/S-003 Design Freeze | profile 与核心的边界由 ERBE/Validation 固定 |
| DEC-004 | 历史来源处理 | Done | 清空业务史+保留通用模板 / 保留只读历史 / 完整改名迁入 | 清空具体项目业务史，只保留去项目化通用模板；历史迁移记录只读保存 | 降低搜索污染、错误 authority 和 false closure 风险 | S-012 active surface 清理 | 删除必须可从 Git 历史恢复并逐项解释 |
| DEC-005 | SGE Skill 分层与未来发布边界 | Done | 单一巨型 Skill / 核心+配套+编排+领域扩展 / 全部独立无依赖 | `sge-governed-checkpoints` 通用核心；Dashboard/contract/KB/evaluator/PDI/UAT 为独立配套；Loop 编排与领域扩展均为可选 | 避免核心绑定任何具体产品，同时允许按需逐层采用；Beginner Guide 与独立 UAT 保持不同 authority | 后续公共合同 Session 重新冻结 | 当前只记录设计方向；不创建、发布或同步任何 Skill |
| DEC-006 | Open-source 双仓命名与真源 | Done | 单仓同时开发发布 / 私有 canonical + 公开 projection / 双向同步 | 私有仓 `sge-governance-skill` 是唯一 canonical development source；公开仓固定为 `bm-sge-governance`，只接受 exact-allowlist deterministic projection | 公开仓可保留 GitHub 版本历史与外部 PR，但不能成为第二真源；普通用户直接从公开仓安装，不先 export candidate | SP-003 S-016 source-of-truth freeze | 本决策只冻结架构方向和逻辑名称；owner/URL/default branch、逐文件再分发权、push/tag/release 仍需人类授权 |
