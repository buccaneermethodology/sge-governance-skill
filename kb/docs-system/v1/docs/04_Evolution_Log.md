# Evolution Log

## Strategy Evolution (Codebase → M1)

V1.0:
Flow-based → unstable

V2.1:
Direct extraction → semantic loss

V2.2:
M0.5 + Slice → stable

Conclusion:
M1 = semantic correctness + intent stability


## V1.0 → V2.0
- 从 `Evidence → Flow → M1 → Mc → DRP` 改为 `Evidence → M1 → Mc → Flow → DRP`
- 把 Flow 从正式抽取入口降为 Mc 投影后的行为层
- 引入 USL / Repair / Convergence 为正式 phase

## V2.0 → V2.2
- 发现 `Code → M1` 裸跳会降低 M1 质量
- 引入 M0.5 Fact Units
- 引入 Semantic Flow
- 引入 Semantic Slice
- 形成：
  `Evidence → M0.5 → Semantic Flow → Semantic Slice → M1 Candidate → M1`
- 明确区分：
  - Semantic Flow（抽取 scaffold）
  - Behavioral Flow（正式行为层）
