# S-017 本地确定性投影合同

## 目标

本合同只覆盖 maintainer 从一个 fresh source root 生成本地 public projection candidate：读取 `public_export_manifest_v1.json` 的逐文件 exact allowlist，默认拒绝未知内容，并在写入前检查路径、对象类型、私有残留和 Git/source 状态。

## 可观察行为

- source root 必须是目录且不能是 symlink；manifest path 只能是规范化的相对 POSIX 文件路径，拒绝绝对路径、盘符、`.`、`..`、空段和反斜杠。
- 在 private canonical worktree 中，未列入 allowlist 的执行面可以被 inventory 后省略；在 fresh staging/source root 中，任何未列入 allowlist 的 regular file 都必须返回 `unknown_path_default_deny`，不能静默接受。这一区分保持 default-deny 与私有执行面隔离。
- allowlisted 文件必须是 regular file；source tree 中发现 symlink、gitlink、nested repository、LFS pointer、unexpected binary、绝对本机路径或 credential residue 时 fail closed。
- destination 必须是 fresh/empty directory或尚不存在的目录；destination 本身及最近存在的父目录不能是 symlink。正常系统路径别名（例如 macOS `/var`）不被误判为用户可控 redirect。
- 输出文件集合严格等于 allowlist；`EXPORT_METADATA.json` 只记录本地候选身份、逐文件 bytes/sha256、`file_set_sha256`、`tree_sha256` 与完整 inventory 统计。
- `verify` 从 source 和 destination 重新计算 exact file set 与 digest；未知文件、缺失文件、digest drift、destination symlink 或特殊对象均失败。

## S-017 可定位验收定义

| ID | 可观察 predicate | 证据与 owner |
| --- | --- | --- |
| S017-AC-01 | 对 fresh source root 执行 export 时，allowlist 外 regular file 返回 `unknown_path_default_deny`，且 destination 不创建；allowlist 内文件集合可完整复制 | [tests/test_public_projection.py](../../tests/test_public_projection.py) 的 unknown source case；S-017 Builder/独立 Validation |
| S017-AC-02 | 对 fresh destination 执行 verify 时，file set、每文件 bytes/sha256 与 tree digest 与 source 一致；新增或篡改文件分别返回 `unknown_path_default_deny`/`projection_digest_drift` | [Projection Evidence](SP003_S017_ProjectionEvidence.json)；S-017 independent Validation |
| S017-AC-03 | symlink/path escape、private/absolute residue、binary/LFS/gitlink/nested repo、dirty source 和不安全 destination 均按唯一 failure fingerprint fail closed | [tests/test_public_candidate.py](../../tests/test_public_candidate.py)、[tests/test_public_projection.py](../../tests/test_public_projection.py)；S-017 independent Validation |

`PROC-03`（Validation Handoff predicate）：Validation 必须读取原始 Goal 与本合同、以同一 case identity 重算 C03/AC-01..03、记录 changed files 与最终 diff，并给出唯一 verdict；Builder/卡片/schema/test pass 不能替代该 verdict。该 predicate 的 durable witness 是 [S-017 Validation Review](SP003_S017_ValidationReview.md) 与其 snapshot。

## 保持的边界

`bootstrap`、`install`、`upgrade`、`uninstall` 的命令兼容性由 S-018 独立合同承接；S-017 不把 lifecycle 证据吞入 projection verdict。本切片不实现 license rights 授权、GitHub create/push/tag/release、remote read-back 或生产就绪。`candidate` 只表示本地 projection evidence，不表示批准或发布。

## 验收与证据

实现入口：[tools/sge_public.py](../../tools/sge_public.py)；focused 负例与回归：[tests/test_public_candidate.py](../../tests/test_public_candidate.py)、[tests/test_public_projection.py](../../tests/test_public_projection.py)。机器可重算结果见 [SP003_S017_ProjectionEvidence.json](SP003_S017_ProjectionEvidence.json)。

## 当前未实现与 bounded claim

`ODA-MH-02` 的本地 exact allowlist/residue/path safety slice 有实现和 focused test evidence；`ODA-MH-03` 仅实现 export/verify 的本地可重算部分，未实现 authorized public repo update、独立 Validation 或最终 diff/release pipeline。因此本 artifact 只能支持“受限 maintainer local deterministic projection candidate evidence”，不能支持 S-017 全 Session、SP-003、release 或 production 完成声明。

## BDD 影响

本轮只增加 Python unit/seam negative cases，没有修改 maintained non-unit gate、case catalog 或 BDD authority；因此未新增 BDD 文件。若后续将 projection validator 提升为 maintained non-unit gate，应在该 gate 变更同时同步对应 BDD readable card/case catalog。
