# SP-001 Strategy 来源扩展 Goal Patch

## Patch 身份

- Base Goal：`SP-001 audio-transcriptor 可复用 SGE Governance 迁移 Loop Goal`
- Base revision：Git `8c7d6aa`
- Patch ID：`SP001-GP-001`
- Sequence：`1`
- 人类 authority：用户于 2026-09-01 明确要求逐一审阅 semx-cli `semx-kb/docs/strategy/`，过滤 Semx 特定内容，并把可通用内容补入 SP-001。

## Replacement

1. 新增 `MH-11`：56 个 strategy 表面逐文件审计、canonical JSON mapping、通用 truth 重新冻结与 Semx/runtime 排除证据。
2. S-002 增加完整 strategy source manifest 与 docs→canonical mapping。
3. S-003 增加经重新冻结的通用 strategy contracts/read models。
4. S-004 增加逐文件删除/替代与身份清除。
5. S-005 增加 56/56 coverage、provenance、authority split 和 forbidden-collapse 验收。
6. S-006 的 OPCM、Scope Delta 与 final reconciliation 必须吸收 MH-11。
7. Completion Rule 从 `MH-01..MH-10` 更新为 `MH-01..MH-11`。

## Scope impact

- 类型：`approved scope expansion`，中文含义是增加来源审计与迁移质量要求。
- 删除/降级：无。
- 产品非目标：不变；仍不实现音频转写，不迁移 Semx Runtime 产品能力。
- 当前执行边界：只把扩展落库；SP-001 仍为 `To do`，S-002 未启动。
- 冲突：无。若未来 S-002 发现某候选不适用，可降为 `reference_only/remove`；若要删除 MH-11 或降低 56/56 验收，必须取得新的人类 Scope Delta 批准。

## 解析结果

Resolved Final Goal 由 [Final Loop Goal](SP001_SGEGovernanceMigration_LoopGoal.md) 与本 Patch 共同追踪；Final Goal 正文已吸收 replacement，Builder 不得只消费本 Patch 猜测完整 authority。

