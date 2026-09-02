# Generation Workflow Contract

## Invariant

One pass means one autonomous generation run: frozen inputs progress causally forward
until completion or failure, with no human creative steering and no mutation,
replacement, regeneration, or candidate selection after a creative artifact commits.
Response count is not the invariant. A run may contain many creative calls.

> **Cathedrals reasons backward about what the future must earn, but writes forward
> into a history it cannot revise.**

The externally visible experience is always:

```text
one experience request -> complete autonomous generation -> validation and static build
-> READY_TO_PLAY or FAILED_GENERATION
```

Generation and play never overlap. The current executable always composes and builds
the web format. A visual-novel request alias is retained in the frozen brief but
resolves to `story_format: web` until a future Ren'Py engine revision is implemented.

## 1. Frozen Request and Preflight

Convert the initial request and allowed settings into an immutable `generation_brief`.
Requests such as `survival horror` and `surprise me` are sufficient. The brief may
constrain genre, tone, scale, intensity, content boundaries, pacing, seed, and desired
experience. It must not require claimant identities, plot events, clues, artifacts,
endings, or scene activity. Set `generation_brief.mutable` to `false` before the run.

Freeze and hash:

- the brief and generation ID
- the run-local copy of all active engine inputs
- work, structural, traversal, and geomancy seeds
- explicit possible-scene scope, profile-derived guidance, and cumulative run limits
- provider/model parameters and documented context/output limits
- deterministic abstract topology and threshold-geomancy inputs
- prompt templates and `engine/data/generation-protocol.schema.json`

Prompt templates are immutable run inputs. If any prompt hash changes after start,
fail the run; never pause between steps for a human to edit a prompt.

Preflight every planned creative step, not the whole work as one response:

```text
prepared_context_tokens + max_packet_output_tokens + safety_reserve_tokens
<= selected_model_context_window_tokens

max_packet_output_tokens <= selected_model_max_output_tokens
```

Also prove that planned steps fit the derived total creative-step, literary-word,
input-token, output-token, constraint-event, retrieval, and configured cost ceilings. Failure
stops before creative generation.

## 2. Append-Only Run

Create `generated-work/<generation-id>/run-ledger.jsonl`. Each line validates against
the ledger-entry record in the protocol schema and is chained by SHA-256. The ledger
records every creative, analysis, prospective-plan, validation, build, and finalization step.

A technical retry keeps the same planned step ID, prompt/context hashes, parameters,
and seed, while incrementing `attempt`. A creative step counts when valid output is
committed. Failed attempts remain visible in the ledger.

### Phase A — Bounded Genesis

Commit three causally linked records: a foundation containing work canon, web art
direction, and five claimant anchors; one cast record expanding all five claimants
together plus significant characters; then a minimal source-grounded constraint
record. Each commit is immutable. Completed Genesis is their deterministic assembled
view, headed by the constraint commit.

### Phase B — Macroarchitecture

Using frozen engine canon and completed Genesis, commit a bounded macroarchitecture
core containing topology, arcs, attractors, and initial obligations. Deterministically
preallocate content slots, then commit packet plans in batches of at most eight.
Attractors freeze terminal transformations rather than terminal choreography. All
plan batches commit before literary prose begins; tentative realization order is not
canonical.

### Phase C — Forward Literary Packets

Choose the next dependency-lawful packet from the current prospective plan. A planned
packet contains three to eight related scenes, normally six, plus associated artifacts,
formal compositions, and source-grounded constraint deltas. Its scenes share one
4,800-word allowance and have no individual word ceiling. Context is selected by constraint
relevance, not chronology. Commit a mechanically valid packet even when its art is
disappointing. Later packets may read and react to it; they may not replace it.

If the provider truncates an uncommitted packet, preserve the failed response and
deterministically bisect its remaining slots. Committed chunks collectively own the
original plan. A single-content truncation may retry once with a larger allowance only
when the frozen model context leaves the safety reserve intact.

After every creative commit: preserve source; apply fact and knowledge events; append
or resolve obligations; update motif pressure; evaluate viable/endangered/foreclosed/
universally-impossible attractors; recompute the noncanonical prospective plan; then
choose the next lawful packet. Recalculation never increments rewrite, regeneration,
or backtrack counters.

### Phase D — Endings and Residue

Generate final ending prose late, only for viable early attractors whose hard
prerequisites have source-cited satisfaction. Endings may interpret earlier evidence
and create consequences, but may not retcon it.

### Phase E — Validation and Static Build

Project committed records without literary change, validate hard integrity, links,
state, safety, and full-plan coverage, then build the dependency-free static reader.
Artistic and structural quality findings are warnings. A locked npm/Astro enhancement
is optional and cannot veto the baseline. On hard-gate success, publish only the new
generated-work tree before crossing the complete-work barrier.

