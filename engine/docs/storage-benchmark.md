# Incremental SQLite storage rehearsal

This records the initial storage migration before FTS5. Current retrieval behavior
and the later schema-version-2 measurements are in [FTS5 retrieval](fts5-retrieval.md).

The SQLite commit path updates affected rows without rereading historical archive
files. A 5,000-scene synthetic history completed, matched full replay, and rebuilt
successfully after database deletion. This measures storage, not literary quality or
full-scale narrative planning.

## Workload and reproduction

Environment: Python 3.12.12, SQLite 3.37.2, local filesystem, one writer. Each scene
uses the real `commit_record` path with a schema-valid synthetic packet, one fact,
one knowledge event, and one motif event. Facts periodically supersede earlier facts;
knowledge is periodically retracted. Each scene also appends a deterministic audit
step. The 5,000-scene case produces 15,000 events and 10,002 ledger entries, exercising
numeric directory ordering above sequence 9,999. There are no provider requests.

Run [the benchmark](../tests/benchmark_storage.py):

```sh
python3 -B engine/tests/benchmark_storage.py --timeout 0
```

Use `--scenes 150` for a short run. The default timeout is 60 seconds per size;
timeouts are reported explicitly. `--launcher /path/to/saved/launcher` measures a
saved launcher revision against the same checkout's engine inputs. Runs and database
files are temporary; the benchmark does not generate or publish a literary work.

## First completed rehearsal

Times are wall seconds, excluding initial run creation and model inference. The
original launcher (revision `e4b2ecb`) was preserved before migration. Its larger cases were stopped at
the agreed 60-second cutoff; no completion times are extrapolated.

| Scenes | Original commits | SQLite commits | Full audit | Deleted-index rebuild | Database bytes |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 150 | 22.79 | 8.53 | 0.10 | 0.21 | 2,097,152 |
| 1,000 | cutoff at 60 | 53.14 | 0.63 | 0.77 | 13,266,944 |
| 5,000 | cutoff at 60 | 351.23 | 3.85 | 4.40 | 65,789,952 |

The first and last 100-scene batches in the completed 1,000-scene case took 5.14 and
5.25 seconds. Repeated runs varied with overlapping checks; these samples are not
hardware-independent performance thresholds.

## Instrumented verification

The instrumented benchmark compares state with pure full replay **before** running
the archive audit, then checks it again after audit and after rebuilding a deleted
database. This prevents recovery from masking an incremental projection error.

| Scenes / launcher | Commit seconds | Python archive opens during commits | Archive bytes opened |
| --- | ---: | ---: | ---: |
| 150 / original | 31.64 | 125,772 | 607,493,277 |
| 150 / SQLite | 10.52 | 0 | 0 |
| 1,000 / SQLite | 115.08 | 0 | 0 |
| 5,000 / SQLite | 264.94 | 0 | 0 |

The final instrumented 5,000-scene run passed the comparison before audit and
after deleting/rebuilding SQLite. Its full audit took 3.61 seconds, rebuild took
3.84 seconds, and database size was 65,769,472 bytes.

The archive counter observes Python `Path.open` reads of committed records, ledger,
constraints, and planning history. Bytes are the sizes of the complete files opened
by those reads, rather than physical disk traffic. SQLite's internal reads/writes,
engine inputs, and the small run-status checkpoint are excluded. The full audit
intentionally reads archived history outside the timed commit interval.

## Acceptance and limits

The full offline suite passed **215 tests**, including the complete 20-scene
integration run. The generation-protocol validator passed. The
[SQLite recovery suite](../tests/test_sqlite_state.py) covers transactional rollback,
orphaned commits, exact partial append recovery, interrupted prospective planning,
missing/corrupt/incompatible/foreign/stale indexes, source tampering, truncated
ledger history, duplicate commits, accounting, and direct evidence lookup.

The planning timing is an empty-plan history scan, not a rehearsal of thousands of
interacting obligations or routes. At this migration's checkpoint, context ranking
and prospective scheduling retained their existing algorithms and could still scan
growing working sets. Recovery drafts and run-status checkpoints kept their existing
file formats. FTS was deferred here and was subsequently implemented in the linked
retrieval follow-up. Embeddings, Hindsight, broader state migration, and literary
assessments were outside this storage rehearsal.
