# Generation Workflow Contract

## Backward Scaffold Policy

New runs freeze scaffold_planning_version=2. After macro intentions, seed terminal
outcomes and expand earlier scenes in checkpointed groups of at most four. Validate
causal support locally. Linear chapters have one successor; branches have two to
five. Final and premature endings are terminal, with route-specific entry cases.
The engine assigns declaration IDs before requesting connections from closed
successor interfaces. Each connection, draft amendment and audit task is
checkpointed. Only a single Genesis-grounded opening closes the frontier. Compile technical
slots, authored-exit requirements, actual scope, and writing dependencies afterward.
Scene count is a ceiling, not a requirement to fill. Write prose forward; audit hard
guarantees against immutable source quotations for every admitted entry case.
The current engine has one scaffold policy. Older runs delegate to their saved
launcher before current schemas are applied. See engine/docs/backward-scaffold.md.

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

Use frozen law and completed Genesis to allocate stable macro IDs, then author
arcs, attractors and obligations in bounded record batches. Routing at this point is
only a small macro projection. Declare terminal outcomes, expand predecessors and
verify the grounded opening as described above. Compile technical slots, navigation
and packet dependencies from the accepted scaffold. All architecture batches commit
before prose. Attractors freeze terminal transformations rather than choreography;
prospective realization order remains noncanonical.

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

Planning allocates macro IDs and collection sizes before requesting coherent batches
of up to four records. Reference-resolution batches contain at most sixteen tasks.
A failed batch preserves valid entries and members, then splits only its unsuccessful
remainder. Isolated values retain three attempts per invocation. The engine supplies
containers, IDs and initial active obligation status. No whole-map repair or separate
backward-setup placement pass remains in current operation.

Scoped requests retain frozen law, global canon, relevant records and mandatory
source evidence. Complete required data must fit the frozen phase ceiling and the
loaded context window, including output and safety reserve. Otherwise pause with
saved work intact. Read-only retrieval may add verified source units; it cannot
replace direct retrieval of mandatory proof or weaken the strict authoring schema.

Complete parsed members and array elements survive inside unfinished containers;
the engine never invents JSON closure or treats a truncated array prefix as its final
count. Every recovery request carries the complete assembled draft, Genesis, staged
core and plan batches, original unassigned annotations, and pending hints. Compact
JSON and referenced schema definitions reduce overhead without removing authored
content. Completed setup instructions are rendered once in packet guidance; setup
history uses a JSON Pointer to that exact guidance only when it matches uniquely in
the same prompt. Pending instructions and unmatched copies remain complete, and
checkpoint bytes are never changed by context rendering. If full context still
cannot fit frozen prompt/model limits, pause with a
capacity breakdown and saved progress. Other hard resource exhaustion remains a
terminal failure. No oversized request is sent and no context is silently clipped.
Accepted values, including false, zero, and empty collections, persist before further
requests. Actual response usage is ledgered immediately, once per request, and is
not charged again for split successes or the eventual parent commit. Resume continues
only pending work, with no complete Architecture rewrite.

Focused string planning values use a strict `{"value": "..."}` response object,
with the original field schema applied to `value`. The engine unwraps that one
value before schema and domain validation. Literal/quoted strings and exact singleton
field-path wrappers remain readable for saved responses, including JSON code fences.
Extraction never searches a graph patch, explanation, or reasoning for a plausible
ID. Extra sibling fields, duplicate JSON keys, invalid targets, and ambiguous containers
are rejected. `$connect` and other `$` paths label engine tasks rather than draft
properties to create. Raw provider responses remain unchanged; accepted values and
their original response evidence are checkpointed and replayed without another call.

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
The initial whole-delta allowance is 8,192 output tokens, covering reasoning and JSON.
Extract concise new supported changes, rather than restating canon or exhaustively
indexing description. Normalize metadata without changing any accepted literary bytes.

Packet obligation updates offer only the canonical resolution outcomes `satisfied`
and `intentionally_unresolved`. Active obligations persist without an update; extra
evidence belongs in facts or knowledge. Deliberate ambiguous resolution is distinct
from ongoing uncertainty. New soft obligations still begin active. Foreclosure and
impossibility retain their separate scoped-candidate requirements.
In completion-contract v1, an ending prerequisite offers only supported satisfaction.
A source-grounded resolution audit may remove an uncommitted ongoing or unsupported
update; it never invents satisfaction or changes prose. Long-range hard payoffs retain
their active pressure before their final literary deadline rather than forcing a
terminal update in the opening packet. Soft pressure does not become a binding task.

Truncation preserves complete records and closed categories, then switches remaining
work to pages of at most eight records with an explicit completion flag. Facts precede
knowledge, followed by new soft obligations, obligation updates, and motifs. Page
limits bound responses, not important information; continuation must preserve every
needed change. Accepted fact positions and aliases stay stable. Resolve references
to locally generated facts/motifs after assembling all categories. A truncated page
retains its complete prefix and reduces page size; one oversized record may use the
existing context-safe 15,000-token analysis ceiling. No-progress pages receive three
corrections per invocation. Interrupted streams preserve progress and pause at once.

