# Validation Runbook

## Rule

Validation decides whether an immutable autonomous run lives or dies. It never becomes
a creative revision loop.

## 1. Preflight

Pass only when one instruction authorizes a generation branch, the generation brief
is frozen, engine/prompt/schema hashes and seeds are recorded, every selected model can
fit its planned context/output, total derived scope budgets fit cumulative limits, topology
capacity and geomancy are deterministic, and preparation authored no fiction.

## 2. Forward-Run Audit

Validate every protocol record and ledger entry. Confirm strict sequences and hash
chains; frozen manifest/brief/engine inputs; dependency order; atomic unique commits;
no overwrites; no candidate selection; and complete step metadata. Recompute hashes
from raw and committed files.

For `READY_TO_PLAY`, require:

```text
human_intervention_count = 0
committed_rewrite_count = 0
committed_regeneration_count = 0
backtrack_count = 0
creative_step_count >= 1
```

Technical retries must be identical except for attempt/audit fields and must have no
prior creative output. A malformed response is terminal, not retryable.

## 3. Mechanical and Continuity Validation

Run every mechanical check in `engine/canon/acceptance-tests.md`, including protocol,
IDs, cross-references, scope/packet bounds, graph reachability, choices, splitting,
reconvergence, redirects, hesitation, state effects, variants, formal compositions,
safe MDX, projection bytes, memory provenance, resource totals, and complete static
compilation.

Check suspected contradictions against original immutable passages. Preserve lawful
incompatible evidence or perspectival contradiction. If a true mechanical
impossibility prevents completing the frozen graph without changing prior canon,
return `FAILED_GENERATION`.

Serialization repair is lawful only before commit and only when creative bytes and
facts remain unchanged. Never complete truncated or malformed creative output by
inference.

## 4. Whole-Work Artistic Acceptance

After all creative steps end, a configured non-authorial evaluator reads the complete
immutable work and returns `PASS` or `FAIL GENERATION` with concrete reasons. Assess
claimant differentiation, route distinction, prose quality, dramatic scene function,
detail, artifact force, thematic coherence, formal composition, redundancy, generic
AI habits, and ending consequence. Do not emit edits or feed findings into a repair
call.

## 5. Static Build and Barrier

Project all required content, compile Astro, validate every route/state behavior, and
verify the complete build uses only deterministic client-side state. Confirm every
presented choice points to prebuilt content or behavior and no runtime model/API is
needed.

Only a complete mechanical pass, artistic pass, and build pass may finalize
`READY_TO_PLAY` with `playable: true`. Every failure finalizes `FAILED_GENERATION`
with `playable: false`; partial content remains quarantined under the retention policy.

## 6. Accepted Hashes

Finalization records the ledger head, every committed creative record, memory event
stream, projections, decision graph, validation verdicts, and build hash. Any later
literary or generated-fact hash mismatch invalidates publication. Engine presentation
defects may be fixed in a separate engine revision without changing generated content.
