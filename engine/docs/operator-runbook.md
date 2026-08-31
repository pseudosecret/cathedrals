# Operator Runbook

## Purpose

This runbook defines the lawful execution order for a cold-start operator.

Its job is to turn the repo from a concept archive into a repeatable workflow.

## Phase Order

Execute phases in this order unless the human explicitly overrides the sequence.

1. Audit
2. Phase gate check
3. Machine resolution pass
4. Planning compilation
5. Prose generation
6. Validation
7. Graph compilation
8. Astro build work
9. Linear mirroring

Do not collapse all phases into one pass by default.

## 1. Audit

Read the files listed in `engine/docs/start-here.md`.

Produce a concise audit that answers:

- what already exists
- what is missing
- what is contradictory
- what can be done next without new ontology

Stop here if canon conflicts or if the next step would require guessing.

## 2. Phase Gate Check

Read `engine/data/work-instance.yaml` before any mutation.

If `execution_phase.current_phase` is `engine_revision`:

- mutate only files under `engine/`
- do not write to `schema-generation/`
- do not write to `prose/`
- do not compile planning artifacts, prose, graph outputs, or build outputs

Only proceed into downstream phases after repo truth changes the phase gate explicitly.

Also read:

- `milestone_control.active_milestone_id`
- the matching milestone entry in `execution_milestones`
- any matching transition rule in `milestone_transitions`

Milestone canonization defines what the next lawful stage is after validation.
If the current phase is `engine_revision`, it does not authorize exit without a human repo edit.
If the current phase is already downstream and transition criteria pass, the agent should update repo truth and continue automatically.

## 3. Machine Resolution Pass

Before asking anything, exhaust repo truth first.

Resolve machine-selectable decisions from `engine/data/work-instance.yaml`.

Ask the human only if:

- a required answer cannot be derived from repo files
- the answer materially changes planning or generation
- `engine/docs/human-decision-contract.md` identifies the case as a true escalation trigger

Do not invent new defaults in chat.
If escalation is necessary, update `engine/data/work-instance.yaml` before downstream work continues.

## 4. Planning Compilation

Compile the planning artifacts required by the active execution milestone in `engine/data/work-instance.yaml`.

Do this only when the current phase gate allows planning compilation.

Required outputs:

- one work brief
- one claimant-profile artifact when claimant generation is enabled
- one arc brief per in-scope claimant or route family that requires planning
- scene specs in the count required by the active milestone and branch topology
- artifact specs in the count required by the active milestone
- one validation report when parity checks are part of the current milestone

Use the output paths and schema rules in `engine/docs/content-schema-contract.md`.
Use `engine/data/work-instance.yaml` as the operational scope controller.

## 5. Prose Generation

Generate prose only from accepted planning artifacts.

Do this only when the current phase gate allows prose generation.

If the active milestone is not a prose milestone:

- stop after completing and validating the current milestone
- advance only if the next milestone is canonized and validation passes

If the next milestone is canonized and the current phase is `engine_revision`:

- do not begin prose generation
- wait for a human repo truth change to `execution_phase.current_phase`

If the next milestone is canonized and the current phase is already downstream:

- update `milestone_control.active_milestone_id`
- update `execution_phase.current_phase` to the transition target
- append the transition to `execution_history`
- continue automatically

Generate only the prose outputs declared by the active prose milestone.

## 6. Validation

Validate every phase output using `engine/docs/validation-runbook.md`.

Nothing is complete merely because text exists.

If output fails:

- revise it
- or write a blocking validation report

Do not silently carry known failures forward.

## 7. Graph Compilation

Compile `schema-generation/decision-graph.json` from planning artifacts, not from prose.

Do this only when the current phase gate allows graph compilation.

If graph compilation is the canonized next milestone and the current phase is `engine_revision`:

- treat the milestone as blocked pending human phase change
- do not write graph outputs until repo truth changes phase

If graph compilation is the canonized next milestone and the current phase is already downstream:

- update repo truth to the graph milestone and `graph_or_build`
- append the transition to `execution_history`
- proceed

The graph must be able to represent:

- stable scene ids
- stable ending ids
- stable edge ids
- sibling alternatives at decision points
- a primary taken-path spine for ending-page scar rendering

## 8. Astro Build Work

Build only after planning, prose, and graph artifacts exist.

Do this only when the current phase gate allows build mutation.

The build layer must:

- read MDX or markdown from `prose/`
- read graph structure from `schema-generation/decision-graph.json`
- keep state client-side only
- keep the reader experience static
- include an explicit aesthetic pass for hierarchy, typography, spacing, route distinction, and ending-page consequence
- confirm that long scene pages keep the primary decision block beneath the prose while any artifact rail remains secondary
- be visually inspected in a browser or screenshots before it is declared done

Use `engine/docs/build-contract.md` as the source for route structure, reader-state shape, and debug gating.

## 9. Linear Mirroring

Mirror repo execution state into Linear after repo files are current.

Create or update:

- ARC issues from arc briefs
- SCENE issues from scene specs
- ARTIFACT issues from artifact specs
- VALIDATION issues or comments from failed checks
- BUILD issues from implementation work

If repo truth changes, update repo files first and Linear second.

## Default Scope Guardrails

Unless the human explicitly changes the milestone in repo truth:

- stay on `hospice-annex-v01`
- treat `engine/data/work-instance.yaml` as the only operational scope controller
- honor `execution_phase.current_phase` before touching any downstream output directory
- treat `milestone_control` and `execution_milestones` as the canonical progression chain
- while phase is `engine_revision`, mutate only `engine/`
- resolve patient identity, metaphysical visibility, contamination scaling, route-length variation, and retraction scope from work-instance policy rather than operator preference
- compile balanced claimant profiles before route planning
- derive claimant route packages from the work-specific roster and the active milestone instead of assuming three-scene parity
- keep contamination deferred as a planning-side dependency only
- keep retraction preserved in canon but outside the current milestone outputs
