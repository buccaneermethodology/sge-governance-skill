# Exceptions

| ID | Topic | Scope | Purpose | Trigger | Escalation Path | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EX-001 | S-001 checkpoint bootstrap | 仅限 Git seed、Final Goal/Plan/Context 与 Dashboard entry 落库 | 解决仓库硬门要求 repo-local checkpoint、但迁移前该 Skill 尚不存在的启动悖论 | `.codex/skills/semx-governed-checkpoints/` 与 `sge-governed-checkpoints/` 均缺失 | 使用 semx-cli `main@19e967a` 固定源脚本验证；S-002 必须建立 repo-local Skill，之后本例外失效 | Done | 只表示 S-001 bootstrap 例外已按边界关闭，不表示 repo-local Skill 已迁入。外部源检查不得扩展到产品或 S-002 Builder。现有 `archive_manifest.json` 中的 Semx 源路径与 `created_by_session=S-485` 是待 S-004 移除或替代的 legacy 派生工具限制，只描述迁移前工具 provenance，不是 S-001 当前 registry provenance，也不得作为 S-001 完成证据；在 S-004 前手工改写该派生表面会造成 registry drift。 |
