# Dashboard Methodology

This file records the working semantics of the dashboard so a future LLM can continue the project without relying on chat memory.

## Dashboard Definition

The dashboard is a cognitive tracking system for an evolving project. 
Dashboard method is one of the many tools and methods in Buccanneer Methodology. Here is more information:https://github.com/buccaneermethodology/ExplorationDashboardSynthesizer.git.

It is not:

- a pure task list
- a final report
- a canonical design document
- a flat backlog of unrelated action items

Its purpose is to preserve:

- visibility into what has already been explored
- traceability across ongoing thinking and implementation
- optionality for what should happen next

In this repository, the dashboard is the execution layer. Canonical truth still lives in `semx-kb/`.

Under the current agentic-execution experiment, the dashboard has three nested responsibilities:

- governance plane: strategic tracks, decisions, risks, quality metrics, automation state
- stage-plan plane: bounded batch-execution contracts
- execution plane: sessions, session units, exceptions, and agent logs

## Dashboard vs Task Management

Traditional task management assumes the target is already clear and work should be scheduled toward it.

This dashboard assumes:

- project understanding continues to emerge
- implementation work reveals new follow-up needs
- some of the highest-value next steps are only visible after finishing the current step

Therefore the dashboard must track both:

- the stable directions of inquiry and delivery
- the newly emerging bounded sessions that push those directions forward

## Big Idea Definition

A `Big Idea` is a long-lived exploration or implementation direction.

It should usually have these properties:

- spans multiple sessions
- is not expected to close quickly
- may branch, split, or be reorganized
- represents a continuing direction of thought or delivery, not just one task

In this repository, a `Big Idea` should be treated as the semantic track or stream under which multiple sessions accumulate over time.

## Session Definition

A `Session` is the smallest manageable execution or exploration unit in the dashboard.

### Session Identity And Storage

Session execution memory now has a three-surface registry:

- `Dashboard/Sessions.md`: current and recent execution entry.
- `Dashboard/Session_Index.md`: compact all-Session locator.
- `Dashboard/Archives/Sessions/*.md`: complete closed historical rows and migrated legacy execution notes.

Every record has a unique `Session Key`. Use `<Parent Stage Plan>/<Historical ID>` when a parent is recoverable, such as `SP-063/S-478`; use `LEGACY/<Historical ID>` otherwise. The old `S-xxx` value is retained as `Historical ID`, not as a guaranteed global primary key. This distinction is necessary because SP-063 and SP-064 both historically used `S-477`, `S-478`, and `S-479`.

Tools and future agents must resolve a duplicate historical ID to all matching canonical keys or require parent context. Silent first-wins is forbidden. Stable historical links use anchors in `Session_Index.md` or `Archives/Sessions/`; line numbers in the compact current file are not durable identity.

### Session Registry 日常操作

Session registry 是可检查的 execution-memory 投影，而不是 `semx-kb/` 的替代真源。新建、更新、关闭、归档 Session，或改动 current/index/archive/manifest 任一表面时，先运行：

```bash
python3 Dashboard/tools/session_registry.py reconcile --repo . --check
python3 Dashboard/tools/session_registry.py validate --repo .
```

修改经确认的 record source 后，再运行 `reconcile --check`。仅当它报告可重建的派生 drift 且预检没有 error 时，才明确运行：

```bash
python3 Dashboard/tools/session_registry.py reconcile --repo . --apply
python3 Dashboard/tools/session_registry.py reconcile --repo . --check
python3 Dashboard/tools/session_registry.py validate --repo .
```

在任一 check/validate 非零时，不能把受影响 Session 标为 `Done` 或写等价关闭结论。duplicate canonical key、malformed row、unknown Status、ambiguous identity、unexpected archive surface 或历史说明表面错误必须人工处理；日常 `--apply` 不得猜测记录、first-wins、删除未知 archive 文件或改写 `Legacy_Execution_Notes.md`。

当 registry check/validate 已通过且变更影响 Dashboard KG / DKG 时，才使用 `Dashboard/tools/generate_dashboard_kg.py` 的显式输出路径重建 DKG，并运行 focused registry gate。DKG 是生成的查询/阅读投影，不是 reconcile 的副作用，也不反向决定记录身份或修复内容。`migrate` 仅为 S-485 frozen 487-record legacy bootstrap；`migrate-references` 仅为受控 locator migration；二者都不是日常同步或 repair 命令。

The current surface retains all `To do` and `Doing` records plus a bounded recent window. Closed older rows move to archives but remain fully discoverable through the index. Status remains one of the four display values from `Dashboard/Rules.md`; prior compound wording is preserved separately as `Historical Status Snapshot`.

