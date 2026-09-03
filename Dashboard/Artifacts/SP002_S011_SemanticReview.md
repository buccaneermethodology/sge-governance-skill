# SP-002/S-011 独立语义边界复核

## 关键结论中文展开

当前 public candidate 不能通过最终语义边界复核。设计文件已经明确公共/私有分层、四层依赖、可选扩展与发布 claim ceiling，但实际候选仍把私有 `Dashboard` artifact 作为公开 glossary 的 source scope/source ref；四层归属没有进入 manifest 的可验证字段；被称为 `profile-driven optional orchestrator` 的脚本没有 profile/hooks 输入；ERBE 合同又以“先实现、后冻结并记录例外”的状态出现，而 task card 没有提供 Cases、可信 RED/GREEN、例外批准或 re-RED 证据。

这意味着：本 review 只支持“发现并界定当前候选的语义 blocker”，不支持 public candidate pass、发布授权、Git/push、生产就绪或任意仓库适用。

## Review 身份与边界

- Reviewer：独立 SP-002 Semantic Reviewer。
- Task card：[SP002_S011_SemanticLaneTaskCard.json](SP002_S011_SemanticLaneTaskCard.json)。card digest 校验通过，`card_id=sp002-s011-semantic-v1`。
- 模式：`full_baseline`；仅消费 card 指定的原始 artifacts。
- 写范围：仅本文件；未修改候选实现、Goal、ERBE、KB、manifest、extension registry 或工具代码。
- Maximum claim：只给出当前 public candidate 的独立语义边界复核；不批准发布、Git、生产或普遍适用。

## Read Manifest 与证据完整性

### 已读且摘要与 card 匹配

- [AGENTS.md](../../AGENTS.md)
- [SP-002 Loop Goal](SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md)
- [S-007 Design](SP002_S007_Design.md)
- [SP-002 ERBE Contract](SP002_ERBE_Contract.json)
- [public export manifest](../../public_export_manifest_v1.json)
- [glossary canonical candidate](../../kb/data/glossary_v1.json)
- [glossary Markdown projection](../../kb/docs/Glossary.md)
- [optional extension registry](../../extensions/registry_v1.json)
- [Loop Goal continuation helper](../../tools/run_sge_loop_goal_cycle.py)
- Repo-local `sge-governed-checkpoints` skill 与 Semantic Reviewer Protocol v2 checklist。

### 已执行

- `lane_task_card.py validate ... --expected-card-sha256 ...`：通过；只证明 card identity、结构与所列 source digest 当前匹配。
- `python3 tools/sge_public.py doctor`：`public_doctor:pass`。
- `python3 kb/tools/render_kb.py --check`：通过 6 个 manifest documents。
- 上述两个绿色结果只证明当前 doctor/render 所编码的结构条件，不证明 public/private 语义隔离、四层依赖、独立 UAT、ERBE 时序、final diff 或发布 readiness。

### 未由 card 提供，因而不能推定已满足

- SP-002 ERBE Cases、同 identity 的可信 RED/GREEN、failure fingerprints 与独立重算记录；
- S-007 至 S-011 的完整 closeout、最终 Original Plan Coverage Matrix、final Scope Delta audit；
- Validation Handoff、独立 final Validation/post-closeout reconciliation、closeout-language verdict；
- 独立 UAT、clean-room negative-case evidence、最终 public staging inventory 与完整 tracked/untracked final diff；
- `frozen_after_initial_implementation_with_sequence_exception_recorded` 所称 sequence exception 的人类批准 reference、Contract Patch 与 re-RED。

依据仓库硬门，以上 final-review 必需证据缺失时不得给 `PASS`。

## 双 verdict

| Verdict | 结论 | 中文含义 |
| --- | --- | --- |
| Design Freeze Validity | `FAIL` | 设计文本的目标边界总体清楚，但当前冻结包存在 public/private authority 污染、ERBE 冻结时序不可验证、四层合同未机器化以及当前状态面互相冲突，不能作为有效的最终 design freeze。 |
| Implementation Entry Readiness | `FAIL` | Builder 不能把现有 candidate 当作已就绪基线继续扩大实现；只能进入下面定义的 blocker-repair 最小切片，完成后重新独立验证和语义复核。 |
| Overall Verdict | `BLOCKED` | 当前不能声明完成；缺失证据与语义 blocker 见下。可选收束状态只能是 `blocked/partial`，不能是 `pass/done`。 |

## Blocking findings

### B1 — 公开 glossary 以私有 Dashboard execution memory 作为 provenance（S6 authority confusion，L0/L2）

