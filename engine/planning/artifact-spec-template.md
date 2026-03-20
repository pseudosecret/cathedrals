# Artifact Spec Template

## Purpose

This file defines one artifact as a meaningful object within a specific work instance, arc, or scene sequence.

An artifact spec is not prose.
It is not a decorative prop list.
It is not a lore dump in document costume.

It must define:

- what the artifact is
- why it exists
- what interpretive pressure it applies
- what clue, contradiction, or residue it introduces
- how it relates to claimant logic and state logic
- what later prose generation must and must not do

Use this file as the planning input for artifact generation.

---

## Instructions for Completion

When filling this template:

- Be concrete.
- Be operational.
- Make the artifact plausible as an object first.
- Give it a real interpretive job.
- Do not use it as an excuse to explain the hidden setting directly.
- Do not invent new ontology unless canon explicitly permits it.
- Do not make the artifact decorative or redundant.
- If the artifact cannot be specified lawfully from canon and arc planning, flag it in an ambiguity report instead of guessing.

A good artifact spec should let a later generation pass create a readable artifact that matters.

---

## Artifact Identity

- **work_id:** `WORK_ID_HERE`
- **arc_id:** `ARC_ID_HERE | none`
- **scene_id:** `SCENE_ID_HERE | none`
- **artifact_id:** `ARTIFACT_ID_HERE`
- **artifact_title_working:** `ARTIFACT_TITLE_HERE`
- **status:** `planned | ready | blocked | revised`
- **priority:** `first_spike | core | secondary`
- **artifact_type:** `letter | form | chart | log | receipt | note | transcript | photograph_caption | room_card | report | other`
- **route_context:** `ROUTE_CONTEXT_HERE`
- **claimant_relevance:** `CLAIMANT_ID_HERE | multiple | none`

---

## Artifact Function

### One-Sentence Function

What does this artifact do?

`WRITE_ONE_SENTENCE_FUNCTION_HERE`

### Interpretive Function

What job does this artifact perform?

Examples:

- support claimant plausibility
- contradict prior evidence
- destabilize chronology
- pressure accusation
- reframe a scene
- reveal environmental drift through documentation
- leave residue after a choice

`WRITE_INTERPRETIVE_FUNCTION_HERE`

### Why This Artifact Exists

Why is this artifact needed instead of rolling its content into a scene?

`WRITE_REASON_HERE`

### Reader Effect

What should the reader feel or realize after encountering it?

Examples:

- uneasy confidence
- renewed doubt
- procedural suspicion
- emotional destabilization
- recognition that neutrality is collapsing

`WRITE_READER_EFFECT_HERE`

---

## Surface Reality

### Surface Plausibility

Why could this object plausibly exist in the setting?

`WRITE_SURFACE_PLAUSIBILITY_HERE`

### Physical or Documentary Form

What kind of object is it in the world?

Examples:

- intake form with handwritten corrections
- folded letter stained at one edge
- medication chart photocopy
- maintenance log page torn from binder
- room assignment card in plastic sleeve

`WRITE_DOCUMENTARY_FORM_HERE`

### Condition

What is its condition?

Examples:

- pristine
- worn from handling
- smudged
- partially redacted
- water-damaged
- copied and incomplete

`WRITE_CONDITION_HERE`

### Provenance

How does the reader encounter it?

Examples:

- found in drawer
- handed over by claimant
- taped inside cabinet
- embedded in a scene
- retrieved after a decision
- visible only after state shift

`WRITE_PROVENANCE_HERE`

### Route Diversion

Does this artifact divert the reader onto a materially different track or require its own page?

Examples:

- false because it should expand inline inside the scene flow
- true because it initiates a distinct branch or separate evidence corridor

Use a literal boolean in the compiled spec.

`WRITE_DIVERTS_ROUTE_HERE`

## Surface Contamination

### Artifact Contamination Band

What focus-scaled contamination band should govern this artifact overall?

Use one of:

- ambient
- passing_focus
- primary_focus
- dominant_focus

`WRITE_ARTIFACT_CONTAMINATION_BAND_HERE`

### Framing Contamination Rules

How may the framing prose around the artifact drift in diction, cadence, and structure?

`WRITE_FRAMING_CONTAMINATION_RULES_HERE`

### Document Body Contamination Rules

How may the core document body drift while remaining a plausible object?

`WRITE_DOCUMENT_BODY_CONTAMINATION_RULES_HERE`

### Material Distortion Rules

What visible distortions should carry contamination materially?

Examples:

- corrections left legible
- repeated labels
- reordered fields
- omitted lines
- unstable emphasis

`WRITE_MATERIAL_DISTORTION_RULES_HERE`

---

## Ontological Role

### Dominant Ontology

What world-logic is strongest in this artifact?

`WRITE_DOMINANT_ONTOLOGY_HERE`

### Truth Style

What kind of truth does this artifact seem to claim?

Examples:

