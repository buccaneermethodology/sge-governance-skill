# S-001 规划落库设计复核

## 设计结论

`有条件通过`：当前 Goal、Plan、Context 与 Dashboard 主行整体保持原始范围；本设计只支持完成 S-001 规划落库，不实施治理迁移，不启动 S-002，也不批准 SP-001 或产品完成。权威来源为 [Loop Goal](SP001_SGEGovernanceMigration_LoopGoal.md)、[迁移计划](SP001_SGEGovernanceMigration_Plan.md) 与 [Context](SP001_SGEGovernanceMigration_ContextBootstrap.json)。原始产品设计必须保持字节不变。

## 状态边界

- 关闭前：S-001=`Doing`；SP-001、BI-001=`To do`；S-002 只是用户明确启动 SP-001 后的下一入口。
- 关闭后：仅 S-001 可变为 `Done`；SP-001、BI-001 仍为 `To do`，并继续写明“迁移未启动”。
- Closeout 不得使用“治理已迁移”“Goal complete”“产品可用”等措辞。

## 阻断项

1. `Dashboard/Decisions.md` 使用 `Resolved`，不符合 [Dashboard Rules](../../Rules.md) 规定的四态 Status；关闭前须人工修正或提供合法字段解释。
2. `archive_manifest.json` 仍声称由 `S-485` 创建并引用 semx-cli 历史源，不能作为 S-001 当前 registry provenance；须人工修正，禁止用 reconcile 猜测。
3. `Session_Index.md` 指向 `Sessions.md#sp-001-s-xxx`，但当前 Session 表没有对应锚点；须确保定位链接真实可用。
4. `S001-AC-01..03` 在已读 Goal/Plan/Context 中没有可观察判定正文；独立 Validation 前须给出权威定义与逐项证据。
5. Closeout、独立 Validation Review、最终 Dashboard 状态与最终 diff 尚未形成，因此当前不得关闭 S-001。

## Builder 与关闭交接

Builder/Closure 只修复上述 S-001 控制面，生成中文 closeout，并运行 registry check/validate 与 closeout-language；不得迁入 Skill、KB truth 或 runtime。任何偏离须在 closeout 记录 Design Delta。

## Validation focus

独立 Validation 必须核对：种子 commit 与原始设计摘要；MH-01、MH-07、MH-09、MH-10 及 S001-AC-01..03；BI/SP/Session/Current State/Index/manifest 一致性；card/lane 时序；registry 与语言门禁；实际 closeout、最终 tracked/untracked diff；且明确结论只证明 S-001 规划落库。
