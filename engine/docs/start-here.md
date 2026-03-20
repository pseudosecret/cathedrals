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

- make the repo blind-executable for the current engine-revision phase
- keep canon in repo files
- treat the invoked directory as the full project boundary
- do not inspect parent or sibling directories unless the human explicitly authorizes it
- keep `schema-generation/` and `prose/` untouched during engine revision
- move into compilation only after the phase gate in `engine/data/work-instance.yaml` changes
- keep the final reader experience static and Astro-based

## Default First Task

If the user says "continue" or gives a broad execution instruction, start here:

1. audit repo truth against the read order above
2. apply defaults from `engine/docs/human-decision-contract.md`
3. treat the invoked directory as the complete project root and do not inspect parent or sibling directories
4. check the current phase gate in `engine/data/work-instance.yaml`
5. if the phase is `engine_revision`, mutate only `engine/` files
6. do not compile `schema-generation/` or `prose/` outputs until the phase gate changes
7. validate engine-side contract consistency using `engine/docs/validation-runbook.md`
8. update build code only after the phase gate allows downstream work
9. mirror execution state into Linear only after repo artifacts are current

## Do Not Guess

Stop and ask for human review if:

- canon files conflict
- a required planning artifact would need new ontology
- a threshold geomancy rule is required but undefined
- route differentiation collapses into cosmetic variation
- a build choice would move important story truth out of repo files

## Current Scope Lock

The current operational scope is:

- work: `hospice-annex-v01`
- current phase: `engine_revision`
- milestone: `planning_parity_01`
- claimant routes in scope: `custodian_route`, `mourner_route`, `examiner_route`
- route package shape: three scenes plus one artifact spec per claimant route
- contamination: canonical but deferred from the current milestone
- retraction: preserved in canon and state logic, not required as playable output in the current milestone
- prose/build parity: not yet required
- writes to `schema-generation/` and `prose/`: forbidden until the phase gate changes
- parent/sibling directory inspection: forbidden unless the human explicitly authorizes it