## 3. Commit Semantics

A commit atomically preserves the raw response, validated protocol record, prompt and
context hashes, output hash, generated IDs, constraint deltas, canonical-state hashes,
and ledger entry. After that point the creative bytes and facts are history.

Later steps may read, quote, retrieve, reinterpret from a character's perspective,
contradict diegetically, or create consequences from committed material. They may not
rewrite, improve, regenerate, silently retcon, or discard it in favor of another
candidate. If awkwardness remains executable, the run lives with it. If immutable
history makes completion mechanically impossible, the run fails.

No call may generate several fictional candidates for scoring or selection. A valid
creative output consumes the possibility space and commits. Deterministic structural
selection before creative generation remains lawful.

## 4. Constraint Propagation and Context

The immutable creative records are source evidence. `constraint-events.jsonl` is an
append-only, source-hashed index of minimal past facts, tracked epistemic state, typed
future debt, motif pressure, and foreclosure evidence. Source truth always wins.

Architecture plans backward with the same recursive grammar used forward:

```text
desired residue ← consequence ← choice/deferment ← pressure ← interpretation ← encounter
```

This produces prerequisite obligations, never reverse-authored prose. Literary
authorship still commits forward only.

For each packet, deterministic weighted retrieval scores hard obligation/direct
dependency matches at 12, branch at 10, knowledge at 9, claimant/causal debt/attractor
prerequisite at 8, object/location at 6, motif at 5, lexical overlap variably, and
recency at no more than 2. It then retrieves original immutable source records and
locators. Thus Scene 130 may retrieve Scene 12 when Scene 12 constrains it.

Whole records are packed in this priority: engine law, brief, packet plan, hard past
constraints, hard future obligations, direct source evidence, relevant knowledge,
attractor prerequisites, original evidence, motif/branch residue, local recent prose,
soft pressure. A lower-priority section is omitted before a hard record is sliced.

Creative packets emit their own structured deltas. There is no routine secondary
index call. A future noncreative analysis call may classify constraints or feasibility
only if deterministic/packet-emitted data proves insufficient; it can never return
replacement prose.

## 5. Prospective Foreclosure

A committed fact may make a foreclosable attractor impossible. The packet remains
immutable. Foreclosure is lawful only when a cited immutable event negates a declared
prerequisite, no lawful realization remains, and the obligation is scoped to that
future. Universal hard obligations cannot be dropped; making one impossible causes
`FAILED_GENERATION`. Foreclosure changes future feasibility, not history.

## 6. Failures and Terminal States

- Transport failure before a response: retry the identical planned step.
- Provider failure before creative output: retry the identical planned step.
- Malformed or unparseable creative output: record it and `FAILED_GENERATION`; do not
  creatively repair or resample.
- Mechanically valid but weak art: commit and continue.
- Lawful diegetic contradiction: preserve and continue.
- Unresolvable mechanical continuity impossibility: `FAILED_GENERATION`; do not retcon.
- Artistic weakness: publish with warnings; no repair loop.
- Correctable uncommitted provider, schema, or build trouble: `PAUSED_GENERATION`.
- Irrecoverable committed-history corruption or hard-budget exhaustion: `FAILED_GENERATION`.
  An engine defect may be fixed only in a later engine revision, never by altering the
  committed work.

The terminal states are `READY_TO_PLAY` and `FAILED_GENERATION`.
`PAUSED_GENERATION` is resumable and never writes finalization.

Every new attempt copies the current local launcher and engine into
`.cathedrals/runs/<generation-id>/engine-snapshot/`. Resume uses that run-local copy and
does not inspect the installation. Runs never descend from or modify one another.

## 7. Complete-Work Barrier

Before `READY_TO_PLAY`, all generated canon, claimants, characters, architecture,
scenes, artifacts, formal compositions, endings, state-dependent variants, lawful
branches, graph data, projections, hard validations, static baseline, and build
validation must exist and pass.

Never expose partial play, generate a chapter after player input, observe play to
complete the work, or defer an unvisited branch until runtime. Every playable choice
points to prebuilt content or deterministic state behavior. The completed reader uses
no LLM, API, database, or server-side story logic.

## Human Escalation

Once the run starts, ask no creative questions. Before a run, ask only for missing
engine-level doctrine, technical authority, safety/legal constraints, or a genuinely
required initial experience choice. Ordinary fictional uncertainty belongs to the
generator.

## README Interpretation

Engine law operationally interprets README `one pass` as one uninterrupted,
forward-only generation run rather than one response. This preserves irreversibility
and surrendered human control but remains in textual tension with README language
that says all scenes and arcs are generated in a single pass and forbids prompting
one scene and then the next. The root README is not edited or silently redefined.
