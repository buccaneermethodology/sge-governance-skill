# S-003 设计交接：Skills、schemas、scripts 与 workflow registry

## 目标

把 S-002 已冻结的合同接入可执行工具面：本地 `sge-governed-checkpoints`、profile 驱动的 context bootstrap、lane task card、Goal patch、Validation snapshot 与 generic workflow contract。

## 迁移裁决

- 保留：通用治理脚本、JSON schema、read-model/checklist 与 deterministic workflow contract。
- 删除：绑定具体产品阶段、旧项目 runtime/SAG executor、provider、KYM/TCO 业务数据的脚本或 schema。
- `build-kym`、`build-tco-coverage` 仅为可选领域扩展；未安装时核心流程仍必须通过。
- `run-loop-goal-cycle` 不原样迁移；通用编排候选延期至 SP-002。

## 验收

运行 `workflow_contract.py --stage full`、全部治理 checklist、脚本编译、context/lane card schema 验证，并检查 Skill 文档只把来源项目名用于 provenance/排除说明，不作为目标 authority。

## Builder 排除

不得在本 Session 实现音频 CLI、runtime、Whisper/FFmpeg、provider 或公共发布；不得修改 S-002 冻结合同预期字段。
