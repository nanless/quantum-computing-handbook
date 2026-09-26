#!/usr/bin/env python3
"""Offline regression tests for snapshot publication, isolated in temporary dirs.

Run from any directory: python3 /path/to/codes/tests/test_snapshot_sources.py
Only standard-library dependencies. No git, curl, or upstream code is executed.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

SOURCE = pathlib.Path(__file__).resolve().parents[1] / 'snapshot_sources.py'
NEW_COMMIT = 'a' * 40
OLD_COMMIT = 'b' * 40


def tree_hashes(directory):
    """Include the manifest, README, marker, and all source bytes in comparison."""
    return {
        str(item.relative_to(directory)): hashlib.sha256(item.read_bytes()).hexdigest()
        for item in directory.rglob('*') if item.is_file()
    }


class SnapshotPublicationTests(unittest.TestCase):
    def setUp(self):
        # Import a fresh module per case to avoid retaining patched globals.
        spec = importlib.util.spec_from_file_location('snapshot_sources_under_test', SOURCE)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory(prefix='handbook-snapshot-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = pathlib.Path(self.temp.name)
        self.module.BASE = self.base
        self.module.MANIFEST = self.base / 'vendor' / 'manifest.json'
        self.module.PROJECTS = {'demo': ('example/demo', ['demo.py'])}
        self.old_tree = self.seed_old_snapshot()
        self.rename_calls = []
        self.download_calls = []
        self.log = io.StringIO()

    def seed_old_snapshot(self):
        vendor = self.base / 'vendor'
        (vendor / 'demo').mkdir(parents=True)
        records = []
        for name, data in [('LICENSE', b'OLD LICENSE'), ('demo.py', b'old source')]:
            (vendor / 'demo' / name).write_bytes(data)
            records.append({
                'path': name, 'bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest(),
                'url': 'https://example.invalid/' + name,
            })
        manifest = {'projects': [{
            'name': 'demo', 'commit': OLD_COMMIT,
            'repository': 'https://example.invalid/demo', 'files': records,
        }]}
        (vendor / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        (vendor / 'README.md').write_text('OLD README', encoding='utf-8')
        (vendor / 'old-marker.txt').write_text('old snapshot sentinel', encoding='utf-8')
        return tree_hashes(vendor)

    def invoke(self, *, mode='--refresh', source_failure=None, fail_rename=None):
        """Mock every external operation; keep real writes/renames under self.base."""
        real_replace = self.module.os.replace

        def fake_command(args):
            self.assertEqual(args, [
                'git', 'ls-remote', 'https://github.com/example/demo.git', 'HEAD',
            ])
            return (NEW_COMMIT + '\tHEAD\n').encode()

        def fake_download(url, optional=False):
            self.download_calls.append(url)
            if url.endswith('/demo.py'):
                if source_failure == 'missing':
                    self.assertTrue(optional)
                    return None
                if source_failure == 'exception':
                    raise RuntimeError('injected download failure')
                return b'new source'
            if url.endswith('/LICENSE'):
                return b'NEW LICENSE'
            if optional:
                return None
            raise AssertionError('Unexpected mocked URL: ' + url)

        def fake_replace(source, destination):
            source, destination = pathlib.Path(source), pathlib.Path(destination)
            # Prevent a future implementation change from touching real paths.
            self.assertIn(self.base, source.parents)
            self.assertIn(self.base, destination.parents)
            self.rename_calls.append((source.relative_to(self.base),
                                      destination.relative_to(self.base)))
            if fail_rename == len(self.rename_calls):
                raise OSError('injected rename failure')
            return real_replace(source, destination)

        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(self.module, 'command', fake_command))
            stack.enter_context(patch.object(self.module, 'download', fake_download))
            stack.enter_context(patch.object(self.module.os, 'replace', fake_replace))
            stack.enter_context(patch.object(sys, 'argv', ['snapshot_sources.py', mode]))
            stack.enter_context(contextlib.redirect_stdout(self.log))
            # A new unexpected subprocess path must fail, never contact the network.
            stack.enter_context(patch.object(
                self.module.subprocess, 'check_output',
                side_effect=AssertionError('External subprocess forbidden in offline test'),
            ))
            self.module.main()

    def check_old_unchanged(self):
        self.assertEqual(tree_hashes(self.base / 'vendor'), self.old_tree)
        self.assertEqual(list(self.base.glob('.snapshot-*')), [])

    def test_missing_source_does_not_publish(self):
        with self.assertRaisesRegex(RuntimeError, 'no source paths found'):
            self.invoke(source_failure='missing')
        self.assertTrue(any(url.endswith('/LICENSE') for url in self.download_calls))
        self.assertEqual(self.rename_calls, [])
        self.check_old_unchanged()

    def test_download_exception_preserves_snapshot(self):
        with self.assertRaisesRegex(RuntimeError, 'injected download failure'):
            self.invoke(source_failure='exception')
        self.assertEqual(self.rename_calls, [])
        self.check_old_unchanged()

    def test_success_publishes_matching_files_and_manifest(self):
        self.invoke()
        vendor = self.base / 'vendor'
        self.assertEqual(len(self.rename_calls), 2)
        self.assertEqual((vendor / 'demo' / 'demo.py').read_bytes(), b'new source')
        self.assertEqual((vendor / 'demo' / 'LICENSE').read_bytes(), b'NEW LICENSE')
        data = json.loads((vendor / 'manifest.json').read_text())
        self.assertEqual(data['projects'][0]['commit'], NEW_COMMIT)
        self.assertEqual(data['projects'][0]['missing_requested_paths'], [])
        self.assertIn(NEW_COMMIT, (vendor / 'README.md').read_text())
        self.assertFalse((vendor / 'old-marker.txt').exists())
        with contextlib.redirect_stdout(self.log):
            self.module.verify(data)
        self.assertEqual(list(self.base.glob('.snapshot-*')), [])

    def test_first_rename_failure_preserves_snapshot(self):
        with self.assertRaisesRegex(OSError, 'injected rename failure'):
            self.invoke(fail_rename=1)
        self.assertEqual(len(self.rename_calls), 1)
        self.check_old_unchanged()

    def test_publication_rename_failure_rolls_back_previous(self):
        with self.assertRaisesRegex(OSError, 'injected rename failure'):
            self.invoke(fail_rename=2)
        self.assertEqual(len(self.rename_calls), 3)
        old_source, backup = self.rename_calls[0]
        rollback_source, rollback_destination = self.rename_calls[2]
        self.assertEqual(old_source, pathlib.Path('vendor'))
        self.assertEqual(rollback_source, backup)
        self.assertEqual(rollback_destination, pathlib.Path('vendor'))
        self.check_old_unchanged()

    def test_fetch_hash_mismatch_does_not_publish(self):
        # Existing manifest expects OLD LICENSE; mocked response is NEW LICENSE.
        with self.assertRaisesRegex(AssertionError, 'https://example.invalid/LICENSE'):
            self.invoke(mode='--fetch')
        self.assertEqual(self.rename_calls, [])
        self.check_old_unchanged()


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: snapshot integrity assertions must stay enabled')
    unittest.main(verbosity=2)
