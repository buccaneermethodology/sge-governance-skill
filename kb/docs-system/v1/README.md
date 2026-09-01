# Semx Doc System V1

## 本包包含
- 多层文档体系设计
- Doc as Data JSON Schema
- Doc Evolution Protocol
- Semx Phase Expansion DSL
- 收敛后的最终架构文档


## 落地方式

不要直接把docs-system当成运行时代码的一部分，而是把它当成 Semx 的设计知识库（design KB）来管理

最推荐的落地方式是：

semx/
  docs-system/
    v1/
      README.md
      docs/
      schemas/
      prompts/

也就是：
	•	放进 semx CLI 工程里，方便和代码一起演进
	•	但它属于 知识与规范层，不是 semx/ Python package 的一部分
	•	不建议先放进 semx/semx/... 这种运行时代码目录

因为这套 Doc System 的角色是：
	•	架构真理源
	•	phase contract 源
	•	CLI spec 源
	•	文档演化协议源

它不是：
	•	Python 运行时代码
	•	import 进去执行的模块


## Docs System是什么

Docs System的作用是 “文档系统骨架 + 方法论 +规范”

它不是一个已经完成的“文档生成器程序”。

它提供的是：
	•	文档体系结构
	•	Doc as Data schema
	•	Evolution Protocol
	•	Phase Expansion DSL
	•	当前收敛后的架构总文档

需要基于它，构建自己的 Semx 知识库 V1.0。

## 正确的使用方式

Step 1：把它当成“种子模板库”

你先把它解压到：

semx/docs-system/v1/

然后把里面这些文件视为：
	•	母版规范
	•	文档模板
	•	文档生成协议
	•	当前 canonical 架构基线

这一步不是生成，而是建立知识库根基。

⸻

Step 2：建立正式 Semx KB 仓库结构

建议在工程里新建：

semx/
  docs-system/
    v1/
  kb/
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
    data/
      architecture.json
      logical_pipeline.json
      cli_spec.json
      phase_specs/

这里要区分两个东西：

docs-system/v1/ 是方法论与模板

kb/是真正开始写的 Semx V1.0 知识库

⸻

Step 3：从 JSON 真源开始，一份份生成 Markdown

也就是：

Doc as Data JSON → Markdown

不应该一开始就手写所有 Markdown。
而应该先做最小真源 JSON，再编译 Markdown。

⸻

## 如何构建Doc System V1.0

第 1 批：先建 5 份核心文档

这是最小可实施集合。

1. Architecture

回答：
	•	Semx 是什么
	•	为什么存在
	•	核心对象是什么
	•	核心原则是什么

2. Logical Pipeline

回答：
	•	从 Code 到 Final UCS 的正式链路是什么
	•	每个阶段先后顺序是什么

3. CLI Spec

回答：
	•	一级命令
	•	二级命令
	•	参数
	•	运行模式

4. Artifact Spec

回答：
	•	.semx/latest/<run_id>/ 下各文件是什么
	•	每个 artifact 的 contract 是什么

5. Evolution Log

回答：
	•	V1.0 → V2.0 → V2.2 到底保留了什么
	•	删除了什么
	•	替换了什么

⸻

第 2 批：再建 Phase 文档

建议先写这些 phase：
	•	Manifest
	•	Evidence
	•	M0.5
	•	Semantic Flow
	•	Semantic Slice
	•	M1 Candidate
	•	M1 Validation
	•	Mc
	•	Behavioral Flow
	•	DRP
	•	Alignment
	•	UCS
	•	USL Lint
	•	Repair Plan
	•	Repair Apply
	•	Convergence

⸻

第 3 批：再建 Strategy 文档

优先级最高的 4 个：
	•	Strategy_M1_Extraction.md
	•	Strategy_USL.md
	•	Strategy_Repair.md
	•	Strategy_Convergence.md

⸻

## 示例问法
用 Doc_Evolution_Protocol_V1.md 作为统一总协议
每次只构建一个明确文档对象。

也就是说，不要这样：

“帮我写一份 Architecture.md”

而要这样：

基于 Doc Evolution Protocol，
先输出 Architecture 的 Doc JSON，
再输出 Markdown


⸻

## 需要准备哪些信息

A. 当前 canonical 结论

也就是你现在已经接受的正式架构事实。

至少包括：
	•	Semx 的定位
	•	M1 / Mc / Behavioral Flow / DRP 的定义
	•	M0.5 / Semantic Flow / Semantic Slice 的角色
	•	V2.2 主 pipeline
	•	USL / Repair / Convergence 的地位


B. CLI 实施边界

要决定：
	•	首版只支持 Java 还是 Java + Python
	•	是否首版就接 LLM
	•	是否首版就做 Repair / Convergence
	•	是否首版就支持 Doc JSON → Markdown 自动编译

⸻

C. 实施优先级

需要决定：
	•	哪几个 phase 先编码
	•	哪些只是规范先写，不立刻实现
	•	CLI 第一阶段的最小可运行链路是什么

例如：

Manifest → Evidence → M0.5 → Semantic Flow → Semantic Slice → M1 Candidate → M1

是不是第一阶段就够了？