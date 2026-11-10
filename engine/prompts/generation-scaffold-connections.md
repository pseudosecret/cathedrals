# Connect a declared predecessor

Select only supplied successor interfaces. Do not author new node, case, requirement,
or guarantee IDs. The engine has assigned all IDs and ownership.
The assignment fixes every destination and entry case. Bind evidence for all of
them; do not add or omit targets or switch to another case to evade a prerequisite.
If the assignment cannot be earned by this contract, report contract_issue so the
engine can repair or locally re-declare the uncommitted predecessor.

Return connections keyed by destination node ID. Choose that destination's exact
entry_case_id. For its supports object, fill every supplied requirement key once.
Each evidence_ids array must contain at least one supplied predecessor guarantee ID
or a valid Genesis source ID. Explain why it supports the requirement. A guarantee
ID belongs inside evidence_ids; it never replaces a requirement key. Do not use the
predecessor's entry-case ID as the destination's case ID. No missing prerequisites,
unsupported evidence, or invented future facts are permitted.

One destination is a linear chapter continuation. Two to five destinations are a
branch. Several predecessors may enter one successor when their chosen cases are
supported. Every selected successor already exists or was declared earlier in this
batch's backward order; cycles cannot be added. A destination occurs only once. Connections fixed by the supplied schema are
already accepted; preserve their complete values, including evidence and reasons.

If the declared contract lacks a guarantee, entry condition or other field necessary
for any earned connection, return contract_issue identifying ONLY the deficient
contract fields and reason. Do not fabricate evidence to pass the schema. This
requests a focused amendment to uncommitted planning, preserving other contracts.

LOCAL PLANNING CONTEXT

{{SCAFFOLD_CONTEXT}}
