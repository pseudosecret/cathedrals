# Scene Spec Template

## Purpose

This file defines one scene as a structural unit within a specific arc and work instance.

A scene spec is not prose.
It is not a mood paragraph.
It is not a synopsis written to sound literary.

It must define:

- what this scene is for
- what beat role it performs
- what state it assumes on entry
- what changes by the end
- what evidence, pressure, or mutation it introduces
- what options it presents, if any
- what later prose generation must and must not do

Use this file as the immediate planning input for scene generation.

---

## Instructions for Completion

When filling this template:

- Be concrete.
- Be operational.
- Keep it brief but sufficient.
- Prefer function over flourish.
- Do not write the final scene here.
- Do not solve missing canon by improvising.
- Do not create a scene that lacks a clear job.
- If the scene cannot be specified lawfully from canon and arc brief, flag it in an ambiguity report.

A good scene spec should let a later generation pass write the scene without inventing its structural purpose.

---

## Scene Identity

- **work_id:** `WORK_ID_HERE`
- **arc_id:** `ARC_ID_HERE`
- **scene_id:** `SCENE_ID_HERE`
- **scene_title_working:** `SCENE_TITLE_HERE`
- **status:** `planned | ready | blocked | revised`
- **priority:** `first_spike | core | secondary`
- **scene_type:** `interview | exploration | artifact_encounter | threshold | accusation | residue | transition | other`
- **claimant:** `CLAIMANT_ID_HERE | none`
- **route_context:** `ROUTE_CONTEXT_HERE`

---

## Scene Function

### One-Sentence Function

What does this scene do?

`WRITE_ONE_SENTENCE_FUNCTION_HERE`

### Beat Role

What beat from the arc grammar does this scene fulfill?

Examples:

- invitation
- plausibility
- contradiction
- pressure
- threshold
- aftershock
- residue
- artifact_interruption
- premature_lock

`WRITE_BEAT_ROLE_HERE`

### Scene Purpose

What is this scene structurally for?

Examples:

- establish claimant plausibility
- introduce contradiction
- increase pressure toward accusation
- reveal a concrete fact
- mutate the annex
- create a decision point
- leave residue after a choice

`WRITE_SCENE_PURPOSE_HERE`

### Why This Scene Exists

Why is this scene needed instead of being merged into another scene?

`WRITE_REASON_HERE`

---

## Entry State

### Required Preconditions

What must already be true for this scene to occur?

```yaml
required_preconditions:
  - PRECONDITION_1
  - PRECONDITION_2
```

### Current State Inputs

What state assumptions does this scene take as input?

```yaml
current_state_inputs:
  accused_claimant: VALUE_HERE
  dominant_regime: VALUE_HERE
  contamination: VALUE_HERE
  indecision_count: VALUE_HERE
  retraction_count: VALUE_HERE
  claimants_seen:
    - CLAIMANT_1
  artifacts_seen:
    - ARTIFACT_1
  world_scars:
    - SCAR_1
```

## Entry Tone / Pressure

What pressure should already be active when this scene begins?

Examples:

- procedural suspicion
- uneasy neutrality
- mounting contradiction
- exhausted hesitation
- quiet foreclosure

WRITE_ENTRY_TONE_PRESSURE_HERE

## Claimant Focus and Surface Contamination

### Primary Claimant Focus

Which claimant is currently exerting the strongest prose-surface pressure?

Use one of:

- ambient
- passing_focus
- primary_focus
- dominant_focus

Also name the claimant if the scene is route-bound.

`WRITE_PRIMARY_CLAIMANT_FOCUS_HERE`

### Secondary Claimant Bleed

Does another claimant lightly contaminate the scene in passing?

Use `none` if not applicable, or describe the claimant and intensity briefly.

`WRITE_SECONDARY_CLAIMANT_BLEED_HERE`

### Contamination Intensity Band

What intensity band must later prose generation obey?

Examples:

- ambient
- passing_focus
- primary_focus
- dominant_focus

`WRITE_CONTAMINATION_INTENSITY_BAND_HERE`

### Diction Requirements

What claimant-specific lexical contamination must later prose generation show here?

