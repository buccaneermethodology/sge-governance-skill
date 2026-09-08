# S-021 语义架构复核（当前基线）

## 关键结论中文展开

本轮复核的是 S-021 的 clean-room/UAT、ERBE evidence package、独立验证入口与后续实现/收束边界。当前双仓 authority、default-deny、target authority、identity/state 分离仍然成立；S-021 ERBE 也已把 `CR-*`/`NEG-*` 明确降为本地 witness alias，并映射到 S-016 冻结的 `C01–C14`。

但这不等于 S-021 已通过独立 Validation：现有 [S-021 Validation Review](SP003_S021_ValidationReview.md) 仍记录修复前的 identity、13/14 计数和 AC 缺口，不能作为当前修复后输入的独立 verdict。当前最多支持有界的结构/本地行为证据和后续 Validation 入口，不支持 `S-021 complete`、`SP-003 complete`、`published`、`production-ready` 或任何 GitHub mutation 已发生的结论。

## 两个必需 verdict

### Design Freeze Validity（设计冻结有效性）

**Verdict：`partial`（部分有效）**。

冻结的语义框架有效：私有 `sge-governance-skill` → fresh staging → public projection 是唯一维护方向；普通用户的 lifecycle surface 与 maintainer export/release surface 分离；target project 仍拥有自身治理文件；candidate、validated、approved、published、production_ready、git_mutation、license_authorized 保持正交；本地测试或 candidate 不授予远端、权利或生产 authority。

当前证据一致性已有两项实质修复：

- [S-021 ERBE](SP003_S021_ERBE_RED_GREEN.json) 的 `contract_id`/revision 已绑定 S-016 冻结合同；`local_witness_aliases` 将 `CR-*`/`NEG-*` 映射到 `C01–C14`，并把未重放的 frozen cases 明确标为 `not_replayed_in_this_lane`。
- [S-021 UAT](SP003_S021_CleanRoom_UAT.md) 已说明当前 focused command 是 candidate 8 + projection 6 = `14`，历史 `13/13` 只作为旧范围声明保留，不再与当前 14 个 test method 合并成单一结果；AC-01..03 也已有 predicate、expected 和 witness 入口。

仍阻止 `valid` 或更强语义冻结结论的事项：

1. 当前 S-021 独立验证 carrier 虽然已有文件，但内容仍引用修复前的 `CR/NEG` identity 和 13/14 缺口；它必须针对当前 UAT/ERBE 重新读取、重算并更新，而不能仅由 Semantic Review、UAT 或 ERBE 自报替代。
2. ERBE 的 `red_case_ids`/`green_case_ids` 是完整 inventory，而不是全部已重放或已通过的 case。当前 `trusted_red=false`、`green.status=not_claimed_pending_independent_validation` 保护了这一边界，但字段名仍容易被未来 Agent 单行读取后误判为全量 RED/GREEN。
3. ERBE 中 evidence repair lane 的 `post_write_result=blocked_by_base_context_digest_drift` 是历史 provenance，不是当前 Semantic lane card 的失败；但若不把历史 lane binding 与当前 lane binding 分开，未来读者可能把历史重绑定阻断误读为当前 evidence package 的技术失败，或反向忽略重新 Validation 的必要性。

因此，本轮确认了设计边界，但不确认 S-021 的独立验证、最终收束或 Goal completion。

### Implementation Entry Readiness（实现入口准备度）

**Verdict：`conditional`（条件性可进入）**。

当前唯一安全的下一入口是：以本轮 Semantic Review 为新的 source，重新绑定/验证 S-021 Validation lane card，然后由独立 Validation 从当前 durable UAT、ERBE、S-016 cases、实现测试和原始 ODA-MH-01..12 重算 S-021 的局部 predicates。该入口不需要修改双仓 runtime 或扩大 public/release capability。

