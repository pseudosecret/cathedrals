# Validation Runbook

## Rule

Validation decides whether an immutable autonomous run lives or dies. It never becomes
a creative revision loop.

## 1. Preflight

Pass only when one instruction authorizes a generation, the generation brief is
frozen, the run-local engine snapshot and seeds exist, every selected model can
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

Transport failures retry under the provider retry law. Invalid uncommitted structured
output receives three schema-aware corrections per invocation; exhaustion pauses the
run, and explicit resume grants three more. No correction may alter committed history.
Request timeouts and interrupted streams are the exception to automatic transport
retry: `provider_incomplete_response` immediately pauses and retains partial evidence.
Require a finish reason and `[DONE]` for streamed completions; never accept an
incomplete envelope or repair missing JSON by inference. Socket inactivity, including
the initial wait, defaults to 5,400 seconds; total active generation time is unbounded
by HTTP timeout but remains subject to frozen output-token limits.
Validate the 1,200-word scene/ending chunk ceiling, including nested artifacts, before
preserving artistic prose or requesting semantic normalization. A length overrun is
an uncommitted payload correction, never a metadata correction. The 4,800-word logical
packet target is guidance only; whole-work literary limits remain hard safeguards.

Reference failures are resolved before commit using typed declared-target catalogs
and the focused `engine/prompts/resolve-reference.md` instruction. Only an exact
listed identifier or `UNRESOLVED` is accepted. Check reference-repair history against
immutable raw responses and confirm that literary strings did not change. Complete
packet validation must precede metadata staging; a metadata error must not spend an
artistic correction attempt. Missing content and committed-history corruption retain
their existing failure handling.

Architecture drafts, including complete members and array elements of malformed
responses, are staged before recovery. Verify one broad request per core/batch, then
coherent recovery batches before isolated fields. A batch's valid entries must persist
while only unsuccessful entries split. Each request retains the entire assembled
planning context in compact JSON and only referenced schema definitions. No missing
JSON closure or final collection count may be inferred and no context may be clipped.
False, zero, and empty
collections are accepted values. Exhaustion must preserve them and retry only pending
values on explicit resume. Interrupted bulk and batch responses pause before further
requests. Genuine prompt-capacity shortfalls must pause without finalization, retain
all progress, and report capacity components before contacting the provider.
Allocated scene/ending IDs must resolve before assembled Architecture exists; motif
aliases must match committed event-to-motif identities. Failed `UNRESOLVED` lookups
must not be cached as success. Usage is counted once for every actual response.

Check initial whole-core and plan-batch prompts as well as recovery prompts. Required
sections must be complete before the final UTF-8 estimate is checked; builders must
not silently omit sections or list items using a different character/token ratio.
The planning-context suite reproduces saved failing input sizes with synthetic data,
checks all 25 geomancy assignments instead of the previously rendered 13, and verifies
that genuinely oversized complete requests pause before provider contact. Empty
collections, Unicode, authored whitespace, and the last required catalog item must
survive serialization. Verify the new optional model-derived planning ceiling,
unchanged limits for legacy manifests and other phases, cumulative input headroom,
and the smaller frozen/loaded window with output and reserve accounted for.
Replay the saved backward-setup context sizes with synthetic data: attached
instructions must reference unique exact guidance without changing checkpoints;
pending, missing, ambiguous, and mismatched copies must remain complete. Remaining
setups must finish in coherent batches and resume without repeating accepted work.

Verify that every ending seed, prerequisite, and retained narrative hint has an earlier
scene placement and authored setup guidance before any Architecture record commits.
A pause during this work must leave the core and every batch uncommitted. Resume must
reuse accepted placements. Arbitrary state labels must not become new runtime keys.
Check complete schema and dependency validation before the commit barrier and confirm
that scene/ending prose still uses coherent content requests.

Offline verification: run `python3 -B -m unittest discover -s engine/tests`, then
`python3 -B engine/tests/validate-generation-protocol.py`. The reference-resolution
suite includes a synthetic 20-scene run through `READY_TO_PLAY`, exercising real
validation, commits, projection, baseline build, accounting, and automatic repairs
with only provider responses replaced. It creates no fiction in the installation.
The provider-streaming suite uses synthetic SSE data and simulated time to check split
UTF-8, reasoning fields, usage-only events, long active streams, stalled requests,
malformed events, interrupted attempts, and replay without network access.
The planning-recovery suite includes saved failing-run metadata, allocated-slot
validation, exact aliases, malformed and truncated JSON, full-context field completion,
staged batch dependencies, backward setup interruption/resume, lossless context
compaction at saved failing prompt sizes, batch call-count reduction, partial success,
and exact accounting. All provider
responses are synthetic; the local model is never required by these checks.

The semantic-recovery suite uses metadata-only measurements from the saved 4,096-token
truncation. Verify the 8,192-token initial allowance, concise extraction instructions,
and unchanged literary bytes. A cut-off whole response must retain complete categories
and records; only pending categories are paged. Pages may continue beyond eight total
records, with stable fact aliases and delayed resolution of locally created motifs.
Check page-size reduction, expanded single-record headroom, no-progress rejection,
accurate attempt counts, category-specific canonical correction, interrupted-page
resume, exact response accounting, and a capacity pause before any oversized request.
The full 20-scene rehearsal must exercise semantic truncation recovery and retain its
complete validation, publication, and zero-human-intervention result.

## 3. Mechanical and Continuity Validation

Run every mechanical check in `engine/canon/acceptance-tests.md`, including protocol,
IDs, cross-references, scope/packet bounds, graph reachability, choices, splitting,
reconvergence, technical-slot destination resolution, redirects, hesitation, state
effects, variants, formal compositions, safe Markdown rendering, projection bytes,
generated art direction, constraint provenance, resource totals, and complete static
compilation.

Check suspected contradictions against original immutable passages. Preserve lawful
incompatible evidence or perspectival contradiction. If a true mechanical
impossibility prevents completing the frozen graph without changing prior canon,
return `FAILED_GENERATION`.

Serialization repair is lawful only before commit and only when creative bytes and
facts remain unchanged. Never complete truncated or malformed creative output by
inference.

## 4. Static Build and Diagnostic Preservation

Project all required content, render Markdown with raw HTML disabled, build the
dependency-free static reader, validate route/state behavior, and verify the complete
build uses only deterministic client-side state. A locked npm/Astro enhancement may
run afterward; its failure preserves and publishes the baseline with a warning.

## 5. Advisory Artistic Review

Artistic review is outside the publication gate. It may report warnings, but it does
not rewrite committed work, trigger replacement generation, or prevent publication
of a mechanically valid and buildable complete work.

## 6. Publication and Barrier

After validation and the baseline build, publish only the new generated-work tree. Paused and failed runs remain
under `.cathedrals/` by default.

Only complete planned content, a hard mechanical pass, and a baseline build pass may
finalize `READY_TO_PLAY` with `playable: true`. Correctable uncommitted failures pause;
partial content remains quarantined under the retention policy.

## 7. Accepted Hashes

Finalization records the ledger head, every committed creative record, constraint
event stream, prospective-plan history, projections, decision graph, validation verdicts, and build hash. Any later
literary or generated-fact hash mismatch invalidates publication. Engine presentation
defects may be fixed in a separate engine revision without changing generated content.
