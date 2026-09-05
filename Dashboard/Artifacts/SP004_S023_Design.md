# S-023 现状重基线、合同与裁决冻结

## 关键结论中文展开

本 lane 只形成 S-023 的设计交接与 ERBE 输入，冻结十项 Finding 的当前证据、身份/状态边界、可观察判定和后续实现入口。十项 Finding 当前均未关闭；`contract_frozen_for_implementation` 只表示合同可以交给 S-024 及后续 lane 使用，不表示修复、批准、发布或 rights 已发生。

## 读取清单与边界

| 类型 | 本次读取 | 用途与边界 |
| --- | --- | --- |
| 用户指定 lane card | [S-023 Design Lane Task Card](SP004_S023_DesignLaneTaskCard.json) | 以 card 的 source、Delta Read Set、write scope 和最大主张为准；摘要校验已通过 |
| 原始目标 | [SP-004 Loop Goal](SP004_SemxResidueOpenSourceGaps_LoopGoal.md) | 保留 GAP-MH-01..10 与 AC-01..12；不重写原始范围 |
| Finding 来源 | [Capability Panorama](RepositoryCapabilityPanorama.md)、[Audit Report](RepositoryCapabilityPanorama_Audit_Report.md) | 作为当前 finding inventory；不是批准或发布 authority |
| 当前实现/证据 | [README](../../README.md)、[Quick Start](../../docs/Quick_Start_CN.md)、[Beginner Guide](../../docs/Beginner_Guide_CN.md)、[public manifest](../../public_export_manifest_v1.json)、[public tool](../../tools/sge_public.py)、`tests/`、`kb/data/strategy/` | 做静态/结构性现状核对；未把文件存在或旧测试结果升级为端到端证据 |
| 相邻历史 | `Dashboard/Artifacts/SP003_*` | 仅作为前置边界和历史证据；SP-003 有界结果不吸收本次 Finding |
| 治理规则 | [AGENTS.md](../../AGENTS.md)、[SGC v1](../../kb/data/strategy/strategy_sgc_structural_contract_v1.json) | 约束 claim ceiling、Scope Delta、truth split 和 RED/GREEN |

未读取/不可补齐：具体 GitHub owner/repo/branch、最终 candidate rights owner 确认、远端 CI/commit/tree/tag/assets/read-back、外部 CG。`CG skipped: no CG input provided`。本 lane 不访问 credential，不执行远端动作。

## 当前基线与身份矩阵

当前 checkout 为 `sge/sp002`；工作区已有用户变更，不能把其 dirty 状态当成新 candidate。public manifest 当前声明 48 个 allowlisted files，候选仍是 `candidate_not_approved`。现有实现/文档已经提供部分本地 lifecycle 和 default-deny 证据，但不能证明 public repo、rights、release 或生产状态。

| 身份轴 | 当前设计裁决 | 当前证据/缺口 | 不可替代 |
| --- | --- | --- | --- |
| `private_source_revision` | `sge-governance-skill` 是唯一 canonical development source | 当前本地仓与 SP-003 双仓策略；无公开仓存在证据 | public repo、candidate、release |
| `candidate_id` / `candidate_tree_digest` | 每次 exact allowlist projection 的独立候选身份 | manifest/tool 有 identity 结构；本轮未生成 fresh candidate | rights approval、远端 commit |
| `public_owner_repo_url` / `default_branch` | 目标 proposal 为 `bm-sge-governance`；具体 URL/branch 待 C2 冻结 | Panorama/Goal 为 proposal | public repo 已存在 |
| `commit` / `tag` / `asset_checksum` | 只在授权远端 mutation/read-back 后填写实际值 | 当前无远端 read-back | candidate/local validation |
| `rights_approved` | 必须由 rights owner 对 exact candidate 逐文件确认 | 当前不存在 | MIT 字段、manifest、测试、登录态 |

状态轴必须独立记录：`candidate_built`、`locally_validated`、`rights_approved`、`release_authorized`、`remote_mutation_succeeded`、`remote_readback_verified`、`production_ready`。本设计允许的当前状态是：候选/本地证据可能存在，但 rights、授权、远端 mutation/read-back、production 均未证明。

## 十项 Finding 当前证据矩阵

