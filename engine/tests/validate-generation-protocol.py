#!/usr/bin/env python3
"""Small stdlib check for the append-only engine contract."""

import json
from pathlib import Path


ROOT = Path(__file__).parents[2]
ENGINE = ROOT / "engine"
SCHEMA = ENGINE / "data/generation-protocol.schema.json"


def resolve_pointer(document, pointer):
    value = document
    for part in pointer.removeprefix("#/").split("/"):
        value = value[part.replace("~1", "/").replace("~0", "~")]
    return value


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


schema = json.loads(SCHEMA.read_text())
for node in walk(schema):
    ref = node.get("$ref")
    if ref and ref.startswith("#/"):
        resolve_pointer(schema, ref)

record_types = {
    schema["$defs"][name]["properties"]["record_type"]["const"]
    for name in (
        "runManifest",
        "genesis",
        "architecture",
        "creativePacket",
        "constraintEvent",
        "prospectivePlan",
        "ledgerEntry",
        "finalization",
    )
}
assert len(record_types) == 8
assert schema["$defs"]["runManifest"]["properties"]["protocol_version"]["const"] == "3.0"
assert {"engine_base_branch", "engine_base_commit"} <= set(
    schema["$defs"]["runManifest"]["properties"]["engine_snapshot"]["required"]
)
assert "web_art_direction" in schema["$defs"]["genesis"]["required"]
assert schema["$defs"]["genesis"]["properties"]["web_art_direction"]["$ref"] == "#/$defs/webArtDirection"
assert schema["$defs"]["decisionEdge"]["required"] == [
    "edge_id",
    "from_content_id",
    "destination",
    "label",
    "kind",
    "availability",
    "decision_group_id",
    "major_decision",
    "state_conditions",
    "state_effects",
]
assert "to_content_id" not in schema["$defs"]["decisionEdge"]["properties"]
assert schema["$defs"]["destinationRef"]["properties"]["kind"]["enum"] == ["technical_slot", "content"]
assert schema["$defs"]["claimant"]["properties"]["technical_slot_id"]["enum"] == [
    f"claimant_slot_{number:02d}" for number in range(1, 6)
]

work_instance = (ENGINE / "data/work-instance.yaml").read_text()
for invariant in (
    "human_creative_interventions_required: 0",
    "committed_creative_rewrites_allowed: false",
    "committed_creative_regeneration_allowed: false",
    "backward_canon_mutation_allowed: false",
    "candidate_cherry_picking_allowed: false",
    "append_only: true",
    "creative_authorship_forward_only: true",
    "planning_may_reason_backward: true",
    "The frozen possible_scene_count supplied by the user is the primary run-level",
):
    assert invariant in work_instance

for phase_gate_rule in (
    "current_phase: engine_revision",
    "allowed_write_roots:\n    - engine\n    - cathedrals",
    "Files listed by an active milestone are required minimum outputs and audit records, not the exclusive set of authorized engine files.",
    "without requiring a new milestone or per-file allow-list update",
    "target_outputs_do_not_limit_followup_files: true",
    "exclusive_write_allowlist: false",
    "- generated-work",
):
    assert phase_gate_rule in work_instance
assert "allowed_write_files:" not in work_instance

assert not (ENGINE / "data/generation-bundle.schema.json").exists()
assert not (ENGINE / "prompts/single-transaction-generation.md").exists()
assert (ENGINE / "formats/web.md").exists()
assert "deferred" in (ENGINE / "formats/visualnovel.md").read_text().lower()

stale_terms = (
    "creative_transaction_count",
    "generation-bundle.schema.json",
    "single-transaction-generation.md",
    "one_transaction_32k",
)
for path in ENGINE.rglob("*"):
    if path.is_file() and path.suffix in {".md", ".yaml", ".json"}:
        if path.name == "first-spike-freeze.md":
            continue
        text = path.read_text()
        assert not any(term in text for term in stale_terms), path

print("append-only generation protocol: valid")
