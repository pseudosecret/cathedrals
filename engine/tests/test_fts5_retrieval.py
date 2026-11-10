"""Search, context protection, provenance, and recovery using real archived packets."""

import json
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from benchmark_storage import RUNNER, packet


def plan(**changes):
    return {"packet_slot_id": "packet_next", "packet_kind": "literary", "scene_slot_ids": ["scene_slot_next"],
        "ending_slot_ids": [], "artifact_count": 0, "formal_composition_count": 0, "attractor_ids": [],
        "advance_obligation_ids": [], "may_satisfy_obligation_ids": [], "depends_on_packet_slot_ids": [],
        "relevance": {}, "soft_guidance": [], "branch_path_relation": "fixture", **changes}


def decode_context(text):
    sections = {}
    parts = re.split(r"^===== (.*?) =====\n", text, flags=re.MULTILINE)
    for label, body in zip(parts[1::2], parts[2::2]):
        if label in {"SHARED SOURCE METADATA", "SHARED SOURCE RECORDS", "SHARED CONTEXT VALUES"}:
            body = body.split("\n", 1)[1]
        values = []
        decoder = json.JSONDecoder()
        while body.strip():
            body = body.lstrip()
            try:
                value, end = decoder.raw_decode(body)
            except json.JSONDecodeError:
                values.append(body.strip())
                break
            values.append(value)
            body = body[end:]
        sections.setdefault(label, []).extend(values)
    shared = sections.pop("SHARED SOURCE METADATA", [{}])[0]
    shared.update(sections.pop("SHARED SOURCE RECORDS", [{}])[0])
    shared.update(sections.pop("SHARED CONTEXT VALUES", [{}])[0])

    def expand(value):
        if isinstance(value, dict):
            if set(value) == {"$context_ref"}:
                return expand(shared[value["$context_ref"]])
            return {key: expand(child) for key, child in value.items()}
        return [expand(child) for child in value] if isinstance(value, list) else value

    return {label: expand(values) for label, values in sections.items()}


