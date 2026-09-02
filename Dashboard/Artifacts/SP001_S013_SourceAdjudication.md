# S-013 Semantic-governance 来源逐节裁决

## 关键结论中文展开

本文件记录三份历史 canonical JSON 的只读来源裁决。它是 Dashboard execution evidence，不是 canonical truth；Builder 只能消费 `migrate/adapt` 的稳定规则，并必须在本仓库重新定义 owner、source scope、dependencies 与 claim ceiling。

## 来源与边界

- 来源 revision：`19e967a782e2e95d24475770bc234d86ad7c583e`。
- 读取顺序：canonical JSON 优先；对应 Markdown 只作阅读面。
- 目标不包含来源项目的产品阶段、KYM/TCO、P00-P17、M1/P04/P05/P06、provider/runtime/SAG/KG-L1、历史 Session、发布记录或本机路径。
- 本裁决最多支持 `PASS_FOR_READ_ONLY_SOURCE_ADJUDICATION_ONLY`，中文含义是 Builder 输入已具备，不表示 canonical promotion 或 S-013 完成。

## Human-AI Development（44 sections）

| Verdict | Section IDs | 处理规则 |
| --- | --- | --- |
| migrate | human-ai-roles；human-ai-role-mode-note；task-intake-evaluation-gate；validation-agent-prompt-quality-gate；contract-calibration-summary；a1-adequacy-discipline；ai-native-governance-architecture；cognitive-isolation-and-handoff；validation-handoff-packet；goal-conformance-scope-delta；closeout-language-gate；reader-facing-chinese-explanation；semantic-reviewer-trigger-policy；automatic-rejection-and-promotion | 只迁移可独立成立的角色、scope、validation、closeout 与 promotion 规则。 |
| adapt | paradigm；goal-agent-prompt-quality-gate；context-efficient-goal-validation-protocol；reusable-validation-agent-prompt；operating-loop；operating-loop-steps；acceptance-posture；bdd-validation-collaboration；contract-calibration-before-runtime；default-phase-delivery-pattern；dashboard-governed-agentic-delivery；governed-closeout-artifact；contract-delta-scan；semantic-inconsistency-reviewer-guidance；semantic-reviewer-frame-first-discipline；semantic-reviewer-architecture-review-discipline；dashboard-agent-collaboration-mode；governed-multi-agent-activation；agentic-role-split；delegation-guidance；human-on-the-loop-checkpoints；audit-logging-boundary；automation-boundary；open-source-skill-packaging；anti-patterns | 去除来源身份、阶段和产品事实；taxonomy/architecture 正文归 Semantic Surface；公共包装只保留为 SP-002 边界。 |
| reject | semantic-inconsistency-review-examples；delegation-prompt-templates；reusable-skills；packaged-skills；forward-test-results | 来源 witness、模板清单、环境路径、发布与执行证据不进入 canonical truth。 |

## Semantic Surface Engineering（10 sections）

| Verdict | Section IDs | 处理规则 |
| --- | --- | --- |
| migrate | semantic-inconsistency-taxonomy；diagnostic-alignment-surfaces；semantic-surface-subpractices | 作为有界诊断词汇，不是数值评分或普遍科学定律。 |
| adapt | promotion-verdict；core-definitions；meaning-transformation-flow；practice-registry；review-usage；promotion-boundaries | 去掉来源 Session、产品 carrier 与 runtime rollout；保留 meaning/flow/taxonomy/review/boundary。 |
| reject | promotion-issues | 来源 promotion 历史不迁移。 |

## KB Promotion and Graph Source Policy（9 sections）

| Verdict | Section IDs | 处理规则 |
| --- | --- | --- |
| migrate | contract-delta-scan-policy；promotion-criteria | 稳定复用。 |
| adapt | policy-decision；promotion-ladder；non-promises | 改写为 `kb/data` canonical、Dashboard execution memory、derived projection；删除 KG-L1 专属事实。 |
| reject | artifact-classification-map；r-depends-policy；source-set-expansion-protocol；s210-advisory-review | 来源 Session、图投影、计数与运行证据不迁移。 |

## Target Dependency Graph

```text
Human-AI Development
├── SGC Structural Contract
├── Semantic Surface Engineering
└── KB Promotion and Source Policy
    └── Semantic Surface Engineering
```

Human-AI 是基础层；Semantic Surface 和 KB Promotion 只依赖它，禁止形成循环依赖。Human-AI 中重复的 taxonomy/architecture 正文只保留短引用。

## Forbidden Semantic Inventory

- 来源项目名称和 package identity；本机绝对路径、线程 UUID、历史 Session/closeout ID。
- KYM/TCO、P00-P17、M1/P04/P05/P06、Co-Sight、SAG、provider/runtime 产品 ontology。
- KG-L1/GEXF/source-set/具体计数、来源公共发布状态、GitHub URL、forward-test verdict。
- 把 Markdown、case、report、matrix、Dashboard artifact 或 runtime output当作 semantic law。
- 把来源 standing agent authorization 迁入当前仓库。
- 通过迁移自动改变 runtime、schema、BDD、acceptance、provider、CLI、图或发布边界。

## Builder Handoff

- Human-AI owner：`sge-governance-core`；基础合同，不依赖另外三份 specialized strategy。
- Semantic Surface owner：`sge-semantic-governance`；依赖 Human-AI。
- KB Promotion owner：`sge-kb-governance`；依赖 Human-AI 与 Semantic Surface。
- source scope 只引用本仓库 source manifest、本裁决和当前硬门，不写本机绝对来源路径。
- Markdown 必须由 `kb/tools/render_kb.py` 的显式 manifest 生成，并通过 `--check`。

