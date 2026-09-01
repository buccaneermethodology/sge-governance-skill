# Semx Phase Expansion DSL

## 1. 目的
Semx Phase Expansion DSL 用于把每个 phase 的设计收敛为可统一生成的 phase 文档对象。

## 2. DSL 结构
```json
{
  "phase_id": "P05",
  "name": "M1 Candidate Extraction",
  "goal": "Extract candidate atomic capabilities from semantic slices and M0.5 clusters",
  "inputs": ["04_semantic_slices.json", "02_m05_units.json"],
  "outputs": ["05_m1_candidates.json"],
  "internal_logic": [],
  "constraints": [],
  "failure_modes": [],
  "upstream": [],
  "downstream": []
}
```

## 3. 字段解释
- phase_id
- name
- goal
- inputs
- outputs
- internal_logic
- constraints
- failure_modes
- upstream
- downstream

## 4. 推荐 phase DSL 列表
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


## Expansion Binding Rule

Every Expansion must bind to a pipeline segment:

Expand(P_i → P_j)

Constraints:
- P_i and P_j must exist in Logical Pipeline
- Expansion cannot introduce new phases

---

## Replaceability Rule

An Expansion can be replaced independently if:

- bound to a specific segment
- does not break IO contract

Example:
Replace Expand(Codebase → M1) V2.1 with V2.2