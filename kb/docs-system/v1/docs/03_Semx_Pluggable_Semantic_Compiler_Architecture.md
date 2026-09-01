# Semx 可插拔语义编译器架构

## 1. 定位
Semx 是一个面向代码库的可插拔语义编译器。它的正式目标不是帮助人看懂代码，而是从代码中稳定抽取 capability semantics，并形成可验证、可修复、可收敛的 Capability Knowledge System。

## 2. 总体原则
### 2.1 M1 是唯一正式原子锚点
正式 capability graph 只能以 M1 为原子锚点。

### 2.2 M1 不能裸从代码直接生成
为了保证质量，M1 抽取必须经过：
- Evidence
- M0.5 Fact Units
- Semantic Flows
- Semantic Slices

### 2.3 Behavioral Flow 不是抽取入口
Behavioral Flow 只在 M1 / Mc 稳定之后才从 Mc 投影出来。

### 2.4 DRP 不是代码摘要
DRP 必须是 reasoning pattern，不允许退化为方法调用链复述。

### 2.5 Lint / Repair / Convergence 是正式 phase
它们不是附属工具，而是编译链的一部分。

## 3. 总体编译链
```text
Codebase
→ Manifest
→ Evidence
→ M0.5 Fact Units
→ Semantic Flows
→ Semantic Slices
→ M1 Candidates
→ M1 Validated
→ Mc
→ Behavioral Flows
→ DRP
→ Alignments
→ UCS
→ USL Lint
→ Issue Graph
→ Repair Plan
→ Repair Apply
→ Post-Lint
→ Convergence
→ Final UCS
```

## 4. 三类关键中间层
### 4.1 Evidence
负责 grounding，不负责能力命名。

### 4.2 M0.5 Fact Units
负责把代码转换为“事实描述层”，回答：
- 输入
- 处理
- 输出
- 副作用
- 边界

### 4.3 Semantic Flow / Semantic Slice
它们不是最终语义栈里的 Behavioral Flow，而是 extraction-time scaffolding：
- Semantic Flow 负责保存控制流与分支
- Semantic Slice 负责生成最小推理单元

## 5. 正式语义对象层
### 5.1 M1
M1 是 stable single-function capability。

### 5.2 Mc
Mc 是由多个 M1 组成的组合能力，是执行层正式单元。

### 5.3 Behavioral Flow
Behavioral Flow 是 Mc 的行为投影，不再作为 M1 抽取基础。

### 5.4 DRP
DRP 是从 Flow / Mc / M1 稳定结构中抽象出来的 reasoning pattern。

## 6. 正式 phases
P00 Manifest / Config Load
P01 Evidence Extraction
P02 M0.5 Fact Unit Extraction
P03 Semantic Flow Extraction
P04 Semantic Slice Extraction
P05 M1 Candidate Extraction
P06 M1 Validation & Canonicalization
P07 Mc Derivation
P08 Behavioral Flow Derivation
P09 DRP Derivation
P10 Alignment Build
P11 UCS Build
P12 USL Lint
P13 Issue Graph Build
P14 Repair Planning
P15 Repair Apply
P16 Post-Lint
P17 Convergence

## 7. Logical Pipeline
### 7.1 抽取链
Code → Evidence → M0.5 → Semantic Flow → Semantic Slice → M1 Candidate → M1

### 7.2 组合链
M1 → Mc → Behavioral Flow → DRP → Alignment → UCS

### 7.3 质量闭环
UCS → USL Lint → Issue Graph → Repair Plan → Repair Apply → Post-Lint → Convergence

## 8. CLI Spec
### 8.1 一级命令
```bash
semx init
semx extract
semx derive
semx align
semx lint
semx repair
semx converge
semx build
semx inspect
```

### 8.2 关键二级命令
```bash
semx extract evidence <repo>
semx extract m05 <repo>
semx extract semantic-flow <repo>
semx extract semantic-slice <repo>
semx extract m1-candidates <repo>

semx derive m1 <repo>
semx derive mc <repo>
semx derive flow <repo>
semx derive drp <repo>
semx derive ucs <repo>

semx lint all <repo>
semx repair all <repo>
semx converge <repo>
```

## 9. Artifact Spec
```text
.semx/latest/<run_id>/
00_manifest.json
01_evidence.json
02_m05_units.json
03_semantic_flows.json
04_semantic_slices.json
05_m1_candidates.json
06_m1_records.json
07_mc_records.json
08_flow_records.json
09_drp_records.json
10_alignments.json
11_unified_schema.json
12_lint_report.json
13_issue_graph.json
14_repair_plan.json
15_repair_report.json
16_repaired_schema.json
17_post_lint_report.json
18_convergence_report.json
```

## 10. Strategy
### 10.1 M1 Extraction Strategy
M1 抽取不能从方法粒度开始，也不能从用户流程候选开始，而要从：
- facts
- control semantics
- reasoning slices
同时收敛意图与决策语义。

### 10.2 USL Strategy
USL 同时覆盖 structure 与 semantic，并要求统一 issue output 格式。

### 10.3 Repair Strategy
Repair 以最小 patch 为原则，不允许整份 schema 重写。

### 10.4 Convergence Strategy
系统必须在有限轮内收敛、停滞或明确进入人工 review。

## 11. Evolution Log（收敛结论）
### 11.1 从 V1.0 保留
- Evidence 作为 grounding layer
- Mc / DRP / Alignment / Lint / Repair 的基本层次
- CLI 总体命令风格
- `.semx/latest/<run_id>/` artifact 思路

### 11.2 从 V1.0 删除
- Flow Candidate Extraction 作为正式入口
- Flow Consolidation 作为 M1 前置基础
- Flow 负责系统行为理解的主导地位

### 11.3 从 V2.0 修正
- 修正 Code → M1 裸跳问题
- 把 M0.5 / Semantic Flow / Semantic Slice 插回能力抽取链
- 保持正式语义对象层仍然 M1-first

### 11.4 当前 Canonical 结论
M1 抽取必须由 Semantic Slice 保证语义正确性，由 M0.5 保证意图稳定性；正式语义栈仍然以 M1 为唯一原子锚点，并由 M1 推导 Mc，再由 Mc 投影 Behavioral Flow。

## 12. 实施建议
先落地：
1. artifact contracts
2. Evidence / M0.5 / Semantic Flow / Semantic Slice
3. M1 Candidate / M1 Validation
4. Mc / Behavioral Flow / DRP / Alignment / UCS
5. USL / Repair / Convergence
