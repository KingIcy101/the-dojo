#!/usr/bin/env node
'use strict';

const WORKSPACE = '/home/podhi/.openclaw/workspace';
const { EmbeddingGenerator } = require(`${WORKSPACE}/shared/embeddings`);
const { parseArgs } = require(`${WORKSPACE}/shared/args`);

const { getDb } = require('./db-init');

async function main() {
  const args = parseArgs(process.argv.slice(2), {
    limit: 5,
    threshold: 0.3,
  });

  const query = args._[0] || args.query;
  if (!query) {
    console.error('Usage: query.js "<question>" [--limit N] [--threshold 0.3] [--tags X]');
    process.exit(1);
  }

  const limit = Number(args.limit) || 5;
  const threshold = Number(args.threshold) || 0.3;
  const tagsFilter = args.tags ? String(args.tags) : null;

  // Generate query embedding
  const embedder = new EmbeddingGenerator();
  let queryEmbedding;
  try {
    queryEmbedding = await embedder.generate(String(query));
  } catch (err) {
    console.error(`Embedding generation failed: ${err.message}`);
    process.exit(1);
  }

  const db = getDb();

  // Build source filter
  let sourceFilter = '';
  const sourceParams = [];
  if (tagsFilter) {
    sourceFilter = `WHERE s.tags LIKE ?`;
    sourceParams.push(`%${tagsFilter}%`);
  }

  // Load all chunks with source info
  const rows = db.prepare(`
    SELECT
      c.id AS chunk_id,
      c.source_id,
      c.chunk_index,
      c.content AS chunk_content,
      c.embedding,
      s.title,
      s.type,
      s.url,
      s.tags,
      s.created_at
    FROM chunks c
    JOIN sources s ON s.id = c.source_id
    ${sourceFilter}
    ORDER BY c.source_id, c.chunk_index
  `).all(...sourceParams);

  db.close();

  if (rows.length === 0) {
    console.log('No entries in knowledge base' + (tagsFilter ? ` matching tag: ${tagsFilter}` : '') + '.');
    return;
  }

  // Compute cosine similarity for each chunk
  const scored = [];
  for (const row of rows) {
    if (!row.embedding) continue;
    const chunkEmbedding = new Float32Array(new Uint8Array(row.embedding).buffer);
    const sim = EmbeddingGenerator.cosineSimilarity(queryEmbedding, chunkEmbedding);
    if (sim >= threshold) {
      scored.push({ ...row, similarity: sim });
    }
  }

  if (scored.length === 0) {
    console.log(`No results above similarity threshold ${threshold}.`);
    return;
  }

  // Sort by similarity desc, dedupe by source (keep best chunk per source)
  scored.sort((a, b) => b.similarity - a.similarity);

  // Deduplicate: keep top chunk per source
  const seenSources = new Set();
  const topResults = [];
  for (const r of scored) {
    if (!seenSources.has(r.source_id)) {
      seenSources.add(r.source_id);
      topResults.push(r);
    }
    if (topResults.length >= limit) break;
  }

  console.log(`\nSearch results for: "${query}"\n${'─'.repeat(60)}`);
  for (const r of topResults) {
    const sim = r.similarity.toFixed(2);
    const title = r.title || r.url || 'Untitled';
    const date = r.created_at ? r.created_at.slice(0, 10) : 'unknown';
    const preview = r.chunk_content.replace(/\s+/g, ' ').slice(0, 200);
    const tags = r.tags ? `Tags: ${r.tags}` : '';

    console.log(`[${sim}] ${r.type.charAt(0).toUpperCase() + r.type.slice(1)}: "${title}" (ID: ${r.source_id}, ${r.type})`);
    console.log(`  ...${preview}...`);
    if (tags) console.log(`  ${tags} | Ingested: ${date}`);
    else console.log(`  Ingested: ${date}`);
    console.log();
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
