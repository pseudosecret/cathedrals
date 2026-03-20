FILE FOR ARCHIVAL PURPOSES ONLY

# First Spike Freeze

Current operational scope is controlled by `engine/data/work-instance.yaml`.

## Purpose

This document freezes the first executable slice so operators do not improvise IDs, filenames, or scope.

It is the contract for the custodian-route vertical slice of `hospice-annex-v01`.

## Scope

The first spike includes:

- one work brief
- one compiled claimant-profile artifact
- one custodian arc brief
- three custodian scene specs
- one artifact spec
- three custodian scenes
- one generated artifact
- one custodian accusation ending
- one compiled decision graph

It does not include:

- mourner-route execution
- examiner-route execution
- contamination-route execution
- playable retraction
- a full multi-route Astro reader

## Stable IDs

Use these IDs exactly unless the human explicitly approves a refactor.

### Work

- `work_id`: `hospice-annex-v01`

### Arc

- `arc_id`: `custodian_route`
- `arc_file`: `custodian-arc-01.md`

### Scenes

- `scene_id`: `custodian_scene_01`
  `scene_file`: `custodian-scene-01.md`
  `beat_role`: `invitation`
- `scene_id`: `custodian_scene_02`
  `scene_file`: `custodian-scene-02.md`
  `beat_role`: `contradiction`
- `scene_id`: `custodian_scene_03`
  `scene_file`: `custodian-scene-03.md`
  `beat_role`: `threshold`

### Artifact

- `artifact_id`: `intake_discrepancy_01`
- `artifact_file`: `intake-discrepancy-01.md`
- `artifact_type`: `intake_document`

### Ending

- `ending_id`: `accusation_custodian_01`
- `ending_file`: `custodian-ending-01.mdx`

### Edge IDs

- `edge_custodian_scene_01_to_scene_02`
- `edge_custodian_scene_02_to_scene_03`
- `edge_custodian_scene_03_to_accusation_custodian_01`
- `edge_custodian_scene_03_withhold_judgment_reserved`

The reserved edge exists so the graph and decision-scar model have a lawful sibling alternative without forcing first-spike prose for a second ending.

## Frozen Output Paths

Planning:

- `schema-generation/work-briefs/hospice-annex-v01-work-brief.md`
- `schema-generation/claimant-profiles/hospice-annex-v01-claimant-profiles.yaml`
- `schema-generation/arc-briefs/custodian-arc-01.md`
- `schema-generation/scene-specs/custodian-scene-01.md`
- `schema-generation/scene-specs/custodian-scene-02.md`
- `schema-generation/scene-specs/custodian-scene-03.md`
- `schema-generation/artifact-specs/intake-discrepancy-01.md`

Generated prose:

- `prose/scenes/custodian-scene-01.mdx`
- `prose/scenes/custodian-scene-02.mdx`
- `prose/scenes/custodian-scene-03.mdx`
- `prose/artifacts/intake-discrepancy-01.mdx`
- `prose/endings/custodian-ending-01.mdx`

Graph:

- `schema-generation/decision-graph.json`

## Frozen Behavioral Defaults

- center the first spike on the custodian truth style: records, signatures, room assignments, procedural coherence
- compile claimant profiles for all active claimants before route planning begins
- keep the released resident concrete but unnamed
- let metaphysical drift appear through contradiction and mutation, not explanation
- keep contamination as background pressure only
- keep retraction out of the playable first spike
- end the spike with a custodian accusation outcome

## Minimum Graph Shape

The first spike graph must include:

- three scene nodes
- one ending node
- one reserved sibling option at the final decision point
- stable labels for all edges
- enough metadata to derive a taken-path spine and rejected sibling options

## Acceptance Condition

The first spike is frozen successfully only if later agents can generate planning, prose, graph, and build work from this document without needing new naming decisions.
