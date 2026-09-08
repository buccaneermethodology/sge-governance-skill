# SP-002 独立复核问题驱动改进记录

## 问题队列

来源为 [S-010 UAT](SP002_S010_NewcomerUAT.md) 的 UAT-B1/UAT-B2，以及 [S-011 Semantic Review](SP002_S011_SemanticReview.md) 的 SEM-B1..SEM-B6。以下逐项保留原 finding，不把 reviewer 意见自动当作事实。

## UAT-B1：manifest 自身携带私有 token 且被 doctor 跳过

- disposition：`accept`。首轮导出和源码检查确认 manifest 含具体私有 token，且 validator 对 manifest `continue`。
- root cause：公开策略数据与内部 denylist 混放，测试只覆盖普通 allowlisted 文件。
- implemented change：manifest 改为通用 `content_policy`，validator 对包括 manifest 在内的所有文件检查通用 home 绝对路径。
- verification：聚焦测试、新空目录 delta UAT 和 exported recursive scan 通过。
- recurrence prevention：新增 manifest-self 私有 token 回归与通用绝对 home-path 负例。
- residual risk/claim ceiling：只证明当前扫描规则与候选集合；不证明所有可能身份形式。
- status：`resolved_with_bounds`。

## UAT-B2：新手文档缺 export/upgrade 主路径

- disposition：`accept`。两份文档确实不能独立发现完整 lifecycle。
- root cause：实现测试直接调用 API，没有验证文档可发现性。
- implemented change：Guide 与 Quick Start 补齐 staging export、source/target、upgrade、backup 定位、成功输出和 recoverable uninstall。
- verification：独立 delta UAT 未使用 `--help` 完成整条路径。
- recurrence prevention：新增文档必须包含六个 lifecycle command 与 backup/trash 的测试。
- residual risk/claim ceiling：一次 macOS clean-room 重放，不代表所有平台。
- status：`resolved_with_bounds`。

## SEM-B1：公开 glossary 引用私有 Dashboard provenance

- disposition：`accept`。
- root cause：把设计 witness 当作稳定术语 authority。
- implemented change：metadata source_scope 与条目 source_refs 全部改为公开 Skill/KB/README authority；增加候选 promotion metadata；重新渲染。
- verification：ERBE C11 GREEN 只检查 source_scope/source_refs，且无 `Dashboard/` ref；renderer check 通过。
- recurrence prevention：ERBE private-source-ref case。
- residual risk/claim ceiling：glossary 仍是 `candidate_not_approved`，未获发布批准。
- status：`resolved_with_bounds`。

## SEM-B2：ERBE specification-first 时序不可验证

- disposition：`accept_with_revision`。
- root cause：初始实现先于正式 ERBE Contract/Cases；此历史不能追溯伪造。
- implemented change：冻结 revision 2，明确原始时序例外；对全部后续 semantic/UAT repair 使用同 identity RED/GREEN，并保留 claim ceiling。
- verification：[RED](SP002_ERBE_RED_Report.json)与[GREEN](SP002_ERBE_GREEN_Report.json)均为 revision 2 pass。
- recurrence prevention：Contract status 与 report 明确禁止把 revision-2 repair evidence 倒推为原始 pre-Builder 合规。
- residual risk/claim ceiling：原始 PROC-01 仍为未获人类批准的 topology/sequence exception。
- status：`resolved_with_bounds`，仅修复链；原始时序例外仍需最终权限判断。

## SEM-B3：四层模型只有 prose

- disposition：`accept`。
- root cause：manifest 只有文件级 provenance，没有机器可重算层依赖。
- implemented change：manifest 新增 `layer_contract`、安装顺序、prefix mapping、requires/optional；doctor 验证每个文件层解析并拒绝 core→extension collapse。
- verification：public doctor与 `core_dependency_collapse` 负例通过。
- recurrence prevention：四层合同测试固定 core 不得依赖 optional domain extension。
- residual risk/claim ceiling：prefix mapping 只覆盖当前 manifest contract，不是通用包管理器。
- status：`resolved_with_bounds`。

## SEM-B4：optional extension 只有标签式接口

- disposition：`accept`。
- root cause：registry 缺 contract version、entrypoint、compatibility、provenance 和 missing behavior。
- implemented change：两个扩展补齐显式字段，保持 entrypoint=null、default-off 和 core-continues/fail-closed 语义；doctor 校验字段集合和默认关闭。
- verification：registry 回归、core 无扩展安装/UAT通过。
- recurrence prevention：扩展合同 deterministic validator。
- residual risk/claim ceiling：仅注册接口，不证明适配器已安装或领域正确。
- status：`resolved_with_bounds`。

## SEM-B5：profile-driven orchestrator overclaim

- disposition：`accept`。
- root cause：工具只消费四轴自报状态，却以 profile-driven 和 complete 描述。
- implemented change：新增 project-neutral profile 和 decision hooks；工具强制 profile、authority_ref 与 validation_verdict，终态只路由到 completion audit，输出 `completion_evidence=false`。
- verification：continue/human/terminal/invalid-terminal 四类测试通过。
- recurrence prevention：terminal-without-pass fail-closed test。
- residual risk/claim ceiling：这是 routing helper，不创建任务也不验证 Goal 完成。
- status：`resolved_with_bounds`。

## SEM-B6：final review 与动态状态、最终证据不一致

- disposition：`accept`。
- root cause：Goal/Stage Plan 混入易漂移 live state，Dashboard 尚未吸收执行进展；首轮 semantic card 也早于 final package。
- implemented change：Goal/Stage Plan 标记 initial state/entry并把 live authority路由到Dashboard；Stage Plan、Current State和Sessions进入Doing；新增OPCM、closeout draft、release packet与Cycle Ledger。
- verification：等待 final UAT、delta Semantic、final Validation 与 post-closeout reconciliation覆盖最终状态。
- recurrence prevention：最终 reviewers 必须绑定实际 closeout/Dashboard/KB/final diff。
- residual risk/claim ceiling：在最终 reviewers 完成前不能关闭。
- status：`in_progress`。

## PDI 当前结论

UAT-B1/B2 与 SEM-B1/B3/B4/B5 已完成直接修复、聚焦验证和防复发机制；SEM-B2 只能有界修复 revision-2 repair 链，不能重写历史；SEM-B6 等待最终复核后关闭。故当前 `pdi_queue=partial`，不得表述为全部完成。