class FTS5RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        with mock.patch.object(RUNNER, "RUNTIME_ROOT", root), mock.patch.object(RUNNER, "RUNS_ROOT", root / "runs"):
            self.run = RUNNER.create_run(RUNNER.FrozenInputs(possible_scene_count=150), "http://offline.invalid", "offline", output_fn=lambda _: None)
        law = self.run / "state/frozen-engine-context.txt"
        law.chmod(0o644)
        law.write_text("Synthetic engine law.")
        for patch in (
            mock.patch.object(RUNNER, "scoped_root_sources", return_value=[]),
            mock.patch.object(RUNNER, "instruction_profile", return_value=("Synthetic engine law.", {"purpose": "fixture"})),
            mock.patch.object(RUNNER, "plan_batch_for", return_value={"commit_id": "fixture_batch"}),
        ):
            patch.start()
            self.addCleanup(patch.stop)
        self.architecture = {"architecture_core_commit_id": "fixture_core", "obligation_graph": [], "attractors": [], "arcs": [], "packet_plans": []}

    def commit(self, number, *, prose=None, title=None, change=None, required=False):
        record = packet(self.run.name, number)
        if prose is not None:
            record["scenes"][0]["prose_mdx"] = prose
        if title is not None:
            record["scenes"][0]["title"] = title
        if required:
            record["constraint_delta"]["new_obligations"] = [{"obligation_id": f"obligation_{number}", "kind": "promise",
                "description": "Synthetic prerequisite evidence.", "status": "active", "created_by_ids": [record["scenes"][0]["scene_id"]],
                "requires": [], "hardness": "hard", "universality": "local", "resolution_modes": ["revelation"], "range": "local",
                "termination_targets": [], "sources": record["constraint_delta"]["canonical_facts"][0]["sources"], "relevance": {}}]
        if change:
            change(record)
        return RUNNER.commit_record(self.run, record, RUNNER.canonical_json(record).decode(), {},
            planned_step_id=f"fixture_{number:06d}", attempt=1, step_phase="literary_packet", prompt="fixture",
            context="fixture", parameters={"seed": "fixture"}, branch_relation="fixture")

    def search(self, term, **kwargs):
        return RUNNER.search_history(self.run, RUNNER.search_query(plan(relevance={"keywords": [term]})), **kwargs)

    def context(self, packet_plan, **kwargs):
        with mock.patch.object(RUNNER, "committed_record", return_value={"record_type": "genesis", "claimants": [], "characters": []}), mock.patch.object(
            RUNNER, "ensure_frozen_geomancy", return_value={"assignments": []}
        ):
            return RUNNER.relevant_packet_context(self.run, self.architecture, packet_plan, **kwargs)

    def test_search_finds_unextracted_prose_as_a_complete_original_unit(self):
        prose = "Rareword communiqué.\n\n  Preserve this spacing.\n\nLast paragraph."
        self.commit(1, prose=prose)
        for number in range(2, 8):
            self.commit(number, prose="Unrelated synthetic placeholder.")
        query = RUNNER.search_query(plan(relevance={"keywords": ["rareword"]}))
        self.assertEqual(RUNNER.search_history(self.run, query, constraints=True), [])
        hits = RUNNER.search_history(self.run, query)
        self.assertEqual(hits[0]["source_id"], "scene_000001")
        source = RUNNER.read_search_source(self.run, hits[0])
        self.assertEqual(source["immutable_source"]["prose_mdx"].encode(), prose.encode())
        self.assertEqual(source["record_pointer"], "/scenes/0")
        self.assertEqual(source["authority"], "COMMITTED LITERARY MATERIAL")
        context = self.context(plan(relevance={"keywords": ["rareword"]}))
        sections = decode_context(context)
        self.assertEqual(sections["RETRIEVED ORIGINAL SOURCE EVIDENCE"][0]["immutable_source"]["prose_mdx"], prose)

    def test_unicode_literal_operators_no_stemming_and_empty_queries(self):
        self.commit(1, prose="CAFÉ promise AND asterisks * quotation \" exact tokens.")
        self.commit(2, prose="promised otherword")
        self.assertEqual(self.search("café")[0]["source_id"], "scene_000001")
        self.assertEqual([hit["source_id"] for hit in self.search("promise")], ["scene_000001"])
        self.assertEqual([hit["source_id"] for hit in self.search("promised")], ["scene_000002"])
        self.assertEqual(self.search("AND")[0]["source_id"], "scene_000001")
        self.assertEqual(RUNNER.search_history(self.run, RUNNER.search_query(plan())), [])
        self.assertEqual(RUNNER.search_history(self.run, RUNNER.search_query(plan(relevance={"keywords": ["***"]}))), [])
        for term in ['" OR *', '(NEAR x)', '"; DROP TABLE records; --']:
            self.search(term)
        self.assertEqual(len(RUNNER.all_committed_records(self.run)), 2)

    def test_query_limits_resolved_names_and_technical_ids(self):
        query = RUNNER.search_query(plan(relevance={"keywords": ["Rareword", "rareword"], "character_ids": ["character_001"]},
            soft_guidance=["scene_slot_0001 " + " ".join(f"word{number}" for number in range(100))]),
            {"characters": [{"character_id": "character_001", "name": "Name With Spaces"}]})
        self.assertEqual(query["terms"][:2], ["Rareword", "Name With Spaces"])
        self.assertEqual(len(query["terms"]), 32)
        self.assertNotIn("scene_slot_0001", query["expression"])
        self.assertNotIn('"0001"', query["expression"])

    def test_structured_old_constraint_survives_empty_search_and_bounded_candidates(self):
        def old_tag(record):
            record["constraint_delta"]["canonical_facts"][0]["relevance"] = {"branch_ids": ["distant_branch"]}
        self.commit(1, change=old_tag)
        for number in range(2, 40):
            self.commit(number)
        with mock.patch.object(RUNNER, "constraint_events", side_effect=AssertionError("full event scan")), mock.patch.object(
            RUNNER, "all_committed_records", side_effect=AssertionError("full record scan")
        ):
            selected = RUNNER.select_relevant_constraints(self.run, self.architecture, plan(relevance={"branch_ids": ["distant_branch"]}))
        self.assertEqual(selected[0]["constraint_id"], "fact_000001")
        self.assertLessEqual(len(selected), 96)

    def test_title_weight_and_rebuild_order_are_deterministic(self):
        self.commit(1, title="rareword", prose="Common fixture.")
        self.commit(2, title="Other", prose="Common fixture rareword.")
        before = self.search("rareword")
        self.assertEqual(before[0]["source_id"], "scene_000001")
        RUNNER.index_path(self.run).unlink()
        RUNNER.reconcile_run(self.run)
        after = self.search("rareword")
        self.assertEqual([(hit["commit_id"],hit["pointer"],hit["bm25"]) for hit in before], [(hit["commit_id"],hit["pointer"],hit["bm25"]) for hit in after])

    def test_metadata_compaction_is_lossless_and_preserves_section_roles(self):
        reference = {"artifact_type": "scene", "artifact_id": "scene_fixture", "source_commit_id": "commit_fixture",
            "source_hash": "a" * 64, "source_locator": "Original source locator."}
        record = {"fact_id": "fact_fixture", "sources": [reference], "value": "Unchanged fact."}
        prose = " First line.\n\nSecond café line.  "
        literary = {"source_id": "scene_fixture", "immutable_source": {"prose_mdx": prose}}
        required = [("FACTS", [record] * 5), ("SAME FACT IN ANOTHER ROLE", [record]), ("LITERARY", [literary])]
        receipt = {"omissions": []}
        text = RUNNER.pack_packet_context(required, [], 10000, receipt)
        decoded = decode_context(text)
        self.assertEqual(decoded["FACTS"], [record] * 5)
        self.assertEqual(decoded["SAME FACT IN ANOTHER ROLE"], [record])
        self.assertEqual(decoded["LITERARY"][0]["immutable_source"]["prose_mdx"].encode(), prose.encode())
        self.assertLess(receipt["required_compact_bytes"], receipt["required_pretty_bytes"])

    def test_mandatory_context_never_clips_and_omits_optional_overflow(self):
        receipt = {"omissions": []}
        text = RUNNER.pack_packet_context([("REQUIRED", [{"required": "x" * 100}])], [("OPTIONAL", [{"extra": "y" * 1000}])], 50, receipt)
        self.assertIn("x" * 100, text)
        self.assertNotIn("y" * 1000, text)
        self.assertEqual(receipt["omissions"][0]["reason"], "prepared_context_budget")
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.pack_packet_context([("REQUIRED", ["z" * 1000])], [], 10, {"omissions": []})

    def test_whole_predecessor_is_required_and_discovery_is_deduplicated(self):
        prose = "rareword complete predecessor material"
        self.commit(1, prose=prose, required=True)
        receipt = {}
        context = self.context(plan(relevance={"keywords": ["rareword"]}, depends_on_packet_slot_ids=["packet_000001"], advance_obligation_ids=["obligation_1"]), receipt=receipt)
        self.assertEqual(context.count(prose), 1)
        self.assertTrue(any(item["reason"] == "covered_by_required_context" for item in receipt["omissions"]))
        self.assertTrue(receipt["selected_sources"][0]["required"])
        self.commit(2, prose="x" * 160000, required=True)
        transport = mock.Mock()
        oversized = plan(depends_on_packet_slot_ids=["packet_000002"], advance_obligation_ids=["obligation_2"])
        with mock.patch.object(RUNNER, "packet_payload_schema", return_value={}), mock.patch.object(RUNNER, "committed_record", side_effect=lambda _run, kind: self.architecture if kind == "architecture" else {"record_type": "genesis"}), mock.patch.object(
            RUNNER, "ensure_frozen_geomancy", return_value={"assignments": []}
        ), self.assertRaises(RUNNER.PausedError):
            RUNNER.request_packet_slice(self.run, self.architecture, oversized, transport)
        transport.assert_not_called()
        receipt_path = self.run / ".staging" / f"{RUNNER.packet_step_id(oversized)}.retrieval.json"
        self.assertTrue(RUNNER.read_json(receipt_path)["capacity_failure"])

    def test_required_evidence_bypasses_the_optional_source_limit(self):
        for number in range(1, 28):
            self.commit(number)
        events = [event for event in RUNNER.constraint_events(self.run) if event["constraint_kind"] == "canonical_fact"]
        self.assertEqual(len(RUNNER.retrieve_original_sources(self.run, events, limit=None, strict=True)), 27)
        self.assertLessEqual(len(RUNNER.retrieve_original_sources(self.run, events)), 24)

    def test_tool_discovery_cannot_overflow_required_context_or_consume_correction_space(self):
        self.commit(1, prose="Required complete predecessor.", required=True)
        assignment = plan(depends_on_packet_slot_ids=["packet_000001"], advance_obligation_ids=["obligation_1"])
        step = RUNNER.packet_step_id(assignment)
        provenance = {"source_id": "shared_discovery", "source_commit_id": "commit_discovery", "source_hash": "a" * 64}
        records = [provenance | {"record_pointer": "/large", "immutable_source": "x" * 180000},
                   provenance | {"record_pointer": "/small", "immutable_source": "Useful additional background."}]
        RUNNER.write_json(self.run / "raw" / f"{step}.retrieval-session.json", {"working_set": records})
        receipt = {}
        context = self.context(assignment, receipt=receipt)
        decoded = decode_context(context)
        self.assertIn("Required complete predecessor.", context)
        self.assertEqual(decoded["MODEL REQUESTED VERIFIED RECORDS"], [records[1]])
        self.assertTrue(any(item.get("source_id") == "shared_discovery" and item.get("record_pointer") == "/large"
                            and item["reason"] == "prepared_context_budget" for item in receipt["omissions"]))
        self.assertTrue(any(item.get("source_id") == "shared_discovery" and item["record_pointer"] == "/small"
                            for item in receipt["selected_sources"]))
        self.assertEqual(receipt["correction_headroom_tokens"], RUNNER.BASE_OUTPUT_TOKENS)
        self.assertLessEqual(receipt["estimated_context_tokens"] + RUNNER.BASE_OUTPUT_TOKENS, receipt["context_ceiling"])

    def test_packet_context_accepts_sources_constraints_and_tentative_plan_items(self):
        self.commit(1, prose="Complete source unit for mixed retrieval.")
        source = RUNNER.read_retrieval_tool(self.run, "get_records", {"ids": ["scene_000001"]})[0]
        event = RUNNER.constraint_events(self.run)[0]
        RUNNER.save_planning_draft(self.run, "future_plan", {"payload": {"arcs": [{"arc_id": "arc_future", "purpose": "Tentative future intention."}]}})
        tentative = RUNNER.read_retrieval_tool(self.run, "get_plan_items", {"ids": ["arc_future"]})[0]
        records = [source, event, tentative]
        self.assertEqual(RUNNER.current_retrieval_records(self.run, records), records)
        self.assertNotIn("source_id", event)
        self.assertNotIn("source_id", tentative)
        assignment = plan()
        RUNNER.write_json(self.run / "raw" / f"{RUNNER.packet_step_id(assignment)}.retrieval-session.json", {"working_set": records})
        receipt = {}
        decoded = decode_context(self.context(assignment, receipt=receipt))
        self.assertEqual(decoded["MODEL REQUESTED CONSTRAINT HISTORY"], [event])
        self.assertEqual(decoded["MODEL REQUESTED TENTATIVE PLAN ITEMS"], [tentative])
        self.assertTrue(any(item["source_id"] == source["source_id"] for item in receipt["selected_sources"]))
        self.assertTrue(any(item["constraint_id"] == event["constraint_id"] and item["event_sequence"] == event["constraint_event_sequence"]
                            for item in receipt["selected_constraints"]))
        self.assertEqual(receipt["selected_plan_items"], [{"step_id": tentative["step_id"], "revision": tentative["revision"],
            "record_pointer": tentative["record_pointer"], "required": False}])

    def test_malformed_retrieval_record_reports_missing_fields(self):
        with self.assertRaisesRegex(RUNNER.IntegrityError, "missing source_id"):
            RUNNER.retrieval_record_metadata({"immutable_source": {}, "source_commit_id": "commit_fixture",
                "source_hash": "a" * 64, "record_pointer": ""})
        with self.assertRaisesRegex(RUNNER.IntegrityError, "Unknown retrieval record shape"):
            RUNNER.retrieval_record_metadata({"unexpected": "shape"})

    def test_shared_retrieval_validation_rejects_changed_hashes(self):
        self.commit(1)
        source = RUNNER.read_retrieval_tool(self.run, "get_records", {"ids": ["scene_000001"]})[0]
        source["source_hash"] = "0" * 64
        with self.assertRaisesRegex(RUNNER.IntegrityError, "Cached retrieval evidence changed"):
            RUNNER.current_retrieval_records(self.run, [source])

    def test_shared_tentative_retrieval_rejects_stale_items_and_noncanonical_pointers(self):
        state = {"payload": {"arcs": [{"arc_id": "arc_future", "purpose": "Original intention."}]}}
        RUNNER.save_planning_draft(self.run, "future_plan", state)
        item = RUNNER.read_retrieval_tool(self.run, "get_plan_items", {"ids": ["arc_future"]})[0]
        self.assertIsNone(RUNNER.current_retrieval_records(self.run, [item | {"record_pointer": "/arcs/00"}]))
        state["payload"]["arcs"][0]["purpose"] = "Updated intention."
        RUNNER.save_planning_draft(self.run, "future_plan", state)
        self.assertIsNone(RUNNER.current_retrieval_records(self.run, [item]))

    def test_retracted_knowledge_is_labeled_as_history(self):
        for number in range(1, 4):
            self.commit(number)
        context = self.context(plan(relevance={"keywords": ["knows"], "character_ids": ["character_fixture"]}))
        self.assertIn("retracted_or_superseded", context)
        decoded = decode_context(context)
        current = decoded.get("CHARACTER KNOWLEDGE / BELIEF CONSTRAINTS", []) + decoded.get("OTHER RELEVANT CHARACTER KNOWLEDGE", [])
        self.assertFalse(any(subject["knows"] for subject in current))

    def test_search_index_corruption_and_v1_version_rebuild(self):
        self.commit(1, prose="rareword")
        with RUNNER.index_connection(self.run) as db:
            row = db.execute("SELECT id,title,body FROM search_documents WHERE kind='literary'").fetchone()
            db.execute("INSERT INTO search_fts(search_fts,rowid,title,body) VALUES('delete',?,?,?)", row)
        self.assertEqual(self.search("rareword"), [])
        RUNNER.reconcile_run(self.run)
        self.assertEqual(self.search("rareword")[0]["source_id"], "scene_000001")
        with RUNNER.index_connection(self.run) as db:
            db.execute("PRAGMA user_version=1")
            db.execute("DROP TABLE search_fts")
        RUNNER.reconcile_run(self.run)
        self.assertEqual(self.search("rareword")[0]["source_id"], "scene_000001")

    def test_fts_insert_failure_rolls_back_then_recovers(self):
        insert = RUNNER.insert_search_document
        def interrupted(db, document):
            insert(db, document)
            raise sqlite3.OperationalError("synthetic interrupted FTS insert")
        with mock.patch.object(RUNNER, "insert_search_document", side_effect=interrupted), self.assertRaises(RUNNER.PausedError):
            self.commit(1, prose="rareword")
        with RUNNER.index_connection(self.run) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM search_documents").fetchone()[0], 0)
        RUNNER.reconcile_run(self.run)
        self.assertEqual(self.search("rareword")[0]["source_id"], "scene_000001")

    def test_search_source_hash_is_verified(self):
        directory = self.commit(1, prose="rareword")
        hit = self.search("rareword")[0]
        record = directory / "record.json"
        record.chmod(0o644)
        record.write_text("changed")
        with self.assertRaises(RUNNER.IntegrityError):
            RUNNER.read_search_source(self.run, hit)

    def test_composition_anchor_is_text_while_genesis_extension_anchor_is_an_object(self):
        record = packet(self.run.name, 1)
        record["formal_compositions"] = [{"composition_id": "composition_fixture", "container_id": "scene_000001",
            "form": "refrain", "dramatic_function": "Synthetic function", "anchor": "Exact anchor text."}]
        meta = {"constraint_events": [], "ledger_entry": {"ledger_sequence": 1}}
        documents = RUNNER.search_documents_for(record, meta)
        self.assertTrue(any(doc["source_id"] == "composition_fixture" and "Exact anchor text." in doc["body"] for doc in documents))
        extension = {"record_type": "genesis_constraints", "commit_id": "commit_extension", "constraint_delta": {},
            "claimant_extensions": [{"anchor": {"claimant_id": "claimant_new", "name": "Synthetic name"}, "profile": {"voice": "Synthetic voice"}}]}
        document = RUNNER.search_documents_for(extension, meta)[0]
        self.assertEqual(document["source_id"], "claimant_new")
        self.assertEqual(document["tags"]["claimant_ids"], ["claimant_new"])

    def test_saved_writing_reuses_its_receipt_without_another_provider_call(self):
        self.commit(1, prose="rareword source material")
        step = "saved_writing"
        context = self.context(plan(relevance={"keywords": ["rareword"]}), step_id=step)
        record = packet(self.run.name, 2)
        response = {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(record)}}],
                    "usage": {"prompt_tokens": 11, "completion_tokens": 7}}
        provider = mock.Mock(return_value=response)
        arguments = dict(expected_record_type="creative_packet", step_id=step, phase="literary_packet", prompt=context,
            context=context, branch_relation="fixture", temperature=0.8, transport=provider, response_schema={"type": "object"},
            payload_preserver=lambda payload, content, api: RUNNER.preserve_artistic_payload(self.run, step, payload, content, api))
        with self.assertRaises(RUNNER.PausedError):
            RUNNER.request_record(self.run, record_builder=mock.Mock(side_effect=RUNNER.PausedError("metadata", "synthetic pause")), **arguments)
        receipt = self.run / "raw" / f"{step}-attempt1.retrieval.json"
        original = receipt.read_bytes()
        RUNNER.index_path(self.run).unlink()
        RUNNER.reconcile_run(self.run)
        restored_context = self.context(plan(relevance={"keywords": ["rareword"]}), step_id=step)
        self.assertEqual(restored_context, context)
        arguments.update(prompt=restored_context, context=restored_context)
        RUNNER.request_record(self.run, record_builder=lambda payload: payload, **arguments)
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(receipt.read_bytes(), original)
        directory = next(path for path in RUNNER.committed_directories(self.run) if path.name.endswith(step))
        self.assertEqual((directory / "retrieval-receipt.json").read_bytes(), original)
        self.assertNotIn(b"immutable_source", original)


if __name__ == "__main__":
    unittest.main()