In this repository, a session may be:

- completed work that actually happened
- active work happening now
- a proposed next time-slice that is expected to happen soon

A session row is candidate memory, not a promise that the project must execute it next or at all.

A session should satisfy the BM spirit:

- time-bounded
- focused on one core topic
- bounded in scope
- motivated by a specific purpose
- capable of producing cognitive or implementation progress

If a session completes only after its original scope is intentionally narrowed, the dashboard should not hide that by leaving the original scope text untouched. In that case:

- rewrite the completed session row so its scope, exit criteria, next step, and notes describe the subset that actually landed
- add a follow-on session for the deferred remainder when that remainder is still concrete and materially relevant
- prefer an explicit new session over burying the remaining work inside notes or chat memory

In the agentic workflow, a dashboard session remains the visible bounded work item, but one session may fan out into multiple agent-owned `session units` under a stage plan.

## Stage Plan Definition

A `Stage Plan` is a bounded execution contract for one governed batch of work.

It exists to let AI run continuously without continuous human steering.

A stage plan should freeze:

- which backlog items are in scope for the batch
- which lanes may run in parallel
- which write scopes each lane may touch
- which gate pack and acceptance posture apply
- what retry, revision, drift, and cost limits apply
- which events trigger human checkpoint or exception escalation
- what exit criteria must be satisfied before promotion

A stage plan is not canonical truth and should not redefine contracts that belong in `semx-kb/`.

## Goal Conformance And Scope Delta Definition

A `Goal Scope Ledger` is the Dashboard execution-memory surface that preserves the original user Goal, Stage Plan, or tracked Session objective before implementation narrows or stages it.

For non-trivial Goals, Stage Plans, and tracked Sessions, the ledger should identify:

- the original requirement or acceptance criterion
- whether it is a must-have, non-goal, risk, or acceptance evidence requirement
- the current status
- evidence needed or produced
- the owning Session, Stage Plan, or lane
- the defer, blocker, or not-applicable reason when it is not landed

A `Scope Delta` is any deletion, replacement, renaming, weakening, postponement, newly excluded scope, or must-have-to-non-goal conversion relative to the original objective. A Scope Delta should state the original requirement, revised target, reason, impact or lost evidence, human approval status, and deferred session or blocker.

An `Original Plan Coverage Matrix` is the closeout table that compares original requirements against landed scope. Each original item should be classified as:

- `landed`
- `not landed human-approved deferred`
- `not landed blocked`
- `not applicable with reason`

Dashboard `Status` cells are filtering fields, not claim ledgers. If any original must-have is not landed, the row should not create a new status phrase such as bounded done or partial done. Instead, rewrite the row's `Scope`, `Exit Criteria`, `Next Step`, and `Notes` so the row describes the actual landed bounded scope before marking it `Done`; then add a follow-on session for any still-concrete remainder, or record the human-approved deferral, not-applicable rationale, blocker, termination condition, or cancellation reason in the row and closeout evidence.

## Execution Entry Order

Dashboard execution should not start from `Sessions.md` alone unless the task is explicitly a narrow row update.

For non-trivial Dashboard work, the default entry order is:

1. `Dashboard/Current_State.md`
2. the relevant parent row in `Big_Ideas.md`
3. the relevant `Stage_Plans.md` row, when one exists or is adjacent
4. the selected `Sessions.md` row
5. high-signal evidence from `Dashboard/Artifacts_Index.md`

For an archived Session, step 4 means first resolving its `Session Key` in `Dashboard/Session_Index.md`, then opening the linked archive row or primary evidence. Do not search only the compact current table and conclude that an older Session does not exist.

The reason is simple: Sessions are bounded execution memory, not the source of strategic direction. Big Ideas define the long-lived semantic track, Stage Plans define governed batch contracts, and Current State records the latest operational reading across those layers.

## Parent Row Review Gate

At closeout for any non-trivial task that changes Dashboard state or next-step advice, check the parent rows before only updating the Session row:

- If the work changes the preferred next direction of a Big Idea, update that Big Idea's `Next Step` or `Notes`.
- If the work advances, narrows, bypasses, or invalidates an active Stage Plan, update that Stage Plan or state why no Stage Plan applies.
- If the work creates a new current entry point, add or update `Dashboard/Current_State.md`.
- If the work produces a high-signal artifact future agents will need, add it to `Dashboard/Artifacts_Index.md`.
- If no parent Big Idea or Stage Plan update is needed, say so in the closeout instead of silently ignoring those layers.

