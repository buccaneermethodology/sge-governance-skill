
# Logical Pipeline

## Pipeline Definition

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

## Pipeline Purity Rule

Logical Pipeline must remain abstract and implementation-free.

Allowed:
- phases
- phase ordering
- input/output relations

Forbidden:
- algorithm details
- strategy-specific constructs (M0.5/Slice/etc)
- implementation logic
