# S-008 中文新手与生命周期候选收束

## 关键结论中文展开

S-008 已提供中文 Beginner Guide、Quick Start、最小项目，以及 doctor、export、bootstrap、install、upgrade、recoverable uninstall。工具拒绝覆盖非空 bootstrap 目标，升级先备份旧 core，卸载移动到 `.sge-trash/`，并保留项目自己的 AGENTS、KB 与 Dashboard。

## 落地范围

- [中文新手指南](../../../docs/Beginner_Guide_CN.md)
- [快速开始](../../../docs/Quick_Start_CN.md)
- [最小项目](../../../examples/minimal-project/README.md)
- [生命周期工具](../../../tools/sge_public.py)

## 明确非目标

作者侧命令通过不是独立新手验收，也不证明任意环境均可用。

## 连续执行扫描

`goal_terminal=false`；`next_session=S-009`；`next_session_ready=true`；`human_decision_required=false`。因此继续执行 S-009。
