# Source-Grounded Index Instruction

This is a non-creative analysis call. Return exactly one `index_batch` conforming to
the supplied frozen protocol definitions.

Extract only canonical-state or narrative-working-memory observations directly
supported by the supplied immutable sources. Cite artifact type, artifact ID, and
exact locator for every proposition. Preserve ambiguity and intentional
contradictions. Do not invent connective facts, resolve uncertainty without evidence,
write fiction, critique prose, suggest revisions, or treat a prior summary as stronger
than original source evidence.

If an existing index record is wrong, emit a `correct_index` observation that
supersedes the index record. Never alter or override the immutable creative source.

IMMUTABLE SOURCES BEGIN

{{INDEX_SOURCE_CONTEXT}}

IMMUTABLE SOURCES END

EXISTING RELEVANT MEMORY BEGIN

{{EXISTING_MEMORY_CONTEXT}}

EXISTING RELEVANT MEMORY END

RELEVANT PROTOCOL DEFINITIONS BEGIN

{{INDEX_PROTOCOL_DEFINITIONS}}

RELEVANT PROTOCOL DEFINITIONS END

Return the one index batch now.
