# Operator Runbook

## Current State

Read `engine/data/work-instance.yaml` first. While its phase is `engine_revision`,
mutate only its declared write roots. Do not generate work canon, generation planning
artifacts, prose, a graph, or Astro story pages.

## End-User Run

From the Cathedrals installation, run:

```bash
./cathedrals
```

The executable asks only for project name, free-text genre/flavor, possible scene
scope, and story format. Visual-novel aliases are currently recorded but resolve to
the active web format. Model selection, when needed, is operational. After the brief
freezes, the executable asks no creative questions.

It then owns this sequence:

1. Create an independent generation ID and copy the current local launcher and engine
   into `.cathedrals/runs/<generation-id>/engine-snapshot/`.
2. Use that run-local snapshot for prompts, schemas, canon, formats, and resume.
3. Freeze the initial experience request as `generation_brief.mutable: false`.
4. Derive resource budgets from the explicit possible-scene scope; profile labels are
   guidance and never clamp the requested scope.
5. Verify documented model context/output limits; calculate per-step and cumulative
   token, literary-word, constraint-event, retrieval, and configured cost budgets.
6. Deterministically prepare abstract topology/state capacity and all relevant
   threshold-geomancy assignments.
7. Write the immutable run manifest, initialize counters, and start the ledger.
8. Make and commit the bounded Genesis foundation, cast, and constraint calls.
9. Make and commit the bounded Architecture core and every plan batch; freeze topology,
   attractors, hard obligations, and packet dependencies without freezing tentative realization order.
10. Assemble constraint-relevant contexts and execute each dependency-lawful packet
    selected by the current prospective plan. Append constraint and ledger records.
11. After every commit, update fact/knowledge/obligation/motif state and recompute
    audited future feasibility without changing canon.
12. Generate endings only after their prerequisite histories commit.
13. Deterministically project all committed content and validate protocol, hashes,
    graph, technical destinations, state, counts, Markdown, constraint provenance, and budgets.
14. Build and validate the dependency-free static baseline.
15. Attempt the locked npm/Astro enhancement when locally available; warn on failure.
16. On hard-gate success publish only the new generated-work tree. Write
    `finalization.json`: `READY_TO_PLAY` only after every barrier passes;
    otherwise `FAILED_GENERATION` with `playable: false`.

Artistic or structural quality concerns are recorded as publication warnings and do
not block a mechanically valid baseline.

Do not pause for creative approval. A valid but ugly packet commits. A run either
completes or dies.

The runner talks directly to LM Studio. It does not invoke Pi, Codex, CrewAI, or an
agent framework. Interrupted runs are detected under `.cathedrals/runs/`; resuming
reuses the run-local engine snapshot, frozen model, prompt hashes, seeds, ledger, and
committed records.

## Provenance and Counters

Every attempted step records generation ID, ledger sequence, planned step and attempt,
type/phase, parent hashes, prompt/context hashes, provider/model/parameters/seed,
timestamps, output hash, generated IDs, past/future/motif deltas, prospective-plan hash, branch relation,
commit status, failure class, and token/cost accounting.

`READY_TO_PLAY` requires zero human interventions, committed rewrites, committed
regenerations, and backtracks. `creative_step_count` may exceed one.

## Lawful Retry

Generation and analysis requests stream through the OpenAI-compatible Chat Completions
endpoint, requesting usage totals. The launcher prints request-start status and, as
chunks arrive, elapsed time and received-character counts at most every 15 seconds.
It does not print generated content or reasoning. `CATHEDRALS_HTTP_TIMEOUT` defaults
to 5,400 seconds of socket inactivity, including the wait for initial output; an
active stream may run longer than ninety minutes. Ordinary JSON responses remain supported.
The HTTP reader has no overall generation deadline.

Timeouts and interrupted streams use `provider_incomplete_response` and immediately
pause, without another automatic generation request. Check the named diagnostic
before resuming: the server may still be finishing the abandoned request. Raw
`*.api.sse` archives and incomplete `*.api.json` envelopes are retained per attempt;
partial streams cannot commit. A complete saved stream can be replayed without a
provider call. Scene and ending token-limit truncation retains its bounded expanded retry.
Other failures before a response retain bounded retries with identical requests.

Retry transport/provider failures under the provider law. Invalid uncommitted output
receives three schema-aware correction attempts per invocation; exhaustion enters
`PAUSED_GENERATION`, and resume grants three more. Packet prose must pass schema,
allocation, Markdown, reference, and length validation before it is staged for semantic
normalization and reused after a pause. Length corrections occur before staging;
metadata normalization cannot shorten preserved prose.

Invalid references receive automatic focused resolution throughout Genesis,
Architecture, packet plans, scenes, endings, and semantic metadata. After deterministic
aliases, the model receives the invalid field, source context, and typed valid targets;
it returns only an exact identifier or `UNRESOLVED`. Repairs change reference fields
before commit and preserve literary bytes. Missing targets or unsupported mappings
remain subject to bounded correction rather than automatic invented replacements.

Planning makes one broad draft request for the core and each plan batch, allowing up
to 21,800 output tokens when frozen context headroom permits. Recovery then requests
up to four coherent records together, sixteen independent reference resolutions, or
four setup requirements with their placements and instructions. Recovery batches allow
up to 8,192 output tokens, reduced to fit model headroom. Unknown collection counts
are chosen together in a layout request. The engine constructs containers, IDs, and
initial obligation status without asking the model for engine-owned values.

