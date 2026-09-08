# SGE Governance Dashboard

本目录是 SGE Governance Skill 的 execution memory：记录 Big Ideas、Stage Plans、Sessions、决定、风险、例外、验证和 closeout。它不是 canonical truth；稳定治理合同、术语和来源规则位于 `kb/`。

## 文件地图

- `Big_Ideas.md`：跨 Session 的长期主题。
- `Stage_Plans.md`：冻结批次范围和依赖。
- `Sessions.md`：可关闭的执行单元；完整历史在 `Archives/Sessions/`。
- `Decisions.md`、`Risks.md`、`Exceptions.md`：决策、风险与例外登记。
- `Artifacts/`：Context、合同、Validation、Semantic Review、closeout 等持久证据；根目录是定位面，具体文件按 owner 收束到 [Artifacts 批次索引](Artifacts/README.md) 下的 `Stage-Plan-SP-001`、`Stage-Plan-SP-002`、`Stage-Plan-SP-003` 或审计 Session 批次。
- `tools/`：registry、DKG 与 SGE 辅助工具。

## 使用顺序

1. 先读 `kb/` 的 canonical truth 和 `AGENTS.md` 的硬门。
2. 再读 `Stage_Plans.md`、`Decisions.md` 与当前 Session 行。
3. 修改 Session 或 Dashboard 表面后运行 `python3 Dashboard/tools/session_registry.py reconcile --repo . --check` 和 `validate`。
4. 完成 non-trivial 工作时保留中文 closeout、独立 Validation、必要的 Semantic Review 与 post-closeout reconciliation。

## 范围声明

当前仓库只维护 SGE Governance Skill，不实现任何具体产品、不写全局目录。KYM/TCO、历史 phase/runtime 与 `run-loop-goal-cycle` 仅作为排除或未来 optional extension，不是默认 authority。