允许消费的最小切片：当前 local projection/lifecycle witness、显式 `C01–C14` alias mapping、14 个当前 test method 的范围说明、S-019 state/permission matrix，以及它们各自的 claim ceiling。禁止直接进入 GitHub create/push/tag/release、许可证批准、生产就绪或 SP-003 closeout。

实现阶梯为：

```text
当前 S-021 UAT/ERBE evidence package
  -> 重新绑定当前 Semantic Review 的 Validation card
  -> 独立重算相同 C01-C14 identity 与 S021-AC-01..03
  -> 复核原始 ODA-MH-01..12、最终 diff 与 Dashboard/KB 状态
  -> S-022 OPCM/closeout/post-closeout reconciliation
```

`S-022` 在既有 Session DAG 中是下一入口，但在当前独立 Validation Review 针对修复后输入重新形成之前，只能视为有条件入口，不能视为最终证据已就绪。若后续只修复 evidence binding/Validation，不改变合同、authority、acceptance 或 runtime，属于 rebaseline 后的验证工作；若改变 case identity、predicate、expected 或 claim ceiling，则必须走 Contract Patch + Scope Delta + re-RED。

## Read Manifest 与证据边界

### 已读取并消费

- [S-021 Semantic Lane Task Card](SP003_S021_SemanticLaneTaskCard.json) 与 [renderer prompt](SP003_S021_SemanticLanePrompt.txt)：确认 `full_baseline`、原始 ODA-MH-01..12、唯一 write scope、maximum claim 和 rebaseline reference。
- [S-016 Design](SP003_S016_Design.md)、[S-016 ERBE Contract](SP003_S016_ERBE_Contract.json)、[S-016 ERBE Cases](SP003_S016_ERBE_Cases.json)：确认 source authority、predicates、INV-01..08、forbidden collapses、frozen case identity 和 implementation ladder。
- [S-017 ProjectionContract](SP003_S017_ProjectionContract.md)、[ProjectionEvidence](SP003_S017_ProjectionEvidence.json)、[S-017 Validation Review](SP003_S017_ValidationReview.md)：确认 local projection 的 48-file evidence、14-test report、独立 S-017 claim ceiling 和其不吸收 S-021 的边界。
- [S-018 LifecycleContract](SP003_S018_LifecycleContract.md)、[S-018 LifecycleEvidence](SP003_S018_LifecycleEvidence.json)：确认 default-source、backup、install record、rollback、recoverable uninstall 与 target authority 的本地生命周期边界。
- [S-019 ReleaseGovernanceContract](SP003_S019_ReleaseGovernanceContract.md)、[S-019 State/Permission Matrix](SP003_S019_StatePermissionMatrix.json)、[S-020 ContributionPolicy](SP003_S020_ContributionPolicy.md)、[S-020 PR Provenance](SP003_S020_PRProvenanceRecord.json)：确认状态轴、权限、权利、PR 回流和 remote readback 的非替代关系。
- [S-021 Clean-room UAT](SP003_S021_CleanRoom_UAT.md)、[S-021 ERBE RED/GREEN](SP003_S021_ERBE_RED_GREEN.json)：确认当前 alias mapping、case coverage、AC-01..03、14-test scope、`trusted_red=false` 和 pending independent Validation。
- [既有 S-021 Validation Review](SP003_S021_ValidationReview.md)：识别其仍绑定修复前语义，因此仅作为历史/待重跑入口，不能采纳其旧 blocker 作为当前输入的最终判断。
- [SP-003 Goal Contract](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalContract.json)、[Loop Goal](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_LoopGoal.md)、[Stage Plan](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_StagePlan.md)、[S-021 Closeout](SP003_S021_Closeout.md)：确认原始 ODA-MH-01..12、Session DAG、completion rule、continuation 字段和禁止完成措辞。
- [AGENTS.md](../../../AGENTS.md)、[双仓 KB 策略](../../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)、[Semantic Surface Engineering](../../../kb/data/strategy/strategy_semantic_surface_engineering.json)、[SGC v1](../../../kb/docs/strategy/Strategy_SGC_Structural_Contract_V1.md)：确认 truth split、诊断词汇、SGC claim/evidence 边界与语义复核协议。

