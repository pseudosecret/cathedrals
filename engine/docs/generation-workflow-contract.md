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
direction, and five to eight claimant anchors; one cast record expanding every initial
claimant together plus significant characters; then a minimal source-grounded
constraint record. Before that final record commits, invalid semantic references are
resolved to committed claimants or characters when possible. A genuinely distinct
world-logic may instead promote an existing character or add a new claimant, up to a
twelve-claimant maximum; the extension commits atomically in the same constraints
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
formal compositions, and source-grounded constraint deltas. Author and commit that
logical packet as deterministic one-scene chunks with exact response cardinalities.
Distribute artifact/composition totals across the chunks. Each scene or ending chunk
may contain up to 1,200 combined literary words, including its nested artifacts. The
logical packet's 4,800-word target is pacing guidance; it is not a shared hard ceiling
or an equal per-scene allocation. The whole-work literary ceiling is 1,200 times the
sum of the requested possible scene count and derived maximum ending count. Artifact
words are already included in chunks and are not budgeted twice.

Validate schema, allocation, Markdown, literary length, and technical references
before staging immutable artistic prose or requesting semantic normalization. Invalid
uncommitted prose receives bounded corrections; normalization only repairs metadata
and never changes literary bytes. Context is selected by constraint relevance, not
chronology. Commit a mechanically valid chunk even when its art is disappointing.
Later chunks may read and
react to it; they may not replace it.

Before commit, every phase resolves eligible invalid reference fields against typed
catalogs of declared, in-scope targets. Deterministic aliases run first. Remaining
unknown references receive the focused `resolve-reference.md` prompt: one invalid
value, its field and usage context, and bounded candidates with descriptions. The
response must be one exact listed identifier or `UNRESOLVED`; explanations and new
identifiers fail validation. Only the identified field changes. Declaration IDs,
free-form fictional labels, and literary strings are not reference-repair targets.
Missing content, duplicates, graph cycles, and unsatisfied prerequisites retain their
structural checks. Committed records and final integrity failures are never repaired.

The shared pass covers Genesis identities, relationships, sources, and knowledge;
Architecture node/edge, obligation, arc, claimant, and attractor references; packet-plan
join keys and dependencies; scene/ending/artifact references, destinations, variants,
epistemic dependencies and state keys; and semantic proposition, source, obligation,
termination, and typed relevance references. Slot repairs must preserve the frozen
one-to-one allocation. A source-grounded mapping is required; `UNRESOLVED` returns to
bounded correction, with the existing explicit Genesis expansion path preserved.

Planning tries one broad core or plan-batch draft with up to 21,800 output tokens
when context permits, then recovers pending content in coherent batches. Defaults
are four records, sixteen reference resolutions, or four backward setup requirements
per batch, with an 8,192-token output ceiling. Unknown collection counts are resolved
together. A failed batch preserves independently valid entries and members, then
splits only the unsuccessful remainder. Isolated values retain three attempts per
invocation. The engine supplies containers, IDs, and initial active obligation status.

Complete parsed members and array elements survive inside unfinished containers;
the engine never invents JSON closure or treats a truncated array prefix as its final
count. Every recovery request carries the complete assembled draft, Genesis, staged
core and plan batches, original unassigned annotations, and pending hints. Compact
JSON and referenced schema definitions reduce overhead without removing authored
content. If full context still cannot fit frozen prompt/model limits, pause with a
capacity breakdown and saved progress. Other hard resource exhaustion remains a
terminal failure. No oversized request is sent and no context is silently clipped.
Accepted values, including false, zero, and empty collections, persist before further
requests. Actual response usage is ledgered immediately, once per request, and is
not charged again for split successes or the eventual parent commit. Resume continues
only pending work, with no complete Architecture rewrite.

