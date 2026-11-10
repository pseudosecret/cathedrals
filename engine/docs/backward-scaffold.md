# Backward causal scaffold

New preflight policies freeze `scaffold_planning_version: 3`. The saved causal
scaffold remains version 1; the planning response interface is separately versioned. These runs seed
terminal outcomes in pages of at most four, then expand predecessors in groups of
at most four. The existing derived ending ceiling remains in force; there is no
additional fixed sixteen-ending limit. Existing
runs continue to use their frozen launcher and policy; there is no migration.

A scene has one authored continuation or two to five branch destinations. A shared
scene declares alternative sufficient entry cases. Transitions name the admitted
case and support every requirement using predecessor guarantees or Genesis source
IDs. These are planned contracts, separate from committed facts and character
knowledge. Endings can be premature or final, with one or multiple incoming paths.
They are terminal under this policy. Browser history and `start_over` are separate.

Version 3 selects targets before drafting each predecessor. A closed-schema mapping
selects one to five known destination/entry-case pairs and a concise causal job.
The engine/model chooses these automatically; there is no human target-selection
step. It then authors one contract, assigns its IDs, and binds evidence to exactly
those selected cases. These stages interleave for up to four scenes, so a later
predecessor can target an earlier declaration in the same batch. The model can end
a batch after its first scene rather than fill unused capacity.

Contracts contain no authored declaration IDs. The engine assigns IDs by owner,
ordinal and revision. Binding schemas fix destination keys and the selected entry
case, and accept only predecessor guarantee IDs or supplied Genesis sources for
its requirements. The shared evidence definition remains bounded. Future and self
references cannot be selected; duplicate JSON keys remain invalid.

Target assignments, declarations and connections are separate checkpoints in
`.staging/scaffold_expand_NNNNN.contracts.json` (checkpoint version 3). Each request
is keyed by its actual prompt and schema. Interruptions replay completed responses
without repeating their usage. Old checkpoint formats use their saved launcher;
there is no in-process migration.

An unchanged or whitespace-only amendment cannot advance a revision. A requested
repair of missing guarantees cannot leave those guarantees empty while changing
other fields. Punctuation-only clauses, serialized engine fields inside clauses,
and identical alternative entry cases are rejected before acceptance, including
in terminal outcomes. Empty guarantees still remain valid for scenes whose work
needs no new hard fact.

Causal review can amend only flagged fields or rebind faulty connections, preserving
unrelated destinations. When focused repair is ineffective, one bounded local
re-declaration per failed node per invocation can choose new targets and replace
that uncommitted contract. Its node ID stays fixed. Only a validated change creates
a revision. Unchanged successor conditions can be remapped to new engine-owned case
IDs without redrafting consumers; changed conditions require affected consumers to
reselect and redeclare. Other contracts and raw responses remain unchanged.

Four repair cycles per invocation and the existing frozen request/cumulative budgets
bound recovery. The final cycle does not issue another unreviewed amendment. Pause
diagnostics identify the last evaluated revisions and any pending declarations.
No committed contract or literary bytes are changed by these draft repairs.

Repair field/destination selectors are treated as sets: exact repeated strings are
removed before schema validation, preserving their first-occurrence order. This
also applies to `contract_issue.fields`. The original raw response stays unchanged;
the planning audit and ledger retain the canonical selection. Unknown names,
malformed values, duplicate JSON keys and contradictory support verdicts still fail.
Causal review receives accepted successor interfaces without their outgoing edges,
so its evidence bundle covers the new patch rather than unrelated older routes.

Closure is a separate request, offered only after one opening reaches all nodes,
all alternative entries are supported, eight scenes exist, and the opening has one
explicit entry case. A free `complete=true` flag cannot close an expansion. Genesis
support is still authored and verified; arithmetic does not invent an opening.

An accepted patch adds predecessors leading to supplied frontier nodes. It cannot
replace existing nodes or invent unattached destinations. A node remains on the
frontier until all its declared alternative entry cases have supporting parents,
even after its first incoming edge exists. Local causal review checks
whether guarantees actually support the chosen successor requirements and whether
shared scenes preserve their guarantees across alternative entries. Cycles,
unsupported references, incomplete requirement coverage, and insufficient capacity
to close the frontier fail before acceptance. Scene count is a cap: the engine does
not allocate or pad all requested scenes.

The planner closes only with one opening reaching every node. Its single entry case
must name an explicit Genesis-supported requirement. At least eight scenes and two
outcomes remain required. Final validation also requires every entry case to have
an incoming supporting transition. A DAG with successors for every nonterminal
ensures every scene can reach an ending. Capacity arithmetic reserves at least
`max(1, ceil((missing_entry_cases - 1) / 4), most_missing_cases_at_one_node)`
earlier scenes while incomplete; it does not
invent joins to make the arithmetic work. If the cap cannot accommodate a coherent
closure, the run pauses with the draft intact.

