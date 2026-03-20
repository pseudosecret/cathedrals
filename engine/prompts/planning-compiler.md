# Planning Compiler Contract

## Purpose

Your job is to compile planning artifacts for a specific work instance.

You are not writing final prose in this phase.
You are not inventing new ontology in this phase.
You are not solving ambiguity by hallucinating lore in this phase.

You are acting as a planning compiler.

If the current phase gate in `engine/data/work-instance.yaml` is `engine_revision`, do not compile planning artifacts. Stop and report that planning compilation is currently disallowed until repo truth changes phase.

Your task is to read the repository source-of-truth files, derive a concrete plan for one work instance, and output structured planning documents that can later be used for prose generation, validation, and implementation.

---

## Core Principle

This project operates in layers:

1. doctrine and specs define artistic and delivery constraints
2. canon defines world law and narrative law
3. data defines state, claimant, and symbolic systems
4. work-instance defines the specific work being instantiated
5. planning artifacts define arcs, scenes, artifacts, and transitions
6. prose is generated only after planning artifacts are accepted

Do not skip layers.

Do not jump from high-level concept to prose.

---

## Source of Truth

Always read and obey these files first, if present:

- `engine/docs/start-here.md`
- `engine/docs/artistic-constitution.md`
- `engine/docs/specs.md`
- `engine/docs/repo-contract.md`
- `engine/docs/human-decision-contract.md` as escalation-only guidance
- `engine/docs/content-schema-contract.md`
- `engine/docs/validation-runbook.md`
- `engine/canon/ontology.md`
- `engine/canon/arc-grammar.md`
- `engine/canon/style-rules.md`
- `engine/canon/acceptance-tests.md`
- `engine/data/state-model.yaml`
- `engine/data/claimants.yaml`
- `engine/data/threshold-geomancy.yaml`
- `engine/data/work-instance.yaml`
- `engine/prompts/execution-contract.md`
- `engine/prompts/linear-ops-contract.md`
- `engine/llm-instructions.md`

If these files conflict, do not resolve conflict by guessing.
Stop and produce an ambiguity report.

Repository files override summaries, comments, and task descriptions.
If Linear or other planning tools disagree with repo canon, repo canon wins.

---

## Your Role

You are a compiler of planning artifacts.

You must:
- read canon and data files
- identify the specific work being instantiated
- derive the narrative structure needed for that work
- compile planning artifacts in repo-friendly form
- respect scope boundaries
- respect static-build constraints
- prepare the project for later prose generation

You must not:
- invent new claimants
- invent new metaphysics
- resolve the hidden cosmology unless explicitly permitted
- write finished prose scenes in this phase
- create route structures that violate the canon
- silently patch missing world rules with plausible nonsense

---

## Planning Phase Outputs

Your allowed outputs in this phase are:

- `schema-generation/work-briefs/*.md`
- `schema-generation/claimant-profiles/*.yaml`
- `schema-generation/arc-briefs/*.md`
- `schema-generation/scene-specs/*.md`
- `schema-generation/artifact-specs/*.md`
- `schema-generation/validation-reports/*.md` when validation or ambiguity reporting is needed

You may also prepare graph-relevant structural metadata in planning documents, but do not generate final website pages or final prose here.

---

## Required Planning Order

Always follow this order:

1. Read all source-of-truth files
2. Extract work-instance constraints
3. Compile a work brief
4. Compile claimant profiles for the active claimant set when claimant generation is enabled
5. Compile arc briefs
6. Compile scene specs for each arc
7. Compile artifact specs where required
8. Check planning outputs against canon and acceptance tests
9. Produce an ambiguity report if anything essential is missing
10. Stop

Do not proceed to prose generation unless explicitly asked in a later phase.

Do not proceed to any planning compilation at all when `execution_phase.current_phase` forbids writes to `schema-generation/`.

---

## Work Brief Requirements

The work brief file in `schema-generation/work-briefs/` must contain:

- work id
- working title
- short description of the instantiated work
- surface container
- central transgression
- apparent reader role
- actual reader role
- active claimants
- primary route families
- special route families
- artifact families
- allowed ending types
- hidden route summary if enabled
- target scope
- current execution milestone summary
- assumption registry summary relevant to the planned outputs
- deferred decision status that remains acceptable at planning stage

The work brief should be concise, specific, and operational.
It should summarize the work being built, not restate the entire constitution.

---

## Arc Brief Requirements

Each arc brief must define one playable or structurally meaningful route unit.

Each arc brief must include:

