# Arc Brief Template

## Purpose

This file defines one arc as a playable or structurally meaningful route unit within a specific work instance.

An arc brief is not prose.
It is not a lore essay.
It is not a mood board.

It must define:

- what this arc does
- how it differs from other arcs
- what beats it must contain
- what state pressures it applies
- how it can end
- what kinds of scenes and artifacts it requires

Use this file as a planning artifact that later generation passes can rely on.

---

## Instructions for Completion

When filling this template:

- Be concrete.
- Be brief but sufficient.
- Prefer operational language over atmospheric language.
- Do not invent new ontology or claimant law unless explicitly allowed by canon.
- Do not write scene prose here.
- Do not restate the entire project doctrine.
- Keep the arc small enough to fit current scope.
- If a section cannot be completed lawfully from canon, flag it in an ambiguity report rather than guessing.

This file should be easy for:

- a human to skim quickly
- an LLM to parse consistently
- a later compiler pass to turn into scene specs

---

## Arc Identity

- **work_id:** `WORK_ID_HERE`
- **arc_id:** `ARC_ID_HERE`
- **route_type:** `claimant_route | contamination_route | neutral_route | other`
- **claimant:** `CLAIMANT_ID_HERE | none`
- **status:** `planned | ready | blocked | revised`
- **priority:** `first_spike | core | secondary`

---

## Arc Summary

### One-Sentence Function

What does this arc do in the work?

`WRITE_ONE_SENTENCE_HERE`

### Arc Purpose

What is this arc for structurally and dramatically?

Examples:

- establish claimant plausibility
- pressure accusation
- destabilize neutrality
- reframe the reader
- intensify contamination
- produce an accusation ending

`WRITE_PURPOSE_HERE`

### Arc Summary

Give a concise operational summary of the arc.

This should describe:

- what kind of movement the arc has
- what kind of pressure it applies
- what kind of consequence it tends toward

`WRITE_SUMMARY_HERE`

---

## Ontological Role

### Dominant Ontology

What world-logic dominates this arc?

`WRITE_DOMINANT_ONTOLOGY_HERE`

### Claimant Pressure

If claimant-bound, how does this claimant try to make reality cohere?

`WRITE_CLAIMANT_PRESSURE_HERE`

### Truth Style

What counts as truth in this arc?

Examples:

- records
- memory
- diagnosis
- ritual pattern
- witness contradiction

`WRITE_TRUTH_STYLE_HERE`

### Environmental Drift

How does the setting begin to mutate within this arc?

Examples:

- labels proliferate
- rooms feel inhabited by residue
- language becomes diagnostic
- time sequencing weakens

`WRITE_ENVIRONMENTAL_DRIFT_HERE`

### Reader Role Pressure

How is the reader pressured here?

Examples:

- toward judgment
- toward false neutrality
- toward complicity
- toward retraction
- toward premature certainty

`WRITE_READER_ROLE_PRESSURE_HERE`

---

## Arc Entry and Exit

### Entry Conditions

What must already be true for this arc to begin?

Examples:

- reader has entered neutral route
- claimant has been encountered
- artifact family unlocked
- contamination below threshold

```yaml
entry_conditions:
  - CONDITION_1
  - CONDITION_2
```

### Exit Conditions

What counts as lawful completion of this arc?

```yaml
exit_conditions:
  - CONDITION_1
  - CONDITION_2
```

### Premature Termination Conditions

How can this arc end before full realization?

Use only conditions legal under canon.

```yaml
premature_termination_conditions:
  - type: death | disappearance | unresolved_exit | collapse | adjudicated_lock | other
    description: DESCRIPTION_HERE
  - type: death | disappearance | unresolved_exit | collapse | adjudicated_lock | other
    description: DESCRIPTION_HERE
```

### Result of Exit

What does this arc produce when it ends?

Examples:

- accusation opportunity
- ending access
- residue state
- contamination increase
- blocked route
- world scar

