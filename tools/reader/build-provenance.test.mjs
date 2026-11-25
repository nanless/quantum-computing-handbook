import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { recordDeliveryBuild, snapshotDeliverySource, verifyDeliveryBuilds } from './build-provenance.mjs';

test('a release suite rejects stale source or a changed output', async t => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'handbook-source-test-'));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  await Promise.all(['handbook', 'codes', 'tools/reader', 'dist'].map(dir =>
    fs.mkdir(path.join(root, dir), { recursive: true })
  ));
  const chapter = path.join(root, 'handbook/chapter.md');
  const pdf = path.join(root, 'dist/book.pdf');
  await fs.writeFile(chapter, 'first');
  await fs.writeFile(path.join(root, 'Makefile'), 'build');
  await fs.writeFile(pdf, 'printed page');
  const digest = await snapshotDeliverySource(root);
  await recordDeliveryBuild(root, 'pdf', pdf, digest);
  assert.equal(await verifyDeliveryBuilds(root, { pdf }), digest);

  await fs.writeFile(chapter, 'second');
  await assert.rejects(verifyDeliveryBuilds(root, { pdf }), /stale or changed/);
  await assert.rejects(recordDeliveryBuild(root, 'pdf', pdf, digest), /Source changed/);
  await fs.writeFile(chapter, 'first');
  await fs.writeFile(pdf, 'other printed page');
  await assert.rejects(verifyDeliveryBuilds(root, { pdf }), /stale or changed/);
});
