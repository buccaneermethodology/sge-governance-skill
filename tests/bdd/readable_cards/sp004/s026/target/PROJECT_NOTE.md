# 项目说明示例

## 项目目的

本目录 `target` 是一个本地项目治理骨架。本说明帮助读者找到项目规则和当前文档任务的执行记录。它是一份本地说明示例，项目权限与声明范围以 [AGENTS.md](AGENTS.md) 和 [项目配置](kb/data/strategy/profile.json) 为准。

## 使用步骤

在终端进入本示例目录，然后读取实际配置：

```sh
cd /tmp/sp004-s026-01a0744b/target
cat AGENTS.md
python3 -m json.tool kb/data/strategy/profile.json
```

第一条读取命令应显示：稳定事实写入 `kb/data/`，执行记忆写入 `Dashboard/`，候选、验证、批准和发布分开记录。第二条应显示 `project_id` 为 `target`、`canonical_truth` 为 `kb/data/`、`execution_memory` 为 `Dashboard/`，以及 `claim_ceiling` 为 `repo-local governance skeleton only`，意思是这里只能主张本仓的治理骨架。若目录已移动，请把 `cd` 后的路径换成实际 target 根目录；若出现文件不存在，先确认目录，不能据此声称示例通过。

查看本次任务的目标及状态：

```sh
cat Dashboard/Artifacts/Goal.md
cat Dashboard/Sessions.md
cat Dashboard/Current_State.md
```

[目标](Dashboard/Artifacts/Goal.md)列出 M1–M5；[Session 表](Dashboard/Sessions.md)与[当前状态](Dashboard/Current_State.md)记录 UAT-S001 的进度。状态会随独立验证更新，文件存在本身不等于任务完成。

## 边界

本例只创建说明文档与执行证据，没有实现产品，也没有使用 provider、发布 release、写入远端或提升语义权威（semantic promotion）。项目配置中的路径分工不证明产品能力。

本地文档验收和外层 S-026 UAT 结论分别判断。只有原目标要求的独立验证、中文收束和最终核对全部满足时，才可判断本例完成；不能由此推导完整 UAT、新手普遍可用、公开发布或生产就绪。