### 未读取或不能采纳

未读取或操作 GitHub、remote readback、credentials、外部授权系统；这些不属于本 lane 的本地 authority。当前 Validation Review 的旧版内容不能证明修复后输入已独立重算；本 lane 也不把其旧 verdict 继承为当前 verdict。

## Frame-First Review（先审语义框架）

### Authority、层次与核心对象

语义 law 位于 KB、Goal Contract、S-016 Contract/Cases 和各 Session contract；case witness 位于 UAT/fixture/test 输出；evaluation result 位于独立 Validation Review；具体 release、license 或 Git mutation 决策必须由相应 human authorization record 承载。Dashboard 记录执行状态和证据，不覆盖 KB truth；Semantic Review 只解释和约束这些层，不升级任何一层的 authority。

核心对象按以下 family 分离：source/authority、projection boundary、end-user lifecycle、release/permission、contribution return、validation/closeout。它们之间不能跨 family 转移含义：projection candidate 不能转成 published；lifecycle replay 不能转成 license-authorized；permission contract 不能转成已获授权；UAT/ERBE 不能转成独立 Validation；closeout prose 不能转成 Dashboard canonical state。

### 必须保持的不变量

1. `private canonical → fresh staging → public projection` 的方向唯一，public PR 只能作为输入。
2. exact allowlist/default-deny、私有 residue、未知文件、路径逃逸和不安全对象必须 fail closed。
3. source、manifest、tool、run、candidate、projection、tag identity 各自证明自己的对象。
4. candidate、validated、approved、published、production_ready、git_mutation、license_authorized 正交存在。
5. deterministic diff、UAT、independent Validation、人类授权和 remote readback 各自有独立证明责任。
6. RED/GREEN 必须复用同一 frozen `case_id`；环境、fixture、import、path 错误只能为 `error`。

## Semantic Architecture Review（语义架构复核）

### Truth carrier audit

| Truth 类型 | 正确载体 | 当前判断 |
| --- | --- | --- |
| Semantic law | KB、Goal Contract、S-016 Contract/Cases、S-017/S-018 contracts | 双仓方向、deny 面、target authority、state/identity 分离清楚；不要由 UAT 结果反向改写 law。 |
| Frozen case identity 与 expected | S-016 `C01–C14` | 当前 S-021 已正确使用 `C01–C14` 作为 identity，并将 `CR/NEG` 限定为 alias；S-021 尚未重放全部 frozen cases。 |
| Local witness | S-021 UAT、tests、ERBE aliases/coverage | 可支持有界本地观察；`red_case_ids`/`green_case_ids` 仍需按 status 解读，不能单独当作 pass。 |
| Evaluation result | 独立 S-021 Validation Review | 当前文件存在但内容落后于修复后的 UAT/ERBE，需重跑；producer JSON 不构成独立 verdict。 |
| Governance decision | S-019 matrix、具体 repo-owner authorization、remote readback | matrix 只冻结能力和禁止折叠；当前没有具体 repo/tree/payload 授权或 remote readback。 |

### Object responsibility、God Object 与复杂度轨迹

S-016 Contract/Cases 已承担 law、predicate、invariant 和 frozen identity；S-021 UAT 负责 readable local witness；ERBE result 负责将 alias、case coverage、execution 状态和 claim ceiling 组合成 evidence package；独立 Validation 应单独承担 evaluation result。当前不应继续向 ERBE 添加 approval、release、production 或 Dashboard terminal 字段，否则会把 law、witness、evaluation 和 governance decision 合并为 God Object。

尤其要把 `same_case_ids` 理解为 inventory/命名映射断言，而不是 RED/GREEN validity；把 `trusted_red`、`green.status` 和 `recomputed_by` 理解为证据状态字段，而不是独立 reviewer 身份。若未来需要更复杂的 transition、revocation 或 permission semantics，应拆为版本化 contract/matrix/case/evaluation artifacts，而不是继续堆字段。

