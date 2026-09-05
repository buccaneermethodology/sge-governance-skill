# S-016 语义架构复核

## 关键结论中文展开

本报告只复核 `SP-003/S-016` 的 Design/ERBE Contract/Cases 是否形成了可安全交给后续实现的语义边界。它不是实现报告、Validation verdict、candidate verdict、release decision 或 production readiness 证明。

当前结论为：双仓单向真源、公共边界、target authority 保留和 claim ceiling 的总体方向成立；但状态/权限的可执行语义、ERBE 的值域与演进约束、若干 negative case 的唯一 expected 行为仍未闭合。因此不批准把整个双仓生命周期作为一个已冻结、可直接广泛实现的合同。

## 读取范围与门禁证据

- lane card：[SP003 S-016 Semantic Lane Task Card](SP003_S016_SemanticLaneTaskCard.json)。按 renderer 输出的命令执行 `lane_task_card.py validate`，结果为 `verdict=pass`；该结果只证明 card identity、结构和所列引用摘要匹配。
- 主要审查输入：[S-016 Design](SP003_S016_Design.md)、[ERBE Contract](SP003_S016_ERBE_Contract.json)、[ERBE Cases](SP003_S016_ERBE_Cases.json)。
- 目标与稳定策略：[SP-003 Goal Contract](SP003_OpenSourceDistributionArchitecture_GoalContract.json)、[双仓策略 KB JSON](../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)、[Stage Plan](SP003_OpenSourceDistributionArchitecture_StagePlan.md)。
- 条件性接口参照：[现有 public lifecycle tool](../../tools/sge_public.py)、[现有 public export manifest](../../public_export_manifest_v1.json)。它们是实现输入，不是本报告的运行成功证据。
- `semantic` 与 `sgc` checkpoint 输出已读取；本审查采用 `structurally_supported` 的证据上限加审阅判断，不把字段存在、JSON 可解析或 checklist 输出当作行为正确。

## Frame-First Review

### Authority、分层与核心本体

| 审查面 | 当前判断 | 影响 |
| --- | --- | --- |
| Authority | `sge-governance-skill` 被定义为 private canonical source，`bm-sge-governance` 为 public projection，target project 保有自身 authority；`repo-owner` 是人类 oracle，但批准状态明确为未提供。 | 方向清楚；不能把本报告或 Design 的 `ready` 解释为人类批准。 |
| Layer separation | Contract 承载 predicates/invariants，Cases 承载 fixture/expected/observable，`oracle_owner` 与 claim ceiling 承载治理边界，且本 lane 声明未执行 RED/GREEN。 | 初步分层存在，但 Cases 的 `expected`/`forbidden_overread` 同时承担 witness、解释和治理语义，仍有混层。 |
| Core ontology | 已有 `surface`、`actor`、identity axis、state axis、candidate、projection、release、target overlay。 | 缺少一等的 `witness evidence`、`evaluation result`、`authorization record`、`capability`、`transition/event` 本体，后续实现容易用布尔字段替代这些对象。 |
| Claim/evidence | Design 和 Contract 明确区分 design handoff、执行、独立 Validation、批准、远端 mutation、发布和生产主张。 | claim ceiling 是清楚的；但字段本身还不能证明相应 evidence 已存在。 |

### Invariants、failure taxonomy 与跨族迁移

`INV-01` 至 `INV-08` 和 `FC-01` 至 `FC-10` 对单向真源、default-deny、target authority、identity/state 非替代、独立验证和 no-mutation 有良好覆盖。14 个 case 也覆盖了若干关键正负形状。

但它们还不是完整的可执行状态模型或跨族迁移规则：

- identity/state 只有名称和文字规则，没有值域、必填/可空条件、版本化、事件顺序、撤销/失效和变更后的重验证规则。
- capability family 没有形式化。当前只有 actor/action 的叙述，没有定义 capability 原子、资源、作用、前置条件、可组合关系、显式 deny 优先级和授权有效期。
- failure fingerprint 已命名，但没有统一的错误分类、输入观察与 predicate 失败的映射；`environment/fixture/import/path error` 的判定边界依赖未来实现者解释。
- public projection、lifecycle、PR 回流、GitHub authorization 和 production evidence 被放在同一大合同的相邻语义中，尚未定义哪些规则可以跨 family 复用、哪些必须由子合同单独证明。

