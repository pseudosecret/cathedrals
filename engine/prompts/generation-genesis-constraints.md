# Genesis Constraint Instruction

Return exactly one Genesis constraints payload conforming to the supplied schema.
Return JSON only.

Extract only minimal initial constraints grounded in the immutable foundation and cast:
at most 12 initial canonical facts, coalescing equivalent facts;
at most 24 knowledge changes; and at most 8 motif events. Identify each source using exactly one
handle from VALID GENESIS SOURCE HANDLES. World canon sections and chronology events are valid
sources in their own right. Choose the source that contains the evidence: a claimant anchor,
a complete claimant profile, a supporting character, or a canon section. The engine binds each
handle to its original commit and JSON Pointer; do not substitute a character for world canon.
Leave relevance.technical_slot_ids empty or omit it; the engine derives the direct source tag.
Leave relevance.arc_ids and relevance.branch_ids empty; Architecture does not exist yet.
Use committed `claimant_NN` or `character_NNN`
IDs—not technical slots—as knowledge subjects. Use `fact_01`, `fact_02`, and so on when a knowledge change
refers to that exact fact position in this payload. Reuse the fact alias when several
knowledge changes concern the same fact; do not number aliases by knowledge-row
position. Motif IDs declare local motif-state keys. Use only a string, number,
boolean, or null as each fact value. Leave
new soft obligations and obligation updates empty; Architecture owns initial future
pressure. The engine assigns IDs and provenance, coalesces duplicate facts, and may
resolve an unknown reference or expand the claimant set before commit. Do not add
fiction, revise wording, deliberately repeat equivalent facts, or emit a synopsis.

IMMUTABLE GENESIS CONTEXT BEGINS

{{GENESIS_CONSTRAINT_CONTEXT}}

IMMUTABLE GENESIS CONTEXT ENDS

RELEVANT PROTOCOL DEFINITIONS BEGIN

{{GENESIS_CONSTRAINT_PROTOCOL_DEFINITIONS}}

RELEVANT PROTOCOL DEFINITIONS END

Return the Genesis constraints payload now.
