# Execution Contract

## Current Gate

Read `engine/data/work-instance.yaml`. During `engine_revision`, change only the
engine. Do not create generated work or mutate downstream projections.

## Compliant Generation

After `./cathedrals` collects and freezes one explicit experience request:

1. create a generation branch and generation ID
2. freeze the high-level request as `generation_brief.mutable: false`
3. freeze/hash engine inputs, seeds, explicit scene scope, model, derived budgets, and traversal strategy
4. preflight every planned call against per-step and cumulative limits
5. write the immutable run manifest and initialize the hash-chained ledger
6. generate and commit genesis with `engine/prompts/generation-genesis.md`
7. generate and commit architecture with `engine/prompts/generation-architecture.md`
8. follow its frozen dependencies using `generation-packet.md` and
   `generation-ending-packet.md`
9. optionally use `generation-index.md` only for source-grounded memory work
10. project, validate, artistically accept or reject, build, and validate the complete
    static work
11. finalize only as `READY_TO_PLAY` or `FAILED_GENERATION`

## Allowed Actions

- deterministic seed, geomancy, topology-envelope, hash, budget, and context assembly
- multiple causally forward creative calls inside the one autonomous run
- source-grounded analysis/index calls that cannot author replacement fiction
- append-only commits, ledgers, memory events, and deterministic projections
- graph, state, MDX, continuity, resource, hash, and static-build validation
- whole-work artistic acceptance after creative generation ends

## Forbidden Actions

- human creative steering after the run starts
- fictional candidate generation followed by scoring, selection, or discard
- overwrite, rewrite, regenerate, improve, or retcon any committed creative record
- retry malformed but creatively substantive output
- treat artistic weakness as technical failure
- publish or play a partial or failed work
- generate missing content during play
- place generated work on `main`

## Failure

Transport or provider failure before creative output may retry the identical planned
step. Malformed output, impossible continuity, exhausted frozen budgets, failed
mechanics, artistic rejection, or generated-content build failure ends the run. A
later attempt requires a new generation ID.