| ID | 当前证据与结论 | 可观察 predicate | 负例/阻断 | owner/时序 | 当前 claim ceiling |
| --- | --- | --- | --- | --- | --- |
| GAP-MH-01 / F-P0-IDENTITY | Panorama 记录 README/title、candidate_id 仍与 `bm-sge-governance` proposal 不一致；public 命中为 0；现有 doctor 未阻断 | source/public project/Skill/candidate 四角色分别声明且冲突时 gate 非零 | 角色混用、同名伪装或 public identity 无对应 gate => `fail_closed` | S-024 Builder + independent Validation | `current_evidence_only` |
| GAP-MH-02 / F-P1-QUICKSTART | [Quick Start](../../docs/Quick_Start_CN.md) 当前把中文说明放在 bash fence 内 | 每个 `bash` fence 仅含 shell；逐块复制有成功或预期 fail-closed transcript | 自然语言进入 shell => `fail_closed` | S-024/S-026 | `not_validated` |
| GAP-MH-03 / F-P1-CODEX-UAT | Beginner Guide 有 Goal/Session/Validation 提示，但无真实独立可见 clean-room task/transcript/artifact inventory | 独立 task 完成 discovery→Goal→Session→Validation→closeout，且证据可定位 | 主线程代做、只给 prompt/CLI/最终文件 => 不合格 | S-026 UAT + independent Validation | `evidence_gap` |
| GAP-MH-04 / F-P1-CORE-COVERAGE | manifest 有 48 项，现有历史仅代表性入口/本地测试；未见消费仓逐文件 capability matrix | 17 core 文件逐项有角色；8 core scripts 有入口 smoke 或有理由的 N/A | 文件存在、import 或零测试不能算能力通过 | S-025 Builder/Validation | `evidence_gap` |
| GAP-MH-05 / F-P1-RIGHTS | manifest 有 `source/license/provenance/public/execution_context` 字段；没有 rights owner 对 exact candidate 的人类确认 | 每个 allowlisted file 绑定 candidate/tree digest 并获 owner 确认 | 未确认、冲突、dirty/digest drift => 阻断 release | S-027/C2 human authority | `authority_gap` |
| GAP-MH-06 / F-P1-RELEASE-ASSETS | 当前无冻结 owner/URL/branch/version/tag、最终 checksums/license report/release notes/remote read-back | release packet 与授权 payload、远端 commit/tree/tag/assets/checksum 一一匹配 | 本地 tag、CI check、结构字段冒充远端发布 => `fail_closed` | S-027/S-028 | `not_run` |
| GAP-MH-07 / F-P2-PROVENANCE-LINKS | Panorama 指出若干 public KB refs 指向未随包发布的 Dashboard/Artifacts 历史文件 | locator 可在 public 包解析，或显式 `external/private` 且不伪装相对 public path | private Dashboard relative locator => `fail_closed` | S-024 Builder/Validation | `evidence_gap` |
| GAP-MH-08 / F-P2-PILOT-ID | Panorama 指出 `context_efficiency_pilot.py` 等 public core 仍硬编码 SP-041 paired rollouts | public API/help/text 使用项目中立概念；历史 provenance 留 private/external | SP-041 作为 public default product semantics => `fail_closed` | S-024 | `evidence_gap` |
| GAP-MH-09 / F-INFO-SEMX | audit 仅见 `semx` deny token/负例；无 Semx 产品依赖或个人路径 | deny token 保留为 isolation control；contextual scan 区分 token、fixture 与 active dependency | token 被删、变成 product dependency 或 authority => `fail_closed` | S-024/S-029 | `preserve_and_prove` |
| GAP-MH-10 / F-INFO-HISTORY | 历史 Dashboard/Archives/closeout/Agent Logs 含 provenance，manifest default-deny 排除 | private history 可定位；public allowlist 不含这些 surface，且扫描有边界 | 为了 grep 零命中而公开/删除历史 => `fail_closed` | S-024/S-029 | `preserve_and_prove` |

以上是现状与设计判断，不是十项的关闭状态。最终 OPCM 必须仍逐项列出 observable result、精确链接、阻断/例外、lane/时序、claim ceiling 与 Parent/Closeout 吸收状态。

## ERBE 设计冻结

`erbe_applicability=required`：本 Goal 改变 identity、authority routing、provenance locator、rights gate、candidate→release 状态边界。机器合同见 [SP004 S-023 Contract](SP004_S023_Contract.json)，案例见 [SP004 S-023 Cases](SP004_S023_Cases.json)。

冻结规则：

- Contract/Cases 的 `case_id`、predicate、expected、failure fingerprint 和 claim ceiling 是 Builder 禁止修改的输入。
- 可信 RED 必须同时满足 `contract_verdict=valid`、`execution_verdict=ok`、failure fingerprint 匹配；环境、fixture、import、path、network 错误只能记 `error`。
- GREEN 必须复用相同 frozen case identity，由独立 Validation 从 durable inputs 重算；producer 自报 terminal status 不算 GREEN。
- `candidate_not_approved` 不等于 `rights_approved`；local success 不等于 remote success；Dashboard evidence 不等于 KB canonical truth。
- 本轮不执行 RED/GREEN，不修改公共行为、KB canonical truth、BDD、Dashboard registry、Git/远端元数据。
- 失败诊断完整覆盖 S1-S6 与 L0-L6：S1-S6 均有对应 Finding；L0-L5 适用于本设计，L6 在 S-023 明确标为“不适用”（本阶段无 runtime evolution），若后续 S-024 改变运行时行为必须重新分类并 rebaseline。

## 实现入口与验证重点

### 最小安全实现切片

S-024 的最小切片固定为：输入=当前 manifest、Quick Start、pilot script、KB locator 与冻结 RED 案例；输出=项目中立 identity/locator/residue gate、文档修订和 exact candidate diff；独立 gate=同一组 RED identity 的负例回放；回滚=只撤销 S-024 文件，不触碰 C2 packet、rights 记录或远端；依赖=本 Design/Contract/Cases 与 Semantic Review 通过。该切片不得修改 expected、case identity、rights 状态或远端。

