---
name: data-analysis
description: Analyze CSV, JSON, or spreadsheet data. Drop a file and get instant exploration — column summaries, anomalies, trends, plain-English insights. Use when: Matt shares a data file, asks about numbers, wants to understand leads/orders/revenue/performance data. Works on Sellerboard exports, lead sheets, order CSVs, Notion exports, Google Sheet downloads.
---

# Data Analysis Skill

When triggered, load this skill and follow the pattern below. Do NOT ask "what would you like to know?" — just run the full exploration and surface what matters.

---

## Step 1 — Load & Profile the Data

```js
const fs = require('fs');
const path = require('path');

// Support CSV, JSON, TSV
function loadFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const raw = fs.readFileSync(filePath, 'utf8');
  
  if (ext === '.json') return JSON.parse(raw);
  
  // CSV/TSV parser
  const delim = ext === '.tsv' ? '\t' : ',';
  const lines = raw.trim().split('\n');
  const headers = lines[0].split(delim).map(h => h.replace(/"/g, '').trim());
  return lines.slice(1).map(line => {
    const vals = line.split(delim).map(v => v.replace(/"/g, '').trim());
    return Object.fromEntries(headers.map((h, i) => [h, vals[i] || '']));
  });
}

function profileData(rows) {
  if (!rows.length) return {};
  const cols = Object.keys(rows[0]);
  const profile = {};
  
  for (const col of cols) {
    const vals = rows.map(r => r[col]).filter(v => v !== '' && v != null);
    const nums = vals.map(Number).filter(v => !isNaN(v));
    
    profile[col] = {
      total: rows.length,
      filled: vals.length,
      empty: rows.length - vals.length,
      unique: new Set(vals).size,
      isNumeric: nums.length > vals.length * 0.8,
    };
    
    if (profile[col].isNumeric && nums.length) {
      const sorted = [...nums].sort((a, b) => a - b);
      profile[col].min = sorted[0];
      profile[col].max = sorted[sorted.length - 1];
      profile[col].avg = nums.reduce((a, b) => a + b, 0) / nums.length;
      profile[col].sum = nums.reduce((a, b) => a + b, 0);
      profile[col].median = sorted[Math.floor(sorted.length / 2)];
    } else {
      // Top values by frequency
      const freq = {};
      vals.forEach(v => freq[v] = (freq[v] || 0) + 1);
      profile[col].topValues = Object.entries(freq)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([val, count]) => ({ val, count }));
    }
  }
  return profile;
}
```

---

## Step 2 — Flag Anomalies

```js
function findAnomalies(rows, profile) {
  const flags = [];
  
  for (const [col, stats] of Object.entries(profile)) {
    // Missing data flag
    if (stats.empty > rows.length * 0.2) {
      flags.push(`"${col}" is ${Math.round(stats.empty/rows.length*100)}% empty — ${stats.empty} rows missing`);
    }
    
    if (stats.isNumeric) {
      // Outlier detection (simple IQR)
      const nums = rows.map(r => Number(r[col])).filter(v => !isNaN(v)).sort((a,b) => a-b);
      const q1 = nums[Math.floor(nums.length * 0.25)];
      const q3 = nums[Math.floor(nums.length * 0.75)];
      const iqr = q3 - q1;
      const outliers = nums.filter(v => v < q1 - 1.5*iqr || v > q3 + 1.5*iqr);
      if (outliers.length) {
        flags.push(`"${col}" has ${outliers.length} outlier(s) — min: ${stats.min}, max: ${stats.max}, avg: ${stats.avg.toFixed(2)}`);
      }
      
      // Zero/negative where unexpected
      const zeros = rows.filter(r => Number(r[col]) === 0).length;
      if (zeros > rows.length * 0.1) {
        flags.push(`"${col}" has ${zeros} zero values (${Math.round(zeros/rows.length*100)}%)`);
      }
    }
  }
  return flags;
}
```

---

