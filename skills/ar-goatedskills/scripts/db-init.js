'use strict';

const path = require('path');
const WORKSPACE = '/home/podhi/.openclaw/workspace';
const { openDb } = require(`${WORKSPACE}/shared/db`);

const DB_PATH = path.join(__dirname, '..', 'data', 'knowledge.db');

const SCHEMA = `
CREATE TABLE IF NOT EXISTS sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT,
  title TEXT,
  type TEXT NOT NULL DEFAULT 'article',
  tags TEXT,
  summary TEXT,
  content TEXT,
  word_count INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chunks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  chunk_index INTEGER NOT NULL,
  content TEXT NOT NULL,
  embedding BLOB,
  token_count INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(type);
CREATE INDEX IF NOT EXISTS idx_sources_tags ON sources(tags);
CREATE INDEX IF NOT EXISTS idx_chunks_source ON chunks(source_id);
`;

function getDb() {
  const db = openDb(DB_PATH);
  db.exec(SCHEMA);
  return db;
}

module.exports = { getDb, DB_PATH };
