# Engine cleanup

Implemented in `foundation` during `engine_revision`. No attempt directory, real run
archive, generated fiction or downstream site was changed. No dependencies were added.

## Reduction

Counts compare the starting Git revision with the completed cleanup. Test counts
include all Python files under `engine/tests`, including the new policy/resume tests.

| Python source | Before | After | Net reduction |
| --- | ---: | ---: | ---: |
| Production launcher | 11,975 lines | 10,448 lines | 1,527 lines (12.8%) |
| Tests and fixture utilities | 9,645 lines | 8,802 lines | 843 lines |

Forty obsolete launcher functions were removed. Documentation and retired prompts
are excluded from these code totals. Code was deleted or simplified rather than
moved into new runtime modules.

## Current behavior

- New runs always use bounded macro planning, scoped context, completion contract 1
  and scaffold planner 2. Contracts, per-predecessor connections, focused amendments,
  source audits and immutable checkpoints remain active.
- Removed allocation-first packet planning, whole-map navigation repair, scaffold
  version 1 response handling, bulk-draft bookkeeping and unused artistic review calls.
  Current field/batch and semantic recovery remain intact.
- Older runs dispatch their saved launcher before current policy validation. Missing
  snapshot machinery stops resume without finalizing or modifying the original run.
- Publication has one dependency-free static HTML path. Astro templates, package
  setup, Node downloads and optional build/restore loops were removed. Projection
  metadata says `static_html`; the required finalization field `npm_enhancement`
  truthfully says `NOT_RUN` without adding a warning. Artistic review status remains
  separate from the mechanical publication gates.
- SQLite/FTS5, immutable archives, exact source exports, append-only history,
  context ceilings, hard prerequisite/guarantee audits and complete publication
  checks remain in place.

The acceptance run also exposed an ending-schema mismatch: an outcome could have no
prerequisites while its committed ending required a nonempty satisfied list. The
list can now be empty when the outcome declares none. The existing validator still
requires the exact declared prerequisite set and supported satisfaction of every
member.

## Retired files

These prompts belonged to replaced response interfaces. Older snapshots retain
their own copies:

- `engine/prompts/generation-architecture.md`
- `engine/prompts/generation-architecture-plan-batch.md`
- `engine/prompts/generation-scaffold.md`

Current declarations, connections, reviews and audits use their separate scaffold
prompts. Active operator, workflow, build and repository contracts were updated.
Historical milestone notes remain historical.

## Verification

The starting suite had 351 tests and 15 errors, chiefly stale run fixtures. Tests for
removed interfaces were retired; retained tests now use current policy/contract
fixtures and isolate the layer they test.

Final verification: **317 tests passed, zero failures or errors**, with socket
connections and unmocked URL requests blocked. Coverage includes:

- Current scaffold generation from Genesis through `READY_TO_PLAY`, with 30 scenes,
  five endings, exact token accounting and complete static publication.
- Interruption after a durable packet, resume without duplicate authorship, unchanged
  committed archive bytes and an unchanged ledger prefix.
- 100/150-scene reader fixtures, source-byte preservation, rendered prose, assets,
  local links and missing-output detection.
- Iterative 5,000-scene graph validation; mixed branches, linear chapters, merges,
  capacity bounds and scoped evidence audits.
- SQLite recovery/replay/corruption, FTS5 retrieval, semantic/reference recovery,
  frozen snapshot dispatch and missing-snapshot protection.

`validate-generation-protocol.py`, Python syntax, JSON parsing, allowed write paths
and `git diff --check` also passed.

No live LM Studio generation, browser session, or 5,000-scene literary generation
was run. There is no measured live-model token or speed improvement claim. Display
Markdown retains the existing small static renderer; exact Markdown source bytes
remain available in the publication exports. This cleanup does not establish live
model reliability or literary quality.
