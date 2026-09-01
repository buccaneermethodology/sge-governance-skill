# Doc as Data and Markdown Generation Rules

## 1. 基本原则
Semx 文档必须先表达为 JSON 文档对象，再经过 Markdown 编译器生成 `.md`。
JSON 是真源，Markdown 是投影。

## 2. 最小字段
- doc_id
- doc_type
- title
- version
- status
- metadata
- sections

## 3. 常见 section 类型
- narrative
- definition
- table
- phase_contract
- dsl_spec

## 4. Markdown 自动生成规则
- 一级标题来自 title
- 每个 section 渲染为二级标题
- phase_contract 固定渲染为 Goal / Inputs / Outputs / Internal Logic / Constraints / Failure Modes / Upstream / Downstream
- table 使用标准 Markdown 表

## 5. 推荐编译链
Doc JSON → validate → normalize → render markdown → write *.md