This gate is proportional. It can be one sentence for small tasks. Its purpose is to prevent Dashboard execution from becoming Session-led backlog processing while Big Ideas and Stage Plans drift.

## Dashboard Operating Graph

`Dashboard/Artifacts/Dashboard_Operating_Graph.json` is the generated Dashboard KG / DKG-L1 projection.

`Dashboard/Artifacts/Dashboard_Operating_Graph.gexf` is the recommended Gephi Lite visual import export.

`Dashboard/Artifacts/Dashboard_Operating_Graph.graphology.json` is a Graphology-compatible JSON export kept as a secondary visual/programmatic format. If Gephi Lite JSON import rejects it, use the `.gexf` file instead.

The GEXF export has a deterministic layered layout:

- `L0 Dashboard`
- `L1 Control Surfaces`
- `L2 Big Ideas`
- `L3 Stage Plans`
- `L4 Sessions`
- `L5 Artifacts`
- `L6 Quality Metrics`

Each layer is placed on a fixed x-axis column and each node carries a `visual_layer` attribute. In Gephi Lite, import the `.gexf` file and keep imported positions to inspect the Dashboard by BI / SP / Session / Artifact layer instead of starting from a force-directed hairball.

It is a read-only generated projection over Dashboard execution memory. It helps answer questions such as:

- which Sessions belong to a Big Idea
- which Sessions depend on a prior reconciliation
- which artifacts a Session produced or referenced
- which Stage Plans are open
- which rows were reconciled by a Dashboard cleanup
- which control surfaces and query reports are current

It does not replace Markdown. The Markdown Dashboard remains the editable authority surface for execution state, while DKG-L1 is a generated query/read model. It also does not replace `semx-kb/` or KG-L1: canonical architecture, contract, strategy, and terminology truth still live in `semx-kb/`; DKG-L1 only projects Dashboard governance state.

Regenerate both JSON outputs after Dashboard changes:

```bash
python3 Dashboard/tools/generate_dashboard_kg.py \
  --out Dashboard/Artifacts/Dashboard_Operating_Graph.json \
  --query-report Dashboard/Artifacts/Dashboard_Operating_Graph_Query_Report.md \
  --graphology-out Dashboard/Artifacts/Dashboard_Operating_Graph.graphology.json \
  --gexf-out Dashboard/Artifacts/Dashboard_Operating_Graph.gexf \
  --created-by-session <SESSION-ID> \
  --created-at <YYYY-MM-DD>
```

If Dashboard KG use grows beyond the current generated report, add a separate reviewed session for validation gates or a richer query CLI instead of silently turning the generated projection into a second Dashboard truth source.

The DKG Session node ID is the canonical `Session Key`, not the historical `S-xxx` alias. The generated node keeps `historical_id` and `parent_stage_plan` attributes for lookup. Duplicate canonical keys and conflicting graph node IDs fail closed; duplicate historical IDs remain separate nodes.

## Session Unit Definition

A `Session Unit` is the smallest agent-owned construction packet under a stage plan.

Examples:

- implement one runtime patch in one write scope
- harden one validator surface
- update one fixture family
- assemble one dashboard or KB patch set

Session units may be tracked inside a stage plan or agent log without each one becoming a top-level dashboard row.

## Agent Log Definition

An `Agent Log` is an append-only Markdown record of one agent's participation in non-trivial governed multi-agent execution, tracked Session / Stage Plan execution that starts lanes, or a triggered Semantic Reviewer lane.

Its purpose is to preserve:

- the exact user-visible workflow notes emitted by the agent
- the exact final output emitted by the agent
- the inputs, scope, artifacts, gates, and exceptions that explain what happened

Agent logs are execution-layer audit material. They do not export model-private chain-of-thought.

By default, Agent Logs are on for non-trivial governed multi-agent execution, tracked Session / Stage Plan execution that starts lanes, and triggered Semantic Reviewer lanes. The dashboard stays at summary level only for trivial read/query/formatting tasks, low-risk single-agent summary-level work, or work without Dashboard/KB/contract/gate/semantic-promotion impact unless the user or Stage Plan asks for full logs.

A `Validation Handoff Packet` is the lightweight default evidence packet for non-trivial work. It should state original objective coverage when a Goal, Stage Plan, or tracked Session is involved, claimed scope, Scope Delta if any, claimed semantic change, explicit non-goals, files/artifacts changed, gates/tests run, evidence produced, known risks, KB/Dashboard impact, and `Closeout language verdict`. Store it by default in the task's Dashboard closeout artifact under a `验证交接包` section, and copy or link it from Agent Logs when Agent Log default applies. It supports validation but is not itself a Validation verdict.

