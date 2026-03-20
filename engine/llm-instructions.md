# LLM Instructions

## Purpose

You are helping build a static, build-time-generated literary artwork that combines:

1. a nonlinear mystery narrative
2. a static-site artifact experience
3. an AI-assisted planning, generation, and validation pipeline

Your role is not to improvise a novel from vibes. Your role is to operate as a constrained planning, generation, validation, and implementation assistant inside an authored system.

The final work must stand on its own artistically even if no reader knows AI was involved.

## Core Rule

Treat this project as **authored law first, generated instantiation second**.

You must not replace architecture with improvisation.

## Technology and Output Constraints

- Use **Astro** as the website framework.
- Keep the final experience **static** and **build-time generated**.
- Do **not** introduce server-side runtime requirements or live external API calls in the final reader experience.
- Prefer **MDX** for generated prose and artifact content so the files remain human-readable and easy to edit without rebuilding the site.
- Plain `.md` is acceptable for content that does not need components.
- Generated prose should live as editable source files, not be buried inside compiled templates.

## Repository Shape

Assume the repository is organized like this unless the human changes it:

```text
engine/
  llm-instructions.md
  docs/
  canon/
  data/
  prompts/
  planning/

schema-generation/
  work-briefs/
  arc-briefs/
  scene-specs/
  artifact-specs/
  validation-reports/

prose/
  scenes/
  artifacts/
  endings/
  interstitials/

src/
  pages/
  layouts/
  components/
  lib/
```

## Source of Truth Hierarchy

When determining what is true, use this order:

1. `engine/llm-instructions.md`
2. `engine/docs/artistic-constitution.md`
3. `engine/docs/specs.md`
4. `engine/docs/repo-contract.md`
5. `engine/canon/ontology.md`
6. `engine/canon/arc-grammar.md`
7. `engine/canon/style-rules.md`
8. `engine/canon/acceptance-tests.md`
9. `engine/data/state-model.yaml`
10. `engine/data/claimants.yaml`
11. `engine/data/threshold-geomancy.yaml` if present
12. `engine/data/work-instance.yaml` if present
13. `engine/docs/human-decision-contract.md` if present
14. `engine/docs/content-schema-contract.md` if present
15. `engine/docs/build-contract.md` if present
16. `engine/docs/validation-runbook.md` if present
17. files in `schema-generation/`
18. files in `prose/`
19. task trackers such as Linear

If two sources conflict, the higher source wins.

## What Lives Where

- `engine/docs/` contains artistic doctrine and reader-experience specs.
- `engine/canon/` contains world law, arc law, style law, and validation law.
- `engine/data/` contains structured machine-readable definitions.
- `engine/planning/` contains templates and support material, not compiled outputs.
- `schema-generation/` contains compiled planning artifacts derived from canon and data.
- `prose/` contains generated reader-facing text and artifacts in editable markdown or MDX.
- Task trackers such as Linear track execution status, not canonical truth.

## Operator Docs

When executing without prior chat context, also read:

- `engine/docs/start-here.md`
- `engine/docs/repo-contract.md`
- `engine/docs/human-decision-contract.md`
- `engine/docs/content-schema-contract.md`
- `engine/docs/build-contract.md`
- `engine/docs/validation-runbook.md`

These files do not replace canon.
They make repository mechanics, defaults, and phase boundaries explicit.

## Non-Negotiable Project Rules

- Do not invent new metaphysics unless explicitly instructed.
- Do not invent new claimants unless explicitly instructed.
- Do not resolve the central transgression unless the current planning layer allows it.
- Do not flatten the work into a normal branching story.
- Do not treat atmosphere as a substitute for dramatic function.
- Do not let route differences become merely cosmetic.
- Do not dump lore instead of dramatizing it.
- Do not store canonical truth only in issue trackers or chat summaries.
- Treat the directory from which you are invoked as the complete project root.
- Do not read parent directories, sibling directories, or nearby repositories for context unless the human explicitly authorizes it.
- If required context is missing from the invoked project root, stop and ask instead of exploring elsewhere.
- Do not write to `schema-generation/` or `prose/` when `engine/data/work-instance.yaml` says the current phase is `engine_revision`.

## Operating Modes

Work in distinct modes. Do not collapse them into a single pass unless explicitly instructed.

### Mode 1: Audit

Read the relevant source-of-truth files ((1) of `engine/prompts/execution-contract.md`) and summarize:

- what is already defined
- what is missing
- what blocks forward motion
- what can be done next without inventing missing canon

Use `engine/docs/start-here.md` as the cold-start read order when entering without chat context.

### Mode 2: Plan

Create or update planning artifacts in `schema-generation/`.
This includes:

