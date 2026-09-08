# SP-001 Strategy 来源逐文件迁移清单

## 边界与裁决口径

- 来源：semx-cli `main@19e967a782e2e95d24475770bc234d86ad7c583e` 的 `semx-kb/docs/strategy/`。
- 覆盖：56/56 个文件表面；20 个非 Runtime、22 个非 SAG Runtime、14 个 SAG Runtime。
- authority：本清单是 Dashboard execution memory 与 S-002 设计输入。Markdown 是阅读面；稳定 truth 迁移必须在 S-002 追溯 `semx-kb/data/strategy/*.json` 或明确记录“无 canonical source”，再重新冻结。
- `migrate_after_refreeze` 不等于原样复制；`adapt_extract` 只允许抽取通用不变量；`reference_only` 不进入新 KB truth；`remove` 从目标仓库排除并记录替代机制。
- 本轮不复制任何策略正文、schema、runner 或 runtime，不启动 SP-001。

## A. 非 Runtime 表面（20/20）

| # | 文件 | 裁决 | 可复用内容 | 必须过滤内容 | 计划落点 |
| ---: | --- | --- | --- | --- | --- |
| 1 | `.DS_Store` | `remove` | 无 | Finder 二进制元数据 | S-004 删除并加入 `.gitignore` |
| 2 | `20 practices.png` | `adapt_extract` | 治理实践全景与新手认知结构 | Semx 品牌、P1-P20、实现先行暗示 | SP-002 可选重绘；SP-001 不复制图片 |
| 3 | `Glossary.md` | `adapt_extract` | truth split、claim ceiling、Scope Delta、lane/Validation/OPCM 等通用词 | M1/P05/P06、SAG、Runtime、KYM/TCO、历史 Session | S-002 冻结词汇 ownership；S-004 生成 SGE glossary |
| 4 | `Semx_测试策略_中文翻译版.md` | `remove` | 中文解释风格由新 read model 吸收 | 陈旧 P01-P05 命令与双真源 | S-004 删除；新中文面从 canonical truth 生成 |
| 5 | `Strategy_Acceptance_Postures.md` | `adapt_extract` | acceptance registry、blocking/advisory、evidence/profile/成熟度分轴 | P00-P17、Semx gates、provider/runtime 状态 | S-002 profile contract；S-003 registry/tests |
| 6 | `Strategy_BDD_Validation.md` | `adapt_extract` | BDD companion、shared validator authority、no-omission、反伪可读性 | Semx gate catalog、P02/P05 case IDs | S-003 BDD contract/tests；S-005 负例 |
| 7 | `Strategy_Convergence.md` | `adapt_extract` | bounded retry、fixed point、stall/oscillation/human handoff | M1/Mc/Flow/DRP 顺序、未经校准阈值 | S-002 profile policy；S-003 loop/repair gate |
| 8 | `Strategy_ERBE_Specification_First_Acceptance_V1.md` | `migrate_after_refreeze` | ERBE applicability、RED/GREEN identity、Builder exclusion、projection boundary | Semx owner/path | S-002 重冻结 canonical JSON/schema；S-003 gates |
| 9 | `Strategy_Goal_Effect_Integrity_V1.md` | `adapt_extract` | primary effect 与流程/状态分离、正交 evidence axes、final reconciliation | SP-063、S-472..476、M1/P06/runtime 历史 | S-002 与 SGC/ERBE 去重；S-003 effect gate |
| 10 | `Strategy_Human_AI_Development.md` | `adapt_extract` | intake、context、Goal/Scope Delta、Validation、closeout、多 Agent、human checkpoint | P00-P17、M1、provider、Semx 路径和巨型重复正文 | S-002 分拆 KB/core/profile；S-003 checkpoints |
| 11 | `Strategy_KB_Promotion_and_Graph_Source_Policy.md` | `adapt_extract` | KB/Dashboard split、promotion ladder、Contract Delta、JSON→read model | Semx KG-L1、历史 Session、P06-P17 | S-002 truth carrier contract；S-004 KB/DKG 适配 |
| 12 | `Strategy_M1_Extraction_Target_B.md` | `remove` | honesty-first 等原则由 SGC/Acceptance 吸收 | M1/P00-P05 产品 extractor | S-004 排除 |
| 13 | `Strategy_M1_Extraction.md` | `remove` | calibration/lineage/anti-overclaim 已有更高 authority 来源 | KYM/TCO、M1/Mc/Flow/DRP、P00-P06 产品链 | S-004 排除 |
| 14 | `Strategy_P05_Four_Bucket_Minimal_Index.md` | `remove` | structure-not-truth 由 SGC 吸收 | P05/P06 sidecar 产品合同 | S-004 排除 |
| 15 | `Strategy_Repair.md` | `adapt_extract` | Local First、Evidence Bound、revalidation、冲突/停机 | USL/M1 mapping、`semx repair` CLI | S-002 repair contract；S-003/PDI integration |
| 16 | `strategy_runtime_kernel_v1_target_contract.json` | `remove` | Goal ledger/target freeze 边界由 Goal Conformance 吸收 | SP-038、G1-G10、Runtime Kernel 产品 roadmap | S-004 排除 |
| 17 | `Strategy_Semantic_Surface_Engineering.md` | `adapt_extract` | S1-S6、L0-L6、truth promotion、claim/non-promise | S-176..191、P16/P17 runtime 和 universal wording | S-002 semantic taxonomy；S-003 reviewer reference |
| 18 | `Strategy_SGC_Structural_Contract_V1.md` | `migrate_after_refreeze` | SGC claim/evidence、forbidden collapses、SI-1..SI-6、completion | Semx owner/path、P06/M1 示例 | S-002 canonical contract；S-003 core gate/tests |
| 19 | `Strategy_SGC_to_P06_Contract_Evolution.md` | `adapt_extract` | observation→human-reviewed delta→accepted implementation | P06 disposition、M1/Runtime/KYM/TCO | S-002 Contract Evolution；S-003 Contract Delta Scan |
| 20 | `Strategy_USL.md` | `reference_only` | structure/semantic 双轴、issue/repair hint | UCS、M1/Mc/Flow/DRP、KYM/TCO lint 产品 | SP-002 evaluator extension 参考 |