### Negative space 与 promotion boundary

现有负例没有覆盖以下高风险空白：manifest 重复/歧义/越界、dirty worktree、source/manifest/tool digest 漂移、缺失或不兼容 license、gitlink/LFS/nested repo/unexpected binary、安装记录篡改、备份失败后的部分写入、授权过期或撤销、授权 payload 与实际 tree/tag 不匹配、验证后到 mutation 间的 TOCTOU、remote readback 不一致，以及状态回退/撤销。

策略 KB 的 `candidate_not_approved` 和 Design 的“future promotion candidate”保留了候选边界，但没有单独的 promotion decision schema、批准对象、版本/生效时间、撤销规则和“从 Dashboard evidence 进入 KB JSON”的明确证据门。故本报告只把当前审查 artifact 视为 Dashboard 执行证据；不进行 KB promotion。

## Semantic Architecture Review

### Truth carrier audit：law、witness、evaluation、governance

| Truth carrier | 当前承载 | 审查结论 |
| --- | --- | --- |
| Semantic law | Contract 的 predicates、invariants、forbidden collapses | 方向正确，但状态转移、capability algebra 和可执行 pre/postcondition 不足。 |
| Witness evidence | Cases 的 durable_inputs、fixture、expected、observable、failure fingerprint | 作为 witness 目录是合理的；但 `expected` 不是实际结果，不能与 Validation result 混用。 |
| Evaluation result | Contract/Cases 明确写 `not_executed`，本 lane 未产生 RED/GREEN | 这点边界正确；后续必须使用独立 Validation artifact，而不是回填本文件。 |
| Governance decision | `repo-owner`、approval status、human authorization、claim ceiling | 当前只有责任归属和边界声明，缺少绑定具体 artifact/payload、时间、权限、撤销和 readback 的独立 authorization record。 |

主要语义风险是把同一 JSON 逐渐扩展成“法律、案例、实际结果、批准记录和发布状态”的总载体。应保留 Contract law、Case witness、Validation result、Human authorization 四类独立 carrier，并只通过稳定 identity 引用连接。

### God Object、semantic bureaucracy 与复杂度轨迹

当前设计不是立即不可用的 God Object：implementation ladder 已将 S-017 至 S-022 拆成有界切片，且 claim ceiling 较保守。但 Contract 同时定义 export、安装、target overlay、贡献回流、license、GitHub 权限、release 和 production 状态；每次扩展若继续向同一文件增加 actor、axis、case、例外和禁止折叠，就会变成难以验证的治理总表。

另一个风险是 semantic bureaucracy：多个表面重复书写 `covered-in-design-freeze`、`design-input-ready`、forbidden overread 和 claim ceiling，却没有统一的 status/value vocabulary 或机器引用关系。缓解方向不是继续添加 metadata，而是拆分 projection、lifecycle、contribution、authorization 子合同，并让主合同只保留跨子合同的不变量和 identity linkage。

### Half-schema / DSL 边界

`erbe_contract_v1` 与 `erbe_cases_v1` 有稳定的 `schema_version` 字段和结构，但当前输入没有为这些类型提供对应的 JSON Schema、枚举/值域、引用完整性、版本演进和迁移规则。因此它们目前是“schema-shaped contract”，不是可以由实现者安全解析的完整 DSL。

具体不一致包括：Contract 将 state axes 作为概念集合，C08 使用布尔值，而 C13 使用 `git_mutation: "authorized_only"`；C08 允许 `false or unknown`，C10 允许“终止或跳过”两种结果，均不是唯一的可判定输出。C13 的 `human_authorization` 虽绑定 repo/tree/tag/payload，却没有授权主体、作用、有效期、撤销或 mutation/readback 结果字段。

### Law quality 与 case adequacy

