"""Source-grounded reference repairs and an offline uninterrupted generation rehearsal."""

import copy
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_cathedrals import (
    ROOT, RUNNER, architecture_core_payload, art_direction, claimant_expansion,
    genesis_foundation_fixture, genesis_cast_fixture, genesis_semantic_payload,
    packet_payload, packet_plan,
)


def api_response(value, *, text=False):
    return {"choices": [{"finish_reason": "stop", "message": {
        "content": value if text else json.dumps(value),
    }}], "usage": {"prompt_tokens": 11, "completion_tokens": 7}}


def planning_path(path):
    return [json.loads(quoted) if quoted else int(index) if index else name
            for name, index, quoted in re.findall(r'\.([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]|\[("[^\"]*")\]', path)]


def planning_response(request, resolve):
    prompt = request["messages"][1]["content"]
    schema = json.loads(prompt.split("VALUE SCHEMA\n", 1)[1].split("\nFULL ASSEMBLED", 1)[0])

    def project(value, node):
        node = RUNNER.planning_schema_node(node, schema)
        if isinstance(value, dict) and node.get("type") == "object":
            return {key: project(value[key], child) for key, child in node.get("properties", {}).items() if key in value}
        if isinstance(value, list) and "items" in node:
            return [project(item, node["items"]) for item in value]
        return value

    if "BATCH TARGETS\n" in prompt:
        targets = json.loads(prompt.split("BATCH TARGETS\n", 1)[1].split("\nVALUE SCHEMA", 1)[0])
        return api_response({item["key"]: project(resolve(planning_path(item["path"]),
            schema["properties"][item["key"]] | {"$defs": schema.get("$defs", {})}), schema["properties"][item["key"]]) for item in targets})
    path = prompt.split("FIELD PATH\n", 1)[1].split("\n", 1)[0]
    value = project(resolve(planning_path(path), schema), schema)
    return api_response(value, text=isinstance(value, str))


def foundation_payload():
    return {
        "format_composition_law": "Synthetic format fixture.",
        "claimant_anchors": [{"name": f"Synthetic claimant {index}", "incident_role": f"Synthetic role {index}"} for index in range(1, 6)],
        "web_art_direction": art_direction(),
        "work_canon": {
            "generated_title": "Synthetic reference rehearsal", "premise": "Synthetic premise.",
            "central_incident": {"event": "Synthetic event.", "subjects": ["claimant_01"],
                "circumstances": "Synthetic circumstances.", "culpability": "Synthetic ambiguity.", "competing_interpretations": []},
            "chronology": [{"relative_order": index, "event": f"Synthetic event {index}.", "certainty": "established"} for index in range(1, 4)],
            "claimant_relationships": [{"claimant_ids": ["claimant_01", f"claimant_{index:02d}"],
                "relationship": "Synthetic relationship.", "dramatic_pressure": "Synthetic pressure."} for index in range(2, 6)],
            "generated_motifs": [], "environmental_mutation_law": "Synthetic law.", "principal_tensions": [],
        },
    }


class ReferenceResolutionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", self.root / ".cathedrals"), mock.patch.object(
            RUNNER, "RUNS_ROOT", self.root / ".cathedrals/runs"
        ):
            self.run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=20), "http://offline.invalid", "offline", output_fn=lambda _: None)

    def records(self):
        foundation, cast = genesis_foundation_fixture(), genesis_cast_fixture()
        architecture = {"arcs": [{"arc_id": "arc_one", "purpose": "Synthetic arc."}],
            "attractors": [], "packet_plans": [packet_plan()]}
        return {"genesis_foundation": foundation, "genesis_cast": cast,
            "genesis": {"claimants": foundation["claimant_anchors"]}, "architecture": architecture}

    def test_exact_name_only_answers_retries_audit_and_context_scoped_cache(self):
        issue = {"path": ["knowledge_changes", 0, "proposition_id"], "kind": "proposition",
            "invalid": "fact_new_pencil_notation", "context": "A pencil notation appears on a receipt.",
            "candidates": {"fact_01": "Pencil notation.", "fact_02": "Seal shortage."}}
        transport = mock.Mock(side_effect=[api_response('"fact_01"', text=True),
            api_response("fact_01 because it matches", text=True), api_response("  fact_01\n", text=True)])
        answer = RUNNER.resolve_named_reference(self.run, "packet_one", issue, transport)
        self.assertEqual(answer, "fact_01")
        self.assertEqual(transport.call_count, 3)
        prompt = transport.call_args.args[2]["messages"][1]["content"]
        self.assertIn("fact_new_pencil_notation", prompt)
        self.assertIn("ONLY one exact identifier", prompt)
        self.assertNotIn("response_format", transport.call_args.args[2])
        before = {path: path.read_bytes() for path in (self.run / "raw").iterdir()}
        self.assertEqual(RUNNER.resolve_named_reference(self.run, "packet_one", issue, transport), "fact_01")
        self.assertEqual(transport.call_count, 3)
        changed = issue | {"context": "A seal shortage appears on another receipt."}
        with mock.patch.object(RUNNER, "http_json", side_effect=AssertionError("network")):
            self.assertEqual(RUNNER.resolve_named_reference(self.run, "packet_one", changed,
                lambda *_args, **_kwargs: api_response("fact_02", text=True)), "fact_02")
        for path, original in before.items():
            self.assertEqual(path.read_bytes(), original)
        entries = [entry for entry in RUNNER.ledger_entries(self.run) if entry["commit_status"] == "FAILED_BEFORE_COMMIT"]
        self.assertEqual(len(entries), 2)
        self.assertTrue(all(entry["failure_class"] == "malformed_response" for entry in entries))
        self.assertEqual(RUNNER.load_state(self.run)["input_tokens"], 44)

    def test_reasoning_fallback_accepts_only_an_entire_exact_reference_answer(self):
        response = {"choices": [{"message": {"content": "", "reasoning": " fact_01\n"}}]}
        self.assertEqual(RUNNER.normalize_provider_response(response, plain_answers={"fact_01"}), "fact_01")
        response["choices"][0]["message"]["reasoning"] = "I think the answer is fact_01"
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.normalize_provider_response(response, plain_answers={"fact_01"})

    def test_frozen_budget_stops_reference_request_before_contacting_provider(self):
        issue = {"path": ["target"], "kind": "source", "invalid": "missing", "context": "Synthetic use.",
            "candidates": {"source_one": "Synthetic source."}}
        read_json = RUNNER.read_json

        def constrained(path):
            value = read_json(path)
            if path == self.run / "run-manifest.json":
                value["budgets"]["max_cumulative_output_tokens"] = 0
            return value

        transport = mock.Mock()
        with mock.patch.object(RUNNER, "read_json", side_effect=constrained), self.assertRaises(RUNNER.CathedralsError) as raised:
            RUNNER.resolve_named_reference(self.run, "budget", issue, transport)
        self.assertEqual(raised.exception.failure_class, "budget_exhaustion")
        transport.assert_not_called()

    def test_unsupported_answers_and_empty_catalog_do_not_invent_targets(self):
        issue = {"path": ["target"], "kind": "source", "invalid": "missing", "context": "Synthetic use.", "candidates": {}}
        transport = mock.Mock()
        self.assertEqual(RUNNER.resolve_named_reference(self.run, "empty", issue, transport), "UNRESOLVED")
        transport.assert_not_called()
        issue["candidates"] = {"source_one": "Synthetic source."}
        self.assertEqual(RUNNER.resolve_named_reference(self.run, "unsupported", issue,
            lambda *_args, **_kwargs: api_response("UNRESOLVED", text=True)), "UNRESOLVED")
        with self.assertRaisesRegex(RUNNER.PausedError, "exhausted 3"):
            RUNNER.resolve_named_reference(self.run, "invalid", issue,
                lambda *_args, **_kwargs: api_response("invented_again", text=True))

    def test_schema_enum_references_are_repaired_before_strict_validation(self):
        payload = foundation_payload()
        payload["work_canon"]["central_incident"]["subjects"] = ["unknown_claimant"]
        schema = RUNNER.genesis_foundation_schema(self.run)
        original = copy.deepcopy(payload)
        repaired = RUNNER.repair_named_references(self.run, "foundation", payload,
            "genesisFoundationPayload", schema, lambda *_args, **_kwargs: api_response("claimant_01", text=True))
        RUNNER.validate_json_schema(repaired, schema)
        self.assertEqual(repaired["work_canon"]["central_incident"]["subjects"], ["claimant_01"])
        self.assertEqual(payload, original)
        payload["work_canon"]["premise"] = 42
        transport = mock.Mock()
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.repair_named_references(self.run, "bad_shape", payload, "genesisFoundationPayload", schema, transport)
        transport.assert_not_called()

    def test_inventory_covers_cast_architecture_plans_and_literary_references(self):
        records = self.records()
        with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records.get(kind)):
            cast = {"claimants": [claimant_expansion("missing_claimant")], "characters": []}
            self.assertEqual(RUNNER.named_reference_issues(self.run, cast, "genesisCastPayload")[0]["kind"], "claimant")
            core = architecture_core_payload()
            core["topology"]["edges"][0]["to_node_id"] = "missing_node"
            core["arcs"][0]["claimant_pressures"] = ["missing_claimant"]
            with mock.patch.object(RUNNER, "architecture_id_catalog", return_value={}):
                issues = RUNNER.named_reference_issues(self.run, core, "architectureCorePayload")
            self.assertTrue({"missing_node", "missing_claimant"}.issubset({item["invalid"] for item in issues}))
            specs = [packet_plan()]
            annotation = {"packet_plans": [{"packet_slot_id": "packet_one", "depends_on_packet_slot_ids": ["future_packet"],
                "attractor_ids": ["missing_attractor"], "relevance": {"claimant_ids": ["missing_claimant"]}}]}
            issues = RUNNER.named_reference_issues(self.run, annotation, "architecturePlanBatchPayload", specs=specs)
            self.assertEqual({item["invalid"] for item in issues}, {"future_packet", "missing_attractor", "missing_claimant"})
            payload = packet_payload()
            scene = payload["scenes"][0]
            scene.update(arc_id="missing_arc", claimant_focus_ids=["missing_claimant"], variant_of_scene_id="missing_scene")
            scene["epistemic_dependencies"] = [{"subject_id": "missing_subject", "proposition_ids": ["missing_fact"]}]
            scene["artifacts"][0]["claimant_relevance_ids"] = ["missing_artifact_claimant"]
            scene["choices"] = [{"destination": {"kind": "technical_slot", "id": "missing_destination"}, "state_conditions": [], "state_effects": []}]
            scene["state_effects"] = [{"operation": "increment", "key": "missing_state", "value": 1}]
            issues = RUNNER.named_reference_issues(self.run, payload, "creativePacketPayload", plan=packet_plan())
            self.assertEqual(len(issues), 8)
            destination = next(item for item in issues if item["invalid"] == "missing_destination")
            self.assertNotIn("claimant_slot_01", destination["candidates"])

    def test_metadata_corrects_multiple_labels_without_regenerating_facts_or_prose(self):
        records = self.records()
        artistic = {"scenes": [{"technical_slot_id": "scene_slot_0002", "prose_mdx": "Immutable synthetic prose."}], "endings": []}
        semantic = genesis_semantic_payload("scene_slot_0002")
        semantic["canonical_facts"][0].update(subject="receipt", predicate="pencil notation", value="Synthetic notation.")
        semantic["canonical_facts"].append(copy.deepcopy(semantic["canonical_facts"][0]) | {"predicate": "seal shortage"})
        semantic["knowledge_changes"] = [{"source": {"technical_slot_id": "scene_slot_0002"}, "subject_id": "claimant_01",
            "relation": "knows", "proposition_id": name, "action": "establish", "relevance": {}}
            for name in ("fact_new_pencil_notation", "fact_new_seal_kit_shortage")]
        responses = [api_response(semantic), api_response("fact_01", text=True), api_response("fact_02", text=True)]
        transport = mock.Mock(side_effect=responses)
        with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records.get(kind)):
            normalized = RUNNER.request_semantic_normalization(self.run, "packet_one", artistic, "Synthetic context.", transport)
            again = RUNNER.request_semantic_normalization(self.run, "packet_one", artistic, "Synthetic context.", transport)
        self.assertEqual(transport.call_count, 3)
        self.assertEqual(normalized, again)
        self.assertEqual(normalized["canonical_facts"], semantic["canonical_facts"])
        self.assertEqual([item["proposition_id"] for item in normalized["knowledge_changes"]], ["fact_01", "fact_02"])
        self.assertEqual(artistic["scenes"][0]["prose_mdx"], "Immutable synthetic prose.")

    def test_paused_lookup_resumes_original_metadata_and_ledgers_every_response_once(self):
        records = self.records()
        artistic = {"scenes": [{"technical_slot_id": "scene_slot_0002", "prose_mdx": "Immutable synthetic prose."}], "endings": []}
        semantic = genesis_semantic_payload("scene_slot_0002")
        semantic["canonical_facts"].append(copy.deepcopy(semantic["canonical_facts"][0]) | {"predicate": "closed"})
        semantic["knowledge_changes"] = [{"source": {"technical_slot_id": "scene_slot_0002"}, "subject_id": "claimant_01", "relation": "knows",
            "proposition_id": name, "action": "establish", "relevance": {}} for name in ("fact_missing_one", "fact_missing_two")]
        transport = mock.Mock(side_effect=[api_response(semantic), api_response("fact_01", text=True)] + [api_response("bad_name", text=True)] * 3)
        with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records.get(kind)):
            with self.assertRaisesRegex(RUNNER.PausedError, "exhausted 3 focused"):
                RUNNER.request_semantic_normalization(self.run, "packet_one", artistic, "Synthetic context.", transport)
            original = {path: path.read_bytes() for path in (self.run / "raw").iterdir()}
            resume = mock.Mock(return_value=api_response("fact_02", text=True))
            normalized = RUNNER.request_semantic_normalization(self.run, "packet_one", artistic, "Synthetic context.", resume)
            RUNNER.request_semantic_normalization(self.run, "packet_one", artistic, "Synthetic context.", resume)
        self.assertEqual(resume.call_count, 1)
        self.assertNotIn("response_format", resume.call_args.args[2])
        self.assertEqual(normalized["knowledge_changes"][0]["proposition_id"], "fact_01")
        self.assertEqual(normalized["knowledge_changes"][1]["proposition_id"], "fact_02")
        self.assertIn("Immutable synthetic prose.", resume.call_args.args[2]["messages"][1]["content"])
        for path, value in original.items():
            self.assertEqual(path.read_bytes(), value)
        self.assertFalse((self.run / ".staging/packet_one.semantic-pending.json").exists())

    def test_full_twenty_scene_run_repairs_references_and_reaches_ready_without_resume(self):
        calls = []
        authored_slots = []
        original_prose = {}
        normalization_counts = {}

        def transport(_method, _url, request, **_kwargs):
            name = request.get("response_format", {}).get("json_schema", {}).get("name", "reference")
            prompt = request["messages"][1]["content"]
            if "FIELD PATH\n" in prompt:
                name = "planningValue"
            if "BATCH TARGETS\n" in prompt:
                name = "planningBatchValues"
            if "Choose ONLY the category needing correction" in prompt:
                name = "semanticCorrectionCategory"
            calls.append(name)
            schema = request.get("response_format", {}).get("json_schema", {}).get("schema", {})
            if name in {"planningValue", "planningBatchValues"}:
                def resolve(path, node):
                    if "__NEW_ATTRACTOR__" in node.get("enum", []):
                        return "__NEW_ATTRACTOR__"
                    if "__NARRATIVE_HINT__" in node.get("enum", []):
                        return "__NARRATIVE_HINT__"
                    if path[0] == "$setups":
                        return {"setup_slot_id": "scene_slot_0001", "instruction": "Synthetic earlier setup."}
                    if "enum" in node:
                        return node["enum"][0]
                    template = architecture_core_payload()["attractors"][0] | {"kind": "claimant"}
                    return template if len(path) == 2 else template[path[-1]]
                return planning_response(request, resolve)
            if name == "reference":
                prompt = request["messages"][1]["content"]
                candidates = json.loads(prompt.split("VALID REFERENCES\n", 1)[1].split("\n\nWhich", 1)[0])
                # Injected unknown labels each have one intended, described target.
                target = ("fact_01" if "fact_new_pencil_notation" in prompt else "fact_02" if "fact_new_seal_kit_shortage" in prompt
                    else "arc_001" if "missing_arc" in prompt else "claimant_01")
                self.assertIn(target, [item["id"] for item in candidates])
                return api_response(target, text=True)
            if name == "genesisFoundationPayload":
                value = foundation_payload()
                value["work_canon"]["central_incident"]["subjects"] = ["missing_claimant"]
            elif name == "genesisCastPayload":
                value = {"claimants": [claimant_expansion(f"claimant_{index:02d}") for index in range(1, 6)], "characters": []}
            elif name == "architectureCorePayload":
                value = architecture_core_payload()
                value["obligation_graph"][0]["termination_targets"].append("attractor_missing")
                foundation = RUNNER.committed_record(self.run, "genesis_foundation")
                value["obligation_graph"][0].update(created_by_ids=[foundation["commit_id"]], sources=[{
                    "artifact_type": "genesis", "artifact_id": foundation["commit_id"], "source_locator": "Synthetic foundation."}])
                value["arcs"] = [copy.deepcopy(value["arcs"][0]) | {"arc_id": f"arc_draft_{index}"} for index in range(1, 5)]
                response = api_response(value)
                response["choices"][0]["finish_reason"] = "length"
                return response
            elif name == "architectureRepair":
                if "resolutions" in schema["properties"]:
                    value = {"resolutions": {key: "UNRESOLVED" for key in schema["properties"]["resolutions"]["properties"]}}
                else:
                    value = {"replacement": "attractor_missing", "new_obligation": None,
                        "new_attractor": architecture_core_payload()["attractors"][0] | {"attractor_id": "attractor_missing", "kind": "claimant"}}
            elif name == "architecturePlanBatchPayload":
                core = RUNNER.planning_core(self.run)
                value = {"packet_plans": [{"packet_slot_id": spec["packet_slot_id"], "initial_priority": index,
                    "depends_on_packet_slot_ids": [], "branch_path_relation": "Synthetic relation.",
                    "attractor_ids": [core["attractors"][0]["attractor_id"]] if spec["packet_kind"] == "ending" else [],
                    "relevance": {"technical_slot_ids": spec["scene_slot_ids"] + spec["ending_slot_ids"],
                        "motif_ids": ["motif_pencil"], "state_keys": ["intro_phase"] if index == 1 else ["contamination"]},
                    "soft_guidance": []} for index, spec in enumerate(RUNNER.planned_packet_specs(core), 1)]}
            elif name == "creativePacketPayload":
                group = "scenes" if schema["properties"]["scenes"]["maxItems"] else "endings"
                definition = "scenePayload" if group == "scenes" else "endingPayload"
                properties = schema["$defs"][definition]["properties"]
                slot = properties["technical_slot_id"]["const"]
                authored_slots.append(slot)
                template = packet_payload(20, 5)["scenes"][0]
                if group == "scenes":
                    value = {"scenes": [template | {"technical_slot_id": slot, "arc_id": "missing_arc" if slot == "scene_slot_0002" else "arc_001"}], "endings": []}
                else:
                    value = {"scenes": [], "endings": [{"technical_slot_id": slot, "title": "Synthetic ending.", "ending_type": "commitment",
                        "claimant_pressure_ids": [], "entry_conditions": [], "state_effects": [], "redirect_destination": None,
                        "prose_mdx": "Synthetic ending fixture.", "artifacts": [], "choices": [], "formal_compositions": []}]}
                item = value[group][0]
                item["artifacts"] = [copy.deepcopy(template["artifacts"][0]) for _ in range(properties["artifacts"]["minItems"])]
                item["formal_compositions"] = [copy.deepcopy(template["formal_compositions"][0]) for _ in range(properties["formal_compositions"]["minItems"])]
                original_prose[slot] = item["prose_mdx"]
            elif name == "semanticCorrectionCategory":
                return api_response("obligation_updates", text=True)
            elif name == "semanticCategoryPage":
                if "Continue ONLY obligation_updates" in prompt:
                    source = schema["$defs"]["semanticSource"]["properties"]["technical_slot_id"]["enum"][0]
                    updates = [{"source": {"technical_slot_id": source}, "obligation_id": key,
                        "status": "satisfied", "reason": "Synthetic evidence fixture."}
                        for key, event in RUNNER._read_state_map(self.run, "obligations.json").items()
                        if source == "scene_slot_0006" and event["data"]["status"] == "active"]
                    value = {"items": updates, "complete": True}
                else:
                    self.assertIn("Continue ONLY motif_events", prompt)
                    value = {"items": [], "complete": True}
            elif name == "semanticDeltaPayload":
                source = schema["$defs"]["semanticSource"]["properties"]["technical_slot_id"].get("enum", ["claimant_slot_01"])[0]
                value = genesis_semantic_payload(source)
                normalization_counts[source] = normalization_counts.get(source, 0) + 1
                if source == "claimant_slot_01":
                    value["motif_events"] = [{"source": {"technical_slot_id": source}, "motif_id": "motif_pencil",
                        "action": "establish", "current_function": "Synthetic notation fixture.", "pressure": "Synthetic pressure.",
                        "overuse_risk": "low", "relevance": {}}]
                if source.startswith(("scene_slot_", "ending_slot_")):
                    value["canonical_facts"][0].update(subject="receipt", predicate="pencil notation", value="Synthetic notation.")
                    value["canonical_facts"][0]["relevance"]["motif_ids"] = ["motif_pencil"]
                    value["canonical_facts"].append(copy.deepcopy(value["canonical_facts"][0]) | {"predicate": "seal shortage"})
                    value["knowledge_changes"] = [{"source": {"technical_slot_id": source}, "subject_id": "claimant_01", "relation": "knows",
                        "proposition_id": identifier, "action": "establish", "relevance": {}}
                        for identifier in ("fact_new_pencil_notation", "fact_new_seal_kit_shortage")]
                if source == "scene_slot_0002":
                    self.assertEqual(schema["$defs"]["semanticObligationUpdate"]["properties"]["status"]["enum"],
                                     ["satisfied", "intentionally_unresolved"])
                    # Simulate a provider ignoring its corrected enum to exercise focused recovery.
                    obligation_id = next(iter(RUNNER._read_state_map(self.run, "obligations.json")))
                    value["obligation_updates"] = [{"source": {"technical_slot_id": source}, "obligation_id": obligation_id,
                        "status": "active", "reason": "Additional evidence, without resolution."}]
                if source == "scene_slot_0003":
                    self.assertTrue(all(event["data"]["status"] == "active" and "resolution_event" not in event
                        for event in RUNNER._read_state_map(self.run, "obligations.json").values()))
                if source == "scene_slot_0001":
                    partial = {key: item for key, item in value.items() if key != "motif_events"}
                    response = api_response(json.dumps(partial)[:-1] + ',"motif_events":[', text=True)
                    response["choices"][0]["finish_reason"] = "length"
                    return response
            else:
                self.fail(f"Unexpected request {name}")
            return api_response(value)

        with mock.patch.object(RUNNER, "ROOT", self.root):
            build_path, counts, _brief = RUNNER.execute_run(self.run, output_fn=lambda _: None, transport=transport)
        self.assertEqual(counts["scenes"], 20)
        self.assertEqual(counts["endings"], 5)
        self.assertEqual(len(authored_slots), len(set(authored_slots)))
        self.assertEqual(calls.count("reference"), 52)
        self.assertEqual(calls.count("architectureCorePayload"), 1)
        self.assertGreater(calls.count("planningValue"), 0)
        self.assertGreater(calls.count("planningBatchValues"), 0)
        self.assertEqual(calls.count("architectureRepair"), 0)
        self.assertEqual(normalization_counts["scene_slot_0002"], 1)
        self.assertEqual(normalization_counts["scene_slot_0006"], 1)
        failures = [entry for entry in RUNNER.ledger_entries(self.run) if entry["commit_status"] == "FAILED_BEFORE_COMMIT"]
        self.assertEqual(len(failures), 4)
        self.assertEqual(calls.count("semanticCategoryPage"), 3)
        self.assertEqual(calls.count("semanticCorrectionCategory"), 1)
        self.assertEqual({item["failure_class"] for item in failures}, {"provider_truncation", "malformed_response"})
        core_commit = next(path for path in RUNNER.committed_directories(self.run) if path.name.endswith("-architecture_core"))
        core_api = RUNNER.read_json(core_commit / "api-response.json")
        self.assertTrue(core_api["_cathedrals_assembled_from_fields"])
        self.assertEqual(core_api["choices"][0]["finish_reason"], "stop")
        planning = RUNNER.read_json(core_commit / "planning-draft.json")
        self.assertTrue(planning["setups_complete"])
        self.assertTrue(all(item["attached"] for item in planning["setups"]))
        finalization = RUNNER.read_json(self.run / "finalization.json")
        self.assertEqual(finalization["run_status"], "READY_TO_PLAY")
        self.assertTrue((build_path / "index.html").exists())
        for record in RUNNER.committed_records(self.run, "creative_packet"):
            for item in record["scenes"] + record["endings"]:
                self.assertEqual(item["prose_mdx"], original_prose[item["technical_slot_id"]])
        self.assertTrue(any((path / "named-reference-repair.json").exists() for path in RUNNER.committed_directories(self.run)))
        self.assertTrue(any((path / "semantic-recovery.json").exists() for path in RUNNER.committed_directories(self.run)))
        self.assertEqual(finalization["token_accounting"]["input_tokens"], 11 * len(calls))
        self.assertEqual(finalization["token_accounting"]["output_tokens"], 7 * len(calls))
        self.assertEqual(finalization["human_intervention_count"], 0)
        self.assertEqual(finalization["committed_regeneration_count"], 0)
        RUNNER.reconcile_run(self.run)


if __name__ == "__main__":
    unittest.main()