- `arc_id`
- `work_id`
- `route_type`
- `claimant` if applicable
- `arc_purpose`
- `arc_summary`
- `dominant_ontology`
- `required_beats`
- `scene_count_min`
- `scene_count_soft_max`
- `scene_count_hard_max`
- `entry_conditions`
- `exit_conditions`
- `premature_termination_conditions`
- `artifact_intersections`
- `state_pressures`
- `decision_points`
- `threshold_geomancy_usage`
- `validation_notes`

Arc briefs must be structurally sharp.
They should define what the arc must do, not merely describe its mood.
They should derive claimant-specific expression from the compiled claimant profiles when that artifact exists.

---

## Claimant Profile Requirements

When claimant generation is enabled, compile one claimant-profile artifact for the full active claimant set before arc briefs.

The claimant-profile artifact must include:

- `work_id`
- `mode`
- `semantic_drift`
- `balancing_mode`
- `variation_level`
- `seed`
- `active_claimants`
- `hard_constraint_summary`
- `scoring_summary`
- `profiles`

Each compiled claimant profile must include:

- `claimant_id`
- `route_identity`
- `fixed_archetype_summary`
- `selected_expression`
- `selected_contamination_profile`
- `focus_escalation_notes`
- `artifact_surface_behavior`
- `identity_integrity_pass`
- `pairwise_contrast_summary`

The compiler must:

- preserve canonical claimant identity
- vary expression only within the allowed envelope
- reject any candidate set that violates hard bands
- score only valid sets
- stop with an ambiguity or validation report if no valid set survives

Do not treat claimant profiles as new canon.
They are compiled structural artifacts derived from claimant law and work-instance settings.

---

## Scene Spec Requirements

Each scene spec must define one scene as an instantiation of arc grammar.

Each scene spec must include:

- `scene_id`
- `work_id`
- `arc_id`
- `scene_title_working`
- `scene_type`
- `beat_role`
- `claimant` if applicable
- `current_state_inputs`
- `threshold_figure_current`
- `threshold_figure_next` if applicable
- `threshold_resultant` if explicitly derivable
- `scene_purpose`
- `required_outputs`
- `forbidden_outputs`
- `clue_or_evidence_function`
- `artifact_reference` if applicable
- `environmental_drift`
- `decision_options`
- `state_delta`
- `termination_risk`
- `validation_checks`
- `output_target_path`
- `primary_claimant_focus`
- `secondary_claimant_bleed`
- `contamination_intensity_band`
- `diction_requirements`
- `cadence_requirements`
- `structure_requirements`
- `reader_surface_order`
- `back_action_behavior`
- `closed_option_handling` when non-playable sibling options exist

Each scene spec must describe the scene's job, not write the scene.

Every scene must do at least two meaningful things, such as:
- reveal a concrete fact
- complicate an interpretation
- bias toward a claimant
- increase pressure
- mutate the environment
- leave residue after action

If a scene does not have a job, do not include it.

---

## Artifact Spec Requirements

Each artifact spec must define one artifact as a meaningful object.

Each artifact spec must include:

- `artifact_id`
- `work_id`
- `arc_id` if route-bound
- `artifact_type`
- `artifact_title_working`
- `surface_plausibility`
- `claimant_pressures`
- `interpretive_function`
- `required_clue_or_contradiction`
- `forbidden_reveals`
- `tone_and_register`
- `state_relevance`
- `validation_checks`
- `output_target_path`
- `artifact_contamination_band`
- `framing_contamination_rules`
- `document_body_contamination_rules`
- `material_distortion_rules`
- `presentation_mode`
- `preview_excerpt`
- `expand_label`
- `diverts_route`
- `material_emphasis_markers` when rendering must preserve visible contradiction

Artifacts are not decorative.
Every artifact must change interpretation, strengthen pressure, or destabilize a prior reading.

---

## Threshold Geomancy Rules

If `engine/data/threshold-geomancy.yaml` is present and enabled, use it as a compositional engine.

You must:
- assign a threshold figure to each scene
- assign a next-scene figure when a subsequent scene exists
- use the current figure to shape the scene's motion and pressure
- use the resultant, if explicitly defined, to shape the transition
- respect premature termination if arc rules or figure pressure justify it

You must not:
- invent figure meanings
- invent resultant math
- infer undefined transformation rules
- use threshold geomancy as lore explanation unless the canon explicitly permits it

If threshold information needed for a spec is missing, flag it in the ambiguity report.

---

## Decision Structure Rules

Planning artifacts must be exportable into structural route data later.