A `Design Artifact` is the default post-C0 design handoff surface for non-trivial governed implementation work. After C0 approval, use `Dashboard/Artifacts/<SessionID>_<ShortTopic>_Design.md` for a single tracked session and `Dashboard/Artifacts/<StageID>_<ShortTopic>_Design.md` for a Stage Plan or multi-session batch. It should turn approved scope, non-goals, constraints, and exit criteria into module/data/API/contract boundaries, implementation slices, gate/test plan, risks, Builder handoff, and Validation focus. It is Dashboard execution memory, not canonical truth.

A `Closeout Artifact` is the default durable evidence surface for non-trivial governed work. Use `Dashboard/Artifacts/<SessionID>_<ShortTopic>_Closeout.md` for a single tracked session and `Dashboard/Artifacts/<StageID>_<ShortTopic>_Closeout.md` for a Stage Plan or multi-session batch. It should use Chinese headings by default: `关键结论中文展开`, `落地范围`, `原始目标覆盖矩阵` when applicable, `范围变更复核`, `Lane 启动与例外`, `设计交接`, `验证交接包`, `验证结论`, `明确非目标`, `证据`, `运行的门禁`, `语义复核`, `延后范围`, `KB/Dashboard 复核`, and `后续候选`. It is Dashboard execution memory, not canonical truth.

A `Closeout Language Gate` is the executable reader-facing closeout check. Run `guardrail_checklist.py --mode closeout-language --file <closeout.md>` before final completion wording for non-trivial governed work. It checks that H1/H2 headings contain Chinese explanation, English verdict/status/routing labels are explained in Chinese, and `验证交接包` includes an explicitly passing `Closeout language verdict`. A missing, failed, blocked, pending, not-run, or non-explicit verdict blocks final completion. This gate protects closeout readability and governance evidence; it does not change runtime behavior, schemas, acceptance posture, or KB truth by itself.

Reader-facing evidence citation rule: Closeout, final summary, Dashboard parent/row prose, and the explanatory part of `验证交接包` must link to the exact source artifact with a clickable Markdown link. They must not use a bare SHA-256/hash/digest number as the human reader's source reference. Exact digests remain in machine-readable lane cards, manifests, snapshots, JSON, or validation reports when required by a machine gate; the human-facing text links to those files and explains the evidence boundary.

A `Reader-Facing Chinese Explanation` is the explanation layer that prevents compressed status terms, gate verdicts, KB/Dashboard routing labels, semantic-risk labels, scope fences, or next-candidate shorthand from becoming hard for the human reader to judge. When such compressed conclusions appear in a closeout artifact, include `关键结论中文展开`: original conclusion, Chinese meaning, judgment impact, evidence or boundary, and next action. In final chat, a shorter `这意味着什么` explanation is acceptable when it preserves the same judgment support.

A `Task Intake Evaluation Gate` is the entry action that treats every user instruction as an instruction candidate before execution. It checks objective, source authority, boundaries, risk, and execution route. It is proportional: simple low-risk work may pass silently, while persistent edits, proposals, approval text, contracts, KB/Dashboard, acceptance/gate, or semantic-promotion work needs explicit intake before action.

A `Goal Conformance / Scope Delta Gate` is the scope-integrity check for non-trivial Goals, Stage Plans, and tracked Sessions. It runs after C0 or initial design, before dominant Builder implementation, and before closeout. It compares the revised design and landed scope against the original objective, not only against the latest implementation plan. It prevents scope substitution: a narrower revised target may be completed honestly, but it cannot be used to claim the original goal is complete unless all original must-haves are landed, approved for deferral, blocked by a termination condition, or not applicable with reason.

A `Contract Delta Scan` is the closeout action that checks whether an approved Dashboard artifact, proposal, reviewed baseline, matrix, or gate artifact contains stable contract or promotion semantics. The scan routes each actual delta to KB JSON, Dashboard-only evidence, gate docs, runtime/tests, or a deferred session; it does not make every Dashboard artifact canonical truth.

A `Multi-Agent Activation Gate` is the first control-plane check for tracked or non-trivial governed work. Standing user authorization is in effect for future Semx non-trivial governed tasks: AI is explicitly authorized to use subagents / delegation as needed. In this repository, AI may decide to start subagents / delegation for tracked Session, Stage Plan, or non-trivial governed work even when the user has not explicitly asked for subagents. A human request to execute or start a tracked Session or Stage Plan is sufficient authorization for governed multi-agent execution unless the human says single-agent. After C0 approval, the approved scope automatically enters governed implementation mode unless the human says single-agent / no multi-agent or the task is truly trivial. Default governed execution starts Design, Builder, Validation, and Closure lanes; missing default lanes must be recorded as a `Single-Agent Exception` in the closeout artifact. The absence of an explicit subagent request is not itself a valid exception reason.

