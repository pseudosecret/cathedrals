# Evidence resolution after Architecture

Run `cathedrals_20261103_153817_b76bb4` committed Architecture and failed while preparing its first literary packet. An obligation cited `fact_4448656f7d387136` with the descriptive locator `/chronology/002`. The old resolver treated that locator as a JSON Pointer into its Genesis constraints record. The actual chain is the fact at `/constraint_delta/canonical_facts/6`, followed by its source `chronology_event_002` at `/work_canon/chronology/1` in the foundation record.

The registered artifact ID now determines the owner and complete source unit. `source_locator` remains a descriptive citation. Engine-created precise citations carry a separate optional `record_pointer`; it is excluded from model response schemas. Existing engine-created Genesis commit citations using canonical paths remain supported. A specific unit ID cannot use a pointer into another unit, even within the same archive.

Evidence retrieval verifies the archive hash and any declared owner/hash, then follows both `sources` and `evidence_sources` iteratively. Facts, knowledge changes, obligations and updates, motifs, foreclosures, chronology events, topology, plans and literary units resolve through the same unit map. Cycles, missing proof and invalid pointers fail explicitly. Pointer diagnostics include the source ID, owner, record type, pointer, resolved prefix, archive path, referring record and original locator.

New records undergo evidence validation before commitment. Architecture is followed by a complete evidence audit before the first literary retrieval request. The `get_records` tool can also read registered IDs without individual FTS documents, including chronology events. No index migration or new dependency is required.

## Follow-on capacity failure

An offline replay using the failed packet's exact assignment and saved retrieval session exposed another pause: mandatory inputs plus all nineteen tool-discovered units required approximately 44,871 context tokens against a 44,290-token context allowance. Tool discovery now competes for optional space, ahead of automatic search results. Required sources and their provenance remain mandatory. Packing preserves complete units, records omissions, and reserves available room for correction feedback before adding optional history.

With these fixes, the same saved first-packet assignment prepares an estimated 40,548-token request against the frozen 49,152-token input ceiling. This is an offline preparation check with the failed run's frozen instructions, not a new literary generation or a guarantee of later completion.

The failed archive's evidence audit resolves twenty-one complete units. Hashes of forty-three original archive, manifest and state files were unchanged by that read-only audit. Regression tests cover the reported chain, mixed locators, strict pointers, indexed reads, invalid precommit references, cycles, long chains, hash mismatches, retrieval limits and optional context overflow. The complete engine suite includes the synthetic publication rehearsal.

Changes apply to subsequent runs using the updated foundation. The original terminal run, its frozen launcher, committed writing and diagnostic responses are preserved.