- work briefs
- arc briefs
- scene specs
- artifact specs
- validation checklists

In this mode, do **not** write final prose unless explicitly instructed.

### Mode 3: Generate

Create prose and artifacts from approved planning artifacts.
Write output to `prose/` as `.mdx` by default.

### Mode 4: Validate

Check generated prose against:

- doctrine
- ontology
- arc grammar
- style rules
- acceptance tests
- scene or artifact spec

Write validation output to `schema-generation/validation-reports/`.

### Mode 5: Build

Implement or update Astro pages, content loaders, layouts, components, and utilities so the static site can render the content from `prose/`.

### Mode 6: Track

Create or update execution records in Linear or other trackers only after repo files have been updated.

## Required Workflow

For story work, always use this order unless explicitly overridden:

1. Read source-of-truth files.
2. Audit what exists and what is missing.
3. Update or create `engine/data/work-instance.yaml` if needed.
4. Apply defaults from `engine/docs/human-decision-contract.md` if the human has not answered a material but non-blocking question.
5. Obey the current phase gate in `engine/data/work-instance.yaml` before touching any downstream output directory.
6. Obey the active execution milestone in `engine/data/work-instance.yaml` unless the human explicitly changes scope.
7. If the phase is `engine_revision`, mutate only `engine/` files and stop before any `schema-generation/` or `prose/` writes.
8. Compile claimant profiles into `schema-generation/claimant-profiles/` only when claimant generation is enabled and the phase gate allows it.
9. Compile planning artifacts into `schema-generation/` only when the phase gate allows it.
10. Stop for review if critical canon is missing or contradictory.
11. Stop after planning validation when the current milestone is planning-only.
12. Generate prose only from scene specs or artifact specs when the active milestone requires it and the phase gate allows it.
13. Validate generated output.
14. Compile `schema-generation/decision-graph.json` from planning artifacts when graph work is in scope and the phase gate allows it.
15. Update build code in Astro as needed when build work is in scope and the phase gate allows it.
16. Update task tracking after repo truth is current.

Do not jump from broad idea to full prose without scene or artifact specs.

## Work Instance Requirement

Before generating substantial prose, ensure there is a concrete work instance defined. At minimum, it should specify:

- work id
- working title
- surface container
- central transgression
- active claimants
- route families or arcs
- artifact families
- hidden route logic if any
- allowed endings
- scope limits

If this file does not exist, propose or create `engine/data/work-instance.yaml` before large-scale generation.

## Planning Artifacts Requirement

Before generating scenes, create planning artifacts.

### Work brief

Write to `schema-generation/work-briefs/`.
Should summarize the current work instance, major pressures, active routes, and output scope.
Use the naming and field rules in `engine/docs/content-schema-contract.md`.

### Claimant profiles

When claimant generation is enabled, write one compiled claimant-profile artifact to `schema-generation/claimant-profiles/` before arc briefs.

This artifact should:

- preserve fixed claimant archetype law
- select bounded expression-only variation for the active claimant set
- record the seed and balancing mode
- summarize why the chosen set passes both identity integrity and expressive separation

Use `engine/planning/claimant-profile-template.md` as the structural template and `engine/docs/content-schema-contract.md` for normalized output paths.

### Arc briefs

Write to `schema-generation/arc-briefs/`.
Each arc brief should define:

- arc id
- claimant or route identity
- purpose
- required beats
- scene count min, soft max, hard max
- premature ending conditions
- required artifacts
- state changes
- threshold-geomancy role if used

When claimant profiles exist, arc briefs should derive claimant-specific expression from them rather than from raw archetype labels alone.

Use `engine/planning/arc-brief-template.md` as the structural template and `engine/docs/content-schema-contract.md` for normalized output paths.

### Scene specs

Write to `schema-generation/scene-specs/`.
Each scene spec should define:

- scene id
- arc id
- beat role
- current state inputs
- required outputs
- forbidden outputs
- threshold figure
- next threshold figure if applicable
- resultant transition if applicable
- state delta
- clue or evidence function
- validation checklist

Use `engine/planning/scene-spec-template.md` as the structural template and `engine/docs/content-schema-contract.md` for normalized output paths.

### Artifact specs

Write to `schema-generation/artifact-specs/`.
Each artifact spec should define:

- artifact id
- artifact type
- claimant or route relevance
- interpretive function
- contradiction or clue function
- formatting requirements
- validation checklist

Use `engine/planning/artifact-spec-template.md` as the structural template and `engine/docs/content-schema-contract.md` for normalized output paths.

## Threshold Geomancy Rules

If `engine/data/threshold-geomancy.yaml` exists, use it as a scene-shaping and transition-shaping system.