## Dashboard Agent Mode

A `Dashboard Agent` is a strategic Dashboard steward. Its job is to reconstruct the project panorama, judge Dashboard health, surface stale or misleading rows, and give the human high-quality next-step choices.

For a full refresh, it should use `exploration-dashboard-synthesizer`, then read the current Dashboard surface and relevant `semx-kb/` truth. The report should cover current stage, validation maturity, code/artifact quality, active Stage Plans, stale rows, risks, and open directions.

By default, a Dashboard Agent gives three candidate next moves:

- one steady quality/stability move
- one speed/progress move
- one blue-sky move outside the current Dashboard when useful

Dashboard updates from this role are proposals by default. The agent should list suggested archive, cancel, rewrite, or add actions with evidence and rationale, but should not write those changes unless the human explicitly asks to update the Dashboard.

## Delegation Guidance

- Start with a short local decomposition before spawning agents.
- Standing user authorization applies to future Semx non-trivial governed tasks: AI is explicitly authorized to use subagents / delegation as needed, subject to the Multi-Agent Activation Gate.
- Treat `执行 S-xxx`, `启动 S-xxx`, `execute S-xxx`, or `执行 SP-xxx` as governed multi-agent activation by default unless the human says single-agent. For other non-trivial governed work, AI should use the Multi-Agent Activation Gate to decide whether subagents / delegation are warranted; it does not need a separate explicit user request for subagents.
- After C0 approval, start governed implementation mode automatically for the approved scope unless the human says single-agent / no multi-agent or the task is truly trivial.
- For tracked Session / Stage Plan execution and other non-trivial governed work, spawn or assign Design, Builder, Validation, and Closure lanes before substantial work. Deciding not to do so requires a recorded `Single-Agent Exception`.
- Prefer design, builder, validation, and closure lanes over default read-only explorer lanes.
- Non-trivial governed batches should usually include at least one Design Agent lane, one Validation Agent lane, and one Closure Agent lane, even if there is only one builder lane.
- Every post-C0 implementation batch should save a Design Artifact / Design Handoff before dominant Builder work, and any material Builder divergence from that design should be recorded as a Design Delta in the closeout.
- Every non-trivial task should provide a Validation Handoff Packet before final validation and store it in the closeout artifact rather than only in the final chat summary. The packet should include `Closeout language verdict`. When Agent Log default applies, copy or link the handoff from the relevant log.
- Start Validation early enough to review substantive work before final promotion or closeout; it should not be only a last-minute afterthought.
- Treat Validation as a gate, not as optional commentary. Final closeout should wait for a validation verdict or an explicit blocker/exception record.
- A Validation Handoff Packet is not a Validation Agent verdict. If no Validation lane ran, the closeout must say so.
- Use a Semantic Reviewer as a separate semantic-governance lane only when the human requests it, the Stage Plan requires it, or Orchestrator/Validation records a semantic-risk escalation such as capability widening, genericization, semantic promotion, acceptance posture change, oracle/golden freeze, calibration promotion, major canonical KB change, hidden widening, or future drift risk.
- Semantic Reviewer should work from evidence and explicit claims in an independent thread, not from builder exploratory reasoning or persuasion-style handoffs.
- Semantic Reviewer starts with Semantic Architecture Review before field-level repair: truth carrier placement, law/witness/evaluation/governance split, complexity trajectory, God Object drift, semantic bureaucracy, half-schema/DSL drift, invariant law quality, and capability-family algebra.
- Semantic Reviewer starts with Frame-First Review before local wording or table consistency: authority level, layer split, core ontology, claim/evidence mapping, semantic invariants, failure taxonomy, transfer rules, negative space, likely future misuse, and promotion boundary.
- Use a Dashboard Agent as a strategic read-mostly lane for Dashboard refresh, macro next-step choice, stale-state audit, and blue-sky candidate generation. It is not a default implementation lane and should not write Dashboard rows unless the human explicitly asks for that update.
- Use explorer lanes only when the work is genuinely exploratory or the unknown cannot yet be bounded into a concrete builder or validator task.
- Give Validation a meaningful first review window on non-trivial batches. Use that time for non-overlapping gates, doc sync, or closure prep; interrupt only for blocker triage or when the batch is truly blocked on a validation decision.
- Closure should create or update the closeout artifact for non-trivial governed work and make the changed Dashboard session or Stage Plan row reference it.
- Closeout artifacts should include a `Lane Activation / Single-Agent Exception` section listing actual Design Agent, Builder, Validation, Closure, Semantic Reviewer, and Dashboard Agent lanes.
- Closeout artifacts should include `关键结论中文展开` when they contain compressed conclusions that affect human judgment; final chat summaries should include an equivalent Chinese explanation instead of leaving English/status shorthand unexplained.
- Closeout artifacts should run and record the `closeout-language` gate before final completion wording. Missing, failed, blocked, pending, not-run, or non-explicit `Closeout language verdict` means the task is not ready for final closeout.
- Keep Agent Logs on by default for non-trivial governed multi-agent execution, tracked Session / Stage Plan execution that starts lanes, and triggered Semantic Reviewer lanes; skip them only for trivial, low-risk, or explicitly summary-level work.

