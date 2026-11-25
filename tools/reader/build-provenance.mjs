import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';

const sourceEntries = ['handbook', 'codes', 'tools/reader', 'Makefile', 'LICENSE'];
const excludedNames = new Set(['.DS_Store', '__pycache__', 'node_modules']);

async function hashTree(root, entries) {
  const hash = createHash('sha256');
  async function visit(file) {
    const stat = await fs.lstat(file);
    const label = path.relative(root, file).split(path.sep).join('/');
    if (stat.isDirectory()) {
      for (const name of (await fs.readdir(file)).sort()) {
        if (!excludedNames.has(name) && !name.endsWith('.pyc')) {
          await visit(path.join(file, name));
        }
      }
    } else if (stat.isFile()) {
      const contents = createHash('sha256').update(await fs.readFile(file)).digest('hex');
      hash.update(JSON.stringify([label, contents]) + '\n');
    } else {
      throw new Error(`Cannot record non-file build entry: ${label}`);
    }
  }
  for (const entry of entries) await visit(path.join(root, entry));
  return hash.digest('hex');
}

export async function snapshotDeliverySource(root) {
  const entries = [];
  for (const entry of sourceEntries) {
    try {
      await fs.stat(path.join(root, entry));
      entries.push(entry);
    } catch (error) {
      if (entry !== 'LICENSE' || error.code !== 'ENOENT') throw error;
    }
  }
  return hashTree(root, entries);
}

function recordPath(root, kind) {
  return path.join(root, 'work/release-provenance', `${kind}.json`);
}

export async function recordDeliveryBuild(root, kind, artifact, sourceDigest) {
  if (await snapshotDeliverySource(root) !== sourceDigest) {
    throw new Error(`Source changed while building ${kind}. Rebuild from one source snapshot.`);
  }
  const output = path.relative(root, artifact);
  const outputDigest = await hashTree(root, [output]);
  const record = { schemaVersion: 1, kind, output, outputDigest, sourceDigest };
  const file = recordPath(root, kind);
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, JSON.stringify(record, null, 2) + '\n');
}

export async function verifyDeliveryBuilds(root, artifacts) {
  const sourceDigest = await snapshotDeliverySource(root);
  for (const [kind, artifact] of Object.entries(artifacts)) {
    const output = path.relative(root, artifact);
    const record = JSON.parse(await fs.readFile(recordPath(root, kind), 'utf8'));
    if (record.schemaVersion !== 1 || record.kind !== kind ||
        record.sourceDigest !== sourceDigest || record.output !== output ||
        record.outputDigest !== await hashTree(root, [output])) {
      throw new Error(`The ${kind} build is stale or changed. Rebuild it from the current sources.`);
    }
  }
  return sourceDigest;
}
