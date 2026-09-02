# 仓库质量全景审计报告

## 关键结论中文展开

当前结论为 `repository_consistency=fail` 与 `public_candidate=blocked`。中文含义是：核心 `sge-governed-checkpoints` 的有界 portability test 可以通过，但当前整个仓库仍存在 registry 漂移、无效 lane card、active canonical 断链、历史证据腐化和公共发布合同缺失，不能据此声明 SP-001 完成，也不能把仓库原样视为可开源候选。

这不是说历史工作全部无效。S-001..S-006 的大部分有界 artifacts 仍可定位，S-012 的 genericity test 也真实通过；但这些证据的强度分别停留在历史有界收束或 `test_bound`，不能覆盖当前 Stage Plan 的 completion rule、公共发布、许可证、default-deny export 或新手验收。

## 全景图与数据

- [可筛选 HTML 全景](RepositoryQualityPanorama.html)：离线单文件，包含 Overview、Big Idea、Stage Plan、Session、Source views，关键词/字段筛选、排序、分页、URL hash 状态和详情抽屉。
- [全景 Markdown](RepositoryQualityPanorama.md)：便于 Git review 的主要阅读面。
- [全景 JSON](RepositoryQualityPanorama_Data.json)：保存 3 个 Big Idea/审计分组、2 个 Stage Plan、22 个 Session/Knowledge 条目、source manifest 与冲突。
- [生成器](RepositoryQualityPanorama_Generator.py)：从当前 Dashboard/KB/Skill/tests/Git 表面重建 JSON 与 Markdown；HTML 使用用户指定 Skill 的 renderer 生成。

全景是派生读模型，不是 `kb/` canonical truth、Dashboard status authority、批准凭据或 SP-001 完成证据。

## P0 阻断项

### 1. SP-001 当前没有完成

[Stage Plans](../Stage_Plans.md)把 SP-001 标为 `Doing`，Current Entry 为 S-012；[Sessions](../Sessions.md)把 S-012 标为 `Doing`；[Current State](../Current_State.md)明确要求 S-012 独立 Validation 与 post-closeout 完成前不得关闭 SP-001。与此同时，[Big Ideas](../Big_Ideas.md)仍保留 `BI-001=Done` 和“SP-001 历史迁移已完成”的旧父面文字，形成状态冲突。

允许的最大结论：S-001..S-006 有历史有界证据，S-012 portability test 通过；SP-001 必须保持 `Doing`。

### 2. Session registry 当前失败

`python3 Dashboard/tools/session_registry.py reconcile --repo . --check` 返回 `drift`；`validate --repo .` 返回 `projection_drift`。漂移目标是 [Session Index](../Session_Index.md)和 [archive manifest](../Archives/Sessions/archive_manifest.json)：manifest 仍记录 11 条/5 条 current、`S-485` 和 Semx 绝对源路径，而当前权威表面是 12 条/6 条 current/6 条 archived。

本轮是 review，没有运行 `reconcile --apply`；修复后必须重跑相同 check/validate。

### 3. S-012 执行合同无效且终态证据缺失

[S-012 Context](SP001_S012_Genericity_ContextBootstrap.json)结构校验通过，[genericity test](../../tests/contract/sge_skill_generality.py)直接运行通过；但 [S-012 Lane Task Card](SP001_S012_Genericity_LaneTaskCard.json)的 `base_context_refs[0].sha256` 仍为 `PENDING`，机器校验失败。当前也没有 S-012 Design、独立 Validation Review、中文 closeout 或 post-closeout reconciliation。

这意味着 portability test 只支持 `test_bound` 主张，不能替代 Builder 前有效 card、独立 Validation 或完成证据。

### 4. active canonical authority/依赖断链

- [AGENTS](../../AGENTS.md)指向不存在的 `kb/data/strategy/strategy_human_ai_development.json`。
- active canonical [SGC JSON](../../kb/data/strategy/strategy_sgc_structural_contract_v1.json)把不存在的 `Strategy_Human_AI_Development.md` 列入 `source_scope`，并依赖不存在的对应 doc ID。
- 同一 `source_scope` 还列出不存在的 `contract/SGC_v1.md`、S247 closeout、Semantic Surface Strategy 与 KB Promotion Strategy。

