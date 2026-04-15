#!/usr/bin/env node
'use strict';

const WORKSPACE = '/home/podhi/.openclaw/workspace';
const { parseArgs } = require(`${WORKSPACE}/shared/args`);

const { getDb } = require('./db-init');

function main() {
  const args = parseArgs(process.argv.slice(2), {});

  const db = getDb();

  const conditions = [];
  const params = [];

  if (args.type) {
    conditions.push('type = ?');
    params.push(args.type);
  }

  if (args.tag) {
    conditions.push("tags LIKE ?");
    params.push(`%${args.tag}%`);
  }

  const where = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';
  const limit = args.recent ? `LIMIT ${Number(args.recent)}` : '';

  const rows = db.prepare(`
    SELECT id, title, url, type, tags, word_count, created_at
    FROM sources
    ${where}
    ORDER BY created_at DESC
    ${limit}
  `).all(...params);

  db.close();

  if (rows.length === 0) {
    console.log('No entries found.');
    return;
  }

  console.log(`\nKnowledge Base — ${rows.length} entr${rows.length === 1 ? 'y' : 'ies'}\n${'─'.repeat(60)}`);
  for (const row of rows) {
    const title = row.title || row.url || 'Untitled';
    const tags = row.tags ? ` [${row.tags}]` : '';
    const date = row.created_at ? row.created_at.slice(0, 10) : '?';
    const words = row.word_count ? ` ${row.word_count}w` : '';
    console.log(`[${row.id}] ${title} (${row.type})${tags}${words} | ${date}`);
  }
  console.log();
}

main();
