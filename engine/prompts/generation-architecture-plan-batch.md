# Architecture Plan Batch Instruction

Return exactly one Architecture plan annotation payload conforming to the supplied schema.
Return JSON only.

Annotate every supplied deterministic packet allocation by its exact `packet_slot_id`, including
both literary and ending allocations. Return one annotation per listed allocation; do not infer,
rename, add, or omit packets. Do not restate fixed allocation fields (`packet_kind`, `scene_slot_ids`, `ending_slot_ids`, artifact count, or formal-composition count);
the engine merges those fixed allocations. Author priority, lawful dependencies, branch relation, attractor pressure, relevance,
and soft guidance. Dependencies may reference only prior staged packet IDs or earlier
packet IDs in this batch; this keeps the complete dependency graph acyclic.
Each ending plan selects exactly one ending attractor. Do not write scenes or prose.
When the schema requests `required_navigation`, map every allocated scene slot to
one or more intended destination slots from the supplied destination domain. Ending
packets supply an empty map. Plan actual branches and reconvergence: across batches,
every surface must be reachable from the opening and every scene must have a route
to an ending. Later scene requests will author the labels and transitions; the
engine will not add fallback reading links. Do not confuse reading links with the
acyclic generation dependencies above.
Plan backward from its terminal transformation and prerequisites to earlier literary
packets. Express necessary setups in soft guidance. Technical-slot relevance may use
the allocated scene and ending IDs; state-key relevance must use declared runtime
state keys. A narrative milestone is a setup instruction, not a new state variable.
An ending's entry prerequisites must be establishable in preceding literary scenes.
Do not make the ending's own still-unwritten terminal transformation a prerequisite
for authoring that ending. If the payoff belongs to a preceding climax instead,
place that climax and its necessary evidence explicitly before the ending.
The engine stages every batch and completes backward setup placement before committing
Architecture or requesting prose.
Keep annotations concise. During recovery, the engine may request several pending
records or setup requirements together; preserve already accepted fields and answer
only the supplied targets.

IMMUTABLE ARCHITECTURE CONTEXT BEGINS

{{ARCHITECTURE_PLAN_CONTEXT}}

IMMUTABLE ARCHITECTURE CONTEXT ENDS

THIS BATCH'S EXACT ALLOCATIONS BEGIN

{{ARCHITECTURE_PLAN_ALLOCATIONS}}

THIS BATCH'S EXACT ALLOCATIONS END

RELEVANT PROTOCOL DEFINITIONS BEGIN

{{ARCHITECTURE_PLAN_PROTOCOL_DEFINITIONS}}

RELEVANT PROTOCOL DEFINITIONS END

Return the Architecture plan annotation payload now.
