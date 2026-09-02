# Operator Runbook

## Current State

Read `engine/data/work-instance.yaml` first. While its phase is `engine_revision`,
mutate only its declared write roots. Do not generate work canon, generation planning
artifacts, prose, a graph, or Astro story pages.

## End-User Run

From the Cathedrals installation, run:

```bash
./cathedrals
```

The executable asks only for project name, free-text genre/flavor, possible scene
scope, and story format. Visual-novel aliases are currently recorded but resolve to
the active web format. Model selection, when needed, is operational. After the brief
freezes, the executable asks no creative questions.

It then owns this sequence:

1. Create an independent generation ID and copy the current local launcher and engine
   into `.cathedrals/runs/<generation-id>/engine-snapshot/`.
2. Use that run-local snapshot for prompts, schemas, canon, formats, and resume.
3. Freeze the initial experience request as `generation_brief.mutable: false`.
4. Derive resource budgets from the explicit possible-scene scope; profile labels are
   guidance and never clamp the requested scope.
5. Verify documented model context/output limits; calculate per-step and cumulative
   token, literary-word, constraint-event, retrieval, and configured cost budgets.
6. Deterministically prepare abstract topology/state capacity and all relevant
   threshold-geomancy assignments.
7. Write the immutable run manifest, initialize counters, and start the ledger.
8. Make and commit the bounded Genesis foundation, cast, and constraint calls.
9. Make and commit the bounded Architecture core and every plan batch; freeze topology,
   attractors, hard obligations, and packet dependencies without freezing tentative realization order.
10. Assemble constraint-relevant contexts and execute each dependency-lawful packet
    selected by the current prospective plan. Append constraint and ledger records.
11. After every commit, update fact/knowledge/obligation/motif state and recompute
    audited future feasibility without changing canon.
12. Generate endings only after their prerequisite histories commit.
13. Deterministically project all committed content and validate protocol, hashes,
    graph, technical destinations, state, counts, Markdown, constraint provenance, and budgets.
14. Compile and validate the complete static Astro site.
15. Perform whole-work artistic acceptance without a repair prompt.
16. On success publish only the new generated-work tree. Write
    `finalization.json`: `READY_TO_PLAY` only after every barrier passes;
    otherwise `FAILED_GENERATION` with `playable: false`.

An artistically rejected complete work keeps its build under ignored run storage for
diagnosis. It is never copied to accepted publication paths or described as playable.

Do not pause for creative approval. A valid but ugly packet commits. A run either
completes or dies.

The runner talks directly to LM Studio. It does not invoke Pi, Codex, CrewAI, or an
agent framework. Interrupted runs are detected under `.cathedrals/runs/`; resuming
reuses the run-local engine snapshot, frozen model, prompt hashes, seeds, ledger, and
committed records.

## Provenance and Counters

Every attempted step records generation ID, ledger sequence, planned step and attempt,
type/phase, parent hashes, prompt/context hashes, provider/model/parameters/seed,
timestamps, output hash, generated IDs, past/future/motif deltas, prospective-plan hash, branch relation,
commit status, failure class, and token/cost accounting.

`READY_TO_PLAY` requires zero human interventions, committed rewrites, committed
regenerations, and backtracks. `creative_step_count` may exceed one.

## Lawful Retry

Retry only a transport failure or provider failure before creative output. Keep the
same planned step, prompt, context, parameters, and seed; increment only attempt and
audit data. Malformed output, artistic disappointment, or continuity trouble is not a
retry condition.

## Stop Conditions

Stop before creative generation for engine conflict, mutable/missing brief, failing
preflight, missing deterministic inputs, insufficient model limits, candidate-
selection logic, or forbidden phase writes. During the run, stop as
`FAILED_GENERATION` for malformed creative output, exhausted frozen resources,
unresolvable continuity, mechanical failure, artistic rejection, or build failure.

Do not stop for ordinary fictional choices. They belong to autonomous generation.
