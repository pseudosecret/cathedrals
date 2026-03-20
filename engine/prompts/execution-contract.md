# Execution Contract

## 1. Source of Truth

The source of truth is:

- engine/docs/artistic-constitution.md
- engine/docs/specs.md
- engine/docs/repo-contract.md
- engine/docs/human-decision-contract.md if present, as escalation-only guidance
- engine/docs/content-schema-contract.md if present
- engine/docs/build-contract.md if present
- engine/docs/validation-runbook.md if present
- engine/canon/ontology.md
- engine/canon/arc-grammar.md
- engine/canon/style-rules.md
- engine/canon/acceptance-tests.md
- engine/data/state-model.yaml
- engine/data/claimants.yaml
- engine/data/threshold-geomancy.yaml if present
- engine/data/work-instance.yaml if present

## 2. Allowed Actions

The agent may:

- mutate `engine/` files that revise canon, data, prompts, docs, and templates
- compile claimant-profile artifacts when the phase gate allows it
- generate scene specs when the phase gate allows it
- generate scene prose when the phase gate allows it
- generate artifacts when the phase gate allows it
- compile decision-graph.json from planning outputs when the phase gate allows it
- generate page variants or static site components when the phase gate allows it
- generate validation reports

## 3. Forbidden Actions

The agent may not:

- invent new core metaphysics
- add new claimants without approval
- resolve central truths not permitted by the current canon
- weaken static-build constraints
- ignore style rules or acceptance tests
- write to `schema-generation/` when `execution_phase.current_phase` forbids it
- write to `prose/` when `execution_phase.current_phase` forbids it

## 4. Generation Order

1. Read source-of-truth files
2. Read and obey `execution_phase.current_phase` in `engine/data/work-instance.yaml`
3. Apply the current execution milestone and resolve machine-selectable decisions from `engine/data/work-instance.yaml`; consult the human-decision contract only for true escalation triggers
4. If phase is `engine_revision`, mutate only `engine/` and stop before downstream output generation
5. Compile claimant profiles when claimant generation is enabled and the phase gate allows planning compilation
6. Produce the planning outputs required by the current milestone in `schema-generation/` only when the phase gate allows it
7. Stop after planning validation when the current milestone is planning-only
8. Produce prose and artifacts from specs in `prose/` only when the current milestone or the human requires it and the phase gate allows it
9. Validate outputs against canon and tests
10. Compile `schema-generation/decision-graph.json` only when graph work is in scope and the phase gate allows it
11. Render static pages only when build work is in scope and the phase gate allows it

## 5. Validation Order

Validate:

- claimant-profile integrity
- claimant-profile separation
- ontology consistency
- claimant consistency
- scene function
- style compliance
- mobile readability assumptions
- route differentiation

## 6. Stop Conditions

The agent must stop and flag for human review if:

- canon files conflict
- a scene cannot satisfy both ontology and style rules
- a route collapses into cosmetic variation
- no valid claimant-profile set satisfies both hard constraints and expressive separation
- the build requires a new world rule not already present
- the requested action would violate the current phase gate

## 7. Graph and Path Trace Implementation

- every scene spec must have a stable scene_id
- every branch or decision option must have a stable edge_id
- every ending must have a stable ending_id
- every compiled route must be graph-exportable into decision-graph.json
- ending-page decision visuals must be derivable from the full graph plus the reader's recorded path
- the rendered ending-page view must show the taken path as the primary spine and rejected sibling options at each decision point
- in debug mode, rejected sibling options may also display their destination scene titles
- reserved sibling edges may exist for alternatives that are structurally preserved but not yet playable
- no scene, branch, or ending may be considered complete unless its graph links are valid and its local path-trace relationships can be derived

## 8. Scene generation must obey the scene spec length budget.

Rules:

- aim for target_min to target_soft_max by default
- do not exceed target_hard_max
- if a scene would exceed target_soft_max, compress before expanding
- only exceed target_soft_max when the scene’s structural role explicitly justifies it
- if the scene cannot satisfy its required outputs within budget, flag for review rather than silently bloating
