#!/usr/bin/env node
// memory-stack/runner.js
// PM2 entry point. Runs all memory processes on their schedules.

const { run: memoryWriter } = require('./memory-writer');
const { run: handoffWriter } = require('./handoff-writer');
const { run: consolidator } = require('./memory-consolidator');
const { run: correctionDetector } = require('./correction-detector');
const { run: repeatMistakeDetector } = require('./repeat-mistake-detector');
const { run: learningEffectivenessTracker } = require('./learning-effectiveness-tracker');
const { log, loadState, saveState } = require('./lib');
const cfg = require('./config');
const http = require('http');

const PROCESS = 'runner';
const CONTEXT_LIMIT = 200000;

// Tiered thresholds — each fires once per session, writes handoff + alerts Matt
const THRESHOLDS = [
  { pct: 0.70, key: 't70', label: '70%', emoji: '🟡', message: 'Context is 70% full — I\'ve backed up everything. Still plenty of room but heads up.' },
  { pct: 0.85, key: 't85', label: '85%', emoji: '🟠', message: 'Context is 85% full — backup written. Compaction likely coming soon if this session continues.' },
  { pct: 0.95, key: 't95', label: '95%', emoji: '🔴', message: 'Context is 95% full — emergency backup written. Compaction is imminent. I\'ll recover automatically from handoff note.' },
];

async function checkContextUsage() {
  return new Promise((resolve) => {
    const req = http.get(`${cfg.GATEWAY_URL}/api/sessions`, {
      headers: { 'Authorization': `Bearer ${cfg.GATEWAY_TOKEN}` }
    }, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', async () => {
        try {
          const json = JSON.parse(data);
          const sessions = json.sessions || [];
          const main = sessions.find(s => s.key === cfg.SESSION_KEY);
          if (!main) { resolve(); return; }

          const tokens = main.contextTokens || 0;
          const pct = tokens / CONTEXT_LIMIT;
          const state = loadState();
          if (!state.thresholds) state.thresholds = {};

          log(PROCESS, `Context: ${tokens.toLocaleString()} / ${CONTEXT_LIMIT.toLocaleString()} (${Math.round(pct * 100)}%)`);

          // Fire each threshold exactly once per session (resets when context drops back below 60%)
          for (const tier of THRESHOLDS) {
            if (pct >= tier.pct && !state.thresholds[tier.key]) {
              log(PROCESS, `${tier.emoji} Threshold ${tier.label} hit — writing backup handoff...`);

              // Write a backup handoff specifically labeled for this threshold
              const fs = require('fs');
              const path = require('path');
              const { callHaiku, getSessionHistory, formatMessages } = require('./lib');
              try {
                const history = await getSessionHistory(100);
                const formatted = formatMessages(history.messages || []);
                const handoff = await callHaiku(
                  `Write a CRITICAL session backup note at ${tier.label} context capacity.
This must be comprehensive — compaction may happen soon.
Include EVERYTHING: builds completed, Matt's exact words and instructions, pending tasks, active context, file paths, URLs, decisions made, where we left off.
Write in second person for Alo to read after compaction.`,
                  formatted
                );
                const ts = new Date().toISOString().slice(0, 16).replace('T', ' ');
                const content = `# Threshold Backup — ${tier.label} Context\n*Written at: ${ts} PST*\n\n${handoff.trim()}\n`;
                const backupPath = path.join('/Users/mattbender/.openclaw/workspace/memory/handoffs', `backup-${tier.key}-${new Date().toISOString().slice(0,10)}.md`);
                fs.writeFileSync(backupPath, content);
                // Also overwrite handoff-current
                fs.writeFileSync('/Users/mattbender/.openclaw/workspace/memory/handoff-current.md', content);
                log(PROCESS, `Backup written → ${path.basename(backupPath)}`);
              } catch(e) { log(PROCESS, `Backup write failed: ${e.message}`); }

              // Alert Matt
              await sendTelegramAlert(`${tier.emoji} *Alo context backup — ${tier.label}*\n\n${tier.message}\n\n_${tokens.toLocaleString()} / ${CONTEXT_LIMIT.toLocaleString()} tokens used_`);
              state.thresholds[tier.key] = true;
              saveState(state);
            }
          }

          // Reset all thresholds if context drops below 60% (new session / fresh start)
          if (pct < 0.60 && Object.values(state.thresholds || {}).some(Boolean)) {
            state.thresholds = {};
            saveState(state);
            log(PROCESS, 'Context dropped below 60% — threshold flags reset.');
          }

          resolve();
        } catch(e) { log(PROCESS, `context check error: ${e.message}`); resolve(); }
      });
    });
    req.on('error', e => { log(PROCESS, `context check error: ${e.message}`); resolve(); });
    req.setTimeout(5000, () => { req.destroy(); resolve(); });
  });
}

async function sendTelegramAlert(text) {
  return new Promise((resolve) => {
    try {
      const env = require('fs').readFileSync('/Users/mattbender/.openclaw/workspace/voice-server/.env', 'utf8');
      const token = (env.match(/TELEGRAM_BOT_TOKEN=(.+)/) || [])[1]?.trim();
      const chatId = (env.match(/TELEGRAM_CHAT_ID=(.+)/) || [])[1]?.trim();
      if (!token || !chatId) { resolve(); return; }

      const https = require('https');
      const body = JSON.stringify({ chat_id: chatId, text, parse_mode: 'Markdown' });
      const req = https.request({
        hostname: 'api.telegram.org',
        path: `/bot${token}/sendMessage`,
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
      }, res => { res.resume(); resolve(); });
      req.on('error', () => resolve());
      req.write(body);
      req.end();
    } catch(e) { resolve(); }
  });
}

// Run memory writer + correction detector + repeat detection + token check every 5 min
async function runFast() {
  try { await memoryWriter(); } catch(e) { log(PROCESS, `memory-writer error: ${e.message}`); }
  try { await correctionDetector(); } catch(e) { log(PROCESS, `correction-detector error: ${e.message}`); }
  try { await repeatMistakeDetector(); } catch(e) { log(PROCESS, `repeat-mistake-detector error: ${e.message}`); }
  try { await checkContextUsage(); } catch(e) { log(PROCESS, `context-check error: ${e.message}`); }
}

// Run handoff writer every 20 min
async function runMedium() {
  try { await handoffWriter(); } catch(e) { log(PROCESS, `handoff-writer error: ${e.message}`); }
}

// Run consolidator + learning effectiveness tracker every 2 hours
async function runSlow() {
  try { await consolidator(); } catch(e) { log(PROCESS, `consolidator error: ${e.message}`); }
  try { await learningEffectivenessTracker(); } catch(e) { log(PROCESS, `learning-effectiveness-tracker error: ${e.message}`); }
}

// Initial run on startup (staggered)
log(PROCESS, '🧠 Memory stack starting...');

setTimeout(async () => {
  await runFast();
  setInterval(runFast, 5 * 60 * 1000); // every 5 min
}, 5000);

setTimeout(async () => {
  await runMedium();
  setInterval(runMedium, 20 * 60 * 1000); // every 20 min
}, 30000);

setTimeout(async () => {
  await runSlow();
  setInterval(runSlow, 2 * 60 * 60 * 1000); // every 2 hours
}, 60000);

log(PROCESS, 'Scheduled: fast=5min (memory+corrections+repeat-detector+token-check), medium=20min (handoff), slow=2hr (consolidate+effectiveness)');
