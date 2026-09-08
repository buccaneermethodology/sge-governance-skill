# S-026 已观察用例阅读卡

这些卡只整理真实 transcript，不是独立 pass/fail authority。当前结果与最终 UAT verdict 分开。

| 用例 | 操作/前提 | 预期 | 实际证据 | 边界 |
| --- | --- | --- | --- | --- |
| 安装正例 | fresh target bootstrap → install | 5 个骨架文件 + 17 个 core 文件 + install record | [transcript](../../../../../Dashboard/Artifacts/Stage-Plan-SP-004/SP004_S026_UATTranscript.json) 的 bootstrap/install 步骤 | 本次本地 candidate |
| 非空 bootstrap | 已有 target 再 bootstrap | 拒绝且文件不变 | transcript bootstrap_negative：destination_must_be_empty | 不证明所有覆盖风险 |
| 重复安装 | 已有 managed core 再 install | 拒绝且文件不变 | transcript install_negative：already_installed | 本次目标 |
| 重复卸载 | Quick Start 已卸载后再 uninstall | 拒绝且文件不变 | transcript uninstall_negative：uninstall_requires_install_record | 不猜测删除范围 |
| Quick Start | bash fence 只替换隔离目录名 | 全部完成 | transcript quick_start_bash_fence_copy_paste | CLI 路径证据 |
| 新手指南 | 所有 bash fence 只替换隔离目录名 | 全部完成 | transcript beginner_bash_fences_copy_paste | 文本 Goal prompt 另按真实 Codex 执行记录 |
| README 占位命令 | 原始第一个 bash fence 用 zsh -n 检查 | 模板需实例化，直接复制不能承诺成功 | transcript readme_template_bash_parse：parse error | 公开文档可复制性缺口 |

不将 CLI 成功升级为完整 newcomer UAT，不将模板解析失败写成产品 runtime RED。