## B. 非 SAG Runtime 表面（22/22）

| # | 文件 | 裁决 | 可复用内容 | 必须过滤内容 | 计划落点 |
| ---: | --- | --- | --- | --- | --- |
| 21 | `Strategy_Runtime_Authority_Boundary_V1.md` | `adapt_extract` | trace/read-model/BDD 不等于 truth；canonical write 独立授权 | Stage 2、P06/M1、SAG controller | S-002 authority contract；S-003 gate |
| 22 | `Strategy_Runtime_Budget_Retry_Context_Minimum_V1.md` | `adapt_extract` | budget/retry ceiling、stop condition、context fail-closed | G9/G10、Runtime runner/schema | S-002 可选 orchestration policy；S-003 loop extension |
| 23 | `Strategy_Runtime_Budget_Retry_Persistent_Context_Runtime_V1.md` | `remove` | claim 边界由上一合同吸收 | Runtime 决策行为 | S-004 排除 |
| 24 | `Strategy_Runtime_Controller_Scheduler_Minimum_V1.md` | `reference_only` | deterministic selection、无 eligible 则阻断 | Runtime scheduler/G ledger | SP-002 高级编排参考 |
| 25 | `Strategy_Runtime_Event_Failure_Next_Action_Contract_V1.md` | `adapt_extract` | witness/mutation/system failure 分层、immutable refs | P00-P17 next-action mapping | S-002 governance-event contract；S-003 logs/loop |
| 26 | `Strategy_Runtime_Executor_Adapter_V1.md` | `remove` | adapter claim 边界由 authority contract 吸收 | 单一 Semx gate adapter | S-004 排除 |
| 27 | `Strategy_Runtime_Feedback_Controlled_Runtime_Slice_V1.md` | `remove` | advisory/revalidation 原则由下一行吸收 | 自动 feedback runtime | S-004 排除 |
| 28 | `Strategy_Runtime_Feedback_Loop_Event_Slice_V1.md` | `adapt_extract` | repair candidate/accepted/executed 分轴、revalidation refs | Runtime G6/G8 fixtures | S-002 repair event contract；S-003 delta/PDI handoff |
| 29 | `Strategy_Runtime_First_Guarded_Vertical_Slice_V1.md` | `reference_only` | exactly-one bounded path、correlation refs | G1-G10 runtime artifact chain | S-005 集成验收参考 |
| 30 | `Strategy_Runtime_Invalidation_Model_Runner_V1.md` | `adapt_extract` | affected 仅代表需复核；silence is not approval | SAG diff/invalidation runner | S-002 change-impact contract；S-003 promotion review |
| 31 | `Strategy_Runtime_Invalidation_Rollback_Proposal_V1.md` | `adapt_extract` | proposal/decision/execution/truth owner 分离 | G7/SAG/Runtime rollback | S-002 high-risk change proposal contract |
| 32 | `Strategy_Runtime_Kernel_Execution_Posture_Cross_Cutting.md` | `adapt_extract` | 并行 eligibility、human barrier、readiness≠production | daemon/console/provider/G9-G10 | S-002 orchestration posture；S-003 optional loop profile |
| 33 | `Strategy_Runtime_Kernel_Global_State_Machine_C0_1.md` | `adapt_extract` | coordination state≠truth、reject non-mutation、explicit unblock/terminal | Runtime 状态全集、P00/P06/M1/SAG | S-002 lifecycle invariants；禁止第二状态真源 |
| 34 | `Strategy_Runtime_Kernel_Integration_Audit_V1.md` | `reference_only` | gap 未落地则 blocked；deferral≠landed | G1-G10 ledger/SP-038 | S-005 OPCM/Evidence Matrix 参考 |
| 35 | `Strategy_Runtime_Kernel_Orchestration_Controller_C0_3.md` | `adapt_extract` | route≠execute、fallback 不得缩窄、controller 不写 truth | P00-P17 controller/G ledger | S-002 orchestration boundary；S-003 registry；SP-002 编排 |
| 36 | `Strategy_Runtime_Kernel_V1_Target_Contract.md` | `remove` | Goal 原则由 SGC/Goal Conformance 吸收 | Runtime G1-G10 roadmap | S-004 排除 |
| 37 | `Strategy_Runtime_Orchestration_Stage1.md` | `remove` | witness non-interference 已由 authority contract 吸收 | Semx CLI replay/P06/M1 | S-004 排除 |
| 38 | `Strategy_Runtime_Orchestration_Stage2.md` | `remove` | BDD/read-model/KB promotion 已有通用来源 | Semx CLI/P00-P05/SP-035 | S-004 排除 |
| 39 | `Strategy_Runtime_Route_To_State_Apply_V1.md` | `remove` | mutation preflight 由 registry/authority gate 吸收 | Runtime state apply | S-004 排除 |
| 40 | `Strategy_Runtime_Router_Planner_Dry_Run_V1.md` | `reference_only` | DAG/no-cycle、dry-run≠execution、explain 无 authority | P00-P17 node types/runner | SP-002 `run-sge-loop-goal-cycle` 参考 |
| 41 | `Strategy_Runtime_State_Contract_V1.md` | `reference_only` | declared transition、reject non-mutation、terminal closure | Runtime transition catalog | S-002 与 Dashboard registry 对照，不复制第二状态机 |
| 42 | `Strategy_Runtime_State_Store_Apply_V1.md` | `reference_only` | hash/sequence preflight、duplicate event 防重 | Runtime store runner/schema | 未来 Dashboard integrity follow-on 参考 |

