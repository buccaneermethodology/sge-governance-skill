# SP-002 Goal Patch：开源候选、术语与执行面隔离

## Patch 身份

- Base：[`SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md`](SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md)
- Patch ID：`SP002-GP-001`
- Sequence：`1`
- 类型：把已有 Stage Plan 解析为可下发的 Loop Goal，并补充 glossary 与 public/private execution-surface boundary。
- Scope Delta：新增两个明确的公共合同要求（SGE glossary、执行面隔离）；不删除、不降低原 SP-002 must-have。
- Base revision：`2940aa448fb4c2d1e3081307203565374094514f`（应用本 Patch 前的 Git HEAD）
- Base digest：`73b007a36bf6036b5d49b428539cac5d441684406a1cf5121c37c75090083187`（绑定 Base revision 中 Stage Plan 的真实 SHA-256）
- 被替换 section：无；本 Patch 以新增 Goal handoff 与两项 must-have 为主。
- Replacement：将 tracking Stage Plan 解析为独立 reader-facing Loop Goal，并保留原 `SP002-MH-01..10`。
- Conflicts：无已知冲突；若 base revision/digest 不匹配，必须停止解析并重新建立 Patch。

## 原因

现有文件已经定义了 SP-002 的 Stage Plan、S-007～S-011 和公共发布边界，但还不是完整的 Goal handoff contract：缺少原始目标覆盖矩阵、连续执行规则、明确的术语真源，以及“公共 Skill 仓库”和“本仓库特定执行面”之间的可验收分层。

## 新增要求

1. 在 S-007 冻结一份去 Semx 化的 SGE glossary：canonical source 位于 `kb/data/`，Markdown 是派生阅读面；只纳入可复用治理术语，不复制 Semx 产品 ontology。
2. 冻结四类表面的公共/私有边界：public core、public documentation/KB、private execution memory、private provenance/evidence。
3. public export 必须从显式 default-deny manifest 构建；不能把当前仓库根目录、Dashboard、Agent Logs、历史 provenance 或 dirty worktree 当作发布输入。
4. 每个被公开的文件必须有 source、license、provenance、身份污染和是否含执行上下文的裁决。
5. public package 与 target project execution overlay 必须能在 clean-room 中分别安装、验证和理解；公共包不依赖本仓库的 Session、Goal、历史 artifact 或本机路径。

## 不改变的边界

- SP-002 仍保持 `To do`，本 Patch 不启动 S-007。
- 不实际发布、不 push、不创建 release、不写全局 Skill。
- 不把当前 Dashboard/closeout/Agent Log 状态复制进 public package。
- 不把 Semx glossary、P00–P17、M1/Mc/Flow/DRP、Runtime/SAG/RCP/USL 等产品或 runtime 术语原样迁移。
- glossary 只定义 SGE 稳定治理术语；项目/产品术语由使用该 Skill 的 target repo 自己维护。

## 影响

- `SP002_SGEOpenSourceNewcomerReadiness_StagePlan.md`：增加 Goal 入口、glossary must-have、public/private 分层说明。
- `SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md`：新增最终 Goal handoff contract。
- S-007：新增 glossary contract、公共/私有边界和 default-deny manifest 设计。
- 未来 `kb/data/glossary_v1.json` 与 `kb/docs/Glossary.md`：仅在 S-007 获明确启动授权后创建，并通过 renderer/check。
- `Dashboard/`：继续作为本仓库执行记忆；不得进入 public export，除非某个文件经过逐文件批准并已去执行上下文。

## 解析规则

本 Patch 必须与 base Stage Plan 一起解析，生成完整的 `SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md`。Builder、Validation 和 Closure 只接受解析后的完整 Goal，不接受只携带本 Patch 的 handoff。