专项判定：`Strategy_Human_AI_Development.md` 不是仅仅“文件名曾出现在历史 inventory”。它仍参与 active hard gate 和 canonical contract 的 authority 路由，因此必须补齐经批准的真实 canonical carrier，或把引用改到现有、确实落地的 contract/mapping；不能用“如已迁移”掩盖依赖不完整。

### 5. 当前仓库不是公共发布候选

仓库没有 LICENSE/NOTICE，也没有 public export manifest/default-deny allowlist。[SP-002/S-007](../Sessions.md)仍为 `To do`，而 [README](../../README.md)也明确公共发布须另行验证和授权。

公共边界扫描还发现：11 个文件共 15 处个人绝对路径；archive manifest 的 Semx 路径与 `S-485` 属 active registry surface；`.gitignore` 仍含 `.semx/`；workflow registry 的 disabled extension 说明仍写“音频项目治理核心”；`session_registry.py` 仍保留不可从当前 CLI 调用的 legacy `migrate()`/`migrate_references()` 代码。`S-384` 精确命中为 0。

多数 Semx/KYM/TCO/P00-P17 命中位于历史 provenance，不是 runtime authority；但如果整仓直接公开，它们仍会进入分发物并暴露迁移史/本机路径。因此未来公共投影必须 default-deny，而不是假设“历史文件不会被看到”。

## SP-001 逐 Session 证据矩阵

| Session | 当前登记 | 已落地 artifacts | 当前差距 | 最大可支持结论 |
| --- | --- | --- | --- | --- |
| S-001 | archived `Done` | Goal、Plan、Context、closeout、Validation、post-closeout 均存在 | 多处链接指向已删除的 audio-transcriptor design | 历史“规划落库完成”有界成立；不证明当前设计文件存在 |
| S-002 | archived `Done` | provenance、ledger、profile/schema、ERBE、Design、Semantic、closeout、Validation 存在 | Semantic Review 链接已删除 ERBE runner | 历史 repo-local core/ERBE 有界验收；当前不可完整复跑 |
| S-003 | archived `Done` | Context、card、Design、closeout、Validation、post-closeout 存在 | post-closeout 指向已归档 Session 的旧 current anchor；无独立 OPCM/Scope Delta 面 | 历史 tooling 技术切片有界验收 |
| S-004 | archived `Done` | Context、card、cleanup record、closeout、Validation 存在 | 无 post-closeout final-state reconciliation；Validation 未覆盖随后 closeout；无 OPCM/Scope Delta | 只能支持清理候选/关闭前验证，不能按当前硬门重证终态 Done |
| S-005 | archived `Done` | Context、card、Integration Validation、Semantic Review 存在 | 无专属 closeout/post-closeout；source manifest 链接错误；把 Review 当 closeout 时语言门失败 | 支持历史“可进入 S-006”的集成审查，不支持独立终态完成 |
| S-006 | archived `Done` | Context、card、OPCM、closeout、post-closeout 存在 | OPCM 不满足当前完整字段要求；source manifest 链接错误；completion 已被 S-012 supersede | 仅支持 S-012 出现前的历史有界收束 |
| S-012 | current `Doing` | Context、card 文件、genericity test 存在 | card digest=`PENDING`；缺 Design、独立 Validation、中文 closeout、post-closeout；Artifacts Index 未登记 | 只支持 genericity test 的 `test_bound` 通过 |

## 引用与可执行性问题

### 当前高优先断链

- [S-005 Validation](SP001_S005_IntegrationValidation_ValidationReview.md)和 [S-006 OPCM](SP001_S006_GoalClosure_OPCM.md)的 source manifest 相对链接少一层 `../`。
- [S-002 Semantic Review](SP001_S002_PreBuilderSemanticReview.md)链接已删除的 `Dashboard/tools/sge/s002_erbe_acceptance.py`。
- 另有 14 个历史 Markdown 链接指向已删除的 `kb/bm-doc/audio-transcriptor-skill_design_v1.0.md`。这些可以改为明确的历史 tombstone/provenance 说明，但当前不能当可点击证据入口。
- [KB README](../../kb/README.md)列出不存在的 `kb/tools/glossary_v21_validator.py`。

