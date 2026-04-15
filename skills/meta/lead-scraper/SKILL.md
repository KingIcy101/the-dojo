# Lead Scraper Skill
*Use when: scraping leads for any niche, enriching existing lead lists with emails/phones, or pulling contact data from business websites.*

---

## Core Pattern

### 1. Google Maps Scraping (best for bulk leads by niche + city)

```js
const { chromium } = require('/Users/mattbender/.nvm/versions/node/v25.6.1/lib/node_modules/playwright');
const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
const context = browser.contexts()[0];
const page = (await context.pages())[0];

// Navigate to Google Maps search
await page.goto(`https://www.google.com/maps/search/${encodeURIComponent('chiropractor Virginia Beach VA')}`);
await sleep(3000);

// Scroll to load more results (do 3-5 times)
for (let s = 0; s < 3; s++) {
  await page.evaluate(() => {
    const panel = document.querySelector('[role="feed"]');
    if (panel) panel.scrollTop += 400;
  });
  await sleep(1000);
}

// Extract results
const results = await page.evaluate(() => {
  const items = document.querySelectorAll('[role="article"]');
  return Array.from(items).slice(0, 10).map(item => {
    const name = item.querySelector('[class*="fontHeadlineSmall"]')?.textContent?.trim() || '';
    const spans = item.querySelectorAll('[class*="fontBodyMedium"] span');
    const addr = spans[0]?.textContent?.trim() || '';
    const phone = item.querySelector('[data-tooltip="Copy phone number"]')?.parentElement?.textContent?.trim() || '';
    const website = item.querySelector('a[data-value="Website"]')?.href || '';
    return { name, addr, phone, website };
  });
});
```

**Tips:**
- Always skip chains (The Joint, franchise locations) — they won't buy
- Filter `state !== target state` to keep only local results
- Deduplicate by lowercased name across search batches
- Search 1 city at a time — broader searches miss local practices
- Rate: ~30 cities/hour safely

---

### 2. Website Email/Phone Enrichment

```js
async function scrapeWebsiteForContact(page, url) {
  if (!url.startsWith('http')) url = 'https://' + url;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 12000 });
  await sleep(1500);

  // Try contact page if no email found on homepage
  const contactLinks = await page.$$eval('a', links =>
    links.map(l => l.href).filter(h => h && (h.includes('contact') || h.includes('about')))
  );

  let text = await page.content();
  let emails = extractEmails(text);
  let phones = extractPhones(text);

  if (!emails.length && contactLinks.length) {
    await page.goto(contactLinks[0], { waitUntil: 'domcontentloaded', timeout: 10000 });
    await sleep(1000);
    text = await page.content();
    emails = extractEmails(text);
    if (!phones.length) phones = extractPhones(text);
  }

  return { email: emails[0] || '', phone: phones[0] || '' };
}

function extractEmails(text) {
  const matches = text.match(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g) || [];
  return [...new Set(matches.filter(e =>
    !e.includes('example') && !e.includes('domain') && !e.includes('email@') &&
    !e.includes('sentry') && !e.includes('wix') && !e.includes('wordpress') &&
    !e.includes('squarespace') && !e.includes('google') && !e.includes('facebook') &&
    !e.match(/\.(png|jpg|gif|svg|css|js)/)
  ))];
}

function extractPhones(text) {
  const matches = text.match(/\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}/g) || [];
  return [...new Set(matches)];
}
```

---

### 3. Write Results to Google Sheets (TSV clipboard paste)

```js
// Navigate to sheet tab
await page.goto(`https://docs.google.com/spreadsheets/d/${SHEET_ID}/edit?gid=${GID}`);
await sleep(5000);
await page.bringToFront();

// Clear existing data
await page.keyboard.press('Escape');
await page.keyboard.press('Control+Home');
await page.keyboard.press('Control+A');
await page.keyboard.press('Delete');
await sleep(1000);
await page.keyboard.press('Control+Home');
await sleep(500);

// Paste TSV
const tsv = rows.map(r => r.join('\t')).join('\n');
await page.evaluate(async (text) => { await navigator.clipboard.writeText(text); }, tsv);
await page.keyboard.press('Meta+V');
await sleep(4000);
```

---

### 4. Standard Lead Schema

Always use this column order for Halo Marketing leads:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Office Name | Website | Street Address | City | State | Zip Code | Email | Phone |

Sheet IDs:
- **Agency Practitioner Leads:** `1gFHuOrNO0qlemhb50KNwT8Xlq6M3HW8YTJZwnuge7X8`
  - Virginia chiros: `gid=1721774714`

---

### 5. Chains to Always Skip

```js
const SKIP_CHAINS = ['the joint', 'rxwellness', 'concentra', 'urgent care', 'hospital', 'health system'];
if (SKIP_CHAINS.some(c => name.toLowerCase().includes(c))) continue;
```

---

### 6. Rate Limiting & Reliability

```js
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// Between website scrapes: 800ms
// Between Maps searches: 1500ms
// After Maps page load: 3000ms
// After Sheets navigation: 5000ms
```

- Wrap each scrape in try/catch — sites go down, timeouts happen
- Run enrichment as background exec with `yieldMs` so it doesn't block
- Log progress `[i/total]` so you can track without polling constantly
- Save intermediate state to JSON file so you can resume if it crashes

---

### 7. Niche Search Templates

```
chiropractor [CITY] VA
dentist [CITY] VA
physical therapist [CITY] VA
dermatologist [CITY] VA
[niche] near [CITY] [STATE]
```

Batch searches: 1 niche × N cities. Start with cities 50K+ population, then work smaller.

---

### 8. Deduplication

```js
const existingNames = new Set(rows.map(r => r.name.toLowerCase()));
// Before adding any new lead:
if (existingNames.has(result.name.toLowerCase())) continue;
existingNames.add(result.name.toLowerCase());
```

---

## Full Script Reference

See: `/Users/mattbender/.openclaw/workspace/enrich_va_leads.js`
- Enriches existing leads (phases 1+2)
- Adds new leads from underserved cities (phase 3)
- Reads from + writes back to Google Sheets
- Skips chains, deduplicates, handles errors

## Notes
- Always use `profile="openclaw"` / CDP `http://127.0.0.1:18800`
- Google Maps selectors can change — test `[role="article"]` and `[class*="fontHeadlineSmall"]` if results come back empty
- bimmer-tech style: for niche-specific data, check competitor CDN files for lookup tables (see `tools/site-inspector/`)


## Learned from Use (2026-03-22)
SKIP

The session logs provided contain deployment troubleshooting, build reviews, and task coordination — but they do not document any actual use of the "lead-scraper" skill itself. There are no instances showing:

- How lead-scraper was invoked or what it extracted
- What corrections were made to its output
- What patterns or gotchas emerged from its performance
- How it succeeded or failed in practice

The correction logs address image reading and Codex briefing processes, neither of which relate to lead-scraper usage. Without documented examples of the skill being applied and corrected, no genuine lessons can be extracted.
