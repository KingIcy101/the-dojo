# Firecrawl — Web Scraping & Crawling Skill

## What It Is
Firecrawl is a CLI tool and API for scraping, searching, crawling, and mapping the web. Results are written directly to the filesystem. Use it when you need to extract content from websites — competitor pages, lead enrichment, news scanning, documentation scraping.

## When to Use
- Scraping a website's content (products, pricing, contact info, blog posts)
- Crawling an entire site and mapping its structure
- Extracting clean markdown from messy web pages
- Web research that goes deeper than a single search result
- Lead enrichment (scrape a company's site for context before outreach)

## Install
```bash
npm install -g firecrawl-cli
```

Or via API directly:
```bash
pip install firecrawl-py
```

## API Key
Store in `.env` as `FIRECRAWL_API_KEY`. Get from https://firecrawl.dev

## Core Commands (CLI)
```bash
# Scrape a single URL → clean markdown
firecrawl scrape https://example.com

# Crawl entire site
firecrawl crawl https://example.com --limit 50

# Search the web (like Brave but returns full page content)
firecrawl search "AI receptionist software" --limit 5

# Map a site's URL structure
firecrawl map https://example.com
```

## API Usage (Node.js)
```js
const FirecrawlApp = require('@mendable/firecrawl-js');
const app = new FirecrawlApp({ apiKey: process.env.FIRECRAWL_API_KEY });

// Scrape single page
const result = await app.scrapeUrl('https://example.com', { formats: ['markdown'] });
console.log(result.markdown);

// Crawl site
const crawl = await app.crawlUrl('https://example.com', { limit: 10 });
```

## Use Cases for Halo/AI Agency
- Scrape competitor agency sites (pricing, services, positioning)
- Enrich prospect leads (scrape their website before a cold call)
- Pull practitioner website content for AI receptionist onboarding
- News scanning for n8n workflows (better than basic fetch)

## Notes
- Free tier: 500 credits/mo
- Handles JS-rendered pages (unlike basic fetch)
- Returns clean markdown — great for feeding into Claude
- Works well combined with Brave Search (search → then scrape the top results)


## Learned from Use (2026-03-22)
SKIP

The session logs provided contain no mentions of the "firecrawl" skill being used. The logs document deployment issues, UI building, and coordination between team members (Matt, Pixel, Forge, Alo), but do not reference firecrawl in any context. Therefore, there are no specific lessons about firecrawl usage to extract from these logs.
