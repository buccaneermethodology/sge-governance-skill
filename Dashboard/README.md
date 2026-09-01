# Semx Dashboard

This directory is the execution-control layer for Semx.

It is not canonical truth. Stable architecture, pipeline, contracts, and terminology still live in `semx-kb/`.

This dashboard borrows the `Big Ideas` and `Sessions` framing from the Exploration Dashboard style, and adds a separate `Decisions` ledger because Semx currently has several architecture and rollout choices that should not be mixed into task rows.

In the current experiment, the dashboard also acts as the governance layer for low-intervention agentic execution:

- upper layer: strategic tracks, decisions, risks, quality metrics, automation state
- middle layer: stage plans that freeze a bounded execution batch
- lower layer: sessions, session units, exceptions, and agent logs

## Purpose

- Track implementation status without polluting canonical KB.
- Keep long-running themes, bounded sessions, and open decisions separate.
- Make it obvious what is `todo`, `doing`, `blocked`, `decision-needed`, or `done`.
- Force completed work to end in code, KB, or ADR-level artifacts instead of staying as dashboard-only state.
- Keep `Big Ideas` more stable than `Sessions`; sessions are expected to emerge as the project advances.

## File Map

- `Big_Ideas.md`: long-running implementation streams.
- `Stage_Plans.md`: bounded batch-execution contracts for multi-agent work.
- `Sessions.md`: bounded execution units, usually closable in one PR or one focused work cycle.
- `Decisions.md`: pending or resolved implementation decisions.
- `Risks.md`: active governance risks that could distort quality or execution.
- `Exceptions.md`: exception and escalation records produced by governed execution.
- `Quality_Metrics.md`: quality thresholds and observed control signals for agentic execution.
- `Automation.md`: automation coverage, human checkpoint rates, and intervention accounting.
- `External_Artifacts.md`: repo-visible pointers for intentionally local or ignored deliverables that still need durable closeout references.
- `Artifacts/`: session, Stage Plan, and Big Idea output artifacts such as closeouts, proposals, reports, reviews, explainers, and articles.
- `Agent_Logs/`: append-only per-agent execution logs in Markdown.
- `Methodology.md`: durable definitions for Dashboard, Big Ideas, Sessions, TSP, and emergent session handling.
- `Rules.md`: maintenance rules, status definitions, and placement rules.

## How To Use

1. Read `semx-kb/` for stable truth.
2. Read `Methodology.md` to align on dashboard semantics.
3. Read `Decisions.md` before starting major implementation work.
4. If work is agentic and low-intervention, read `Stage_Plans.md` before selecting concrete sessions or session units.
5. Pick the highest-priority open row from `Sessions.md`, or let the current stage plan fan out bounded session units.
6. Update rows in the same PR that changes code or KB, and append agent logs for each participating agent.
7. When a Big Idea is complete, move its durable outcome into code, KB, or ADR-style docs.

## Modeling Bias

- `Big Ideas` should usually represent durable streams, not first deliverables.
- `Stage Plans` freeze batch execution boundaries; they do not replace canonical contracts in `semx-kb/`.
- `Sessions` are expected to be incomplete at the start and to grow over time as new work emerges.
- Finishing one session usually advances a Big Idea; it does not automatically close it.
- A Big Idea may close after one session only when it is intentionally a one-off governance or decision artifact.
- Both `Big Ideas` and `Sessions` should expose TSP: `Topic`, `Scope`, and `Purpose`.
- High-priority new sessions should emerge from actual progress, not from speculative backlog growth.
- Agent logs record visible workflow and original outputs, not model-private chain-of-thought.

## Current Snapshot

- Maintained runtime and governed validation now exist through the first bounded P05 path: `SP-011` / `S-077` landed guarded ECCN `05_m1_candidates` extraction over maintained `02_m05_units` plus `04_semantic_slices`, with real LLMAPI A1 evidence and deterministic acceptance gates.
- The dashboard-governed execution model is no longer experimental bootstrap only: `SP-001` through `SP-010` established the current batch pattern, and `S-087` added a repo-local checkpoint skill so oracle review and deferred-follow-on capture stop depending on rule recall alone.
- The validation surface now has a landed six-layer taxonomy and maintained deterministic runner from `S-088`, so operators can distinguish unit seams, schema/example contracts, phase acceptance gates, runtime-line regressions, runtime-oracle regressions, and repo/facade/matrix gates before the acceptance line grows wider.
- Generalization is still represented by explicit phase-owned candidate Stage Plans: `SP-013` for P00 repo-entry generalization, `SP-014` for P01 evidence generalization, `SP-015` for P02 M0.5 generalization, `SP-016` for P03 semantic-flow generalization, `SP-017` for P04 semantic-slice generalization, and `SP-018` for the new P05 calibration-to-generalization transition. The latest closed three-repo tranche was `SP-012`, which temporarily pulled `S-103` through `S-117` upstream slices into one governed P00-P05 batch instead of treating P05 as a separate container.
- Several concrete slices remain intentionally visible after `SP-012` closeout: `SP-018` / `S-127` through `S-131` have now closed the first P05 pattern-level generalization pack after the landed github+exa readiness pair, while `S-086` still records guarded P04 oracle wording/taxonomy refinement and `S-089` / `S-090` through `S-092` keep prompt-surface parity plus compatibility/taxonomy cleanup options visible. `S-137` and `S-138` closed the readiness v1.1 / v2 C0 follow-on review, `S-140` hardened the seed-profile regression, `S-141` / `S-142` added artifact-level v1.1/v2 review fixtures, `S-143` / `S-144` promoted those lanes into bounded executable follow-on profiles, `S-145` approved a classification-only generic cross-family readiness router C0, and `S-146` / `S-147` / `S-148` / `S-149` / `S-150` / `S-151` have now advanced that boundary into typed structured disclosure, explicit route disposition, full lineaged reject/review carriers, and additive maintained candidate detection while continuing to reject generic validation.

