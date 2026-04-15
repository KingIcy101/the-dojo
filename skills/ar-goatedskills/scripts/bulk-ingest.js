#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = '/home/podhi/.openclaw/workspace';
const { parseArgs } = require(`${WORKSPACE}/shared/args`);

const INGEST_SCRIPT = path.join(__dirname, 'ingest.js');
const DELAY_MS = 1000;

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function main() {
  const args = parseArgs(process.argv.slice(2), {});

  const filePath = args._[0];
  if (!filePath) {
    console.error('Usage: bulk-ingest.js <urls_file> [--tags X] [--type X]');
    process.exit(1);
  }

  const resolved = path.resolve(filePath);
  if (!fs.existsSync(resolved)) {
    console.error(`File not found: ${resolved}`);
    process.exit(1);
  }

  const lines = fs.readFileSync(resolved, 'utf8').split('\n');
  const entries = lines
    .map(l => l.trim())
    .filter(l => l && !l.startsWith('#'));

  if (entries.length === 0) {
    console.log('No URLs/entries found in file.');
    return;
  }

  console.log(`\nBulk ingesting ${entries.length} entries...\n`);

  let success = 0;
  let failed = 0;

  for (let i = 0; i < entries.length; i++) {
    const entry = entries[i];
    const progress = `[${i + 1}/${entries.length}]`;

    // Build command
    const extraArgs = [];
    if (args.tags) extraArgs.push(`--tags "${args.tags}"`);
    if (args.type) extraArgs.push(`--type ${args.type}`);

    const isText = !entry.startsWith('http') && !entry.startsWith('/') && !entry.startsWith('./');
    const inputArg = isText ? `--text "${entry.replace(/"/g, '\\"')}"` : `"${entry}"`;
    const cmd = `node "${INGEST_SCRIPT}" ${inputArg} ${extraArgs.join(' ')}`;

    process.stdout.write(`${progress} ${entry.slice(0, 60)}... `);

    try {
      const output = execSync(cmd, { encoding: 'utf8', timeout: 60000 });
      console.log('✓');
      // Print last line of output (the "Ingested:" line)
      const lines = output.trim().split('\n');
      const lastLine = lines[lines.length - 1];
      if (lastLine) console.log(`        ${lastLine}`);
      success++;
    } catch (err) {
      console.log('✗');
      const errMsg = (err.stderr || err.message || '').trim().split('\n')[0];
      if (errMsg) console.log(`        Error: ${errMsg}`);
      failed++;
    }

    if (i < entries.length - 1) {
      await sleep(DELAY_MS);
    }
  }

  console.log(`\n${'─'.repeat(50)}`);
  console.log(`Bulk ingest complete: ${success} succeeded, ${failed} failed`);
  console.log();
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