- bureaucratic truth
- emotional truth
- diagnostic truth
- procedural truth
- partial witness truth
- contradictory institutional truth

`WRITE_TRUTH_STYLE_HERE`

### Claimant Pressures

How does this artifact pressure interpretation toward one or more claimants?

```yaml
claimant_pressures:
  - claimant: CLAIMANT_1
    effect: supports | complicates | undermines | reframes
    notes: NOTES_HERE
  - claimant: CLAIMANT_2
    effect: supports | complicates | undermines | reframes
    notes: NOTES_HERE
```

### Environmental Drift Expression

If the annex is mutating, how does this artifact express that drift?

Examples:

- numbering conventions have changed
- language becomes more institutional
- handwriting suggests layered realities
- categories shift from care to diagnosis
- document headers no longer match room labels

WRITE_ENVIRONMENTAL_DRIFT_EXPRESSION_HERE

## Required Content

### Required Clue or Contradiction

What concrete clue, contradiction, or pressure point must this artifact contain?

WRITE_REQUIRED_CLUE_OR_CONTRADICTION_HERE

### Minimum Concrete Detail Requirement

What specific, memorable detail must appear?

Examples:

- two signatures in different inks
- a scratched-out room number
- a date that precedes the patient’s supposed arrival
- a checkbox marked in contradiction to the handwritten note
- a folded corner hiding a crucial line

WRITE_MINIMUM_CONCRETE_DETAIL_HERE

### Required Internal Features

What must the artifact include structurally?

Examples:

- date
- signature field
- room designation
- missing line
- contradictory notation
- stamped header
- personal salutation
- dosage schedule
- maintenance initials

```yaml
required_internal_features:
  - FEATURE_1
  - FEATURE_2
  - FEATURE_3
```

### Required Interpretive Pressure

How should this artifact bend interpretation?

Examples:

- make one claimant more plausible while opening a contradiction
- make chronology less stable
- make accusation feel more tempting but less certain
- expose the annex as institutionally inconsistent
- make the reader distrust the surface narrative

WRITE_REQUIRED_INTERPRETIVE_PRESSURE_HERE

## Forbidden Content

### Forbidden Reveals

What must this artifact not reveal directly?

Examples:

- the final truth of the central transgression
- explicit hidden cosmology
- confirmed metaphysical explanation
- full resolution of claimant conflict

```yaml
forbidden_reveals:
  - FORBIDDEN_REVEAL_1
  - FORBIDDEN_REVEAL_2
  - FORBIDDEN_REVEAL_3
```

### Forbidden Failure Modes

What would make this artifact weak or invalid?

Examples:

- only atmospheric flavor
- no change to interpretation
- could belong to any claimant unchanged
- implausible as an object
- overexplains what should remain indirect

```yaml
forbidden_failure_modes:
  - FAILURE_1
  - FAILURE_2
  - FAILURE_3
```

### Forbidden Style Failures

```yaml
forbidden_style_failures:
  - faux archival language with no function
  - generic creepiness
  - obvious exposition disguised as document text
  - claimant voice blur
  - decorative ambiguity without pressure
```

## Scene and Arc Intersections

### Linked Scenes

Which scenes should this artifact intersect with?

```yaml
linked_scenes:
  - SCENE_ID_1
  - SCENE_ID_2
```

### Arc Role

What does this artifact do within the larger arc?

Examples:

- anchors plausibility beat
- triggers contradiction beat
- intensifies pressure beat
- helps create threshold toward accusation
- provides residue after a choice

WRITE_ARC_ROLE_HERE

### Timing of Encounter

When should the reader meet this artifact?

Examples:

- before first claimant contact
- between scene 1 and scene 2
- during contradiction beat
- only after a decision
- only in debug or alternate state

WRITE_TIMING_OF_ENCOUNTER_HERE

## Decision and State Relevance

### Decision Relevance

Does this artifact affect a decision point?

true | false

### If Yes, How?

How does it affect the decision?

Examples:

- adds plausibility to one branch
- creates a new hesitation
- unlocks an alternate option
- deepens contamination risk through extra browsing
- destabilizes a prior accusation

WRITE_DECISION_RELEVANCE_HERE | none

### State Relevance

What state variables does this artifact touch?

```yaml
state_relevance:
  accusation:
    effect: up | down | none | conditional
    notes: NOTES_HERE
  contamination:
    effect: up | down | none | conditional
    notes: NOTES_HERE
  indecision_count:
    effect: up | down | none | conditional
    notes: NOTES_HERE
  dominant_regime:
    effect: toward_claimant | neutral | unstable | none | conditional
    notes: NOTES_HERE
  artifacts_seen:
    effect: add
    notes: NOTES_HERE
  world_scars:
    effect: add | none | conditional
    notes: NOTES_HERE
```

### Residue

What should linger after the artifact is read?

WRITE_RESIDUE_HERE

## Presentation and Form

### Intended Presentation Mode

