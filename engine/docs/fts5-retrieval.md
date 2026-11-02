# FTS5 retrieval and scale rehearsal

Scene and ending generation now searches the whole committed work automatically.
The engine can recover a detail in old prose even if metadata extraction never
recorded it as a fact. This is SQLite full-text word search, using Python's existing
`sqlite3` dependency; it adds no service or model requests.

## Runtime behavior

The root [launcher](../../cathedrals) keeps the implementation in the existing
runtime structure. Schema version 2 of each generation's `state/index.sqlite3`
adds a document catalog, FTS5 postings, and indexed relevance relationships.

The corpus includes complete scenes, artifacts, endings, decision edges, formal
compositions, constraint descriptions, and descriptive Genesis/Architecture units.
Documents belong to a commit and JSON Pointer. This preserves multiple records about
the same claimant instead of overwriting one document with another. Technical IDs,
source hashes, and presentation settings do not supply ordinary search words.

Queries contain at most 32 unique literal terms/phrases, in order: explicit packet
keywords, resolved claimant/character names, then guidance words. Quoted terms are
joined with OR and passed as a bound SQL parameter. There is no query-authoring model
call. Empty queries still permit structural and recent-event retrieval.

FTS5 uses `unicode61`, with its default case folding and Latin-diacritic handling.
There is no stemming, synonym expansion, or prefix search. BM25 weights title/body
matches 2:1; overlapping relevance tags break ties, then archive sequence, commit,
and pointer stabilize ordering. These SQLite features are documented in the
[official FTS5 reference](https://www.sqlite.org/fts5.html).

Constraint candidates are bounded: up to 192 FTS matches, 192 structural matches,
and 96 recent events. The final optional selection keeps at most 96 events, using
existing structural weights plus a bounded FTS-rank bonus. Structural source and
obligation lookup remains independent of lexical matching.

The engine retains required narrative canon, the whole local plan and predecessor packets,
assigned obligations and prerequisite closure, their cited evidence, and selected
current state tied to that evidence. Required proof bypasses optional search limits.
Optional discovery permits up to 24 complete units within the frozen retrieval
allowance, then packs optional constraints, knowledge, history, motifs, recent prose,
and soft pressures into remaining context. New runs retain the existing 12,288-token
optional retrieval allowance and prepared-context ceiling.

Original source units come from checksum-verified archive records. JSON formatting
is compact; exact source payloads appear once in SHARED SOURCE RECORDS, and repeated
source-reference metadata can share objects in SHARED SOURCE METADATA. `$context_ref`
preserves every role while addressing a complete object. Genesis uses its three
original archives, with prerequisite citations pointing into that same shared pool.
Sharing requires matching owning commit, hash, pointer, and payload. Literary strings
stay complete and the local plan is displayed once. Required overflow pauses before
the provider call with shared payloads counted once; optional overflow omits complete
units and records why.

The later [packet-capacity correction](packet-context-capacity.md) adds phase-specific
instruction profiles and replaces the fixed 14,000-token overhead allowance with the
rendered instructions/schema size. Packet estimates now use conservative UTF-8 bytes/3,
matching analysis. The frozen input and retrieval ceilings remain unchanged. The
measurements below precede that correction and retain their original estimator.

Labels distinguish planned intentions, root canon, committed literary material,
composition metadata, and constraint history. Retracted/superseded history does not
become current knowledge. Retrieval itself does not prove branch applicability,
fictional chronology, reader knowledge, or whether a revelation feels earned.

## Durability and inspection

Catalog entries, FTS postings, relevance tags, and the ordinary state checkpoint are
updated in the same commit transaction. Archives remain authoritative. Startup and
recovery verify the catalog against archive extraction and run FTS integrity checking
against its external content. Missing, incompatible (including version 1), stale, or
damaged databases rebuild from verified history. Old frozen engine snapshots retain
their own implementation. Publication includes archived provenance, not SQLite.

Selection receipts live at:

- `.staging/<step>.retrieval.json`: current selection, including capacity failure.
- `raw/<step>-attempt<N>.retrieval.json`: immutable receipt for actual writing.
- `committed/<sequence>-<step>/retrieval-receipt.json`: hash-checked accepted receipt.

Receipts record query terms, state/checkpoint identity, candidate counts,
constraint ranks/scores, selected source IDs/hashes/pointers, omissions, context and
prompt hashes, and size estimates. They contain no prose. Saved writing restores its
original attempt receipt and checks that reconstructed context matches; it does not
request another creative response. No new CLI command is required.

## Recorded synthetic measurements

Environment: Python 3.12.12, SQLite 3.37.2, local filesystem, one coordinator.
The [benchmark](../tests/benchmark_storage.py) uses real commits with synthetic
packets, three constraint events per scene, periodic fact supersession and knowledge
retraction, and one deterministic audit entry per scene. There are no provider calls.
The 5,000-scene case has 15,000 events and 10,002 ledger entries.

```sh
python3 -B engine/tests/benchmark_storage.py --scenes 150 1000 5000 --timeout 0
```

The comparison runs the previous metadata scoring algorithm against the same SQL
store, then the indexed selector. The planted word appears only in scene 1's prose,
outside its extracted constraints. FTS ranks that scene first at every size; the
previous metadata selection does not select its original source.

| Scenes | Old scan, ms | Old events decoded | Indexed selection, ms | Indexed events decoded | Source search, ms |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 150 | 11.90 | 450 | 2.67 | 96 | 0.47 |
| 1,000 | 58.73 | 3,000 | 3.97 | 96 | 1.26 |
| 5,000 | 339.73 | 15,000 | 2.73 | 96 | 0.48 |

| Scenes | Commit seconds | Full audit, s | Deleted-index rebuild, s | Database bytes | Context assembly, ms | Context bytes |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 150 | 10.46 | 0.10 | 0.42 | 2,482,176 | 77.71 | 140,595 |
| 1,000 | 106.40 | 0.70 | 0.93 | 15,302,656 | 80.01 | 140,018 |
| 5,000 | 260.57 | 3.98 | 4.69 | 75,677,696 | 158.31 | 140,085 |

Each case matched pure full replay before audit and again after deleting/rebuilding
the database. Ordinary commits opened zero historical archive files under the Python
read counter used by the [earlier storage rehearsal](storage-benchmark.md). SQLite's
own I/O is excluded. Overlapping checks affected timings, especially the 1,000-scene
commit run; these samples are observations, not hardware-independent thresholds.

A separate fixed-coverage fixture holds the same 24 required events and synthetic
law constant. Compact formatting and shared source metadata reduce 19,725 bytes to
14,150 bytes, about 28%. This is a byte measurement, not measured model-token or
inference-cost savings. Full-context measurements include the real frozen engine law
but use minimal synthetic Genesis and no geomancy; they do not demonstrate a full
5,000-scene planner or narrative.

## Validation and limits

The full offline suite passed **230 tests**, including 15 focused FTS5 tests and the
20-scene integration run through publication. The generation-protocol validator
passed. Tests cover literal/Unicode queries, distant unextracted prose, deterministic
ranking/rebuild, complete source bytes, corpus coverage, repeated claimant IDs,
lossless compaction, required overflow before provider access, optional omissions,
retraction labels, tampering, transaction rollback, and saved receipt replay.

FTS5 must be compiled into Python's SQLite build; initialization pauses with the
SQLite error if unavailable. Lexical search can miss paraphrases, and bounded optional
selection can omit relevant material. Explicit dependencies must therefore remain
declared and directly retrieved. Actual local-model token usage, literary quality,
semantic search, conditional knowledge analysis, progressive planning changes, and
prospective literary assessments were not tested or implemented by this FTS5 change.
