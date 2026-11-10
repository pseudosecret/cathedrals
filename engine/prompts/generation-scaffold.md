# Backward Causal Scaffold Expansion

Return only the schema-constrained patch. Preserve every accepted node.

Plan backward from the supplied successor contracts. Add one to four earlier scenes,
using a prefix of the allocated node IDs in order. Each new scene must reach an
existing frontier node, possibly through another new scene in this patch. Successors
may only be supplied frontier nodes or newly allocated nodes. Do not invent a
separate scene inventory, pad the scene cap, or rewrite a whole navigation map.

A scene may have exactly ONE successor: an ordinary chapter or continuation. It may
instead offer TWO TO FIVE materially different successors. Several predecessors may
reach a shared successor when every admitted entry case remains valid. Different
branches may end at different depths. A premature ending can have just one parent;
shared endings are optional. Do not manufacture choices in a linear chapter.

Give each node a purpose, intended change, alternative entry cases, hard exit
guarantees, and preserved conditions. Empty hard guarantees are allowed: stillness,
reflection, and movement need not introduce a new fact. Dramatic/thematic intentions
are advisory. Keep descriptions concise. Requirement and case IDs must be unique
across the work; prefix them with their allocated node ID. Planned IDs are never
committed facts or proof that events have occurred. Scene prerequisite_obligation_ids
is empty; terminal prerequisites were specified separately with the outcomes.

For each outgoing transition, choose one sufficient entry case of its successor.
Support every requirement in that case, once each, using this predecessor's explicit
exit guarantees or exact committed Genesis source IDs. Explain why the support earns
the requirement. Alternatives are OR cases, not a demand to read exclusive paths.
A predecessor's guarantees must hold for ALL its admitted entry cases. Shared scenes
must not assume that every reader encountered evidence from every other branch.
Split incompatible scenes rather than forcing a merge.

A frontier node remains pending until every declared entry case has an incoming
supporting route. pending_entry_case_ids identifies those gaps, including nodes
that already have other parents. Fill those gaps before proposing closure.

The scene cap is a maximum, not a quota. Consolidate the unresolved frontier while
there is still capacity. A five-way join can reduce the frontier by at most four;
reserve at least ceil((unresolved_entry_case_count - 1) / 4) earlier scenes,
at least the greatest number of missing cases at any one node, and at least one
scene until the opening is grounded. Arithmetic capacity does not justify an arbitrary
narrative join. Add the smallest useful predecessor structure with earned causes.

Set complete=true only when the entire graph has one opening, every outcome and
scene is reachable from it, at least eight scenes exist, and every declared entry
case has a supporting incoming transition. The opening has one entry case supported
entirely by cited Genesis evidence in opening_support. Set opening_node_id to that
new opening. Before completion, use opening_node_id=null and opening_support=[].
The opening may lead to a linear chapter; the first branch occurs when the story
needs it. There is no fixed introduction length or forced three-choice hub.

Planning moves backward; prose will be written forward in topological order. Reader
progression is a DAG. Do not create return loops, runtime-generated continuations,
or terminal redirects. Browser history and start_over are separate controls.

LOCAL PLANNING CONTEXT

{{SCAFFOLD_CONTEXT}}
