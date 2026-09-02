# Acceptance Tests

Every accepted work must pass mechanical validation and whole-work artistic
acceptance. Failure kills the generation. Nothing here authorizes creative repair.

## Authorship Boundary

Before generation, all answers must be `No`:

1. Can the human know the five fictional claimant identities?
2. Can the human know their exact roles, relationships, voices, or evidence modes?
3. Can the human know the exact central incident beyond its event-class envelope?
4. Can the human know what happens scene by scene?
5. Can the human know which exact artifacts, formal compositions, or endings exist?

Pass only when exactly five semantically blank slots were instantiated together in
genesis and no fictional claimant menu, archetype, name, occupation, evidence family,
genre, contradiction mode, or consequence existed in engine canon.

## Autonomous Run and Irreversibility

Pass only when:

- one frozen initial `generation_brief` initiated the entire run
- the brief was never mutated and no human creative input entered after start
- `creative_step_count >= 1`; multiple creative calls are lawful
- genesis, architecture, and packet dependencies proceeded causally forward
- every valid creative response was committed without candidate scoring or selection
- no committed creative artifact or fact was rewritten, regenerated, replaced,
  silently retconned, or removed
- later calls used earlier material only as immutable evidence and causal history
- `human_intervention_count = 0`
- `committed_rewrite_count = 0`
- `committed_regeneration_count = 0`
- `backtrack_count = 0`

Any wrong condition is a conformance failure.

## Ledger and Protocol Validation

Fail for any of the following:

- a run record fails `engine/data/generation-protocol.schema.json`
- ledger sequences or SHA-256 links are missing, duplicated, reordered, or invalid
- a committed-record hash differs from its ledger output hash
- a canonical-state parent hash does not equal the preceding committed state hash
- the frozen engine snapshot, brief, explicit scene scope, model parameters, seeds, or traversal
  law changes during the run
- step-specific provider/model, prompt/context hashes, timestamps, output hashes,
  artifact IDs, deltas, branch relation, commit status, or token/cost fields are absent
- a failed attempt is hidden or a technical retry changes prompt, context, parameters,
  or seed
- a valid creative result is discarded in favor of another candidate
- derived scope, packet, cumulative token/cost, retrieval, or constraint bounds are exceeded

## Content and Graph Validation

Fail when:

- IDs duplicate or references dangle
- claimant slots are missing, repeated, or not exactly five
- any architecture node lacks exactly one committed reader-facing output
- prospective packet choice violates frozen dependencies or mutates canon
- literary/ending packet sizes or whole-work derived scope bounds fail
- the opening hub lacks exactly three playable situated actions after three to five
  reader-perspective scenes, or acts as a claimant menu
- another meaningful decision has fewer than two or more than five playable actions
- opening branches do not split again
- reconvergence erases consequential inbound state
- branch depth is uniformly shallow without dramatic cause
- a major irreversible decision lacks consequential hesitation
- a technical destination is absent from architecture, unresolved, or owned more than once
- a generated content destination names unwritten future content instead of a frozen technical slot
- redirective endings point anywhere except exactly resolved prebuilt content
- a stateful variant is cosmetic
- formal-composition anchors or required source evidence are absent
- generated Markdown contains authored HTML/executable MDX, raw HTML is enabled in the renderer, or deterministic projection changes literary bytes
- graph/state/frontmatter/static Astro compilation fails

## Constraint-Topology Validation

Pass only when immutable source, minimal canonical facts, character knowledge, typed
future obligations, motif pressure, and mutable prospective planning remain distinct.
Every derived constraint identifies immutable source type, artifact ID, locator,
source commit, and source hash; original sources remain retrievable; corrections append
superseding events; and source truth outranks derived state.

Fail a dangling or circular obligation graph, a silently vanished obligation, a
satisfied debt without evidence, an unlawful universal-obligation foreclosure, a
foreclosed attractor without the immutable event that negated it, an ending missing a
hard prerequisite, tracked character reasoning from explicitly unavailable knowledge,
recursive summary chains, or any analysis call that writes replacement fiction.

## Long-Form Structural Health

