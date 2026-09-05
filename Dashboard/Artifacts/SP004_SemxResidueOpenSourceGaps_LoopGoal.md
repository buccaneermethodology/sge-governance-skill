# SP-004 Semx 残留与开源缺口闭环 Loop Goal（提案）

## Goal 身份与提案状态

- Goal ID：`SP-004`（本轮执行身份；Dashboard registry 注册与 Git 交接受当前权限边界约束）。
- Session DAG：`S-023 → S-024 → S-025 → S-026 → S-027 → C2 人类授权 → S-028 → S-029`；`S-023..S-029` 均为提案编号，正式登记前必须复核是否冲突。
- 当前状态：`executing_with_release_authority_checkpoint`（已由本次用户指令启动；本文件不证明 Finding 已关闭、rights 已批准、公开仓已存在或 release 已发布）。
- 原始范围：[Repository Capability Panorama 的“Semx 残留与开源缺口”](RepositoryCapabilityPanorama.md#semx-残留与开源缺口)中的 10 项 Finding，逐项保留，不得以 SP-003 的有界完成或一次 grep/doctor 结果整体吸收。
- 上下文启动证据：[Context Bootstrap](SP004_SemxResidueOpenSourceGaps_ContextBootstrap.json)。
- `CG skipped: no CG input provided`。
- 本轮启动时间：2026-09-04；当前 checkout：`sge/sp002`，Git branch 创建因本地 `.git` 写权限失败，已作为执行边界记录，不改变 Goal 范围。

## 中文任务解释

本 Goal 要把当前公共候选从“本地架构与工具已有基础，但仍存在身份、文档、端到端证据、权利和真实发布缺口”的状态，推进到一份可由外部读者独立使用、可由维护者审计、并在获得具体人类授权后完成远端发布与 read-back 的公开版本。

它不等于“删除所有 Semx 字样”。`semx` 作为 `forbidden_target_authority_tokens` 的负例，以及私有 Dashboard 中的历史迁移 provenance，分别承担防污染与可追溯作用；只要它们不进入错误的 active/public authority，就应保留并由测试证明隔离。真正需要清理的是 active/public 身份冲突、不可复制的新手说明、内部 Session 耦合和公共包无法解析的 provenance 入口。

SP-003 已把双仓方向、local projection/lifecycle 和发布权限边界做成有界合同，但明确没有证明逐文件 rights、公开 GitHub 仓、真实 push/tag/release、远端 CI/read-back 或 production readiness。本 Goal 以该边界为前置条件，不重做 SP-003，也不把它的 `bounded_complete`（有界完成）误读为公开发布完成。

## Read Manifest

### 已读

- 用户指定源：[Repository Capability Panorama](RepositoryCapabilityPanorama.md)及其[详细审计报告](RepositoryCapabilityPanorama_Audit_Report.md)。
- 仓库治理：`AGENTS.md`、`.codex/skills/sge-governed-checkpoints/SKILL.md`、Goal/Loop/Context Efficiency checklist。
- 当前 Dashboard：[Current State](../Current_State.md)、[Stage Plans](../Stage_Plans.md)、[Sessions](../Sessions.md)。
- 既有双仓边界：[SP-003 Loop Goal](SP003_OpenSourceDistributionArchitecture_LoopGoal.md)、[S-022 Closeout](SP003_S022_Closeout.md)。
- canonical truth：[双仓策略 JSON](../../kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json)、[SGC v1 JSON](../../kb/data/strategy/strategy_sgc_structural_contract_v1.json)。
- 当前 public surface：[public manifest](../../public_export_manifest_v1.json)、[README](../../README.md)、[Quick Start](../../docs/Quick_Start_CN.md)、`context_efficiency_pilot.py`。

### 缺失或执行期必读

- 具体 GitHub owner、repo URL、default branch、保护规则、release version/tag/payload：尚无人类冻结，必须在 S-027/C2 读取或取得。
- 最终逐文件 rights owner 签署：当前不存在，必须在 C2 由人类对最终 candidate 精确确认。
- 真实 remote CI、commit/tree/tag/assets/checksum read-back：只有 S-028 获得具体写入授权并实际执行后才会存在。
- 外部 CG 输入：未提供，因此不产生 CG verdict。

### 跳过

- 本轮 Goal 设计不读取或操作任何登录态、credential、远端仓库或全局 Skill 目录，因为用户尚未授权实现或发布动作。

## Source authority 与现状校准

| 表面 | authority | 本 Goal 如何使用 |
| --- | --- | --- |
| 用户本次指令 | 原始目标 authority | 要求覆盖 Finding 表的每一项内容 |
| `kb/data/strategy/strategy_open_source_dual_repo_distribution_v1.json` | 稳定双仓 canonical truth | 固定私有 `sge-governance-skill`、公开 `bm-sge-governance`、单向 projection 与外部授权边界 |
| Panorama / Audit Report | Dashboard 派生观察与 finding 来源 | 作为 must-have inventory，不直接充当当前真相或完成 verdict |
| SP-003 closeout/OPCM | 历史执行证据 | 证明本地/合同范围与明确未做的远端/rights 范围 |
| 当前代码、manifest、文档、tests | 实现与 witness | 每个 Session 必须重新检查，不得只引用旧审计 |
| 人类 rights/release 授权记录 | 外部 mutation authority | C2 前不存在；任何结构字段、测试或 GitHub 登录都不能替代 |
| 独立 Validation / remote read-back | evaluation evidence | 支撑相应 claim，但不自动提升到 production readiness |

## Goal Mission

在保留私有 `sge-governance-skill` 为唯一 canonical development source、公开 `bm-sge-governance` 为单向 exact-allowlist projection 的前提下，逐项关闭 Panorama 中可修复的 active/public 与 evidence 缺口；为两项 INFO 建立“应保留且受隔离”的回归证据；冻结最终 candidate 的逐文件 rights/identity/release packet；并且只有在 repo owner 对具体 owner/repo/tree/branch/tag/payload/rights 明确授权后，才执行远端发布与 read-back。最终由独立 Validation、Semantic Review、OPCM、中文 closeout 与 post-closeout reconciliation 判断 Goal 是否完成。

## 原始 Must-have Ledger

| ID | Panorama Finding | 必须达成的可观察结果 | 验收 evidence | 主 Session | 当前设计状态 |
| --- | --- | --- | --- | --- | --- |
| GAP-MH-01 | `F-P0-IDENTITY` | private source、public repo、project display、manifest `candidate_id`、docs、doctor/gate 的身份角色一致；不要求把私有源仓也改成 public 名 | identity matrix；正负 fixtures；doctor 在冲突时非零；公开树扫描 | S-023/S-024 | pending |
| GAP-MH-02 | `F-P1-QUICKSTART` | bash fenced blocks 只含可执行 shell；说明移出 code fence；从 fresh candidate 逐块 copy/paste 可成功或按预期 fail closed | fence parser/copy-paste test；clean-room transcript | S-024/S-026 | pending |
| GAP-MH-03 | `F-P1-CODEX-UAT` | 真实、独立可见的 clean-room Codex 流程覆盖 Skill discovery、入口、Goal→Session→Validation→closeout 与预期文件 | 独立 task/thread ID、clean target、UAT transcript、artifact inventory、verdict | S-026 | pending |
| GAP-MH-04 | `F-P1-CORE-COVERAGE` | public manifest 中所有 17 个 core 文件都有角色、入口/非入口解释、smoke/negative/不适用 verdict；8 个 core script 的公共入口逐项执行或有可验证 N/A | capability matrix；逐入口命令/输出；consumer repo artifacts | S-025 | pending |
| GAP-MH-05 | `F-P1-RIGHTS` | 对最终冻结 candidate 的每个 allowlisted 文件获得人类 rights owner 的 source/license/provenance/public/execution-context 确认；任何未确认或冲突项阻断发布 | exact manifest/tree digest；逐文件 signed/approved record；blocker list | S-027/C2 | pending human authority |
| GAP-MH-06 | `F-P1-RELEASE-ASSETS` | 冻结 owner/URL/default branch/version/tag、CI、SHA256SUMS、license report、release notes、authorization record；授权后执行并 read back commit/tree/tag/assets/checksum/CI | release packet；CI results；remote read-back report；授权 reference | S-027/S-028 | pending human authority |
| GAP-MH-07 | `F-P2-PROVENANCE-LINKS` | 每个 public allowlisted KB JSON/Markdown 的 source locator 在公开包内可解析，或按 canonical policy 明确标为 external/private locator 且不会伪装成公开相对路径 | locator inventory；resolver/gate；负例；KB Contract Delta 证据 | S-023/S-024 | pending |
| GAP-MH-08 | `F-P2-PILOT-ID` | 公共 core 不再把 SP-041 当作产品默认语义；公共接口使用项目中立名称，历史 SP-041 provenance 只留私有层或显式外部 locator | source scan；API/help/test；private provenance link | S-024 | pending |
| GAP-MH-09 | `F-INFO-SEMX` | `semx` deny token 的防污染语义明确保留；公开候选不得出现 Semx product dependency、authority 或私有路径；fixture token 不被误报为依赖 | contextual residue classifier；positive/negative fixtures；public tree scan | S-023/S-024/S-029 | preserve-and-prove |
| GAP-MH-10 | `F-INFO-HISTORY` | 私有 Dashboard 中的 Semx provenance 保持可定位；public manifest 继续 default-deny 排除 Dashboard/Agent Logs/closeout/history；不得用“清理”破坏历史 | private/public boundary test；manifest inventory；history link audit | S-023/S-024/S-029 | preserve-and-prove |

所有 10 行均为原始 must-have。合并 Session 不等于合并验收行；最终 OPCM 必须仍逐行给出 acceptance predicate、精确链接、实际结果、状态、blocker/例外、lane/时序、claim ceiling 与 Parent/Closeout 吸收状态。

## Scope 与 Non-goals

### In scope

- 当前 private canonical 与其 deterministic public candidate/public repo 的 identity、docs、provenance、core coverage、Codex newcomer UAT、rights packet、release assets、authorized publication/read-back。
- 与上述行为直接对应的 contracts、tests/gates、public docs、manifest、CI、release evidence、KB stable delta、Dashboard execution evidence。
- 对 INFO finding 的保留与隔离验证，而不是机械删除。

### Out of scope

- 不实现 Semx/KYM/TCO/audio 产品能力，不迁移其业务 runtime 或历史 Session 到 public core。
- 不把 `build-kym`、`build-tco-coverage` 的接口占位改写为已安装实现。
- 不证明任意 repo、所有 OS、所有 Codex 版本、性能/SLA、安全审计或 production readiness。
- 不把公开仓变成第二 canonical source；public PR 仍须回流 private source 后重新 export/validate。
- 未经 C2 明确授权，不创建/改写远端 repo，不 push、tag、release，不配置具有 mutation 权限的 CI，不使用 credential。
- 不以删除 private historical provenance 来换取“grep 为零”。

## 默认执行配置与拓扑

- 工作目录：`/Users/xiaomei/Documents/projects/sge-governance-skill`；执行前重新确认 branch、HEAD、dirty/untracked inventory 与现有用户改动。
- 本轮显式授权 Codex 按需使用 subagents / delegation / parallel agent work；是否启用由 Multi-Agent Activation Gate 决定。
- 每个 non-trivial lane 在 delegation 前创建并验证 `lane_task_card_v1`，使用 renderer 生成 prompt，接收端先运行 `--expected-card-sha256` 校验；相邻 lane 运行 duplication audit。
- 默认 lanes：Design → Builder → independent Validation → Closure；identity/provenance/release 变更触发独立 Semantic Reviewer。Orchestrator 保持 control-plane，不接管用户要求的独立可见 Codex UAT 或 dominant Builder；任何 topology 例外都作为 Scope Delta 取得人类批准并留证。
- 首轮 Validation 建立 full baseline；修复轮使用 Validation State Snapshot + Delta Read Set；命中 user/Goal/governance/AC/authority/claim/truth/topology/final-diff trigger 时 rebaseline。
- 所有外部 side effect 默认关闭；S-028 只能消费 C2 对具体 payload 的可定位授权。

## ERBE 适用性与冻结要求

`ERBE applicability=required`。理由：本 Goal 会改变 identity predicate、public/private authority routing、provenance locator contract、rights approval gate、candidate→approved→published transition 和远端写入边界。

S-023 dominant Builder 前必须冻结 machine-readable Contract/Cases，至少包含：

- state axes：`candidate_built`、`locally_validated`、`rights_approved`、`release_authorized`、`remote_mutation_succeeded`、`remote_readback_verified`、`production_ready`；各轴不可互替。
- identities：private source revision、manifest revision、candidate/tree digest、public repo owner/URL/default branch、commit、tag、asset checksum。
- predicates：10 个 GAP-MH 的 pass/fail/blocked 判定、human authority owner、write exclusions、claim ceiling。
- negative cases：identity role collapse、说明进入 bash block、虚假 core coverage、private Dashboard locator 暴露、SP-041 作为默认产品语义、deny token 被误删、rights 字段冒充批准、CI token 冒充授权、本地 tag 冒充远端 release、remote asset checksum 不匹配。
- trusted RED：Contract/Cases 有效、执行环境正常，且指定行为按冻结 failure fingerprint 失败；import/path/fixture/network 错误只能是 `error`。
- GREEN：必须复用 frozen case identity，由独立 Validation 从 durable inputs 重算；Builder 不得改 expected/RED evidence/claim ceiling。任何改动走 Contract Patch + Scope Delta + re-RED。

## Session DAG 与逐段交付

### S-023：现状重基线、合同与裁决冻结

目标：把 Panorama 的旧快照与当前 checkout 对齐，冻结 10 项 finding contract、identity role matrix、provenance locator 选择、ERBE Contract/Cases 和 Original Plan ledger。

必须输出：Design Handoff、ERBE Contract/Cases、current-state finding matrix、public/private identity matrix、provenance locator decision proposal、Scope Delta registry（初始应为空）、Validation focus。

退出条件：10 项 finding 都有当前 evidence 与可执行 predicate；F-P0 不再被简化为“所有地方统一一个名称”，而是明确 private source=`sge-governance-skill`、public repo/project=`bm-sge-governance`、Skill=`sge-governed-checkpoints`、candidate identity 的独立角色；pre-Builder Semantic Review 同时给出 `Design Freeze Validity` 与 `Implementation Entry Readiness`。

Claim ceiling：只允许 `contract_frozen_for_implementation`；不得声称任何 finding 已修复。

### S-024：active/public 修复与防回归门禁

目标：一次落地身份一致性、Quick Start code fence、公共 provenance locator、SP-041 中立化，以及 Semx deny/history 隔离的代码/文档/测试闭环。

必须输出：最小代码/文档修订；identity/locator/residue/copy-paste deterministic gates；公共 candidate 重导出与 exact diff；必要的 KB JSON stable delta 及 deterministic Markdown render；BDD sync 判定。

退出条件：GAP-MH-01/02/07/08 的冻结正负例通过；GAP-MH-09/10 的保留/隔离负例通过；公共树不存在 Semx product authority、private Dashboard relative locator、SP-041 默认耦合或无法复制的 shell block。

Claim ceiling：`active_public_repairs_test_bound`；不证明全部 core、完整 Codex UAT、rights 或 release。

### S-025：消费仓 core capability matrix

目标：在 fresh public projection/consumer repo 中逐项验证 manifest 的 17 个 core 文件和 8 个 scripts，区分 executable entrypoint、library、schema、reference 与明确 N/A。

必须输出：逐文件/逐入口 capability matrix；每个 CLI 的 `--help` 与至少一个成功或按合同 fail-closed 的 smoke；library/schema/reference 的加载或结构检查；失败 transcript；独立 Validation。

退出条件：GAP-MH-04 每一行均有 observable predicate 和 durable evidence；0 tests、未执行、仅存在文件、仅 import 成功均不得写成 end-to-end capability pass。

Claim ceiling：`declared_core_matrix_validated_on_frozen_consumer`；不推广到所有平台/仓库。

### S-026：独立可见 clean-room Codex newcomer UAT

目标：让一个未继承本仓上下文的独立、用户可见 Codex task 在 fresh target 中，从公开入口完成 Skill discovery、最小 Goal、一个 Session、Validation Handoff、独立 Validation 与中文 closeout。

必须输出：真实 task/thread ID、worktree/target path、source/candidate fingerprint、逐步命令与用户输入、预期/实际文件清单、成功与负例 transcript、UAT verdict、未覆盖限制。

退出条件：GAP-MH-02 的 copy/paste 路径和 GAP-MH-03 的完整交互路径均被独立 reviewer 检查；主线程代做、仅提供 prompt、仅跑 CLI 或只看最终文件均不算 UAT 完成。

Claim ceiling：`one_frozen_clean_room_codex_flow_passed`；不证明通用 newcomer readiness 或所有 Codex 版本。

### S-027：最终 release candidate、rights 与发布包预检

目标：在无远端 mutation 下冻结 exact candidate，并生成供人类判断的逐文件 rights packet 和完整 release packet。

必须输出：source/manifest/tool/candidate/tree digest；owner/URL/default branch/version/tag/payload proposal；exact manifest；`SHA256SUMS`；license/NOTICE/copyright report；逐文件 rights confirmation 表；release notes；CI workflow candidate；rollback/revocation/read-back plan；未确认 blocker。

退出条件：所有自动检查和独立 Validation 通过；rights 状态仍为 `pending_human_confirmation`；任何不确定、冲突、unknown file、dirty source、digest drift 或 license 缺口都 fail closed。

Claim ceiling：`release_candidate_preflight_complete`；不允许 `rights_approved`、`release_authorized`、`published`。

### C2：人类 rights 与远端发布授权 checkpoint

这是必须暂停的 authority checkpoint。一次性向 repo owner 展示并请求决定：

1. 是否对冻结的每个 allowlisted 文件确认再分发 rights；
2. 是否批准具体 GitHub owner/repo URL/default branch；
3. 是否批准具体 source revision、candidate tree、version/tag、release assets、CI 与 mutation commands；
4. 是否批准 S-028 执行 push/tag/release/remote read-back，以及授权有效期/撤销条件。

推荐：只有逐文件无冲突、candidate fingerprint 与待执行 payload 完全一致、独立预检无 blocker 时才批准。未决定时状态为 `blocked_pending_human_authority`；拒绝则记录 `release_not_authorized`，Goal 不能宣称完成。人类批准后自动恢复 S-028，不再要求额外“继续”。

### S-028：授权范围内的远端发布与 read-back

目标：严格按 C2 的具体 payload 更新 `bm-sge-governance`，运行公开 CI，并从远端独立读取 commit/tree/tag/assets/checksum/release notes。

必须输出：授权 record；实际 commands；remote URLs/IDs；CI result；commit/tree/tag/assets identity；checksum verification；release read-back；任何偏差及撤销/修复动作。

退出条件：实际远端状态与授权 payload/本地 frozen candidate 一致，public CI 通过，assets checksum 可从远端重算；若 mutation 部分成功、身份漂移或 read-back 失败，状态为 `partial_remote_mutation` 或 `blocked`，必须按预案恢复或发布修复版本，不得伪写成功。

Claim ceiling：允许 `published_and_remote_readback_verified_for_exact_release`；仍不允许 `production_ready` 或普遍适用。

### S-029：全量独立终态验证、全景更新与 Goal 收束

目标：从原始 10 项 finding、实际 final diff、公开远端状态和最终 KB/Dashboard 表面重新建立 full baseline，完成 Final Validation、final Semantic Review、OPCM、中文 closeout、registry/DKG（仅在受影响时）和 post-closeout reconciliation。

必须输出：10 行 evidence-complete OPCM；Scope Delta audit；Final Validation Review；Semantic Review；更新后的 Repository Capability Panorama 派生读模型；Closeout；独立 post-closeout reconciliation；KB/Dashboard Contract Delta Scan。

退出条件：不存在未登记 Scope Delta；10 项 finding 全部为 `landed`、`preserved_and_verified` 或经人类批准的 `not_applicable`；Final Validation 与 post-closeout reconciliation 对实际 closeout、最终 Dashboard/KB、最终 diff 和 remote read-back 给出唯一且无冲突的 passing verdict；registry、closeout-language、KB render、public/local doctor、tests、clean-room 与 remote checks 全部符合各自边界。

Claim ceiling：最多 `Goal complete for the exact published release and declared environments`；不扩展为 production readiness、所有平台或所有仓库适用。

## Acceptance Criteria 总表

| AC | 判定 |
| --- | --- |
| AC-01 Finding 完整性 | 10 个 GAP-MH 在 Final OPCM 中逐项有精确证据；不得以“Semx 清零”或“release done”合并替代 |
| AC-02 Identity | private source/public repo/Skill/candidate identities 各有明确角色；任何冲突触发 doctor/gate 非零 |
| AC-03 Docs copy/paste | 所有 shell fenced blocks 可逐块执行；自然语言不进入 shell；clean-room transcript 可定位 |
| AC-04 Codex UAT | 独立可见 task 完成冻结流程与 artifact inventory；仅 prompt/CLI 不合格 |
| AC-05 Core coverage | 17 core 文件与 8 scripts 逐项有 pass/fail/N/A rationale，无“文件存在=能力可用”替代 |
| AC-06 Provenance | public source locator 自包含可解析或被明确类型化为 external/private；不得暴露伪相对 Dashboard 链接 |
| AC-07 Semx/history | deny token 与私有历史被保留并隔离；公开无 Semx 产品 authority/依赖/本机路径 |
| AC-08 Rights | exact candidate 每个文件有可定位的人类确认；结构字段、MIT 文件或测试不能替代 |
| AC-09 Release packet | owner/URL/branch/version/tag/CI/checksums/license/release notes/rollback/read-back 全部冻结且绑定 candidate |
| AC-10 Remote truth | 获授权后实际远端 commit/tree/tag/assets/CI/checksum 与 payload 一致，并完成独立 read-back |
| AC-11 State separation | candidate/local validation/rights/authorization/mutation/read-back/production 各轴保持独立 |
| AC-12 Governed closeout | 原始目标、Scope Delta、独立 Validation/Semantic、中文 closeout、KB/Dashboard review、post-closeout reconciliation 全部完成 |

## Validation Handoff 合同

每个 Session closeout 的 `验证交接包` 必须包含：claimed scope、semantic change、non-goals、changed files、gates/tests、durable evidence、known risks、KB/Dashboard impact、Scope Delta、当前 state axes、`Closeout language verdict`。Validation Handoff 只是输入，不是 verdict。

Final Validation 必须：

- 先运行 `guardrail_checklist.py --mode validation-agent`，使用固定 read-mostly Validation Agent Prompt；
- 同时检查本 Goal 原始 10 项 must-have 与 landed artifacts，不得只检查 revised design；
- 首轮全量、后续 delta、终态 rebaseline；区分 Validation Reviewer、Adversarial Tester 与 Governance Architect finding；
- 验证真实 task topology、C2 authorization provenance、最终 remote read-back、KB/Dashboard truth split 和 final diff；
- 缺 mandatory evidence 时只能给 `blocked/partial`，不能给 `pass/done`。

## Semantic Reviewer 触发与重点

本 Goal 默认触发 Semantic Reviewer，至少在 S-023 pre-Builder 与 S-029 final-state 各一次，二者时序证据必须分别保留。重点检查：

- identity role 是否把 private source、public project、Skill 和 candidate 错压成同一个字符串；
- public provenance projection/policy 是否把 private Dashboard 变成公共 canonical truth，或让 witness/profile 承担 semantic law；
- rights 字段、CI token、GitHub 登录、test pass 是否被误读为人类授权；
- `released`、`published`、`verified`、`ready` 是否在 Dashboard 一行摘要中造成未来 Agent 误读；
- 最小安全切片、implementation ladder、negative space、至少三个 future-agent misuse scenarios 是否完整；
- `Design Freeze Validity` 与 `Implementation Entry Readiness` 两个 verdict 是否分别成立。

## SGC v1 与禁止折叠

每个 Session 与 Goal closeout 前按 SGC v1 检查 claim level、evidence layer、SI-1..SI-6。禁止：

- schema/manifest 字段替代 rights truth；producer 重算替代独立 Validation；
- local clean-room 替代 remote publication；CI green 替代授权；Git tag 替代 release asset/read-back；
- deny token 命中替代 Semx product dependency 判断；grep 零命中替代 provenance 合规；
- SP-003 有界完成替代本 Goal 的 10 项原始覆盖；一个 Session pass 替代 Goal completion；
- `candidate_not_approved`、`rights_approved`、`release_authorized`、`published`、`production_ready` 相互折叠。

## Scope Delta 规则

- 删除、合并、改名、降级、延期任一 GAP-MH，改变 public/private authority，取消独立可见 Codex UAT，主线程接管要求独立的 Builder/UAT，或把真实 remote release 改成仅生成 packet，均为 Scope Delta。
- 每个 delta 必须记录 original requirement、reason、replacement、impact、human approval required/status/reference、deferred Session 与 completion impact。
- 未获人类批准的 material delta 不得进入 completion baseline。人类拒绝发布不是“自动缩窄后完成”；应记录 `release_not_authorized` 并使 full Goal 保持 blocked/partial。

## Continuous execution contract

本 Goal 默认连续执行整个 Session DAG。任何单个 Session、lane、closeout 或 post-closeout pass 都不是停止条件。每个 Session closeout 后必须记录：`goal_terminal`、`next_session`、`next_session_ready`、`human_decision_required`。

当 `goal_terminal=false`、`next_session_ready=true`、`human_decision_required=false` 时，禁止发送 final answer 或“如果需要我可以继续”，必须直接进入下一 Session。只有以下情况允许暂停：Goal completion；用户显式停止；C2 或新的真实 human-authority/destructive decision；明示资源阈值；网络/工具中断；同一恢复条件连续失败超过三次。普通 gate/test failure、card/digest drift、可重建 baseline 或尚未创建下一 Session artifact 均由 Orchestrator 在原 scope 内修复后继续。

C2 人类决定返回后自动恢复 S-028，不再要求额外“继续”。Context compaction 或 task resume 后，从本 Goal、Dashboard rows 和最近 closeout/reconciliation 恢复 continuation state，进入第一个 unfinished 且 ready 的 Session。

## Completion Rule

只有以下条件全部满足，才允许写 `SP-004 Goal complete`：

1. GAP-MH-01..10 逐项满足 AC，或有明确人类批准的 not-applicable Scope Delta；
2. S-023 frozen Contract/Cases 的相同 case identity 完成可信 RED/GREEN 和独立重算；
3. S-024 active/public 修复、S-025 core matrix、S-026 独立 Codex UAT、S-027 final candidate/release packet 均有 durable evidence；
4. C2 对 exact candidate 与 exact remote payload 的逐文件 rights 和发布授权可定位；
5. S-028 的远端 mutation、CI 与 read-back 实际完成并与授权 payload 一致；
6. S-029 Final Validation、final Semantic Review、Evidence-complete OPCM、中文 closeout 和独立 post-closeout reconciliation 对最终状态给出唯一无冲突的 passing verdict；
7. KB stable truth、Dashboard execution memory、public repo、candidate/release/production state axes 均无权威污染或 overclaim。

若 C2 未批准或 S-028 不能执行，允许收束状态只能是 `blocked_pending_human_authority`、`release_not_authorized`、`partial` 或具体 failure；不能把本地 candidate/release packet 写成 Goal complete。

## KB/Dashboard 与 Contract Delta Scan

- `kb/`：identity roles、public provenance locator policy、rights/release state law 或 reusable acceptance rule 若发生批准的稳定变化，提取最小稳定子集到 JSON truth，并确定性重渲染 Markdown；不得复制整个 closeout/Panorama。
- `Dashboard/`：注册后记录 SP-004、S-023..S-029、blocker、C2 decision、lane/task topology、candidate/release IDs、Validation/Semantic verdict、closeout 与 next-session state。
- public candidate/repo：只承载 allowlisted public content、public-facing provenance projection/policy、CI/release assets；不得承载 private Dashboard/Agent Logs/closeout。
- 每个 approved artifact 做 Contract Delta Scan，分类为 `promote-to-KB`、`Dashboard-only`、`gate-docs later`、`runtime/tests later` 或 `deferred session`。
- 如本提案获准登记，创建/更新 registry 表面后必须运行 `session_registry.py reconcile --repo . --check` 与 `validate --repo .`；只有可重建派生漂移且无 error 时才可 `--apply`，随后重跑两项检查。只有影响 DKG 时才显式重建 DKG。

## 允许与禁止的收束措辞

### 当前提案阶段允许

“已形成覆盖 Panorama 10 项 Finding 的 SP-004 Loop Goal 提案；它尚未登记或执行，不证明任何缺口已关闭，也不授予 rights 或远端发布权限。”

### 执行中的有界措辞

- “identity/Quick Start/provenance/pilot-id 修复在冻结测试范围内通过。”
- “一个 frozen clean-room consumer/Codex flow 通过独立 UAT。”
- “release candidate preflight 完成，等待 exact rights/release authorization。”
- “exact release 已发布并由 remote read-back 验证”，仅在 S-028 实际证据存在时使用。

### 禁止

- 在 C2/S-028 前写 `rights approved`、`published`、`release complete`、公开仓已同步或远端验证通过；
- 把 public doctor/tests/manifest/license 文件写成再分发权批准；
- 把一次 macOS/Codex UAT 写成跨平台、所有 Codex 版本、所有 repo 或 production-ready；
- 把保留的 deny token/历史 provenance 称为 Semx 产品依赖，或为了“零残留”删除应保留的审计线索；
- 在 Final Validation 与 post-closeout reconciliation 之前写 `SP-004 Done`、`Goal complete` 或等价最终完成。

## 提案审批后的第一步

若人类批准本 Goal，先将 SP-004 与 S-023..S-029 正式登记到 Dashboard，运行 registry gate，创建并验证 S-023 Design/ERBE/Semantic lane cards，再开始任何 Builder 修改。若人类只批准 Goal 设计、不批准登记或执行，则保持 `proposed_for_human_review`，不得自行启动。
