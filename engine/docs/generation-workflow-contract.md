# Generation Workflow Contract

## Invariant

One pass means one autonomous generation run: frozen inputs progress causally forward
until completion or failure, with no human creative steering and no mutation,
replacement, regeneration, or candidate selection after a creative artifact commits.
Response count is not the invariant. A run may contain many creative calls.

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
- engine commit and all active engine inputs
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
input-token, output-token, memory, retrieval, and configured cost ceilings. Failure
stops before creative generation.

## 2. Append-Only Run

Create `generated-work/<generation-id>/run-ledger.jsonl`. Each line validates against
the ledger-entry record in the protocol schema and is chained by SHA-256. The ledger
records every creative, analysis/index, validation, build, and finalization step.

A technical retry keeps the same planned step ID, prompt/context hashes, parameters,
and seed, while incrementing `attempt`. A creative step counts when valid output is
committed. Failed attempts remain visible in the ledger.

### Phase A — Genesis

Generate in one creative step:

- all five claimants as one differentiated set
- significant non-claimant characters
- the exact threshold incident and core chronology
- relationships, generated motifs, environmental mutation law, and principal tensions

Commit `genesis.json`. It becomes immutable generated root canon.

### Phase B — Macroarchitecture

Using frozen engine canon and genesis, generate the complete macro topology, arc
purposes, major decisions, reconvergence, hidden-route opportunities, narrative
promises, ending families, and dependency/traversal plan. Commit
`architecture.json`. Its generated meaning and traversal order are immutable.

### Phase C — Forward Literary Packets

Follow the frozen dependency order. A packet normally contains three to eight related
scenes plus associated artifacts, formal compositions, and source-grounded memory
deltas. Assemble only relevant context. Commit a mechanically valid packet even when
its art is disappointing. Later packets may read and react to it; they may not replace
it.

### Phase D — Endings and Residue

Generate ending packets only after all prerequisite path content and state histories
have committed. Endings may interpret earlier evidence and create consequences, but
may not retcon it.

### Phase E — Validation and Static Build

Project committed records without literary change, validate the entire graph and
content set, perform whole-work artistic acceptance, compile Astro, validate the
build, and cross the complete-work barrier only on full success.

## 3. Commit Semantics

A commit atomically preserves the raw response, validated protocol record, prompt and
context hashes, output hash, generated IDs, memory deltas, canonical-state hashes,
and ledger entry. After that point the creative bytes and facts are history.

Later steps may read, quote, retrieve, reinterpret from a character's perspective,
contradict diegetically, or create consequences from committed material. They may not
rewrite, improve, regenerate, silently retcon, or discard it in favor of another
candidate. If awkwardness remains executable, the run lives with it. If immutable
history makes completion mechanically impossible, the run fails.

No call may generate several fictional candidates for scoring or selection. A valid
creative output consumes the possibility space and commits. Deterministic structural
selection before creative generation remains lawful.

## 4. Narrative Memory and Context

The immutable creative records are source evidence. `memory-events.jsonl` is an
append-only index divided into canonical generated state and narrative working
memory. Every event cites source type, artifact ID, locator, source commit, and source
hash. Index corrections append a superseding event; they never change source fiction.
When memory conflicts with immutable prose, prose wins.

For each later creative step, deterministically assemble a bounded context packet
from frozen engine law, genesis, relevant architecture, current branch/world state,
relevant claimant and relationship records, recent scenes, open promises, motifs,
artifacts, exact retrieved source passages, geomancy, and packet obligations.
Retrieval selects evidence; it cannot invent truth.

Creative packets should emit their own memory observations. Optional analysis/index
calls may extract facts, classify motifs, check consistency, or select source
passages. They have no authority to write replacement fiction or silently promote a
summary over its source.

## 5. Failures and Terminal States

- Transport failure before a response: retry the identical planned step.
- Provider failure before creative output: retry the identical planned step.
- Malformed or unparseable creative output: record it and `FAILED_GENERATION`; do not
  creatively repair or resample.
- Mechanically valid but weak art: commit and continue.
- Lawful diegetic contradiction: preserve and continue.
- Unresolvable mechanical continuity impossibility: `FAILED_GENERATION`; do not retcon.
- Whole-work artistic rejection: `FAILED_GENERATION`; no repair loop.
- Mechanical or static-build failure caused by generated content: `FAILED_GENERATION`.
  An engine defect may be fixed only in a later engine revision, never by altering the
  committed work.

The only terminal states exposed to the user are `READY_TO_PLAY` and
`FAILED_GENERATION`. A failed run follows its frozen retention policy. Any later
attempt starts from frozen inputs under a new generation ID.

## 6. Complete-Work Barrier

Before `READY_TO_PLAY`, all generated canon, claimants, characters, architecture,
scenes, artifacts, formal compositions, endings, state-dependent variants, lawful
branches, graph data, projections, validations, artistic acceptance, static build,
and build validation must exist and pass.

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
