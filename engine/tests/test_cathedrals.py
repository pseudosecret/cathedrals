#!/usr/bin/env python3
"""Offline checks for the end-user executable; no creative call is made."""

import copy
import dataclasses
import importlib.machinery
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest import mock

ROOT = Path(__file__).parents[2]
STATIC_READER_FIXTURE = ROOT / "engine/tests/fixtures/static-reader-work.json"
LOADER = importlib.machinery.SourceFileLoader(
    "cathedrals_runner", str(ROOT / "cathedrals")
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is not None:
    RUNNER = importlib.util.module_from_spec(SPEC)
else:
    raise RuntimeError("Failed to load cathedrals_runner module (note: SPEC is None)")
sys.modules[LOADER.name] = RUNNER
LOADER.exec_module(RUNNER)


def answers(*values):
    values = iter(values)
    return lambda _prompt="": next(values)


def static_reader_fixture():
    return json.loads(STATIC_READER_FIXTURE.read_text(encoding="utf-8"))


def art_direction(**updates):
    value = static_reader_fixture()["genesis"]["web_art_direction"]
    value.update(updates)
    return value


def source_ref(identifier="scene_old"):
    return {
        "artifact_type": "scene",
        "artifact_id": identifier,
        "source_locator": "prose_mdx#relevant",
    }


def hashed_source(identifier="scene_old"):
    return source_ref(identifier) | {
        "source_commit_id": "commit_source",
        "source_hash": "a" * 64,
    }


def empty_delta(**updates):
    value = {
        "canonical_facts": [],
        "knowledge_changes": [],
        "new_obligations": [],
        "obligation_updates": [],
        "motif_events": [],
        "potential_foreclosures": [],
    }
    value.update(updates)
    return value


def claimant_expansion(identifier):
    fields = (
        "setting_relationship",
        "personality",
        "epistemic_regime",
        "relationship_to_responsibility",
        "evidence_logic",
        "emotional_pressure",
        "rhetorical_behavior",
        "diction",
        "cadence",
        "contradiction_mode",
        "artifact_affinity",
        "environmental_pressure",
        "literary_effect",
        "accusation_consequence",
        "retraction_consequence",
    )
    return {
        "claimant_id": identifier,
        **{field: f"{identifier} {field}" for field in fields},
        "differentiation_notes": [f"{identifier} is distinct"],
    }


def genesis_foundation_fixture(count=5):
    anchors = [
        {
            "claimant_id": f"claimant_{number:02d}",
            "technical_slot_id": f"claimant_slot_{number:02d}",
            "name": f"Claimant {number}",
            "incident_role": f"Incident role {number}",
        }
        for number in range(1, count + 1)
    ]
    return {
        "record_type": "genesis_foundation",
        "generation_id": "generation_test",
        "commit_id": "commit_foundation",
        "format_composition_law": "Composition law",
        "work_canon": {
            "central_incident": {"subjects": ["claimant_01"]},
            "claimant_relationships": [],
            "generated_motifs": ["motif_one"],
            "principal_tensions": [],
        },
        "web_art_direction": {},
        "claimant_anchors": anchors,
    }


def genesis_cast_fixture(count=5):
    return {
        "record_type": "genesis_cast",
        "commit_id": "commit_cast",
        "claimants": [claimant_expansion(f"claimant_{number:02d}") for number in range(1, count + 1)],
        "characters": [{
            "character_id": "character_001",
            "technical_slot_id": "character_slot_001",
            "name": "Supporting Witness",
            "role": "Witnessed the transfer",
            "relationships": ["Works beside Claimant 1"],
            "dramatic_function": "Supplies independent provenance",
        }],
    }


def genesis_semantic_payload(source_slot="claimant_slot_01"):
    return {
        "canonical_facts": [{
            "source": {"technical_slot_id": source_slot},
            "subject": "threshold", "predicate": "opened", "value": True,
            "status": "established", "relevance": {"technical_slot_ids": [source_slot]},
        }],
        "knowledge_changes": [],
        "new_soft_obligations": [],
        "obligation_updates": [],
        "motif_events": [],
    }


def obligation(identifier="obligation_one", **updates):
    value = {
        "obligation_id": identifier,
        "kind": "ending_prerequisite",
        "description": "Earn the terminal transformation.",
        "status": "active",
        "created_by_ids": ["attractor_one"],
        "requires": [],
        "hardness": "hard",
        "universality": "attractor_scoped",
        "resolution_modes": ["transformation"],
        "range": "long_range",
        "termination_targets": ["attractor_one"],
        "sources": [source_ref("commit_architecture")],
        "relevance": {"branch_ids": ["branch_one"], "keywords": ["archive"]},
    }
    value.update(updates)
    return value


def attractor(identifier="attractor_one", prerequisite_ids=None, **updates):
    value = {
        "attractor_id": identifier,
        "kind": "ending",
        "terminal_transformation": "The reader becomes the documented subject.",
        "thematic_function": "Completion becomes participation.",
        "emotional_register": "contamination",
        "foreclosable": True,
        "prerequisite_obligation_ids": prerequisite_ids or ["obligation_one"],
        "soft_seed_conditions": ["institutional second person"],
        "unresolved_realization": ["exact document", "exact room", "final prose"],
        "ending_slot_ids": ["ending_slot_0001", "ending_slot_0002"],
        "relevance": {"branch_ids": ["branch_one"]},
    }
    value.update(updates)
    return value


def packet_plan(identifier="packet_one", **updates):
    value = {
        "packet_slot_id": identifier,
        "packet_kind": "literary",
        "initial_priority": 1,
        "scene_slot_ids": ["scene_slot_0001", "scene_slot_0002", "scene_slot_0003"],
        "ending_slot_ids": [],
        "artifact_count": 0,
        "formal_composition_count": 0,
        "depends_on_packet_slot_ids": [],
        "branch_path_relation": "branch_one",
        "attractor_ids": ["attractor_one"],
        "relevance": {
            "branch_ids": ["branch_one"],
            "character_ids": ["character_one"],
            "keywords": ["archive"],
        },
        "soft_guidance": ["Pressure the archive contradiction."],
    }
    value.update(updates)
    return value


def architecture_fixture(plans=None, obligations=None, attractors=None):
    return {
        "record_type": "architecture",
        "generation_id": "generation_test",
        "commit_id": "commit_architecture",
        "obligation_graph": obligations or [obligation()],
        "attractors": attractors or [attractor()],
        "packet_plans": plans or [packet_plan()],
    }


def architecture_core_payload():
    return {
        "saturation_rationale": "The macro structure is sufficient.",
        "obligation_graph": [obligation(created_by_ids=["commit_foundation"], sources=[source_ref("commit_foundation")])],
        "attractors": [{key: value for key, value in attractor().items() if key != "ending_slot_ids"}],
        "arcs": [{
            "arc_id": "arc_one",
            "purpose": "Pressure the opening contradiction.",
            "branch_role": "introduction",
            "required_beats": ["encounter", "choose"],
            "claimant_pressures": ["claimant_01"],
            "entry_conditions": ["entry"],
            "exit_conditions": ["choice"],
            "state_pressure": "indecision rises",
            "hard_obligation_ids": ["obligation_one"],
        }],
        "topology": {
            "entry_segment_id": "node_intro",
            "opening_branch_node_id": "node_intro",
            "reconvergence_node_ids": [],
            "nodes": [
                {"node_id": "node_intro", "node_type": "introduction", "purpose": "Open.", "hard_obligation_ids": []},
                *[
                    {"node_id": f"node_branch_{number}", "node_type": "branch_family", "purpose": f"Branch {number}.", "hard_obligation_ids": []}
                    for number in range(4)
                ],
            ],
            "edges": [
                {"edge_id": f"edge_{number}", "from_node_id": "node_intro", "to_node_id": f"node_branch_{number}", "relation": "branch", "hard_obligation_ids": []}
                for number in range(3)
            ],
        },
    }


def architecture_genesis_records():
    claimant = {
        "claimant_id": "claimant_01",
        "technical_slot_id": "claimant_slot_01",
        "occupation": "archivist",
        "setting_relationship": "Keeps the sealed archive.",
        "epistemic_regime": "Records establish reality.",
    }
    foundation = {
        "record_type": "genesis_foundation", "commit_id": "commit_foundation",
        "claimant_anchors": [{"technical_slot_id": "claimant_slot_01", "claimant_id": "claimant_01"}],
    }
    cast = {"record_type": "genesis_cast", "commit_id": "commit_cast"}
    constraints = {"record_type": "genesis_constraints", "commit_id": "commit_constraints"}
    genesis = {
        "record_type": "genesis", "commit_id": "commit_constraints",
        "claimants": [claimant], "characters": [],
        "work_canon": {"premise": "A sealed archive contradicts itself.", "central_incident": {"event": "A record vanished."}, "chronology": []},
        "constraint_delta": {"canonical_facts": [], "knowledge_changes": [], "motif_events": []},
    }
    return {
        "genesis_foundation": foundation,
        "genesis_cast": cast,
        "genesis_constraints": constraints,
        "genesis": genesis,
    }


def constraint_event(
    sequence,
    kind,
    data,
    constraint_class="past_constraint",
    source="scene_old",
    action="establish",
):
    return {
        "record_type": "constraint_event",
        "protocol_version": "6.0",
        "generation_id": "generation_test",
        "constraint_event_sequence": sequence,
        "origin_step_id": "packet_one",
        "constraint_id": data.get("fact_id")
        or data.get("knowledge_id")
        or data.get("obligation_id")
        or data.get("update_id")
        or data.get("motif_event_id")
        or data.get("foreclosure_id"),
        "constraint_class": constraint_class,
        "constraint_kind": kind,
        "action": action,
        "data": data,
        "sources": [hashed_source(source)],
    }


def genesis_ledger(seed="12345"):
    return {
        "record_type": "ledger_entry",
        "protocol_version": "6.0",
        "generation_id": "generation_test",
        "ledger_sequence": 1,
        "planned_step_id": "genesis",
        "attempt": 1,
        "step_type": "creative",
        "step_phase": "genesis",
        "previous_entry_hash": None,
        "entry_hash": "a" * 64,
        "parent_canonical_state_hash": "b" * 64,
        "prompt_hash": "c" * 64,
        "context_hash": "d" * 64,
        "provider": "LM Studio",
        "model": "model",
        "parameters": {"seed": seed},
        "seed": seed,
        "started_at": "2026-01-01T00:00:00Z",
        "completed_at": "2026-01-01T00:00:01Z",
        "output_hash": "e" * 64,
        "generated_artifact_ids": ["commit_genesis"],
        "past_constraint_delta_ids": [],
        "future_obligation_delta_ids": [],
        "motif_pressure_delta_ids": [],
        "prospective_plan_hash_after": None,
        "branch_path_relation": "generated_root_canon",
        "commit_status": "COMMITTED",
        "canonical_state_hash_after": "f" * 64,
        "failure_class": "none",
        "token_accounting": {
            "input_tokens": 10,
            "output_tokens": 20,
            "cost": None,
            "currency": None,
        },
    }


class CathedralsRunnerTests(unittest.TestCase):
    def test_four_inputs_and_defaults(self):
        output = []
        brief = RUNNER.collect_inputs(answers("", "", "", "web"), output.append)
        self.assertEqual(brief.project_name, "Cathedrals")
        self.assertEqual(brief.genre_flavor, "existential mystery")
        self.assertEqual(brief.possible_scene_count, 150)
        self.assertEqual(brief.story_format, "web")
        self.assertFalse(brief.mutable)

    def test_incomplete_runs_ignore_pre_protocol_6_generations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, version in (("old", "5.0"), ("current", "6.0")):
                run = root / name
                (run / "state").mkdir(parents=True)
                RUNNER.write_json(run / "state/run-state.json", {"status": "GENESIS"})
                RUNNER.write_json(run / "run-manifest.json", {"protocol_version": version})
            with mock.patch.object(RUNNER, "RUNS_ROOT", root):
                self.assertEqual(RUNNER.incomplete_runs(), [root / "current"])

    def test_scene_count_rejects_nonpositive_and_noninteger(self):
        for value in ("0", "-1", "3.5", "many"):
            with self.assertRaises(ValueError):
                RUNNER.parse_scene_count(value)
        self.assertEqual(RUNNER.parse_scene_count("151"), 151)

    def test_format_aliases_are_accepted_but_effective_output_is_web(self):
        for alias in ("visualnovel", "visual novel", "visual-novel", "vn"):
            self.assertEqual(RUNNER.normalize_requested_format(alias), "visualnovel")
            self.assertEqual(RUNNER.renderer_for(alias), "astro")
            self.assertEqual(RUNNER.active_format_contract(alias).name, "web.md")
        with self.assertRaises(ValueError):
            RUNNER.normalize_requested_format("")

    def test_generation_inputs_are_frozen(self):
        brief = RUNNER.FrozenInputs()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            brief.genre_flavor = "changed"

    def test_lm_studio_url_default_and_override(self):
        self.assertEqual(
            RUNNER.configured_lm_studio_url({"UNRELATED": "1"}), "http://127.0.0.1:1234"
        )
        self.assertEqual(
            RUNNER.configured_lm_studio_url(
                {"CATHEDRALS_LM_STUDIO_URL": "http://127.0.0.1:5555/"}
            ),
            "http://127.0.0.1:5555",
        )

    def test_unreachable_lm_studio_fails_in_preflight(self):
        def unreachable(*_args, **_kwargs):
            raise RUNNER.CathedralsError("test", "offline", "transport_before_response")

        with self.assertRaisesRegex(
            RUNNER.CathedralsError, "Open LM Studio on Windows"
        ):
            RUNNER.lm_studio_preflight("http://127.0.0.1:1234", transport=unreachable)

    def test_model_discovery_and_selection(self):
        payload = {"data": [{"id": "writer"}, {"id": "embedder", "type": "embedding"}]}
        self.assertEqual(RUNNER.usable_model_ids(payload), ["writer"])
        self.assertEqual(RUNNER.choose_model(["writer"]), "writer")
        self.assertEqual(
            RUNNER.choose_model(
                ["a", "b"], input_fn=answers("2"), output_fn=lambda _line: None
            ),
            "b",
        )
        with self.assertRaises(RUNNER.CathedralsError):
            RUNNER.choose_model(["writer"], override="missing")

    def test_provider_response_normalization_is_shared_and_strict(self):
        def response(message, finish_reason="stop"):
            return {"choices": [{"finish_reason": finish_reason, "message": message}]}

        self.assertEqual(
            RUNNER.normalize_provider_response(
                response(
                    {
                        "content": '{"source":"content"}',
                        "reasoning": "{}",
                        "reasoning_content": "[]",
                    }
                )
            ),
            '{"source":"content"}',
        )
        for field in ("reasoning", "reasoning_content"):
            self.assertEqual(
                RUNNER.normalize_provider_response(
                    response({"content": "", field: '{"result":"PASS"}'})
                ),
                '{"result":"PASS"}',
            )
        with self.assertRaisesRegex(RUNNER.SchemaError, "conflicting reasoning"):
            RUNNER.normalize_provider_response(
                response({"content": "", "reasoning": "{}", "reasoning_content": "[]"})
            )
        with self.assertRaisesRegex(RUNNER.SchemaError, "complete JSON"):
            RUNNER.normalize_provider_response(
                response({"content": None, "reasoning": 'notes {"result":"PASS"}'})
            )
        with self.assertRaisesRegex(RUNNER.TruncationError, "truncated"):
            RUNNER.normalize_provider_response(response({"content": "{}"}, "length"))
        for empty in (
            None,
            response({"content": "", "reasoning": "", "reasoning_content": None}),
        ):
            with self.assertRaises(RUNNER.CathedralsError) as raised:
                RUNNER.normalize_provider_response(empty)
            self.assertNotIsInstance(raised.exception, RUNNER.IntegrityError)
            self.assertEqual(
                raised.exception.failure_class, "provider_before_creative_output"
            )
        with self.assertRaises(RUNNER.CathedralsError) as raised:
            RUNNER.provider_response(
                lambda *_args, **_kwargs: None, "http://offline.invalid", {}, 1
            )
        self.assertNotIsInstance(raised.exception, RUNNER.IntegrityError)
        self.assertIn("provider_response", RUNNER.request_record.__code__.co_names)
        self.assertIn("provider_response", RUNNER.request_analysis.__code__.co_names)

    def test_grammar_parse_http_400_pauses_after_one_attempt(self):
        http_error = RUNNER.urllib.error.HTTPError(
            "http://offline.invalid", 400, "Bad Request", {}, None
        )
        http_error.read = lambda: b'{"error":"Failed to initialize samplers: failed to parse grammar"}'
        with mock.patch.object(RUNNER.urllib.request, "urlopen", side_effect=http_error), self.assertRaises(
            RUNNER.CathedralsError
        ) as raised:
            RUNNER.http_json("POST", "http://offline.invalid", {})
        self.assertEqual(raised.exception.failure_class, "provider_schema_incompatibility")
        self.assertIn(raised.exception.failure_class, RUNNER.PAUSABLE_FAILURES)

        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            for name in ("state", "raw", "committed", "constraints", ".staging"):
                (run / name).mkdir(parents=True)
            RUNNER.save_state(run, RUNNER.initial_run_state(run.name, "a" * 64, "b" * 64, "offline"))
            RUNNER.write_json(run / "generation-brief.json", {
                "generation_seed": "seed", "lm_studio_base_url": "http://offline.invalid",
            })
            RUNNER.write_json(run / "run-manifest.json", {
                "budgets": {"max_prepared_context_tokens": 49152},
            })
            def reject_grammar(*_args, **_kwargs):
                raise RUNNER.CathedralsError(
                    "LM Studio structured output", "could not compile grammar",
                    "provider_schema_incompatibility",
                )

            transport = mock.Mock(side_effect=reject_grammar)
            with self.assertRaises(RUNNER.CathedralsError) as request_error:
                RUNNER.request_record(
                    run, expected_record_type="genesis_foundation", step_id="grammar_test",
                    phase="genesis", prompt="prompt", context="context",
                    branch_relation="foundation", temperature=0.8,
                    response_definition="claimantAnchorPayload", transport=transport,
                )
            self.assertEqual(request_error.exception.failure_class, "provider_schema_incompatibility")
            self.assertEqual(transport.call_count, 1)
            self.assertEqual(len(RUNNER.ledger_entries(run)), 1)

    def test_numeric_genesis_seed_has_structured_schema_error(self):
        protocol = RUNNER.load_protocol()
        self.assertIsInstance(RUNNER.step_seed("generation-seed", "genesis"), str)
        with self.assertRaises(RUNNER.SchemaError) as raised:
            RUNNER.validate_json_schema(genesis_ledger(12345), protocol)
        self.assertEqual(
            str(raised.exception),
            "Genesis failed schema validation with 1 problem:\n\n"
            "1. $.seed\n"
            "   Expected: string\n"
            "   Received: integer (12345)",
        )

    def test_schema_validation_reports_all_problems_together(self):
        protocol = RUNNER.load_protocol()
        invalid = genesis_ledger(12345)
        del invalid["model"]
        invalid["failure_class"] = "build_failure"
        invalid["token_accounting"]["input_tokens"] = -1
        with self.assertRaises(RUNNER.SchemaError) as raised:
            RUNNER.validate_json_schema(invalid, protocol)
        reason = str(raised.exception)
        self.assertIn("Genesis failed schema validation with 4 problems:", reason)
        self.assertIn(
            "$.seed\n   Expected: string\n   Received: integer (12345)", reason
        )
        self.assertIn(
            "$.model\n   Expected: required field\n   Received: missing", reason
        )
        self.assertIn(
            '$.failure_class\n   Expected: "none"\n   Received: "build_failure"', reason
        )
        self.assertIn(
            "$.token_accounting.input_tokens\n   Expected: number greater than or equal to 0\n   Received: -1",
            reason,
        )

    def test_valid_schema_record_passes_unchanged(self):
        protocol = RUNNER.load_protocol()
        valid = genesis_ledger()
        original = json.loads(json.dumps(valid))
        RUNNER.validate_json_schema(valid, protocol)
        self.assertEqual(valid, original)

    def test_genesis_cast_schema_authors_expansions_only(self):
        protocol = RUNNER.load_protocol()
        schema = protocol["$defs"]["claimant"]
        valid = claimant_expansion("claimant_01")
        original = json.loads(json.dumps(valid))
        RUNNER.validate_json_schema(valid, schema, protocol)
        self.assertEqual(valid, original)

        invalid = valid | {
            "technical_slot_id": "claimant_slot_01",
            "name": "Repeated name",
            "incident_role": "Repeated role",
        }
        with self.assertRaises(RUNNER.SchemaError) as raised:
            RUNNER.validate_json_schema(invalid, schema, protocol)
        reason = str(raised.exception)
        self.assertIn("failed schema validation with 3 problems", reason)
        for field in ("technical_slot_id", "name", "incident_role"):
            self.assertIn(f"$.{field}", reason)

    def test_genesis_cast_requires_every_anchor_id_and_reports_all_offenders(self):
        foundation = genesis_foundation_fixture()
        valid = {
            "foundation_commit_id": foundation["commit_id"],
            "commit_id": "commit_cast",
            "claimants": [
                claimant_expansion(f"claimant_{number:02d}")
                for number in range(5, 0, -1)
            ],
            "characters": [],
        }
        with mock.patch.object(RUNNER, "committed_record", return_value=foundation):
            RUNNER.validate_genesis_cast(valid, Path("/offline"))
        self.assertEqual(
            RUNNER.generated_ids(valid | {"record_type": "genesis_cast"}),
            ["commit_cast"],
        )

        invalid = valid | {
            "claimants": [
                claimant_expansion(identifier)
                for identifier in (
                    "claimant_01",
                    "claimant_01",
                    "unexpected_a",
                    "unexpected_b",
                    "unexpected_b",
                )
            ]
        }
        with mock.patch.object(
            RUNNER, "committed_record", return_value=foundation
        ), self.assertRaises(RUNNER.SchemaError) as raised:
            RUNNER.validate_genesis_cast(invalid, Path("/offline"))
        reason = str(raised.exception)
        for identifier in (
            "claimant_01",
            "claimant_02",
            "claimant_03",
            "claimant_04",
            "claimant_05",
            "unexpected_a",
            "unexpected_b",
        ):
            self.assertIn(identifier, reason)
        self.assertIn("missing:", reason)
        self.assertIn("unexpected:", reason)
        self.assertIn("duplicated:", reason)

    def test_genesis_initial_claimant_range_and_character_slots(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            RUNNER.write_json(run / "generation-brief.json", {"generation_id": "generation_test"})
            for count in (5, 8):
                foundation = genesis_foundation_fixture(count) | {"story_format": "web"}
                RUNNER.validate_genesis_foundation(foundation, run)
            for count in (4, 9):
                foundation = genesis_foundation_fixture(count) | {"story_format": "web"}
                with self.assertRaisesRegex(RUNNER.SchemaError, "five to eight"):
                    RUNNER.validate_genesis_foundation(foundation, run)

        foundation = genesis_foundation_fixture()
        payload = genesis_cast_fixture()
        payload["characters"] = [{
            key: value for key, value in payload["characters"][0].items()
            if key not in {"character_id", "technical_slot_id"}
        }]
        with mock.patch.object(RUNNER, "committed_record", return_value=foundation):
            built = RUNNER.build_genesis_cast(Path("/generation_test"), payload)
        self.assertEqual(built["characters"][0]["technical_slot_id"], "character_slot_001")

    def test_genesis_reference_repair_resolves_repeated_unknown_slot_to_character(self):
        foundation = genesis_foundation_fixture()
        cast = genesis_cast_fixture()
        records = {"genesis_foundation": foundation, "genesis_cast": cast}
        payload = genesis_semantic_payload("claimant_slot_07")
        calls = []

        def resolve(_run, _step, _prompt, _schema, _transport, validator=None, **_kwargs):
            result = {
                "action": "resolve", "replacement": "character_slot_001",
                "claimant_extension": None, "reason": "The supporting witness is the source.",
            }
            validator(result)
            calls.append(result)
            return result, {"usage": {}}

        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            (run / ".staging").mkdir(parents=True)
            with mock.patch.object(
                RUNNER, "committed_record", side_effect=lambda _run, kind: records[kind]
            ), mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=resolve):
                repaired = RUNNER.repair_genesis_constraints_payload(
                    run, "genesis_constraints", payload, "{}", {"usage": {}}, None
                )
                record = RUNNER.build_genesis_constraints(run, repaired)
        self.assertEqual(len(calls), 1)
        self.assertEqual(repaired["canonical_facts"][0]["source"]["technical_slot_id"], "character_slot_001")
        self.assertEqual(repaired["canonical_facts"][0]["relevance"]["technical_slot_ids"], ["character_slot_001"])
        self.assertEqual(record["constraint_delta"]["canonical_facts"][0]["sources"][0]["artifact_id"], "character_001")
        self.assertEqual(repaired["_claimant_extensions"], [])

    def test_genesis_reference_repair_can_promote_or_create_one_claimant(self):
        for origin, name in (("character_001", "Supporting Witness"), (None, "New Claimant")):
            with self.subTest(origin=origin):
                foundation = genesis_foundation_fixture()
                cast = genesis_cast_fixture()
                records = {"genesis_foundation": foundation, "genesis_cast": cast}
                profile = claimant_expansion("draft")
                profile.pop("claimant_id")
                decision = {
                    "action": "expand", "replacement": None,
                    "claimant_extension": {
                        "name": name,
                        "incident_role": "Held the unrepresented threshold authority",
                        "origin_character_id": origin,
                        "profile": profile,
                        "relationships_to_existing": [{
                            "claimant_id": "claimant_01",
                            "relationship": "Contests the first claimant's custody",
                            "dramatic_pressure": "Their records cannot both govern the transfer.",
                        }],
                    },
                    "reason": "The fact requires a distinct world-logic.",
                }

                def expand(_run, _step, _prompt, _schema, _transport, validator=None, **_kwargs):
                    validator(decision)
                    return decision, {"usage": {}}

                with tempfile.TemporaryDirectory() as temporary:
                    run = Path(temporary) / "generation_test"
                    (run / ".staging").mkdir(parents=True)
                    with mock.patch.object(
                        RUNNER, "committed_record", side_effect=lambda _run, kind: records[kind]
                    ), mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=expand):
                        repaired = RUNNER.repair_genesis_constraints_payload(
                            run, "genesis_constraints", genesis_semantic_payload("claimant_slot_07"),
                            "{}", {"usage": {}}, None,
                        )
                        record = RUNNER.build_genesis_constraints(run, repaired)
                        protocol = RUNNER.load_protocol()
                        RUNNER.validate_json_schema(record, protocol["$defs"]["genesisConstraints"], protocol)
                        RUNNER.validate_genesis_constraints(record, run)
                        events = RUNNER.make_constraint_events(
                            run, record, record["commit_id"], "a" * 64, "genesis_constraints"
                        )
                extension = record["claimant_extensions"][0]
                self.assertEqual(extension["anchor"]["claimant_id"], "claimant_06")
                self.assertEqual(extension["anchor"]["technical_slot_id"], "claimant_slot_06")
                self.assertEqual(extension["origin_character_id"], origin)
                self.assertEqual(repaired["canonical_facts"][0]["source"]["technical_slot_id"], "claimant_slot_06")
                self.assertEqual(events[0]["sources"][0]["artifact_id"], "claimant_06")
                self.assertEqual(events[0]["sources"][0]["source_commit_id"], record["commit_id"])

    def test_genesis_expansion_cap_disables_expansion(self):
        foundation = genesis_foundation_fixture(8)
        cast = genesis_cast_fixture(8)
        records = {"genesis_foundation": foundation, "genesis_cast": cast}
        extensions = []
        with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records[kind]):
            for number in range(4):
                profile = claimant_expansion("draft")
                profile.pop("claimant_id")
                extensions.append(RUNNER.materialize_claimant_extension({
                    "name": f"Extension {number}", "incident_role": f"Role {number}",
                    "origin_character_id": None, "profile": profile,
                    "relationships_to_existing": [{
                        "claimant_id": "claimant_01", "relationship": "Opposes",
                        "dramatic_pressure": "Distinct pressure",
                    }],
                }, Path("/offline"), extensions))
            issue = {"kind": "source", "invalid": "claimant_slot_99", "contexts": [], "candidates": ["claimant_slot_01"]}
            _prompt, schema = RUNNER.claimant_resolution_request(issue, Path("/offline"), extensions)
        self.assertEqual(schema["properties"]["action"]["enum"], ["resolve"])

    def test_assembled_genesis_merges_anchors_with_cast_expansions(self):
        foundation = genesis_foundation_fixture()
        cast = {
            "record_type": "genesis_cast",
            "commit_id": "commit_cast",
            "claimants": [
                claimant_expansion(f"claimant_{number:02d}")
                for number in range(5, 0, -1)
            ],
            "characters": [],
        }
        constraints = {
            "record_type": "genesis_constraints",
            "commit_id": "commit_constraints",
            "constraint_delta": empty_delta(),
        }
        records = {
            "genesis_foundation": foundation,
            "genesis_cast": cast,
            "genesis_constraints": constraints,
        }
        committed_inputs = json.loads(json.dumps(records))
        with mock.patch.object(
            RUNNER,
            "committed_record",
            side_effect=lambda _run, record_type: records[record_type],
        ):
            genesis = RUNNER.assembled_genesis(Path("/offline"))
        self.assertEqual(
            [item["claimant_id"] for item in genesis["claimants"]],
            [f"claimant_{number:02d}" for number in range(1, 6)],
        )
        for claimant in genesis["claimants"]:
            self.assertIn("technical_slot_id", claimant)
            self.assertIn("name", claimant)
            self.assertIn("incident_role", claimant)
            self.assertIn("personality", claimant)
        self.assertEqual(records, committed_inputs)

    def test_semantic_delta_accepts_compatibility_aliases_and_coalesces_duplicate_facts(self):
        payload = {
            "canonical_facts": [
                {
                    "source": {"technical_slot_id": "claimant_slot_01"},
                    "subject": "room_archive",
                    "predicate": "sealed",
                    "value": True,
                    "status": "established",
                    "relevance": {"claimant_ids": ["claimant_01"], "keywords": ["archive"]},
                },
                {
                    "source": {"technical_slot_id": "claimant_slot_02"},
                    "subject": "room_archive",
                    "predicate": "sealed",
                    "value": True,
                    "status": "established",
                    "relevance": {"claimant_ids": ["claimant_02"], "keywords": ["archive", "seal"]},
                },
            ],
            "knowledge_changes": [
                {
                    "source": {"technical_slot_id": "claimant_slot_01"},
                    "subject_id": "claimant_01",
                    "relation": "knows",
                    "proposition_id": "prop_01",
                    "action": "establish",
                    "relevance": {},
                },
                {
                    "source": {"technical_slot_id": "claimant_slot_02"},
                    "subject_id": "claimant_02",
                    "relation": "believes",
                    "proposition_id": "proposition_02",
                    "action": "establish",
                    "relevance": {},
                },
                {
                    "source": {"technical_slot_id": "claimant_slot_02"},
                    "subject_id": "claimant_02",
                    "relation": "suspects",
                    "proposition_id": "fact_02",
                    "action": "establish",
                    "relevance": {},
                },
                {
                    "source": {"technical_slot_id": "claimant_slot_01"},
                    "subject_id": "claimant_01",
                    "relation": "believes",
                    "proposition_id": "p01",
                    "action": "establish",
                    "relevance": {},
                },
                {
                    "source": {"technical_slot_id": "claimant_slot_01"},
                    "subject_id": "claimant_01",
                    "relation": "claims",
                    "proposition_id": "p_001",
                    "action": "establish",
                    "relevance": {},
                },
            ],
            "new_soft_obligations": [],
            "obligation_updates": [],
            "motif_events": [],
        }
        content_ids = {
            "claimant_slot_01": ("genesis", "claimant_01"),
            "claimant_slot_02": ("genesis", "claimant_02"),
        }
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            (run / "state").mkdir(parents=True)
            delta = RUNNER.build_semantic_delta(run, "genesis_constraints", payload, content_ids)

            fact = delta["canonical_facts"][0]
            self.assertEqual(len(delta["canonical_facts"]), 1)
            self.assertEqual(fact["fact_id"], RUNNER.deterministic_id("fact", run.name, "genesis_constraints", 1))
            self.assertEqual([source["artifact_id"] for source in fact["sources"]], ["claimant_01", "claimant_02"])
            self.assertEqual(fact["relevance"]["claimant_ids"], ["claimant_01", "claimant_02"])
            self.assertEqual(fact["relevance"]["keywords"], ["archive", "seal"])
            self.assertEqual({item["proposition_id"] for item in delta["knowledge_changes"]}, {fact["fact_id"]})

            for unknown in ("proposition_03", "p03", "p_003"):
                payload["knowledge_changes"][0]["proposition_id"] = unknown
                with self.assertRaisesRegex(RUNNER.SchemaError, f"unknown proposition {unknown}"):
                    RUNNER.build_semantic_delta(run, "genesis_constraints", payload, content_ids)

    def test_genesis_constraints_schema_bounds_raw_normalization(self):
        schema = RUNNER.genesis_constraints_schema(Path("/offline"))
        self.assertEqual(set(schema["$defs"]), {
            "id", "idList", "nonEmptyString", "relevanceTags", "semanticFact",
            "semanticKnowledge", "semanticMotif", "semanticSource", "stringList",
        })
        unsupported = {"allOf", "if", "then", "else", "uniqueItems"}
        self.assertFalse(any(unsupported & set(node) for node in RUNNER._walk(schema) if isinstance(node, dict)))
        self.assertEqual(
            schema["$defs"]["semanticFact"]["properties"]["value"]["type"],
            ["string", "number", "boolean", "null"],
        )
        payload = {
            "canonical_facts": [{
                "source": {"technical_slot_id": "claimant_slot_01"},
                "subject": "room_one", "predicate": "sealed", "value": True,
                "status": "established",
                "relevance": {
                    "claimant_ids": ["claimant_01"],
                    "character_ids": ["character_001"],
                    "motif_ids": ["motif_one"],
                    "technical_slot_ids": ["claimant_slot_01"],
                },
            }],
            "knowledge_changes": [],
            "new_soft_obligations": [],
            "obligation_updates": [],
            "motif_events": [{
                "source": {"technical_slot_id": "claimant_slot_01"},
                "motif_id": "motif_one", "action": "establish",
                "current_function": "Marks the sealed room.", "pressure": "The seal persists.",
                "overuse_risk": "low", "relevance": {},
            }],
        }
        RUNNER.validate_json_schema(payload, schema)
        self.assertEqual(schema["properties"]["canonical_facts"]["maxItems"], 24)
        self.assertEqual(schema["properties"]["knowledge_changes"]["maxItems"], 24)
        self.assertEqual(schema["properties"]["new_soft_obligations"]["maxItems"], 0)
        self.assertNotIn("items", schema["properties"]["new_soft_obligations"])
        for value in ("open", 3.5, True, None):
            scalar = copy.deepcopy(payload)
            scalar["canonical_facts"][0]["value"] = value
            RUNNER.validate_json_schema(scalar, schema)
        for value in (["open"], {"state": "open"}):
            nonscalar = copy.deepcopy(payload)
            nonscalar["canonical_facts"][0]["value"] = value
            with self.assertRaises(RUNNER.SchemaError):
                RUNNER.validate_json_schema(nonscalar, schema)
        invalid = copy.deepcopy(payload)
        invalid["canonical_facts"] *= 25
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(invalid, schema)

        too_many_unique = copy.deepcopy(payload)
        too_many_unique["canonical_facts"] = [
            payload["canonical_facts"][0] | {"subject": f"subject_{number}"}
            for number in range(13)
        ]
        with self.assertRaisesRegex(RUNNER.SchemaError, "twelve unique"):
            RUNNER.validate_genesis_constraints_payload(too_many_unique)

        slots = [f"claimant_slot_{number:02d}" for number in range(1, 13)] + [
            f"character_slot_{number:03d}" for number in range(1, 13)
        ]
        duplicate_payload = copy.deepcopy(payload)
        duplicate_payload["canonical_facts"] = [
            payload["canonical_facts"][0] | {"source": {"technical_slot_id": slot}}
            for slot in slots
        ]
        with tempfile.TemporaryDirectory() as temporary:
            fact = RUNNER.build_semantic_delta(
                Path(temporary), "genesis_constraints", duplicate_payload,
                {slot: ("genesis", f"source_{number:02d}") for number, slot in enumerate(slots, 1)},
            )["canonical_facts"][0]
        self.assertEqual(len(fact["sources"]), 24)
        protocol = RUNNER.load_protocol()
        RUNNER.validate_json_schema(fact, protocol["$defs"]["canonicalFact"], protocol)

    def test_genesis_constraints_uses_fixed_8192_token_request_without_expanded_retry(self):
        captured = {}

        def committed(_run, kind):
            return {"commit_id": f"commit_{kind}"} if kind in {"genesis_foundation", "genesis_cast"} else None

        def stop_after_request(_run, **kwargs):
            captured.update(kwargs)
            raise RuntimeError("captured")

        with mock.patch.object(RUNNER, "verify_engine_snapshot"), mock.patch.object(
            RUNNER, "ensure_frozen_geomancy"
        ), mock.patch.object(RUNNER, "committed_record", side_effect=committed), mock.patch.object(
            RUNNER, "genesis_constraints_prompt", return_value=("prompt", "context")
        ), mock.patch.object(RUNNER, "request_record", side_effect=stop_after_request), mock.patch.object(
            RUNNER, "request_bounded_record"
        ) as bounded, self.assertRaisesRegex(RuntimeError, "captured"):
            RUNNER.execute_creative_phases(Path("/offline"), output_fn=lambda _value: None)
        self.assertEqual(captured["max_tokens"], 8192)
        self.assertIsNotNone(captured["payload_repairer"])
        self.assertIsNotNone(captured["response_schema"])
        bounded.assert_not_called()

    def test_packet_semantic_request_constrains_sources_to_authored_slots(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            for name in ("state", "raw", ".staging"):
                (run / name).mkdir(parents=True)
            RUNNER.save_state(run, RUNNER.initial_run_state(run.name, "a" * 64, "b" * 64, "offline"))
            RUNNER.write_json(run / "generation-brief.json", {
                "generation_seed": "seed", "lm_studio_base_url": "http://offline.invalid"
            })
            seen = []

            def transport(_method, _url, request, **_kwargs):
                seen.extend(request["response_format"]["json_schema"]["schema"]["$defs"]
                    ["semanticSource"]["properties"]["technical_slot_id"]["enum"])
                return {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps({
                    "canonical_facts": [], "knowledge_changes": [], "new_soft_obligations": [],
                    "obligation_updates": [], "motif_events": [],
                })}}]}

            result = RUNNER.request_semantic_normalization(
                run, "packet_one", {
                    "scenes": [{"technical_slot_id": "scene_slot_0002"}],
                    "endings": [{"technical_slot_id": "ending_slot_0001"}],
                }, "context", transport,
            )
        self.assertEqual(result["canonical_facts"], [])
        self.assertEqual(seen, ["ending_slot_0001", "scene_slot_0002"])

    def test_architecture_builder_reports_all_semantic_reference_problems(self):
        payload = {
            "obligation_graph": [{
                "obligation_id": "obligation_soft",
                "hardness": "soft",
                "created_by_ids": ["genesis_commit_01"],
                "requires": ["obligation_missing"],
                "termination_targets": ["attractor_missing"],
                "sources": [{"artifact_id": "source_missing"}],
            }],
            "attractors": [{
                "attractor_id": "attractor_one",
                "prerequisite_obligation_ids": ["obligation_soft", "obligation_absent"],
            }],
            "arcs": [{
                "arc_id": "arc_01",
                "claimant_pressures": ["claimant_slot_02"],
                "hard_obligation_ids": ["obligation_hard_missing"],
            }],
            "topology": {
                "entry_segment_id": "node_entry",
                "opening_branch_node_id": "node_missing",
                "reconvergence_node_ids": [],
                "nodes": [{"node_id": "node_entry", "hard_obligation_ids": []}],
                "edges": [{
                    "edge_id": "edge_01",
                    "from_node_id": "node_entry",
                    "to_node_id": "edge_node_missing",
                    "relation": "progression",
                    "hard_obligation_ids": [],
                }],
            },
        }
        genesis = {"claimants": [{"claimant_id": "claimant_01", "technical_slot_id": "claimant_slot_01"}]}
        with mock.patch.object(RUNNER, "committed_record", return_value=genesis), mock.patch.object(
            RUNNER, "_source_index", return_value={"source_known": {}}
        ), self.assertRaises(RUNNER.SchemaError) as raised:
            RUNNER.build_architecture_core(Path("/offline"), payload)
        reason = raised.exception.reason
        for problem in (
            "undeclared topology nodes: edge_node_missing, node_missing",
            "unknown claimant pressures: claimant_slot_02",
            "unknown obligation origins: genesis_commit_01",
            "unknown obligation references: obligation_absent, obligation_hard_missing, obligation_missing",
            "unknown obligation termination targets: attractor_missing",
            "unresolved obligation sources: source_missing",
            "opening branch node has 0 outgoing branch edges; expected 3",
        ):
            self.assertIn(problem, reason)

        architecture_node = RUNNER.load_protocol()["$defs"]["architectureNode"]
        self.assertNotIn("generation_dependency_ids", architecture_node["required"])
        self.assertNotIn("generation_dependency_ids", architecture_node["properties"])

    def test_architecture_prompt_lists_allowed_claimant_and_source_ids(self):
        manifest = {"budgets": {"max_prepared_context_tokens": 20000}}
        genesis = {"claimants": [{"claimant_id": "claimant_02"}, {"claimant_id": "claimant_01"}]}
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / "state").mkdir()
            (run / "state/frozen-engine-context.txt").write_text("canon", encoding="utf-8")
            with mock.patch.object(RUNNER, "read_json", return_value=manifest), mock.patch.object(
                RUNNER, "committed_record", return_value=genesis
            ), mock.patch.object(
                RUNNER, "_source_index", return_value={"source_two": {}, "source_one": {}}
            ), mock.patch.object(RUNNER, "compact_definition", return_value="{}"), mock.patch.object(
                RUNNER, "render_prompt", side_effect=lambda _run, _name, replacements: replacements["FROZEN_ARCHITECTURE_CONTEXT"]
            ):
                prompt, context = RUNNER.architecture_core_prompt(run)
        self.assertEqual(prompt, context)
        self.assertIn("===== ALLOWED GENESIS CLAIMANTS =====\nclaimant_01\n\nclaimant_02", context)
        self.assertIn("===== ALLOWED COMMITTED SOURCES =====\nsource_one\n\nsource_two", context)

    def test_architecture_normalizes_unambiguous_genesis_and_topology_references(self):
        payload = architecture_core_payload()
        payload["obligation_graph"][0] |= {
            "status": "satisfied", "hardness": "soft", "created_by_ids": ["claimant_slot_01"],
            "termination_targets": [], "sources": [source_ref("genesis_work_canon")],
        }
        payload["arcs"][0]["claimant_pressures"] = ["claimant_slot_01"]
        payload["topology"] |= {
            "entry_segment_id": "segment_introduction",
            "opening_branch_node_id": "opening_alias",
            "reconvergence_node_ids": ["node_reconverge"],
        }
        payload["topology"]["nodes"][-1]["node_type"] = "reconvergence"
        records = architecture_genesis_records()
        with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records[kind]), mock.patch.object(
            RUNNER, "_source_index", return_value={"commit_foundation": {}}
        ):
            normalized = RUNNER.normalize_architecture_core_payload(payload, Path("/offline"))
        obligation_record = normalized["obligation_graph"][0]
        self.assertEqual(normalized["arcs"][0]["claimant_pressures"], ["claimant_01"])
        self.assertEqual(obligation_record["created_by_ids"], ["claimant_01"])
        self.assertEqual(obligation_record["sources"][0]["artifact_id"], "commit_foundation")
        self.assertEqual((obligation_record["status"], obligation_record["hardness"]), ("active", "hard"))
        self.assertEqual(obligation_record["termination_targets"], ["attractor_one"])
        self.assertEqual(normalized["topology"]["entry_segment_id"], "node_intro")
        self.assertEqual(normalized["topology"]["opening_branch_node_id"], "node_intro")
        self.assertEqual(normalized["topology"]["reconvergence_node_ids"], ["node_branch_3"])

    def test_architecture_reference_repair_splits_failed_batch_and_preserves_successes(self):
        payload = architecture_core_payload()
        payload["arcs"][0]["claimant_pressures"] = ["claimant_missing"]
        payload["attractors"][0]["prerequisite_obligation_ids"] = ["obligation_missing"]
        records = architecture_genesis_records()
        calls = []

        def repair(_run, _step, _prompt, schema, _transport, validator=None):
            properties = schema["properties"]["resolutions"]["properties"]
            calls.append(list(properties))
            if len(properties) > 1:
                raise RUNNER.PausedError("Architecture repair", "batch failed")
            issue_id, definition = next(iter(properties.items()))
            result = {"resolutions": {issue_id: definition["enum"][0]}}
            if validator:
                validator(result)
            return result, {"usage": {"prompt_tokens": 5, "completion_tokens": 1}}

        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / ".staging").mkdir()
            with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records[kind]), mock.patch.object(
                RUNNER, "_source_index", return_value={"commit_foundation": {}}
            ), mock.patch.object(RUNNER, "request_architecture_analysis", side_effect=repair):
                repaired = RUNNER.repair_architecture_core_payload(
                    run, "architecture_core", payload, "{}", {"usage": {}}, lambda *_args: None
                )
            repair_state = RUNNER.read_json(run / ".staging/architecture_core.repair.json")
        self.assertEqual(len(calls), 3)
        self.assertEqual(repaired["arcs"][0]["claimant_pressures"], ["claimant_01"])
        self.assertEqual(repaired["attractors"][0]["prerequisite_obligation_ids"], ["obligation_one"])
        self.assertEqual(len(repair_state["history"]), 2)

    def test_architecture_coupled_failure_replaces_only_topology(self):
        payload = architecture_core_payload()
        payload["topology"]["edges"].append({
            "edge_id": "edge_3", "from_node_id": "node_intro", "to_node_id": "node_branch_3",
            "relation": "branch", "hard_obligation_ids": [],
        })
        records = architecture_genesis_records()
        replacement = copy.deepcopy(payload["topology"])
        replacement["edges"] = replacement["edges"][:3]

        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / ".staging").mkdir()
            with mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: records[kind]), mock.patch.object(
                RUNNER, "_source_index", return_value={"commit_foundation": {}}
            ), mock.patch.object(
                RUNNER, "request_architecture_analysis",
                return_value=(replacement, {"usage": {"prompt_tokens": 5, "completion_tokens": 1}}),
            ):
                repaired = RUNNER.repair_architecture_core_payload(
                    run, "architecture_core", payload, "{}", {"usage": {}}, lambda *_args: None
                )
                expected = RUNNER.normalize_architecture_core_payload(payload, run)
        self.assertEqual({key: value for key, value in repaired.items() if key != "topology"}, {
            key: value for key, value in expected.items() if key != "topology"
        })
        self.assertEqual(len(repaired["topology"]["edges"]), 3)

    def test_scope_is_dynamic_not_clamped_to_profiles(self):
        scope = RUNNER.derive_scope(150)["scope"]
        self.assertEqual(scope["possible_scene_count"], 150)
        self.assertEqual(scope["profile_guidance"], "cathedral")
        self.assertGreater(scope["literary_packet_target"], 16)

    def test_toolchain_state_is_ignored_and_renpy_is_deferred(self):
        self.assertIn(".cathedrals/", (ROOT / ".gitignore").read_text().splitlines())
        self.assertEqual(RUNNER.renderer_for("visualnovel"), "astro")
        self.assertFalse((RUNNER.RUNTIME_ROOT / "toolchains/renpy").exists())

    def test_web_bootstrap_reuses_compatible_system_node(self):
        def located(name):
            return f"/usr/bin/{name}" if name in {"node", "npm"} else None

        with mock.patch.object(
            RUNNER.shutil, "which", side_effect=located
        ), mock.patch.object(
            RUNNER,
            "run_command",
            return_value=CompletedProcess([], 0, "v22.12.0\n", ""),
        ):
            node, npm = RUNNER.ensure_node(output_fn=lambda _line: None)
        self.assertEqual(node, Path("/usr/bin/node"))
        self.assertEqual(npm, Path("/usr/bin/npm"))

    def test_snapshots_accept_zip_dirty_and_untracked_installations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "zip-install"
            run = Path(temporary) / "run"
            (root / "engine/.git").mkdir(parents=True)
            (root / "cathedrals").write_text("locally modified launcher\n")
            (root / "engine/prompt.md").write_text("locally modified engine\n")
            (root / "engine/untracked.md").write_text("new local engine file\n")
            (root / "engine/.git/HEAD").write_text("arbitrary branch\n")
            run.mkdir()
            with mock.patch.object(RUNNER, "ROOT", root):
                RUNNER.copy_engine_snapshot(run)
            snapshot = run / "engine-snapshot"
            self.assertEqual(
                (snapshot / "cathedrals").read_text(), "locally modified launcher\n"
            )
            self.assertEqual(
                (snapshot / "engine/untracked.md").read_text(),
                "new local engine file\n",
            )
            self.assertFalse((snapshot / "engine/.git").exists())
            self.assertFalse((root / ".git").exists())

    def test_multiple_new_runs_use_their_own_local_engine_snapshots(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copy2(ROOT / "cathedrals", root / "cathedrals")
            shutil.copytree(ROOT / "engine", root / "engine")
            (root / "engine/local-new.md").write_text("local engine input\n")
            runtime = root / ".cathedrals"
            runs = runtime / "runs"
            with mock.patch.object(RUNNER, "ROOT", root), mock.patch.object(
                RUNNER, "RUNTIME_ROOT", runtime
            ), mock.patch.object(RUNNER, "RUNS_ROOT", runs), mock.patch.object(
                RUNNER, "generation_id", side_effect=("generation_a", "generation_b")
            ):
                run_a = RUNNER.create_run(
                    RUNNER.FrozenInputs(possible_scene_count=1),
                    "http://offline.invalid",
                    "offline",
                    lambda _line: None,
                )
                (root / "engine/added-between-runs.md").write_text(
                    "later local engine input\n"
                )
                run_b = RUNNER.create_run(
                    RUNNER.FrozenInputs(possible_scene_count=1),
                    "http://offline.invalid",
                    "offline",
                    lambda _line: None,
                )
            snapshot_a = run_a / "engine-snapshot"
            snapshot_b = run_b / "engine-snapshot"
            self.assertTrue((snapshot_a / "engine/local-new.md").exists())
            self.assertFalse((snapshot_a / "engine/added-between-runs.md").exists())
            self.assertTrue((snapshot_b / "engine/added-between-runs.md").exists())
            self.assertEqual(
                set(RUNNER.read_json(run_a / "run-manifest.json")["engine_snapshot"]),
                {"work_id", "path", "work_seed", "structural_seed", "geomancy_seed"},
            )
            RUNNER.verify_engine_snapshot(run_a)
            RUNNER.verify_engine_snapshot(run_b)

    def test_repeated_generations_keep_independent_engine_snapshots_and_ignore_branch_state(
        self,
    ):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "engine").mkdir()
            (root / ".git").mkdir()
            (root / ".git/HEAD").write_text("branch one\n")
            (root / "cathedrals").write_text("launcher A\n")
            (root / "engine/prompt.md").write_text("engine A\n")
            run_a, run_b = root / "run-a", root / "run-b"
            run_a.mkdir()
            run_b.mkdir()
            with mock.patch.object(RUNNER, "ROOT", root):
                RUNNER.copy_engine_snapshot(run_a)
                (root / ".git/HEAD").write_text("branch two\n")
                (root / "cathedrals").write_text("launcher B\n")
                (root / "engine/prompt.md").write_text("engine B\n")
                (root / "engine/new.md").write_text("new in B\n")
                RUNNER.copy_engine_snapshot(run_b)
            self.assertEqual(
                (run_a / "engine-snapshot/engine/prompt.md").read_text(), "engine A\n"
            )
            self.assertFalse((run_a / "engine-snapshot/engine/new.md").exists())
            self.assertEqual(
                (run_b / "engine-snapshot/engine/prompt.md").read_text(), "engine B\n"
            )
            self.assertTrue((run_b / "engine-snapshot/engine/new.md").exists())
            self.assertNotIn(
                "branch",
                RUNNER.initial_run_state(
                    "generation_test", "a" * 64, "b" * 64, "model"
                ),
            )

    def test_resume_and_publication_do_not_invoke_repository_tools(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / ".cathedrals/runs/generation_test"
            project = run / "projection/web"
            (run / "state").mkdir(parents=True)
            project.mkdir(parents=True)
            (project / "index.html").write_text("fixture")
            RUNNER.save_state(
                run,
                RUNNER.initial_run_state(
                    "generation_test", "a" * 64, "b" * 64, "model"
                ),
            )
            RUNNER.write_json(
                run / "generation-brief.json",
                {"lm_studio_base_url": "http://127.0.0.1:1234", "model": "model"},
            )
            transport = mock.Mock(return_value={"data": [{"id": "model"}]})
            with mock.patch.object(RUNNER, "ROOT", root), mock.patch.object(
                RUNNER, "reconcile_run"
            ), mock.patch.object(RUNNER, "preflight_model_capacity"), mock.patch.object(
                RUNNER.subprocess,
                "run",
                side_effect=AssertionError("external command invoked"),
            ):
                RUNNER.ensure_resume_ready(run, transport=transport)
                destination = RUNNER.publish_success(
                    run, project, {"run_status": "READY_TO_PLAY"}
                )
            self.assertEqual(destination, root / "generated-work/generation_test")
            self.assertTrue((destination / "web/index.html").exists())
            launcher = (ROOT / "cathedrals").read_text()
            self.assertNotIn("def " + "git" + "(", launcher)
            self.assertNotIn('run_command(["git"', launcher)

    def test_resume_dispatches_to_the_run_local_launcher(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            snapshot = run / "engine-snapshot"
            snapshot.mkdir(parents=True)
            (snapshot / "cathedrals").write_text(
                "def main(argv=None, **kwargs):\n    kwargs['output_fn']('snapshot launcher')\n    return 7\n",
                encoding="utf-8",
            )
            output = []
            result = RUNNER.run_snapshot_launcher(run, [], answers(), output.append, None)
            bytecode_caches = list(snapshot.rglob("__pycache__")) + list(snapshot.rglob("*.pyc"))
        self.assertEqual(result, 7)
        self.assertEqual(output, ["snapshot launcher"])
        self.assertEqual(bytecode_caches, [])

    def test_failed_generation_does_not_publish_tracked_provenance(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / ".cathedrals/runs/generation_test"
            (run / "state").mkdir(parents=True)
            RUNNER.save_state(
                run,
                RUNNER.initial_run_state(
                    "generation_test", "a" * 64, "b" * 64, "model"
                ),
            )
            failed = {
                "run_status": "FAILED_GENERATION",
                "completed_at": "2026-01-01T00:00:00Z",
            }
            with mock.patch.object(RUNNER, "ROOT", root), mock.patch.object(
                RUNNER, "make_finalization", return_value=failed
            ):
                RUNNER.finalize_failure(
                    run,
                    RUNNER.CathedralsError("test", "rejected", "artistic_rejection"),
                )
            self.assertFalse((root / "generated-work").exists())
            self.assertTrue((run / "finalization.json").exists())

    def test_web_projection_creates_static_route_families_without_changing_source(self):
        fixture = static_reader_fixture()
        source = fixture["packets"][0]["scenes"][0]["prose_mdx"]
        original_edge = json.dumps(
            fixture["packets"][0]["decision_edges"][0], sort_keys=True
        )
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_fixture"
            run.mkdir()
            RUNNER.write_json(run / "run-manifest.json", fixture["manifest"])
            with mock.patch.object(
                RUNNER, "committed_record", side_effect=lambda _run, kind: fixture[kind]
            ), mock.patch.object(
                RUNNER, "all_committed_records", return_value=fixture["packets"]
            ), mock.patch.object(
                RUNNER, "append_deterministic_step"
            ):
                project, counts = RUNNER.project_web(run)
                first_hash = RUNNER.sha256_file(project / "public/style.css")
                RUNNER.project_web(run)
            self.assertEqual(counts, {"scenes": 2, "artifacts": 1, "endings": 1})
            self.assertEqual(
                (project / "public/source/fixture_introduction.md").read_text(), source
            )
            self.assertEqual(
                RUNNER.sha256_file(project / "public/style.css"), first_hash
            )
            work = RUNNER.read_json(project / "public/work.json")
            self.assertEqual(
                work["decision_edges"][0]["resolved_content_id"],
                "arbitrary_generated_destination",
            )
            self.assertEqual(
                json.dumps(fixture["packets"][0]["decision_edges"][0], sort_keys=True),
                original_edge,
            )
            package = RUNNER.read_json(project / "package.json")
            self.assertEqual(
                package["dependencies"]["markdown-it"], RUNNER.MARKDOWN_IT_VERSION
            )
            renderer = (project / "src/lib/markdown.mjs").read_text()
            scene_template = (project / "src/pages/scenes/[sceneId].astro").read_text()
            self.assertIn("html:false", renderer)
            self.assertIn("set:html={renderMarkdown(scene.prose_mdx)}", scene_template)
            for route in (
                "scenes/[sceneId].astro",
                "artifacts/[artifactId].astro",
                "endings/[endingId].astro",
            ):
                self.assertTrue((project / "src/pages" / route).exists())

    def test_generated_markdown_rejects_authored_html_and_executable_mdx(self):
        for source in (
            "<script>alert(1)</script>",
            "<iframe src='x'></iframe>",
            "<object></object>",
            "<embed>",
            "<style>body{}</style>",
            "<link href='x'>",
            "<meta charset='x'>",
            "<form></form>",
            "<input>",
            "<button>run</button>",
            "<svg/onload=alert(1)>",
            "<!-- authored HTML -->",
            "export const value = 1",
            "export{value}",
        ):
            with self.assertRaises(RUNNER.SchemaError):
                RUNNER.validate_markdown_source(source, "Fixture")
        RUNNER.validate_markdown_source("# Heading\n\n*safe emphasis*", "Fixture")
        RUNNER.validate_markdown_source("See <https://example.invalid>.", "Fixture")

    def test_art_direction_is_deterministic_bounded_and_work_specific(self):
        first = art_direction()
        second = art_direction(
            typography={
                "body_family_class": "humanist_sans",
                "heading_family_class": "engraved_serif",
                "scale": "restrained",
                "tracking": "open",
            },
            spatial_density="compressed",
            border_language="ruled",
            surface_language="terminal",
        )
        self.assertEqual(
            RUNNER.art_direction_css(first), RUNNER.art_direction_css(first)
        )
        self.assertNotEqual(
            RUNNER.art_direction_css(first), RUNNER.art_direction_css(second)
        )
        self.assertNotIn(first["visual_thesis"], RUNNER.art_direction_css(first))
        light = RUNNER.light_art_direction_palette(first)
        for foreground, minimum in (
            ("text", 4.5),
            ("muted", 4.5),
            ("accent", 3.0),
            ("danger", 3.0),
        ):
            self.assertGreaterEqual(
                RUNNER.contrast_ratio(light[foreground], light["background"]), minimum
            )
            self.assertGreaterEqual(
                RUNNER.contrast_ratio(light[foreground], light["surface"]), minimum
            )

    def test_art_direction_schema_rejects_invalid_values_and_code_fields(self):
        protocol = RUNNER.load_protocol()
        for invalid in (
            art_direction(border_language="freeform_css"),
            art_direction(palette=art_direction()["palette"] | {"accent": "red"}),
            art_direction(css="body{position:fixed}"),
            art_direction(javascript="alert(1)"),
        ):
            with self.assertRaises(RUNNER.SchemaError):
                RUNNER.validate_json_schema(
                    invalid, protocol["$defs"]["webArtDirection"], protocol
                )

    def test_art_direction_corrects_insufficient_contrast(self):
        low_contrast = art_direction(
            palette=art_direction()["palette"] | {"muted": "#whatever"}
        )

        palette = RUNNER.accessible_art_direction_palette(low_contrast)

        for foreground, minimum in (
            ("text", 4.5),
            ("muted", 4.5),
            ("accent", 3.0),
            ("danger", 3.0),
        ):
            self.assertGreaterEqual(
                RUNNER.contrast_ratio(
                    palette[foreground],
                    palette["background"],
                ),
                minimum,
            )
            self.assertGreaterEqual(
                RUNNER.contrast_ratio(
                    palette[foreground],
                    palette["surface"],
                ),
                minimum,
            )

    def test_cross_packet_technical_destinations_resolve_without_mutating_edges(self):
        fixture = static_reader_fixture()
        scenes = [item for packet in fixture["packets"] for item in packet["scenes"]]
        endings = [item for packet in fixture["packets"] for item in packet["endings"]]
        edges = [
            item for packet in fixture["packets"] for item in packet["decision_edges"]
        ]
        before = json.dumps(edges, sort_keys=True)
        resolved, _ = RUNNER.resolve_cross_packet_links(scenes, endings, edges)
        self.assertEqual(
            resolved[0]["resolved_content_id"], "arbitrary_generated_destination"
        )
        self.assertEqual(resolved[1]["resolved_content_id"], "fixture_ending")
        self.assertEqual(json.dumps(edges, sort_keys=True), before)

    def test_cross_packet_resolution_rejects_missing_and_duplicate_slots(self):
        scene = {"technical_slot_id": "scene_slot_one", "scene_id": "scene_one"}
        edge = {"destination": {"kind": "technical_slot", "id": "scene_slot_missing"}}
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.resolve_cross_packet_links([scene], [], [edge])
        duplicate = {
            "technical_slot_id": "scene_slot_one",
            "ending_id": "ending_one",
            "redirect_destination": None,
        }
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.resolve_cross_packet_links([scene], [duplicate], [])

    def test_redirect_to_future_ending_slot_resolves(self):
        endings = [
            {
                "technical_slot_id": "ending_slot_one",
                "ending_id": "ending_one",
                "redirect_destination": {
                    "kind": "technical_slot",
                    "id": "ending_slot_two",
                },
            },
            {
                "technical_slot_id": "ending_slot_two",
                "ending_id": "ending_generated_name",
                "redirect_destination": None,
            },
        ]
        _, resolved = RUNNER.resolve_cross_packet_links([], endings, [])
        self.assertEqual(
            resolved[0]["resolved_redirect_content_id"], "ending_generated_name"
        )

    def test_append_helpers_refuse_rewrite_and_preserve_ledger_prefix(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / "state").mkdir()
            RUNNER.save_state(
                run,
                RUNNER.initial_run_state(
                    "generation_test", "a" * 64, "b" * 64, "model"
                ),
            )
            RUNNER.append_deterministic_step(run, "preflight", "preflight", "c" * 64)
            first = (run / "ledger.jsonl").read_bytes()
            RUNNER.append_deterministic_step(run, "preflight", "preflight", "d" * 64)
            self.assertEqual((run / "ledger.jsonl").read_bytes(), first)
            immutable = run / "committed.json"
            RUNNER.write_json(immutable, {"value": 1}, exclusive=True)
            with self.assertRaises(RUNNER.IntegrityError):
                RUNNER.write_json(immutable, {"value": 2}, exclusive=True)

    def test_canonical_fact_event_preserves_immutable_source_provenance(self):
        fact = {
            "fact_id": "fact_archive_destroyed",
            "subject": "room_archive",
            "predicate": "destroyed",
            "value": True,
            "status": "established",
            "sources": [source_ref()],
            "relevance": {"location_ids": ["room_archive"]},
        }
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / "state").mkdir()
            (run / "constraints").mkdir()
            RUNNER.write_json(
                run / "state/source-index.json",
                {"scene_old": {"commit_id": "commit_source", "hash": "a" * 64}},
            )
            record = {
                "record_type": "fixture",
                "generation_id": "generation_test",
                "commit_id": "commit_packet",
                "constraint_delta": empty_delta(canonical_facts=[fact]),
            }
            event = RUNNER.make_constraint_events(
                run, record, "commit_packet", "b" * 64, "packet_one"
            )[0]
        self.assertEqual(event["sources"][0]["source_commit_id"], "commit_source")
        self.assertEqual(event["sources"][0]["source_hash"], "a" * 64)

    def test_character_knowledge_is_distinct_from_world_truth(self):
        fact = constraint_event(
            1,
            "canonical_fact",
            {
                "fact_id": "fact_truth",
                "subject": "room_archive",
                "predicate": "destroyed",
                "value": True,
                "status": "established",
                "relevance": {},
            },
        )
        ignorance = constraint_event(
            2,
            "knowledge_state",
            {
                "knowledge_id": "knowledge_ignorance",
                "subject_id": "character_one",
                "relation": "explicitly_does_not_know",
                "proposition_id": "fact_truth",
                "action": "establish",
                "relevance": {},
            },
            source="scene_new",
        )
        facts, knowledge, _, _, _ = RUNNER.project_constraint_state([fact, ignorance])
        self.assertTrue(facts["fact_truth"]["data"]["value"])
        self.assertIn(
            "fact_truth", knowledge["character_one"]["explicitly_does_not_know"]
        )

    def test_active_obligation_survives_later_packets(self):
        debt = constraint_event(1, "obligation", obligation(), "future_obligation")
        later_fact = constraint_event(
            2,
            "canonical_fact",
            {
                "fact_id": "fact_later",
                "subject": "room_archive",
                "predicate": "sealed",
                "value": True,
                "status": "established",
                "relevance": {},
            },
        )
        _, _, obligations, _, _ = RUNNER.project_constraint_state([debt, later_fact])
        self.assertEqual(obligations["obligation_one"]["data"]["status"], "active")

    def test_satisfied_obligation_retains_evidence(self):
        debt = constraint_event(1, "obligation", obligation(), "future_obligation")
        update = constraint_event(
            2,
            "obligation_update",
            {
                "update_id": "update_paid",
                "obligation_id": "obligation_one",
                "status": "satisfied",
                "reason": "The copied register was recovered.",
            },
            "future_obligation",
            source="scene_new",
            action="satisfy",
        )
        _, _, obligations, _, _ = RUNNER.project_constraint_state([debt, update])
        resolved = obligations["obligation_one"]
        self.assertEqual(resolved["data"]["status"], "satisfied")
        self.assertEqual(
            resolved["resolution_event"]["sources"][0]["artifact_id"], "scene_new"
        )

    def test_ending_attractor_has_backward_prerequisite_chain(self):
        obligations = [
            obligation(
                "obligation_encounter",
                requires=[],
                termination_targets=["obligation_interpretation"],
            ),
            obligation(
                "obligation_interpretation",
                requires=["obligation_encounter"],
                termination_targets=["obligation_one"],
            ),
            obligation("obligation_one", requires=["obligation_interpretation"]),
        ]
        architecture = architecture_fixture(obligations=obligations)
        self.assertEqual(
            architecture["attractors"][0]["prerequisite_obligation_ids"],
            ["obligation_one"],
        )
        self.assertEqual(
            architecture["obligation_graph"][2]["requires"],
            ["obligation_interpretation"],
        )

    def test_architecture_rejects_hard_obligation_with_unknown_origin(self):
        with self.assertRaisesRegex(RUNNER.SchemaError, "unknown origin"):
            RUNNER.validate_obligation_origins(
                [obligation(created_by_ids=["missing_origin"])],
                {"attractor_one"},
                "Architecture obligation",
            )

    def test_ending_context_labels_prerequisites_and_reader_state(self):
        reader_fact = constraint_event(
            1,
            "canonical_fact",
            {
                "fact_id": "fact_reader_state",
                "subject": "reader",
                "predicate": "documented",
                "value": True,
                "status": "established",
                "relevance": {"state_keys": ["reader_documented"]},
            },
        )
        satisfied = constraint_event(
            2, "obligation", obligation(status="satisfied"), "future_obligation"
        )
        satisfied["resolution_event"] = constraint_event(
            3,
            "obligation_update",
            {
                "update_id": "update_one",
                "obligation_id": "obligation_one",
                "status": "satisfied",
                "reason": "Established.",
            },
            "future_obligation",
        )
        plan = packet_plan(
            packet_kind="ending",
            scene_slot_ids=[],
            ending_slot_ids=["ending_slot_0001"],
            advance_obligation_ids=[],
            may_satisfy_obligation_ids=[],
        )
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / "state").mkdir()
            (run / "state/frozen-engine-context.txt").write_text(
                "law", encoding="utf-8"
            )
            RUNNER.write_json(
                run / "run-manifest.json",
                {
                    "generation_brief": {},
                    "budgets": {
                        "max_retrieved_source_tokens": 100,
                        "max_prepared_context_tokens": 20000,
                    },
                },
            )
            RUNNER.write_json(
                run / "state/canonical-facts.json", {"fact_reader_state": reader_fact}
            )
            RUNNER.write_json(
                run / "state/obligations.json", {"obligation_one": satisfied}
            )
            for name in ("knowledge-state.json", "motifs.json"):
                RUNNER.write_json(run / f"state/{name}", {})
            with mock.patch.object(
                RUNNER, "committed_record", return_value={"record_type": "genesis"}
            ), mock.patch.object(
                RUNNER, "all_committed_records", return_value=[]
            ), mock.patch.object(
                RUNNER,
                "select_relevant_constraints",
                return_value=[reader_fact, satisfied],
            ), mock.patch.object(
                RUNNER, "retrieve_original_sources", return_value=[]
            ), mock.patch.object(
                RUNNER, "ensure_frozen_geomancy", return_value={"assignments": []}
            ):
                context = RUNNER.relevant_packet_context(
                    run, architecture_fixture(), plan
                )
        self.assertIn("===== ENDING ATTRACTOR =====", context)
        self.assertIn("===== BACKWARD PREREQUISITE CHAIN =====", context)
        self.assertIn("===== SATISFIED PREREQUISITES WITH SOURCES =====", context)
        self.assertIn("===== CURRENT READER STATE =====", context)

    def test_packet_context_includes_only_selected_current_character_knowledge(self):
        selected = constraint_event(
            1,
            "knowledge_state",
            {
                "knowledge_id": "knowledge_selected",
                "subject_id": "character_one",
                "relation": "suspects",
                "proposition_id": "fact_selected",
                "action": "establish",
                "relevance": {"character_ids": ["character_one"]},
            },
        )
        unrelated = constraint_event(
            2,
            "knowledge_state",
            {
                "knowledge_id": "knowledge_unrelated",
                "subject_id": "character_one",
                "relation": "suspects",
                "proposition_id": "fact_unrelated",
                "action": "establish",
                "relevance": {"character_ids": ["character_one"]},
            },
        )
        _, knowledge, _, _, _ = RUNNER.project_constraint_state([selected, unrelated])
        plan = packet_plan(advance_obligation_ids=[], may_satisfy_obligation_ids=[])
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / "state").mkdir()
            (run / "state/frozen-engine-context.txt").write_text(
                "law", encoding="utf-8"
            )
            RUNNER.write_json(
                run / "run-manifest.json",
                {
                    "generation_brief": {},
                    "budgets": {
                        "max_retrieved_source_tokens": 100,
                        "max_prepared_context_tokens": 20000,
                    },
                },
            )
            for name, value in (
                ("canonical-facts.json", {}),
                ("knowledge-state.json", knowledge),
                ("obligations.json", {}),
                ("motifs.json", {}),
            ):
                RUNNER.write_json(run / f"state/{name}", value)
            with mock.patch.object(
                RUNNER, "committed_record", return_value={"record_type": "genesis"}
            ), mock.patch.object(
                RUNNER, "all_committed_records", return_value=[]
            ), mock.patch.object(
                RUNNER, "select_relevant_constraints", return_value=[selected]
            ), mock.patch.object(
                RUNNER, "retrieve_original_sources", return_value=[]
            ), mock.patch.object(
                RUNNER, "ensure_frozen_geomancy", return_value={"assignments": []}
            ):
                context = RUNNER.relevant_packet_context(
                    run, architecture_fixture(), plan
                )
        self.assertIn("knowledge_selected", context)
        self.assertNotIn("knowledge_unrelated", context)

    def test_prospective_plan_may_change_without_changing_canon(self):
        first = obligation("obligation_one", termination_targets=["packet_one"])
        second = obligation(
            "obligation_two",
            created_by_ids=["attractor_one"],
            termination_targets=["packet_two"],
        )
        plans = [
            packet_plan("packet_one"),
            packet_plan("packet_two", initial_priority=2),
        ]
        architecture = architecture_fixture(plans=plans, obligations=[first, second])
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            for name in ("state", "committed", "planning"):
                (run / name).mkdir(parents=True)
            state = RUNNER.initial_run_state(
                "generation_test", "a" * 64, "b" * 64, "model"
            )
            RUNNER.save_state(run, state)
            one = constraint_event(1, "obligation", first, "future_obligation")
            two = constraint_event(2, "obligation", second, "future_obligation")
            _, _, obligations, _, _ = RUNNER.project_constraint_state([one, two])
            RUNNER.write_json(run / "state/obligations.json", obligations)
            RUNNER.write_json(run / "state/foreclosure-candidates.json", {})
            before = RUNNER.build_prospective_plan(
                run, architecture, "commit_architecture"
            )
            obligations["obligation_one"]["data"]["status"] = "satisfied"
            RUNNER.write_json(run / "state/obligations.json", obligations)
            after = RUNNER.build_prospective_plan(run, architecture, "commit_packet")
            self.assertEqual(RUNNER.load_state(run)["canonical_state_hash"], "b" * 64)
        self.assertNotEqual(
            before["packet_order"][0]["packet_slot_id"],
            after["packet_order"][0]["packet_slot_id"],
        )

    def test_prospective_change_cannot_change_committed_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "scene.md"
            source.write_text("immutable scene bytes")
            before = RUNNER.sha256_file(source)
            RUNNER.evaluate_feasibility(
                architecture_fixture(),
                {
                    "obligation_one": constraint_event(
                        1, "obligation", obligation(), "future_obligation"
                    )
                },
                {},
            )
            self.assertEqual(RUNNER.sha256_file(source), before)

    def test_lawful_committed_fact_can_foreclose_foreclosable_attractor(self):
        impossible = obligation(status="impossible")
        obligations = {
            "obligation_one": constraint_event(
                1, "obligation", impossible, "future_obligation"
            )
        }
        candidate_data = {
            "foreclosure_id": "foreclosure_one",
            "attractor_id": "attractor_one",
            "negated_prerequisite_obligation_ids": ["obligation_one"],
            "reason": "Committed death negated survival.",
        }
        candidates = {
            "foreclosure_one": constraint_event(
                2,
                "foreclosure_candidate",
                candidate_data,
                "prospective_foreclosure",
                action="establish",
            )
        }
        result = RUNNER.evaluate_feasibility(
            architecture_fixture(), obligations, candidates
        )
        self.assertEqual(result[0]["status"], "foreclosed")

    def test_universal_hard_obligation_cannot_be_foreclosed(self):
        impossible = obligation(status="impossible", universality="universal")
        obligations = {
            "obligation_one": constraint_event(
                1, "obligation", impossible, "future_obligation"
            )
        }
        candidate_data = {
            "foreclosure_id": "foreclosure_one",
            "attractor_id": "attractor_one",
            "negated_prerequisite_obligation_ids": ["obligation_one"],
            "reason": "Attempted loophole.",
        }
        candidates = {
            "foreclosure_one": constraint_event(
                2, "foreclosure_candidate", candidate_data, "prospective_foreclosure"
            )
        }
        result = RUNNER.evaluate_feasibility(
            architecture_fixture(), obligations, candidates
        )
        self.assertEqual(result[0]["status"], "universally_required_but_impossible")

    def test_relevance_selects_older_hard_fact_over_new_irrelevant_record(self):
        architecture = architecture_fixture()
        plan = packet_plan() | {
            "advance_obligation_ids": ["obligation_one"],
            "may_satisfy_obligation_ids": [],
        }
        old = constraint_event(1, "obligation", obligation(), "future_obligation")
        new = constraint_event(
            100,
            "canonical_fact",
            {
                "fact_id": "fact_irrelevant",
                "subject": "other_room",
                "predicate": "painted",
                "value": True,
                "status": "established",
                "relevance": {"location_ids": ["other_room"]},
            },
        )
        self.assertGreater(
            RUNNER.relevance_score(old, plan, architecture, set(), 100),
            RUNNER.relevance_score(new, plan, architecture, set(), 100),
        )

    def test_recency_bonus_is_not_dominant(self):
        architecture = architecture_fixture()
        plan = packet_plan() | {
            "advance_obligation_ids": ["obligation_one"],
            "may_satisfy_obligation_ids": [],
        }
        old = constraint_event(1, "obligation", obligation(), "future_obligation")
        new = constraint_event(
            1000,
            "canonical_fact",
            {
                "fact_id": "fact_recent",
                "subject": "other_room",
                "predicate": "painted",
                "value": True,
                "status": "established",
                "relevance": {},
            },
        )
        old_score = RUNNER.relevance_score(old, plan, architecture, set(), 1000)
        new_score = RUNNER.relevance_score(new, plan, architecture, set(), 1000)
        self.assertGreaterEqual(old_score - new_score, 10)

    def test_context_budget_keeps_hard_constraint_before_recent_prose(self):
        context = RUNNER.bounded_context(
            [
                ("HARD PAST CONSTRAINTS", "room_archive destroyed"),
                ("RECENT LOCAL SOURCE", "x" * 500),
            ],
            16,
        )
        self.assertIn("room_archive destroyed", context)
        self.assertNotIn("RECENT LOCAL SOURCE", context)

    def test_original_evidence_is_retrieved_for_selected_constraint(self):
        event = constraint_event(
            1,
            "canonical_fact",
            {
                "fact_id": "fact_old",
                "subject": "room_archive",
                "predicate": "destroyed",
                "value": True,
                "status": "established",
                "relevance": {},
            },
        )
        packet = {
            "record_type": "creative_packet",
            "scenes": [{"scene_id": "scene_old", "prose_mdx": "original passage"}],
            "artifacts": [],
            "endings": [],
            "formal_compositions": [],
        }
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            commit = run / "committed/0001-packet"
            commit.mkdir(parents=True)
            RUNNER.write_json(commit / "record.json", packet)
            retrieved = RUNNER.retrieve_original_sources(run, [event])
        self.assertEqual(
            retrieved[0]["immutable_source"]["prose_mdx"], "original passage"
        )
        self.assertEqual(retrieved[0]["source_locator"], "prose_mdx#relevant")

    def test_new_long_range_obligation_is_in_future_graph(self):
        protocol = RUNNER.load_protocol()
        debt = obligation("obligation_new", termination_targets=["packet_future"])
        RUNNER.validate_json_schema(debt, protocol["$defs"]["obligation"], protocol)
        event = constraint_event(1, "obligation", debt, "future_obligation")
        _, _, obligations, _, _ = RUNNER.project_constraint_state([event])
        self.assertIn("obligation_new", obligations)

    def test_ending_cannot_commit_without_required_prerequisite(self):
        ending = {
            "attractor_id": "attractor_one",
            "satisfied_prerequisite_obligation_ids": ["obligation_one"],
            "prerequisite_evidence_source_ids": ["scene_old"],
        }
        state = {
            "obligation_one": constraint_event(
                1, "obligation", obligation(), "future_obligation"
            )
        }
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_ending_prerequisites(
                ending,
                {"attractor_one": attractor()},
                state,
                {"attractor_one": "viable"},
                {"scene_old"},
            )

    def test_motif_occurrence_updates_pressure_and_provenance(self):
        first = constraint_event(
            1,
            "motif_state",
            {
                "motif_event_id": "motif_event_one",
                "motif_id": "motif_frost",
                "action": "appear",
                "current_function": "warning",
                "pressure": "Transform before recurrence.",
                "overuse_risk": "elevated",
                "relevance": {},
            },
            "motif_pressure",
        )
        second = constraint_event(
            2,
            "motif_state",
            {
                "motif_event_id": "motif_event_two",
                "motif_id": "motif_frost",
                "action": "transform",
                "current_function": "evidence",
                "pressure": "Do not repeat as wallpaper.",
                "overuse_risk": "low",
                "relevance": {},
            },
            "motif_pressure",
            source="scene_new",
            action="update",
        )
        _, _, _, motifs, _ = RUNNER.project_constraint_state([first, second])
        self.assertEqual(motifs["motif_frost"]["current_function"], "evidence")
        self.assertEqual(
            motifs["motif_frost"]["appearances"], ["scene_old", "scene_new"]
        )

    def test_recursive_summary_never_substitutes_for_original_source(self):
        event = constraint_event(
            1,
            "canonical_fact",
            {
                "fact_id": "fact_summary",
                "subject": "room_archive",
                "predicate": "summary",
                "value": "derived wording",
                "status": "established",
                "relevance": {},
            },
        )
        packet = {
            "record_type": "creative_packet",
            "scenes": [{"scene_id": "scene_old", "prose_mdx": "source wording"}],
            "artifacts": [],
            "endings": [],
            "formal_compositions": [],
        }
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            commit = run / "committed/0001-packet"
            commit.mkdir(parents=True)
            RUNNER.write_json(commit / "record.json", packet)
            retrieved = RUNNER.retrieve_original_sources(run, [event])
        self.assertEqual(
            retrieved[0]["immutable_source"]["prose_mdx"], "source wording"
        )

    def test_analysis_protocol_cannot_return_replacement_prose(self):
        protocol = RUNNER.load_protocol()
        self.assertNotIn("indexBatch", protocol["$defs"])
        plan = {
            "record_type": "prospective_plan",
            "protocol_version": "6.0",
            "generation_id": "generation_test",
            "plan_id": "prospective_plan_0001",
            "based_on_canonical_state_hash": "a" * 64,
            "recomputed_after_commit_id": "commit_architecture",
            "created_at": "2026-01-01T00:00:00Z",
            "feasibility": [],
            "obligation_assignments": [],
            "packet_order": [],
            "replacement_prose": "forbidden",
        }
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(
                plan, protocol["$defs"]["prospectivePlan"], protocol
            )

    def test_prospective_recomputation_does_not_increment_irreversibility_counters(
        self,
    ):
        architecture = architecture_fixture()
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            for name in ("state", "committed/0001-architecture", "planning"):
                (run / name).mkdir(parents=True)
            RUNNER.save_state(
                run,
                RUNNER.initial_run_state(
                    "generation_test", "a" * 64, "b" * 64, "model"
                ),
            )
            RUNNER.write_json(
                run / "committed/0001-architecture/record.json", architecture
            )
            debt = constraint_event(1, "obligation", obligation(), "future_obligation")
            _, _, obligations, _, _ = RUNNER.project_constraint_state([debt])
            RUNNER.write_json(run / "state/obligations.json", obligations)
            RUNNER.write_json(run / "state/foreclosure-candidates.json", {})
            RUNNER.recompute_prospective_plan(run, "commit_architecture")
            state = RUNNER.load_state(run)
        self.assertEqual(
            [
                state[key]
                for key in (
                    "committed_rewrite_count",
                    "committed_regeneration_count",
                    "backtrack_count",
                )
            ],
            [0, 0, 0],
        )

    def test_artistic_review_is_not_a_publication_gate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / ".cathedrals/runs/generation_test"
            project = run / "projection/web"
            project.mkdir(parents=True)
            RUNNER.write_json(run / "generation-brief.json", {"project_name": "Fixture"})
            order = []

            def build(_run, _project, _output):
                order.append("build")
                (_project / "dist").mkdir()
                (_project / "dist/index.html").write_text("fixture", encoding="utf-8")
                return {"result": "PASS", "reasons": ["built"]}

            build_path = project / "dist"
            with mock.patch.object(RUNNER, "ROOT", root), mock.patch.object(
                RUNNER,
                "execute_creative_phases",
                side_effect=lambda *_: order.append("creative"),
            ), mock.patch.object(
                RUNNER,
                "project_web",
                side_effect=lambda *_: (
                    order.append("projection")
                    or (project, {"scenes": 2, "artifacts": 1, "endings": 1})
                ),
            ), mock.patch.object(
                RUNNER,
                "validate_complete_work",
                side_effect=lambda *_: (
                    order.append("mechanical")
                    or {"result": "PASS", "reasons": ["valid"]}
                ),
            ), mock.patch.object(
                RUNNER, "build_web", side_effect=build
            ), mock.patch.object(RUNNER, "artistic_acceptance") as artistic, mock.patch.object(
                RUNNER, "finalize_success", side_effect=lambda *_: (order.append("finalize") or (build_path, {}))
            ):
                result, _, _ = RUNNER.execute_run(run, output_fn=lambda _line: None)
        self.assertEqual(result, build_path)
        self.assertEqual(order, ["creative", "projection", "mechanical", "build", "finalize"])
        artistic.assert_not_called()

    def test_mechanically_valid_work_reaches_ready_finalizer_without_artistic_call(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            project = run / "projection/web"
            order = []
            build_path = project / "dist"
            with mock.patch.object(
                RUNNER,
                "execute_creative_phases",
                side_effect=lambda *_: order.append("creative"),
            ), mock.patch.object(
                RUNNER,
                "project_web",
                side_effect=lambda *_: (
                    order.append("projection")
                    or (project, {"scenes": 1, "artifacts": 1, "endings": 1})
                ),
            ), mock.patch.object(
                RUNNER,
                "validate_complete_work",
                side_effect=lambda *_: (
                    order.append("mechanical")
                    or {"result": "PASS", "reasons": ["valid"]}
                ),
            ), mock.patch.object(
                RUNNER,
                "build_web",
                side_effect=lambda *_: (
                    order.append("build") or {"result": "PASS", "reasons": ["built"]}
                ),
            ), mock.patch.object(RUNNER, "artistic_acceptance") as artistic, mock.patch.object(
                RUNNER,
                "finalize_success",
                side_effect=lambda *_: (order.append("finalize") or (build_path, {})),
            ), mock.patch.object(
                RUNNER, "read_json", return_value={"project_name": "Fixture"}
            ):
                result, _, _ = RUNNER.execute_run(run, output_fn=lambda _line: None)
        self.assertEqual(result, build_path)
        self.assertEqual(
            order,
            ["creative", "projection", "mechanical", "build", "finalize"],
        )
        artistic.assert_not_called()

    def test_two_thousand_scene_scope_uses_bounded_plan_batches(self):
        core = {
            "scope_commitment": {
                "planned_scene_count": 2000,
                "planned_ending_count": 285,
                "planned_artifact_count": 400,
                "planned_formal_composition_count": 80,
            }
        }
        specs = RUNNER.planned_packet_specs(core)
        literary = [item for item in specs if item["packet_kind"] == "literary"]
        endings = [item for item in specs if item["packet_kind"] == "ending"]
        self.assertEqual(sum(len(item["scene_slot_ids"]) for item in literary), 2000)
        self.assertEqual(sum(len(item["ending_slot_ids"]) for item in endings), 285)
        self.assertTrue(all(3 <= len(item["scene_slot_ids"]) <= 8 for item in literary))
        self.assertTrue(all(2 <= len(item["ending_slot_ids"]) <= 6 for item in endings))
        self.assertTrue(
            all(
                len(batch) <= RUNNER.PLAN_BATCH_SIZE
                for batch in RUNNER.plan_batches(core)
            )
        )
        geomancy_slots = {
            item["technical_slot_id"]
            for item in RUNNER.precompute_geomancy("scale-seed", 2000)["assignments"]
        }
        self.assertEqual(
            {slot for item in literary for slot in item["scene_slot_ids"]},
            geomancy_slots,
        )
        self.assertGreaterEqual(
            RUNNER.derive_scope(2000)["budgets"]["max_creative_step_count"], 2000 + 285
        )

    def test_scene_length_is_flexible_inside_packet_budget(self):
        long_scene = " ".join(["word"] * 1200)
        packet = {"scenes": [{"prose_mdx": long_scene}], "artifacts": [], "endings": []}
        self.assertEqual(RUNNER.packet_literary_word_count(packet), 1200)
        self.assertLess(
            RUNNER.packet_literary_word_count(packet), RUNNER.PACKET_LITERARY_WORDS
        )
        schema = RUNNER.load_protocol()["$defs"]["scene"]["properties"]["prose_mdx"]
        self.assertNotIn("maxLength", schema)

    def test_truncated_packet_is_bisected_without_committing_partial_output(self):
        plan = {
            "packet_slot_id": "literary_packet_0001",
            "packet_kind": "literary",
            "scene_slot_ids": [f"scene_slot_{number:04d}" for number in range(1, 7)],
            "ending_slot_ids": [],
            "artifact_count": 4,
            "formal_composition_count": 2,
            "advance_obligation_ids": ["obligation_one"],
            "may_satisfy_obligation_ids": ["obligation_one"],
            "branch_path_relation": "branch",
        }
        calls = []

        def request(*_args, **kwargs):
            calls.append(kwargs)
            if len(calls) == 1:
                raise RUNNER.TruncationError("truncated")

        with mock.patch.object(
            RUNNER, "packet_prompt", return_value=("prompt", "context")
        ), mock.patch.object(
            RUNNER, "step_was_truncated", return_value=False
        ), mock.patch.object(
            RUNNER, "request_record", side_effect=request
        ):
            RUNNER.request_packet_slice(
                Path("/offline"), {}, plan, transport=lambda *_args, **_kwargs: None
            )
        self.assertEqual(len(calls), 3)
        self.assertNotIn("max_tokens", calls[1])
        self.assertNotIn("max_tokens", calls[2])

    def test_truncated_provider_response_is_preserved_and_ledgered(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            for name in ("state", "raw", "committed", "constraints", ".staging"):
                (run / name).mkdir(parents=True)
            RUNNER.save_state(
                run, RUNNER.initial_run_state(run.name, "a" * 64, "b" * 64, "offline")
            )
            RUNNER.write_json(
                run / "generation-brief.json",
                {
                    "generation_seed": "seed",
                    "lm_studio_base_url": "http://offline.invalid",
                },
            )
            RUNNER.write_json(
                run / "run-manifest.json",
                {
                    "budgets": {"max_prepared_context_tokens": 49152},
                },
            )
            response = {
                "choices": [
                    {"finish_reason": "length", "message": {"content": "partial"}}
                ],
                "usage": {"prompt_tokens": 100, "completion_tokens": 200},
            }
            with self.assertRaises(RUNNER.TruncationError):
                RUNNER.request_record(
                    run,
                    expected_record_type="genesis_foundation",
                    step_id="genesis_foundation",
                    phase="genesis",
                    prompt="prompt",
                    context="context",
                    branch_relation="foundation",
                    temperature=0.8,
                    transport=lambda *_args, **_kwargs: response,
                )
            entries = RUNNER.ledger_entries(run)
            self.assertEqual(entries[-1]["failure_class"], "provider_truncation")
            self.assertEqual(entries[-1]["token_accounting"]["output_tokens"], 200)
            self.assertTrue(
                next((run / "raw").glob("genesis_foundation-attempt*.api.json"), None)
            )
            self.assertEqual(list((run / "committed").iterdir()), [])

    def test_invalid_uncommitted_payload_gets_three_corrections_then_pauses(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            for name in ("state", "raw", "committed", "constraints", ".staging"):
                (run / name).mkdir(parents=True)
            RUNNER.save_state(run, RUNNER.initial_run_state(run.name, "a" * 64, "b" * 64, "offline"))
            RUNNER.write_json(run / "generation-brief.json", {"generation_seed": "seed", "lm_studio_base_url": "http://offline.invalid"})
            RUNNER.write_json(run / "run-manifest.json", {"budgets": {"max_prepared_context_tokens": 49152}})
            calls = []

            def invalid(*args, **_kwargs):
                calls.append(args[2])
                return {"choices": [{"finish_reason": "stop", "message": {"content": "{}"}}]}

            with self.assertRaises(RUNNER.PausedError):
                RUNNER.request_record(
                    run, expected_record_type="genesis_foundation", step_id="correction_test", phase="genesis",
                    prompt="prompt", context="context", branch_relation="foundation", temperature=0.8,
                    response_definition="claimantAnchorPayload", transport=invalid,
                )
            self.assertEqual(len(calls), 3)
            self.assertEqual(calls[2]["messages"][1]["content"].count("CORRECTION REQUIRED"), 2)
            self.assertEqual(len(RUNNER.ledger_entries(run)), 3)
            self.assertFalse((run / "finalization.json").exists())

    def test_schema_valid_artistic_payload_is_reused_after_pause(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary) / "generation_test"
            for name in ("state", "raw", "committed", "constraints", ".staging"):
                (run / name).mkdir(parents=True)
            RUNNER.save_state(run, RUNNER.initial_run_state(run.name, "a" * 64, "b" * 64, "offline"))
            RUNNER.write_json(run / "generation-brief.json", {"generation_seed": "seed", "lm_studio_base_url": "http://offline.invalid"})
            RUNNER.write_json(run / "run-manifest.json", {"budgets": {"max_prepared_context_tokens": 49152}})
            response = {"choices": [{"finish_reason": "stop", "message": {"content": '{"name":"Anchor","incident_role":"Witness"}'}}]}
            transport = mock.Mock(return_value=response)

            def paused(_payload):
                raise RUNNER.PausedError("Semantic normalization", "pause")

            arguments = dict(
                expected_record_type="genesis_foundation", step_id="staged_test", phase="genesis",
                prompt="prompt", context="context", branch_relation="foundation", temperature=0.8,
                response_definition="claimantAnchorPayload", record_builder=paused,
                payload_preserver=lambda payload, content, api: RUNNER.preserve_artistic_payload(run, "staged_test", payload, content, api),
            )
            with self.assertRaises(RUNNER.PausedError):
                RUNNER.request_record(run, transport=transport, **arguments)
            with self.assertRaises(RUNNER.PausedError):
                RUNNER.request_record(run, transport=mock.Mock(side_effect=AssertionError("artistic payload regenerated")), **arguments)
            self.assertEqual(transport.call_count, 1)
            self.assertTrue((run / ".staging/staged_test.artistic.json").exists())

    def test_dependency_free_baseline_does_not_invoke_npm(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "web"
            (project / "public").mkdir(parents=True)
            fixture = static_reader_fixture()
            scenes = [item for packet in fixture["packets"] for item in packet["scenes"]]
            artifacts = [item for packet in fixture["packets"] for item in packet["artifacts"]]
            endings = [item for packet in fixture["packets"] for item in packet["endings"]]
            edges = [item for packet in fixture["packets"] for item in packet["decision_edges"]]
            resolved_edges, resolved_endings = RUNNER.resolve_cross_packet_links(scenes, endings, edges)
            work = {
                "generation_id": "generation_test", "project_name": "Fixture",
                "generated_title": fixture["genesis"]["work_canon"]["generated_title"],
                "entry_content_id": scenes[0]["scene_id"], "scenes": scenes,
                "artifacts": artifacts, "endings": resolved_endings, "decision_edges": resolved_edges,
            }
            RUNNER.write_json(project / "public/work.json", work)
            for name in ("style.css", "state.js", "theme.js"):
                (project / "public" / name).write_text("", encoding="utf-8")
            with mock.patch.object(RUNNER, "ensure_node", side_effect=AssertionError("npm invoked")):
                RUNNER.build_static_baseline(project)
            self.assertTrue((project / "dist/index.html").exists())
            self.assertTrue((project / "dist/work.json").exists())

    def test_single_scene_truncation_gets_one_expanded_retry(self):
        plan = {
            "packet_slot_id": "literary_packet_0001",
            "packet_kind": "literary",
            "scene_slot_ids": ["scene_slot_0001"],
            "ending_slot_ids": [],
            "artifact_count": 0,
            "formal_composition_count": 0,
            "advance_obligation_ids": [],
            "may_satisfy_obligation_ids": [],
            "branch_path_relation": "branch",
        }
        with mock.patch.object(
            RUNNER, "packet_prompt", return_value=("prompt", "context")
        ), mock.patch.object(
            RUNNER,
            "step_was_truncated",
            side_effect=lambda _run, step: not step.endswith("_expanded"),
        ), mock.patch.object(
            RUNNER, "expanded_output_limit", return_value=RUNNER.EXPANDED_OUTPUT_TOKENS
        ), mock.patch.object(
            RUNNER, "request_record"
        ) as request:
            RUNNER.request_packet_slice(
                Path("/offline"), {}, plan, transport=lambda *_args, **_kwargs: None
            )
        self.assertEqual(
            request.call_args.kwargs["max_tokens"], RUNNER.EXPANDED_OUTPUT_TOKENS
        )

    def test_packet_is_complete_only_after_all_chunks_fill_the_plan(self):
        plan = {
            "packet_slot_id": "literary_packet_0001",
            "packet_kind": "literary",
            "scene_slot_ids": [f"scene_slot_{number:04d}" for number in range(1, 7)],
            "ending_slot_ids": [],
            "artifact_count": 2,
            "formal_composition_count": 0,
        }
        architecture = {"packet_plans": [plan]}
        first = {
            "record_type": "creative_packet",
            "packet_slot_id": plan["packet_slot_id"],
            "scenes": [
                {"technical_slot_id": slot} for slot in plan["scene_slot_ids"][:3]
            ],
            "endings": [],
            "artifacts": [{}],
            "formal_compositions": [],
        }
        second = {
            "record_type": "creative_packet",
            "packet_slot_id": plan["packet_slot_id"],
            "scenes": [
                {"technical_slot_id": slot} for slot in plan["scene_slot_ids"][3:]
            ],
            "endings": [],
            "artifacts": [{}],
            "formal_compositions": [],
        }
        self.assertEqual(RUNNER.completed_packet_slots(architecture, [first]), set())
        self.assertEqual(
            RUNNER.completed_packet_slots(architecture, [first, second]),
            {plan["packet_slot_id"]},
        )

    def test_terminal_schema_has_no_partial_play_state(self):
        protocol = RUNNER.load_protocol()
        statuses = protocol["$defs"]["finalization"]["properties"]["run_status"]["enum"]
        self.assertEqual(set(statuses), {"READY_TO_PLAY", "FAILED_GENERATION"})
        barrier = protocol["$defs"]["runManifest"]["properties"][
            "complete_work_barrier"
        ]["properties"]
        self.assertEqual(barrier["partial_play_allowed"]["const"], False)
        self.assertEqual(barrier["runtime_generation_allowed"]["const"], False)
        invalid_ready = {
            "record_type": "finalization",
            "protocol_version": "6.0",
            "generation_id": "generation_test",
            "run_status": "READY_TO_PLAY",
            "run_manifest_hash": "a" * 64,
            "generation_brief_hash": "b" * 64,
            "completed_at": "2026-01-01T00:00:00Z",
            "creative_step_count": 0,
            "analysis_step_count": 0,
            "human_intervention_count": 0,
            "committed_rewrite_count": 0,
            "committed_regeneration_count": 0,
            "backtrack_count": 0,
            "ledger_head_hash": "c" * 64,
            "committed_record_hashes": {"run_manifest": "d" * 64},
            "constraint_event_stream_hash": "e" * 64,
            "prospective_plan_history_hash": "f" * 64,
            "token_accounting": {
                "input_tokens": 0,
                "output_tokens": 0,
                "cost": None,
                "currency": None,
            },
            "mechanical_validation": {"result": "NOT_RUN", "reasons": ["partial"]},
            "artistic_acceptance": {"result": "NOT_RUN", "reasons": ["partial"]},
            "static_build_validation": {"result": "NOT_RUN", "reasons": ["partial"]},
            "warnings": [],
            "npm_enhancement": {"result": "NOT_RUN", "reasons": ["partial"]},
            "complete_work_barrier_satisfied": False,
            "playable": False,
            "failure_class": "none",
        }
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(
                invalid_ready, protocol["$defs"]["finalization"], protocol
            )
        rejected = invalid_ready | {
            "run_status": "FAILED_GENERATION",
            "failure_class": "artistic_rejection",
            "mechanical_validation": {"result": "PASS", "reasons": ["valid"]},
            "static_build_validation": {"result": "PASS", "reasons": ["built"]},
            "artistic_acceptance": {
                "result": "FAIL GENERATION",
                "reasons": ["rejected"],
            },
        }
        RUNNER.validate_json_schema(
            rejected, protocol["$defs"]["finalization"], protocol
        )
        self.assertFalse(rejected["playable"])
        self.assertFalse(rejected["complete_work_barrier_satisfied"])


if __name__ == "__main__":
    unittest.main()
