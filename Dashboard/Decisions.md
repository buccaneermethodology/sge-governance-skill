# Decisions

| ID | Decision | Status | Options | Recommended | Why | Resolution Trigger | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 本轮能力边界 | Done | 仅治理框架 / 治理加产品 KB / 同轮产品实现 | 仅治理框架 | 用户希望后续形成可跨 repo 复用的 SGE Skill，产品实现会污染迁移 claim ceiling | 用户后续另开产品 Goal | 本决策明确排除 CLI、Whisper、FFmpeg 和真实音频 |
| DEC-002 | 项目与命令命名 | Done | 分层命名 / 全部 transcriptor / 全部 transcript | 项目与 Skill=`audio-transcriptor`；CLI=`audio-transcript` | 保留易用 CLI，同时不改变项目身份 | 产品合同冻结时复核 CLI entrypoint | 当前仓库目录保持 audio-transcriptor-skill |
| DEC-003 | Governance Skill 架构 | Done | 通用核心+项目配置 / 项目专用 fork / 保留 Semx 名称 | 通用 `sge-governed-checkpoints` + audio-transcriptor profile | 直接服务未来跨 repo 抽取，避免制造第二个项目专用治理 fork | S-002 Design Freeze | profile 与核心的边界必须由 ERBE/Validation 固定 |
| DEC-004 | Semx 历史处理 | Done | 清空业务史+保留通用模板 / 保留只读历史 / 完整改名迁入 | 清空 Semx 业务史，只保留去项目化通用模板 | 降低搜索污染、错误 authority 和 false closure 风险 | S-004 删除与替代审计 | 删除必须可从 Git seed 恢复并逐项解释 |
| DEC-005 | SGE Skill 分层与未来发布边界 | Done | 单一巨型 Skill / 核心+配套+编排+领域扩展 / 全部独立无依赖 | `sge-governed-checkpoints` 通用核心；Dashboard/contract/KB/evaluator/PDI/UAT 为独立配套；`run-sge-loop-goal-cycle` 为高级编排；KYM/TCO 为可选领域扩展 | 避免核心绑定 Semx/KYM/TCO，同时允许新手按需逐层采用；Beginner Guide 与独立 UAT 保持不同 authority | SP-002 S-007 重新冻结公共合同 | 本轮只记录设计方向；不创建、发布或同步任何 Skill |
