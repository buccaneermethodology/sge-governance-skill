# S-010 最终快照 clean-room 重放（主线程证据）

## 边界

这是 Orchestrator 对当前最终快照的可重算重放，不是独立 UAT verdict，不替代 [独立 UAT](SP002_S010_NewcomerUAT.md)。它提供 final Validation 可复跑的输入和命令结果。

## 实际执行

在两个新建空目录中依次运行：

```bash
python3 tools/sge_public.py doctor
python3 tools/sge_public.py export /tmp/sp002-final-export.DMoExz
python3 tools/sge_public.py bootstrap /tmp/sp002-final-consumer.tEX03N
python3 /tmp/sp002-final-export.DMoExz/tools/sge_public.py install --source /tmp/sp002-final-export.DMoExz --target /tmp/sp002-final-consumer.tEX03N
python3 /tmp/sp002-final-export.DMoExz/tools/sge_public.py upgrade --source /tmp/sp002-final-export.DMoExz --target /tmp/sp002-final-consumer.tEX03N
python3 /tmp/sp002-final-export.DMoExz/tools/sge_public.py uninstall --target /tmp/sp002-final-consumer.tEX03N
rg -n -i '/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|semx-cli|semx-kb|S-384|S-485|audio-transcriptor' /tmp/sp002-final-export.DMoExz
python3 Dashboard/tools/sge/s002_erbe_acceptance.py --phase green
```

观察：`public_doctor:pass`；`exported:48`；bootstrap/install/upgrade/uninstall 全部返回 0；`rg` 返回 1（无命中）；ERBE GREEN report=`pass`。macOS 把 `/tmp` 规范化显示为 `/private/tmp`，仅是路径解析，不是用户 home path。

## Claim ceiling

这只证明当前机器上的一次最终快照重放；不证明独立 UAT、发布授权、生产就绪或普遍适用。
