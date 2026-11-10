# Backward causal scaffold

New preflight policies freeze `scaffold_planning_version: 2`. The saved causal
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

Version 2 uses two stages. The model first declares narrative contracts without
node, entry-case, requirement, or guarantee IDs. The engine assigns IDs by owner,
ordinal and draft revision. It then requests connections per predecessor using
closed schemas: destination keys fix the node, entry-case alternatives fix its
requirements, and each requirement accepts only that predecessor's guarantee IDs
or known Genesis sources. Sources cannot be empty for a required support. The evidence selector is stored
once in a shared schema definition rather than repeated for every requirement. A
predecessor may target existing frontier nodes or earlier declarations in the batch,
so same-batch cycles cannot be represented. Duplicate JSON keys are rejected.

Contracts and accepted connections are checkpointed in
`.staging/scaffold_expand_NNNNN.contracts.json` before the next request. A failed
connection does not redeclare scenes. Missing guarantees can be reported explicitly
as `contract_issue`, followed by an amendment restricted to the flagged fields.
Causal review may also select particular faulty source-to-destination connections.
Other destinations from that predecessor are locked to their accepted values.
Amending a contract creates a new draft revision and invalidates only its own
connections and affected consumers; unrelated connections remain available.
Four review rounds per invocation bound this recovery. The latest amendments and
all accepted work survive a pause. No committed contract or literary bytes are
changed by these draft repairs.

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

Forward writing receives its local contracts, predecessor support, successor entry
requirements, and directly fetched immutable evidence. It never receives the full
scaffold merely to write one scene. Linear chapter assignments require exactly one
authored exit. Ending assignments allow no story choices or redirects. Reader-state
verification follows all distinct reachable states, including both sides of a merge;
more than 128 states at a node pauses verification without dropping paths.

Version 2 source audits use engine-owned task IDs. Each task fixes one guarantee
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
advisory, and a linear chapter need not add a fact. Unsupported hard promises pause
with the original prose intact. They cannot be repaired by inventing normalization
facts or rewriting literary bytes. This is model-assisted semantic verification;
it does not prove literary quality or eliminate model mistakes.

`.staging/causal-scaffold.json` checkpoints accepted
outcomes, expansions, the frontier derivable from them, and stable IDs. Accepted
provider responses and local support reviews are ledgered and reused on resume.
The compiled scaffold is frozen in the Architecture core. Hard-guarantee receipts
are archived as `scaffold-evidence.json` with each content commit, covered by commit
hashes. Downstream support loads those immutable receipts and verifies their
quotations against original source units. Staging copies are diagnostic conveniences.

Implementation: root `cathedrals`; protocol definitions in
`engine/data/generation-protocol.schema.json`; expansion prompt in
`engine/prompts/generation-scaffold.md`. Regression definitions are in
`engine/tests/test_backward_scaffold.py` and `engine/tests/test_scaffold_compiler.py`, covering mixed linear/branch structures,
orphan slots, merges, capacity, interrupted expansion, source preservation, and
100/150-scene static publication fixtures, plus iterative 5,000-scene graph validation.

For this change, verification is restricted by the operator's instruction: no engine
execution, replay, imports, or engine-loading tests. Static syntax, JSON references,
source review, and diff checks are allowed. The version 1 planning path and frozen runs retain their original interfaces.
There is no migration of archived runs. The regression suite is supplied for a
later operator-authorized run; no end-to-end generation success is claimed.
