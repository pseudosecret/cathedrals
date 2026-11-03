"""Prevent the source-slot repair storm without changing committed Genesis bytes."""
import copy
import json
import unittest
from unittest import mock

from test_cathedrals import RUNNER, claimant_expansion, genesis_cast_fixture, genesis_semantic_payload
import test_reference_resolution as fixtures


class GenesisReferencePreventionTests(unittest.TestCase):
    setUp = fixtures.ReferenceResolutionTests.setUp

    def roots(self):
        payload = fixtures.foundation_payload()
        foundation = RUNNER.build_genesis_foundation(self.run, payload)
        self.commit(foundation, 'genesis_foundation')
        cast_payload = {'claimants': [claimant_expansion(f'claimant_{index:02d}') for index in range(1, 6)],
            'characters': genesis_cast_fixture()['characters']}
        cast = RUNNER.build_genesis_cast(self.run, cast_payload)
        self.commit(cast, 'genesis_cast')
        return foundation, cast

    def commit(self, record, step):
        RUNNER.commit_record(self.run, record, '{}', {}, planned_step_id=step, attempt=1, step_phase='genesis',
            prompt='Synthetic root fixture.', context='Synthetic context.', parameters={'seed': '1'}, branch_relation='genesis')

    def request(self, transport, precommit=None):
        schema = RUNNER.genesis_constraints_schema(self.run)
        return RUNNER.request_record(self.run, expected_record_type='genesis_constraints', step_id='genesis_constraints',
            phase='genesis', prompt='Synthetic extraction.', context='Synthetic immutable context.', branch_relation='genesis',
            temperature=0.4, max_tokens=8192, transport=transport, response_definition='semanticDeltaPayload', response_schema=schema,
            reference_context={}, payload_validator=RUNNER.validate_genesis_constraints_payload,
            payload_repairer=lambda step, payload, content, response: RUNNER.repair_genesis_constraints_payload(
                self.run, step, payload, content, response, transport),
            record_builder=lambda payload: RUNNER.build_genesis_constraints(self.run, payload),
            precommit_validator=precommit or (lambda record: RUNNER.validate_genesis_constraints(record, self.run)))

    def test_catalog_and_schema_close_every_known_source_domain(self):
        foundation, cast = self.roots()
        catalog = RUNNER.genesis_source_catalog(self.run)
        required = {'central_incident', 'environmental_mutation_law', 'principal_tensions', 'chronology_event_001',
            'claimant_slot_01', 'claimant_profile_slot_01', 'character_slot_001'}
        self.assertTrue(required.issubset(catalog))
        self.assertEqual(catalog['central_incident']['source_ref'], {'artifact_type': 'genesis',
            'artifact_id': foundation['commit_id'], 'source_locator': '/work_canon/central_incident'})
        self.assertEqual(catalog['claimant_profile_slot_01']['source_ref']['artifact_id'], cast['commit_id'])
        schema = RUNNER.genesis_constraints_schema(self.run)
        for handle in required:
            RUNNER.validate_json_schema(genesis_semantic_payload(handle), schema)
        for handle in ('invented_source', self.run.name):
            with self.assertRaises(RUNNER.SchemaError):
                RUNNER.validate_json_schema(genesis_semantic_payload(handle), schema)
        invalid = genesis_semantic_payload('central_incident')
        invalid['canonical_facts'][0]['relevance']['arc_ids'] = ['invented_arc']
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(invalid, schema)
        invalid = genesis_semantic_payload('central_incident')
        invalid['canonical_facts'] *= 13
        with self.assertRaises(RUNNER.SchemaError):
            RUNNER.validate_json_schema(invalid, schema)

    def test_world_and_profile_sources_commit_with_exact_proof_and_zero_repairs(self):
        foundation, cast = self.roots()
        hashes = {path: path.read_bytes() for path in RUNNER.committed_directories(self.run) for path in [path / 'record.json']}
        payload = genesis_semantic_payload('central_incident')
        payload['canonical_facts'][0]['relevance'] = {}
        for handle in ('environmental_mutation_law', 'chronology_event_001', 'claimant_profile_slot_01'):
            fact = copy.deepcopy(payload['canonical_facts'][0])
            fact.update(source={'technical_slot_id': handle}, predicate=f'observed_{handle}')
            payload['canonical_facts'].append(fact)
        transport = mock.Mock(return_value=fixtures.api_response(payload))
        with (mock.patch.object(RUNNER, 'resolve_named_reference', side_effect=AssertionError('Individual repair forbidden')),
                mock.patch.object(RUNNER, 'request_architecture_analysis', side_effect=AssertionError('No repair needed'))):
            record = self.request(transport)
        self.assertEqual(transport.call_count, 1)
        wire = transport.call_args.args[2]['response_format']['json_schema']['schema']
        self.assertEqual(wire['$defs']['relevanceTags']['properties']['technical_slot_ids']['maxItems'], 0)
        facts = record['constraint_delta']['canonical_facts']
        self.assertEqual([fact['relevance']['technical_slot_ids'] for fact in facts], [[fact['source']['technical_slot_id']] for fact in payload['canonical_facts']])
        events = RUNNER.constraint_events(self.run)
        retrieved = RUNNER.retrieve_original_sources(self.run, events, limit=None, strict=True)
        units = {source['record_pointer']: source for source in retrieved}
        self.assertEqual(units['/work_canon/central_incident']['immutable_source'], foundation['work_canon']['central_incident'])
        self.assertEqual(units['/work_canon/environmental_mutation_law']['immutable_source'], foundation['work_canon']['environmental_mutation_law'])
        self.assertEqual(units['/work_canon/chronology/0']['immutable_source'], foundation['work_canon']['chronology'][0])
        self.assertEqual(units['/claimants/0']['immutable_source'], cast['claimants'][0])
        self.assertTrue(all(len(source['source_hash']) == 64 for source in retrieved))
        literary = {'record_type': 'creative_packet', 'commit_id': 'commit_literary', 'scenes': [{'scene_id': 'scene_fixture'}],
            'artifacts': [], 'endings': [], 'formal_compositions': []}
        mixed = events + [{'sources': [{'artifact_id': 'scene_fixture', 'source_locator': 'Synthetic literary source'}]}]
        self.assertEqual(len(RUNNER.retrieve_original_sources(self.run, mixed, limit=2, records=[foundation, cast, literary])), 2)
        for path, content in hashes.items():
            self.assertEqual(path.read_bytes(), content)
        self.assertEqual(RUNNER.load_state(self.run)['input_tokens'], 11)

    def test_same_invalid_label_with_different_meaning_is_batched_without_global_replacement(self):
        self.roots()
        payload = genesis_semantic_payload('unknown_label')
        payload['canonical_facts'] *= 3
        payload['canonical_facts'] = [copy.deepcopy(fact) | {'predicate': f'case_{index}'}
            for index, fact in enumerate(payload['canonical_facts'])]
        choices = ['central_incident', 'character_slot_001', 'claimant_slot_01']
        calls = []
        def transport(_method, _url, request, **_kwargs):
            name = request['response_format']['json_schema']['name']
            calls.append(name)
            if name == 'semanticDeltaPayload': return fixtures.api_response(payload)
            self.assertEqual(name, 'genesisReferenceBatch')
            schema = request['response_format']['json_schema']['schema']
            keys = schema['properties']['resolutions']['required']
            self.assertEqual(len(keys), 3)
            return fixtures.api_response({'resolutions': dict(zip(keys, choices))})
        with mock.patch.object(RUNNER, 'resolve_named_reference', side_effect=AssertionError('Individual repair forbidden')):
            record = self.request(transport)
        self.assertEqual(calls, ['semanticDeltaPayload', 'genesisReferenceBatch'])
        catalog = RUNNER.genesis_source_catalog(self.run)
        for fact, choice in zip(record['constraint_delta']['canonical_facts'], choices):
            self.assertEqual(fact['sources'][0], catalog[choice]['source_ref'])
            self.assertEqual(fact['relevance']['technical_slot_ids'], [choice])

    def test_late_validation_pause_resumes_original_payload_without_provider(self):
        self.roots()
        payload = genesis_semantic_payload('central_incident')
        transport = mock.Mock(return_value=fixtures.api_response(payload))
        with self.assertRaisesRegex(RUNNER.PausedError, 'complete payload was not requested again'):
            self.request(transport, mock.Mock(side_effect=RUNNER.SchemaError('Synthetic late validation failure')))
        archive = self.run / '.staging/genesis_constraints.artistic.json'
        original = archive.read_bytes()
        record = self.request(transport)
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(record['constraint_delta']['canonical_facts'][0]['predicate'], payload['canonical_facts'][0]['predicate'])
        commit = next(path for path in RUNNER.committed_directories(self.run) if path.name.endswith('-genesis_constraints'))
        self.assertEqual((commit / 'artistic-payload.json').read_bytes(), original)
        self.assertEqual(RUNNER.load_state(self.run)['input_tokens'], 11)

    def test_completed_repair_batches_survive_pause_and_usage_is_counted_once(self):
        self.roots()
        payload = genesis_semantic_payload('unknown_source')
        payload['canonical_facts'] = [copy.deepcopy(payload['canonical_facts'][0]) | {'predicate': f'case_{index}'} for index in range(7)]
        batch_calls = []
        blocked = [True]
        def response(value):
            result = fixtures.api_response(value)
            result['usage']['completion_tokens_details'] = {'reasoning_tokens': 3}
            return result
        def transport(_method, _url, request, **_kwargs):
            name = request['response_format']['json_schema']['name']
            if name == 'semanticDeltaPayload': return response(payload)
            self.assertEqual(name, 'genesisReferenceBatch')
            keys = request['response_format']['json_schema']['schema']['properties']['resolutions']['required']
            batch_calls.append(tuple(keys))
            if len(keys) == 3 and blocked[0]: return response({'resolutions': {}})
            return response({'resolutions': {key: 'central_incident' for key in keys}})
        provider = mock.Mock(side_effect=transport)
        with self.assertRaises(RUNNER.PausedError):
            self.request(provider)
        checkpoint = RUNNER.read_json(self.run / '.staging/genesis_constraints.repair.json')
        self.assertEqual(len(checkpoint['history']), 1)
        self.assertEqual(sum(fact['source']['technical_slot_id'] == 'central_incident' for fact in checkpoint['payload']['canonical_facts']), 4)
        blocked[0] = False
        record = self.request(provider)
        self.assertEqual(len(record['constraint_delta']['canonical_facts']), 7)
        self.assertEqual([len(keys) for keys in batch_calls], [4, 3, 3, 3, 3])
        self.assertEqual(provider.call_count, 6)
        self.assertEqual(RUNNER.load_state(self.run)['input_tokens'], 66)
        self.assertEqual(RUNNER.load_state(self.run)['output_tokens'], 42)
        self.assertEqual(sum(entry['token_accounting'].get('reasoning_tokens', 0) for entry in RUNNER.ledger_entries(self.run)), 18)

    def test_pointer_errors_and_archive_tampering_cannot_be_hidden_by_source_selection(self):
        foundation, _cast = self.roots()
        source = {'artifact_id': foundation['commit_id'], 'source_locator': '/work_canon/missing'}
        with self.assertRaises(RUNNER.IntegrityError):
            RUNNER.retrieve_original_sources(self.run, [{'sources': [source]}], strict=True)
        path = next(path / 'record.json' for path in RUNNER.committed_directories(self.run) if path.name.endswith('-genesis_foundation'))
        path.chmod(0o644)
        path.write_text('{}')
        source['source_locator'] = '/work_canon/central_incident'
        with self.assertRaises(RUNNER.IntegrityError):
            RUNNER.retrieve_original_sources(self.run, [{'sources': [source]}], strict=True)


if __name__ == '__main__':
    unittest.main()
