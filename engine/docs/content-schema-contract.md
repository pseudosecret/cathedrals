# Content Schema Contract

## Authority

`engine/data/generation-protocol.schema.json` is the machine-readable contract for
each record in an append-only generation run. There is no whole-work creative bundle.
Committed genesis, architecture, and packet records collectively form generated-work
canon. `schema-generation/` and `prose/` are deterministic projections, never later
creative inputs except as retrieval views of their immutable sources.

## Generated-Work Layout

A successful generation may publish:

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
    constraints/
      constraint-events.jsonl
    planning/
      prospective-plans.jsonl
    state/
      canonical-facts.json
      knowledge-state.json
      obligations.json
      motifs.json
      prospective-plan.json
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
  characters, and initial fact/knowledge/motif deltas.
- `architecture`: generated arcs, major topology, ending and other-scale attractors,
  backward prerequisite chains, the initial obligation graph, and technical packet
  envelopes. It freezes dependencies, not tentative execution order.
- `creative_packet`: several related scenes or endings, associated artifacts/formal
  compositions, and source-located constraint deltas.
- `constraint_event`: source-hashed append-only past-constraint, knowledge,
  future-obligation, motif-pressure, or foreclosure-candidate event.
- `prospective_plan`: replaceable noncanonical feasibility, obligation-to-packet
  assignment, and packet-order snapshot; every snapshot is retained in planning history.
- `ledger_entry`: hash-chained provenance for one attempted step.
- `finalization`: counters, hashes, resource accounting, verdicts, build status, and
  the sole terminal state.

Each JSON record must parse and validate before commit. Raw responses are preserved.
Truncated, ambiguous, or creatively malformed output is not completed by inference.

## Atomic Commit and Immutability

A creative commit succeeds only when the raw response is preserved, its protocol
record validates, all locally resolvable IDs and obligations pass, its content hash is
calculated, constraint events can be source-resolved, and a ledger entry can be appended.
The validated record is then atomically moved into `committed/` and becomes immutable.

Commit directories are never overwritten. Hash validation detects filesystem
mutation; each `entry_hash` is SHA-256 over canonicalized entry JSON with the
`entry_hash` field omitted. The ledger's `previous_entry_hash`,
`parent_canonical_state_hash`,
`canonical_state_hash_after`, and committed-record hashes establish the forward
lineage. A failed pre-commit attempt may leave audit evidence but creates no canon.

## Constraint Topology

> The second brain is not a memory of the book. It is the constraint topology
> surrounding the current point of composition.

Creative records emit a typed `constraint_delta`. Deterministic projection adds the
immutable source commit/hash and appends `constraint_event` records. The event stream
is an index with provenance, never stronger authority than immutable source.

Past constraints are minimal world facts and tracked epistemic state. Facts cover
chronology, relationships, object ownership/location/status, evidence, irreversible
events, reader/game state, claimants, environmental mutations, and anything whose
contradiction would create mechanical impossibility. Knowledge records distinguish
what a character knows, believes, suspects, explicitly does not know, and claims.

Future constraints are typed obligations: unresolved question, causal debt, promise,
required payoff, branch residue, motif/arc/evidence/thematic pressure, ending
prerequisite, or hidden-route prerequisite. Each records hardness, universality,
dependencies, allowed resolution modes, lawful termination targets, and status:
`active`, `satisfied`, `foreclosed`, `impossible`, or `intentionally_unresolved`.
Status changes are append-only events with evidence. No obligation may disappear.

Motif state records appearances, current function, pressure, overuse risk, and source
provenance. `prospective-plan.json` may be replaced after each commit because it is
neither fiction nor canon. Its append-only snapshot history preserves auditability.
Changing packet priority or viable-future assignment cannot alter source, facts,
architecture, attractors, or hard obligations. Recursive summaries never substitute
for sources.

## Deterministic Projection

After each commit, deterministic tools may append indexes and project records for
validation. They may copy structured fields, add mechanical frontmatter, and copy
`prose_mdx` or `body_mdx` verbatim. They may not summarize, rephrase, reorder literary
paragraphs, normalize punctuation, add transitions, or change graph meaning.

Those historical `*_mdx` fields contain Markdown only. Generated Markdown is data,
never executable route code; all authored HTML, imports, exports, scripts, and JSX
fail before commit. The build-time `markdown-it` renderer has raw HTML disabled and
produces projection HTML without changing the source bytes.

Genesis also commits bounded `web_art_direction` presentation canon. It may influence
deterministic CSS through enumerated mappings and validated colors, but cannot carry
arbitrary CSS/JavaScript or create narrative facts outside the same genesis record.

## Cross-Record Validation

JSON Schema cannot enforce the whole run. Deterministic validation must also confirm:

- generation IDs, protocol versions, sequences, hash chains, and canonical-state
  parent hashes agree
- the run manifest and generation brief never changed
- all generation-time engine reads resolve inside the run-local snapshot
- every committed creative record still matches its ledger output hash
- all technical claimant slots appear exactly once in genesis
- all IDs are unique and every claimant, character, arc, scene, artifact, ending,
  composition, node, edge, packet dependency, constraint, and original source resolves
- the obligation and packet-dependency graphs resolve and contain no accidental cycle
- prospective packet choice respects immutable dependencies while remaining mutable
- each literary packet contains three to eight planned scenes and each ending packet
  contains two to six prerequisite-satisfied endings
- the complete work honors the explicit possible-scene scope and its derived count and literary-word bounds
- all architecture nodes receive content exactly once; no unplanned candidate is kept
- the opening group has exactly three playable options after three to five
  reader-perspective scene surfaces
- every other meaningful decision has two to five playable options
- opening branches split again; reconvergence preserves state; depth is unequal
- every major decision exposes consequential hesitation
- every technical destination slot resolves exactly once and redirective endings resolve to prebuilt content
- stateful variants differ materially and formal-composition anchors resolve
- every constraint event cites existing immutable source evidence
- universal hard obligations are never foreclosed; satisfied/foreclosed obligations
  cite evidence; ending prerequisites are satisfied before commit
- tracked epistemic dependencies never use knowledge explicitly unavailable to a character
- prospective snapshots never mutate canon and source truth outranks derived state
- generated Markdown is safe, rendered semantically, and projection preserves literary bytes
- counters and cumulative token, cost, retrieval, and constraint budgets are within limits
- `human_intervention_count`, `committed_rewrite_count`,
  `committed_regeneration_count`, and `backtrack_count` are all zero

## Finalization and Complete-Work Barrier

`finalization.json` records the ledger head, committed record hashes, constraint-event
and prospective-history hashes, step counters, token/cost totals, validation verdicts,
and terminal state.
`READY_TO_PLAY` requires positive creative-step count; zero intervention, rewrite,
regeneration, and backtrack counters; full mechanical and artistic passes; a passing
static build; and `complete_work_barrier_satisfied: true`.

`FAILED_GENERATION` always has `playable: false`. There is no partially generated but
playable state. A later run receives a new generation ID and does not reopen the old
canon.