Compact JSON, required schema definitions, and complete source context must fit frozen
limits. Do not clip source content to force a request to fit. Capacity shortfalls
pause; cumulative token, analysis, and event exhaustion retain hard-limit behavior.
Internal recovery checkpoints retain category completion and accepted/pending records.
Schema, reference, and canonical errors in complete responses also enter category
recovery, retaining the current candidate and successful cached reference repairs.
Structured error paths select affected categories directly, including canonical
`new_obligations` paths mapped to `new_soft_obligations`. Errors without usable paths
use a dedicated classifier with a strict category object and a 4,096-token output
ceiling. Classification never receives extraction instructions. Request, retained-record, and page
validation share the same specialized schema, including source and empty-category
restrictions. Rejections and per-category feedback persist across pause/resume.
Canonical correction revisits rejected categories while preserving others;
facts may be appended without renumbering existing aliases. The final candidate still
passes all existing schema, reference, canonical, and packet checks. Incomplete raw
envelopes remain diagnostics; recovered metadata uses an explicit assembled envelope.

Unavailable-knowledge errors carry the scene slot, dependency index, character,
proposition IDs, and prior negative knowledge evidence. They bypass category
selection and enter audited dependency recovery. A source-grounded decision may
replace or remove only flagged declarations on uncommitted scenes, request missing
knowledge acquisition metadata, or report a genuine unresolved contradiction.
Corrections require exact excerpts from the same immutable scene or its artifacts;
subject and proposition IDs must come from existing catalogs. Supported dependencies
cannot be discarded merely to pass a guard. Genuine acquisition preserves its
dependency, establishes supported knowledge, and retracts the exact prior negative
relation through new events. The continuity guard still validates the resulting packet.

Dependency overrides live in a separate artistic-hash-bound checkpoint, leaving the
original artistic files and all prose intact. Candidate validation and final packet
construction apply the same overrides. Accepted decisions, before/after declarations,
and provider responses remain auditable across resume and accompany the immutable
commit. Committed declarations and prior canon cannot be repaired this way.
Each focused lookup permits three attempts within the frozen analysis, context, and
cumulative token budgets. Raw responses are immutable; successful and failed lookup
attempts are ledgered once, and field-level repair history is included in the parent
commit. Cached resolutions require the same invalid value, type, candidates, path,
and usage context.
New-run budget derivation adds a pooled allowance of three successful reference
repairs per possible scene/ending chunk to the existing analysis allowance. The
corresponding cumulative token ceilings freeze with the run; this capacity never
causes calls when references are already valid.
The planning reserve covers three attempts per macro planning field. Scaffold
declaration, connection, amendment and audit recovery have their own bounded
allowance. Object arrays use schema cardinality limits; primitive arrays count as one value. These are conservative recovery limits, not expected usage. Per-request
output and whole-work literary limits remain unchanged.
It also reserves semantic recovery capacity for three attempts per event and five
category completions per possible scene/ending. Page responses are charged once and
the assembled parent metadata contributes no duplicate usage.

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
Artistic and structural quality findings are warnings. The static publisher has no
package installation or optional build step. On hard-gate success, publish only the new
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

Each new generation automatically initializes `state/index.sqlite3`. SQLite supplies
the operational projections, generated-ID and committed-record catalogs, ledger
lookups and accounting, and latest prospective plan. JSON remains the model and
immutable archive format; the run-status checkpoint and unfinished recovery drafts
remain files. Core state reads do not consult the former JSON state-map files.

After preserving a creative commit, append its ledger and constraint bytes, then
apply its records, IDs, events, affected projections, and indexing checkpoint in one
SQLite transaction. Noncreative ledger entries use the same transactional indexing
path. Prospective-plan history precedes its ledger/index update. The checkpoint
records ledger sequence/hash, canonical-state hash, constraint sequence, and usage
totals. No index checkpoint may advance beyond its durable archived input.

Ordinary commits apply only their new events. Startup/resume and complete-work
validation/publication audit the archives and compare the projection with full
replay. Missing, incompatible, foreign, corrupt, or stale databases are replaced
from verified history. Recovery can finish exact known partial appends, complete an
orphaned creative commit's ledger entry, and restore a missing prospective plan;
it never regenerates committed fiction. Unverifiable archive changes fail integrity
checks. Archive replay orders commit directories by numeric ledger sequence.

Architecture plans backward with the same recursive grammar used forward:

```text
desired residue ← consequence ← choice/deferment ← pressure ← interpretation ← encounter
```

This produces prerequisite obligations, never reverse-authored prose. Literary
authorship still commits forward only.

SQLite schema version 2 adds an external-content FTS5 index over a deterministic
document catalog. Scenes, artifacts, endings, choices, compositions, constraint
descriptions, Genesis, and Architecture units are keyed by owning commit and JSON
Pointer. Repeated entity IDs in root-canon records do not replace earlier units.
Catalog, postings, relevance tags, and the ordinary state checkpoint advance in the
same transaction. Startup/recovery compares the catalog with archived records and
checks FTS postings against catalog content; a mismatch rebuilds the derived database.