The completed scaffold determines technical slots in stable topological order,
actual scene/ending counts, artifact and composition guidance, authored navigation,
and packet dependencies. Compatibility macro topology is a small projection only.
Packet groups are technical envelopes; grouping creates no reader edges. A terminal
outcome receives a separate ending attractor carrying its own authored prerequisites,
so premature endings do not inherit every final revelation. Scheduling scores make
obligations eligible for satisfaction; they do not require a terminal update in an
earlier scene. Hard scaffold guarantees and ending prerequisites still bind.
Original macro attractor
IDs remain declared as pressures. Normal context limits and publication checks stay
in effect.

Outcome drafting receives the existing obligation definitions. Selecting a hard
prerequisite compiles its complete dependency closure into every alternative entry
case before backward expansion. These are required future achievements, not facts.
Compilation refuses to drop required conditions to meet an interface bound.
Requests of 8–12 scenes use reduced scope and macro-planning bounds; see
[First complete work](first-complete-work.md) for the eight-scene acceptance target.

Forward writing receives its local contracts, predecessor support, successor entry
requirements, and directly fetched immutable evidence. It never receives the full
scaffold merely to write one scene. Linear chapter assignments require exactly one
authored exit. Ending assignments allow no story choices or redirects. Reader-state
verification follows all distinct reachable states, including both sides of a merge;
more than 128 states at a node pauses verification without dropping paths.

Source audits continue to use engine-owned task IDs. Each task fixes one guarantee
or preserved condition, entry case, incoming route, and permitted source list.
The model returns only its support judgment and exact quotations. Pages contain at
most eight tasks; completed responses are ledgered and reused on resume. Results
compile into the existing canonical receipt format, with an assembly ledger entry
binding the complete result. The model cannot combine fields from different audit
tasks or cite sources outside a task's permitted list.

After artistic preservation, source analysis checks each hard exit guarantee and
preserved condition for every incoming route and its admitted entry case using
exact original quotations. Routes sharing the same case ID still receive separate
checks.
Evidence from an unrelated alternative case is rejected. Thematic intentions are
advisory, and a linear chapter need not add a fact. Unsupported hard promises receive
one source-only reconsideration, checkpointed separately with the original judgment
retained. A sustained rejection fails with the original prose intact and a diagnostic
naming the promise and permitted sources. It cannot be repaired by inventing
normalization facts or rewriting literary bytes. This is model-assisted semantic verification;
it does not prove literary quality or eliminate model mistakes.

`.staging/causal-scaffold.json` checkpoints accepted
outcomes, expansions, the frontier derivable from them, and stable IDs. Accepted
provider responses and local support reviews are ledgered and reused on resume.
The compiled scaffold is frozen in the Architecture core. Hard-guarantee receipts
are archived as `scaffold-evidence.json` with each content commit, covered by commit
hashes. Downstream support loads those immutable receipts and verifies their
quotations against original source units. Staging copies are diagnostic conveniences.

Implementation: root `cathedrals`; protocol definitions in
`engine/data/generation-protocol.schema.json`; target selection in
`engine/prompts/generation-scaffold-targets.md`; expansion prompts in
`engine/prompts/generation-scaffold-declarations.md` and
`engine/prompts/generation-scaffold-connections.md`. Regression definitions are in
`engine/tests/test_backward_scaffold.py` and `engine/tests/test_scaffold_compiler.py`, covering mixed linear/branch structures,
orphan slots, merges, capacity, interrupted expansion, source preservation, and
100/150-scene static publication fixtures, plus iterative 5,000-scene graph validation.
`engine/tests/test_scaffold_review.py` covers repeated selectors, strict rejection
of invalid reviews, scoped evidence, raw response preservation, and replay without
duplicate usage. The selector/context repair passed all 323 offline tests with
network access blocked; no live generation or existing run archive was changed.

Offline imports and synthetic tests are authorized for engine cleanup, with network
access blocked. The acceptance suite exercises a current version 3 generation,
interruption/resume and complete static publication using a synthetic provider.
It makes no claim of live-model literary success. Older runs require their original
saved launcher; the current engine does not migrate their records or fall back to
obsolete in-process planning paths.

Target-first repair verification: all 336 offline tests passed with network access
blocked. The 13 tests in `engine/tests/test_scaffold_targets.py` cover target/case
ownership, chapters and branches, short batches, malformed clauses, ineffective
amendments, bounded local re-declaration, preservation of unrelated branches and
exactly-once replay after target, declaration and amendment checkpoint interruptions.
The full suite also includes the current 30-scene publication/resume rehearsal and
existing 150-scene static publication and 5,000-scene structural checks. No live
model call or change to an existing attempt was part of this verification.

First-completion verification: all 349 offline tests passed with network access
blocked. This includes eight scenes, two endings and static publication through the
same pipeline, with interruption after a committed packet and after publication.
Recovery preserved output and accounting without another provider call. Source
audit regressions cover one reconsideration, interrupted replay, sustained failure,
unchanged prose and invalid quotations. No live-model or browser acceptance was run.
