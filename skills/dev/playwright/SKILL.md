---
name: playwright
description: >
  Playwright — browser automation and UI testing. Catch bugs before Matt sees them.
  Use for E2E testing of all apps, automated UI verification, screenshot comparison, and scraping.
  Also used internally for CDP browser control (port 18800).
---

# Playwright — Browser Automation & Testing

## What It Is
Playwright is Microsoft's browser automation library. Used for two things in our stack:
1. **Internal:** CDP browser control (`http://127.0.0.1:18800`) for Google Sheets, screenshots
2. **Testing:** E2E tests to verify UIs before shipping to Matt or clients

## Setup
```bash
npm install -D @playwright/test
npx playwright install  # installs chromium, firefox, webkit
```

## Our CDP Connection (Already Configured)
```js
// Connect to the running openclaw browser
const { chromium } = require('/Users/mattbender/.nvm/versions/node/v25.6.1/lib/node_modules/openclaw/node_modules/playwright')
const browser = await chromium.connectOverCDP('http://127.0.0.1:18800')
const context = browser.contexts()[0]
const page = (await context.pages())[0]
```

## E2E Test Pattern
```js
// tests/dashboard.spec.js
import { test, expect } from '@playwright/test'

test('dashboard loads with KPI cards', async ({ page }) => {
  await page.goto('http://localhost:7900')
  
  // Auth
  await page.fill('[data-testid="pin-input"]', '2146')
  await page.click('[data-testid="login-btn"]')
  
  // Check KPI cards exist
  await expect(page.locator('.kpi-card')).toHaveCount(4)
  
  // Check MRR displays
  await expect(page.locator('[data-testid="mrr-value"]')).toBeVisible()
  
  // Screenshot for review
  await page.screenshot({ path: 'screenshots/dashboard.png', fullPage: true })
})

test('calendar loads and shows events', async ({ page }) => {
  await page.goto('http://localhost:7900/calendar.html')
  await expect(page.locator('.calendar-grid')).toBeVisible()
  await expect(page.locator('.event')).toHaveCount.greaterThan(0)
})
```

## Run Tests
```bash
# Run all tests
npx playwright test

# Run specific file
npx playwright test tests/dashboard.spec.js

# With UI (visual debugging)
npx playwright test --ui

# Headed (see browser)
npx playwright test --headed

# Screenshot on failure
npx playwright test --screenshot=only-on-failure
```

## Visual Regression (Screenshot Comparison)
```js
test('dashboard looks correct', async ({ page }) => {
  await page.goto('http://localhost:7900')
  // Compare against stored baseline
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100,
  })
})

// Generate baseline: npx playwright test --update-snapshots
```

## Pre-Ship Checklist Automation
```js
// Run before every deploy
test.describe('Pre-ship checks', () => {
  test('no emojis in UI chrome', async ({ page }) => {
    await page.goto('http://localhost:7900')
    const titles = await page.locator('h1, h2, h3, .badge, .status').allTextContents()
    const emojiRegex = /[\u{1F300}-\u{1FFFF}]/u
    titles.forEach(t => expect(t).not.toMatch(emojiRegex))
  })

  test('all interactive elements have hover state', async ({ page }) => {
    // Check buttons have CSS transitions
    const buttons = await page.locator('button').all()
    for (const btn of buttons) {
      const transition = await btn.evaluate(el => getComputedStyle(el).transition)
      expect(transition).not.toBe('all 0s ease 0s') // has some transition
    }
  })

  test('mobile layout works at 375px', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 })
    await page.goto('http://localhost:7900')
    // Sidebar should be hidden
    const sidebar = page.locator('.sidebar')
    await expect(sidebar).toBeHidden()
  })
})
```

## Scraping Pattern (for lead work)
```js
// Already using in enrich_va_phones.js and scrape_state_v2.js
const browser = await chromium.launch({ headless: true })
const page = await browser.newPage()
await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 })
const data = await page.evaluate(() => {
  return document.querySelector('.phone')?.textContent?.trim()
})
await browser.close()
```

## playwright.config.js
```js
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: 1,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:7900',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'Mobile', use: { ...devices['iPhone 13'] } },
  ],
})
```

## Skill Injection for Codex/Claude Code
```
Use Playwright (@playwright/test) for E2E testing. CDP: http://127.0.0.1:18800.
Write tests for: page loads, KPI cards visible, mobile layout (375px), no emojis.
Screenshot on failure. Visual regression with toHaveScreenshot().
Run: npx playwright test before shipping any UI.
```


## Learned In Use

- **2026-03-13:** X.com (Twitter) session remains persistent on Mac mini browser — Playwright can post directly to @mattbendr without per-post authentication setup, only requires browser session login once.
- **2026-03-15:** Playwright skill was installed to Codex but no active usage logged this session — consider documenting web scraping context for future GitHub repo analysis workflows.
- **2026-03-21:** SVG rendering to PNG via Playwright works reliably for generating avatar images, but ensure output paths are explicitly defined and files are properly written before attempting Discord API uploads.

## Learned from Use (2026-03-22)
SKIP

The session logs contain no mentions of the "playwright" skill being used. The activity covers Vercel deployments, frontend rendering issues, UI builds, and Codex briefing processes, but does not reference or demonstrate the playwright skill in any meaningful way that would yield learned lessons about its application.

- **2026-03-25:** Browser profile must be 'openclaw' or CDP http://127.0.0.1:18800; never ask for manual tab attachment — use automation-first approach.

## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Font size violations cascade through QA rounds** — Typography issues (12px components) weren't caught until Judge's visual audit in round 2, then again in round 3 across different files (outcome-badge, calls-bar-chart). Grep verification after fixes prevented round 4 failures — establish a pre-Pixel typography baseline check to avoid repeat corrections.

- **Clerk theme prop overrides are fragile** — Dark theme settings in ClerkProvider bled into the sign-in component despite being a child. The `appearance` prop override fix worked, but theming must be tested in isolation before QA rounds, not discovered during final verification.

- **Empty states and error messages need security review alongside UI fixes** — Forge's fix pass (round 2) updated empty states, but Core later flagged error sanitization gaps. Coordinate with Core on what information is safe to display at component level during initial build, not after deployment.


## Learned from Use (2026-04-05)
SKIP

The session logs provided contain no mentions of the "playwright" skill being used, attempted, or corrected. The logs focus on agent configuration (Pixel, Gemini API), build deployment (Halo Portal), and system infrastructure (OpenClaw, Discord integration). There are no records of playwright-related work, corrections, or learning outcomes to extract.

To provide actionable lessons about playwright usage, I would need session logs that document actual playwright skill deployment.
