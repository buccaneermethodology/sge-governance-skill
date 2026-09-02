# Dashboard Rules

## Placement Rules

- Put stable truth in `kb/`, not here.
- Put implementation tracking, sequencing, blockers, and pending choices here.
- Put ad hoc one-off work logs in PRs or commits, not here.
- Put repeatable agent-execution logs in `Dashboard/Agent_Logs/` by default for non-trivial governed multi-agent execution, tracked Session / Stage Plan execution that starts lanes, and triggered Semantic Reviewer lanes.
- If a row changes project truth, the end state must be reflected in `kb/` or an explicit decision artifact.

## Record Types

- `Big Idea`: a long-running stream that may span multiple sessions.
- `Stage Plan`: a bounded batch-execution contract for agentic work.
- `Session`: a bounded unit of work with a clear exit criterion.
- `Decision`: a choice that can block or distort multiple sessions if left implicit.
- `Dashboard Agent report`: a read-mostly strategic synthesis and update-proposal surface; it is not canonical truth and does not become Dashboard state until the human asks for an update.

## Required Semantics

- Future contributors should be able to use the dashboard correctly without chat history.
- Therefore the dashboard must preserve explicit methodology, not just current rows.
- `Dashboard/Methodology.md` is the durable reference for BM-style semantics in this repository.

## Hierarchy Rules

- Treat `Big Ideas` as more stable than `Sessions`.
- A `Big Idea` should usually represent a stream or outcome area, not the first artifact produced inside that area.
- New sessions may be added under an existing `Big Idea` at any time as the work reveals new needs.
- Completing one session usually advances a `Big Idea`; it should not automatically mark the `Big Idea` as `done`.
- Mark a `Big Idea` as `done` only when its stream-level exit criterion is satisfied for the current implementation phase.
- Exception: a governance or one-off decision idea may close after a single session, but that should be explicit in `Notes`.

## Status Vocabulary

Dashboard status cells are for human filtering only. Use exactly these four display values in `Status` columns:

- `To do`: ready, proposed, blocked on a future decision, or not currently owned.
- `Doing`: currently being worked.
- `Done`: the row's current written scope is complete and reflected in code, KB, Dashboard evidence, or another durable artifact.
- `Cancelled`: was tracked on purpose, but later proved unnecessary, superseded, invalidated, archived, or no longer worth doing.

Do not encode claim ceilings, caveats, boundedness, topology exceptions, approval state, blocker type, or review verdicts in the `Status` cell. Put those details in `Scope`, `Exit Criteria`, `Next Step`, `Notes`, closeout artifacts, or an explicit claim/coverage artifact instead.

## Row Rules

