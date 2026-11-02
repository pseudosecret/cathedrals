# Packet context capacity correction

The saved run `cathedrals_20261101_203738_0272a8` paused before its first literary
request. Its required context was estimated at 75,997 tokens against a 35,152-token
body allowance. No literary response had been requested for that packet.

## Causes and behavior

Eight prerequisite citations expanded into three entire Genesis records repeatedly:
one foundation, one cast, and one constraint record. The merged Genesis view was
also present. The prerequisite section alone contained 139,497 characters. The
packet carried 92,782 characters of engine instructions, including development
milestones and instructions for other phases. Finally, the assembler subtracted a
fixed 14,000-token overhead allowance from the frozen 49,152-token input ceiling.

The corrected engine supplies complete original Genesis records once in SHARED
SOURCE RECORDS. Root-canon and prerequisite roles reference those exact objects with
`$context_ref`. Each citation keeps its own source ID, locator, owner commit, hash,
and JSON Pointer. Matching identity with conflicting payloads is an integrity error.
The original records remain authoritative, checksum-verified archives. The merged
Genesis view still supports internal entity lookup.

Packet instructions keep the complete ontology, style, arc grammar, claimant/state
rules, constitution, branching contract, and web law. The work-instance profile keeps
all sections from `authorship_boundary` through `state_logic_profile`, plus `scope`,
`format_selection`, `generation_run`, `validation`, `complete_work_barrier`, and
`generated_output_integrity`. The workflow profile keeps its Invariant, Commit
Semantics, Prospective Foreclosure, Complete-Work Barrier, and Human Escalation.
Selected sections are exact frozen text, not model-written summaries.

Normalization retains instructions, ontology, the state model, and work-instance
authorship/generation/validation/output-integrity sections. Complete source records,
the immutable artistic payload, required obligations, citations, and current state
remain available. The analysis prompt need not repeat the packet's style and
unrelated workflow instructions.

The engine measures the rendered prompt instructions, execution envelope, and schema
before packing. It estimates packet input as UTF-8 bytes/3, matching analysis, while
keeping the frozen input ceiling. The model window independently reserves output and
safety space. Correction feedback is checked before another request. Optional units
can be omitted whole; required overflow still pauses before provider access.

Receipts identify instruction file hashes and selected sections, measured overhead,
shared-source coverage, saved payload bytes, and component sizes. Diagnostics count
each shared source payload once and separate it from its role references.

## Read-only verification against the saved run

The new assembler was evaluated using the paused run's frozen inputs and committed
records. SQLite was opened read-only, receipt writes were intercepted, and provider
calls and other writes were blocked. Hashes of the manifest, ledger, run state,
database, constraint stream, frozen launcher, and existing staging files matched
before and after.

| Measurement | Result |
| --- | ---: |
| Frozen prepared-input ceiling | 49,152 estimated tokens |
| Measured prompt overhead | 4,784 estimated tokens |
| Available context body | 44,368 estimated tokens |
| Packed context body | 44,328 estimated tokens |
| Complete writing prompt, including system text | 49,112 estimated tokens |
| Normalization with 1,200 synthetic placeholder words | 37,548 estimated tokens |
| Shared source units, including optional discoveries | 6 |
| Source-role references | 14 |
| Repeated compact source payload avoided | 137,148 bytes |
| Original Genesis records, each displayed exactly once | 3 |
| Provider calls | 0 |

These are serialization-based estimates, not measured model-token usage. The
normalization payload is synthetic; no new fiction was generated. Future packets
with genuinely larger mandatory evidence can still exceed capacity and pause.

The [capacity regression suite](../tests/test_packet_context_capacity.py) recreates
the sizes and citation pattern with synthetic data. It verifies field/role
round-tripping, exact frozen instruction sections and hashes, source tampering,
conflicting identities, Unicode byte estimates, optional overflow, correction
feedback, output/safety reserves, and writing plus initial/paged normalization.
The existing FTS5 suite retains predecessor overflow, saved-writing receipts, and
index-rebuild coverage; the complete integration run checks real commit/publication
paths with synthetic provider responses.

The full offline suite passed **241 tests**, including the complete 20-scene
integration run. The generation-protocol validator and the 150-scene storage/search
smoke rehearsal passed. No live model generation was used for validation.

## Selected-model capacity and rollout

The earlier 23,308-token Genesis rejection had a separate cause: the selected model
was running with an 8,192-token context, while preflight could accept another loaded
model's 80,384-token capacity. Preflight now requires the selected unique instance's
actual `config.context_length`. It rejects unloaded, undersized, ambiguous, or
unmeasurable instances and does not use a model's theoretical maximum. These fields
are distinguished in [LM Studio's model-list documentation](https://lmstudio.ai/docs/developer/rest/list).

Streamed context refusals preserve the complete provider error and report the
requested and available capacities at the `LM Studio context capacity` stage. They
retain the existing diagnostic/attempt preservation path and pause after one attempt.

Changes apply to `foundation` and new engine snapshots. The paused `attempt` run,
committed work, and original snapshot remain unchanged. A fresh clone/new generation
uses the fix; resuming the existing run continues using its frozen implementation.