Goal 明确要求 `Dashboard/` 的 Goal、Stage Plan、Session 和 closeout 留在私有执行面，并要求 public glossary 的 `source_refs` 只指向公开或明确可审计的 SGE source；见 [Loop Goal 的公共/私有边界](SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md#public--private-execution-surface-contract) 与 [Glossary 验收](SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md#glossary-验收)。设计也明确排除历史 Session/Goal，见 [S-007 Design](SP002_S007_Design.md#glossary-v1-合同)。

但 canonical candidate 的 `metadata.source_scope` 直接包含 `Dashboard/Artifacts/SP002_S007_Design.md`，`Candidate`、`Session`、`Stage Plan`、`Future-agent Misuse Scenario` 等条目也引用 SP-002 Dashboard artifacts；相同 locator 被渲染到公开 [Glossary.md](../../kb/docs/Glossary.md#source-scope)。与此同时，manifest 又把 JSON 与 Markdown 都列为 public 文件，见 [public export manifest](../../public_export_manifest_v1.json)。

这不是“Dashboard 文件没有被复制”即可消除的问题：公开 canonical artifact 已依赖并暴露私有 execution-memory locator，未来 agent 会把 Dashboard witness 当作 glossary law 的 authority。必须将 source scope/source refs 改为公开稳定 KB/Skill source，或使用经过裁决、不暴露私有执行身份的逻辑 provenance/tombstone，再重渲染并做 private-locator negative test。

### B2 — ERBE 的 specification-first 时序没有可验证证据（S5 unverifiability，L5）

[ERBE Contract](SP002_ERBE_Contract.json) 的状态是 `frozen_after_initial_implementation_with_sequence_exception_recorded`。这表明冻结发生在 initial implementation 之后，和 specification-first 的 dominant Builder 前冻结要求存在直接时序张力。Task card 只提供 Contract，没有提供 Cases、可信 RED、同 identity GREEN、独立重算、sequence exception 批准 reference、Contract Patch 或 re-RED。

因此不能把 `frozen` 压缩读成“有效且可追溯的 design freeze”。需要补齐明确的人类批准/Scope Delta reference，并按 frozen case identity 重建可验证 RED/GREEN；否则 B2 持续阻断 Design Freeze Validity。

### B3 — 四层模型只存在于 prose，manifest 无法核对层归属、依赖与 optionality（S4 ambiguity，L2/L5）

[S-007 Design](SP002_S007_Design.md#公共四层与依赖) 要求 core、companion、orchestrator、domain extension 四层中的每个文件在 manifest 中逐文件列出，并明确安装顺序和 optional contract。当前 manifest 的 file records 只有 path/source/license/provenance/public/execution_context，没有 `layer`、`requires`、`optional`、installation order 或 compatibility contract。

因此“所有文件已 allowlist”不能推出“SP002-MH-03 四层依赖可核对”。需要为 manifest 增加可验证的 layer/dependency/optionality 表达及 negative cases，或提供与 manifest 同 authority、由 doctor 强制验证的独立四层合同；在此之前不得声明四层依赖已独立验证。

### B4 — optional extension registry 仍是标签式接口，不足以支撑显式 interface/provenance（S4 ambiguity，L2/L3）

[extension registry](../../extensions/registry_v1.json) 正确声明 `core_requires_extensions=false` 且两个 extension 默认关闭，这是边界正证据；但每个 extension 只有 id/kind/enabled_by_default/自由文本 interface/claim_ceiling，没有 schema/version、entrypoint、compatibility、provenance ref、安装/缺失行为或 validator identity。

因此它只能证明“候选配置声称可选”，不能证明未安装时 core 不依赖 extension，也不能证明安装时存在 Goal 要求的显式接口与 provenance。必须把这些最小合同变成可验证字段并以 core-without-extension、unknown-extension、invalid-interface/provenance negative cases 重算。

### B5 — `profile-driven optional orchestrator` 名称超过实际入口能力（S3 overclaim，L2/L3）

设计和 Goal 的 SP002-MH-06 要求 profile/hooks 驱动；manifest 也把工具命名为 `profile-driven optional orchestrator`。但 [run_sge_loop_goal_cycle.py](../../tools/run_sge_loop_goal_cycle.py) 只接受一个 state JSON，检查四个顶层键并返回 continuation decision；没有 profile、hooks、extension registry 或 project-neutral routing 接口。

此外，输入只要自报 `goal_terminal=true`，脚本就输出 `decision=complete`；该输出没有绑定 Goal completion evidence 或 authority ref。它可以作为“对已获权威验证状态的纯决策 helper”，不能作为 Goal completion verifier。修复方向二选一：实现并验证设计所称 profile/hooks 合同；或将名称、manifest provenance、文档与输出语义收窄为 `validated-state continuation decision helper`，并明确 `complete` 只是消费上游权威状态后的 routing result。

### B6 — “S-011 final review”与 Goal 当前状态、must-have 状态及 final evidence 不一致（S2 drift / S3 overclaim，L3/L5）

Task card 把本 lane 定义为 `SP-002 final semantic boundary review`，但 [Loop Goal](SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md#文档身份) 仍写 `To do`、当前入口 `S-007`、仍需明确启动授权；其 SP002-MH-01..12 也全部是 `pending`。Goal completion rule 又要求逐项 OPCM、独立 UAT/Validation、中文 closeout、post-closeout reconciliation、最终 diff 和未裁决文件归零，但这些均未进入本 card 的 Read Set。

设计期 Scope Delta 段落不能替代 final Scope Delta audit，doctor/render 也不能替代 final Validation。必须先对齐权威执行状态，并向独立 reviewer 提供完整 final evidence package；否则 `final`、`complete`、`ready` 均不可使用。

## Non-blocking observations

- `candidate_not_approved`、manifest claim ceiling、Design 非目标和 Goal 的 release/production/universal applicability 禁止用语保持一致；这些措辞有效降低把候选误读为已发布的风险。
- glossary 条目普遍具有 definition/scope/authority/boundary/claim ceiling/forbidden overreads/related concepts/source refs，JSON 与 Markdown 当前确定性一致。该正证据不抵消 B1 的 source-authority 污染，也不证明 ontology 已获最终 promotion。
- Design 给出了从 manifest/glossary 到 docs/lifecycle、optional orchestrator、clean-room/UAT 的高层 implementation ladder；但当前 final-stage repair 缺少绑定 blocker、输入、输出和复核顺序的 next-session/repair map，因此不能提升 Implementation Entry Readiness。

## Authority、ontology、四层、optional extension 与 claim ceiling 复核

| 面 | 观察 | 判定 |
| --- | --- | --- |
| Public/private authority | 文件级 allowlist 排除了 Dashboard 文件，但公开 glossary 的 provenance/source refs 仍指向私有 Dashboard artifacts。 | `BLOCKING` |
| Glossary ontology | 核心术语族和 boundary 字段较完整；但 candidate ontology 已放入 public canonical path，同时依赖私有 design witness，law/witness/promotion 边界未闭合。 | `BLOCKING` |
| Four-layer dependency | prose 有四层和安装顺序；manifest 无机器可核对的 layer/dependency/optional 字段。 | `BLOCKING` |
| Optional extension | 默认关闭与 core 不依赖的意图明确；接口、provenance、entrypoint、compatibility 仍不可验证。 | `BLOCKING` |
| Claim ceiling | candidate/release/Git/production/universal applicability 基本分轴；doctor/render 结论保持在结构证据层。 | `SUPPORTED WITHIN BOUNDED WORDING`，不解除其他 blocker |

## 状态词压缩误读测试

| 压缩表面 | 未来 agent 只看到这一行时的可能误读 | 风险与要求 |
| --- | --- | --- |
| Goal：`To do` / 当前入口 `S-007` | 认为 SP-002 未启动并从 S-007 重跑，或否认当前 S-011 lane 的 provenance。 | 高风险；把动态执行状态放回 Dashboard authoritative row，Goal 只保留 `initial entry`，并在 final card 引用当前状态证据。 |
| ERBE：`frozen_after_initial_implementation_with_sequence_exception_recorded` | 把“有一个未定位例外”读成已满足 specification-first freeze。 | 高风险；必须链接批准、Scope Delta、Contract Patch/re-RED；否则使用 `sequence_exception_unverified`。 |
| Manifest：`candidate_not_approved` | 识别为尚未发布的候选。 | 低风险；保持，不得压缩为 `active`、`ready` 或 `released`。 |
| Glossary：`Status: candidate` 且位于 `kb/data/` | 把候选 ontology 当成已 promotion 的 canonical truth。 | 高风险；增加明确 promotion state/decision ref，或在批准前置于 candidate staging authority。 |
| Manifest：`profile-driven optional orchestrator` | 认为 profile/hooks 和 optional extension routing 已实现。 | 高风险；实现相应合同或收窄为 continuation decision helper。 |
| Tool output：`decision=complete` | 把上游自报布尔值转译为 Goal completion verdict。 | 高风险；改为带 authority/validation 前提的 routing 术语，明确不是 completion evidence。 |

## Future-agent misuse scenarios

1. **私有 provenance 扩散**：未来 agent 从公开 glossary 的 `Dashboard/Artifacts/SP002_*` source ref 追读、复制或打包私有 Goal/Design。缓解：只允许 public authority refs；为 Dashboard-origin stable subset 使用去身份逻辑 provenance 和 promotion decision。
2. **候选被误当 canonical release truth**：未来 agent 看到 `kb/data/glossary_v1.json` 与 `Status: candidate`，仍因路径是 KB 而直接当成已批准 ontology。缓解：candidate staging 与 canonical promotion 分离，记录 promotion state、owner 和 decision ref。
3. **四层依赖被文本标签替代**：未来 Builder 根据 provenance 字符串自行猜测 layer，把 companion/orchestrator/extension 依赖偷偷并入 core。缓解：manifest/独立 contract 增加 layer、requires、optional、install order，并由 doctor 与 negative fixtures 强制验证。
4. **可选扩展被当成已接通能力**：未来 agent 看到 registry entry 就声明 KYM/TCO 支持已落地或领域正确。缓解：registry 明确 entrypoint/schema/version/provenance 与 `candidate-only` ceiling；缺 adapter/evidence 时只允许 `registered proposal`。
5. **自报终态变成完成 verdict**：未来 agent 构造 `goal_terminal=true`，工具返回 `complete`，随后绕过 OPCM、Validation 和 closeout。缓解：将工具定位为消费已验证状态的纯 routing helper；要求 authority ref/validation verdict，或把输出改为 `reported_terminal` 而非完成结论。
6. **S-011 与 `To do/S-007` 状态分叉**：未来 agent 可能重复执行、覆盖候选或使用错误 baseline。缓解：final task card 必须引用当前 Dashboard execution state；Goal 不承载易漂移的“当前入口”。

## 允许的最小修复切片

Builder 下一步只可进入 `SP-002/S-011 semantic-blocker repair`，不得扩大为发布、远端、生产或跨仓库通用化：

1. 清除 public glossary 中所有私有 Dashboard source refs，以 public KB/Skill authority 或已裁决逻辑 provenance 替换，并重渲染。
2. 为四层 manifest/contract 增加可验证 layer/dependency/optional/install-order 表达；补 unknown layer、dependency collapse 与 missing optional layer negative cases。
3. 将 extension registry 最小化扩展为可验证的 schema/version/entrypoint/compatibility/provenance contract，并验证 core-without-extension。
4. 对 orchestrator 做一次明确选择：实现 profile/hooks；或收窄名称、文档、manifest 与 `complete` 输出语义，禁止把纯 state decision helper 描述为已实现的 profile-driven orchestration。
5. 补齐 ERBE Cases、可信 RED/GREEN、sequence exception 批准与 re-RED 证据；对齐 Goal/Dashboard 当前状态。
6. 产出 final OPCM、Scope Delta audit、Validation Handoff、独立 final Validation、中文 closeout、closeout-language 与 post-closeout reconciliation；随后重新派发 digest-bound Semantic lane。

### 修复切片输入、输出与验收

- 输入：本 review、frozen Goal/Contract/Cases、当前 public candidate、当前 Dashboard authority state。
- 输出：修复后的 manifest/glossary/registry/orchestrator contract 与实现、negative fixtures、最终治理证据包。
- 验收：私有 locator 扫描为零；四层与 optional dependency 可重算；orchestrator 名称和实际接口一致；同 identity ERBE GREEN 由独立 Validation 重算；final review 覆盖实际 closeout、Dashboard/KB 和完整 diff。
- 明确非目标：public release、Git push/tag、全局安装、production readiness、任意 repo 适用、KYM/TCO 领域正确性。

## 必须保持的 claim ceiling

修复前最多允许声明：

> 当前 public candidate 的 doctor 与 KB render check 在现有编码条件下通过；独立 Semantic Review 发现 blocking authority、contract、ontology 与 evidence gaps，候选仍为 `blocked/partial` 且 `candidate_not_approved`。

不得声明：

- `SP-002 complete`、public candidate pass、release ready/authorized；
- public/private execution-surface 已完全隔离；
- core/companion/orchestrator/domain extension 四层依赖已验证；
- profile/hooks orchestrator 已实现；
- optional KYM/TCO integration、领域正确性或生产适用；
- Git、push、tag、公开发布、生产就绪或任意仓库适用。

## 最终结论

当前不能声明完成；缺失证据为 ERBE Cases 与可信 RED/GREEN、sequence exception 批准与 re-RED、final OPCM、final Scope Delta audit、Validation Handoff、独立 final Validation/post-closeout reconciliation、closeout-language、独立 UAT、final staging inventory 和完整 final diff；同时存在 B1–B6 语义 blocker。可选收束状态只能是 `blocked/partial`，不能是 `pass/done`。
