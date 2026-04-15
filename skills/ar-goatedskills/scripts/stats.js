#!/usr/bin/env node
'use strict';

const fs = require('fs');

const { getDb, DB_PATH } = require('./db-init');

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
}

function main() {
  const db = getDb();

  const totalSources = db.prepare('SELECT COUNT(*) as count FROM sources').get().count;
  const totalChunks = db.prepare('SELECT COUNT(*) as count FROM chunks').get().count;
  const lastIngest = db.prepare('SELECT MAX(created_at) as last FROM sources').get().last;

  const byType = db.prepare(`
    SELECT type, COUNT(*) as count
    FROM sources
    GROUP BY type
    ORDER BY count DESC
  `).all();

  db.close();

  // DB file size
  let dbSize = 'N/A';
  try {
    const stat = fs.statSync(DB_PATH);
    dbSize = formatBytes(stat.size);
  } catch (_) {}

  console.log('\n📚 Knowledge Base Stats');
  console.log('─'.repeat(40));
  console.log(`  Total sources : ${totalSources}`);
  console.log(`  Total chunks  : ${totalChunks}`);
  console.log(`  Database size : ${dbSize}`);
  console.log(`  Last ingested : ${lastIngest ? lastIngest.slice(0, 16) : 'never'}`);

  if (byType.length > 0) {
    console.log('\n  Breakdown by type:');
    for (const row of byType) {
      console.log(`    ${row.type.padEnd(12)} : ${row.count}`);
    }
  }

  console.log();
}

main();
