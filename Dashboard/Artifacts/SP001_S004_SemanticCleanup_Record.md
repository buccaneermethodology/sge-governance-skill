# S-004 清理记录：Semx/KYM/TCO/runtime 历史排除

## 已删除

- `kb/docs-system/v1/` 下的 Semx 文档系统、M1/CLI/Phase DSL、旧 schema 与演进记录。
- `Dashboard/tools/visualization/` 下的 KYM/TCO 业务模型、provider 试验、覆盖提示词和生成器。
- Finder 元数据与生成的 Python 缓存，并加入 `.gitignore` 防止回流。

## 保留的通用替代

- truth/authority/claim ceiling：`kb/data/strategy/` 的 SGE profile、SGC、ERBE 与 workflow registry。
- 执行状态与证据：`Dashboard/`、`session_registry.py`、DKG 生成器。
- 领域扩展：`build-kym`、`build-tco-coverage` 仅在 profile 中标记为 optional，不作为默认 Skill 或样例数据。
- 高级编排：`run-loop-goal-cycle` 不原样迁入，延期至 SP-002 设计 `run-sge-loop-goal-cycle`。

## 语义边界

删除这些文件不表示通用治理原则被删除；可复用的不变量已在 SGE Skill、SGC/ERBE 与来源清单中抽取。删除也不表示 audio-transcriptor 产品 runtime 已实现或已验收。
