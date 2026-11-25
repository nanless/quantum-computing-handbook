"""Regression checks for validation scopes, timeout handling and saved archives."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_all
from algorithms import round73_checks
from sdk.round73 import check_saved


class UnifiedRunnerTests(unittest.TestCase):
    def test_standalone_marker_cannot_override_repository_scope(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(run_all, 'ROOT', Path(directory)):
            self.assertEqual(run_all.validation_profile(), 'full-repository')
            marker = run_all.ROOT / 'CODE-VALIDATION.json'
            marker.write_text(json.dumps(run_all.RELEASE_MANIFEST), encoding='utf-8')
            self.assertEqual(run_all.validation_profile(), 'authored-code-release')
            (run_all.ROOT / '.git').mkdir()
            self.assertEqual(run_all.validation_profile(), 'full-repository')

    def test_timeout_does_not_stop_independent_checks(self):
        commands = [['first.py'], ['second.py']]
        results = [
            subprocess.TimeoutExpired('first.py', 90, output=b'partial output'),
            subprocess.CompletedProcess('second.py', 0, stdout='finished', stderr=''),
        ]
        with tempfile.TemporaryDirectory() as directory, patch.object(run_all, 'COMMANDS', commands):
            dest = Path(directory) / 'code-validation.json'
            dest.write_text('{"status":"passed","checks":[]}', encoding='utf-8')
            with patch.object(run_all.subprocess, 'run', side_effect=results) as process:
                self.assertEqual(run_all.main(['--output-dir', directory]), 1)
            self.assertEqual(process.call_count, 2)
            report = json.loads(dest.read_text(encoding='utf-8'))
            self.assertEqual(report['status'], 'failed')
            self.assertEqual([row['status'] for row in report['checks']], ['timed_out', 'passed'])
            self.assertEqual(report['checks'][0]['stdout'], 'partial output')
            self.assertEqual(report['checks'][1]['stdout'], 'finished')


class SLCArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = check_saved.load('slc-results.json')
        cls.raw = check_saved.load('slc-randomizations-counts.json')

    def replay(self, archive):
        files = {'slc-results.json': self.summary, 'slc-randomizations-counts.json': archive}
        with patch.object(check_saved, 'load', side_effect=files.__getitem__):
            return check_saved.slc()

    def test_complete_archive_recomputes_shots_and_cluster_errors(self):
        report = self.replay(self.raw)
        self.assertEqual(report['randomizations'], 3072)
        self.assertEqual(report['shots'], 196608)
        self.assertAlmostEqual(report['batches'][0]['cluster_standard_error'], 0.014756246405037593)

    def test_empty_and_missing_raw_batches_fail(self):
        for archive in ([], self.raw[:-1]):
            with self.subTest(batches=len(archive)), self.assertRaisesRegex(AssertionError, 'three raw SLC'):
                self.replay(archive)

    def test_repeated_batch_fails(self):
        with self.assertRaisesRegex(AssertionError, 'duplicate raw SLC batch'):
            self.replay([self.raw[0], self.raw[0], self.raw[2]])

    def test_truncated_sign_vector_fails(self):
        archive = copy.deepcopy(self.raw)
        archive[0]['pauli_signs'][0].pop()
        with self.assertRaisesRegex(AssertionError, 'invalid sign vector'):
            self.replay(archive)

    def test_duplicate_json_key_fails(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
            json.loads('{"010":9,"010":1}', object_pairs_hook=check_saved.unique_object)


class AlgorithmArchiveTests(unittest.TestCase):
    def test_archive_presence_required(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FileNotFoundError, 'Missing required SDK archive'):
                round73_checks.compare_archive({'07': round73_checks.hhl()}, Path(directory) / 'missing.json')

    def test_truncated_hhl_archive_fails(self):
        path = round73_checks.ROOT / 'sdk73/results-all.json'
        archive = json.loads(path.read_text(encoding='utf-8'))
        archive['cases']['hhl']['cases'].pop(1)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'truncated.json'
            target.write_text(json.dumps(archive), encoding='utf-8')
            with self.assertRaisesRegex(AssertionError, 'Missing or duplicate HHL'):
                round73_checks.compare_archive({'07': round73_checks.hhl()}, target)

    def test_missing_qsvt_case_fails(self):
        path = round73_checks.ROOT / 'sdk73/results-all.json'
        archive = json.loads(path.read_text(encoding='utf-8'))
        del archive['cases']['qsvt']
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'missing-qsvt.json'
            target.write_text(json.dumps(archive), encoding='utf-8')
            with self.assertRaisesRegex(KeyError, 'qsvt'):
                round73_checks.compare_archive({'16': round73_checks.polynomial()}, target)


if __name__ == '__main__':
    unittest.main()
