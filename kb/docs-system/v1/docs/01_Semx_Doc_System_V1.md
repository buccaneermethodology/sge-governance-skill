# Semx Doc System V1

## 1. 目标

Semx Doc System V1 的目标是建立一套可直接服务于 Semx CLI 实施的知识库系统。它有三个正式目标：

1. 让 Semx 的核心设计以多层文档体系稳定沉淀。
2. 让文档先转为 Doc as Data，再编译为 Markdown。
3. 让所有架构变化通过版本化演化协议进入知识库。

## 2. 多层文档结构

### L0. Index / Navigation Layer
统一入口与导航。
典型文件：
- README.md
- docs/_index.md
- docs/_toc.md

### L1. Canonical Architecture Layer
沉淀当前有效的正式架构真理。
典型文件：
- Architecture.md
- Logical_Pipeline.md
- Runtime_Model.md
- Knowledge_Model.md

### L2. Phase Expansion Layer
展开每个 phase 的职责、输入、输出、约束与失败边界。
典型文件：
- Phase_00_Manifest.md
- Phase_01_Evidence.md
- Phase_02_M05.md
- Phase_03_Semantic_Flow.md
- Phase_04_Semantic_Slice.md
- Phase_05_M1_Candidate.md
- Phase_06_M1_Validation.md
- Phase_07_Mc.md
- Phase_08_Behavioral_Flow.md
- Phase_09_DRP.md
- Phase_10_Alignment.md
- Phase_11_UCS.md
- Phase_12_USL_Lint.md
- Phase_13_Issue_Graph.md
- Phase_14_Repair_Plan.md
- Phase_15_Repair_Apply.md
- Phase_16_Post_Lint.md
- Phase_17_Convergence.md

### L3. Strategy Layer
沉淀跨 phase 的横切策略。
典型文件：
- Strategy_M1_Extraction.md
- Strategy_USL.md
- Strategy_Repair.md
- Strategy_Convergence.md
- Strategy_Prompt_Protocol.md

### L4. CLI Spec Layer
给实施者提供可直接编码的命令、artifact、配置与目录规范。
典型文件：
- CLI_Spec.md
- Artifact_Spec.md
- Config_Spec.md
- Command_Reference.md

### L5. Evolution Layer
记录架构从旧版到新版的变化原因、保留项与废弃项。
典型文件：
- Evolution_Log.md
- ADR_*.md
- Deprecated_Designs.md

## 3. 文档生成关键规则

1. 文档必须先有 JSON，再有 Markdown。
2. Canonical 文档只写当前有效真理。
3. 每个章节必须是可执行知识，而不是泛泛描述。
4. Phase 文档必须统一模板：Goal / Inputs / Outputs / Internal Logic / Constraints / Failure Modes / Upstream / Downstream。
5. 文档禁止混层。
6. Evolution 必须显式记录“保留 / 删除 / 替换”。
7. 推荐英语术语 + 中文解释并存。

## 4. 推荐知识库目录

```text
semx-kb/
  README.md
  docs/
    Architecture.md
    Logical_Pipeline.md
    CLI_Spec.md
    Artifact_Spec.md
    Glossary.md
    phases/
    strategy/
    evolution/
```

## 5. Doc System 与 CLI 的关系

Doc System 不是 CLI 的附属物，而是 CLI 的静态知识面。它负责：
- 固化架构真理
- 固化 Phase Contract
- 固化横切策略
- 固化演化过程
