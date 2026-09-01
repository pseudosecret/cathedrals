# Execution Contract

## Current Gate

Read `engine/data/work-instance.yaml`. During `engine_revision`, change only the
engine. Do not create generated work or mutate downstream projections.

## Compliant Generation

When an explicit future instruction activates a generation test:

1. create a generation branch
2. deterministically calculate scope, budget, abstract topology, state constraints,
   threshold figures, resultants, provenance, and context hashes
3. fail before generation if the selected model cannot fit the declared budget
4. assemble the complete engine context and JSON Schema
5. make exactly one creative model request using
   `engine/prompts/single-transaction-generation.md`
6. preserve the one complete response as the generation bundle
7. parse, validate, project, hash, and build deterministically
8. accept with `PASS` or reject with `FAIL GENERATION`

## Allowed Deterministic Actions

- seed and hash calculation
- abstract structural preparation
- threshold-geomancy calculation
- prompt assembly
- schema and graph validation
- file projection and frontmatter creation
- checksums and manifest creation
- Astro static compilation

## Forbidden Actions

- pre-author claimant identities, incident facts, scene events, artifacts, or endings
- select fictional archetypes for technical slots
- use separate creative planning, profiling, prose, critique, or repair calls
- creatively fill a truncated or invalid bundle
- edit generated literary content after the call
- publish a failed generation
- place a generated work on `main`

## Failure

Mechanical and artistic validation produce verdicts, not repair tasks. A failed work
may be followed only by an entirely new generation ID and a new single creative
transaction after explicit instruction.
