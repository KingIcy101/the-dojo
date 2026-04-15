---
name: playwright-portal-audit
description: Use when running E2E visual or functional audits on client portals — Judge uses this before every deploy.
category: dev
---
# Playwright Portal Audit

## When to Use
Before every deploy of Mission Control or client portal. When Judge is asked to audit a UI. When Matt reports a visual bug that needs systematic verification.

## Steps
1. Connect via CDP to the running browser (port 18800)
2. Sign in as test user
3. Verify each section loads with real data
4. Screenshot any failures
5. Assert against pass criteria
6. Post results to Discord #agency-team-chat

## Key Patterns / Code

```ts
// scripts/audit-portal.ts
import { chromium } from 'playwright';

async function auditPortal() {
  // Connect to running OpenClaw browser via CDP
  const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  const results: { check: string; pass: boolean; note?: string }[] = [];

  try {
    await page.goto('https://portal.inthepast.ai/sign-in');
    await page.fill('[name=email]', process.env.TEST_EMAIL!);
    await page.fill('[name=password]', process.env.TEST_PASSWORD!);
    await page.click('[type=submit]');
    await page.waitForURL('**/dashboard', { timeout: 10000 });

    // Check: dashboard loads with real data
    const callCount = await page.textContent('[data-testid=total-calls]');
    results.push({ check: 'Dashboard loads', pass: !!callCount && callCount !== '0' });

    // Check: no empty states without a message
    const emptyStates = await page.$$('.empty-state');
    for (const el of emptyStates) {
      const text = await el.textContent();
      results.push({ check: 'Empty state has message', pass: !!text?.trim() });
    }

    // Check: no text below 13px
    const smallText = await page.evaluate(() => {
      const elements = document.querySelectorAll('*');
      const violations: string[] = [];
      elements.forEach(el => {
        const size = parseFloat(getComputedStyle(el).fontSize);
        if (size < 13 && el.textContent?.trim()) {
          violations.push(`${el.tagName}: ${size}px`);
        }
      });
      return violations;
    });
    results.push({ check: 'No text below 13px', pass: smallText.length === 0, note: smallText.join(', ') });

    // Check: all CTAs clickable (not disabled, not hidden)
    const ctas = await page.$$('button:not([disabled]), a[href]:not([aria-hidden])');
    results.push({ check: 'CTAs clickable', pass: ctas.length > 0 });

    // Screenshot pass
    await page.screenshot({ path: '/tmp/portal-audit.png', fullPage: true });

  } catch (err) {
    await page.screenshot({ path: '/tmp/portal-audit-FAIL.png', fullPage: true });
    results.push({ check: 'No uncaught errors', pass: false, note: String(err) });
  }

  const passed = results.filter(r => r.pass).length;
  const failed = results.filter(r => !r.pass);
  console.log(`Audit: ${passed}/${results.length} passed`);
  if (failed.length) console.log('FAILURES:', failed);

  return { passed, total: results.length, failures: failed };
}
```

```bash
# playwright_cli.sh — quick audit runner
#!/bin/bash
npx ts-node scripts/audit-portal.ts 2>&1 | tee /tmp/audit-$(date +%Y%m%d-%H%M).log
```

## Pass Criteria
- No empty states without a message
- No overflow or horizontal bleed (check right edge)
- No elements with font-size below 13px
- All CTAs are clickable and visible
- No console errors on load
- Page loads in under 3s

## Gotchas
- CDP port 18800 — if down, restart via mission-control or `openclaw gateway restart`
- `browser.contexts()[0]` — use existing context to inherit auth cookies
- Screenshots save to `/tmp/` — pull with `cat` or browser tool to inspect
- Run audit BEFORE `pm2 restart` on production — not after
- Playwright version must match the installed browsers — run `npx playwright install` if errors
- Never run in watch mode in prod — one-shot only