## Step 3 — Plain English Summary Output

Always produce this structure when analyzing data:

```
## Data Summary: [filename]
**[X] rows × [Y] columns**

### Key Numbers
- [Most important metric]: [value]
- [Second metric]: [value]
- [Third metric]: [value]

### What Stands Out
- [Anomaly or insight 1]
- [Anomaly or insight 2]
- [Trend or pattern]

### Missing / Incomplete
- [Column] — X% empty
- [Any data quality issues]

### Actionable Takeaways
1. [What to do based on this data]
2. [Second action]
3. [Third action]
```

---

## Common Analysis Patterns by Data Type

### Lead Sheets (VA leads, chiro prospects)
Focus on: contact completeness (email % + phone %), city/state distribution, website presence rate
Key question: "Of these leads, how many are actually contactable right now?"

```js
const contactable = rows.filter(r => (r.email || r.Email) && (r.phone || r.Phone)).length;
const emailOnly  = rows.filter(r => (r.email || r.Email) && !(r.phone || r.Phone)).length;
const phoneOnly  = rows.filter(r => !(r.email || r.Email) && (r.phone || r.Phone)).length;
const dead       = rows.filter(r => !(r.email || r.Email) && !(r.phone || r.Phone)).length;
console.log(`Fully contactable: ${contactable} | Email only: ${emailOnly} | Phone only: ${phoneOnly} | Dead: ${dead}`);
```

### Order / Revenue Data (Sellerboard, Amazon, Walmart)
Focus on: total spend, top brands by revenue, COGS vs revenue margin, month-over-month trend

```js
// Group by brand/supplier
const byBrand = {};
rows.forEach(r => {
  const brand = r.brand || r.Brand || r['Item Name'] || 'Unknown';
  if (!byBrand[brand]) byBrand[brand] = { revenue: 0, orders: 0, cost: 0 };
  byBrand[brand].revenue += Number(r.revenue || r.Revenue || 0);
  byBrand[brand].orders  += 1;
  byBrand[brand].cost    += Number(r.cost || r['Buy Cost'] || 0);
});
const ranked = Object.entries(byBrand).sort((a,b) => b[1].revenue - a[1].revenue);
console.log('Top brands:', ranked.slice(0,5).map(([b,s]) => `${b}: $${s.revenue.toFixed(0)}`).join(' | '));
```

### Client / CRM Data
Focus on: MRR per client, time since last contact, churn risk signals (no recent activity)

### Google Sheets (our stack)
Read via fetch with credentials (must run in CDP browser context):
```js
const csv = await page.evaluate(async (url) => {
  const r = await fetch(url, { credentials: 'include' });
  return r.text();
}, `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent(tabName)}`);
```

---

## Output Rules

- **Never just echo back the data** — always interpret it
- Lead with the number that matters most, not column names
- Flag problems before opportunities
- End with 2-3 specific actions Matt can take
- If data is about leads: always compute contactability rate
- If data is about revenue: always compute top 3 performers and worst 3
- If data is about clients: flag any with no activity in 14+ days
- Keep summary under 300 words — dense, not verbose

---

## Trigger Phrases
- "analyze this CSV/file/data"
- "what does this spreadsheet show"
- "how many leads do we have"
- "look at these numbers"
- "check the [sheet/export/data]"
- Any time Matt shares a `.csv`, `.json`, `.tsv`, or `.xlsx` file path


## Learned from Use (2026-03-22)
SKIP

The session logs contain no instances where the "data-analysis" skill was actually used or needed. The logs document deployment troubleshooting, build issues, UI implementation problems, and task coordination—but none of these involved data analysis, metrics review, pattern detection, or analytical decision-making that would generate lessons about using that skill.

The corrections logged (image reading, codex briefing process) are unrelated to data-analysis. To extract genuine lessons about data-analysis skill usage, there would need to be documented instances where the skill was applied, succeeded, failed, or was corrected by the user.
