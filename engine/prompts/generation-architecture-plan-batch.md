# Architecture Plan Batch Instruction

Return exactly one Architecture plan annotation payload conforming to the supplied schema.
Return JSON only.

Annotate every supplied deterministic packet allocation by its exact `packet_slot_id`, including
both literary and ending allocations. Return one annotation per listed allocation; do not infer,
rename, add, or omit packets. Do not repeat the packet kind, technical slots, artifact count, or formal-composition count;
the engine merges those fixed allocations. Author priority, lawful dependencies, branch relation, attractor pressure, relevance,
and soft guidance. Dependencies may reference only prior staged packet IDs or earlier
packet IDs in this batch; this keeps the complete dependency graph acyclic.
Each ending plan selects exactly one ending attractor. Do not write scenes or prose.
Plan backward from its terminal transformation and prerequisites to earlier literary
packets. Express necessary setups in soft guidance. Technical-slot relevance may use
the allocated scene and ending IDs; state-key relevance must use declared runtime
state keys. A narrative milestone is a setup instruction, not a new state variable.
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