## Common Lane Types

- `Design Agent`: stays read-mostly or design-doc-only after C0 approval and saves the software design artifact that defines module/data/API/contract boundaries, implementation slices, gate/test plan, risks, Builder handoff, and Validation focus.
- `Builder`: owns a bounded write scope and lands code, tests, fixtures, docs, or CLI wiring.
- `Validation`: stays read-mostly and returns a quality report covering design, code, docs, tests, gates, and blocking versus non-blocking issues.
- `Validation` also owns the last substantive quality gate before promotion; its timing should preserve review quality rather than optimize orchestrator speed.
- `Validation Agent Prompt`: the default validation posture for Goal / Stage Plan / tracked Session closeout. It requires a Read Manifest, plain-Chinese task understanding, original-objective coverage review, Scope Delta audit, evidence completeness check, blocking/non-blocking findings, and evidence-bound verdict. Orchestrator pressure cannot waive these checks.
- `Semantic Reviewer`: stays read-mostly in a separate thread and reviews semantic integrity, boundary discipline, calibration sufficiency, future drift, truth-layer contamination, accidental generalization, and promotion risk. It must first review semantic architecture and evolution direction: truth carrier placement, law/witness/evaluation/governance split, God Object drift, semantic bureaucracy, half-schema/DSL drift, invariant law quality, and capability algebra. It then challenges authority level, ontology/layer separation, semantic invariants, failure taxonomy, and transfer rules before artifact-local consistency review. It is triggered by human request, Stage Plan requirement, or recorded semantic-risk escalation rather than every non-trivial task by default.
- `Dashboard Agent`: stays read-mostly by default and reviews the project panorama, Dashboard health, stale rows, strategic candidates, and blue-sky directions. It proposes archive/cancel/rewrite/add actions but only writes them after explicit human approval.
- `Closure`: audits what actually landed, checks scope honesty, updates or proposes Dashboard state, and recommends the next SP / Sessions.
- `Closure` should recommend next SP / Sessions with enough context that a later human or agent can understand the recommendation without replaying the whole batch: what each candidate is, why it is relevant now, and why it outranks nearby alternatives.
- `Explorer`: gathers codebase facts only when the unknown itself is still the work and the batch cannot yet be decomposed into builder or validator ownership.

## Closeout Recommendation Detail

For a non-trivial closeout, the recommended next `SP` and `Sessions` should not be emitted as IDs alone unless the user explicitly asks for an ultra-short answer. This applies even when the completed work was not executed under an explicitly named active Stage Plan.

A good closeout recommendation should briefly preserve:

- the candidate `SP` or `Session` topic in plain language
- the immediate leverage or bottleneck it addresses
- the reason it is ranked above other currently open sessions

These recommendations are decision support, not commitments. The Dashboard should keep candidate memory visible without pretending that every suggested session must later be executed.

If no plausible next candidate `SP` or no concrete next `Session` exists, the closeout should say that explicitly rather than silently omitting the recommendation section.

## Execution-Memory Hardening

This repository now uses one repo-local operational skill at `.codex/skills/semx-governed-checkpoints/` to reinforce two failure-prone checkpoints that were easy to miss when they lived only as long-form rules.

- `Pre-freeze oracle review`: when a new golden/oracle fixture is being created, the first AI-authored artifact is a proposal, not a frozen truth. The human should review or approve it unless they explicitly delegate the final semantic choice.
- `Pre-closeout deferred scan`: before final closeout, explicitly check for narrowed scope, concrete deferred follow-ons, and later candidate sessions so they are recorded in the Dashboard rather than left in chat memory.

The skill is an execution aid, not canonical truth. The truth still lives in `AGENTS.md`, `Dashboard/Rules.md`, and `semx-kb/`; the skill exists to make those rules easier to remember and apply at the right moment.