- Every row must have an `ID`.
- Session records additionally use a globally unique `Session Key`. Its format is `<Parent Stage Plan>/<Historical ID>` when a parent is known, for example `SP-063/S-478`; legacy rows without a recoverable parent use `LEGACY/<Historical ID>`. `Historical ID` is a compatibility/search alias and may collide across parent Stage Plans, so tools must never silently choose the first match.
- The active Session registry is split across three execution-memory surfaces: `Sessions.md` is current/recent work, `Session_Index.md` is the compact all-Session locator, and `Archives/Sessions/*.md` preserves complete closed history. None of these surfaces is canonical KB truth.
- A Session registry parser or projection must fail closed on duplicate `Session Key`, malformed rows, unknown status mappings, missing index/archive locations, or current/index/archive count drift. Duplicate `Historical ID` is legal only when each record has a distinct parent-qualified `Session Key`.
- 新建、更新、关闭、归档 Session 或改动 registry 任一表面时，先运行 `reconcile --check` 与 `validate`；若编辑造成可重建派生 drift，仅可在预检无 error 时显式运行 `reconcile --apply`，随后重跑两项检查。任一命令非零时不得把受影响 Session 标为 `Done` 或等价关闭。
- duplicate canonical key、malformed row、unknown Status、ambiguous identity、unexpected archive surface 或历史说明表面错误必须人工处理；日常 `--apply` 不得猜测、first-wins、删除未知 archive 文件或改写 `Legacy_Execution_Notes.md`。
- registry check/validate 通过后，若 Dashboard KG / DKG 受影响，才以 `Dashboard/tools/generate_dashboard_kg.py` 的显式输出路径重建 DKG 并运行 focused registry gate；reconcile 不生成 DKG，DKG 也不是 registry 真源。
- 本仓库不提供历史迁移命令；`reconcile --check/--apply` 只维护当前 SGE Dashboard registry，禁止隐式执行外部迁移或 locator rewrite。
- Stable links to Session history should use `Session_Index.md` or an archive anchor. Line-number links into `Sessions.md` are not stable after archival.
- Rows in the same table should remain in numeric ID order unless that file explicitly documents another ordering scheme.
- Every `Big Idea`, `Stage Plan`, and `Session` row must expose `Topic`, `Scope`, and `Purpose`.
- Every row must define a concrete `Exit Criteria`.
- Every `Doing` row should have a single next action.
- Sessions should be small enough to close in one focused implementation cycle.
- If a session lands only through intentional scope narrowing, rewrite the row to the shipped subset before marking it `Done`, and create a follow-on session for the deferred remainder when it is still concrete and relevant. If the remainder is no longer needed, record the reason in `Notes`.
- For non-trivial Goals, Stage Plans, and tracked Sessions, preserve original objective coverage through a Goal Scope Ledger and an Original Plan Coverage Matrix in the closeout artifact.
- Treat deleted, renamed, replaced, downgraded, postponed, newly excluded, or must-have-to-non-goal items as Scope Delta and record the original requirement, revised target, reason, impact, approval status, and deferred session or blocker.
- Do not use a `Done` row to imply the original broader objective completed when the row has been intentionally narrowed. The completed row text must describe the actual landed bounded scope, and the unlanded remainder must be either tracked as a separate session, explicitly marked not applicable, blocked by a termination condition, or explained in `Notes` with human-approved deferral/cancellation rationale.
- Big Ideas should point to one or more concrete sessions.
- Stage Plans should point to one or more concrete sessions or explicitly bounded session units.
- Decisions should state the recommended option even when unresolved.
- Sessions should carry explicit priority.
- Standing user authorization applies to future SGE non-trivial governed tasks: AI is explicitly authorized to use subagents / delegation as needed, subject to the Multi-Agent Activation Gate.
- AI may decide to start subagents / delegation for tracked Session, Stage Plan, or non-trivial governed work even when the user has not explicitly asked for subagents. A user request to execute or start a tracked Session or Stage Plan, such as `执行 S-xxx`, `启动 S-xxx`, `execute S-xxx`, or `执行 SP-xxx`, is sufficient authorization for governed multi-agent execution by default unless the user says single-agent or no multi-agent.
- Before substantial work on a tracked Session, Stage Plan, or non-trivial governed task, run a Multi-Agent Activation Gate. If the task changes KB truth, Dashboard state, acceptance posture, fixtures/tests, runtime/schema behavior, or requires design handoff, validation handoff, or closeout artifact, start Design, Builder, Validation, and Closure lanes by default. C0 approval automatically enters this governed implementation mode unless the user says single-agent / no multi-agent or the task is truly trivial. Do not treat the absence of an explicit subagent request as a valid Single-Agent Exception by itself.
- If a default Design / Builder / Validation / Closure lane is not started, record a `Single-Agent Exception` in the closeout artifact with the reason, risk, compensating checks, and whether an independent Design artifact or Validation verdict is missing. Valid reasons include explicit human single-agent direction, true triviality, or a concrete external runtime/tool constraint.
- After a short local decomposition, prefer design, builder, validation, and closure lanes over default read-only explorer lanes unless the task is genuinely exploratory.
- Non-trivial governed batches should usually include at least one Design Agent lane, one Validation Agent lane, and one Closure Agent lane unless the task is intentionally single-agent or too small to justify the split.
- Every non-trivial task should provide a lightweight `Validation Handoff Packet` before final validation: original objective coverage when a Goal/Stage Plan/tracked Session is involved, claimed scope, Scope Delta if any, claimed semantic change, explicit non-goals, files/artifacts changed, gates/tests run, evidence produced, known risks, KB/Dashboard impact, and `Closeout language verdict`. Store it by default in the task's Dashboard closeout artifact under a `验证交接包` section.
- A `Validation Handoff Packet` is input to Validation, not a Validation Agent verdict. Do not claim Validation passed unless an independent Validation lane actually reviewed the work or an explicit single-agent exception says validation was not independently run.
- Validation lanes should start early enough to inspect substantive work before final closeout, and their verdict should be treated as a gate rather than optional commentary.
- Validation Agent lanes must apply the fixed Validation Agent Prompt: build a Read Manifest, explain the task in Chinese for the human owner, check original objective coverage and landed evidence, identify blocking/non-blocking issues, and keep verdict wording evidence-bound.
- If mandatory evidence is incomplete under Orchestrator pressure, Validation Agent may only close as `blocked` or `partial` and must report the missing evidence; it must not write `pass`, `done`, `SP complete`, or `Goal complete`.
- Semantic Reviewer is a separate read-mostly semantic-governance lane, started by human request, Stage Plan requirement, or recorded semantic-risk escalation. It is not mandatory for every non-trivial task by default.
- Semantic-risk triggers include capability widening, genericization, semantic promotion, acceptance posture or gate-strictness change, oracle/golden freeze, phase calibration promotion, major canonical KB truth change, hidden widening, accidental generalization, or future drift risk. If such a trigger is visible and Semantic Reviewer is not started, record why in closeout or the relevant row.
- When Semantic Reviewer runs, it first performs Semantic Architecture Review: truth carrier placement, law/witness/evaluation/governance split, long-term complexity trajectory, God Object drift, semantic bureaucracy, half-schema/DSL drift, invariant law quality, and capability-family algebra.
- When Semantic Reviewer runs, it first challenges the artifact frame before local consistency review: authority level, layer split, core ontology, claim/evidence mapping, semantic invariants, generalization failure taxonomy, transfer rules, negative space, likely future misuse, and promotion boundary. Missing layer split, ontology, invariant model, failure taxonomy, or transfer rules in high-risk artifacts are findings.
- Dashboard Agent is a separate strategic Dashboard lane for full-dashboard refresh, macro next-step guidance, stale-row audit, and blue-sky candidate generation. It defaults to proposal-only updates: do not write archive/cancel/rewrite/add changes unless the human explicitly asks to update the Dashboard.
- Dashboard Agent next-step guidance should default to three candidate options: one quality/stability move, one speed/progress move, and one blue-sky move beyond the currently landed Dashboard when useful.
- Every non-trivial governed task that changes a tracked session, Stage Plan, KB truth, acceptance posture, fixture/test pack, or substantive Dashboard state should create or update a concise closeout artifact under `Dashboard/Artifacts/`. Use `Dashboard/Artifacts/<SessionID>_<ShortTopic>_Closeout.md` for a single session and `Dashboard/Artifacts/<StageID>_<ShortTopic>_Closeout.md` for a Stage Plan or multi-session batch. The artifact should use Chinese headings by default, including `关键结论中文展开`, `落地范围`, `原始目标覆盖矩阵` when applicable, `范围变更复核`, `Lane 启动与例外`, `设计交接`, `验证交接包`, `验证结论`, `明确非目标`, `证据`, `运行的门禁`, `语义复核`, `延后范围`, `KB/Dashboard 复核`, and `后续候选`.
- All task closeout artifacts and final closeout summaries should be written in Chinese by default. If lane outputs or command evidence are in English, translate or summarize them into Chinese in the closeout, preserving exact English only when it is necessary evidence.
- User-facing Dashboard closeouts and final summaries should include a reader-facing Chinese explanation layer when they contain compressed conclusions that affect human judgment. The closeout artifact should add `关键结论中文展开` when needed, explaining the original conclusion, its Chinese meaning, judgment impact, evidence or boundary, and next action.
- Reader-facing evidence citations in Closeout, final summaries, Dashboard parent/row prose, and `验证交接包` explanation must use clickable Markdown links to the exact source artifact, not bare SHA-256/hash/digest numbers. Keep machine-required digests in lane cards, manifests, snapshots, JSON, or validation reports and link to those files from the human-facing text; historical immutable artifacts may retain their original digests.
- Before final completion wording, run `guardrail_checklist.py --mode closeout-language --file <closeout.md>` against the closeout artifact. A missing, failed, blocked, pending, not-run, or non-explicit `Closeout language verdict` blocks final completion; pure-English H1/H2 headings and unexplained English verdict/status labels must be repaired first.
- This explanation layer is execution readability support. It does not make Dashboard memory canonical truth, does not replace evidence or gates, and does not change runtime/schema/acceptance behavior by itself.
- When a phase contract is still unstable, do not skip directly to a large maintained runtime implementation. Prefer the visible sequence `golden/oracle -> candidate trial -> acceptance hardening -> maintained runtime boundary/body -> formalized provider automation`.
- Real-provider prompt trials may be used during candidate trial when they are the clearest way to expose contract drift, but they do not become part of the deterministic acceptance posture itself, and scripted trial runs are still distinct from a formally maintained provider automation surface.
- When planning a new or unstable phase, treat `C0 -> A1 -> A2 -> C1 -> A3 -> A4` as the default delivery pattern unless the task explicitly justifies a narrower or reordered slice.
- When a task creates a new golden/oracle fixture, treat the first AI-authored version as a draft proposal until the human has reviewed or approved it, unless the human explicitly delegated the final semantic choice.

