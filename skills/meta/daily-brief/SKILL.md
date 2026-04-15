---
name: daily-brief
description: Generate Matt's daily operating brief — what's happening today, what needs attention, what to prioritize. Use when: Atlas generates the morning/evening brief, or Matt asks "what's on my plate" / "what should I focus on today". Pulls from calendar, Trello sprint, Halo pipeline, Atlas pending tasks, and recent memory.
---

# Daily Brief Skill

Produce the brief immediately. No preamble. Lead with the most important thing.

---

## Brief Structure (always this order)

```markdown
# Daily Brief — [Day, Date] [Morning/Evening]

## Today's Priority (just one)
[The single most important thing. One sentence. Specific.]

## Must Do Today
1. [Specific task — who/what/deadline]
2. [Specific task]
3. [Specific task]
Max 5 items. If it's not urgent + important, cut it.

## Halo Update
- MRR: $[X] | Pipeline: [X active prospects]
- Hot: [Name] — [status/next step]
- Follow-up due: [Name] — [what/when]
- Blockers: [anything holding deals or delivery]

## Commerce Update (if relevant)
- Amazon MTD: ~$[X] | Walmart MTD: ~$[X]
- Pending orders: [X] | Flagged items: [if any]

## Calendar
- [Time]: [Event]
- [Time]: [Event]
[Only events today. Skip if empty.]

## Quick Wins Available
- [Something that takes <30 min and moves a needle]
- [Another quick win]

## Reminders
- [Upcoming deadline or time-sensitive item]
```

---

## Data Sources to Pull From

### Trello Sprint (Halo 1 Week Sprint)
```js
const TRELLO_KEY = '37a0f142cebf4afd33ba014b36727dfe';
const BOARD_ID = '6988d4473037a3745a13dd33';
const url = `https://api.trello.com/1/boards/${BOARD_ID}/cards?key=${TRELLO_KEY}&token=${TRELLO_TOKEN}`;
const cards = await fetch(url).then(r => r.json());
const inProgress = cards.filter(c => c.idList === '[IN_PROGRESS_LIST_ID]');
const blocked = cards.filter(c => c.labels?.some(l => l.name === 'Blocked'));
```

### Atlas Pending Executions
Read: `/Users/mattbender/.openclaw/workspace/agents/atlas/pending-executions.json`
Flag any `status: "awaiting-approval"` — Matt needs to review.

### Halo Pipeline
From MEMORY.md — current clients + pipeline status:
- Clients: Renee ($950), Jacek ($950)
- Hot: Pierce ($1,950 — signing), Alex (free trial, A2P pending), Carl (follow-up due)

### Sellerboard Data
Read: `/Users/mattbender/.openclaw/workspace/sellerboard-data.json`
Pull: Amazon MTD, Walmart MTD, top brands

### Calendar Events
Endpoint: `GET /api/calendar/events` on Mission Control (localhost:7900)
Filter to today's date only.

### HEARTBEAT.md
Read: `/Users/mattbender/.openclaw/workspace/HEARTBEAT.md`
Pull any blockers or scheduled follow-ups listed there.

---

## Brief Rules

- **One priority.** Not five. The hardest thing to do, or the highest leverage. Just one.
- **No filler.** If there's nothing to report on commerce, skip that section.
- **Specifics only.** "Follow up with Pierce" not "follow up with prospects."
- **Flag blockers louder.** If something is stuck, say it clearly: "BLOCKED: [what/why]"
- **Morning brief** = what to do today. **Evening brief** = what got done, what's tomorrow.
- Total length: under 300 words. Dense, not long.

---

## Evening Brief Variant

For 7pm Atlas brief:
```markdown
# Evening Brief — [Date]

## Today's Wins
- [What actually got done]

## Still Open
- [What didn't get done — move to tomorrow or cut]

## Tomorrow's Priority
[One thing. The most important.]

## Heads Up
- [Anything coming in next 24-48h that needs attention]
```

---

## Trigger Phrases
- "what's on my plate today"
- "morning brief"
- "daily brief"
- "what should I focus on"
- "catch me up"
- Atlas 7am / 7pm scheduled brief runs
- Any heartbeat that detects unread urgent items


## Learned from Use (2026-03-22)
## Learned from Use (2026-03-22)

- **Brief quality directly impacts execution — vagueness gets flagged.** When the daily-brief to Forge didn't emphasize visual requirements (avatars, labels, colors) as mandatory, Forge delivered skeleton-only UI. Matt's correction: briefs must translate high-level requests into exact, non-negotiable requirements upfront, not treat them as optional polish.

- **Auth/access issues block handoffs — always deploy to production when preview gates reviewers.** Three times preview URLs were gated by SSO, blocking Pixel's review. Decision made: use `--prod` flag to generate public URLs instead of wasting cycles on auth fixes. Brief should flag this for future deploys.

- **Mention handling breaks automation handoffs.** Forge used text `@Pixel` instead of real mentions in the brief, breaking the handoff. When writing briefs that flow to other agents, always use real mentions/IDs, never placeholder text.
