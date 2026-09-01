
# Semx CLI Spec V2 (Executable Specification)

## 1. Execution Model

Execution = Pipeline + Strategy + Policy + Convergence

- Pipeline = fixed phases (WHAT)
- Strategy = pluggable implementations (HOW)
- Policy = execution constraints (STRICT / NORMAL)
- Convergence = iterative optimization loop

---

## 2. Architecture Principles

### Rule 1 — Pipeline Purity
Pipeline must only define:
- phases
- IO relations

Must NOT include:
- algorithms
- strategies
- implementation details

---

### Rule 2 — Expansion Binding
Strategy must bind to pipeline segment:

Expand(P_i → P_j)

---

### Rule 3 — Strategy Versioning
Each segment may have multiple strategies:

Codebase → M1:
- V1.0 Flow-based
- V2.1 Direct
- V2.2 M0.5 + Slice

---

### Rule 4 — CLI Decoupling
CLI depends ONLY on pipeline.
Strategy = plugin.

---

## 3. Pipeline

Codebase
→ Manifest
→ Evidence
→ M0.5
→ Semantic Flow
→ Semantic Slice
→ M1 Candidate
→ M1
→ Mc
→ Behavioral Flow
→ DRP
→ Alignment
→ UCS
→ Lint
→ Repair
→ Convergence

---

## 4. Strategy Plugin Model

Plugin = Strategy(P_i → P_j)

Capabilities:
- Strategy Switching
- A/B Comparison
- Partial Replacement
- Auto Tuning

Constraints:
- must not change pipeline
- must respect IO contracts

---

## 5. Commands

### Full Mode
semx build ./repo

### Stage Mode
semx extract semantic-slice ./repo

### Resume Mode
semx build ./repo --resume-from 04_semantic_slices.json

### Strict Mode
semx build ./repo --strict

### Convergence Mode
semx converge ./repo

---

## 6. Strategy Usage

semx build ./repo --strategy m1=V2_2

Compare:
semx build ./repo --compare m1=V2_1,V2_2

---

## 7. Artifact Contract

.semx/latest/<run_id>/
00_manifest.json
01_evidence.json
02_m05.json
03_flow.json
04_slice.json
05_m1_candidates.json
06_m1.json
07_mc.json
08_flow.json
09_drp.json
10_alignment.json
11_ucs.json
12_lint.json
13_issue_graph.json
14_repair.json
15_post.json
16_convergence.json