How should this artifact be rendered in prose or MDX?

Examples:

- full document transcription
- excerpt with framing note
- facsimile-styled block
- embedded document inside scene page
- standalone artifact page
- `inline_expandable`
- `route_diverting`

WRITE_INTENDED_PRESENTATION_MODE_HERE

### Preview Excerpt

What short excerpt or first lines should appear before expansion?

Examples:

- first three lines of the note
- form header plus one contradictory field
- one paragraph and the marked correction line

WRITE_PREVIEW_EXCERPT_HERE

### Expand Label

What should the expansion affordance say?

Examples:

- read more
- expand document
- open full record

WRITE_EXPAND_LABEL_HERE

### Material Emphasis Markers

What specific marks, corrections, or physical details must the renderer make visually legible?

Examples:

- scratched-out room number
- two initials in different inks
- folded corner concealing a line
- stamped header and blank witness field

```yaml
material_emphasis_markers:
  - MARKER_1
  - MARKER_2
  - MARKER_3
```

### Readability Constraints

What must remain readable and legible?

Examples:

- line breaks must survive on mobile
- handwriting simulation must not obscure text
- redactions must not hide all usable content
- table-like layout must degrade gracefully
- preview excerpt and expanded artifact must both remain legible

WRITE_READABILITY_CONSTRAINTS_HERE

### Mobile Constraints

Any mobile-specific rules?

WRITE_MOBILE_CONSTRAINTS_HERE

## Generation Constraints

### Voice and Register

What prose/document register should later generation obey?

Examples:

- restrained institutional language
- intimate but unstable personal address
- clipped procedural documentation
- cool diagnostic notation

WRITE_VOICE_AND_REGISTER_HERE

### Density

How dense should the artifact be?

Examples:

- lean and functional
- medium density with one contradiction cluster
- compressed and sharp
- sparse but loaded

WRITE_DENSITY_HERE

### Structural Format Notes

How should later generation structure the artifact?

Examples:

- header, body, signature block
- dated entries in sequence
- form fields with handwritten correction
- short paragraphs plus notation block

WRITE_STRUCTURAL_FORMAT_NOTES_HERE

### What the Generator Must Preserve

```yaml
generation_invariants:
  - INVARIANT_1
  - INVARIANT_2
  - INVARIANT_3
```

### What the Generator May Vary

```yaml
generation_variations_allowed:
  - SURFACE_WORDING
  - MINOR_LAYOUT_FEATURES
  - LOCAL_OBJECT_DETAILS
  - INCIDENTAL_PHRASING
```

## Validation Checks

### Artifact Must Achieve

```yaml
artifact_must_achieve:
  - REQUIREMENT_1
  - REQUIREMENT_2
  - REQUIREMENT_3
```

### Artifact Fails If

```yaml
artifact_fails_if:
  - FAILURE_1
  - FAILURE_2
  - FAILURE_3
```

### Distinctiveness Check

Why is this artifact specific to this route, claimant pressure, or interpretive problem?

WRITE_DISTINCTIVENESS_CHECK_HERE

### Legibility Check

Why can a reader understand its surface significance even without grasping the hidden metaphysics?

WRITE_LEGIBILITY_CHECK_HERE

### Artifact Plausibility Check

Why does it still feel like a real object rather than lore theater?

WRITE_ARTIFACT_PLAUSIBILITY_CHECK_HERE

## Output Target

### Planning Source Path

engine/planning/artifact-specs/ARTIFACT_SPEC_FILENAME.md

### Prose Output Target

prose/artifacts/ARTIFACT_FILENAME.mdx

### Structural Export Notes

Anything this artifact must contribute to route graphs, state tracking, or debug views?

Examples:

- stable artifact_id
- linked scene ids
- decision relevance marker
- claimant pressure metadata
- inline expansion metadata
- diverts_route boolean

WRITE_STRUCTURAL_EXPORT_NOTES_HERE

## Notes for the Prose Generator

Use this section to hand off sharp instructions to the artifact generation pass.

Examples:

- keep it plausible as hospice paperwork first
- let the contradiction emerge through small discrepancies
- avoid explicit statement that the release is impossible
- make the dates clean but the signatures troubling
- preserve emotional coldness

WRITE_NOTES_FOR_PROSE_GENERATOR_HERE

## Completion Checklist

Before treating this artifact spec as usable, confirm:

- [ ] artifact identity fields are filled
- [ ] artifact function is concrete
- [ ] surface plausibility is defined
- [ ] claimant pressures are specified
- [ ] required clue or contradiction is specific
- [ ] forbidden reveals are listed
- [ ] scene and arc intersections are meaningful
- [ ] state relevance is specified
- [ ] presentation constraints are usable
- [ ] preview excerpt is specified
- [ ] expand label is specified
- [ ] route diversion behavior is specified
- [ ] validation checks are sharp
- [ ] prose target path is plausible
- [ ] nothing here depends on invented canon
