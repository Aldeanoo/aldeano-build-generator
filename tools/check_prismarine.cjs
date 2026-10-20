// Optional second independent reader. See docs/test-results.md for installation.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const zlib = require('node:zlib');
const nbt = require(path.resolve(__dirname, '../.cache/nbt-check/node_modules/prismarine-nbt'));

async function main() {
  const manifest = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const results = [];
  for (const item of manifest) {
    const blob = fs.readFileSync(item.file);
    const { parsed, type, metadata } = await nbt.parse(blob);
    assert.equal(type, item.format);
    const raw = item.format === 'big' ? zlib.gunzipSync(blob) : blob;
    assert.equal(metadata.size, raw.length, 'Entire NBT must be consumed');
    assert.deepEqual(nbt.simplify(parsed), JSON.parse(fs.readFileSync(item.expected, 'utf8')));
    assert.ok(nbt.writeUncompressed(parsed, type).equals(raw), 'Independent binary roundtrip');
    results.push({ file: item.file, bytes: blob.length, format: type, passed: true });
  }
  console.log(JSON.stringify({ reader: 'prismarine-nbt',
    version: require('../.cache/nbt-check/node_modules/prismarine-nbt/package.json').version,
    checked: results.length, files: results }, null, 2));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