`WRITE_DICTION_REQUIREMENTS_HERE`

### Cadence Requirements

What claimant-specific sentence rhythm or pacing must later prose generation show here?

`WRITE_CADENCE_REQUIREMENTS_HERE`

### Structure Requirements

What claimant-specific paragraph or structural behavior must later prose generation show here?

`WRITE_STRUCTURE_REQUIREMENTS_HERE`

## Threshold Geomancy

### Usage Enabled

true

### Threshold Figure Current

Which threshold figure governs this scene?

CURRENT_FIGURE_HERE

### Threshold Figure Next

If there is a lawful next scene, which figure tentatively governs it?

### NEXT_FIGURE_HERE | none

Threshold Resultant

### If explicitly derivable, what resultant governs the transition?

RESULTANT_FIGURE_HERE | undefined | none

### Scene Motion

How should the current figure shape the internal movement of this scene?

Examples:

- controlled escalation
- stalled negotiation
- cold narrowing
- expressive spill
- procedural bottleneck

WRITE_SCENE_MOTION_HERE

### Transition Pressure

How should the scene transition toward the next scene, if one exists?

Examples:

- narrowing
- interruption
- drift
- administrative closure
- unresolved carryover
- abrupt cut

WRITE_TRANSITION_PRESSURE_HERE

### Termination Bias

Does this scene carry heightened risk of premature ending, lockout, death, disappearance, or unresolved exit?

WRITE_TERMINATION_BIAS_HERE

## Ontological and Environmental Role

### Dominant Ontology in This Scene

What world-logic is strongest here?

WRITE_DOMINANT_ONTOLOGY_HERE

### Truth Style in This Scene

What counts as persuasive truth here?

Examples:

- records
- witness inconsistency
- memory residue
- symptoms
- spatial anomaly
- institutional paperwork

WRITE_TRUTH_STYLE_HERE

### Environmental Drift

What changes in the environment should this scene express?

Examples:

- labels proliferate
- doors gain numbers
- language becomes diagnostic
- warmth feels staged
- objects seem arranged for testimony

WRITE_ENVIRONMENTAL_DRIFT_HERE

### Surface Plausibility

How does this scene remain materially believable on the surface?

WRITE_SURFACE_PLAUSIBILITY_HERE

## Required Outputs

This is the heart of the scene spec.

The scene must do at least two meaningful things.

### Required Outputs

List the required scene jobs.

```yaml
required_outputs:
  - reveal_concrete_fact: FACT_HERE
  - complicate_interpretation: HOW_HERE
  - increase_pressure: HOW_HERE
  - bias_toward_claimant: WHICH_CLAIMANT_AND_HOW
  - environmental_mutation: WHAT_CHANGES
  - leave_residue: WHAT_REMAINS
```

### Minimum Concrete Detail Requirement

What specific, rememberable detail must appear?

Examples:

- a mismatched signature on a release form
- a room number scratched out and rewritten
- a medication chart with one line missing
- a polished chair in an otherwise abandoned corridor

WRITE_MINIMUM_CONCRETE_DETAIL_HERE

### Clue or Evidence Function

What clue, contradiction, or evidence must the reader get here?

WRITE_CLUE_OR_EVIDENCE_FUNCTION_HERE

### Interpretation Pressure

How should this scene push interpretation?

Examples:

- strengthen one claimant while opening a contradiction
- make neutrality less plausible
- make prior evidence unstable
- make accusation feel prematurely tempting

WRITE_INTERPRETATION_PRESSURE_HERE

## Forbidden Outputs

What must not happen here?

Examples:

- final resolution of the central transgression
- explicit lore dump
- claimant monologue explaining metaphysics
- purely atmospheric drift with no consequence
- scene that could belong to any route unchanged

```yaml
forbidden_outputs:
  - FORBIDDEN_OUTPUT_1
  - FORBIDDEN_OUTPUT_2
  - FORBIDDEN_OUTPUT_3
```

### Forbidden Style Failures

What style failures must be actively avoided here?

```yaml
forbidden_style_failures:
  - generic ominous prose
  - faux-profound abstraction
  - claimant voice blur
  - decorative weirdness without pressure
```

## Artifact Intersections