- `P-SOT-01`、`P-BOUNDARY-01`、`P-SURFACE-01` 的方向和 observable witness 可审阅，但需要明确输入规范化、完整树扫描和实际写入观察。
- C01 的 `reverse_edit: false` 更像预置断言，不是一次尝试 public-to-private 写入后的观察；应增加行为事件和拒绝证据。
- C08 的“仍为 false 或 unknown”把两个不同的语义状态合并；应定义 `unknown` 的允许来源以及何时必须拒绝。
- C10 的“终止或跳过受保护面”会让 Builder 选择不同的部分成功语义；应规定 atomic abort、明确 skip 的结果状态及其是否可报告为成功。
- C13 的正例验证的是“有授权形状”，不是已经发生的 mutation；需要把授权接受、实际 mutation 和 remote readback 分为不同阶段。

## Capability algebra 审查

当前合同未冻结 capability algebra。至少应在后续子合同中明确以下不同 capability 原子：读取 private source、读取 manifest、生成 staging、生成 candidate、执行 independent validation、批准指定 payload、执行 push/tag/release、读取 remote、安装到指定 target、修改受控 Skill surface。每个 capability 需要 subject、resource、effect、evidence、有效期和撤销语义；capability 的组合不能自动产生更高权限，显式 deny 必须优先于 token 存在或 CI check 通过。

因此 C12 的 `ci_has_push_token=true` 是很好的风险形状，但当前 Contract 还没有足够的 capability 语义证明“token 存在不等于 capability 被授予”；C13 也没有完整表达“谁在何时对哪个 payload 授权”。这是进入 S-019 release/permission 实现前的 P1 follow-up。

## 状态词压缩误读测试

| 当前词 | 单独出现在 row/title 时的误读风险 | 建议语义 |
| --- | --- | --- |
| `ready` / `ready_after_dependencies` | 可能被读成实现已批准、可发布或 Goal 可关闭。 | `设计边界已审阅；仅允许指定后续切片进入`。 |
| `design-input-ready` | 可能被读成 exporter/installer 已准备完成。 | `可作为后续 Builder 输入；未执行`。 |
| `covered-in-design-freeze` | 可能被读成 must-have 已落地。 | `仅合同覆盖；无运行证据`。 |
| `frozen_for_design_handoff` | 可能被读成 human-approved/finally frozen。 | `设计交接版本；oracle 未批准`。 |
| `candidate`、`validated`、`approved`、`published` | 可能被压缩成一个发布状态。 | 始终显示独立 state axis 及其 evidence/authority。 |

建议未来 row/title 优先使用中文展开词，并把精确英文状态作为字段而非唯一可见标题；本报告不修改这些输入文件。

## Future-agent misuse scenarios 与缓解

| 场景 | 可能的错误动作 | 缓解要求 |
| --- | --- | --- |
| 1. 看到 Goal/Contract 中的 `ready` | 直接启动 S-018 lifecycle，甚至把 S-016 视为 Goal 完成。 | 将 `ready` 改为“仅 S-017 有界入口”；保留原始 ODA-MH-03/05/06/08/09/10/12 未完成状态。 |
| 2. 看到 C13 的 human authorization 对象 | 认为 CI 或工具已获得 push/tag/release capability。 | 增加独立 authorization record、capability/resource/effect/expiry/revocation 和实际 mutation/readback 结果；授权形状不等于 mutation。 |
| 3. 看到 exact allowlist 或 manifest check 通过 | 认为未知源文件、dirty worktree、license/provenance、symlink/gitlink/LFS 等均已安全处理。 | S-017 增加完整源树 inventory、内容/对象类型扫描、license 缺失/不兼容负例和 digest drift gate。 |
| 4. 看到 `validated=true` 或 file digest | 认为语义正确、可公开分发或 production-ready。 | 保持 deterministic diff、独立 Validation、human approval、published readback、production evidence 分轴，并禁止跨轴推导。 |
| 5. 看到 C10 “终止或跳过” | 选择跳过受保护文件后仍报告 install success，导致 target authority 被部分覆盖或误报。 | 冻结 atomic/skip 的唯一结果语义、写入集合、marker 状态和 recovery 证据。 |

## S1-S6 / L0-L6 诊断对齐

这不是评分表，只用于定位修复面：

