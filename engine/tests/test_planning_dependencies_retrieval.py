"""Packet-order constraints and small, reusable, provenance-checked retrieval."""
import copy
import json
import unittest
from unittest import mock

from test_cathedrals import ROOT, RUNNER, architecture_core_payload, architecture_genesis_records, packet_plan_annotation
from test_bounded_execution import POLICY, call, tool_response
import test_reference_resolution as fixtures
import test_genesis_reference_prevention as genesis


class PlanningDependenciesRetrievalTests(unittest.TestCase):
    scene_count = 30
    policy = POLICY
    setUp = fixtures.ReferenceResolutionTests.setUp
    roots = genesis.GenesisReferencePreventionTests.roots
    commit = genesis.GenesisReferencePreventionTests.commit

    def planning(self):
        records = architecture_genesis_records()
        for patch in (mock.patch.object(RUNNER, 'committed_record', side_effect=lambda _run, kind: records.get(kind)),
                mock.patch.object(RUNNER, 'committed_records', return_value=[]),
                mock.patch.object(RUNNER, '_source_index', return_value={'commit_foundation': {}})):
            patch.start()
            self.addCleanup(patch.stop)
        value = architecture_core_payload()
        value['arcs'] = [copy.deepcopy(value['arcs'][0]) | {'arc_id': f'arc_{index:03d}'} for index in range(1, 5)]
        core = RUNNER.build_architecture_core(self.run, value)
        records['architecture_core'] = core
        return RUNNER.planned_packet_specs(core)

    def state(self, payload):
        return {'payload': payload, 'values': {}, 'hints': [], 'unassigned': [], 'checkpoint_version': 3}


    def test_small_retrieval_is_shared_between_related_authoring_calls(self):
        self.roots()
        parent = 'architecture_core'
        state = self.state({'arcs': [{'arc_id': f'arc_{index:03d}'} for index in range(1, 7)]})
        RUNNER.save_planning_draft(self.run, parent, state)
        descriptor = RUNNER.planning_retrieval_task(parent, state, [['arcs', 0], ['arcs', 1]], context={
            'frozen_law': 'LONG_FROZEN_LAW ' * 3000, 'brief': {'genre_flavor': 'mystery'},
            'global_canon': {'work_canon': {'premise': 'A sealed archive repeats midnight.'}},
            'targets': [{'retained_value': {'purpose': None}}]})
        requests = []
        def transport(_method, _url, request, **_kwargs):
            requests.append(request)
            return tool_response([call('get_records', {'ids': ['cathedrals-v01']})]) if 'tools' in request else fixtures.api_response('chosen')
        with mock.patch.object(RUNNER, 'execution_policy', return_value=POLICY | {'retrieval_mode': 'tools'}):
            for step in ('author_one', 'author_two'):
                result, response = RUNNER.request_architecture_analysis(self.run, step, 'LONG_FROZEN_LAW ' * 3000,
                    {'type': 'string'}, transport, planning_mode=True, retrieval_task=descriptor)
                RUNNER.preserve_planning_result(self.run, parent, step, result, response, kind='test')
        native = [request for request in requests if 'tools' in request]
        self.assertEqual(len(native), 1)
        self.assertEqual(len(requests), 3)
        prompt = native[0]['messages'][1]['content']
        self.assertNotIn('LONG_FROZEN_LAW', prompt)
        self.assertLessEqual(RUNNER.estimated_prompt_tokens(prompt), 2048)
        self.assertEqual(len(json.loads(prompt)['task']['allocated_ids']), 6)
        self.assertIn('archive', json.loads(prompt)['task']['keywords'])
        self.assertEqual(RUNNER.load_state(self.run)['input_tokens'], 33)
        replay = RUNNER.read_json(self.run / 'raw/author_two.retrieval-session.json')
        self.assertEqual(replay['reused_from'], 'author_one')
        self.assertEqual(replay['working_set'][0]['authority'], 'GENERATED ROOT CANON')
        cache_path = next((self.run / '.staging').glob('retrieval-cache-*.json'))
        cache = RUNNER.read_json(cache_path)
        cache['working_set'][0]['source_hash'] = '0' * 64
        RUNNER.write_json(cache_path, cache)
        with mock.patch.object(RUNNER, 'execution_policy', return_value=POLICY | {'retrieval_mode': 'tools'}), self.assertRaises(RUNNER.IntegrityError):
            RUNNER.retrieval_working_set(self.run, 'tampered_cache', descriptor['task'], transport,
                scope_id=descriptor['scope_id'], scope_step=parent)
        self.assertEqual(len(requests), 3)

    def test_tentative_cache_reuses_bookkeeping_changes_and_invalidates_changed_content(self):
        self.roots()
        state = self.state({'arcs': [{'arc_id': 'arc_001', 'purpose': 'Before'}]})
        RUNNER.save_planning_draft(self.run, 'architecture_core', state)
        provider = mock.Mock(return_value=tool_response([call('get_plan_items')]))
        with mock.patch.object(RUNNER, 'execution_policy', return_value=POLICY | {'retrieval_mode': 'tools'}):
            first = RUNNER.retrieval_working_set(self.run, 'read_one', 'Fetch arc_001', provider, scope_id='arcs', scope_step='architecture_core')
            state['bookkeeping'] = 'Changed checkpoint only'
            RUNNER.save_planning_draft(self.run, 'architecture_core', state)
            second = RUNNER.retrieval_working_set(self.run, 'read_two', 'Fetch arc_001', provider, scope_id='arcs', scope_step='architecture_core')
            self.assertEqual(provider.call_count, 1)
            self.assertEqual(first[0]['item'], second[0]['item'])
            self.assertNotEqual(first[0]['revision'], second[0]['revision'])
            state['payload']['arcs'][0]['purpose'] = 'After'
            RUNNER.save_planning_draft(self.run, 'architecture_core', state)
            third = RUNNER.retrieval_working_set(self.run, 'read_three', 'Fetch arc_001', provider, scope_id='arcs', scope_step='architecture_core')
        self.assertEqual(provider.call_count, 2)
        self.assertEqual(third[0]['item']['purpose'], 'After')

    def test_upstream_changes_invalidate_shared_retrieval(self):
        self.roots()
        provider = mock.Mock(return_value=fixtures.api_response('READY', text=True))
        with mock.patch.object(RUNNER, 'execution_policy', return_value=POLICY | {'retrieval_mode': 'tools'}):
            RUNNER.retrieval_working_set(self.run, 'query_one', 'Fetch optional evidence', provider, scope_id='plans', scope_step='current')
            RUNNER.save_planning_draft(self.run, 'upstream', self.state({'arcs': [{'arc_id': 'arc_001'}]}))
            RUNNER.retrieval_working_set(self.run, 'query_two', 'Fetch optional evidence', provider, scope_id='plans', scope_step='current')
            record = RUNNER.build_genesis_constraints(self.run, genesis.genesis_semantic_payload('central_incident'))
            self.commit(record, 'genesis_constraints')
            RUNNER.retrieval_working_set(self.run, 'query_three', 'Fetch optional evidence', provider, scope_id='plans', scope_step='current')
        self.assertEqual(provider.call_count, 3)

    def test_other_groups_in_same_checkpoint_invalidate_cohort_cache(self):
        self.roots()
        state = self.state({'arcs': [{'arc_id': 'arc_001'}]})
        RUNNER.save_planning_draft(self.run, 'architecture_core', state)
        task = RUNNER.planning_retrieval_task('architecture_core', state, [['arcs', 0]])['task']
        provider = mock.Mock(return_value=fixtures.api_response('READY', text=True))
        with mock.patch.object(RUNNER, 'execution_policy', return_value=POLICY | {'retrieval_mode': 'tools'}):
            RUNNER.retrieval_working_set(self.run, 'cohort_one', task, provider, scope_id='arcs', scope_step='architecture_core')
            state['payload']['obligation_graph'] = [{'obligation_id': 'obligation_001', 'description': 'New upstream requirement'}]
            RUNNER.save_planning_draft(self.run, 'architecture_core', state)
            RUNNER.retrieval_working_set(self.run, 'cohort_two', task, provider, scope_id='arcs', scope_step='architecture_core')
        self.assertEqual(provider.call_count, 2)

    def test_schema_only_repairs_do_not_start_retrieval(self):
        provider = mock.Mock(return_value=fixtures.api_response('chosen'))
        with mock.patch.object(RUNNER, 'execution_policy', return_value=POLICY | {'retrieval_mode': 'tools'}):
            value, _response = RUNNER.request_architecture_analysis(self.run, 'metadata_one', 'Choose the valid ID.',
                {'type': 'string', 'enum': ['chosen']}, provider, planning_mode=True)
        self.assertEqual(value, 'chosen')
        self.assertEqual(provider.call_count, 1)
        self.assertNotIn('tools', provider.call_args.args[2])

    def test_search_results_do_not_consume_complete_source_allowance(self):
        self.roots()
        ids = [f'source_{index:03d}' for index in range(24)]
        search_results = [{'source_id': value, 'kind': 'root'} for value in ids]
        unit = {'source_id': ids[0], 'immutable_source': {'text': 'Complete source'}}
        responses = [tool_response([call('search_records', {'query': 'source', 'limit': 24})]),
            tool_response([call('get_records', {'ids': [ids[0]]})])]
        provider = mock.Mock(side_effect=responses)
        with mock.patch.object(RUNNER, 'execution_policy', return_value=POLICY | {'retrieval_mode': 'tools'}), mock.patch.object(
                RUNNER, 'read_retrieval_tool', side_effect=[search_results, [unit]]):
            result = RUNNER.retrieval_working_set(self.run, 'search_then_read', 'Find a source', provider)
        self.assertEqual(result, [unit])
        self.assertEqual(provider.call_count, 2)

    def test_large_retrieval_prompt_is_rejected_before_provider(self):
        self.roots()
        provider = mock.Mock()
        with mock.patch.object(RUNNER, 'execution_policy', return_value=POLICY | {'retrieval_mode': 'tools'}), self.assertRaises(RUNNER.PausedError):
            RUNNER.retrieval_working_set(self.run, 'too_large', 'x' * 10000, provider)
        provider.assert_not_called()


if __name__ == '__main__':
    unittest.main()
