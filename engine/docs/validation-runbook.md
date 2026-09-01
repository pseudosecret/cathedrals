# Validation Runbook

## Rule

Validation decides whether an immutable generation lives or dies. It never becomes a
creative revision loop.

## 1. Preflight

Pass only if:

- the current operation explicitly authorizes a generation test
- the target is a generation branch or release, not `main`
- engine commit and configuration hashes are recorded
- the selected model's documented maximum output meets the configured minimum
- the budget formula passes with its safety reserve
- the topology and geomancy inputs were derived deterministically
- no claimant identity, incident fact, scene event, artifact, or ending was selected
  during preparation

Failure stops before any creative transaction.

## 2. Transaction Audit

Pass only if:

- one creative request was made
- one complete creative response was received
- no earlier generated plan or profile was used as a later creative prompt
- no scene, artifact, ending, or replacement passage came from another creative call
- provenance records `creative_transaction_count: 1`

## 3. Mechanical Validation

Run every check in the mechanical section of `engine/canon/acceptance-tests.md`.
At minimum validate:

- JSON parsing and JSON Schema
- unique IDs and complete cross-references
- exactly five unique technical claimant slots
- scene, artifact, and ending count bounds
- graph reachability, decision cardinalities, reconvergence, redirects, and state effects
- exact three-option opening hub after three to five introduction surfaces
- downstream splitting and unequal permissible depths
- consequential hesitation for major decisions
- formal-composition anchors
- word and output budgets
- safe MDX subset and deterministic projection
- Astro static compilation

Emit `PASS` or `FAIL` with concrete machine-readable failures.

Serialization repair is allowed only when all literary strings and creative facts are
byte-identical. Never complete truncated JSON by inference.

## 4. Artistic Acceptance

Evaluate the complete projected work against engine canon. A human or non-creative
evaluator transaction may judge the work, but its only authority is a verdict and
reasons. It may not author replacement content, and its result may not be fed into a
repair call for the same generation.

Return exactly one result:

- `PASS`
- `FAIL GENERATION`

Assess claimant differentiation, route distinction, prose quality, dramatic scene
function, concrete detail, artifact force, thematic coherence, formal composition,
redundancy, generic AI habits, and ending consequence.

## 5. Failure Handling

On any post-transaction failure:

- mark the generation rejected
- preserve failure evidence and provenance if useful
- do not edit generated literary files or fictional facts
- do not ask a model to repair, continue, rewrite, or fill gaps
- do not publish the failed work

A later attempt must use a new generation ID and exactly one new creative transaction.

## 6. Acceptance and Hashes

After both validation categories pass:

- hash the raw bundle, graph, literary files, and verdicts
- record hashes in the generation manifest
- fail publication if any accepted literary hash changes
- visually inspect mobile, light, dark, artifact, choice, and ending surfaces

Visual engine defects may be fixed without changing generated content. Rebuild and
rehash engine artifacts as needed, but preserve literary hashes.
