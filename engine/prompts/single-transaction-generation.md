# Single-Transaction Creative Instruction

Use this prompt only after deterministic preflight passes. Insert the prepared context
at the marked boundary without adding fictional content.

---

You are the sole creative author of one complete Cathedrals generation instance.

Return exactly one JSON document and nothing else. It must conform to the supplied
`generation-bundle.schema.json`. Do not use Markdown fences, commentary, placeholders,
ellipsis, or references to content you have not included.

This response is the only creative transaction for this generation ID. There will be
no later planning, continuation, scene generation, critique, or rewrite call. Author
the complete fictional work now: generated work canon, five claimant identities,
other characters, exact incident and chronology, arcs, scenes, choices, artifacts,
clues, contradictions, endings, formal compositions, all reader-facing prose, and the
decision graph.

Obey the engine canon in the prepared context. Treat it as formal and aesthetic law,
not as prewritten plot.

Generate exactly five claimant identities simultaneously. The technical slot IDs are
semantically blank. Do not infer an archetype, occupation, voice, genre, evidence
family, emotional register, or route from slot order. Make the set pass every hard
differentiation rule in `claimants.yaml`, and make each claimant interact materially
and dramatically with the same generated annex incident.

Generate the exact threshold incident inside the allowed class. Decide its subjects,
circumstances, chronology, relationships, evidence, contradictions, culpability, and
consequences. Do not merely restate the event class.

Keep the work unmistakably Cathedrals: snowbound hospice-annex materiality; traces of
care and administration; pressure around responsibility, isolation, thresholds,
memory, documents, absence, judgment, contradiction, commitment, and foreclosure;
and the theme that saying yes closes other possibilities. Do not reduce this gravity
to generic mystery or generic haunting.

Use the supplied abstract topology without treating it as plot. Begin with three to
five reader-perspective scene surfaces before the first live decision hub. Give that
hub exactly three genuine situated actions, none of them a claimant selector. Split
branches again downstream. Preserve earlier state through reconvergence. Allow uneven
depths. Give every meaningful decision two to five live options. Give every major
irreversible decision a hesitation option whose consequences are not undo. Keep
`start_over` distinct from in-story reconsideration.

Use the supplied threshold figures, resultants, and tendencies as symbolic weather.
Do not turn figure names or example objects into mandatory characters or props. Do not
recompute or replace the supplied geomancy.

Make every scene perform at least two real dramatic jobs. Make clues alter
interpretation, choices produce consequence, artifacts behave as evidence, and
endings convert interpretation into foreclosure, transformation, implication,
release, or a graph-explicit new beginning. Integrate at least two meaningful formal
poetic compositions inside generated content.

Avoid generic ominous prose, faux profundity, lore dumping, therapist-speak,
exposition-vending characters, arbitrary abstraction, adjective-only differentiation,
stock AI uncanny language, inert atmosphere, decorative artifacts, cosmetic
branching, and unreadable experimentation. Keep prose concrete, controlled, literary,
and legible.

Respect every hard count and word budget. Include complete prose strings for every
scene, artifact, and ending. Use plain Markdown-compatible MDX only: no imports,
exports, scripts, or arbitrary JSX. Keep planning metadata concise enough to remain
inside the supplied structured-metadata allowance.

Echo the supplied provenance exactly, including `creative_transaction_count: 1`.

PREPARED CONTEXT BEGINS

{{DETERMINISTIC_PREPARED_CONTEXT}}

PREPARED CONTEXT ENDS

SUPPLIED JSON SCHEMA BEGINS

{{GENERATION_BUNDLE_SCHEMA}}

SUPPLIED JSON SCHEMA ENDS

Return the complete JSON document now.

---
