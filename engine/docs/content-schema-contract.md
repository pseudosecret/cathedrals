# Content Schema Contract

## Purpose

This document defines canonical file naming and minimum schema expectations for compiled planning artifacts, generated prose, and the structural decision graph.

Use this alongside the templates in `engine/planning/`.

## General Rules

- compiled planning files live under `schema-generation/`
- generated prose files live under `prose/`
- all ids are stable, lowercase, and underscore-delimited
- file names are lowercase and kebab-cased
- generated content must remain readable and editable
- these output paths are downstream-only and must not be mutated during `engine_revision`

## Planning Artifacts

### Work Brief

Path:

- `schema-generation/work-briefs/<work-id>-work-brief.md`

Required contents:

- work id
- title
- short description
- active claimants
- route families
- artifact families
- allowed endings
- current execution milestone summary
- assumption registry summary relevant to the planned outputs
- deferred decision status that remains acceptable

Source shape:

- use the work-brief requirements in `engine/prompts/planning-compiler.md`

### Arc Brief

Path:

- `schema-generation/arc-briefs/<arc-file>.md`

Required contents:

- arc id
- work id
- route type
- claimant if applicable
- required beats
- scene limits
- entry and exit conditions
- premature termination conditions
- state pressures
- decision points
- validation notes

Source shape:

- use `engine/planning/arc-brief-template.md`

### Claimant Profile Artifact

Path:

- `schema-generation/claimant-profiles/<work-id>-claimant-profiles.yaml`

Required contents:

- work id
- generation mode
- semantic drift mode
- balancing mode
- seed
- active claimant ids
- hard constraint summary
- scoring summary
- per-claimant selected expressive profile
- per-claimant selected contamination profile
- per-claimant focus escalation notes
- pairwise contrast summary

Per-claimant required contents:

- claimant id
- fixed archetype summary
- selected expressive fields
- selected contamination fields
- artifact surface behavior
- identity-integrity pass summary
- expressive-separation notes against the other active claimants

Source shape:

- use `engine/planning/claimant-profile-template.md`

### Scene Spec

Path:

- `schema-generation/scene-specs/<scene-file>.md`

Required contents:

- scene id
- work id
- arc id
- beat role
- scene type
- claimant if applicable
- current state inputs
- threshold current and next
- threshold resultant if defined
- required outputs
- forbidden outputs
- decision options with stable edge ids if choices exist
- state delta
- validation checks
- output target path
- length budget
- primary claimant focus
- secondary claimant bleed
- contamination intensity band
- diction requirements
- cadence requirements
- structure requirements

Reader-surface additions for new or regenerated scene specs:

- reader surface order
- back action behavior
- closed option handling

Source shape:

- use `engine/planning/scene-spec-template.md`

### Artifact Spec

Path:

- `schema-generation/artifact-specs/<artifact-file>.md`

Required contents:

- artifact id
- work id
- arc id or scene id if applicable
- artifact type
- claimant relevance
- interpretive function
- required clue or contradiction
- validation checks
- output target path
- artifact contamination band
- framing contamination rules
- document body contamination rules
- material distortion rules

Reader-surface additions for new or regenerated artifact specs:

- presentation mode with `inline_expandable` as the default when the artifact does not divert route context
- preview excerpt
- expand label
- diverts route boolean
- material emphasis markers when important corrections or contradictions must be surfaced in rendering

Source shape:

- use `engine/planning/artifact-spec-template.md`

### Validation or Ambiguity Report

Path:

- `schema-generation/validation-reports/<report-file>.md`

Required contents:

- target artifact or target phase
- checks performed
- pass or fail status
- concrete failures or blocking ambiguity
- required remediation or human decision if blocked
- milestone scope confirmation when the report is used to accept a planning milestone

## Generated Prose

### Scene MDX Frontmatter

Path:

- `prose/scenes/<scene-file>.mdx`

Required frontmatter:

```yaml
---
id: custodian_scene_01
work_id: hospice-annex-v01
arc_id: custodian_route
claimant: custodian
beat_role: invitation
scene_type: exploration
state_inputs:
  accused_claimant: null
  dominant_regime: neutral
  contamination: 0
threshold_current: 1-1-2-3
threshold_next: 1-1-3-2
threshold_resultant: 1-1-1-2
artifact_ids:
  - intake_discrepancy_01
status: draft
---
```

The exact threshold figures may vary by accepted planning outputs.
The field names must remain stable.

### Artifact MDX Frontmatter

Path:

- `prose/artifacts/<artifact-file>.mdx`

Required frontmatter:

```yaml
---
id: intake_discrepancy_01
work_id: hospice-annex-v01
arc_id: custodian_route
artifact_type: intake_document
claimant_relevance:
  - custodian
status: draft
---
```

### Ending MDX Frontmatter

Path:

- `prose/endings/<ending-file>.mdx`

Required frontmatter:

```yaml
---
id: accusation_custodian_01
work_id: hospice-annex-v01
arc_id: custodian_route
ending_type: accusation
accused_claimant: custodian
dominant_regime: custodian
decision_scar_enabled: true
status: draft
---
```

## Decision Graph

Path:

- `schema-generation/decision-graph.json`

This file is a compiled structural artifact derived from accepted planning outputs.
Do not treat it as hand-authored canon.

Required top-level shape:

```json
{
  "version": "0.1",
  "work_id": "hospice-annex-v01",
  "generated_from": {
    "work_brief": "schema-generation/work-briefs/hospice-annex-v01-work-brief.md",
    "arc_briefs": ["schema-generation/arc-briefs/custodian-arc-01.md"],
    "scene_specs": [
      "schema-generation/scene-specs/custodian-scene-01.md",
      "schema-generation/scene-specs/custodian-scene-02.md",
      "schema-generation/scene-specs/custodian-scene-03.md"
    ]
  },
  "nodes": [],
  "edges": [],
  "path_trace_defaults": {
    "mode": "normal",
    "debug_mode_available": true
  }
}
```

Required node fields:

- `id`
- `type` as `scene` or `ending`
- `title`
- `route_context`
- `output_path`
- `status`

Required edge fields:

- `id`
- `from`
- `to`
- `label`
- `kind` as `progression`, `decision`, or `ending`
- `availability` as `playable` or `reserved`
- `sibling_group` when the edge is part of a decision set

Optional but preferred edge fields when state changes are canonical:

- `state_effects`

Examples of `state_effects` include:

- `set_accused_claimant_custodian`
- `set_dominant_regime_custodian`
- `increase_indecision_count`
- `add_world_scar`

## Stability Rule

Do not rename ids, file paths, or frontmatter keys casually.
Refactors are allowed only when all dependent repo files are updated in the same change.

New planning fields should prefer extending planning artifacts and graph exports before introducing new prose frontmatter keys.