## Contract Calibration Before Runtime

When a phase contract is still moving, the dashboard should track a calibration loop before it tracks a large maintained runtime implementation. The point is not to slow delivery down for its own sake; it is to keep the repo from hard-coding the wrong structure too early.

Use the following sequence unless there is a clear reason to do otherwise:

1. `Golden / oracle freeze`
   - Capture one manual or human-reviewed artifact that expresses the intended semantic boundary.
   - This answers "what good looks like" before the code starts optimizing for field shape alone.

2. `Candidate trial`
   - Run bounded prompt or LLM trials against the same target shape.
   - These early runs may be manual, scripted, or agent-driven; the important thing is that they remain bounded calibration evidence rather than being mistaken for a stable maintained path.
   - Real-provider trials are allowed when they are the most honest way to expose missing fields, unstable structure, or boundary drift.
   - Keep repeated attempts such as `run1 ... runN` when they help measure stability instead of relying on one lucky sample.

3. `Trial evidence capture`
   - Preserve enough run metadata, reports, or summarized findings that later contributors can see which failure modes actually appeared.
   - The goal is not verbose logging by default; it is durable evidence for why the next gate was added.

4. `Acceptance hardening`
   - Convert the observed failure modes into deterministic checks: schema, lineage, semantic diff, boundary audit, preflight, and regression coverage.
   - A legal JSON shape is not enough if the trial exposed semantic drift, false grounding, or unstable revision behavior.

5. `Maintained runtime body`
   - Only after the contract and gates are stable enough to protect the implementation should the maintained runtime body become the main path.
   - If the phase ultimately depends on provider calls, this step may still land a provider-facing boundary, fake/replay harness, or guarded runtime integration; what should still wait is treating real-provider execution as the already-settled automated path.
   - If only a first-pass subset is ready, track that honestly as a narrower session and keep the remaining hardening visible as a follow-on session.

6. `Provider-backed automation`
   - What comes last is not "provider exists at all" but "real provider execution is formalized as a stable automated surface".
   - Non-deterministic provider runners may call the deterministic acceptance posture, but they do not redefine it.

This separation matters: the acceptance posture is the deterministic contract/gate system that decides whether an artifact may advance. Real-provider candidate trials are a calibration tool that helps discover what that posture still needs to reject or require.

## Default Phase Delivery Pattern

For a new or unstable phase, the default governed pattern is:

1. `C0 Oracle freeze`
   - Human and AI agree on one golden/oracle artifact or oracle pair that expresses the intended semantic boundary.
   - This is the main human checkpoint at the front of the phase.

2. `A1 Automated candidate trials`
   - AI designs prompt plus trial harness and runs repeated candidate generation, including real-provider trials when they are the cheapest honest signal.
   - The goal is to collect calibration evidence, not to declare a maintained path yet.

3. `A2 Acceptance hardening`
   - AI converts the observed failure modes into deterministic acceptance posture elements: schema, lineage, semantic diff, boundary audit, preflight, regression, and policy wording.
   - At this point the phase starts to gain durable protection against rediscovered mistakes.

4. `C1 Boundary review if needed`
   - Human reviews only when the contract meaning, golden semantics, provider/cost boundary, or gate strictness changed materially.
   - If the phase stabilized without semantic drift, this checkpoint can stay implicit.

5. `A3 Maintained runtime body`
   - AI implements or expands the maintained runtime body against the stabilized contract and acceptance posture.
   - If the phase ultimately needs provider calls, this step may still land guarded provider integration, but not yet treat real-provider execution as the settled automation surface.

6. `A4 Optional provider-backed maintained automation`
   - AI formalizes real-provider execution as a stable maintained runner only when it now consumes an already-stable deterministic acceptance gate.
   - This step is optional; some phases may stop at `A3` if no maintained provider automation is needed.

The practical split is simple: humans anchor the semantic oracle and the few high-consequence boundary decisions, while AI owns most of the repeated trial, hardening, and implementation work.

## TSP Requirement

Both `Big Ideas` and `Sessions` must expose:

- `Topic`: the central topic or subject
- `Scope`: the boundary of what is included and what is intentionally outside the current item
- `Purpose`: why this item exists and why it matters now

This is required because topic names alone are too weak for future continuity.

## Session "6x1" Adaptation

Each session should be understandable as a compact unit with:

- one coherent time-slice
- one topic
- one scope boundary
- one goal or purpose
- one durable record in the dashboard
- one summary outcome or exit criterion

Not every field must be rendered as a separate column, but the information must be recoverable from the row.

