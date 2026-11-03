"""Resolve evidence IDs independently of descriptive locators and verify provenance closure."""
import copy
import unittest
from unittest import mock

from test_cathedrals import RUNNER, genesis_semantic_payload
import test_reference_resolution as fixtures
import test_genesis_reference_prevention as genesis


class EvidenceResolutionTests(unittest.TestCase):
    setUp = fixtures.ReferenceResolutionTests.setUp
    roots = genesis.GenesisReferencePreventionTests.roots
    commit = genesis.GenesisReferencePreventionTests.commit

    def facts(self):
        foundation, cast = self.roots()
        payload = genesis_semantic_payload('chronology_event_002')
        payload['canonical_facts'][0]['status'] = 'contested'
        record = RUNNER.build_genesis_constraints(self.run, payload)
        record['constraint_delta']['canonical_facts'][0]['fact_id'] = 'fact_4448656f7d387136'
        self.commit(record, 'genesis_constraints')
        return foundation, cast, record

    def test_reported_fact_locator_resolves_fact_and_original_chronology(self):
        foundation, _cast, record = self.facts()
        reference = {'artifact_id': 'fact_4448656f7d387136', 'artifact_type': 'architecture', 'source_locator': '/chronology/002'}
        with mock.patch.object(RUNNER, 'http_json', side_effect=AssertionError('No provider needed')):
            result = RUNNER.retrieve_original_sources(self.run, [{'constraint_id': 'obligation_fixture', 'sources': [reference]}], limit=None, strict=True)
        self.assertEqual([unit['record_pointer'] for unit in result], ['/constraint_delta/canonical_facts/0', '/work_canon/chronology/1'])
        self.assertEqual(result[0]['source_record_type'], 'genesis_constraints')
        self.assertEqual(result[0]['source_locator'], '/chronology/002')
        self.assertEqual(result[0]['immutable_source']['status'], 'contested')
        self.assertEqual(result[1]['immutable_source'], foundation['work_canon']['chronology'][1])
        self.assertEqual(result[0]['source_commit_id'], record['commit_id'])
        self.assertTrue(all(len(unit['source_hash']) == 64 for unit in result))

    def test_known_chronology_ids_are_available_to_read_tools_without_fts_rows(self):
        foundation, _cast = self.roots()
        with RUNNER.index_connection(self.run) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM search_documents WHERE source_id='chronology_event_002'").fetchone()[0], 0)
        result = RUNNER.read_retrieval_tool(self.run, 'get_records', {'ids': ['chronology_event_002']})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['record_pointer'], '/work_canon/chronology/1')
        self.assertEqual(result[0]['immutable_source'], foundation['work_canon']['chronology'][1])

    def test_mixed_locators_keep_explicit_units_and_descriptive_citations(self):
        foundation, _cast = self.roots()
        precise = RUNNER.genesis_source_catalog(self.run)['central_incident']['source_ref']
        descriptive = {'artifact_type': 'genesis', 'artifact_id': foundation['commit_id'], 'source_locator': 'Overall foundation / context'}
        result = RUNNER.retrieve_original_sources(self.run, [{'sources': [precise, descriptive]}], limit=None, strict=True)
        self.assertEqual({unit['record_pointer'] for unit in result}, {'', '/work_canon/central_incident'})
        duplicate = precise | {'source_locator': 'A second explanation of this evidence'}
        result = RUNNER.retrieve_original_sources(self.run, [{'sources': [precise, duplicate]}], limit=None, strict=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['source_locators'], [precise['source_locator'], duplicate['source_locator']])

    def test_explicit_pointers_cannot_cross_source_identity(self):
        self.roots()
        reference = {'artifact_id': 'chronology_event_002', 'source_locator': 'second event', 'record_pointer': '/work_canon/chronology/0'}
        with self.assertRaisesRegex(RUNNER.IntegrityError, 'different source unit'):
            RUNNER.retrieve_original_sources(self.run, [{'sources': [reference]}], strict=True)

    def test_pointer_diagnostics_escape_rules_and_array_indices(self):
        record = {'commit_id': 'commit_fixture', 'record_type': 'genesis_foundation', 'a/b': {'~key': [10, 20]}}
        self.assertEqual(RUNNER.read_evidence_pointer(record, '/a~1b/~0key/1', source_id='source_fixture'), 20)
        self.assertIs(RUNNER.read_evidence_pointer(record, '', source_id='source_fixture'), record)
        for pointer in ('/a~1b/~0key/01', '/a~1b/~0key/-1', '/a~1b/~0key/-', '/a~1b/~0key/9', '/a~2b', '/a~1b/~0key/0/value'):
            with self.subTest(pointer=pointer), self.assertRaises(RUNNER.IntegrityError) as raised:
                RUNNER.read_evidence_pointer(record, pointer, source_id='source_fixture', archive='/tmp/synthetic-record.json')
            for fragment in ('source_fixture', 'commit_fixture', 'genesis_foundation', pointer, 'resolved prefix', '/tmp/synthetic-record.json'):
                self.assertIn(fragment, raised.exception.reason)

    def test_indexed_search_uses_the_same_strict_pointer_reader(self):
        foundation, _cast = self.roots()
        hit = {'commit_id': foundation['commit_id'], 'source_id': 'chronology_event_002',
            'pointer': '/work_canon/chronology/01', 'kind': 'root'}
        with self.assertRaisesRegex(RUNNER.IntegrityError, 'leading zeroes'):
            RUNNER.read_search_source(self.run, hit)

    def test_missing_transitive_proof_and_cycles_fail_closed(self):
        record = {'record_type': 'genesis_constraints', 'commit_id': 'commit_fixture', 'constraint_delta': {'canonical_facts': [
            {'fact_id': 'fact_a', 'sources': [{'artifact_id': 'fact_missing', 'source_locator': '/opaque'}]}]}}
        with self.assertRaisesRegex(RUNNER.IntegrityError, 'fact_missing'):
            RUNNER.retrieve_original_sources(self.run, [{'sources': [{'artifact_id': 'fact_a', 'source_locator': 'start'}]}], records=[record], strict=True, limit=None)
        record['constraint_delta']['canonical_facts'][0]['sources'][0]['artifact_id'] = 'fact_b'
        record['constraint_delta']['canonical_facts'].append({'fact_id': 'fact_b', 'sources': [{'artifact_id': 'fact_a', 'source_locator': 'cycle'}]})
        with self.assertRaisesRegex(RUNNER.IntegrityError, 'Cyclic evidence'):
            RUNNER.retrieve_original_sources(self.run, [{'sources': [{'artifact_id': 'fact_a', 'source_locator': 'start'}]}], records=[record], strict=True, limit=None)

    def test_precommit_rejects_provenance_cycles_without_committing(self):
        self.roots()
        payload = genesis_semantic_payload('central_incident')
        payload['canonical_facts'].append(copy.deepcopy(payload['canonical_facts'][0]) | {'predicate': 'second'})
        record = RUNNER.build_genesis_constraints(self.run, payload)
        first, second = record['constraint_delta']['canonical_facts']
        first['sources'] = [{'artifact_id': second['fact_id'], 'artifact_type': 'genesis', 'source_locator': 'other fact'}]
        second['sources'] = [{'artifact_id': first['fact_id'], 'artifact_type': 'genesis', 'source_locator': 'other fact'}]
        before = RUNNER.index_checkpoint(self.run)['ledger_sequence']
        with self.assertRaisesRegex(RUNNER.SchemaError, 'Cyclic evidence'):
            self.commit(record, 'genesis_constraints')
        self.assertEqual(RUNNER.index_checkpoint(self.run)['ledger_sequence'], before)
        self.assertEqual(len(RUNNER.committed_directories(self.run)), 2)

    def test_precommit_rejects_bad_explicit_pointers_with_reference_context(self):
        self.roots()
        record = RUNNER.build_genesis_constraints(self.run, genesis_semantic_payload('chronology_event_002'))
        fact = record['constraint_delta']['canonical_facts'][0]
        fact['sources'][0]['record_pointer'] = '/work_canon/chronology/99'
        before = RUNNER.index_checkpoint(self.run)['ledger_sequence']
        with self.assertRaises(RUNNER.SchemaError) as raised:
            self.commit(record, 'genesis_constraints')
        self.assertIn(fact['fact_id'], raised.exception.reason)
        self.assertIn('/work_canon/chronology/99', raised.exception.reason)
        self.assertEqual(RUNNER.index_checkpoint(self.run)['ledger_sequence'], before)

    def test_hash_mismatches_are_integrity_errors_even_for_optional_reads(self):
        foundation, _cast = self.roots()
        source = {'artifact_id': 'chronology_event_002', 'source_locator': '/chronology/002',
            'source_commit_id': foundation['commit_id'], 'source_hash': '0' * 64}
        with self.assertRaisesRegex(RUNNER.IntegrityError, 'source_hash mismatch'):
            RUNNER.retrieve_original_sources(self.run, [{'constraint_id': 'obligation_fixture', 'sources': [source]}])

    def test_required_closures_are_not_silently_cut_at_optional_limits(self):
        self.facts()
        roots = [{'sources': [{'artifact_id': 'fact_4448656f7d387136', 'source_locator': '/chronology/002'}]}]
        with self.assertRaises(RUNNER.PausedError) as raised:
            RUNNER.retrieve_original_sources(self.run, roots, strict=True, limit=1)
        self.assertEqual(raised.exception.failure_class, 'budget_exhaustion')
        self.assertEqual(len(RUNNER.retrieve_original_sources(self.run, roots, limit=1)), 1)
        self.assertEqual(len(RUNNER.retrieve_original_sources(self.run, roots, limit=None, strict=True)), 2)

    def test_json_fact_values_are_not_mistaken_for_provenance_declarations(self):
        record = {'record_type': 'genesis_constraints', 'commit_id': 'commit_fixture', 'constraint_delta': {'canonical_facts': [
            {'fact_id': 'fact_a', 'sources': [{'artifact_id': 'source_real', 'source_locator': 'actual'}],
             'value': {'sources': ['A fictional bibliography'], 'artifact_id': 'not_an_engine_reference'}}]}}
        references = RUNNER.record_evidence_references(record)
        self.assertEqual(references, [{'constraint_id': 'fact_a', 'sources': [{'artifact_id': 'source_real', 'source_locator': 'actual'}]}])

    def test_long_provenance_chains_do_not_use_python_recursion(self):
        facts = [{'fact_id': f'fact_{index}', 'sources': [{'artifact_id': f'fact_{index-1}' if index else 'scene_fixture', 'source_locator': 'original'}]}
            for index in range(1100)]
        record = {'record_type': 'creative_packet', 'commit_id': 'commit_fixture', 'scenes': [{'scene_id': 'scene_fixture', 'prose_mdx': 'Original.'}],
            'constraint_delta': {'canonical_facts': facts}}
        result = RUNNER.retrieve_original_sources(self.run, [{'sources': [{'artifact_id': 'fact_1099', 'source_locator': 'start'}]}],
            records=[record], strict=True, limit=None)
        self.assertEqual(len(result), 1101)
        self.assertEqual(result[-1]['immutable_source']['prose_mdx'], 'Original.')


if __name__ == '__main__':
    unittest.main()
