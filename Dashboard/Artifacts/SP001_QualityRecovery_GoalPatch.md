# SP-001 仓库质量恢复 Goal Patch

## Patch 身份

- Base Goal：`SP-001 audio-transcriptor 可复用 SGE Governance 迁移 Loop Goal`
- Base revision：Git `0aa532989372b9f0f709c832b318cbd9441c1a4c`
- Patch ID：`SP001-GP-002`
- Sequence：`2`
- 人类 authority：用户要求修复仓库审计发现的四类问题，必要时只读 semx-cli 的语义治理来源，并最终在当前硬门下将 SP-001 推进到 `Done`。

## 原始范围保留

本 Patch 不删除、降级或替换 MH-01..MH-11。历史 Goal 中的 audio-transcriptor/Semx 叙述只保留为迁移 provenance，不再作为当前仓库身份、canonical truth、公共候选内容或完成主张。

## 新增 Must-Have

| ID | 原始要求 | 可观察验收判定 | Owner / Lane | Claim ceiling |
| --- | --- | --- | --- | --- |
| MH-12 | 清除 active/public 表面的旧项目身份、绝对来源路径、legacy migrate 入口和 registry 漂移。 | active allowlist 扫描无未批准身份；registry check/validate 通过；历史 provenance 仍可定位。 | S-012 / Builder+Validation | 只证明定义扫描面内的 active 身份隔离。 |
| MH-13 | 恢复 Human-AI、Semantic Surface、KB Promotion 三类通用 semantic-governance canonical truth。 | canonical JSON 存在；来源逐节裁决；Markdown 由本仓库 renderer 确定性生成并 `--check` 通过。 | S-013 / Design+Builder+Semantic | 只证明去项目化后的 repo-local 策略合同，不证明来源项目事实。 |
| MH-14 | 修复缺失引用、历史证据 locator、KB renderer、DKG 和标准 doctor/acceptance 入口。 | 引用检查、KB check、DKG、非零测试发现、doctor 正负例通过。 | S-014 / Builder+Validation | 只证明当前仓库的结构与工具链验收。 |
| MH-15 | 用当前硬门重建 SP-001 全量 OPCM、Scope Delta、独立 Validation、Semantic Review、中文 closeout 与 post-closeout reconciliation。 | 每个 MH/AC 独立行或有可展开分组；最终 verdict 覆盖实际 closeout、Dashboard/KB 和完整 diff。 | S-015 / Validation+Semantic+Closure | 只有全部 completion predicates 同时满足才允许 `SP-001 Done`。 |

## Session DAG Replacement

历史 `S-001→S-006` 保留为已执行 provenance。当前恢复 DAG 固定为：

`S-012 active/public 与 registry 修复 → S-013 semantic-governance canonical 恢复 → S-014 引用与验收工具链修复 → S-015 最终集成与关闭`

Session closeout 不是停止点；下一 Session ready 且不需要人类决定时必须自动继续。

## Semx 来源边界

- 只读来源：`/Users/xiaomei/Documents/projects/semx-cli/semx-kb/data/strategy/`；对应 Markdown 只作阅读面。
- 允许：抽取与本仓库治理目标直接相关、可去项目化、可重新归属和可独立验证的稳定规则。
- 禁止：复制 Semx 名称、产品阶段、KYM/TCO、P00-P17、M1/P05/P06、provider/runtime/SAG ontology、历史 Session/closeout 身份或绝对本机路径进入 canonical truth。
- 新 canonical JSON 的 `owner`、`source_scope`、`depends_on_docs`、状态和 claim ceiling 必须重新冻结。

## ERBE 与 Claim Ceiling

- ERBE applicability：`required`，因为本 Patch 改变 authority routing、completion predicate、canonical strategy 和 acceptance/tooling 边界。
- Builder 不得修改冻结的 Contract/Cases、预期失败或 claim ceiling；变更必须走 Contract Patch + Scope Delta + re-RED。
- 最大完成主张：`SP-001 在当前仓库定义的 repo-local 结构、治理、引用和工具链验收范围内完成；不证明公共发布、普遍适用性、生产成熟性或任何来源产品能力。`

## Completion Rule Replacement

只有同时满足以下条件，才能将 SP-001 与 S-012..S-015 写为 `Done`：

1. MH-01..MH-15 均有与最终 diff 对齐的可点击证据；
2. registry `reconcile --check` 与 `validate` 通过；
3. canonical KB JSON 与派生 Markdown `--check` 通过；
4. DKG 可由显式输入确定性生成；
5. 标准 doctor 发现并执行非零测试，引用/身份/绝对路径扫描无未批准 finding；
6. S-004/S-005 的历史证据缺口通过当前 final-state reconciliation 显式吸收，不伪造历史时序；
7. 独立 Validation 与 Semantic Review 覆盖实际 closeout、最终 Dashboard/KB 和完整 diff；
8. closeout-language 通过，OPCM/Scope Delta/父面状态无冲突；
9. 不把候选、测试、验证、批准、Git、公共发布或生产状态折叠为同一事实。

## Scope Delta

- 类型：`user-approved repair expansion`。
- 删除或降级：无。
- 身份修正：当前仓库从历史产品迁移叙述收束为独立 `sge-governance-skill`；历史材料仍是 provenance。
- 不授权：发布、push、全局 Skill 写入、外部 provider 调用、删除不可恢复历史。

