# Start Here

## Purpose

This document is the cold-start entrypoint for operators working on `hospice-annex-v01`.

Read this when you are entering the repo without prior chat context.
Its job is to tell you what to read first, what not to guess, and what the first lawful unit of execution is.

## Read Order

Read these files in order:

1. `engine/llm-instructions.md`
2. `engine/docs/artistic-constitution.md`
3. `engine/docs/specs.md`
4. `engine/docs/repo-contract.md`
5. `engine/data/work-instance.yaml`
6. `engine/docs/human-decision-contract.md`
7. `engine/docs/content-schema-contract.md`
8. `engine/docs/validation-runbook.md`
9. `engine/docs/build-contract.md`
10. `engine/prompts/execution-contract.md`
11. `engine/prompts/planning-compiler.md`
12. `engine/prompts/linear-ops-contract.md`

If any lower file conflicts with a higher file, the higher file wins.

## What This Repo Is For

This repo defines and will eventually render a static, build-time-generated literary mystery set in a snowbound hospice annex.

The immediate goal is narrower:

- make the repo blind-executable for the current work-instance phase and milestone
- keep canon in repo files
- treat the invoked directory as the full project boundary
- do not inspect parent or sibling directories unless the human explicitly authorizes it
- obey `engine/data/work-instance.yaml` as the single operational scope controller
- keep the final reader experience static and Astro-based

## Default First Task

If the user says "continue" or gives a broad execution instruction, start here:

1. audit repo truth against the read order above
2. resolve machine-selectable decisions from `engine/data/work-instance.yaml`
3. treat the invoked directory as the complete project root and do not inspect parent or sibling directories
4. check the current phase gate in `engine/data/work-instance.yaml`
5. check `milestone_control.active_milestone_id` and the corresponding `execution_milestones` record
6. if the phase is `engine_revision`, mutate only `engine/` files even when downstream milestones are canonized
7. use `engine/docs/human-decision-contract.md` only if repo policy explicitly requires human override
8. treat milestone auto-advance as validation-gated readiness, not execution permission
9. update build code only after the phase gate allows downstream work
10. mirror execution state into Linear only after repo artifacts are current
7. validate engine-side contract consistency using `engine/docs/validation-runbook.md`

## Do Not Guess

Stop and ask for human review if:

- canon files conflict
- a required planning artifact would need new ontology
- a threshold geomancy rule is required but undefined
- route differentiation collapses into cosmetic variation
- a build choice would move important story truth out of repo files

## Current Scope Lock

The live operational scope is controlled by `engine/data/work-instance.yaml`.

Read these sections there instead of relying on stale summaries:

- `execution_phase`
- `milestone_control`
- `execution_milestones`
- `milestone_transitions`
- `generation_resolution_policy`
- `decision_status`
- `assumption_registry`

Project-wide guardrails remain:

- work id is `hospice-annex-v01`
- current claimant roster is `custodian`, `mourner`, `examiner`
- parent/sibling directory inspection remains forbidden unless the human explicitly authorizes it
