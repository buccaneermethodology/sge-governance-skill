# SP-001 S-015 语义阻断修复增量复核

## 任务与证据边界

本轮复用[首轮独立 Semantic Review](SP001_S015_SemanticReview_Round1.md)作为 baseline，只检查 `SEM-B01` taxonomy、`SEM-B02` candidate state、`SEM-B03` Graph ontology removal 与 `SEM-B04` Builder topology disposition。Reviewer 未修改 Builder 产物；`render_kb.py --check` 通过只证明候选 JSON 与阅读面一致，不替代本语义判定。

最大主张是判断三份 `reviewed_candidate` 是否具备进入显式 active-promotion 步骤的条件；本 review 不直接把状态写成 `active`，不关闭 SP-001，也不证明公共发布或生产成熟。

## Frame-First 与语义架构复核

- Truth carrier：三份策略的稳定规则由 `kb/data` JSON 承载，`kb/docs` 是确定性阅读面；来源裁决、Builder 日志、OPCM 与 closeout 仍是 Dashboard evidence，不反向成为 semantic law。
- Object responsibility：Human-AI、Semantic Surface、KB Promotion 分别承载协作边界、诊断 vocabulary、truth promotion/source policy，没有把 witness、evaluation result 和 governance decision塞入同一 God Object。
- 依赖方向：Human-AI 为基础层，Semantic Surface 依赖 Human-AI，KB Promotion 依赖前两者；未见循环。
- Promotion boundary：`reviewed_candidate` 表示候选已完成内容修复但仍等待显式 promotion decision；它不是 `active`、`approved`、`done` 或 release authority。

## 四项 blocker 重算

| Blocker | 当前证据 | 判定 | 影响 |
| --- | --- | --- | --- |
| `SEM-B01 taxonomy` | Semantic Surface 已恢复与仓库 Skill 一致的 S1 Intent Misalignment、S2 Semantic Drift、S3 Semantic Overclaim、S4 Semantic Ambiguity、S5 Semantic Unverifiability、S6 Semantic Authority Confusion，并新增 L0-L6 diagnostic surfaces；同时明确二者不是数值评分或普遍科学定律 | `closed`，中文含义是 taxonomy 不再静默改义 | 可进入 promotion 审查 |
| `SEM-B02 candidate-state` | 三份 canonical JSON 均使用 `status=reviewed_candidate`；S-013 closeout 明示 `candidate pending final Semantic Review`，OPCM 仍写 `landed candidate` | `closed`，中文含义是 candidate 与 active 状态已分离 | 本 review 可判定 promotion eligibility，但不能自动改为 active |
| `SEM-B03 graph-ontology` | KB Promotion 的 doc ID、title、output path 和阅读面文件名均已移除 `Graph`；正文没有把 KG/GEXF/Graph 定义为 active ontology、runtime 或 source contract，仅在明确非承诺中排除“图”行为 | `closed`，中文含义是被来源 adjudication 拒绝的 Graph/GEXF 语义没有从命名恢复 | 可进入 promotion 审查 |
| `SEM-B04 topology-disposition` | Builder Agent Log 与 OPCM 已写明 task identity=`/root`、Orchestrator 同时承担 Builder、三条 delegated audit lane 与两个 final reviewer 的实际时序；但它又将 `Single-Agent Exception` 判为 `not_applicable`，并声称不需要例外 | `open process blocker`，中文含义是事实身份已透明，但 disposition 与当前仓库默认 lane 规则仍未对齐 | 阻止 active promotion 与 SP-001 completion |

## B04 仍阻断的理由

当前仓库硬门要求 non-trivial governed work 默认启动 Design、Builder、Validation、Closure lanes；默认 lane 未启动时，closeout 必须记录 `Single-Agent Exception` 的原因、风险、补偿检查及缺失 verdict。Builder 由 Orchestrator 主任务承担并不等于“整个任务是单 Agent”，但也不能据此把缺少独立 Builder lane 的例外判为 `not_applicable`。

本 Goal 确实没有要求“独立 user-visible Builder task”，所以这里不是需要人类批准的 user-visible topology Scope Delta；然而仍需按普通 Multi-Agent Gate 记录有界 `Single-Agent Exception`，明确：Builder lane 未独立启动、原因是共享工作树写冲突、Design/Validation/Semantic 的独立性仍保留、补偿证据为何足够，以及 claim ceiling 不扩大。完成该 disposition 修复不需要重做 Builder 实现，但需要更新 closeout/OPCM/Agent Log 后再做窄 semantic reconciliation。

