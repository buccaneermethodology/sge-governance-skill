# SGE Governance 专用仓库整理收束

## 关键结论中文展开

本次变更将仓库内容切换为 `sge-governance-skill` 专用仓库。已删除 audio-transcriptor 产品设计与项目专属验收 adapter；SGE 核心 Skill、通用 profile、治理 contracts、schemas、Dashboard/KB 机制继续保留。原迁移 Dashboard 记录作为只读 provenance，不再充当当前产品配置。

## 删除范围

- `kb/bm-doc/audio-transcriptor-skill_design_v1.0.md`：原产品设计源文件。
- `Dashboard/tools/sge/s002_erbe_acceptance.py`：audio-transcriptor/S-002 专属 adapter。
- 旧的 glossary/schema validator 与迁移专用 provenance/ledger builder：不属于可复用核心，已移除以避免死代码和具体项目耦合。

## 当前 Skill 入口

- [根目录 README](../../README.md)
- [SGE Governed Checkpoints](../../.codex/skills/sge-governed-checkpoints/SKILL.md)
- [generic SGE profile](../../kb/data/strategy/sge_project_profile_v1.json)
- [workflow registry](../../kb/data/strategy/sge_workflow_registry_v1.json)

## 验收与边界

- profile validator：通过，`project_id=sge-governance-skill`。
- JSON 解析：profile、registry 通过。
- Skill metadata：已提供 `agents/openai.yaml`。
- `skill-creator quick_validate.py`：环境缺少 Python `yaml` 模块，未能执行；需在具备 PyYAML 的环境补跑。
- 未删除历史 Dashboard provenance，避免破坏既有迁移可追溯性；这些文件不属于当前 Skill authority。

## 验证交接包

- Closeout language verdict：`pass`（中文含义：本 closeout 的标题、章节和状态说明满足语言门禁）。
- 独立验证范围：profile identity、JSON 解析、registry、diff 和删除范围。

允许的主张：仓库内容已切换为通用 SGE Governance Skill 的 repo-local 候选。禁止据此声称已完成公共发布、跨仓库普遍适用性或任何具体产品能力。