Before each scene/ending request, automatic search takes up to 32 unique literal
terms or phrases from packet keywords, resolved entity names, and guidance words.
Terms are quoted and passed as a bound SQL parameter. Unicode61 supplies
case-insensitive word matching without stemming, prefix expansion, or synonyms.
Search spans the whole work, including planned intentions; it never needs another
model call. BM25 weights titles twice as much as bodies, with relevance-tag locality
breaking ties before stable sequence/commit/pointer ordering.

Constraint selection combines at most 192 FTS hits, 192 indexed structural matches,
and 96 recent events, then selects at most 96 optional constraints. Existing weights
remain: hard obligation/direct dependency 12, arc/branch 10, knowledge 9,
claimant/causal debt/attractor prerequisite 8, object/location 6, motif 5, and recency
no more than 2. FTS rank replaces metadata word-overlap scoring with a bounded
`5 / (1 + rank)` bonus. Ordinary selection does not deserialize the whole event
history. Thus Scene 130 may retrieve Scene 12 even when its relevant detail was
never extracted into a constraint.

Required inputs include applicable engine law, brief, generated root source units, the local
packet plan, predecessor interfaces, binding obligations and their recursive
prerequisites, cited proof, and the selected current facts/knowledge tied to that
evidence. These bypass optional retrieval limits. Ending-specific prerequisite,
reader-state, and residue roles remain explicit. If required context cannot fit,
the engine pauses before calling the provider and records component sizes.

Optional discovery admits at most 24 whole source units within the existing frozen
retrieval allowance (12,288 estimated tokens for new runs). Each unit is read from
its checksum-verified archive, with commit/hash/pointer provenance. Required source
coverage is deduplicated; optional constraints, knowledge, historical state, motifs,
recent prose, and soft pressure fill remaining prepared-context space. No unit is
clipped. JSON uses compact separators and repeated source-reference metadata can
use exact `$context_ref` objects; authored strings and literary units stay complete.
Required original Genesis units appear in SHARED SOURCE RECORDS, with root
canon and prerequisite roles referencing their complete objects. Sources share only
when owning commit, source hash, JSON Pointer, and payload agree. Conflicting payloads
fail integrity checking. The merged Genesis view remains internal to entity lookup.
SHARED CONTEXT VALUES also factors exact repeated metadata objects and strings across
roles. Expanding every reference reproduces the complete included values. No summary
or inferred equivalence substitutes for evidence. New completion-contract runs use
49,152 tokens as the normal input target, with mandatory-input headroom bounded by
the verified frozen/loaded model window, complete request envelope, output and safety
reserves. Genuine capacity shortfalls still pause before a provider request.

Packet instructions retain full ontology, style, grammar, claimant/state, constitution,
branching, and web law, plus exact binding sections of the frozen work-instance and
workflow files. Development milestones and unrelated execution instructions stay in
the frozen snapshot rather than every writing prompt. Normalization retains the
instructions, ontology, state model, and authorship/generation/validation/integrity
rules alongside the same complete source objects and required state. It does not
carry the packet's style and operational manuals. The selected section names and
original file hashes are recorded in the retrieval receipt.

The local plan appears once. Packet estimates use conservative UTF-8 bytes/3,
matching analysis. Render the instructions, execution envelope, and schema before
packing context; reserve their measured size instead of subtracting a fixed 14,000
tokens. The frozen input ceiling remains unchanged, and output/safety reserves also
constrain the available model window. Recheck the complete request and correction
feedback before dispatch. No required source is clipped to meet a limit.

Plans, committed literary material, composition metadata, root canon, and historical
constraints carry distinct authority labels. Superseded facts and retracted knowledge
are history, not current state. Search does not establish branch applicability or
convert an intention into an event. Required dependencies remain direct lookups,
independent of FTS rank.

Each writing attempt preserves a compact retrieval receipt containing query terms,
candidate counts, selected constraint ranks/scores, source IDs/hashes/pointers,
omissions, instruction-profile provenance, shared-source coverage and savings,
state/context/prompt hashes, and size estimates. Receipts contain no prose.
Saved writing reuses its original attempt receipt; the accepted receipt is hashed
supplemental commit provenance. See [implementation and rehearsal](fts5-retrieval.md).

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

## Bounded execution policy

Every current manifest freezes bounded planning, scoped sources, completion contract
version 1 and scaffold planning version 2. Engine-allocated layout and coherent
record batches precede scaffold compilation. Up to four records
are authored per batch; accepted fields are checkpointed. Scoped contexts retain
frozen law, global canon, relevant entities, obligations and full mandatory proof.
Read-only retrieval is a separate bounded analysis stage; final authoring retains
strict JSON schemas. See [bounded-execution.md](bounded-execution.md) for the frozen
policy, tool limits, projection authority, replay and acceptance requirements.