### Implementation ladder 与 next-session map

1. S-023：合同/案例/语义边界冻结；handoff 为本文件与 JSON；exit 为 card 与双 verdict 通过。
2. S-024：identity → locator → Quick Start → pilot/residue 修复；handoff 为 exact diff 与 RED/修复报告；exit 为 GAP-MH-01/02/07/08/09/10 的独立验证。
3. S-025：fresh consumer capability matrix；entry 依赖 S-024 candidate；exit 为 17 文件/8 script 逐项 evidence。
4. S-026：独立可见 Codex UAT；entry 依赖 S-025；exit 为 transcript、artifact inventory 和独立 verdict。
5. S-027：exact candidate release/rights packet；entry 依赖 S-026；exit 为 `pending_human_confirmation`，然后进入 C2。
6. S-028/S-029：只有 C2 exact authorization 才进入 remote mutation；否则保持 blocked，不得移除原始 must-have。

任何 source digest、Goal/AC、authority、claim ceiling 或 topology 变化都触发 rebaseline；未改变这些输入时后续 Validation 使用 snapshot + Delta Read Set。

| 后续切片 | 允许入口 | 交付证据 | 禁止提前主张 |
| --- | --- | --- | --- |
| S-024 | identity/locator/residue/SP-041 文档、代码、gate 修订 | exact diff、正负 gate、必要 BDD sync | 全部 core、UAT、rights、release |
| S-025 | consumer fresh target 的 17 core/8 scripts matrix | 逐项 smoke/N/A、失败 transcript、独立复核 | 通用平台/仓库能力 |
| S-026 | 独立可见 Codex clean-room task | task/thread、target、transcript、artifact inventory | 主线程模拟 newcomer |
| S-027/C2 | exact candidate 的 packet/rights 表；C2 才处理 authority | digest-bound manifest、license report、逐文件确认 | `rights_approved` 或 `published` |
| S-028 | 仅消费 C2 具体 payload | remote mutation 与 read-back | production-ready |
| S-029 | Final Validation/Semantic/OPCM/closeout/reconciliation | 覆盖原始十项与最终状态的 durable evidence | 由本设计关闭 Finding |

未来 agent 误用场景及缓解：

1. 看到 `contract_frozen_for_implementation` 就写 `done`：设计标题与结论明确禁止；Validation 必查 claim ceiling。
2. 看到 manifest 的 MIT/provenance 字段就写 rights approved：rights predicate 要求人类逐文件绑定 exact candidate。
3. 看到 `semx` 命中就删除历史/deny token：GAP-MH-09/10 明确 contextual isolation 与历史可追溯性。
4. 看到本地 test/CI 通过就写 release：状态轴、remote read-back 和 C2 authority 分离。

## Design Freeze Validity

`conditional / ready-for-review`（有条件、可供复核）：本设计保持原始十项范围、分离 truth/authority/state、提供逐项 predicate 与 ERBE 输入；但本 lane 尚未获得 Semantic Reviewer verdict，也没有执行行为 RED/GREEN，因此不能称为已验证或已批准的设计。

## Implementation Entry Readiness

`ready_for_bounded_entry`（可进入有界实现）：S-024 可从 GAP-MH-01/02/07/08/09/10 的最小修复切片开始，S-025/S-026/S-027 的输入、禁止越界和证据要求已明确。任何实现若改变 predicate、expected、case identity、authority 或 claim ceiling，必须走 Contract Patch + Scope Delta + re-RED；不能直接编辑本合同来适配结果。

## Scope Delta 与 KB/Dashboard 复核

本 lane 未删除、合并、改名、降级或延期任何原始 must-have；`Scope Delta=none`。本设计只在 card write scope 内更新 Dashboard artifact，不更新 `kb/` canonical truth、Dashboard registry、Sessions/Stage Plan 或公共源码。合同中的稳定规则仍是当前 Session 的 design input；若后续批准并复用为稳定 truth，必须另做 Contract Delta Scan，分类为 `promote-to-KB`、`Dashboard-only`、`gate-docs/runtime/tests later` 或 `deferred session`，不能由本 lane 自动晋升。

### 状态词压缩审计

`Doing`=当前 Session 正在执行，不等于已完成；`To do`=尚未开始；`Done` 在 SP-003 中只表示其本地/合同范围有界完成；`candidate_not_approved`=候选未获发布批准；`contract_frozen_for_implementation`=合同冻结、可供受限实现，不表示修复；`landed`=指定切片已落地，不等于 Goal complete；`preserve_and_prove`=保留并验证隔离，不是删除成功。以上词语在 Dashboard row、Goal、Contract、Closeout 中均不得脱离中文解释单独构成完成结论。

## Claim ceiling

本 lane 最大主张严格为：`contract_frozen_for_implementation`（已冻结可供实现使用的合同）。不得宣称任何 Finding 已关闭、任何修复已落地、独立 Validation 已通过、rights 已批准、release 已授权、远端 mutation/read-back 成功、公开仓已存在或 production ready。
