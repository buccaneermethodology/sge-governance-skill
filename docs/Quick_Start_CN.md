# SGE Governance Skill 快速开始

```bash
python3 tools/sge_public.py doctor
python3 tools/sge_public.py export /tmp/sge-public-candidate
python3 tools/sge_public.py bootstrap /tmp/sge-demo
python3 /tmp/sge-public-candidate/tools/sge_public.py install --source /tmp/sge-public-candidate --target /tmp/sge-demo
python3 /tmp/sge-demo/.codex/skills/sge-governed-checkpoints/scripts/guardrail_checklist.py --mode intake-evaluation
python3 /tmp/sge-public-candidate/tools/sge_public.py upgrade --source /tmp/sge-public-candidate --target /tmp/sge-demo
find /tmp/sge-demo/.sge-backups -name SKILL.md -print
python3 /tmp/sge-public-candidate/tools/sge_public.py uninstall --target /tmp/sge-demo
```

从候选仓库根目录开始运行。`/tmp/sge-public-candidate` 是干净 staging source，`/tmp/sge-demo` 是 target project；两者必须不存在或为空。通过条件：doctor 成功；export 只含 manifest 项；bootstrap 不覆盖非空目录；core 可执行；upgrade 在 `.sge-backups/` 留下旧 core；uninstall 把当前 core 移到 `.sge-trash/`。这是有界 clean-room 行为证据，不是发布授权。
