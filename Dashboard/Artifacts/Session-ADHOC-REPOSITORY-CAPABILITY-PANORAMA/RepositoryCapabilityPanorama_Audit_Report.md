# SGE Governance 仓库质量与开源缺口审计报告

## 关键结论中文展开

`repo_local_quality=pass_with_findings` 表示当前维护门禁和固定基线投影在其合同范围内通过，但有需要修复的发现；它不表示正式开源发布通过。`public_release=blocked` 表示缺少 public identity 一致性、rights authority、最终发布资产与远端 read-back，当前只能停在 `candidate_not_approved`。

## Read Manifest

已读：AGENTS、core Skill 与 references、README/中文指南、manifest、KB strategy、Dashboard Current State/Stage Plans/archives、tools、extensions、tests、两条独立只读审计结果和 Design artifact。未读项：不存在的远端 `bm-sge-governance`、未提供的 rights approval、未执行的完整 Codex newcomer UAT；这些均作为 evidence gap 保留。

## 实际运行的门禁

- source snapshot：生成于 `2026-09-05`；branch `sge/sp002`；完整 HEAD `55da8debbb48bd7c10ec6f37bce02b621ba6d610`；工作树 `tracked_changes=0; untracked_paths=33`。具体 tracked/untracked inventory 保存在[统一 JSON 数据](RepositoryCapabilityPanorama_Data.json)的 `source_identity.current_worktree`。
- `python3 Dashboard/tools/doctor.py --repo .`：`pass`；27 tests；170 JSON；24 Python；1248 refs；genericity/registry/KB/ERBE/DKG 均通过。该数字是本次生成时动态采集的 checkout 快照，不是写死基线。
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`：27/27 passed。
- `python3 tools/sge_public.py doctor`：`public_doctor:pass`。
- registry reconcile check/validate：22 archived / 0 current / no drift or collision。
- `python3 kb/tools/render_kb.py --check`：render-kb: check passed 7 manifest documents。
- clean clone 中 export/verify：48 files，tree digest 与既有 S-017 evidence 一致。
- 当前任务 checkout export：精确返回 `dirty_tree`；这是本任务未跟踪工件触发的安全阻断，不能描述成基线代码失败。

## Findings

| ID | 优先级 | 表面 | 裁决 | 阻断 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| F-P0-IDENTITY | P0 | public allowlist | active/public | 正式开源发布 | 裁决 source provenance 与 public identity，新增一致性 gate |
| F-P1-QUICKSTART | P1 | docs/Quick_Start_CN.md:3-15 | active/public | 小白可直接照做 | 把说明移出代码块并增加 copy/paste 测试 |
| F-P1-CODEX-UAT | P1 | docs/Beginner_Guide_CN.md | evidence_gap | 完整 newcomer-ready 主张 | 做独立可见 clean-room Codex UAT |
| F-P1-CORE-COVERAGE | P1 | installed core | evidence_gap | 完整 capability-ready 主张 | 补消费仓 capability matrix 与逐入口 smoke/UAT |
| F-P1-RIGHTS | P1 | release authority | authority_gap | push/tag/release | 对最终 candidate 做逐文件权利签署 |
| F-P1-RELEASE-ASSETS | P1 | repository | evidence_gap | 正式开源发布 | 完成 release packet、CI/read-back 与具体授权 |
| F-P2-PROVENANCE-LINKS | P2 | public KB | active/public | 自包含 provenance 可用性 | 生成 public provenance projection 或明确 external/private source locator policy |
| F-P2-PILOT-ID | P2 | context_efficiency_pilot.py | active/public | 项目中立 polish | 改为通用名称并保留历史 provenance 于私有层 |
| F-INFO-SEMX | INFO | public candidate | fixture/example | none | 保留负例意图并在发布审查中说明 |
| F-INFO-HISTORY | INFO | Dashboard/Archives 与 Artifacts | historical provenance | none | 继续保持 default-deny 隔离 |

## Semx 残留裁决

- active/public：没有 Semx 产品实现或 `semx-cli`/`semx-kb` 身份；唯一 `semx` 是 generic profile 的 forbidden token。
- historical provenance：Dashboard/Archives、closeout、Agent Logs 与迁移 inventories 中保留来源证据；它们被 manifest default-deny 排除。
- fixture/example：tests 中的 `semx-cli`、`/Users/alice/private` 等是期望被拒绝的负例，不是默认依赖。
- false positive：`/tmp` 是匿名临时目录示例；KYM/TCO 是默认关闭、entrypoint=null 的扩展接口名字，不是随仓产品实现。

因此，“没有 Semx 源仓残留”只能准确表述为：公开候选和默认 core 没有 Semx 产品依赖或个人绝对路径泄露；历史 provenance 仍有意保留在不公开 Dashboard 层，公开 profile 也保留 Semx deny token 作为防污染规则。

## 验证交接包

- claimed scope：能力全景、质量/残留审计、开源缺口、小白与维护者指南。
- semantic change：无；只生成派生读模型和证据化建议。
- non-goals：不修复 source/docs/KB，不提交、不发布、不执行远端动作。
- changed artifacts：仅 `Dashboard/Artifacts/Session-ADHOC-REPOSITORY-CAPABILITY-PANORAMA/RepositoryCapabilityPanorama_*`。
- evidence：本报告、Data JSON、Markdown、HTML、Generator、Design、两条只读 audit lane 与门禁输出。
- known risks：public identity、Quick Start、rights、完整 Codex UAT、core 全入口验证、public provenance links。
- KB/Dashboard impact：无 stable truth 变更；本任务仅写 Dashboard Artifact，不改 registry lifecycle。
- Closeout language verdict：待在 closeout 文件生成后运行；本报告本身不声明任务最终完成。

## 结论边界

最强主张为 `test_bound` 加 `structurally_supported`：当前仓库本地质量基础强、公共候选的 Semx 产品污染已清理到有界范围，但正式开源发布仍被 P0/P1 缺口与人类 authority 阻断。