## 状态词压缩误读测试

- `reviewed_candidate`：只允许理解为“内容已接受本轮 review，可被提交到显式 promotion decision”；不得压缩为 active/approved/canonical completion。
- `landed candidate`：只表示候选文件已写入工作树；不得解释为稳定 truth 已 active promotion。
- `Builder task=/root`：只描述实际执行 identity；不得解释为独立 Builder lane 已满足，也不得解释为整个任务 single-agent。
- `render check pass`：只证明 JSON 与 Markdown 投影一致；不得解释为 semantic correctness、SP-001 complete 或 public-ready。

## Future-Agent misuse 场景

1. 未来 Agent 看到文件位于 `kb/data` 就忽略 `reviewed_candidate`，直接当 active truth。缓解：promotion 必须显式变更状态、记录 decision，并重跑 render/final Validation。
2. 未来 Agent 从旧 Graph 文件名恢复 KG/GEXF scope。缓解：当前 doc ID、title、output path 已统一为 Source Policy；旧文件名不得保留为 active alias。
3. 未来 Agent 看到 Builder 日志写着“不是 single-agent”就推断默认 Builder lane 无需例外。缓解：明确区分“整体多 Agent”与“某个默认 lane 未独立启动”，记录有界 `Single-Agent Exception`。
4. 未来 Agent 把 taxonomy/L0-L6 当 numeric scorecard 或 runtime mandate。缓解：当前 constraints 与 claim ceiling 明确其仅为诊断 vocabulary。

## 双 Verdict

- `Design Freeze Validity: PASS_WITH_PROCESS_BLOCKER`。中文含义：三份 strategy 的 semantic frame、taxonomy、状态边界和 Graph ontology 修复已有效，未发现新的内容层 semantic blocker；但 B04 的治理 disposition 仍违反当前完成流程，不能据此直接 active promotion。
- `Implementation Entry Readiness: READY_FOR_B04_DISPOSITION_REPAIR_ONLY`。中文含义：下一最小安全步骤不是继续改三份策略内容，而是把 Builder lane 例外按仓库规则写入 Agent Log、OPCM 与 closeout，然后用新摘要做一次窄 reconciliation。

## Active promotion 判定

`reviewed_candidate` 当前**不可直接进入 `active` 状态写入**。

更精确地说：B01-B03 已使三份候选具备内容层 promotion eligibility；B04 关闭前，只允许写“reviewed candidate 内容可进入显式 promotion decision 的候选队列”，不允许写“已批准 active promotion”“canonical active”或等价措辞。B04 disposition 修复并经独立 delta reconciliation 后，才可执行显式状态 promotion、重新渲染阅读面，并由 final Validation 覆盖 promotion 后实际 diff。

## 剩余修复与允许措辞

Required repair：

1. 将 Builder topology 的 `Single-Agent Exception` 从 `not_applicable` 改为有界例外记录；不把它写成需追溯批准的 user-visible task Scope Delta。
2. 让 OPCM/closeout 明确整体 multi-agent 与 Builder lane 例外可同时成立。
3. 修复后重跑 lane card-bound Semantic delta、`render_kb.py --check` 与 final Validation。

当前允许措辞：

> 三份 semantic-governance strategy 的 taxonomy、candidate-state 与 Graph ontology blocker 已关闭，内容层已具备 promotion eligibility；Builder lane disposition 尚待按仓库规则记录，因此仍保持 `reviewed_candidate`，不得直接写为 `active`。

当前禁止措辞：`active promotion passed`、`canonical active`、`S-013 Done`、`SP-001 Done`、`public-ready` 或任何发布/生产结论。

## 验证交接包

- 本 review 覆盖 B01-B04、三份 candidate JSON/阅读面、S-013/S-015 closeout、OPCM、Builder Agent Log 与当前 delta diff。
- 尚未允许的状态变化：`reviewed_candidate → active`、S-013/SP-001 状态收束、公共发布或生产主张。
- 后续 reviewer 必须读取 B04 例外修复后的实际 Agent Log、OPCM、closeout 和最终 diff，不得只复用本文 verdict。
- `Closeout language verdict`：`pass`，中文含义是本文 H1/H2 使用中文，并对英文 status/verdict、判断影响、证据边界和下一步作了中文解释；该语言门通过不改变 B04 仍为 blocker 的结论。
