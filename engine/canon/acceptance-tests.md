# Acceptance Tests

Every accepted work must pass mechanical validation and artistic acceptance. A failure
kills that generation. Nothing in this file authorizes creative repair.

## README Conformance

### Authorship

1. Can the human know the five fictional claimant identities before generation? **No.**
2. Can the human know their exact roles, voices, or evidence modes before generation? **No.**
3. Can the human know the exact central incident before generation? **No, beyond its event-class envelope.**
4. Can the human know what happens scene by scene? **No.**
5. Can the human know exactly which artifacts will exist? **No.**
6. Can the human know exactly what the endings depict? **No.**

### Artistic Identity

7. Is the work recognizably Cathedrals rather than generic AI fiction? **Yes.**
8. Are the hospice annex, judgment mechanics, thematic pressure, branching grammar,
   threshold geomancy, and compositional law strongly authored? **Yes.**
9. Are all five generated claimant forces substantially differentiated? **Yes.**

### One Creative Transaction

10. How many creative model transactions produced the work? **Exactly 1.**
11. Was generated creative material used as the prompt for another creative stage? **No.**
12. Was any scene authored in a later independent creative pass? **No.**
13. Was any generated prose creatively rewritten by a human or model? **No.**

### Failure Behavior

14. Can a bad work be rejected? **Yes.**
15. Can that same generated work be creatively repaired? **No.**
16. Can an entirely fresh generation be attempted later? **Yes.**

### Runtime

17. Does the final experience require AI? **No.**
18. Is the final reader artifact static? **Yes.**

Any wrong answer is a conformance failure.

## Mechanical Validation

Fail the generation for any of the following:

- the response is not one complete JSON document
- the bundle fails `engine/data/generation-bundle.schema.json`
- `creative_transaction_count` is not `1`
- IDs are duplicated or references dangle
- claimant slots are missing, repeated, or not exactly five
- graph nodes, edges, entry, or redirects are invalid
- the opening hub does not have exactly three playable edges
- another meaningful decision has fewer than two or more than five playable edges
- an opening branch does not split again
- required reconvergence loses inbound state
- a major irreversible decision lacks consequential hesitation
- required scenes, artifacts, endings, formal compositions, or prose bodies are absent
- the response exceeds the declared scope or was produced without a passing budget preflight
- generated MDX uses executable imports, exports, scripts, or unapproved components
- frontmatter, serialization, or Astro compilation fails
- accepted literary hashes do not match the generated files

Pure serialization repair is lawful only when the literary strings and creative facts
remain byte-for-byte unchanged. Otherwise fail the generation.

## Claimant-Set Acceptance

Pass only if:

- all five identities, incident roles, voices, evidence logics, contradiction modes,
  environmental pressures, and consequences were generated in the single transaction
- each pair is substantially different on the axes in `engine/data/claimants.yaml`
- at least one claimant pressures truth materially or institutionally
- at least one pressures truth relationally or experientially
- at least one way of knowing is initially difficult for the others to assimilate
- influence emerges unevenly through the work rather than as five symmetrical routes

Fail if any claimant is a renamed prewritten archetype, an assigned difference role, or
interchangeable with another after surface adjectives are removed.

## Scene and Route Acceptance

A scene passes only if it:

- performs at least two dramatic jobs
- contains at least one memorable concrete detail
- changes knowledge, pressure, state, interpretation, or consequence
- makes clues alter interpretation
- presents clear actions when it contains a decision
- preserves the generated claimant pressure appropriate to its focus

The work passes only if:

- three to five reader-perspective scene surfaces precede the first live hub
- the first live hub offers exactly three situated actions and is not a claimant menu
- downstream branches split again, terminate at unequal depths, or reconverge meaningfully
- earlier path state survives reconvergence
- hesitation creates residue rather than undo
- `start_over` remains distinct from in-story reconsideration
- endings convert interpretation into consequence; redirective endings are graph-explicit

## Artifact Acceptance

Each artifact must:

- plausibly exist as a material or documentary object
- support, complicate, or bias interpretation
- contain a legible clue, contradiction, omission, or pressure point
- remain readable on mobile
- behave as evidence rather than decoration or disguised exposition

## Artistic Acceptance

Evaluate the complete immutable generation, then return only `PASS` or
`FAIL GENERATION` with reasons. Fail for:

- generic ominous prose, faux profundity, lore dumping, or therapist-speak
- arbitrary abstraction or stock AI uncanny-language habits
- exposition-vending characters or interchangeable voices
- adjective-only stylistic differentiation
- unreadable experimental prose
- atmospheric but inert scenes
- cosmetic branching or inconsequential choices
- meaningless artifacts
- redundant routes, evidence logic, scenes, or endings
- weak concrete detail or incoherent thematic development
- endings that recap instead of foreclose, transform, condemn, release, or redirect

Artistic findings are verdicts, not revision instructions.

## Build Acceptance

The accepted bundle must compile into an Astro static site with:

- prose-dominant, intentionally art-directed reading surfaces
- strong hierarchy and restrained route-sensitive visual pressure
- mobile readability and accessible interactions
- light and dark treatments with sufficient contrast
- clear choices and meaningful artifact presentation
- ceremonial endings and a legible taken-path visualization
- client-side state only and no live AI or server dependency

Fail a visually generic build that resembles text dropped into a template.
