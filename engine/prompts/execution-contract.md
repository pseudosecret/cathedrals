# Execution Contract

## Current Gate

Read `engine/data/work-instance.yaml`. During `engine_revision`, change only the
engine. Do not create generated work or mutate downstream projections.

## Compliant Generation

After `./cathedrals` collects and freezes one explicit experience request:

1. create a generation ID and copy the current local launcher and engine into the run directory
2. freeze the high-level request as `generation_brief.mutable: false`
3. use only the run-local engine copy and freeze seeds, explicit scene scope, model, derived budgets, and traversal strategy
4. preflight every planned call against per-step and cumulative limits
5. write the immutable run manifest and initialize the hash-chained ledger
6. generate and commit genesis with `engine/prompts/generation-genesis.md`
7. generate and commit architecture with `engine/prompts/generation-architecture.md`
8. recompute a prospective plan and follow immutable dependencies using `generation-packet.md` and
   `generation-ending-packet.md`
9. after each commit apply constraint deltas and recompute feasibility without changing canon
10. project and mechanically validate, then build and validate the complete static work
11. artistically accept or reject; publish only after acceptance
12. finalize only as `READY_TO_PLAY` or `FAILED_GENERATION`

## Allowed Actions

- deterministic seed, geomancy, topology-envelope, hash, budget, and context assembly
- multiple causally forward creative calls inside the one autonomous run
- source-grounded noncreative analysis calls that cannot author replacement fiction
- append-only commits, ledgers, constraint events, audited prospective plans, and deterministic projections
- graph, technical destinations, state, safe Markdown, continuity, resource, hash, and static-build validation
- whole-work artistic acceptance after creative generation ends

## Forbidden Actions

- human creative steering after the run starts
- fictional candidate generation followed by scoring, selection, or discard
- overwrite, rewrite, regenerate, improve, or retcon any committed creative record
- retry malformed but creatively substantive output
- treat artistic weakness as technical failure
- publish or play a partial or failed work
- generate missing content during play
- publish generated work anywhere except `generated-work/<generation-id>/`

## Failure

Transport or provider failure before creative output may retry the identical planned
step. Malformed output, impossible continuity, exhausted frozen budgets, failed
mechanics, artistic rejection, or generated-content build failure ends the run. A
later attempt requires a new generation ID.