WRITE_RESULT_OF_EXIT_HERE

## Beat Grammar

### Required Beats

List the beats this arc must contain.

Use the project’s beat vocabulary.

```yaml
required_beats:
  - invitation
  - plausibility
  - contradiction
  - pressure
  - threshold
  - aftershock
  - residue
```

Edit as needed, but do not remove essential beats without justification.

### Optional Beats

Only include beats that are legal and useful.

```yaml
optional_beats:
  - OPTIONAL_BEAT_1
  - OPTIONAL_BEAT_2
```

### Forbidden Beat Failures

What must this arc not do?

Examples:

- pure atmosphere
- claimant voice blur
- route differences that are only cosmetic
- early lore dump
- pressure without consequence

```yaml
forbidden_beat_failures:
  - FAILURE_1
  - FAILURE_2
```

## Scene Count and Shape

### Scene Count Bounds

```yaml
scene_count:
  min: MIN_SCENES_HERE
  soft_max: SOFT_MAX_HERE
  hard_max: HARD_MAX_HERE
```

### Expected Scene Types

What kinds of scenes are likely needed in this arc?

Examples:

- interview
- room exploration
- artifact encounter
- accusation threshold scene
- residue scene

```yaml
expected_scene_types:
  - SCENE_TYPE_1
  - SCENE_TYPE_2
  - SCENE_TYPE_3
```

### Arc Shape Notes

Any special shape requirements for this arc?

Examples:

- scene 2 must complicate scene 1
- final scene must force a narrowing
- one scene must visibly mutate the annex

WRITE_ARC_SHAPE_NOTES_HERE

## Artifact Intersections

### Required Artifact Families

What artifact families should intersect with this arc?

```yaml
required_artifact_families:
  - ARTIFACT_FAMILY_1
  - ARTIFACT_FAMILY_2
```

### Artifact Jobs

What must the artifacts do in this arc?

Examples:

- support claimant plausibility
- contradict prior evidence
- destabilize timeline
- pressure accusation

```yaml
artifact_jobs:
  - JOB_1
  - JOB_2
```

### Artifact Constraints

What must artifacts in this arc avoid?

```yaml
artifact_constraints:
  - CONSTRAINT_1
  - CONSTRAINT_2
```

## Decision Structure

### Decision Points

What meaningful decisions can occur in this arc?

List decision points at the arc level, not final prose phrasing.

```yaml
decision_points:
  - decision_id: DECISION_ID_1
    summary: DECISION_SUMMARY_HERE
    possible_outcomes:
      - OUTCOME_1
      - OUTCOME_2
  - decision_id: DECISION_ID_2
    summary: DECISION_SUMMARY_HERE
    possible_outcomes:
      - OUTCOME_1
      - OUTCOME_2
```

### Accusation Pressure

How does this arc move the reader toward or away from accusation?

WRITE_ACCUSATION_PRESSURE_HERE

### Retraction Relevance

Is retraction relevant in this arc?
If yes, how?

WRITE_RETRACTION_RELEVANCE_HERE

### Indecision / Contamination Relevance

How does noncommitment behave in this arc?

WRITE_INDECISION_CONTAMINATION_RELEVANCE_HERE

## Threshold Geomancy Usage

### Usage Enabled

true

### Arc Pressure Profile

What kinds of figures or tendencies should dominate this arc?

Examples:

- controlled momentum
- bureaucratic bottleneck
- suspended judgment
- constrained escalation

WRITE_ARC_PRESSURE_PROFILE_HERE

### Figure Assignment Notes

How should threshold figures be used here?

Examples:

- early scenes favor entry / contact / negotiation
- middle scenes favor delay / procedural tension
- ending scene favors closure or lock

WRITE_FIGURE_ASSIGNMENT_NOTES_HERE

### Transition Logic Notes

How should transitions tend to feel in this arc?

Examples:

- narrowing
- administrative closure
- mounting contradiction
- suspended approach
- cold foreclosure