## Proposed Sessions

This repository uses proposed sessions intentionally.

That means a session row can exist before execution if:

- it is concrete enough to have a clear boundary
- it is valuable enough to deserve dashboard visibility
- it would be costly or easy to forget if left only in chat memory

It does not need to be the immediate next choice.

Avoid adding speculative low-value possibilities as sessions.

Proposed sessions are prioritized candidates, not execution commitments. A session can remain `To do`, be reprioritized, be split, be merged, or be marked `Cancelled` later as project priorities change.

Multiple high-priority sessions may be added after one task if the work reveals several concrete next steps. There is no one-session-per-task limit.

Within each Dashboard table, rows should stay in numeric ID order unless a file explicitly documents a different ordering rule. For `Sessions.md` and `Stage_Plans.md`, this means append new rows at their numbered position rather than leaving later-numbered rows stranded above earlier ones.

## Big Idea and Session Relationship

The relationship is vertical:

- `Session` is the time-based event or unit
- `Big Idea` is the meaning-based track or stream

Operationally:

- one `Big Idea` should usually contain multiple sessions over time
- one finished session usually advances a big idea rather than closing it
- after each meaningful task, new sessions may emerge under an existing big idea

In the governed execution model, `Big Idea -> Stage Plan -> Session / Session Unit` is the preferred execution hierarchy.

## Emergent Session Rule

High-priority new sessions should be added when they emerge from the actual state of the project.

A new session should be added if it is both:

- concrete enough to be executed in a bounded next step
- important enough that it deserves durable visibility, even if it is not the immediate next pick

Use the following emergence filter:

- `Necessity`: does the new session unblock or protect active work
- `Urgency`: does delay create rework, drift, or blind spots
- `Leverage`: does it improve multiple downstream sessions or big ideas
- `Value`: does it materially improve correctness, quality, lineage, or delivery
- `Freshness`: did it become visible only because the latest task moved the project forward

If at least one candidate scores strongly on several of these dimensions, it should usually be added to `Sessions.md`.

If several candidates satisfy the filter and are `P0` or `P1`, add all of the high-priority candidates that are concrete enough to be useful. Do not force the dashboard to choose only one when the project state has genuinely exposed multiple bounded next steps.

## Priority Rule

Sessions should carry explicit priority.

Use:

- `P0`: immediate next-step or blocker-clearing work
- `P1`: high-value near-term work
- `P2`: important but not immediate

New emergent sessions will most often be `P0` or `P1`, but a concrete `P2` candidate can still be added when it is easy to lose and likely to matter later.

## End-of-Task Dashboard Review

At the end of every non-trivial task, the LLM should explicitly ask:

1. Did any tracked session change status?
2. Did this task advance or reshape a big idea?
3. Did a new high-priority session emerge?
4. Should any existing session be reprioritized, split, merged, or archived?
5. Did any change belong in `Decisions.md` instead of `Sessions.md`?
6. Did this task change the current stage plan, risk picture, quality metrics, automation state, or exception ledger?
7. Did tracked or non-trivial governed work run the Multi-Agent Activation Gate before substantial work?
8. Did Design, Builder, Validation, and Closure lanes actually run, or was a `Single-Agent Exception` recorded?
9. Did every post-C0 implementation task have a saved Design Artifact / Design Handoff, and did every non-trivial task have a lightweight Validation Handoff Packet for final validation stored in the Dashboard closeout artifact?
10. For Goals, Stage Plans, or tracked Sessions, did the closeout include a Goal Scope Ledger / Original Plan Coverage Matrix and a Scope Delta Review?
11. If any original must-have was not landed, did the Dashboard row avoid inventing a special status phrase and instead rewrite the row to the actual landed scope, track any still-concrete remainder as a separate session, or record the human-approved deferral, blocker, not-applicable, or cancellation reason?
12. Did non-trivial governed work create or update the closeout artifact and reference it from the changed Dashboard row?
13. If a semantic-risk trigger was visible, was Semantic Reviewer started or was the decision not to start it recorded in the closeout artifact?
14. If Agent Log default applied, were logs appended for each participating agent or lane? If not, did the closeout explicitly justify the summary-level exception?
15. Did the closeout artifact run `closeout-language`, use Chinese H1/H2 headings, explain English verdict/status labels in Chinese, and record `Closeout language verdict`?

If the answer to question 3 is yes, add the new session immediately.

If the answer is no, state that no high-priority emergent session was identified.

If the answer to question 4 is yes because a session landed only through scope narrowing, update the completed row to the shipped subset and add the follow-on session in the same task.
