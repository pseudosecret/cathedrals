# Packet dependencies and retrieval overhead

The inspected 30-scene acceptance run paused with the first literary packet depending on itself and the next packet. There was no earlier packet ID to substitute. Several later packet plans also contained self references. Genesis remained committed, the architecture core was staged, and no scenes had been written.

Architecture retrieval made 23 calls with 490,793 input tokens; authoring made 15 calls with 307,382 input tokens. Retrieval was being given the full authoring prompt before most writing and metadata-repair calls. These observations describe the frozen acceptance run, not a live benchmark of the following changes.

## Dependency rules

Every allocated packet gets its own schema variant. The first packet permits only an empty dependency list. Later packets may name only earlier packets, including earlier batches supplied by the coordinator. Authoring batches use these record-specific schemas before generation; a general identifier-list schema no longer stands in for a packet's actual dependency domain.

Recovery operates on a complete invalid dependency list. The engine constructs the first packet's forced empty list without sampling. For later packets, the model can remove or replace illegal IDs, including returning an empty list when appropriate. A validator requires already-valid earlier prerequisites to remain. Other accepted plan fields are preserved. Before/after dependency lists are recorded in the planning checkpoint. Narrative obligations and their evidence requirements are unchanged.

## Retrieval rules

Retrieval receives a task descriptor and optional catalog of at most 2,048 estimated tokens. Catalog titles are metadata previews; catalog omissions are marked and search remains available. Frozen law, the complete writing assignment, response schema, canon and mandatory evidence stay in the authoring context. They are not copied into the retrieval request.

Record-group authoring opts into retrieval explicitly. Layout selection and schema-only field repairs do not automatically start another retrieval conversation. All allocated IDs in the group are described together, allowing related batches to share optional results.

The shared cache is scoped to a planning group, committed canonical-state hash, and semantic revisions of upstream planning records. Other groups in the same planning checkpoint also participate in invalidation. A retrieved tentative item is compared with its current checkpoint payload before reuse; bookkeeping-only revision changes refresh its provenance without another model call. Modified or missing items invalidate the cache. Committed sources are read and hash-verified again, and cached constraint events are compared with the indexed events.

Each authoring task still gets its own immutable retrieval-session record. Reused sessions link to the originating session and add no model calls or duplicate usage. Existing per-task working sets remain stable for resume. Shared caches are derived staging files, not new storage authority.

A successful direct read can finish retrieval after one round. Search hits stay in the tool conversation rather than consuming the 24 complete-source slots; a second round can fetch the discovered sources. The existing two-round, eight-call, 24-source and 12,288-token limits remain. Hyphenated source IDs such as `cathedrals-v01` are accepted by the typed read API; SQL remains parameterized and unavailable to the model.

## Verification

`test_planning_dependencies_retrieval.py` and `fixtures/packet-dependency-self-reference.json` cover the saved failure, first-attempt schemas, retained prerequisites, empty lists, small retrieval requests, shared-call accounting, cache invalidation, and search followed by a complete read. Existing Genesis, streaming, provenance, context-capacity, recovery and synthetic 30-scene publication tests remain part of the full suite.

No paused run or frozen snapshot was modified, and no live generation was restarted for this work. Reduced request sizes and fewer retrieval calls are verified offline; live end-to-end timing and token savings remain to be measured on a subsequent run.
