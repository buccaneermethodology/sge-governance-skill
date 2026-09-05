# S-024 独立验证复核

## 关键结论中文展开

本次验证检查的是 S-024 在当前 checkout 中对 active/public 边界的有界修订：身份矩阵、Quick Start shell fence、public provenance、项目中立 pilot-id，以及 Semx/history 隔离。Builder 的实际代码/文档/测试 diff 位于 Builder card 的 `write_scope` 内；S-023 Contract/Cases 文件未被修改，冻结摘要与 card 一致。

当前结果不能写成 S-024 `PASS` 或 `Done`：本地测试与 doctor gates 通过，但两个必要的 fail-closed 语义门禁没有被实现到足以支撑对应 predicate 的强度；同时没有 S-024 durable 的 trusted RED/GREEN case execution evidence。结果是唯一的 `partial_blocked`：已验证的本地结构/行为范围保留，S-024 退出条件与更高层 Goal 完成不能声明。

## Read Manifest

### 已读取

- [AGENTS.md](../../AGENTS.md)：仓库硬门、只读 Validation、SGC、Goal Conformance、closeout 与 KB/Dashboard 分界。
- [S-024 Validation Lane Task Card](SP004_S024_ValidationLaneTaskCard.json)：card digest `46200bb44184d1a42063517ce8185cdda86aca432f74bf8b5b255134331dbf54`，`write_scope` 仅为本 Review 与 State Snapshot。
- [SP-004 Loop Goal](SP004_SemxResidueOpenSourceGaps_LoopGoal.md)：原始十项 must-have、S-024 退出条件、completion rule、禁止收束措辞。
- [S-023 Contract](SP004_S023_Contract.json)、[S-023 Cases](SP004_S023_Cases.json)、[S-023 Semantic Review](SP004_S023_SemanticReview.md)：冻结 state axes、GAP-MH-01/02/07/08/09/10 predicate、RED/GREEN identity、failure fingerprint、claim ceiling 与 Builder 禁止修改项。
- [S-024 Builder Lane Task Card](SP004_S024_BuilderLaneTaskCard.json)：Builder `write_scope`、required outputs、最大主张及 topology。
- 当前 Dashboard：[Sessions](../Sessions.md)、[Session Index](../Session_Index.md)、[Current State](../Current_State.md)、[Stage Plans](../Stage_Plans.md) 及 SP-004 archive；确认 S-024 仍为 `Doing`，S-025/S-026 尚未开始。
- 实际 diff 与源表面：[README](../../README.md)、[Quick Start](../../docs/Quick_Start_CN.md)、[public manifest](../../public_export_manifest_v1.json)、[public lifecycle tool](../../tools/sge_public.py)、[repository doctor](../tools/doctor.py)、pilot、三组测试与 [BDD readable card](../../tests/bdd/readable_cards/sp004/identity-locator-residue.md)。
- KB truth 与门禁：`kb/data/strategy/strategy_sgc_structural_contract_v1.json`、对应 Markdown、`render_kb.py --check`、Session registry check/validate。

### 未读取或明确不执行

- 未读取或访问远端 owner/repo/branch/tag/commit/assets/CI；未执行 remote mutation、rights、release、Git handoff 或生产判断。
- 未启动 S-025 core capability、S-026 独立可见 Codex UAT、S-027 release packet、S-028 remote lane；因此 GAP-MH-03/04/05/06 不在本 Session 的通过范围内。
- S-023 Contract/Cases 规定本 lane 不执行 cases；本轮仍独立核对 case identity 与 durable artifact 缺口，不把普通 unittest 冒充 ERBE RED/GREEN。

## Evidence Completeness

| 原始/当前要求 | 实际证据 | 结果与边界 |
| --- | --- | --- |
| GAP-MH-01 身份分离与冲突 fail-closed | manifest 四角色 distinct；README 声明 public project；identity fixture 测试；repository doctor pass | `partial`：正向与碰撞负例可见；未证明所有文档/locator authority 一致 |
| GAP-MH-02 Quick Start shell-only | [Quick Start](../../docs/Quick_Start_CN.md) 一个 bash fence；30 tests pass | `partial`：语法检查通过；未形成逐块 fresh clean-room durable transcript |
| GAP-MH-07 locator 可解析或 typed external/private | manifest 声明 allowed types 与 relative-private-links forbidden；doctor pass | `blocked`：实现只扫描 `Dashboard/Archives/`、`Dashboard/Agent_Logs/`，未验证每个 source locator 的类型，也未覆盖 `Dashboard/Artifacts/` 相对链接 |
| GAP-MH-08 SP-041 去默认语义 | allowlisted public files 未命中 `SP-041`；pilot 输出加入 project-neutral `pilot_id` | `partial`：当前树未见默认耦合；没有独立 public API/help 及历史 provenance 分离的完整证据 |
| GAP-MH-09 Semx deny token 为隔离控制 | manifest 声明 `semx` deny token；active product token scan pass | `blocked`：`check_public_residue()` 不检查 deny token 是否存在/分类，移除该字段仍可返回 pass |
| GAP-MH-10 私有历史 default-deny | manifest 未 allowlist Dashboard 文件；导出 48 文件；public residue/local doctor pass | `partial`：导出隔离成立；locator gate 未覆盖全部私有历史表面，不能把“未导出”扩大为完整 provenance 可定位证明 |
| frozen S-023 case identity | Contract SHA `da0d15…a8b2`、Cases SHA `4ffb3b…2fb3` 与 Validation card 一致；Cases 内容未出现在 Builder diff | `pass`（identity binding only）；没有可信 RED/GREEN execution evidence |
| public export/verify/doctor | public doctor pass；临时目录 export 48 files；`verify_projection` 重算 tree；repository doctor pass | `pass`（当前 checkout 的结构/行为范围）；不证明 rights/release/remote |
| repository/KB/Dashboard gates | unittest 30/30；repository doctor 全部 gate pass；registry check/validate pass；KB render check pass；DKG 临时生成 pass；diff check pass | `pass`（门禁结果）；不覆盖本 Review 的语义缺口 |