## Current Focus

- Treat the closed `SP-011` / `S-077` P05 path as the current bounded baseline rather than as generic P05 coverage.
- Treat closed `SP-012` as the latest proof that the three required repos can be governed end to end through maintained `P05`, rather than as an always-active container that still owns hidden backlog.
- Keep the newly frozen P04 boundary honest while deferring non-blocking oracle and taxonomy refinements to tracked follow-on sessions instead of silent in-place edits.
- Use the landed `S-088` validation taxonomy as the operator baseline when adding future gates.
- `SP-012` is now closed for its bounded three-repo tranche. Raw TBC, raw ECCN, and raw Co-Sight each run from repo input through maintained `P00-P05`, the generalized P05 matrix is green for all three repos, and the repo-level extract facade is green through maintained `P05`.
- The upstream P04 calibration history remains visible and landed: the historical `A1` adequacy record lives at `Dashboard/Artifacts/SP012_P04_CoSight_CreatePlan_A1_Adequacy_Report.md`, the executable semantic-oracle hardening record remains at `Dashboard/Artifacts/SP012_P04_CoSight_CreatePlan_A2_Hardening_Proposal.md`, and the bounded runtime-promotion / handoff record lives at `Dashboard/Artifacts/SP012_P04_CoSight_CreatePlan_A3_Runtime_Promotion.md`.
- The downstream P05 closeout is now explicit too: `semx/phases/m1_candidate.py` emits the reviewed Co-Sight `create_plan` candidate surface, `tests/contract/p05_runtime_matrix_regression.py` covers TBC/ECCN/Co-Sight, and `semx extract semantic-slice` plus `semx extract m1-candidates` are now maintained thin wrappers. See `Dashboard/Artifacts/SP012_P05_A3_A4_Closeout.md`.
- `S-080`, `S-100`, `S-101`, and `S-102` are now all landed under `SP-012`, so there is no hidden remaining P05/facade work inside this tranche.
- The PRE governance follow-on has now landed as `S-121`: glossary, strategy, acceptance, and repo-local checkpoint guidance all distinguish semantic-oracle seed from executable semantic oracle, scope the split mainly to reviewed semantic-rich surfaces, and codify the A1 -> A2 pivot away from prompt micro-tuning once the remaining drift is deterministic/canonical rather than semantic.
- The review-experience follow-on has landed as `S-119`: `semx extract ...` now emits `artifact_stats.json` under `report_dir`, and `semx inspect early-phase-stats <artifact>` exposes the same deterministic counts/distributions as a maintained operator-facing summary surface.
- The first post-tranche Agent-Reach widening has now expanded into a bounded pair: `S-122` froze `GitHubChannel.check`, `S-123` turned it into a maintained raw-repo `P05` baseline, `S-124` then froze `ExaSearchChannel.check`, and `S-125` turned that second freeze into a maintained Exa Search baseline that now sits beside the retained github readiness candidate in the same raw-repo matrix and extract-facade proof.
- `S-120` is now closed too: `semx semantic-slice-candidate` supports `--prompt-template-override-file`, preserves default-versus-active template provenance in `run.json`, and can replay reviewed prompt-template revisions without ad hoc patching.
- The broader heterogeneous Agent-Reach `check()` family still remains deferred as maintained truth. `SP-018` is now closed with an explicit transition result: `S-128` approved `Backend Readiness Assessment Pattern v1` as a C0 seed, `S-129` approved the first router C0 proposal, `S-130` landed the first executable readiness profile over the reviewed github + exa seed pair, `S-131` classified heterogeneous stress samples without silently widening v1, `S-137` / `S-138` split the next readiness variants into v1.1/v2 C0 lanes, `S-140` hardened the maintained profile regression, `S-141` / `S-142` landed follow-on artifact fixture gates, `S-143` / `S-144` promoted those reviewed lanes into bounded executable follow-on profiles, `S-145` approved the classification-only generic routing boundary, and `S-146` / `S-147` / `S-148` / `S-149` / `S-150` / `S-151` turned that boundary into typed route-family disclosure, explicit route disposition, full lineaged reject/review carriers, additive maintained detection, and maintained generic-router regression while still rejecting generic validation.
- Return to the quality-loop frontier through `S-006`, prefer `S-136` when the next move is broader negative-fixture backfill, or revisit `S-089` / `S-090` through `S-092` by an explicit next planning choice rather than hidden widening.
