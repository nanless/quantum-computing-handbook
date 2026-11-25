"""Use a local release double to check failure and retry paths without GitHub."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "release_publish", Path(__file__).with_name("release-publish.py")
)
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)
VERSION = "v1.2.3"
COMMIT = "0" * 40


class ReleaseTest(unittest.TestCase):
    def setUp(self):
        work = tempfile.TemporaryDirectory()
        self.addCleanup(work.cleanup)
        self.directory = Path(work.name)
        self.files = [
            "quantum-computing-handbook.pdf", "quantum-computing-handbook.epub",
            f"quantum-computing-handbook-{VERSION}-web.zip",
            f"quantum-computing-handbook-{VERSION}-codes.zip",
        ]
        records = []
        for name in self.files:
            file = self.directory / name
            file.write_text(name, encoding="utf-8")
            records.append({"name": name, "bytes": file.stat().st_size,
                            "sha256": publisher.sha256(file)})
        info = self.directory / publisher.BUILD_INFO
        info.write_text(json.dumps({
            "schemaVersion": 1, "sourceCommit": COMMIT, "sourceState": "clean",
            "sourceDigest": "6" * 64,
            "version": VERSION, "artifacts": records,
        }), encoding="utf-8")
        (self.directory / publisher.CHECKSUMS).write_text("".join(
            f"{publisher.sha256(self.directory / name)}  {name}\n"
            for name in self.files + [publisher.BUILD_INFO]
        ), encoding="utf-8")
        self.release = None
        self.changes = []
        self.remote_commit = COMMIT
        self.stop_upload = False
        self.previous_release = b"older release bytes"

    def run_command(self, *args, capture=False):
        if args[:3] == ("git", "rev-parse", "HEAD"):
            return COMMIT + "\n"
        if args[:2] == ("git", "ls-remote"):
            ref = f"refs/tags/{VERSION}"
            return f'{"a" * 40}\t{ref}\n{self.remote_commit}\t{ref}^{{}}\n'
        assert args[:2] == ("gh", "release")
        verb = args[2]
        if verb == "view":
            if self.release is None:
                raise subprocess.CalledProcessError(1, args, stderr="release not found")
            return json.dumps(self.release)
        if verb == "download":
            target = Path(args[args.index("--dir") + 1])
            selected = [args[i + 1] for i, arg in enumerate(args) if arg == "--pattern"]
            if not set(selected) <= {asset["name"] for asset in self.release["assets"]}:
                raise subprocess.CalledProcessError(1, args)
            for name in selected:
                shutil.copyfile(self.directory / name, target / name)
            return None
        self.changes.append(verb)
        if verb == "create":
            assert "--verify-tag" in args
            assert "--draft" in args
            self.release = {"isDraft": True, "body": args[args.index("--notes") + 1], "assets": []}
        elif verb == "upload":
            assert "--clobber" not in args
            for file in args[4:args.index("-R")]:
                self.release["assets"].append({"name": Path(file).name})
                if self.stop_upload:
                    raise subprocess.CalledProcessError(1, args)
        elif verb == "edit":
            assert "--draft=false" in args
            assert args[args.index("--tag") + 1] == VERSION
            self.release["isDraft"] = False
        elif verb == "delete-asset":
            name = args[4]
            self.release["assets"] = [asset for asset in self.release["assets"] if asset["name"] != name]
        else:
            self.fail(f"Unexpected release command {verb}")

    def publish(self):
        with patch.object(publisher, "run", self.run_command):
            publisher.publish(self.directory, VERSION, COMMIT, "example/handbook", False)

    def test_mismatched_tag_and_tampered_file_cannot_create_release(self):
        self.remote_commit = "b" * 40
        with self.assertRaisesRegex(ValueError, "does not point"):
            self.publish()
        self.remote_commit = COMMIT
        (self.directory / self.files[0]).write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
            self.publish()
        self.assertEqual(self.changes, [])

    def test_failed_upload_stays_draft_and_same_suite_resumes(self):
        self.stop_upload = True
        with self.assertRaises(subprocess.CalledProcessError):
            self.publish()
        self.assertTrue(self.release["isDraft"])
        self.assertEqual(self.changes, ["create", "upload"])
        self.assertEqual(self.previous_release, b"older release bytes")

        self.stop_upload = False
        self.publish()
        self.assertFalse(self.release["isDraft"])
        self.assertEqual(self.changes, ["create", "upload", "upload", "edit"])
        self.publish()
        self.assertEqual(self.changes, ["create", "upload", "upload", "edit"])

    def test_existing_public_release_is_never_overwritten(self):
        self.release = {"isDraft": False, "body": "different build", "assets": []}
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.publish()
        self.assertEqual(self.changes, [])

    def test_retry_removes_only_an_empty_owned_draft_placeholder(self):
        self.stop_upload = True
        with self.assertRaises(subprocess.CalledProcessError):
            self.publish()
        self.release["assets"][0].update(state="starter", size=0)
        self.stop_upload = False
        self.publish()
        self.assertEqual(self.changes, ["create", "upload", "delete-asset", "upload", "edit"])


if __name__ == "__main__":
    unittest.main()
