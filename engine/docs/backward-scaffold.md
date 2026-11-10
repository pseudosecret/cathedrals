# Backward causal scaffold

New preflight policies freeze `scaffold_planning_version: 4`. The saved causal
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

Version 4 selects up to five known successor cases before drafting a predecessor.
The engine reserves earlier scene slots from all uncovered cases, including cases
introduced or admitted by tentative assignments in the current batch. This sets
the maximum number of entry cases for each new declaration. The final slot must
cover every remaining destination case and leave one explicit opening condition.

The engine compiles unconditional bindings and exact matches to declared exit
guarantees. For other requirements, the model selects evidence IDs or names the
condition that needs a guarantee. Review addresses individual proofs, contract
compatibility with each entry case, and opening evidence. Capacity is checked
before semantic review.

Each predecessor can receive one focused rebind, one replacement declaration, and
one different feasible assignment. A rebind must change the evidence IDs. A
replacement for missing support must include the named exit condition. Unchanged
entry cases and proofs are remapped when their engine IDs change. The engine keeps
unrelated bindings and checks dependent assignments against revised cases.

Assignments, declarations, bindings and repair usage are checkpointed in
`.staging/scaffold_expand_NNNNN.contracts.json` (version 4). Replay uses the
original model responses and token accounting. Exhausted repairs identify the
blocked contract and available capacity. Provider interruptions remain resumable.

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
the verifier reports budget exhaustion if a node exceeds 128 distinct states.
Writing prompts include the reachable states for the assigned content.

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
access blocked. The earlier version 3 acceptance suite exercised generation,
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