Each batch is attempted once. Valid entries and valid members of partially invalid
records are saved immediately; only unsuccessful entries split into smaller groups.
Isolated values receive three attempts per invocation. Accepted values, including
false, zero, and empty arrays, survive pause/resume without another broad request.
Complete members and array elements survive malformed or truncated JSON, including
records inside unfinished arrays. Unfinished containers remain explicit; missing
delimiters, collection completion, and missing text are never inferred. Interrupted
streams pause before continuing recovery on explicit resume.

Every request retains the whole assembled planning context and Genesis. JSON is
compact, repeated record bodies are removed, and only referenced schema definitions
are included. If complete compact context still exceeds the frozen prompt limit or
model capacity, planning enters `PAUSED_GENERATION`, preserving all accepted work.
The diagnostic reports prompt estimates, schema size, limits, and output/safety
reserves. No oversized request is sent and no authored context is silently clipped.

Planning catalogs include allocated scene and ending slots before Architecture exists.
Motif-event aliases use their exact recorded motif IDs. For an unresolved reference,
the model selects an existing typed target or authors a missing local obligation or
attractor through record recovery. Unknown relevance hints can instead become explicit
earlier setup instructions; they are retained with their original field and text,
not invented runtime state variables. `UNRESOLVED` is never cached as a successful
mapping. Claimants, committed sources, and accepted unrelated content remain fixed.

The core and every plan batch stay in `.staging/*.planning.json` until backward setup
placement is complete. Ending seed conditions, prerequisite obligations, and preserved
hints receive an earlier scene slot and an authored setup instruction, attached to
packet guidance with lawful dependencies. Only after the complete plan passes schema,
reference, dependency, and setup checks does the engine commit it and request prose.
Commits include `planning-draft.json` and field-response evidence. Scene and ending
prose still uses coherent bounded requests, without field-by-field literary generation.

Semantic normalization is separate from story generation. Its initial output allowance
is 8,192 tokens, including reasoning and JSON; the streamed character count is progress
information. Extract new continuity, evidence, knowledge, obligation, and motif changes
concisely, without restating canon or indexing every descriptive detail. Story-length
allowances remain unchanged.

When a whole metadata response truncates, retain its complete records and explicitly
closed categories. Continue pending categories in order: facts, knowledge, new soft
obligations, obligation updates, and motifs. Pages contain up to eight new records and
an explicit completion flag. This bounds each response, not the total information:
important changes may span multiple pages. Accepted facts keep their order and aliases;
references to new facts or motifs resolve after the full delta is assembled.

A truncated page retains its complete prefix and halves the next page size. A single
oversized record may use up to the frozen 15,000-token analysis ceiling when context
permits. Repeated pages that make no progress receive three correction attempts per
invocation, with accurate attempt counts. Interrupted streams pause immediately after
retaining complete records. Context capacity shortfalls pause without clipping source
content; other hard resource limits remain binding.

Progress lives in `.staging/<step>.semantic-recovery.json`; resume keeps accepted prose
and metadata and continues pending work. Canonical errors after paging correct only
the selected rejected category, preserving other categories and fact positions. Full
schema, reference, and packet validation precedes final metadata staging. Commits
include the recovery checkpoint and response evidence; incomplete provider envelopes
are never used as completed metadata responses.

Metadata must pass complete packet validation before staging. A paused lookup retains
the original artistic and pending metadata responses, so resume continues resolution
without repeating either accepted request. Each lookup has three attempts within the
frozen analysis and token budgets. Its raw responses and ledger entries retain token
accounting; the containing commit includes `named-reference-repair.json`. Successful
lookup costs are already ledgered and are not charged again at artistic commit.
New runs reserve three successful reference repairs per possible scene/ending chunk
in addition to the existing analysis allowance; unused capacity makes no calls. This
allowance is pooled across the run. Cumulative token ceilings use the resulting
analysis-step count and remain frozen at run creation. Calculation version 10 retains
the reserve of three attempts per schema-bounded planning field and per backward setup
value. This conservative recovery ceiling is capacity, not a forecast of calls or cost.
Successful and failed planning response usage is recorded before later requests;
accepted batch entries and eventual parent commits do not charge the response twice.
Semantic recovery additionally reserves three attempts per remaining event and per
category/scene-or-ending chunk. Actual category-page usage is ledgered once; the
assembled metadata envelope adds no provider usage at the containing artistic commit.

Each scene or ending chunk has a 1,200-word ceiling including nested artifact prose.
The logical packet's 4,800-word target is guidance only. The whole-work ceiling is
1,200 times the maximum scene-plus-ending count: a 20-scene request with five maximum
endings permits 30,000 literary words. Creative-step and per-request token safeguards
are unchanged; cumulative limits include reference and planning recovery capacity.
New runs freeze this policy in their engine snapshot; existing runs continue using
their original snapshot and budgets.

## Stop Conditions

Stop before creative generation for engine conflict, mutable/missing brief, failing
preflight, missing deterministic inputs, insufficient model limits, candidate-
selection logic, or forbidden phase writes. During the run, stop as
`PAUSED_GENERATION` for correctable uncommitted provider/schema/build trouble, or
`FAILED_GENERATION` for irrecoverable committed-history corruption and hard-budget exhaustion.

Do not stop for ordinary fictional choices. They belong to autonomous generation.
