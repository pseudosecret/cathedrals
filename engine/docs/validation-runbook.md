# Validation Runbook

## Purpose

This runbook defines what "done" means at each phase and which failures require revision or human review.

## Global Rule

Output is not accepted because it exists.
Output is accepted only when it satisfies canon, scope, and phase-specific requirements.

## Phase Gate Validation

Pass if:

- the operator checked `execution_phase.current_phase` before mutating downstream output directories
- engine-revision passes mutated only files under `engine/`

Fail if:

- `schema-generation/` was written during `engine_revision`
- `prose/` was written during `engine_revision`
- graph or build outputs were produced during `engine_revision`
- the operator relied on milestone scope while ignoring the phase write gate

## 1. Audit Validation

Pass if:

- the operator identified the source-of-truth files
- current contradictions were named concretely
- the next smallest lawful task was identified

Fail if:

- the audit relies on chat memory over repo files
- path drift is ignored
- missing canon is hand-waved away

## 2. Planning Validation

Pass if:

- `engine/data/work-instance.yaml` contains machine-resolution policy, decision status, and assumption registry sections sufficient for current scope
- `engine/data/work-instance.yaml` contains explicit branching architecture policy for introduction, opening hub, decision cardinality, hesitation, reconvergence, and navigation semantics
- the claimant-profile artifact exists when claimant generation is enabled
- the active claimant set passes identity-integrity and expressive-separation checks
- each compiled claimant profile includes a selected contamination profile and focus-escalation notes
- the execution-milestone deliverables defined in `engine/data/work-instance.yaml` exist in `schema-generation/`
- each artifact follows the schema contract
- scene and edge ids are stable
- the introduction sequence is explicitly planned before the first hub
- the opening hub is explicitly planned with exactly three live options
- every meaningful decision declares 2 to 5 live options
- every major decision declares a hesitation or reconsideration surface
- reconvergence behavior is explicit wherever branches merge
- each claimant route package satisfies the shared beat scaffold without collapsing into shallow parallel spines
- claimant-focused scene specs declare contamination band plus diction, cadence, and structure requirements
- artifact specs declare framing and document-body contamination rules separately
- cross-route comparison confirms route differences are not merely cosmetic
- route artifacts pressure interpretation differently from one another
- no scene exists without clear structural work

Fail if:

- machine-resolvable project decisions live only in chat or tracker state instead of `engine/data/work-instance.yaml`
- claimant profiles violate archetype law or collapse into interchangeable voices
- claimant balancing silently relaxes hard constraints to get a result
- planning output goes to the wrong directory
- scene specs are mood summaries instead of blueprints
- contamination instructions are generic enough to fit any claimant unchanged
- route packages flatten into cosmetic rewrites of one another
- the opening sequence is inert or reads like setup notes instead of dramatic entry
- any decision scene offers only one live option
- hesitation is missing from an irreversible commitment point
- reconvergence is used to erase path consequence
- unresolved ambiguity is silently patched by invention

Planning milestone advancement is allowed only if:

- `milestone_control.active_milestone_id` names a planning milestone, currently `branching_planning_02`
- the active planning milestone's declared validation report exists
- that report contains `result: pass`
- all planning deliverables declared for the active planning milestone exist
- no active stop condition from `planning_expectations.stop_conditions` is triggered

## 3. Prose Validation

Pass if each generated scene or artifact:

- satisfies its planning spec
- performs the required beat work
- preserves reader-perspective introduction requirements where applicable
- uses concrete memorable detail
- respects claimant voice and ontology
- respects the compiled claimant profile for the current work instance
- respects the declared contamination intensity band for its focus level
- stays within length policy unless justified
- changes pressure, interpretation, or consequence
- gives major decisions a readable hesitation surface when required

Fail if:

- prose is atmospheric but inert
- the introduction drifts into static setup instead of eventful entry
- a supposed choice is really a lone continuation button
- hesitation text exists but does not change pressure or outcome
- claimant voices blur together
- expressive drift changes claimant identity instead of expression
- claimant-focused prose stays structurally neutral despite declared contamination pressure
- heavy contamination destroys readability or dramatic clarity
- artifacts feel decorative
- artifact framing and document body collapse into the same contamination behavior when the object needs separation
- hidden cosmology is explained directly without permission

Prose milestone advancement is allowed only if:

- `milestone_control.active_milestone_id` names a prose milestone, currently `branching_prose_02`
- the active prose milestone's declared validation report exists
- that report contains `result: pass`
- all prose deliverables declared for the active prose milestone exist
- no active stop condition from `planning_expectations.stop_conditions` is triggered

## 4. Graph Validation

Pass if:

- `decision-graph.json` is derived from planning outputs
- every node id is stable and resolvable
- every edge id is stable
- sibling groups are explicit at decision points
- the opening hub exposes exactly three live edges
- every playable decision set exposes between 2 and 5 live edges
- reserved edges are clearly marked
- reconvergent nodes preserve multiple inbound edges explicitly
- redirective endings declare their new-beginning targets explicitly
- the taken-path spine can be reconstructed from client state

Fail if:

- graph structure is inferred from prose alone
- any edge or node dangles
- any decision group has fewer than two live options
- the opening hub cardinality is not exactly three
- reconvergence exists only as undocumented coincidence
- sibling alternatives cannot be reconstructed for the scar view

Graph milestone advancement is allowed only if:

- `milestone_control.active_milestone_id` names a graph milestone, currently `branching_graph_02`
- the active graph milestone's declared validation report exists
- that report contains `result: pass`
- all graph deliverables declared for the active graph milestone exist
- no active stop condition from `planning_expectations.stop_conditions` is triggered

## 5. Build Validation

Pass if:

- routes load content from `prose/`
- ending scar data comes from the graph plus client state
- no server dependency is required
- mobile readability is preserved
- light and dark mode both work
- the first top-level reset control is labeled `start_over` when it resets state
- major decisions expose hesitation/reconsideration behavior when graph/state rules require it

Fail if:

- important story truth is hardcoded only in `src/`
- build logic requires live APIs
- the experience depends on hover or desktop-only affordances
- the UI implies page-history back navigation when it only performs reset

Build milestone completion is allowed only if:

- `milestone_control.active_milestone_id` names a build milestone, currently `branching_build_02`
- the active build milestone's declared validation report exists
- that report contains `result: pass`
- all build deliverables declared for the active build milestone exist
- no active stop condition from `planning_expectations.stop_conditions` is triggered

## 6. Tracking Validation

Pass if:

- Linear items are derived from repo files
- issue descriptions point back to repo paths
- statuses reflect actual repo state

Fail if:

- Linear contains unique canon not present in repo
- issues are updated before repo truth
- completion is claimed without validation

## Human Review Triggers

Require human review if:

- canon files conflict
- no valid claimant-profile set satisfies both hard constraints and expressive separation
- a route loses ontological distinction
- a threshold rule is missing but necessary
- the execution milestone is no longer sufficient
- a requested downstream write conflicts with the current phase gate
- validation failures repeat for structural reasons rather than local wording

## Validation Report Format

Every validation report used as a promotion oracle must contain an explicit status block near the top with these exact fields:

- `result: pass` or `result: fail`
- `blocking_ambiguity: none` or a concrete blocking label
- `stop_conditions_triggered: []` or an explicit list of triggered stop conditions

Downstream auto-advance is allowed only when the report contains `result: pass` and `stop_conditions_triggered: []`.
