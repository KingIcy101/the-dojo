#!/usr/bin/env node
// memory-stack/repeat-mistake-detector.js
// Tracks repeated mistakes (3+ occurrences = critical pattern)
// Runs every 5 min during main memory-writer cycle

const fs = require('fs');
const path = require('path');
const { today, now, loadState, saveState, appendToDailyNotes, callHaiku, log } = require('./lib');
const cfg = require('./config');

const PROCESS = 'repeat-mistake-detector';
const CORRECTIONS_LOG = path.join(cfg.MEMORY_DIR, 'corrections.md');
const REPEAT_PATTERNS = path.join(cfg.MEMORY_DIR, 'repeat-patterns.md');

async function run() {
  if (!fs.existsSync(CORRECTIONS_LOG)) return;

  const corrections = fs.readFileSync(CORRECTIONS_LOG, 'utf8');
  const state = loadState();
  if (!state.repeatMistakes) state.repeatMistakes = {};

  // Extract all rules from corrections.md
  const rulePattern = /RULE:\s*([^—]+)—\s*([^\n]+)/gi;
  const ruleMatches = [...corrections.matchAll(rulePattern)];

  if (!ruleMatches.length) return;

  // Track frequency of each category
  const categoryCount = {};
  for (const match of ruleMatches) {
    const category = match[1].trim().toLowerCase();
    categoryCount[category] = (categoryCount[category] || 0) + 1;
  }

  // Flag critical patterns (3+ corrections in same category)
  const critical = Object.entries(categoryCount)
    .filter(([cat, count]) => count >= 3)
    .map(([cat, count]) => ({ category: cat, count, firstSeen: state.repeatMistakes[cat]?.firstSeen || today() }));

  for (const pattern of critical) {
    if (!state.repeatMistakes[pattern.category]) {
      // New critical pattern detected
      state.repeatMistakes[pattern.category] = {
        count: pattern.count,
        firstSeen: pattern.firstSeen,
        detectedAt: now(),
        escalated: false
      };

      const msg = `🚨 CRITICAL PATTERN: "${pattern.category}" corrected ${pattern.count}+ times. Alo is repeating this mistake. Needs direct intervention.`;
      log(PROCESS, msg);
      appendToDailyNotes(`### Critical Pattern Detected\n${msg}\n`);

      // Write to repeat-patterns.md for documentation
      if (!fs.existsSync(REPEAT_PATTERNS)) fs.writeFileSync(REPEAT_PATTERNS, '# Repeat Mistake Patterns\n\n');
      fs.appendFileSync(REPEAT_PATTERNS, `## ${pattern.category} (${pattern.count} occurrences)\n- First seen: ${pattern.firstSeen}\n- Detected: ${today()} ${now()}\n- Status: ⚠️ Critical pattern requiring Alo focus\n\n`);

      state.repeatMistakes[pattern.category].escalated = true;
    } else if (pattern.count > state.repeatMistakes[pattern.category].count) {
      // Pattern getting worse
      const oldCount = state.repeatMistakes[pattern.category].count;
      state.repeatMistakes[pattern.category].count = pattern.count;

      log(PROCESS, `📈 Repeat pattern worsening: "${pattern.category}" now ${pattern.count} times (was ${oldCount})`);
      appendToDailyNotes(`### Pattern Escalation\n"${pattern.category}" repeated mistake count increased: ${oldCount} → ${pattern.count}\n`);
    }
  }

  // Check if critical patterns are improving (corrections have stopped)
  for (const [category, data] of Object.entries(state.repeatMistakes)) {
    // Check if this category appears in recent corrections
    const recentLines = corrections.split('\n').slice(-50); // last 50 lines (recent)
    const stillAppearing = recentLines.some(line => line.toLowerCase().includes(category.toLowerCase()));

    if (!stillAppearing && data.escalated) {
      log(PROCESS, `✅ Pattern improving: "${category}" no longer appearing in recent corrections`);
      data.escalated = false;
      data.lastImproved = today();
    }
  }

  saveState(state);
}

if (require.main === module) {
  run().catch(e => log(PROCESS, `Fatal: ${e.message}`));
} else {
  module.exports = { run };
}
