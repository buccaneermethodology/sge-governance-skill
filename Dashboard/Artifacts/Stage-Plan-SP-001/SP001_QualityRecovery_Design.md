# SP-001 仓库质量恢复设计

## 任务解释

本设计把上一轮全景审计中的四类 finding 转成四个连续 Session。目标不是美化历史，而是让当前仓库的 active authority、canonical KB、引用图、验收入口和最终证据能够在一个独立公共候选仓库中自洽。

## 最小安全实现阶梯

1. `S-012`：先修执行合同、registry projection、active/public 身份残留和 legacy migrate 入口；历史 Archives 不删除。
2. `S-013`：从 semx-cli canonical JSON 只读抽取 Human-AI、Semantic Surface、KB Promotion 的通用稳定规则，重新定义 SGE owner/source/dependencies/claim ceiling，再由本仓库 renderer 生成 Markdown。
3. `S-014`：修复历史 locator 和 active 引用；让 KB renderer 支持 fail-closed `--check`，让 DKG 输入显式且可生成；建立 fail-on-zero-tests 的标准 doctor。
4. `S-015`：独立 Validation 与 Semantic Reviewer 覆盖实际 closeout、最终 Dashboard/KB 和完整 diff；重建 OPCM 后才允许 parent state 收束。

## Authority Routing

```text
semx-cli canonical JSON (只读 provenance)
        ↓ 逐节裁决与去项目化
kb/data/strategy/*.json (本仓库 canonical truth)
        ↓ render_kb.py
kb/docs/strategy/*.md (确定性阅读面)

Dashboard/*.md + Artifacts (执行状态/证据)
        ↓ session_registry / DKG
Index、manifest、graph、HTML (派生读模型)
```

## 失败与非目标

- 缺 canonical source、无法去项目化或依赖产品 ontology 的 section：不迁移，并记录 rejection reason。
- 历史链接目标已经删除且无法恢复：不伪造内容；改为明确 tombstone/provenance locator，并限制历史主张。
- 公共 LICENSE/NOTICE/export manifest 属于 SP-002；本轮只修进入该阶段的前置质量，不创建发布主张。
- 不把 S-004/S-005 的旧 `Done` 追溯包装为当时满足今天的硬门；由 S-015 当前 final-state reconciliation 吸收 evidence gap。

## Future-Agent Misuse 场景

- 只看到 `Done` 就推断已公开发布：由 release state 独立轴和禁止 collapse 阻断。
- 看到来源路径就把 Semx 当当前 authority：active/public scan 与 source-scope 重写阻断。
- 运行 `unittest discover` 得到 0 测试仍声称绿色：doctor 以 `zero_tests_discovered` 失败。
- 手改派生 Index/manifest 伪造一致性：registry check/validate 从 canonical Session rows 重算。

## Design Freeze Verdict

- ERBE applicability：`required`。
- frozen contract：[SP001_QualityRecovery_ERBE_Contract.json](SP001_QualityRecovery_ERBE_Contract.json)。
- frozen cases：[SP001_QualityRecovery_ERBE_Cases.json](SP001_QualityRecovery_ERBE_Cases.json)。
- Builder write exclusion：semx-cli 来源、远端、全局 Skills、历史 commits。