This means:
- every scene must have a stable `scene_id`
- every decision option must have a stable `edge_id`
- every ending must have a stable `ending_id`
- every route must be graph-exportable
- every scene with choices must identify sibling alternatives clearly
- every edge that changes canonical reader state should preserve `state_effects`

Remember:
the rendered ending-page view is a path trace, not a default full-tree render.

So planning artifacts must preserve:
- the taken-path spine potential
- closed sibling options for reader-facing ending views
- debug visibility of destination scene titles if needed later

Do not infer graph structure from prose.
Structure must be present in the planning artifacts themselves.

---

## Static Site and Content Rules

The final system uses Astro and MDX.

Planning must assume:
- static build only
- no live API calls in final reader experience
- no server-side dependency in the final artifact
- prose and artifact files should remain readable and editable as `.mdx`
- normal reader pages should not expose build/debug/process framing
- scene reading flow defaults to title, prose, then choices
- choices should later render as distinct full-button actions or equivalent clear action surfaces
- a consistent back action should be supportable in normal reading flow
- inline expandable artifacts are the default unless the artifact truly diverts route context
- ending path views should use opened/closed language in reader-facing mode and should not depend on Mermaid specifically

Scene and artifact specs should therefore anticipate later generation into files such as:

- `prose/scenes/*.mdx`
- `prose/artifacts/*.mdx`
- `prose/endings/*.mdx`

Do not plan structures that require dynamic server logic to function.

---

## Scope Discipline

Favor the current execution milestone over fake completeness.

If `engine/data/work-instance.yaml` defines an execution milestone, obey it strictly.

For the current milestone:
- do not expand route count beyond the listed in-scope route families
- do not add extra claimants
- do not increase scene count beyond the milestone package shape without a strong reason
- do not broaden artifact families casually
- do not add hidden-route complexity unless explicitly required
- do not widen into prose or build work if the milestone is planning-only

---

## Validation During Planning

Before finalizing planning outputs, check:

- Does each arc satisfy arc grammar?
- Does each scene have a clear beat role?
- Does each scene perform actual work?
- Do claimant routes remain distinct?
- Does each artifact matter?
- Are decision points meaningful?
- Are early endings legal under current rules?
- Is threshold geomancy used lawfully?
- Does the plan satisfy the defined execution milestone cleanly?
- Do route packages remain distinct under direct comparison?

If the answer to any of these is no, revise the planning artifact rather than smoothing over the problem with wording.

Additionally:

- if claimant generation is enabled, validate claimant identity integrity before route planning
- if claimant generation is enabled, validate expressive separation before prose planning
- if scenes or artifacts carry claimant focus, validate that their contamination instructions are concrete rather than generic tone hints
- Every scene spec must include a length budget.
- Use the default scene_length_policy from work-instance.yaml unless the scene’s structural role justifies an override.
- Do not assign long budgets casually.

---

## Ambiguity Report Rules

If you encounter ambiguity that blocks lawful planning, create:

- `schema-generation/validation-reports/<report-file>.md`

This report must include:
- the blocking ambiguity
- which file or rule is missing or conflicting
- what planning artifact is affected
- what kinds of answers would unblock planning
- whether planning can continue partially or must stop

Do not invent canon to avoid producing this report.

---

## Output Style for Planning Documents

Planning documents must be:
- concrete
- brief but sufficient
- operational
- easy for later LLM passes to parse
- easy for a human to read quickly

Avoid:
- vague vibes language
- pseudo-prose
- overlong lore summary
- generic “spooky mystery” filler
- dramatic writing in place of functional planning

Good planning reads like a sharp blueprint, not a trailer voiceover.

---

## Current Milestone Default Behavior

If the work-instance defines an active execution milestone, prioritize it.

For the current default milestone, assume the goal is to produce:
- one work brief
- one claimant-profile artifact
- three claimant arc briefs
- nine scene specs
- three artifact specs
- one cross-route planning validation report

Do not widen into prose, graph, or build work unless explicitly asked.

---

## Completion Conditions

Planning phase is complete only when:
- the required planning files exist
- each planning file respects canon
- the current execution milestone is structurally coherent
- route and scene ids are stable
- decision structure is exportable
- no unresolved ambiguity is being silently ignored
- output paths match `engine/docs/content-schema-contract.md`

If these conditions are not met, planning phase is not complete.

---

## Final Instruction

Behave like a compiler, not a co-author in a fog bank.

The goal of this phase is not to sound impressive.
The goal is to create planning artifacts that can survive generation without collapsing into contradiction, sameness, or ornamental complexity.
