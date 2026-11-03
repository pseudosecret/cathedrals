# Genesis reference prevention

The inspected acceptance run spent approximately 43 minutes on 192 individual source-reference lookups: 96 source fields and 96 relevance fields. Its reference outputs contained 66,111 tokens, including 63,178 reasoning tokens. These are observations from the saved run, not a benchmark of this change.

The model cited canon sections and chronology events. The schema allowed arbitrary identifier strings, while validation accepted only claimant and character slots. A generic per-field repair pass ran before the existing grouped Genesis repair. Subsequent complete-payload retries repeated many of those repairs.

## New-run behavior

`genesis_source_catalog` supplies exact handles for global canon sections, chronology events, composition law, claimant anchors, complete claimant profiles and supporting characters. Each handle binds an existing artifact ID and a JSON Pointer into its immutable source record. A profile citation points to the cast profile rather than its shorter foundation anchor. The catalog is derived from committed records; it introduces no storage authority or database migration.

The response schema enumerates source handles, knowledge subjects, supported fact aliases and reference tags. Architecture tags must be empty during Genesis. The initial request permits at most twelve fact positions, matching the twelve-distinct-fact invariant and preventing an overlarge initial extraction from triggering another complete request. The semantic builder still coalesces equivalent supplied facts and preserves their evidence.

The wire schema leaves `relevance.technical_slot_ids` empty. The engine derives the direct-source tag and preserves any additional supplied valid source tags. Existing fact-position aliases and subject-slot aliases normalize deterministically. No semantic mapping is inferred from a merely similar label.

Genesis bypasses the generic per-field repair pass. After shape validation, its original extraction and API response are preserved before focused reference repair. The grouped resolver shares a decision only across equivalent uses with the same semantic record context. Equal invalid strings in different contexts remain independent decisions. Up to four ambiguous references are requested together, and both direct citations and duplicate tags update together. Unsupported resolutions retain the explicit focused fallback; the engine does not invent a mapping.

Accepted batches live in `.staging/<step>.repair.json`. Stable issue identities, saved API responses and deduplicated history preserve completed decisions across interruptions and count their usage once. A later canonical or precommit validation error pauses with the original payload and checkpoints intact; it does not request the whole extraction again. Non-reference schema failures before preservation retain the existing bounded correction path.

Source retrieval verifies the archived record hash before extracting each cited complete JSON unit. Several canon fields from the same commit retain separate pointers. Missing pointers and modified archives fail explicitly.

## Verification

`test_genesis_reference_prevention.py` checks closed source domains, zero-repair canon/profile extraction, complete hash-bound evidence, context-sensitive batching, pause/resume, original-payload preservation, exact usage accounting, bad pointers and archive tampering. Existing Genesis promotion and proposition-repair regressions remain in `test_cathedrals.py`. The complete suite includes the synthetic 30-scene publication rehearsal.

These changes apply to subsequent runs using the updated foundation. Existing run snapshots, model settings and committed writing are unchanged. No fresh live generation was started to test this change while the acceptance run continued in the background.