### Half-schema / DSL 边界与 law quality

当前 JSON 字段已经足以表达固定 case identity、alias、coverage、AC predicate、expected 和本地 claim ceiling，但还不是可自行演进的状态机 DSL。任何新增 case namespace、revision、transition、revocation、test-scope 或 reviewer identity，都需要明确 schema/version、引用完整性、owner、expected semantics 和 re-RED/re-Validation 规则。字段存在不等于语义已经验证。

S-016 predicates/invariants 是可审查的规则；S-021 的局部 AC predicates 已可定位，但未重放的 C04、C07、C08、C11–C14 不能被 inventory 覆盖。当前最需要的是 case-level independent Validation，而非更多状态标签。

### Negative space 与 promotion boundary

必须继续显式排除：dirty private source 被泛化为普通 export 许可、local projection root 被当成 public clone、`pass_with_bounds` 被当成发布、candidate 被当成 approved/published、permission matrix 被当成具体 authorization、PR template 被当成真实 round-trip、历史 Validation 被当成修复后 Validation、以及 S-022 closeout 的本地终态被当成 Dashboard/Goal 已闭合。

稳定的双仓规则已经在 [KB JSON](../../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)；本轮只产生 Dashboard semantic execution evidence，不做 KB promotion，也不改变 runtime/schema/BDD/acceptance/release policy。

## S1-S6 / L0-L6 诊断对齐

这只是有界诊断透镜，不是评分，也不改变产品、runtime、schema、BDD 或 acceptance policy。

| 诊断 | 对齐表面 | 当前观察与处理位置 |
| --- | --- | --- |
| S1 意图错位 | L1 | 把 S-021 local evidence 读成 ODA-MH-01..12 或 Goal terminal；由原始目标矩阵与 claim ceiling 约束。 |
| S2 语义漂移 | L0/L1/L4/L5 | 旧版 ValidationReview 的 CR/NEG、13/14 和 AC 缺口已被新输入修复，但旧 artifact 仍需重跑，不能沿用。 |
| S3 语义过度主张 | L1/L4/L5 | `candidate`、`same_case_ids=true`、`pass_with_bounds`、`evidence_repaired_pending_independent_validation` 不得升级为 validated、approved、published 或 production。 |
| S4 语义歧义 | L2/L3/L5 | `red_case_ids`/`green_case_ids` 的 inventory 语义、历史 card binding 和当前 lane binding 必须分开解释。 |
| S5 语义不可验证 | L3/L5 | 修复后 S-021 尚无一致的独立 Validation verdict；下一 Validation 必须从当前 durable inputs 重算相同 case identity。 |
| S6 权威混淆 | L0/L4/L6 | UAT/ERBE/permission matrix 不能替代 repo-owner、license/right、remote readback 或 Dashboard canonical update。 |

## 原始 ODA-MH-01..12 覆盖检查

本轮没有删除、替换、改名、降级或延期原始 must-have，也没有批准 Scope Delta。以下是本 Semantic lane 的实际覆盖和主张上限，不是把 S-021 局部证据写成 Goal 完成：