## C. SAG Runtime 表面（14/14）

| # | 文件 | 裁决 | 可复用内容 | 必须过滤内容 | 计划落点 |
| ---: | --- | --- | --- | --- | --- |
| 43 | `Strategy_Runtime_Kernel_SAG_Artifact_Graph_C0_2.md` | `adapt_extract` | observation/truth/action 分层；affected≠invalidated；repair≠accepted | SAG ontology、G5/G7/G8、P00-P17 | S-002 evidence/authority contract；S-003 负例 |
| 44 | `Strategy_Runtime_SAG_Conflict_Governance_Policy_V1.md` | `adapt_extract` | policy/case/promotion/action 分权、disputed 默认、COI/reopen | SAG/RCP/P06/M1 case vocabulary | S-002 conflict contract；S-003 decision schema；S-005 负例 |
| 45 | `Strategy_Runtime_SAG_Human_Decision_Precondition_Observation_V1.md` | `reference_only` | observed authority precondition≠decision | rollback runtime pipeline | S-002 approval provenance 参考 |
| 46 | `Strategy_Runtime_SAG_Human_Decision_Recording_V1.md` | `adapt_extract` | recorded/approved/executed 分轴、decision provenance | rollback/invalidation/repair fields | S-002 decision record contract；S-003 Dashboard rule |
| 47 | `Strategy_Runtime_SAG_Invalidation_Model_Runner_V1.md` | `adapt_extract` | change observation→review advisory；建议≠动作 | SAG graph mapping/runner | S-002 change-impact contract；S-003 context trigger |
| 48 | `Strategy_Runtime_SAG_Invalidation_Review_Queue_Handoff_V1.md` | `reference_only` | pending human decision、handoff lineage | runtime queue | S-002 Loop pause/Decision 参考，不建第二 queue |
| 49 | `Strategy_Runtime_SAG_Isolated_Rollback_Execution_V1.md` | `remove` | destructive safety 由通用 hard gate 吸收 | rollback executor/store/schema | S-004 排除；未来独立 extension 才可设计 |
| 50 | `Strategy_Runtime_SAG_Observation_Graph_V1.md` | `adapt_extract` | observation≠truth、schema-valid≠accepted、closed claims | SAG nodes/edges/M1/Mc/Flow/Slice | S-002 evidence graph contract；S-004 DKG projection |
| 51 | `Strategy_Runtime_SAG_Observation_Store_Semantic_Diff_V1.md` | `adapt_extract` | append-only provenance、reload validation、structural diff≠resolution | SAG store/runner/schema | S-002 final-diff contract；S-003 validation snapshot |
| 52 | `Strategy_Runtime_SAG_Observation_Store_V1.md` | `reference_only` | stale digest fail-closed、reject no-write | stateful SAG store | S-002 provenance 参考，不迁 runtime |
| 53 | `Strategy_Runtime_SAG_Rollback_Approval_Recording_V1.md` | `reference_only` | decision≠action approval；approved≠executed | rollback-specific state machine | S-002 destructive authority 参考 |
| 54 | `Strategy_Runtime_SAG_Rollback_Decision_Request_Observation_V1.md` | `reference_only` | request≠decision、typed closed filter | rollback queue | S-002 human-decision checkpoint 参考 |
| 55 | `Strategy_Runtime_SAG_Rollback_Execution_Precondition_Observation_V1.md` | `reference_only` | approval≠execution authority；authorized≠executed | rollback target pipeline | S-002 external/global/destructive authority 参考 |
| 56 | `Strategy_Runtime_SAG_Semantic_Diff_Observation_V1.md` | `reference_only` | 两端 reload validation；diff observation≠semantic resolution | SAG graph/hash runner | S-002 delta/final diff 参考 |

## 汇总与 S-002 强制复核

| 裁决 | 数量 |
| --- | ---: |
| `migrate_after_refreeze` | 2 |
| `adapt_extract` | 26 |
| `reference_only` | 14 |
| `remove` | 14 |
| 合计 | 56 |

S-002 必须重新验证每个候选的 canonical mapping、目标 ontology、重复 owner、applicability 和 claim ceiling。本清单最重要的 forbidden collapses 是：observation≠truth、diff≠resolution、advisory≠invalidation/action、request≠decision、recorded≠approved、approved/authorized≠executed、schema-valid≠semantic acceptance、Dashboard/DKG/BDD/read-model≠canonical truth。