Plan reference catalogs include every allocated literary slot before Architecture is
committed and dependencies only from earlier staged allocations. Recorded motif-event
IDs map exactly to their motif IDs. A focused reference value may select an existing
typed target or create a missing local obligation or attractor field by field within
schema capacity. An unknown relevance label may become an authored setup requirement,
preserving its original text and location. It cannot create an arbitrary runtime state
key. Committed Genesis and unrelated accepted fields cannot change. `UNRESOLVED`
answers are accounted as failed lookups and never reused as successful resolutions.

Core and all plan batches remain staged while the engine plans backward from ending
transformations. Each ending seed condition, prerequisite obligation, and preserved
hint receives an earlier scene placement and authored setup instruction. The engine
attaches these to packet guidance and dependencies. Complete schema, reference,
dependency, and setup validation precedes the first Architecture commit. Prose begins
only after the whole plan is committed; scene and ending requests remain coherent
literary units. Checkpoints and field-response evidence accompany immutable commits.

Semantic normalization builds and fully validates the candidate packet before staging
metadata. Metadata errors consume metadata attempts, never another accepted artistic
request. A pending normalization response survives an interrupted focused lookup.
Each focused lookup permits three attempts within the frozen analysis, context, and
cumulative token budgets. Raw responses are immutable; successful and failed lookup
attempts are ledgered once, and field-level repair history is included in the parent
commit. Cached resolutions require the same invalid value, type, candidates, path,
and usage context.
New-run budget derivation adds a pooled allowance of three successful reference
repairs per possible scene/ending chunk to the existing analysis allowance. The
corresponding cumulative token ceilings freeze with the run; this capacity never
causes calls when references are already valid.
Calculation version 9 retains the reserve of three attempts per schema-bounded planning
field, plus earlier placement and instruction values for ending requirements and
preserved hints. Object arrays use schema cardinality limits; primitive arrays count
as one value. These are conservative recovery limits, not expected usage. Per-request
output and whole-work literary limits remain unchanged.

Committed chunks collectively own the original plan. If the provider truncates an
uncommitted single-content chunk, preserve the failed response and retry once with a larger allowance only
when the frozen model context leaves the safety reserve intact.

After every creative commit: preserve source; apply fact and knowledge events; append
or resolve obligations; update motif pressure; evaluate viable/endangered/foreclosed/
universally-impossible attractors; recompute the noncanonical prospective plan; then
choose the next lawful packet. Recalculation never increments rewrite, regeneration,
or backtrack counters.

### Phase D — Endings and Residue

Generate final ending prose late in exact one-ending chunks, only for viable early
attractors whose hard prerequisites have source-cited satisfaction. Endings may
interpret earlier evidence and create consequences, but may not retcon it.

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

Each artistic packet is followed by a temperature-zero, source-grounded metadata
normalization call. Focused reference calls run only when invalid references remain.
Noncreative analysis can classify constraints or feasibility and resolve declared
references; it can never return replacement prose.

## 5. Prospective Foreclosure

A committed fact may make a foreclosable attractor impossible. The packet remains
immutable. Foreclosure is lawful only when a cited immutable event negates a declared
prerequisite, no lawful realization remains, and the obligation is scoped to that
future. Universal hard obligations cannot be dropped; making one impossible causes
`FAILED_GENERATION`. Foreclosure changes future feasibility, not history.

## 6. Failures and Terminal States

- Transport failure before a response: retry the identical planned step.
- Provider failure before creative output: retry the identical planned step.
- Request timeout or interrupted stream: preserve diagnostics and immediately pause
  as `provider_incomplete_response`; an explicit resume authorizes another attempt.
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

All generation and analysis requests use streaming with usage reporting. The shared
transport reconstructs the ordinary completion envelope, preserving separate content,
reasoning fields, finish reason, and usage. It archives received SSE bytes and requires
both a finish reason and `[DONE]` before accepting a stream. Incomplete streams are
diagnostics, never staged creative payloads. A misleading `stop` finish reason does
not make malformed JSON valid. The configurable 5,400-second HTTP timeout applies to
socket inactivity, not total elapsed generation time. Existing buffered responses
and injected transports remain supported.

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