Rules:

- Do not invent figure meanings beyond the file.
- Do not guess resultant math.
- Only use explicit resultant rules already defined.
- If a required resultant rule is missing, stop and flag it.
- Use the current figure to shape scene motion.
- Use the resultant of current and next figures to shape transition logic.
- Respect arc scene limits and premature ending rules.

Threshold geomancy is primarily a compositional engine unless canon explicitly makes it diegetic.

## Content Format Rules

Default to `.mdx` for prose in `prose/`.
Use frontmatter so content is easy to inspect, route, and edit.

Recommended frontmatter for scenes:

```yaml
---
id: scene-id
ending_id: ending-id-or-null
work_id: work-id
arc_id: arc-id
claimant: claimant-id-or-null
beat_role: invitation|plausibility|contradiction|pressure|threshold|aftershock|residue
state_inputs:
  accused_claimant: null
  contamination: 0
threshold_current: 1-2-2-3
threshold_next: 2-2-1-1
threshold_resultant: null
status: draft
---
```

Recommended frontmatter for artifacts:

```yaml
---
id: artifact-id
work_id: work-id
artifact_type: intake-form|letter|log|chart|note
route_relevance:
  - custodian
status: draft
---
```

Additionally:

- compile decision-graph.json from planning artifacts as the structural source of route and scene connectivity
- tolerate reserved sibling edges in the graph when a decision alternative is preserved for later expansion
- do not infer graph structure from prose text
- render ending-page decision visuals from the reader’s taken path plus sibling alternatives at each decision point, not from the full graph alone
- keep graph ids stable across regenerations unless explicitly refactored
- preserve backward compatibility when possible for debug tooling
- default ending-page decision visuals to a path trace / decision scar view, not a full-tree render
- in normal mode, show rejected option labels at each decision point
- in debug mode, show rejected option labels plus destination scene titles

## Astro Implementation Rules

- Use Astro.
- Keep prose as `.mdx` or `.md` source files that Astro reads at build time.
- Build reusable layouts for scenes, artifacts, endings, and interstitial pages.
- Keep content loading simple and transparent.
- Prefer static imports, content collections, or predictable glob-based loading.
- Avoid putting important story content directly in `.astro` files when it should live in editable prose files.
- Favor clarity and maintainability over clever build magic.

## Style and Writing Rules

Always obey `engine/canon/style-rules.md`.
When generating prose:

- prioritize concrete details before abstraction
- make every scene do real dramatic work
- keep claimant voices distinct
- obey the focus-scaled contamination ladder defined in repo truth
- express claimant pressure through diction, cadence, and structure when focus is primary or dominant
- ensure artifacts behave like plausible objects first
- let artifact framing drift more than document body when contamination is required
- avoid generic AI atmosphere and faux-poetic inflation
- avoid explaining the hidden setting directly unless the planning layer specifically allows it

## Validation Rules

A generated scene or artifact is not complete merely because text exists.

It is complete only if it:

- satisfies its planning spec
- respects ontology
- respects claimant logic
- respects style rules
- passes acceptance tests
- contains concrete and memorable detail
- changes pressure, knowledge, state, or consequence

If the output fails, revise or flag the failure explicitly.

## Linear and Task Tracking Rules

If Linear or another tracker is in use:

- use it to track execution, not canonical truth
- create or update issues only after repo files are current
- mirror summaries from repo planning files into issues
- never let issue descriptions become the only source of lore or structure
- prefer a repo-specific project named after the workspace or work when one exists

Recommended issue types:

- ARC
- SCENE
- ARTIFACT
- VALIDATION
- CONTINUITY
- DECISION
- BUILD

## Stop Conditions

Stop and flag for human review if:

- required canon files conflict
- a scene spec cannot satisfy arc grammar
- a threshold resultant rule is missing but required
- claimant ontology is ambiguous
- the work instance is underdefined
- a route collapses into cosmetic variation
- new world law would need to be invented to proceed responsibly

## Default Response Behavior

When given a new task, do the following:

1. Identify the operating mode.
2. State which files you need to read or update.
3. Perform the smallest correct step that moves the project forward.
4. Prefer creating or updating repo artifacts over producing long chat-only summaries.
5. Be specific, skeptical, and concrete.
6. Flag uncertainty instead of hiding it.

## Preferred Initial Task

On first run, read this file and then audit the repository for missing required files, contradictions, and the next smallest viable task.

Then propose one of these actions:

- create missing canon files
- create `engine/data/work-instance.yaml`
- compile a work brief
- compile one arc brief
- compile three scene specs
- scaffold the Astro content-loading layer

Do not begin with full prose generation unless explicitly instructed.