| ID | 可观察要求 | 当前结果 | 状态与主张上限 | 后续吸收 |
| --- | --- | --- | --- | --- |
| ODA-MH-01 | private canonical → public projection 单向 | S-016/KB 合同与 UAT/ERBE 边界一致；无 remote round-trip | `partial`：架构/本地 witness，不证明公开仓 | S-020/S-022 |
| ODA-MH-02 | exact allowlist/default-deny 与 residue/path/object fail closed | S-017 evidence、UAT aliases 和当前 tests 报告局部通过 | `bounded local`：不证明逐文件 rights/release | S-017/S-022 |
| ODA-MH-03 | export→diff→Validation→authorized update 可追溯 | export/verify 与独立 S-017 evidence 存在；授权 update/readback 未执行 | `partial`：不证明完整外部 pipeline | S-022 |
| ODA-MH-04 | source/manifest/run/candidate/projection/tag 不互替 | S-019 axes 与 S-021 `C01–C14` identity 分层；projection/tag 仍无远端值 | `bounded`：不证明 tag/release | S-019/S-022 |
| ODA-MH-05 | current public source + target-only install | projection-root default-source path 有本地 UAT | `bounded local`：不证明 GitHub clone | S-018/S-022 |
| ODA-MH-06 | upgrade/backup/record/recovery/uninstall 保留 target authority | lifecycle evidence/UAT 有局部重放 | `bounded lifecycle`：不证明生产/跨平台 | S-018/S-022 |
| ODA-MH-07 | maintainer/end-user surface 分离 | contract、CLI/docs 与 target sentinel 方向一致 | `partial`：无普遍外部用户验证 | S-018/S-022 |
| ODA-MH-08 | public PR 回流 private canonical 后重导出/验证 | S-020 是 template-only，无真实 PR/round-trip | `not landed`：不得把 template 当事实 | S-020/S-022 |
| ODA-MH-09 | CI 无默认 push/tag/release 权限，具体动作需授权 | S-019 matrix 冻结边界；无具体授权/readback | `not landed`：不支持发布或权利主张 | S-019/S-022 |
| ODA-MH-10 | clean-room/UAT/负例由独立 authority 重算 | 当前 UAT/ERBE evidence package 有界且 identity/计数已修复；独立 Validation Review 需重跑 | `partial / validation pending`：不支持 S-021 full pass | S-021/S-022 |
| ODA-MH-11 | state axes 不折叠 | S-019 matrix 明确七轴；本地 candidate 与其它 false/null 分离 | `bounded`：不授予 approval/publication | S-019/S-022 |
| ODA-MH-12 | OPCM、中文 closeout、final Validation、post-closeout reconciliation | S-021 不是最终 closeout；后续 S-022 仍负责 | `not landed`：不支持 SP-003 completion | S-022 |

原始目标结论：`goal_terminal=false`。本 lane 不改变 Dashboard 状态，也不把 S-021 closeout 的下一入口字段改写为 Goal terminal。

## 状态词压缩误读测试

| 状态词 | 可能误读 | 必须理解为 |
| --- | --- | --- |
| `pass` | 全部语义正确或已发布 | 某个指定 gate/case 在指定输入下通过，仍受 evidence layer 限制。 |
| `pass_with_bounds` | 完整 UAT/Validation 通过 | 指定本地环境的有界观察，不含独立验证、release 或 production。 |
| `same_case_ids=true` | RED/GREEN 已可信 | 当前只表示 S-021 inventory 与 S-016 `C01–C14` 对齐；不能代替重放或 reviewer verdict。 |
| `evidence_repaired_pending_independent_validation` | 修复已完成且可关闭 | evidence package 可交给独立 Validation 重算，尚未形成 GREEN 或 Session closeout。 |
| `candidate` | 已批准可发布 | 有边界的 projection 候选，不含 rights、approval、mutation 或 publication。 |
| `validated` | approved/published | 指定 reviewer 对指定输入的验证结果，不授予更高权限。 |
| `conditional` | 后续所有工作都可开始 | 只有本文列出的最小 Validation/rebaseline 入口可进入。 |
| `complete` / `landed` | SP-003/Goal 已完成 | 只有原始 must-have、流程、最终 Validation、closeout、Dashboard/KB 和 reconciliation 全部一致时才可使用。 |

## Future-agent misuse scenarios 与缓解

