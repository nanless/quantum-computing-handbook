"""Verify an ebook release suite and publish it only from the matching Git tag."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


CHECKSUMS = "SHA256SUMS.txt"
BUILD_INFO = "BUILDINFO.json"
VERSION_PATTERN = re.compile(r"v?[0-9][0-9A-Za-z._-]*\Z")
SHA_PATTERN = re.compile(r"[0-9a-f]{40}\Z")


def run(*args, capture=False):
    return subprocess.run(args, check=True, text=True, capture_output=capture).stdout


def verify_tag(tag, commit):
    if not VERSION_PATTERN.fullmatch(tag) or ".." in tag:
        raise ValueError(f"Invalid release version: {tag}")
    if not SHA_PATTERN.fullmatch(commit):
        raise ValueError("A full Git commit ID is required")
    if run("git", "rev-parse", "HEAD", capture=True).strip() != commit:
        raise ValueError("The build commit differs from HEAD")
    ref = f"refs/tags/{tag}"
    lines = run("git", "ls-remote", "--exit-code", "--tags", "origin",
                ref, f"{ref}^{{}}", capture=True).splitlines()
    resolved = dict((name, obj) for obj, name in (line.split("\t") for line in lines))
    if resolved.get(f"{ref}^{{}}", resolved.get(ref)) != commit:
        raise ValueError(f"Remote tag {tag} does not point to {commit}")


def sha256(file):
    result = hashlib.sha256()
    with file.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def verify_suite(directory, version, commit):
    if not VERSION_PATTERN.fullmatch(version) or ".." in version:
        raise ValueError(f"Invalid release version: {version}")
    core = {
        "quantum-computing-handbook.pdf",
        "quantum-computing-handbook.epub",
        f"quantum-computing-handbook-{version}-web.zip",
        f"quantum-computing-handbook-{version}-codes.zip",
    }
    asset_names = core | {BUILD_INFO, CHECKSUMS}
    if {entry.name for entry in directory.iterdir()} != asset_names:
        raise ValueError("Unexpected or missing release suite files")

    sums = {}
    for line in (directory / CHECKSUMS).read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([0-9A-Za-z._-]+)", line)
        if not match or match[2] in sums:
            raise ValueError("Malformed or duplicate checksum entry")
        sums[match[2]] = match[1]
    if set(sums) != core | {BUILD_INFO}:
        raise ValueError("Checksum entries do not match the release suite")
    for name, expected in sums.items():
        if sha256(directory / name) != expected:
            raise ValueError(f"Checksum mismatch: {name}")

    info = json.loads((directory / BUILD_INFO).read_text(encoding="utf-8"))
    if (info["schemaVersion"], info["version"]) != (1, version):
        raise ValueError("Build information does not match the requested version")
    if not re.fullmatch(r"[0-9a-f]{64}", info["sourceDigest"]):
        raise ValueError("Build information does not identify a source snapshot")
    if commit and (info["sourceCommit"], info["sourceState"]) != (commit, "clean"):
        raise ValueError("Build information does not match the requested clean source")
    entries = info["artifacts"]
    if len(entries) != len(core) or {entry["name"] for entry in entries} != core:
        raise ValueError("Build information has missing or duplicate asset entries")
    for entry in entries:
        name = entry["name"]
        if entry["sha256"] != sums[name] or entry["bytes"] != (directory / name).stat().st_size:
            raise ValueError(f"Build information does not match packaged asset: {name}")
    return asset_names


def publish(directory, tag, commit, repository, prerelease):
    verify_tag(tag, commit)
    names = verify_suite(directory, tag, commit)
    expected = {name: sha256(directory / name) for name in names}
    marker = f"<!-- handbook-suite {expected[CHECKSUMS]} -->"

    def gh(*args, capture=False):
        return run("gh", "release", *args, "-R", repository, capture=capture)

    def release_info():
        return json.loads(gh("view", tag, "--json", "isDraft,body,assets", capture=True))

    try:
        release = release_info()
    except subprocess.CalledProcessError as error:
        detail = error.stderr or ""
        if not re.search(r"release not found|HTTP 404", detail, re.IGNORECASE):
            raise
        release = None

    if release is not None and not release["isDraft"]:
        if marker not in release["body"]:
            raise ValueError(f"Published release {tag} already exists with different build information")
    elif release is None:
        options = ["--prerelease"] if prerelease else []
        gh("create", tag, "--draft", "--verify-tag", "--target", commit,
           "--title", f"量子计算手册 {tag}", "--generate-notes",
           "--notes", f"构建提交 `{commit}`\n\n{marker}", *options)
        release = release_info()

    if marker not in release["body"]:
        raise ValueError(f"Release {tag} already exists for another suite")

    # A failed upload can leave a zero-byte placeholder in an owned draft.
    for asset in release["assets"]:
        name = asset["name"]
        if (release["isDraft"] and name in names and asset.get("state") == "starter"
                and asset.get("size") == 0):
            current = release_info()
            if not current["isDraft"] or marker not in current["body"] or asset not in current["assets"]:
                raise ValueError(f"Release changed before placeholder recovery: {name}")
            gh("delete-asset", tag, name, "--yes")
    release = release_info()
    remote_names = {asset["name"] for asset in release["assets"]}
    if remote_names - names:
        raise ValueError("The release contains assets outside the validated suite")

    def compare_downloads(assets):
        if not assets:
            return
        with tempfile.TemporaryDirectory(prefix="handbook-release-") as scratch:
            args = [arg for name in sorted(assets) for arg in ("--pattern", name)]
            gh("download", tag, *args, "--dir", scratch)
            for name in assets:
                if sha256(Path(scratch) / name) != expected[name]:
                    raise ValueError(f"Downloaded release asset differs: {name}")

    compare_downloads(remote_names)
    if not release["isDraft"]:
        if remote_names != names:
            raise ValueError(f"Published release {tag} has missing assets")
        print(f"{tag}: already published and verified")
        return

    missing = names - remote_names
    if missing:
        gh("upload", tag, *(str(directory / name) for name in sorted(missing)))
    compare_downloads(names)
    verify_tag(tag, commit)
    gh("edit", tag, "--tag", tag, "--draft=false", "--verify-tag")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("tag", "suite", "publish"))
    parser.add_argument("--version", required=True)
    parser.add_argument("--commit")
    parser.add_argument("--directory", type=Path, default=Path("dist/release"))
    parser.add_argument("--repository")
    parser.add_argument("--prerelease", action="store_true")
    args = parser.parse_args()
    if args.mode != "suite" and not args.commit:
        parser.error("--commit is required")
    if args.mode == "tag":
        verify_tag(args.version, args.commit)
    elif args.mode == "suite":
        verify_suite(args.directory, args.version, args.commit)
    else:
        if not args.repository:
            parser.error("--repository is required")
        publish(args.directory.resolve(), args.version, args.commit, args.repository, args.prerelease)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        if getattr(error, "stderr", None):
            print(error.stderr.strip(), file=sys.stderr)
        print(f"Release check failed: {error}", file=sys.stderr)
        sys.exit(1)