### 工具链不一致

- [KB renderer](../../kb/tools/render_kb.py)没有 `--check` 模式；在临时副本上对当前 6 个 KB JSON 全量运行时，因 5 个配置/合同 JSON 不符合其 doc schema 而失败。因此“JSON→Markdown”当前不是可重跑的全 KB 闭环。
- [Dashboard KG generator](../tools/generate_dashboard_kg.py)实跑因缺 `Dashboard/Quality_Metrics.md` 抛出 `FileNotFoundError`。
- 42 个 tracked JSON 可解析；13 个 Python 源在外置 pycache 下可编译；`git diff --check` 通过；genericity direct test 通过。
- 标准测试入口不足：当前只有一个直接执行脚本；`unittest discover` 返回 0 tests 后成功，存在“假绿”风险；当前环境没有可依赖的 pytest 入口证据。

## SGC v1 证据边界

- 全景 JSON/HTML 结构：`structurally_supported`，只证明派生图可生成和读取。
- genericity portability：`test_bound`，只证明当前脚本中的 demo-consumer 路径通过。
- SP-001 completion：`blocked`，缺少有效 S-012 contract、registry、final-state Validation 和 closeout evidence，违反 SI-5/SI-6，且存在 false closure 风险。
- public release readiness：`blocked`，缺 license/provenance contract、default-deny export、clean-room newcomer UAT 和发布授权。

## 改进顺序

1. `P0` 完成 S-012 的有效 card/Design/独立 Validation/中文 closeout/post-closeout，并修复 registry drift；在此之前保持 SP-001 `Doing`。
2. `P0` 修复 active canonical 断链：Human-AI strategy carrier、SGC dependencies、S-005/S-006 relative links、DKG/KB renderer 可执行入口。
3. `P0` 启动 SP-002/S-007 前冻结 LICENSE/NOTICE、public/private allowlist、provenance 和 default-deny export manifest；对最终包而非源仓重跑身份/绝对路径扫描。
4. `P1` 对历史 provenance 使用 tombstone/relocation manifest 或非公开 archive bundle，避免证据链接腐化和个人路径泄露。
5. `P1` 建立统一 `doctor`/test entry：JSON parse、Python compile、profile/genericity、registry、KB render check、DKG generate、Markdown/JSON references；必须 fail on zero tests。
6. `P1` 修复 BI/SP/Session 父面状态，清理 `.semx/`、音频项目措辞和 dead migrate definitions；保留必要 negative controls 时注明其测试目的。

## 验证交接包

- 原始目标：生成可筛选全景，并审计公共残留、SP-001 artifacts、缺失引用及其他质量问题。
- 实际变更：仅新增 `RepositoryQualityPanorama_*` 派生全景、任务合同、lane cards/prompts/audit 和本报告；未修复被审计仓库状态。
- 独立审计来源：公共残留 lane（Cicero）、SP-001 evidence lane（Sagan）、引用/一致性 lane（Boole）。三者均为 read-only。
- 运行证据：HTML/embedded JSON 检查通过；genericity direct test 通过；JSON parse/Python compile/diff check 通过；registry、S-012 card、DKG、KB full render 失败并已如实列为 findings。
- KB/Dashboard 复核：没有批准新稳定 truth，因此不更新 `kb/`；本任务只增加 Dashboard 派生读模型与审计证据，不改变 Session 状态。
- BDD 判定：未修改 maintained runtime/schema/acceptance gate，无 BDD 文件更新。
- Semantic 判定：未批准新语义，独立 Semantic Reviewer 不适用；发现的 S2/S6 风险分别记录为引用漂移与 authority confusion。
- `Closeout language verdict`：`pass`，中文含义是本报告的中文标题、英文状态解释和可点击证据入口满足 reader-facing 语言门；它不改变任何仓库质量 finding，也不证明 SP-001 或公共发布就绪。

## 明确非目标

- 本轮不运行 `reconcile --apply`、不修复断链、不改 SP-001/S-012 状态。
- 不删除历史 provenance，不决定公共包应包含哪些历史 artifacts。
- 不创建 LICENSE、不发布、不推送、不写全局 Skill。