| 场景 | 可能误读或错误动作 | 缓解 |
| --- | --- | --- |
| 1. 读取 `same_case_ids=true` | 直接接受 RED/GREEN 或写 independent Validation passed | 对照 `case_coverage`、`trusted_red=false` 和 `green.status`；要求独立重算相同 `C01–C14`。 |
| 2. 读取 `red_case_ids`/`green_case_ids` 全量列表 | 把 inventory 当成所有 case 已通过 | 以 status、alias 和实际 witness 分开表示；未重放 case 不得填充结果。 |
| 3. 读取旧版 S-021 Validation Review | 把修复前 blocker 或 verdict 直接套到修复后 evidence | 先验证 source revision/digest 与当前 UAT/ERBE；本轮旧文件只能作为历史待重跑入口。 |
| 4. 看到 `require_clean=false` | 在普通 export 中忽略 dirty source | 仅接受显式 test/clean-room mode；普通维护入口仍按 dirty-tree contract fail closed。 |
| 5. 读取 `pass_with_bounds` 或 local candidate | 把 projection root 当成已发布 public repo | 要求 public remote identity、具体授权和 remote readback；本地 candidate 永不替代 published。 |
| 6. 读取 S-022 closeout 的本地终态 | 忽略 Dashboard/Goal 父面或流程证据冲突而写 Goal complete | 同时复核最终 Dashboard、OPCM、Validation、closeout 和 post-closeout reconciliation；不能只读 prose。 |

## SGC v1 与 truth placement 结论

本 Semantic Review 的最强 claim level 是 `structurally_supported`（结构上有支持）：由当前 card、S-016 frozen contract/cases、S-021 UAT/ERBE 字段和各层 claim ceiling 支持边界判断。S-021 test/UAT 的执行结果属于对应 evidence artifact；本文件没有重新执行测试，也不把读取到的 `14/14` 升级为本 lane 的独立 Validation verdict。

| SI | 结论 |
| --- | --- |
| SI-1 Truth is not structure | 不把 card、schema、digest、alias 或状态字段当作行为真相；law、witness、evaluation、governance decision 分层。 |
| SI-2 Grounding completeness | 当前 alias/case/AC grounding 已明显改善；修复后独立 Validation Review 尚未同步，整体 S-021 grounding 仍未闭合。 |
| SI-3 Decision surface validity | 稳定双仓规则留在 `kb/`；本文件是 Dashboard semantic evidence，不做 truth promotion。 |
| SI-4 Non-tautological validation | 不把 ERBE 的 `recomputed_by`、UAT 或本 JSON 自报当 reviewer 证据；需独立 Validation 从 durable inputs 重算。 |
| SI-5 Authority-execution coupling | local candidate/test pass 不支持 validated、approved、published、production_ready、license_authorized 或 Git mutation。 |
| SI-6 Original objective coverage | ODA-MH-01..12 全部保留；S-021 局部 evidence 不吸收 S-020/S-022 remainder，也不关闭原始 Goal。 |

## 收束、KB/Dashboard 与写入边界

- `goal_terminal=false`；`next_session=S-022`。S-022 是既定 DAG 的下一入口，但当前 S-021 独立 Validation 需先针对修复后 evidence 重跑，因此最终完成证据尚未就绪。
- `human_decision_required=false`：本 lane 没有请求外部、权利或破坏性决定；若修改 frozen case/predicate/expected，仍须按 Contract Patch + Scope Delta + re-RED 取得所需 authority。
- `kb/`：不更新。稳定双仓规则已存在于 [KB JSON](../../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)，本轮没有新的已批准稳定 truth。
- `Dashboard/`：仅写本 card 指定的本文件；已有 [Sessions](../../Sessions.md) 已记录 S-022 为后续入口，不新增重复 Session，也不修改 Session registry、Goal、UAT、ERBE、Validation 或代码。
- 外部动作：未执行 GitHub、网络、remote readback、credentials、commit、stage、push、tag 或 release。
- `CG skipped: no CG input provided`（未提供 CG 输入，因此不产生额外结论）。

允许的收束措辞是：`S-021 的双仓语义边界与当前 evidence package 结构复核为 partial；实现入口为 conditional，仅支持重新绑定后的独立 Validation 和既定 local evidence。当前不支持 S-021 complete、SP-003 complete、published、production-ready、license approval 或 GitHub mutation。`
