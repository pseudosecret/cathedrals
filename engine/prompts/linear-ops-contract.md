# Linear Ops Contract

## 1. Purpose
Linear is the execution tracker for this project. It exists to track progress, generation tasks, validation tasks, unresolved design decisions, and continuity fixes.

Linear is not the source of truth for lore, ontology, arc law, state law, or accepted prose. The repository is the source of truth.

## 2. Source of Truth Hierarchy
When determining what is true, use this order:

1. engine/docs/artistic-constitution.md
2. engine/docs/specs.md
3. engine/docs/repo-contract.md
4. engine/data/work-instance.yaml
5. engine/docs/human-decision-contract.md, if present, as escalation-only guidance
6. engine/docs/content-schema-contract.md, if present
7. engine/canon/ontology.md
8. engine/canon/arc-grammar.md
9. engine/canon/style-rules.md
10. engine/canon/acceptance-tests.md
11. engine/data/state-model.yaml
12. engine/data/claimants.yaml
13. engine/data/threshold-geomancy.yaml, if present
14. compiled planning artifacts in `schema-generation/`
15. generated content files in `prose/`
16. Linear issue descriptions and comments

If Linear conflicts with repo files, repo files win.

## 3. Allowed Uses of Linear
Use Linear to track:
- artwork-level progress
- arc generation tasks
- scene generation tasks
- artifact generation tasks
- continuity review tasks
- validation failures
- unresolved lore or design decisions
- build and implementation work

Do not use Linear as the only location for:
- canonical lore
- claimant definitions
- ontology definitions
- accepted state rules
- final scene text

## 4. Required Planning Flow
For narrative generation, always follow this order:

1. Read canon and data files
2. Read `milestone_control.active_milestone_id` and the matching milestone record in `engine/data/work-instance.yaml`
3. Compile or update claimant profiles when enabled
4. Save claimant profiles in the repo
5. Compile or update arc briefs for the in-scope routes
6. Save arc briefs in the repo
7. Create or update Linear arc issues from the repo arc briefs
8. Compile scene and artifact specs for those arcs
9. Save scene and artifact specs in the repo
10. Create or update Linear scene and artifact issues from those specs
11. Generate prose only when the active milestone requires it and the phase gate allows it
12. Validate prose against canon and acceptance tests before closing implementation issues
13. Save approved prose in the repo
14. Update Linear issue status and summary

Repository path rules:

- ARC repo paths point to `schema-generation/arc-briefs/*.md`
- SCENE repo paths point to `schema-generation/scene-specs/*.md` and `prose/scenes/*.mdx`
- ARTIFACT repo paths point to `schema-generation/artifact-specs/*.md` and `prose/artifacts/*.mdx`
- VALIDATION repo paths point to `schema-generation/validation-reports/*.md`

Do not generate prose directly from vague route names or high-level themes.

## 5. Issue Types
The system should use the following conceptual issue types:

- ARC
- SCENE
- ARTIFACT
- VALIDATION
- CONTINUITY
- DECISION
- BUILD

If the Linear workspace supports labels, use these labels. If not, include the type in the title and body.
If no repo-specific project exists for the work, create or use one named after the workspace or work id before broad tracking begins.

## 6. Naming Conventions
Recommended titles:

- ARC: [work_id] Arc - [arc_id]
- SCENE: [work_id] Scene - [scene_id]
- ARTIFACT: [work_id] Artifact - [artifact_id]
- DECISION: [work_id] Decision - [topic]
- CONTINUITY: [work_id] Continuity - [problem]
- BUILD: [work_id] Build - [feature]

Titles should be concise and stable. Canonical IDs should not change casually.

## 7. Required Fields for Arc Issues
Each ARC issue must include:
- work_id
- arc_id
- claimant or route identity
- arc purpose
- required beats
- current status
- preconditions
- scene count target or limits
- early termination rules if applicable
- repo paths to arc brief and related files

## 8. Required Fields for Scene Issues
Each SCENE issue must include:
- work_id
- arc_id
- scene_id
- claimant if relevant
- beat role
- input state
- required outputs
- forbidden outputs
- transition target if known
- validation checklist
- repo paths to scene spec and output file

## 9. Required Fields for Artifact Issues
Each ARTIFACT issue must include:
- work_id
- artifact_id
- artifact type
- route or claimant relevance
- interpretive function
- required clue or contradiction
- output path
- validation checklist

## 10. Required Fields for Decision Issues
Each DECISION issue must include:
- topic
- why unresolved
- impacted files
- blocked tasks
- acceptable answer shape
- deadline or review moment if applicable

Decision issues are for unresolved canon questions, milestone-scope changes, or blocked transitions, not routine prose revision.

## 11. Scene and Arc Summaries
Arc summaries and scene summaries are derived planning artifacts.

Rules:
- derive them from canon and current data
- store them in the repo first
- mirror them into Linear issue descriptions
- refresh them when canon changes
- do not treat them as canonical if they drift from repo truth

## 12. Validation Rules
No issue may be marked complete merely because output exists.

A SCENE or ARTIFACT issue is complete only if:
- required beat function is satisfied
- ontology is respected
- style rules are respected
- acceptance tests pass
- file output path exists in repo

An ARC issue is complete only if:
- all required beats are satisfied
- all required child scenes/artifacts are complete
- or the arc terminates early according to canon rules

## 13. Early Termination and Premature Endings
Arcs may end early due to:
- death
- disappearance
- collapse
- unresolved failure
- contamination threshold
- lockout or adjudicated closure

If an arc ends early:
- update the arc brief in repo
- update the Linear ARC issue
- close or relabel remaining child scene issues as invalidated, skipped, or superseded
- generate residue or aftermath tasks if canon requires them

## 14. Continuity and Lore Changes
When lore or canon changes:
1. update repo canon first
2. identify affected arc and scene specs
3. recompile summaries
4. update affected Linear issues
5. reopen invalidated issues where necessary

Do not patch issue descriptions without updating repo truth.

## 15. Stop Conditions
The system must stop and flag for human review if:
- canon files conflict
- scene spec conflicts with arc brief
- required beat cannot be satisfied
- claimant voice or ontology is ambiguous
- new lore would need to be invented
- arc drift suggests structural redesign rather than local revision

## 16. Default Status Logic
Conceptual statuses should follow this flow:

- planned
- ready
- generating
- validating
- needs_review
- accepted
- blocked
- rejected
- superseded

Map these to the available statuses in the Linear workspace.

## 17. Human Review Triggers
Human review is required when:
- a route changes ontology
- a new contradiction appears at canon level
- a premature ending would reshape downstream arcs
- the hidden route logic changes
- a scene repeatedly fails validation for structural reasons

## 18. Final Rule
Linear exists to make forward motion legible.
The repo exists to preserve truth.
If these two functions are mixed carelessly, the project will accumulate drift and false progress.
