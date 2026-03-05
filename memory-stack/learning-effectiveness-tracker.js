#!/usr/bin/env node
// memory-stack/learning-effectiveness-tracker.js
// Measures if corrections are being applied (corrections trending down = success)
// Runs every 2 hours in slow cycle

const fs = require('fs');
const path = require('path');
const { today, now, appendToDailyNotes, log } = require('./lib');
const cfg = require('./config');

const PROCESS = 'learning-effectiveness-tracker';
const CORRECTIONS_LOG = path.join(cfg.MEMORY_DIR, 'corrections.md');
const EFFECTIVENESS_LOG = path.join(cfg.MEMORY_DIR, 'learning-effectiveness.md');

function countCorrectionsInDate(date) {
  // Read daily notes for that date, count correction entries
  const file = path.join(cfg.MEMORY_DIR, `${date}.md`);
  if (!fs.existsSync(file)) return 0;
  const content = fs.readFileSync(file, 'utf8');
  return (content.match(/Correction Logged/gi) || []).length;
}

function getDateRange(daysBack) {
  const dates = [];
  for (let i = 0; i < daysBack; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    dates.push(d.toISOString().slice(0, 10));
  }
  return dates;
}

async function run() {
  if (!fs.existsSync(CORRECTIONS_LOG)) return;

  const totalLines = fs.readFileSync(CORRECTIONS_LOG, 'utf8').split('\n').length;

  // Measure corrections per week
  const thisWeek = getDateRange(7).reverse();
  const lastWeek = getDateRange(14).slice(0, 7).reverse();

  const thisWeekCount = thisWeek.reduce((sum, date) => sum + countCorrectionsInDate(date), 0);
  const lastWeekCount = lastWeek.reduce((sum, date) => sum + countCorrectionsInDate(date), 0);

  const trend = lastWeekCount > 0 ? Math.round(((thisWeekCount - lastWeekCount) / lastWeekCount) * 100) : 0;
  const direction = trend < -10 ? '📉 Improving' : trend > 10 ? '📈 Worsening' : '➡️ Stable';

  const report = `## Learning Effectiveness Report — ${today()} ${now()}

### Weekly Comparison
- This week: ${thisWeekCount} corrections
- Last week: ${lastWeekCount} corrections
- Trend: ${trend > 0 ? '+' : ''}${trend}% → ${direction}

### Key Metrics
- Total corrections logged: ${totalLines}
- Corrections/day (this week): ${Math.round(thisWeekCount / 7)}
- Status: ${trend < -20 ? '✅ Strong improvement' : trend < 0 ? '✅ Improving' : trend > 20 ? '⚠️ More mistakes' : '✅ Stable'}

### Interpretation
${trend < -15 ? 'Alo is learning well — corrections are decreasing week-over-week. Good momentum.' : 
  trend > 15 ? 'Alo is making repeated mistakes despite corrections. Enforcement needed.' :
  'Alo is maintaining baseline — neither improving nor worsening significantly.'}
`;

  // Write report
  if (!fs.existsSync(EFFECTIVENESS_LOG)) {
    fs.writeFileSync(EFFECTIVENESS_LOG, '# Learning Effectiveness Tracking\n\n');
  }
  fs.appendFileSync(EFFECTIVENESS_LOG, report + '\n---\n\n');

  log(PROCESS, `Learning effectiveness: ${direction} (${trend > 0 ? '+' : ''}${trend}%)`);
  appendToDailyNotes(`### Learning Effectiveness Check\n${direction} — This week ${thisWeekCount} corrections vs last week ${lastWeekCount}\n`);
}

if (require.main === module) {
  run().catch(e => log(PROCESS, `Fatal: ${e.message}`));
} else {
  module.exports = { run };
}