### Artifact Reference

Does this scene involve an artifact directly?

ARTIFACT_ID_HERE | none

### Artifact Function in Scene

If yes, what is the artifact doing here?

Examples:

- introducing contradiction
- anchoring claimant plausibility
- providing procedural evidence
- destabilizing timeline
- recontextualizing prior scene

WRITE_ARTIFACT_FUNCTION_HERE

### Artifact Handling Rules

How should the artifact be encountered?

Examples:

- found in drawer
- handed over by claimant
- embedded in room
- partially legible
- presented as copy not original

WRITE_ARTIFACT_HANDLING_RULES_HERE

## Decision Structure

Does This Scene Contain a Decision Point?

true | false

## Decision Purpose

If yes, what is the decision structurally for?

Examples:

- choose route emphasis
- commit to claimant contact
- defer accusation
- inspect artifact or move on
- risk contamination for more information

WRITE_DECISION_PURPOSE_HERE | none

### Decision Options

List the options at the level of structural intent, not polished final prose.

Each option must have a stable edge_id.

```yaml
decision_options:
  - edge_id: EDGE_ID_1
    label_working: OPTION_LABEL_HERE
    outcome_summary: WHAT_THIS_OPTION_DOES
    target_scene_id: TARGET_SCENE_ID_HERE | none
    state_effects:
      - EFFECT_1
      - EFFECT_2
  - edge_id: EDGE_ID_2
    label_working: OPTION_LABEL_HERE
    outcome_summary: WHAT_THIS_OPTION_DOES
    target_scene_id: TARGET_SCENE_ID_HERE | none
    state_effects:
      - EFFECT_1
      - EFFECT_2
```

### Chosen-Path Significance

Why does the choice here matter?

WRITE_CHOSEN_PATH_SIGNIFICANCE_HERE

### Closed Sibling Significance

What do the rejected options represent thematically or structurally?

WRITE_FORECLOSED_SIBLING_SIGNIFICANCE_HERE

### Reader-Surface Closed Option Handling

How should any non-playable sibling option appear in the normal reader-facing build?

Examples:

- do not show it as a live scene choice
- reserve it for ending path view only
- refer to it as a closed option in reader-facing language

WRITE_CLOSED_OPTION_HANDLING_HERE

## State Delta

What changes by the end of the scene?

```yaml
state_delta:
  accusation:
    effect: up | down | none | conditional
    notes: NOTES_HERE
  contamination:
    effect: up | down | none | conditional
    notes: NOTES_HERE
  indecision_count:
    effect: up | down | none | conditional
    notes: NOTES_HERE
  retraction_count:
    effect: up | down | none | conditional
    notes: NOTES_HERE
  dominant_regime:
    effect: toward_claimant | neutral | unstable | none | conditional
    notes: NOTES_HERE
  world_scars:
    effect: add | none | conditional
    notes: NOTES_HERE
  claimants_seen:
    effect: add | none
    notes: NOTES_HERE
  artifacts_seen:
    effect: add | none
    notes: NOTES_HERE
```

### Residue

What must remain wrong, unresolved, or altered after the scene ends?

WRITE_RESIDUE_HERE

## Premature Ending and Risk

### Premature Ending Risk

none | low | medium | high

### Allowed Premature Outcomes From This Scene

If the scene can terminate an arc early, list lawful outcomes.

```yaml
allowed_premature_outcomes:
  - none
  - unresolved_exit
```

### Risk Notes

How could this scene push toward premature ending without invalidating the arc?

WRITE_RISK_NOTES_HERE

## Generation Constraints

### Voice and Register

What prose register should later generation obey here?

Examples:

- restrained administrative unease
- intimate elegiac pressure
- cold diagnostic observation

WRITE_VOICE_AND_REGISTER_HERE

### Scene Density

How dense should the scene feel?

Examples:

- lean and functional
- medium density with one sharp image cluster
- compressed and tense
- slower, layered, document-heavy

WRITE_SCENE_DENSITY_HERE

### Pacing Notes

What pacing should later prose generation follow?

Examples:

- begin concrete, escalate into contradiction
- delay explanation until final paragraph
- move quickly to the decision threshold
- keep transitions clipped and procedural

