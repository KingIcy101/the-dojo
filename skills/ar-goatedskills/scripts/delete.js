#!/usr/bin/env node
'use strict';

const WORKSPACE = '/home/podhi/.openclaw/workspace';
const { parseArgs } = require(`${WORKSPACE}/shared/args`);

const { getDb } = require('./db-init');

function main() {
  const args = parseArgs(process.argv.slice(2), {});

  const id = args._[0];
  if (!id) {
    console.error('Usage: delete.js <source_id>');
    process.exit(1);
  }

  const sourceId = Number(id);
  if (!Number.isInteger(sourceId) || sourceId <= 0) {
    console.error(`Invalid source ID: ${id}`);
    process.exit(1);
  }

  const db = getDb();

  // Check source exists
  const source = db.prepare('SELECT id, title FROM sources WHERE id = ?').get(sourceId);
  if (!source) {
    console.error(`Source ${sourceId} not found.`);
    db.close();
    process.exit(1);
  }

  // Count chunks
  const chunkCount = db.prepare('SELECT COUNT(*) as count FROM chunks WHERE source_id = ?').get(sourceId).count;

  // Delete (cascading via FK)
  db.prepare('DELETE FROM sources WHERE id = ?').run(sourceId);

  db.close();

  console.log(`Deleted source ${sourceId} ("${source.title || 'Untitled'}") and ${chunkCount} chunk(s).`);
}

main();
