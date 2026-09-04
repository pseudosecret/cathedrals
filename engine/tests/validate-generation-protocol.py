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
        "genesisFoundation",
        "genesisCast",
        "genesisConstraints",
        "architectureCore",
        "architecturePlanBatch",
        "creativePacket",
        "constraintEvent",
        "prospectivePlan",
        "ledgerEntry",
        "finalization",
    )
}
assert len(record_types) == 11
assert schema["$defs"]["runManifest"]["properties"]["protocol_version"]["const"] == "6.0"
engine_snapshot = schema["$defs"]["runManifest"]["properties"]["engine_snapshot"]
assert "path" in engine_snapshot["required"]
assert set(engine_snapshot["properties"]) == {"work_id", "path", "work_seed", "structural_seed", "geomancy_seed"}
assert "web_art_direction" in schema["$defs"]["genesisFoundation"]["required"]
assert schema["$defs"]["genesisFoundation"]["properties"]["web_art_direction"]["$ref"] == "#/$defs/webArtDirection"
assert schema["$defs"]["architecturePlanBatch"]["properties"]["packet_plans"]["maxItems"] == 8
architecture_node = schema["$defs"]["architectureNode"]
assert "generation_dependency_ids" not in architecture_node["required"]
assert "generation_dependency_ids" not in architecture_node["properties"]
assert schema["$defs"]["genesisConstraintDelta"]["properties"]["canonical_facts"]["maxItems"] == 12
assert schema["$defs"]["genesisConstraintDelta"]["properties"]["knowledge_changes"]["maxItems"] == 24
assert schema["$defs"]["genesisFoundationPayload"]["properties"]["claimant_anchors"]["minItems"] == 5
assert schema["$defs"]["genesisFoundationPayload"]["properties"]["claimant_anchors"]["maxItems"] == 8
assert schema["$defs"]["genesisConstraints"]["properties"]["claimant_extensions"]["maxItems"] == 7
assert "technical_slot_id" in schema["$defs"]["character"]["required"]
assert schema["$defs"]["canonicalFact"]["properties"]["sources"]["maxItems"] == 24
assert schema["$defs"]["constraintEvent"]["properties"]["sources"]["maxItems"] == 24
assert "maxLength" not in schema["$defs"]["scene"]["properties"]["prose_mdx"]
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
claimant = schema["$defs"]["claimant"]
for anchor_field in ("technical_slot_id", "name", "incident_role"):
    assert anchor_field not in claimant["required"]
    assert anchor_field not in claimant["properties"]
assert claimant["additionalProperties"] is False

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
