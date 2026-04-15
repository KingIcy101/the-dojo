---
name: content-draft
description: Draft any content piece — Twitter threads, LinkedIn posts, cold emails, ad copy, landing page copy, SMS sequences, YouTube scripts, case studies. Use when Matt or Quinn needs to produce written content. Always writes in Matt's voice. Never generic. Never corporate.
---

# Content Draft Skill

When triggered, produce the draft immediately. Don't ask for a brief — infer from context. If critical info is missing (who it's for, what platform), ask ONE question max.

---

## Matt's Voice (always apply this)

Load `agents/content/twitter-voice-guide.md` if it exists. If not, apply these rules:

- **Short sentences.** No fluff.
- **Building-in-public tone** — honest, specific, numbers when you have them
- **No corporate speak.** No "leverage," "synergy," "streamline," "unlock potential"
- **No hashtags** on Twitter unless it's a trend post
- **No em-dashes** (—) in tweets — use a period or line break
- **Open with a story or a specific number**, not a question
- **Stacked short lines** > paragraphs on Twitter/LinkedIn
- **Real > polished** — sounds like a 24-year-old founder, not a copywriter

---

## Platform-Specific Patterns

### Twitter/X Thread
```
[Hook line — specific number or story open]

[Line break]

[Point 1 — concrete, short]

[Point 2]

[Point 3]

[Point 4]

[CTA or close — no "follow me for more"]
```
- Max 280 chars per tweet
- 4-8 tweets in a thread
- First tweet = the hook. If it's weak, rewrite it.
- Pull from win-log.md for real results to reference

### Cold Email (Halo Marketing)
```
Subject: [city] [specialty] practices

Hey [First Name],

[1-line observation about their practice or market — specific, not generic]

We help [specialty] practices in [region] get [X] new patients/month through [Facebook/Google] ads + an automated follow-up system.

[1 social proof line — client result or specific number]

Worth a 15-min call this week?

[Name]
```
- Under 100 words in body
- Subject line: no clickbait, no ALL CAPS
- One CTA only

### Facebook Ad Copy (Halo clients)
```
HEADLINE: [Pain or desire in 6 words or less]

BODY:
[Pain point they recognize — 1 sentence]
[What we do — 1 sentence]
[Proof — 1 sentence or number]
[CTA — clear, low friction]

CTA BUTTON: Learn More / Book Now / Get Started
```

### Google Ad Copy
```
Headline 1: [Keyword-rich — 30 chars max]
Headline 2: [Benefit — 30 chars max]
Headline 3: [CTA or trust signal — 30 chars max]
Description: [2 sentences, 90 chars each, include keyword + benefit + CTA]
```

### SMS Sequence (appointment reminders)
```
Day 0 (confirmation): "Hi [Name], you're confirmed for [date/time] with Dr. [X]. Reply STOP to opt out."
Day -2 (reminder): "Reminder: your appt with Dr. [X] is in 2 days — [date] at [time]. Need to reschedule? Reply here."
Day -1 (reminder): "See you tomorrow at [time], [Name]. Dr. [X]'s office is at [address]. Questions? Reply here."
No-show follow-up: "We missed you today, [Name]. Life gets busy — want to rebook? [link]"
```

### LinkedIn Post
- Longer than Twitter, still punchy
- Story open (what happened, what I learned)
- 3-5 lessons or observations
- No carousel hooks ("Swipe to see...")
- End with a genuine question or statement, not "What do you think?"

### Case Study
```
## [Client Name or Type] — [Result in headline]

**The situation:** [2 sentences on where they were before]

**What we did:** [3 bullets — specific tactics]

**The result:** [Number. Specific. Timeframe.]

**What made the difference:** [1 insight]
```

---

## Content Calendar Integration

If Matt says "what should I post this week" or "give me a week of content":

Pull from:
1. `memory/win-log.md` — recent wins = content gold
2. `agents/content/twitter-voice-guide.md` — voice rules
3. Any recent Halo client results
4. Current Halo focus (new patients, agency positioning, building-in-public)

Produce 5 posts (Mon-Fri), one per day, varied format (thread / single tweet / LinkedIn / story post).

---

## Output Rules

- Always write the full draft — never "here's a template, fill in X"
- If writing ad copy: write 2-3 variants for A/B testing
- If writing a thread: write every tweet, not just the hook
- Flag if any claim needs a real number to back it up: `[NEED: X stat here]`
- Never use stock phrases: "game-changing," "revolutionary," "unlock your potential," "take your business to the next level"

---

## Trigger Phrases
- "write a tweet/thread/post about..."
- "draft ad copy for [client]"
- "write a cold email for [niche/city]"
- "give me content for this week"
- Quinn receives a writing task
- Any request involving copy, ads, emails, social posts


## Learned In Use

- **2026-03-20:** Correction logging alone (written rules in corrections.md) does not change agent behavior — enforcement requires code-level blocking via hooks, cron jobs, or pre-task checkers that run at decision time, not just at startup.

## Learned from Use (2026-03-22)
SKIP

The session logs provided show deployment, debugging, and project management activities, but contain no evidence of the "content-draft" skill being used. The logs mention builds, deployments, UI issues, and corrections to processes like Codex briefing and image reading—but no instances where content-draft was applied, tested, corrected, or refined.

To extract meaningful lessons about content-draft usage, I would need session logs that actually show this skill being invoked, producing output that was reviewed, and corrections being applied to how it was used.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Pipeline sequencing prevents rework**: Deploying before Judge audit (Round 1) caused 2 typography corrections that could have been caught earlier. Waiting for full Pixel → Forge → Judge cycle eliminated violations in Round 3–4. Drafting code without gating to review creates false "done" states.

- **Font size violations are systematic, not one-off**: Multiple components (Agent ID label, chart tooltip, outcome-badge, calls-bar-chart) all violated 12px minimum at different times. Adding a lint/grep check (13px minimum enforced across codebase) prevented regression rather than fixing per-instance. Future drafts should include automated constraints.

- **Clerk theming context bleeds across components**: Dark theme override in ClerkProvider leaked into sign-in UI until `appearance` prop explicitly reset it. When drafting auth UI, isolation via prop overrides must be written into the initial component, not discovered as a correction.

- **2026-04-01:** When optimizing social media bios for positioning, avoid passive language like '& then became' — use active, forward-looking statements like 'Now I build' to convey current expertise rather than past transitions.