Fail or strongly penalize endless mystery creation without repayment; arbitrary or
unseeded endings; obvious mechanical foreshadowing; early objects that exist only for
an ending; repeated motifs whose meaning never changes; claimant drift caused by lost
epistemic state; checklist-style obligation fulfillment; technically valid but
causally unearned endings; excessive tidiness that destroys ambiguity; and branches
whose cosmetic differences share one teleology.

Reward causal pressure without plot bureaucracy. Deliberate ambiguity may resolve by
contradiction, foreclosure, transformation, contamination, reader judgment, or
irreducible ambiguity. Attractors should create gravity while leaving realization
surprising.

## Claimant-Set Acceptance

Pass only if every pair is substantially different on the axes in
`engine/data/claimants.yaml`; at least one claimant pressures truth materially or
institutionally; at least one pressures it relationally or experientially; at least
one way of knowing is initially difficult for the others to assimilate; and influence
emerges unevenly rather than as five symmetrical routes.

Fail a renamed prewritten archetype, assigned difference role, or claimant
interchangeable with another after surface adjectives are removed.

## Scene, Artifact, and Ending Acceptance

Each scene must perform at least two dramatic jobs, contain memorable concrete
detail, change interpretation/pressure/state/consequence, and preserve relevant
claimant pressure. Each artifact must plausibly exist, alter interpretation, carry a
clue/contradiction/omission/pressure point, remain readable, and behave as evidence.

The work must preserve downstream splitting, meaningful reconvergence, unequal depth,
stateful hesitation, contamination, `start_over` semantics, and endings that transform
or foreclose rather than recap. Every choice and hidden path must already exist before
play.

## Failure Behavior

- Transport or provider failure before creative output may retry identically.
- Malformed creative output fails the run; do not infer or regenerate it.
- Artistically weak but mechanically valid output commits and remains history.
- Contradiction may remain when it is diegetically lawful.
- Unresolvable mechanical continuity failure ends the run without retcon.
- Whole-work artistic acceptance returns only `PASS` or `FAIL GENERATION` with
  concrete reasons and no replacement text.
- A new attempt uses a new generation ID.

## Complete-Work and Runtime Acceptance

`READY_TO_PLAY` requires complete generated canon, all planned content and state
variants, decision graph, projections, mechanical pass, artistic pass, static Astro
build, build validation, hashes, and complete-work barrier. A failed or incomplete
run has `playable: false` and terminal state `FAILED_GENERATION`.

The final experience is static, client-state-only, and AI-free. It never generates a
chapter, branch, ending, or revision during play and never waits for player feedback
or a model response.

## Artistic Acceptance

Evaluate the complete immutable work after creative generation. Return only `PASS` or
`FAIL GENERATION` with reasons. Fail generic ominous prose, faux profundity, lore
dumping, therapist-speak, arbitrary abstraction, interchangeable voices, adjective-
only differentiation, inert scenes, cosmetic branching, meaningless artifacts,
redundancy, weak concrete detail, incoherent thematic development, or endings that
merely recap. Findings are verdicts, not revision instructions.

## Build Acceptance

The accepted run must compile into an Astro static site with prose-dominant,
intentionally art-directed surfaces; mobile readability; accessible interaction;
light/dark contrast; clear choices; meaningful artifact presentation; ceremonial
endings; path visualization; client-side state only; and no runtime AI or server
dependency. Fail a generic template treatment.

Pass only when Markdown headings, emphasis, blockquotes, and lists render as semantic
HTML while immutable source bytes remain exact. Genesis art direction must validate,
produce deterministic work-specific CSS through bounded mappings, retain visible
focus and readable contrast, and expose no arbitrary CSS or script surface.

New generation branches must start from the configured engine base commit, never a
prior generation branch. Successful publication stages only its own
`generated-work/<generation-id>/` tree and creates one final generation commit.
Failed runs remain under ignored `.cathedrals/runs/` by default and leave tracked
paths clean.

A complete mechanically valid work must build before whole-work artistic acceptance.
Artistic rejection remains `FAILED_GENERATION`, `playable: false`, and outside accepted
publication even when its ignored diagnostic static build remains available for
inspection.