WRITE_PACING_NOTES_HERE

### What the Prose Generator Must Preserve

List the invariants.

```yaml
generation_invariants:
  - INVARIANT_1
  - INVARIANT_2
  - INVARIANT_3
```

### What the Prose Generator May Vary

List the allowed variation space.

```yaml
generation_variations_allowed:
  - SURFACE_WORDING
  - LOCAL_DESCRIPTION
  - MINOR_OBJECT_DETAILS
  - DIALOGUE_PHRASE_SHAPE
```

## Validation Checks

This section defines what later validation must confirm.

### Scene Must Achieve

```yaml
scene_must_achieve:
  - REQUIREMENT_1
  - REQUIREMENT_2
  - REQUIREMENT_3
```

### Scene Fails If

```yaml
scene_fails_if:
  - FAILURE_1
  - FAILURE_2
  - FAILURE_3
```

### Distinctiveness Check

Why is this scene specific to this route or arc?

WRITE_DISTINCTIVENESS_CHECK_HERE

### Legibility Check

Why should a reader be able to understand what changed or mattered here, even if they do not understand the hidden metaphysics?

WRITE_LEGIBILITY_CHECK_HERE

### Reader Surface Order

How should the default reader-facing scene surface be composed?

Default:

1. title
2. prose
3. choices

WRITE_READER_SURFACE_ORDER_HERE

### Back Action Behavior

What should the back action do from this scene in normal reading flow?

Examples:

- return to the immediately previous scene
- return to the title page only from scene 1
- remain available without visually competing with primary choices

WRITE_BACK_ACTION_BEHAVIOR_HERE

### Mobile / Presentation Check

Any specific constraints for later MDX or site presentation?

Examples:

- artifact excerpt should remain readable on phone
- no hover-only clue
- one diagram max
- decision options must remain short
- playable choices render as full buttons or equivalent separate action surfaces
- normal reader view hides route/debug metadata

WRITE_MOBILE_PRESENTATION_CHECK_HERE

## Length Budget

### Target Length
```yaml
length_budget:
  measurement: words
  target_min: 500
  target_soft_max: 1100
  target_hard_max: 3000
  exception_allowed: true
  exception_notes: WRITE_EXCEPTION_NOTES_HERE
```

### Length Notes
Why is this scene short, medium, or long?

Examples:
- short because it is a threshold scene with one hard turn
- medium because it introduces contradiction plus one decision point
- long because it carries a major accusation sequence and visible aftershock

WRITE_LENGTH_NOTES_HERE

## Output Target

### Planning Source Path

engine/planning/scene-specs/SCENE_SPEC_FILENAME.md

### Prose Output Target

prose/scenes/SCENE_FILENAME.mdx

### Structural Export Notes

Anything this scene must contribute to route graphs or ending-path rendering?

Examples:

- stable scene_id
- stable edge_ids
- closed sibling options preserved for ending path view
- destination scene titles known in debug mode
- per-edge state_effects exported when the edge changes canonical reader state

WRITE_STRUCTURAL_EXPORT_NOTES_HERE

### Notes for the Prose Generator

Use this section to give the next pass a sharp handoff.

Examples:

- keep the custodian’s language exacting and procedural
- the contradiction should be visible before it is interpreted
- do not explain why the release is impossible
- the scene should end with narrowed options, not a reveal speech

WRITE_NOTES_FOR_PROSE_GENERATOR_HERE

## Completion Checklist

Before treating this scene spec as usable, confirm:

- [ ] scene identity fields are filled
- [ ] beat role is defined
- [ ] scene purpose is concrete
- [ ] entry state is lawful
- [ ] threshold geomancy fields are lawful or disabled
- [ ] required outputs are meaningful
- [ ] forbidden outputs are listed
- [ ] clue/evidence function is specific
- [ ] decision structure is clear if present
- [ ] state delta is specified
- [ ] residue is defined
- [ ] validation checks are usable
- [ ] reader-surface order is specified
- [ ] back action behavior is specified
- [ ] closed option handling is specified if relevant
- [ ] prose target path is plausible
- [ ] nothing here depends on invented canon
