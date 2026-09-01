# Content Schema Contract

## Authority

`engine/data/generation-protocol.schema.json` is the machine-readable contract for
each record in an append-only generation run. There is no whole-work creative bundle.
Committed genesis, architecture, and packet records collectively form generated-work
canon. `schema-generation/` and `prose/` are deterministic projections, never later
creative inputs except as retrieval views of their immutable sources.

## Generation-Branch Layout

`main` keeps downstream directories empty. A generation branch or release may contain:

```text
generated-work/<generation-id>/
  provenance/
    run-manifest.json
    run-ledger.jsonl
    committed/
      <sequence>-<step-id>/record.json
      <sequence>-<step-id>/raw-response.txt
    raw/
      <sequence>-<attempt>.json
    memory/
      memory-events.jsonl
      canonical-memory.json
      working-memory.json
    validation/
      mechanical.json
      artistic.json
      build.json
    finalization.json
  web/
    public/work.json
    public/source/<content-id>.md
    src/
    dist/
```

No generated work becomes canonical content of `main`.

## Record Protocol

The protocol schema validates these independent record types:

- `run_manifest`: immutable brief, frozen engine provenance, limits, traversal
  strategy, providers, retention law, and complete-work barrier.
- `genesis`: generated root canon, exactly five generated claimants, significant
  characters, and initial memory observations.
- `architecture`: generated arcs, complete macro graph, promises, ending families,
  hidden-route opportunities, and frozen packet traversal.
- `creative_packet`: several related scenes or endings, associated artifacts/formal
  compositions, and source-located memory observations.
- `index_batch`: optional non-creative source extraction.
- `memory_event`: source-hashed append-only canonical-state or working-memory record.
- `ledger_entry`: hash-chained provenance for one attempted step.
- `finalization`: counters, hashes, resource accounting, verdicts, build status, and
  the sole terminal state.

Each JSON record must parse and validate before commit. Raw responses are preserved.
Truncated, ambiguous, or creatively malformed output is not completed by inference.

## Atomic Commit and Immutability

A creative commit succeeds only when the raw response is preserved, its protocol
record validates, all locally resolvable IDs and obligations pass, its content hash is
calculated, memory events can be source-resolved, and a ledger entry can be appended.
The validated record is then atomically moved into `committed/` and becomes immutable.

Commit directories are never overwritten. Hash validation detects filesystem
mutation; each `entry_hash` is SHA-256 over canonicalized entry JSON with the
`entry_hash` field omitted. The ledger's `previous_entry_hash`,
`parent_canonical_state_hash`,
`canonical_state_hash_after`, and committed-record hashes establish the forward
lineage. A failed pre-commit attempt may leave audit evidence but creates no canon.

## Memory Projection

Creative packets emit source-located memory observations. Deterministic projection
adds the immutable source commit and SHA-256 hash and appends normalized
`memory_event` records to `memory-events.jsonl`. Analysis/index batches follow the
same path and may only assert propositions supported by cited committed sources.

Canonical-state kinds include characters, chronology, objects, locations,
relationships, character knowledge, world state, and irreversible events. Working
memory includes unresolved threads, promises, callbacks, motifs, questions, branch
residue, foreshadowing, thematic pressure, and intentional contradictions.

Status changes and index corrections are new memory events. They may supersede an
index record, never the cited source. `retrieval-index.json` is rebuildable and has no
canonical authority. Recursive summaries are not source evidence.

## Deterministic Projection

After each commit, deterministic tools may append indexes and project records for
validation. They may copy structured fields, add mechanical frontmatter, and copy
`prose_mdx` or `body_mdx` verbatim. They may not summarize, rephrase, reorder literary
paragraphs, normalize punctuation, add transitions, or change graph meaning.

Generated Markdown is data, never executable route code. Imports, exports, scripts,
and arbitrary JSX in generated literary strings fail mechanical validation.

## Cross-Record Validation

JSON Schema cannot enforce the whole run. Deterministic validation must also confirm:

- generation IDs, protocol versions, sequences, hash chains, and canonical-state
  parent hashes agree
- the run manifest and generation brief never changed
- engine hashes remain identical to the preflight snapshot
- every committed creative record still matches its ledger output hash
- all technical claimant slots appear exactly once in genesis
- all IDs are unique and every claimant, character, arc, scene, artifact, ending,
  composition, node, edge, packet dependency, and memory source resolves
- architecture traversal is dependency-valid and no packet was generated out of order
- each literary packet contains three to eight planned scenes and each ending packet
  contains two to six prerequisite-satisfied endings
- the complete work honors the explicit possible-scene scope and its derived count and literary-word bounds
- all architecture nodes receive content exactly once; no unplanned candidate is kept
- the opening group has exactly three playable options after three to five
  reader-perspective scene surfaces
- every other meaningful decision has two to five playable options
- opening branches split again; reconvergence preserves state; depth is unequal
- every major decision exposes consequential hesitation
- redirective endings resolve to prebuilt scenes
- stateful variants differ materially and formal-composition anchors resolve
- every important memory event cites existing immutable source evidence
- generated MDX is safe and projection preserves literary bytes
- counters and cumulative token, cost, retrieval, and memory budgets are within limits
- `human_intervention_count`, `committed_rewrite_count`,
  `committed_regeneration_count`, and `backtrack_count` are all zero

## Finalization and Complete-Work Barrier

`finalization.json` records the ledger head, committed record hashes, memory stream
hash, step counters, token/cost totals, validation verdicts, and terminal state.
`READY_TO_PLAY` requires positive creative-step count; zero intervention, rewrite,
regeneration, and backtrack counters; full mechanical and artistic passes; a passing
static build; and `complete_work_barrier_satisfied: true`.

`FAILED_GENERATION` always has `playable: false`. There is no partially generated but
playable state. A later run receives a new generation ID and does not reopen the old
canon.