| 诊断 | 对齐表面 | 修复方向 |
| --- | --- | --- |
| S2 语义漂移：Goal 的 identity 列表与 S-016 新增 `export_tool_revision`、设计中的“三表面”与实际四 surface 不完全对齐 | L0/L1/L2 | 在后续 Contract Patch 中明确 additive refinement 与 surface 命名，避免不同文件各自演进。 |
| S3 语义过度主张：`ready`、`design-input-ready`、`covered-in-design-freeze` 可被压缩为 landed | L1/L4 | 术语压缩、claim ceiling 和 row-level 中文展开。 |
| S5 语义不可验证：state 值域、transition、C10/C13 expected 行为和 capability algebra 未冻结 | L2/L3/L5 | Contract Patch、专用 schema、确定性 gate 与同 case identity 的独立 Validation。 |
| S6 权威混淆：authorization shape、CI token、candidate、approved 和 mutation 尚未由 capability/record/readback 完整连接 | L4/L5/L6 | S-019 permission 子合同、人类 oracle、授权绑定和 remote readback。 |

## 两个必要 verdict

### Design Freeze Validity

**Verdict：`partial`（有界设计方向有效；完整语义冻结需 P1 follow-up）。**

理由：单向 source-of-truth、default-deny、target overlay、identity/state 分轴、独立 Validation 边界和 no-mutation claim ceiling 已形成可审阅的结构性设计输入；但 capability algebra、state transition/value domain、law/witness/governance carrier 分离、negative-space 以及 promotion decision boundary 尚未足以支撑“整个双仓生命周期合同已完成语义冻结”。`repo-owner` approval 仍未提供。

这不是 blocker 对 S-016 文档存在性的否定，而是阻止将当前 `frozen_for_design_handoff` 解释成 human-approved、implementation-validated 或 release-ready。

### Implementation Entry Readiness

**Verdict：`conditional`（只允许 S-017 的最小、无远端 mutation 切片；不允许广泛生命周期/发布实现入口）。**

允许的 S-017 入口仅限 fresh-root、exact file set、对象类型/路径安全、私有 residue 扫描、逐文件 license/provenance 记录、tree/bytes/digest projection evidence；输出只能是 candidate/projection 设计或实现证据，不得写 published、release 或 production。

在以下 P1 follow-up 完成 Contract Patch/专用子合同前，不允许把 S-018 至 S-021 作为已准备好的广泛实现入口：

1. 冻结 ERBE contract/cases 的 schema、值域、引用、唯一 expected 行为和版本演进规则。
2. 分离 Contract law、Case witness、Validation result、Human authorization record，并冻结 capability/resource/effect/expiry/revocation/readback 关系。
3. 补齐 manifest/license/digest/dirty-tree/object-type、install recovery、authorization TOCTOU、readback mismatch 和 state revocation 的 negative space。
4. 解决现有 lifecycle CLI 的接口漂移：当前 `tools/sge_public.py` 的 install/upgrade 命令要求 `--source`，而 S-016 目标规定普通用户默认 current public source、只需 `target`；该差异应在 S-018 合同/实现中显式处理，不能由 Builder 默默改名或缩窄目标。

## Scope、KB 与 Dashboard 边界

- 本报告未修改代码、Goal、KB、Dashboard registry、ERBE Contract/Cases 或远端 GitHub。
- 当前审查结果属于 Dashboard artifact 的执行记忆；没有把新稳定规则写入 KB。既有双仓 KB 仍为 `candidate`/`candidate_not_approved`，本报告不改变其 promotion state。
- P1 follow-up 已按现有 DAG 指向 S-017/S-018/S-019/S-021 的后续工作；本 lane 的 card write scope 只有本文件，因此不新增或修改 `Dashboard/Sessions.md`。
- 本报告没有产生 Validation handoff verdict、RED/GREEN、candidate、public repo、release 或 production 结论。

## 允许的收束结论

S-016 的 Design/ERBE 输入已完成独立语义审查，但结论是有界 `partial/conditional`：可从本设计进入 S-017 的最小 projection 切片；必须先处理列出的 P1 语义合同缺口，才能把后续 lifecycle、permission、contribution、independent Validation 或 release 作为安全实现/验证入口。该结论不关闭 SP-003，也不构成独立 Validation 或发布授权。
