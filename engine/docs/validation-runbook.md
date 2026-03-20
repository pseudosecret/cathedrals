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
- the claimant-profile artifact exists when claimant generation is enabled
- the active claimant set passes identity-integrity and expressive-separation checks
- each compiled claimant profile includes a selected contamination profile and focus-escalation notes
- the execution-milestone deliverables defined in `engine/data/work-instance.yaml` exist in `schema-generation/`
- each artifact follows the schema contract
- scene and edge ids are stable
- each claimant route package satisfies the shared three-beat planning scaffold
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
- unresolved ambiguity is silently patched by invention

Planning milestone advancement is allowed only if:

- `milestone_control.active_milestone_id` is `planning_parity_01`
- `schema-generation/validation-reports/hospice-annex-v01-planning-parity-01.md` exists
- that report passes
- all planning deliverables declared for `planning_parity_01` exist

## 3. Prose Validation

Pass if each generated scene or artifact:

- satisfies its planning spec
- performs the required beat work
- uses concrete memorable detail
- respects claimant voice and ontology
- respects the compiled claimant profile for the current work instance
- respects the declared contamination intensity band for its focus level
- stays within length policy unless justified
- changes pressure, interpretation, or consequence

Fail if:

- prose is atmospheric but inert
- claimant voices blur together
- expressive drift changes claimant identity instead of expression
- claimant-focused prose stays structurally neutral despite declared contamination pressure
- heavy contamination destroys readability or dramatic clarity
- artifacts feel decorative
- artifact framing and document body collapse into the same contamination behavior when the object needs separation
- hidden cosmology is explained directly without permission

Prose milestone advancement is allowed only if:

- `milestone_control.active_milestone_id` is `prose_generation_01`
- `schema-generation/validation-reports/hospice-annex-v01-prose-generation-01.md` exists
- that report passes
- all prose deliverables declared for `prose_generation_01` exist

## 4. Graph Validation

Pass if:

- `decision-graph.json` is derived from planning outputs
- every node id is stable and resolvable
- every edge id is stable
- sibling groups are explicit at decision points
- reserved edges are clearly marked
- the taken-path spine can be reconstructed from client state

Fail if:

- graph structure is inferred from prose alone
- any edge or node dangles
- sibling alternatives cannot be reconstructed for the scar view

Graph milestone advancement is allowed only if:

- `milestone_control.active_milestone_id` is `graph_compilation_01`
- `schema-generation/validation-reports/hospice-annex-v01-graph-compilation-01.md` exists
- that report passes
- all graph deliverables declared for `graph_compilation_01` exist

## 5. Build Validation

Pass if:

- routes load content from `prose/`
- ending scar data comes from the graph plus client state
- no server dependency is required
- mobile readability is preserved
- light and dark mode both work

Fail if:

- important story truth is hardcoded only in `src/`
- build logic requires live APIs
- the experience depends on hover or desktop-only affordances

Build milestone completion is allowed only if:

- `milestone_control.active_milestone_id` is `build_release_01`
- `schema-generation/validation-reports/hospice-annex-v01-build-release-01.md` exists
- that report passes
- all build deliverables declared for `build_release_01` exist

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
- milestone auto-advance semantics appear to bypass phase gating