## Frozen RED/GREEN identity 重算

- Contract/Cases 的当前 SHA 与 card 绑定值一致；Cases 的 `SP004-RED-01..06`、`SP004-GREEN-01..10` identity 未被 Builder diff 修改。
- Cases 明确要求 `contract_valid`、`execution_ok`、failure fingerprint 匹配，且环境错误只能是 `error`。本轮没有执行 S-023 cases；普通测试通过不能替代 `trusted_red` 或同 identity 的独立 GREEN recompute。
- 因此 RED identity 为“冻结且未改动”，不是“RED 已可信验证”；GREEN 为 `not_performed`，不是通过。

## 阻断发现

1. `Dashboard/tools/doctor.py:140-152` 的 residue gate 只扫描 `semx-cli`、`semx-kb`、`audio-transcriptor`，没有验证 manifest 中 `deny_tokens_are_controls` 包含 `semx`。这不满足 GAP-MH-09 的 contextual preservation predicate，属于 fail-closed coverage 缺口。
2. `Dashboard/tools/doctor.py:121-137` 的 locator gate 只拒绝两类相对目标，不读取每个 locator 的 typed disposition，也没有拒绝/审计 `Dashboard/Artifacts/` 私有历史相对链接。仅有 manifest policy 字段和当前无命中不能证明 GAP-MH-07/GAP-MH-10。
3. 没有 S-024 durable trusted RED/GREEN execution report；S-023 Cases 的 `本 lane 不执行 cases` 约束不应被普通 unittest 的 `OK` 隐式改写。

## 非阻断发现与开放问题

- Quick Start 的 shell-only parser 只允许有限命令前缀；它对当前文档足够，但不是完整 shell 解析器，仍需 S-026 clean-room transcript。
- Builder 实际变更面与 Builder card `write_scope` 相符；本 checkout 另有 Dashboard/Goal/registry surfaces 变更，它们不属于 Builder write scope，不能归因给 Builder 或由本 Review 重新解释为产品实现。
- `public_export_manifest_v1.json` 自身包含私有历史前缀作为 policy metadata；当前 gate 对 manifest 做了例外式扫描。需要明确这是允许的 policy declaration 还是应使用更精细的 metadata-aware locator audit。

## 要求的 Builder 修复

- 为 GAP-MH-09 增加 deny-token presence/classification 的执行检查与正负 fixture，确保移除或误分类 `semx` 时非零并给出 failure fingerprint。
- 为 GAP-MH-07/GAP-MH-10 建立 locator inventory/resolver：逐项检查 `in_package`、`external`、`private` disposition，禁止所有未声明的私有相对链接，至少覆盖 `Dashboard/Archives/`、`Dashboard/Agent_Logs/`、`Dashboard/Artifacts/`；补充负例。
- 在修复后以相同 frozen case identity 重新建立/运行必要 RED，并由独立 Validation 从 durable inputs 重算 GREEN；环境/fixture/path 错误必须保持 `error`。

## SGC v1 与 claim ceiling

本轮最高 claim ceiling 为 `S-024 active/public repairs partially structurally supported in current checkout`。SGC 结论：测试绑定的本地结构证据不能上升为外部支持、rights approved、release authorized、remote success、production ready 或 Goal complete；当前 `candidate_not_approved`、`rights_approved`、release/remote/production state axes 均未改变。

## Semantic / PDI 触发

- Semantic Reviewer：**触发**。本轮涉及 public/private authority、locator truth placement、deny-token 语义和项目去耦；应对上述两个 gate 缺口做 Boundary Review 与 Evolution/Implementation-Entry Review。当前 Review 不冒充 Semantic verdict。
- PDI：**触发**。这是可复现的治理/门禁缺陷（policy declaration 与 executable classifier 不一致）；应把修复沉淀到 gate、negative fixture、readable card 与后续 Validation evidence，而不是只改 closeout prose。

## KB/Dashboard review

- `kb/`：本轮不写入。当前观察是实现/门禁缺口，尚未形成已批准的稳定 canonical policy delta；若修复后批准 locator/deny-token 规则为稳定 truth，再做最小 Contract Delta Scan 与 JSON-first promotion。
- `Dashboard/`：本轮仅按 card 写入本 Review 与 State Snapshot；不改 Session registry、Goal、Stage Plan 或 Dashboard 状态。S-024 应保持 `Doing`，下一候选为在原范围内修复两项 gate 并重新验证；S-025 不因本轮 partial 自动宣称 ready/complete。

## 唯一 Validation verdict

`partial_blocked`：当前 checkout 的 public export/verify/doctor、repository gates、身份正向检查、Quick Start fence 基础检查和 frozen Contract/Cases identity binding 有证据；GAP-MH-07、GAP-MH-09、GAP-MH-10 的完整 fail-closed predicate 与 trusted RED/GREEN evidence 缺失。因此不能声明 S-024 退出条件满足、不能写 `PASS`/`Done`/`SP-004 complete`。

## 证据命令

- `lane_task_card.py validate ... --expected-card-sha256 46200...`：pass。
- `python3 -m unittest discover -s tests -p 'test_*.py'`：30/30 pass。
- `python3 tools/sge_public.py doctor`：pass；临时目录 export 48 files，`verify_projection` tree 重算成功。
- `python3 Dashboard/tools/doctor.py --repo .`：all gates pass，包括 registry、KB render、genericity 与临时 DKG。
- `git diff --check`：pass。
