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

## SQLite State

New generations initialize `.cathedrals/runs/<generation-id>/state/index.sqlite3`
automatically using Python's standard library. Resume reopens that generation's
database. There is no database server, installation step, or maintenance command.
Use one coordinator per generation. SQLite uses its rollback journal and durable
transactions; keep the run directory on a local filesystem.

The database maintains core facts, character knowledge, obligations, motifs,
foreclosure candidates, ID/source provenance, committed-record and ledger indexes,
usage totals, and the latest prospective plan. Archived JSON/JSONL and raw responses
remain the recovery source. `state/run-state.json` and incomplete planning/semantic
recovery drafts retain their existing file formats. Old frozen engine snapshots
retain their original storage implementation.

Startup/resume verifies archived bytes and compares SQLite with full replay. A
missing, corrupt, incompatible, foreign, or stale index is rebuilt into a temporary
database and replaced only after reconstruction succeeds. Repeated resume applies
each archived step once. Database write errors pause the run with durable progress
preserved. Archive integrity failures retain their existing failure behavior.
Incomplete ledger bytes are completed only when exact immutable commit metadata
justifies the suffix; unknown partial records are integrity failures.

Core projections are queried from SQLite. The former `state/canonical-facts.json`,
`knowledge-state.json`, `obligations.json`, `motifs.json`, `source-index.json`,
`foreclosure-candidates.json`, and `prospective-plan.json` files are no longer
operational inputs. Editing or seeding those files does not change live state.
Evidence retrieval resolves IDs through SQLite and checks the referenced original
record's hash before returning its passage. The database is omitted from static
publication; the reader remains entirely static.

Schema version 2 also maintains FTS5 full-text search automatically. Scene and ending
requests search committed literary units, constraint descriptions, and generated
Genesis/Architecture descriptions and plans. Search uses packet keywords, resolved
entity names, and guidance; there is no search CLI or extra model request. Python's
SQLite build must include FTS5. A missing FTS5 module pauses database initialization
with the SQLite error rather than silently disabling retrieval.

Required predecessor packets, assigned obligations, prerequisite chains, and their
proof cannot be omitted for search limits. If their complete compact context is too
large, the run pauses before a writing request, reporting required component sizes.
Optional search uses the frozen retrieval/prepared-context budgets and returns whole
units. Plans and historical constraints are labelled separately from committed events.

Inspect `.staging/<step>.retrieval.json` for the current selection or a capacity
failure. Actual attempts preserve `raw/<step>-attempt<N>.retrieval.json`; an accepted
packet archives `retrieval-receipt.json` with the other hashed supplemental files.
These contain selection metadata and hashes, not duplicate prose. Resume with saved
writing preserves its original receipt. Missing/incompatible/corrupt search indexes
follow the same verified-archive rebuild path as core state. Frozen snapshots retain
their own implementation. Details and measured limits are in
[FTS5 retrieval](fts5-retrieval.md).

Packet capacity checks use exact shared source records and phase-specific instruction
profiles from frozen engine inputs. The whole Genesis foundation, cast, and constraints
appear once; prerequisite references point to those objects. Narrative doctrine and
mechanics remain required. Development milestones and unrelated workflow instructions
are excluded from the packet profile. Normalization has its own extraction profile,
preserving complete artistic/source content and relevant state.

The engine measures prompt instructions/schema overhead and estimates packet input
as UTF-8 bytes/3. It keeps the frozen input ceiling and reserves output/safety space;
correction feedback is checked before another request. Capacity receipts count shared
source payloads once and report per-role reference overhead. See
[the packet-capacity regression](packet-context-capacity.md).

Model preflight requires the selected model's unique loaded instance and actual
`config.context_length`. It never uses another model's capacity or a theoretical
maximum. Load the intended model explicitly with at least 64,148 context tokens.
Ambiguous model keys require an exact instance ID. Streamed context rejections retain
the full provider error and show the `LM Studio context capacity` stage with the
actual requested and available token counts. They follow the existing incomplete-
response preservation path and do not trigger repeated automatic writing attempts.

These changes apply to new engine snapshots. Updating an installation does not
change a paused run's frozen launcher or inputs; test the corrected engine in a new
generation rather than editing archived snapshots or receipts.
When the installed launcher differs from the selected run's frozen launcher, resume
prints that distinction before handing control to the snapshot. This notice does
not upgrade the snapshot or alter the run.

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

Genesis uses an enumerated canon/entity source catalog and contextual repair batches
of up to four references. The engine derives direct-source tags and preserves accepted
metadata before later validation. See [genesis-reference-prevention.md](genesis-reference-prevention.md).

Invalid references in Architecture, packet plans, scenes, endings, and semantic metadata
receive automatic focused resolution. After deterministic
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
are included. Initial whole-core and plan-batch requests also render every required
section completely: law, canon, reference catalogs, allocations, prior IDs, and frozen
geomancy. Lists remain whole JSON arrays, including empty lists. Planning builders
never pack away sections or trailing records to meet an earlier size estimate; the
complete rendered request is checked by the conservative UTF-8 budget guard.
Completed setup instructions appear once in packet guidance. Their setup-history
entries use `instruction_ref` JSON Pointers into that same prompt only when the full
guidance matches exactly once. Pending, unmatched, or ambiguous instructions stay
complete; saved checkpoints retain every original instruction and its whitespace.