WRITE_TRANSITION_LOGIC_NOTES_HERE

### Termination Bias Notes

If this arc tends toward certain premature endings, note them here.

WRITE_TERMINATION_BIAS_NOTES_HERE

## State Pressures

### Key State Variables Affected

```yaml
state_pressures:
  accusation:
    direction: up | down | conditional
    notes: NOTES_HERE
  contamination:
    direction: up | down | conditional
    notes: NOTES_HERE
  indecision_count:
    direction: up | down | conditional
    notes: NOTES_HERE
  retraction_count:
    direction: up | down | conditional
    notes: NOTES_HERE
  dominant_regime:
    direction: toward_claimant | neutral | unstable | conditional
    notes: NOTES_HERE
  world_scars:
    direction: up | down | conditional
    notes: NOTES_HERE
```

# State Notes

Any special state logic for this arc.

Examples:

- this arc should sharply increase pressure but not finalize accusation
- this arc should punish passive browsing
- this arc should leave residue even if exited early

WRITE_STATE_NOTES_HERE

## Endings and Outcomes

### Allowed Ending Types

Which ending or outcome types may follow from this arc?

```yaml
allowed_outcomes:
  - OUTCOME_1
  - OUTCOME_2
  - OUTCOME_3
```

### Disallowed Ending Types

Which outcomes should not follow directly from this arc?

```yaml
disallowed_outcomes:
  - OUTCOME_1
  - OUTCOME_2
```

### Outcome Notes

Anything important about how this arc resolves.

WRITE_OUTCOME_NOTES_HERE

## Validation Notes

This section exists so later passes can test whether the arc is structurally sound.

### Arc Must Achieve

What must be true if this arc succeeds?

```yaml
arc_must_achieve:
  - REQUIREMENT_1
  - REQUIREMENT_2
  - REQUIREMENT_3
```

### Arc Fails If

What would make this arc structurally weak or invalid?

```yaml
arc_fails_if:
  - FAILURE_1
  - FAILURE_2
  - FAILURE_3
```

### Distinctiveness Check

What specifically makes this arc not interchangeable with the others?

WRITE_DISTINCTIVENESS_CHECK_HERE

### Scope Check

Why is this arc small enough for the current work scope?

WRITE_SCOPE_CHECK_HERE

## Output Targets

List the planning and prose artifacts expected to arise from this arc.

```yaml
output_targets:
  scene_specs:
    - engine/planning/scene-specs/SCENE_SPEC_1.md
    - engine/planning/scene-specs/SCENE_SPEC_2.md
    - engine/planning/scene-specs/SCENE_SPEC_3.md
  artifact_specs:
    - engine/planning/artifact-specs/ARTIFACT_SPEC_1.md
  prose_targets:
    - prose/scenes/SCENE_1.mdx
    - prose/scenes/SCENE_2.mdx
    - prose/scenes/SCENE_3.mdx
    - prose/artifacts/ARTIFACT_1.mdx
    - prose/endings/ENDING_1.mdx
```

## Notes for the Next Pass

Use this section to guide the scene-spec compiler.

Examples:

- scene 1 should establish procedural plausibility
- scene 2 should introduce a contradiction through an artifact
- scene 3 should create a threshold toward accusation
- keep voice restrained and document-heavy
- do not explain the annex cosmology

WRITE_NOTES_FOR_NEXT_PASS_HERE

## Completion Checklist

Before treating this arc brief as usable, confirm:

- [ ] arc identity fields are filled
- [ ] arc purpose is concrete
- [ ] dominant ontology is specific
- [ ] beat grammar is defined
- [ ] scene count bounds are lawful
- [ ] artifact intersections are meaningful
- [ ] decision points are real
- [ ] threshold geomancy usage is lawful or disabled
- [ ] state pressures are specified
- [ ] allowed outcomes are defined
- [ ] validation notes are specific
- [ ] output targets are plausible
- [ ] nothing here depends on invented canon