## Update Rules

- At the start of every user request, run a proportional `Task Intake Evaluation Gate` by default: check objective, source authority, boundaries, material risk, and execution route before action. Simple low-risk tasks may pass silently; persistent edits, proposal/approval text, contracts, KB/Dashboard, acceptance/gate, or semantic-promotion work should make the intake verdict explicit.
- At the end of every non-trivial task, explicitly review whether `kb/` or `Dashboard/` requires an update.
- For non-trivial Goals, Stage Plans, and tracked Sessions, run the Goal Conformance / Scope Delta Gate after C0 or initial design, before dominant Builder implementation, and before closeout; update Dashboard rows if the result is only a partial or approved-subset completion.
- Before final closeout, run a `Contract Delta Scan` when an approved proposal, closeout, reviewed seed, accepted baseline, matrix, contract, or acceptance/gate artifact contains stable contract, artifact semantics, trust/disposition, blocking/advisory, promotion, non-goal, reusable terminology, or policy claims. Record the KB JSON source decision: update KB JSON now, keep Dashboard-only with rationale, route to gate docs/runtime/tests, or add a deferred session.
- Update dashboard rows in the same PR that changes their status.
- When a session finishes, explicitly ask whether the parent `Big Idea` is now complete or whether follow-up sessions have emerged.
- When a session or Stage Plan row changes status because of non-trivial governed work, reference the closeout artifact in `Notes` or `Canonical Target`.
- When a task reveals one or more new `P0` or `P1` bounded next steps, add the concrete high-priority candidates as new sessions unless there is a strong reason not to.
- Also add a concrete `P2` candidate when losing track of it would create rediscovery cost or hidden debt, even if it is not likely to be selected immediately.
- Treat `To do` sessions as visible candidate next steps, not promises that the project must execute them later.
- If a tracked session later stops making sense, mark it `Cancelled` with a brief note instead of silently deleting it.
- Do not add speculative low-priority possibilities as sessions by default.
- If work starts, switch the row to `Doing`.
- If work stops on an unresolved choice, keep or switch the row to `To do` and put the decision/blocker in `Next Step`, `Notes`, `Decisions.md`, or the relevant closeout artifact.
- If work completes, mark the row `Done` and record the durable output path in `Notes` or `Canonical Target`.
- If work completes only for a bounded subset of the original row, update the row text to that bounded subset before marking it `Done`; add the deferred remainder as a new session when it remains concrete and relevant, or explain in `Notes` why it no longer needs tracking.
- On non-trivial governed batches, do not declare final closeout or promotion complete until validation has returned either a passing verdict or an explicit blocker/exception.
- Give validation a meaningful first review window; while waiting, use non-overlapping work instead of rushing the validator for a premature final verdict.
- For non-trivial closeout, do not emit next suggested `SP` / `Sessions` as bare IDs only. Include a short overview of each recommended candidate and a brief prioritization reason explaining why it currently ranks ahead of other visible open sessions.
- Apply that next-suggestion requirement even when the completed task was not run under an explicitly named active Stage Plan. If no plausible candidate exists, say so explicitly instead of silently omitting the recommendation.
- If a task lands only part of the contract-calibration sequence, describe the landed subset honestly in the completed row and add any still-concrete remainder as a follow-on session rather than implying the full runtime line is already stable.
- Before final closeout of a non-trivial task, run the repo-local checkpoint checklist or perform its equivalent scan explicitly so narrowed scope, deferred follow-ons, and later candidate sessions do not stay implicit.
- If non-trivial governed multi-agent work occurs, tracked Session / Stage Plan lanes start, or a Semantic Reviewer lane is triggered, append one Markdown log per participating agent or lane under `Dashboard/Agent_Logs/`.
- Agent logs must preserve a high-fidelity visible execution trace, not a condensed after-the-fact summary: visible working notes and final output should be kept verbatim, with tool actions, gate results, artifacts, risks, repairs, and checkpoint decisions detailed enough for later audit. Use `Dashboard/Agent_Logs/2026-04-15__S-055__main-agent.md` as the reference example for expected detail. Agent logs must not claim to preserve model-private chain-of-thought.
- Agent Logs should include the Validation Handoff Packet or a link to it, including `Closeout language verdict` when a closeout artifact exists, plus any Semantic Reviewer concerns, risk discoveries, required repairs, escalation reasons, and promotion recommendation.
- If work is trivial, low-risk, single-agent summary-level, or has no Dashboard/KB/contract/gate/semantic-promotion impact, keep it at summary level and state why a full Agent Log was not needed instead of manufacturing logs.
- Avoid free-form narrative growth; prefer concise table updates.
- Do not append SP execution chronology, hashes, repeated closeout status overlays, or task-by-task prose outside the Session table. Put current/terminal state in the row and parent surfaces, detailed repeatable execution in `Agent_Logs/` or closeout artifacts, and closed historical prose in `Archives/Sessions/Legacy_Execution_Notes.md`.

## Emergent Session Heuristic

- Add a new session when it is newly visible and scores highly on necessity, urgency, leverage, or value.
- Prefer adding sessions that are likely to be chosen in the next one to three work cycles.
- If several candidates emerge, add the highest-priority concrete candidates; lower-priority or speculative candidates can be captured later if they remain relevant.

## SGE Governance Boundary

- `Dashboard/` is the execution layer.
- `kb/` is the canonical semantic and contract layer.
- The dashboard may reference KB docs, but it must not redefine them.
- Stage plans, metrics, risks, exceptions, and agent logs belong to Dashboard governance unless and until they become stable project truth.