New runs freeze `max_planning_context_tokens` from the detected model window minus
the safety reserve and the existing 256-token minimum response allowance. Initial
Architecture drafts, recovery batches, and isolated planning values use this same
ceiling. Each request still allocates output within the smaller frozen/loaded model
window, preserving existing output caps and headroom fitting. For example, an
80,384-token window can fit a 49,255-token estimated prompt, 15,000 output tokens,
and the 4,096-token safety reserve. Other phases keep their 49,152 prepared-input
ceiling. Cumulative input headroom reflects the larger frozen planning allowance;
actual response usage remains charged exactly once.

Older manifests without the optional planning ceiling use their existing prepared
limit. Existing run snapshots and frozen manifests are not upgraded; use the updated
engine for a new generation. Increasing the loaded window alone does not change an
older run's frozen limits.

If complete compact context still exceeds the frozen prompt limit or
model capacity, planning enters `PAUSED_GENERATION`, preserving all accepted work.
The diagnostic reports prompt estimates, schema size, limits, and output/safety
reserves. No oversized request is sent and no authored context is silently clipped.

Focused string planning requests return a strict `{"value": "..."}` object instead
of an unconstrained string response. The field's enum/pattern and route validation
still apply after decoding. `$connect`, `$layout`, and similar path labels describe
engine operations; the model supplies the requested value, and the engine applies it.
Exact singleton wrappers from saved responses can be decoded without choosing new
content. A full topology/edge patch, alternatives, extra fields, or duplicate keys
cannot substitute for one value. Invalid answers retain the existing three-attempt
limit and pause behavior. Successful decoding preserves raw evidence and accounting.

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

Progress reports both accepted positions and distinct records. Truncated responses may
contain exact repeats; accepted fact positions remain stable, while prompts show each
repeated fact once and use `$fact_ref` aliases at its other positions. These aliases
are prompt references only, never new metadata or a change to source evidence.
When a valid continuation adds nothing and still claims more remains, the next request
audits category completion instead of repeating the extraction instruction. It must
return genuinely missing changes or explicitly declare completion. A valid page may
finish with already accepted items and `complete=true`; those items are not appended
again. A duplicate page with `complete=false` never silently completes a category.
The completion check survives pause/resume and preserves the same correction limits.

A truncated page retains its complete prefix and halves the next page size. A single
oversized record may use up to the frozen 15,000-token analysis ceiling when context
permits. Repeated pages that make no progress receive three correction attempts per
invocation, with accurate attempt counts. Interrupted streams pause immediately after
retaining complete records. Context capacity shortfalls pause without clipping source
content; other hard resource limits remain binding.

Progress lives in `.staging/<step>.semantic-recovery.json`; resume keeps accepted prose
and metadata and continues pending work. Canonical errors after paging correct only
the selected rejected category, preserving other categories and fact positions.
Complete responses with schema, reference, or canonical errors use this same recovery
path. Known error paths route directly to their categories; an opaque error uses the
bounded category selector. It uses a dedicated classification prompt and a strict
JSON object containing only the selected category, with up to 4,096 output tokens.
Correction state survives pause/resume, and successful
reference lookups remain cached. A failure in one category does not request a new
whole semantic delta. Full
schema, reference, and packet validation precedes final metadata staging. Commits
include the recovery checkpoint and response evidence; incomplete provider envelopes
are never used as completed metadata responses.

An existing obligation remains `active` until supported content resolves it; no
status update is needed merely to add evidence. Packet normalization allows only
`satisfied` and `intentionally_unresolved` updates, derived from the canonical
contract. The latter is a deliberate ambiguous resolution, not an open question.
An empty update array is valid. The engine never coerces `active` into a resolution;
foreclosure safeguards and the initial active state of new obligations remain intact.

An unavailable-knowledge conflict reports its exact scene, character, proposition,
and declaration index. It enters dependency recovery directly. Corrections may
change only flagged technical declarations on uncommitted scenes, with exact source
excerpts and valid existing IDs. The original scene, artifacts, and literary bytes
remain preserved. A genuine acquisition instead repairs knowledge metadata for the
exact subject/proposition and retires the prior negative relation. A genuine
contradiction pauses; the harness cannot invent learning or change prior canon.

Audited decisions and effective dependency overrides are saved in
.staging/<step>.epistemic-repair.json, bound to the original artistic hash. The
packet builder uses them consistently for validation and final construction.
Resume retains accepted decisions and metadata. The commit includes
epistemic-repair.json and its supplemental hash alongside the original artistic
payload. These changes apply to new engine snapshots; existing frozen runs remain
unchanged.

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

New runs use the bounded compiler and scoped source policy described in
[bounded-execution.md](bounded-execution.md). A synthetic preflight freezes native
tool retrieval or automatic fallback before fiction starts. Keep the same model
and reasoning settings when comparing runs. Phase progress includes input/output
and reasoning usage. A 30-scene synthetic publication and an actual Chromium
playthrough now supplement the existing offline validation checks.

Updated packet planning constrains each dependency list to earlier allocated packets;
the first packet has an empty list. Recovery preserves valid prerequisites and repairs
the complete invalid list. Optional retrieval receives a compact task/catalog request
and reuses results across related record batches, with semantic revision and source-hash
checks. See [planning-dependencies-retrieval.md](planning-dependencies-retrieval.md).
These installation changes do not update any existing frozen run.
