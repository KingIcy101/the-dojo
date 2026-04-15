#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const WORKSPACE = '/home/podhi/.openclaw/workspace';
const { EmbeddingGenerator } = require(`${WORKSPACE}/shared/embeddings`);
const { parseArgs } = require(`${WORKSPACE}/shared/args`);

const { getDb } = require('./db-init');
const { chunkText } = require('./chunker');

// ── HTML helpers ──────────────────────────────────────────────────────────────

function stripHtml(html) {
  // Remove script and style blocks entirely
  let text = html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, ' ')
    .replace(/<nav[\s\S]*?<\/nav>/gi, ' ')
    .replace(/<footer[\s\S]*?<\/footer>/gi, ' ')
    .replace(/<header[\s\S]*?<\/header>/gi, ' ')
    // Block elements → newlines
    .replace(/<\/(p|div|section|article|h[1-6]|li|br|tr)>/gi, '\n')
    .replace(/<br\s*\/?>/gi, '\n')
    // Strip remaining tags
    .replace(/<[^>]+>/g, ' ')
    // Decode common HTML entities
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&mdash;/g, '—')
    .replace(/&ndash;/g, '–')
    .replace(/&#(\d+);/g, (_, code) => String.fromCharCode(Number(code)))
    // Collapse whitespace
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  return text;
}

function extractTitle(html) {
  const m = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  if (m) return m[1].trim();
  const h1 = html.match(/<h1[^>]*>([^<]+)<\/h1>/i);
  if (h1) return h1[1].trim();
  return null;
}

// ── Fetch URL ─────────────────────────────────────────────────────────────────

const { execSync } = require('child_process');

async function fetchUrl(url) {
  let html;

  // Try native fetch first, fall back to curl
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; KnowledgeBase/1.0)',
        'Accept': 'text/html,application/xhtml+xml,*/*',
      },
      redirect: 'follow',
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    html = await res.text();
  } catch (_) {
    // Fall back to curl
    try {
      html = execSync(
        `curl -sL --max-time 30 -A "Mozilla/5.0 (compatible; KnowledgeBase/1.0)" "${url}"`,
        { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
      );
    } catch (curlErr) {
      throw new Error(`Failed to fetch ${url}: ${curlErr.message}`);
    }
  }

  const title = extractTitle(html);
  const content = stripHtml(html);
  return { title, content };
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv.slice(2), {
    type: 'article',
    threshold: 0.3,
    limit: 5,
  });

  let inputText = null;
  let url = null;
  let title = args.title || null;
  const type = args.type || 'article';
  const tags = args.tags || null;

  if (args.text) {
    // Raw text mode
    inputText = String(args.text);
    if (!title) title = inputText.slice(0, 60) + (inputText.length > 60 ? '...' : '');
  } else if (args._.length > 0) {
    const input = args._[0];
    if (input.startsWith('http://') || input.startsWith('https://')) {
      url = input;
      console.log(`Fetching ${url}...`);
      try {
        const result = await fetchUrl(url);
        inputText = result.content;
        if (!title && result.title) title = result.title;
      } catch (err) {
        console.error(`Failed to fetch URL: ${err.message}`);
        process.exit(1);
      }
    } else if (input.startsWith('/') || input.startsWith('./') || input.startsWith('../')) {
      // File path
      const filePath = path.resolve(input);
      if (!fs.existsSync(filePath)) {
        console.error(`File not found: ${filePath}`);
        process.exit(1);
      }
      inputText = fs.readFileSync(filePath, 'utf8');
      if (!title) title = path.basename(filePath);
    } else {
      // Treat as raw text
      inputText = input;
      if (!title) title = inputText.slice(0, 60) + (inputText.length > 60 ? '...' : '');
    }
  } else {
    console.error('Usage: ingest.js <url|filepath|text> [--text "raw text"] [--title X] [--type article|note|tweet|pdf] [--tags X]');
    process.exit(1);
  }

  if (!inputText || !inputText.trim()) {
    console.error('No content to ingest.');
    process.exit(1);
  }

  // Clean up excessive whitespace
  inputText = inputText.replace(/[ \t]+/g, ' ').replace(/\n{4,}/g, '\n\n\n').trim();

  const wordCount = inputText.split(/\s+/).filter(Boolean).length;

  // Chunk text
  const chunks = chunkText(inputText);
  if (chunks.length === 0) {
    console.error('Content too short or empty after processing.');
    process.exit(1);
  }

  // Generate embeddings
  console.log(`Generating embeddings for ${chunks.length} chunk(s)...`);
  const embedder = new EmbeddingGenerator();
  let embeddings;
  try {
    embeddings = await embedder.generateBatch(chunks);
  } catch (err) {
    console.error(`Embedding generation failed: ${err.message}`);
    process.exit(1);
  }

  // Store in DB
  const db = getDb();

  const insertSource = db.prepare(`
    INSERT INTO sources (url, title, type, tags, content, word_count, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
  `);

  const insertChunk = db.prepare(`
    INSERT INTO chunks (source_id, chunk_index, content, embedding, token_count, created_at)
    VALUES (?, ?, ?, ?, ?, datetime('now'))
  `);

  const ingestTx = db.transaction(() => {
    const sourceResult = insertSource.run(url || null, title || null, type, tags || null, inputText, wordCount);
    const sourceId = sourceResult.lastInsertRowid;

    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];
      const embedding = embeddings[i];
      const blob = Buffer.from(embedding.buffer);
      const tokenCount = chunk.split(/\s+/).filter(Boolean).length;
      insertChunk.run(sourceId, i, chunk, blob, tokenCount);
    }

    return sourceId;
  });

  const sourceId = ingestTx();

  db.close();

  console.log(`Ingested: "${title || url || 'Untitled'}" (ID: ${sourceId}, ${chunks.length} chunks)`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
