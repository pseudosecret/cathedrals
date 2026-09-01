# Operator Runbook

## Current State

Read `engine/data/work-instance.yaml` first. While its phase is `engine_revision`,
mutate only `engine/`. Do not generate work canon, planning artifacts, prose, a graph,
or Astro story pages.

## First Generation Test

Run the following steps only after one explicit human instruction activates the test.

1. Create a generation branch; never place a generated work on `main`.
2. Verify the working tree and engine commit SHA.
3. Select one model whose documented maximum output is at least the configured minimum.
4. Choose the work, structural, and geomancy seeds.
5. Calculate the output budget and stop before generation if it fails.
6. Deterministically create the abstract branch skeleton, state envelope, and
   threshold-geomancy assignments.
7. Hash the engine inputs and assemble the context specified by
   `engine/prompts/single-transaction-generation.md`.
8. Make exactly one creative model call and preserve its raw response.
9. Do not make another creative call for that generation ID.
10. Parse and schema-validate the complete bundle.
11. If validation fails, mark the generation failed; repair only purely
    mechanical serialization when literary bytes and creative facts do not change.
12. Deterministically project the valid bundle into `schema-generation/` and `prose/`.
13. Run cross-reference, graph, MDX, and Astro compile checks.
14. Hash all generated literary files.
15. Perform artistic acceptance and return only `PASS` or `FAIL GENERATION` with reasons.
16. On `PASS`, inspect and publish the static Astro site under the build contract.
17. On any generation failure, do not improve the work. End that generation instance.

## Provenance

The accepted manifest records all fields listed in
`engine/data/work-instance.yaml#provenance`, including
`creative_transaction_count: 1`. Missing provenance is a mechanical failure.

## Tracking

Repo truth comes first. External trackers may mirror a generation ID and its phase,
validation verdicts, and build status, but may not contain unique fiction or authorize
additional creative calls.

## Stop Conditions

Stop before the creative call for:

- engine-canon conflict
- failing output-budget preflight
- missing deterministic geomancy or topology input
- a selected model with insufficient documented output capacity
- an instruction that would require more than one creative transaction
- a requested write forbidden by the current phase gate

Do not stop for ordinary fictional choices. They belong to generation.
