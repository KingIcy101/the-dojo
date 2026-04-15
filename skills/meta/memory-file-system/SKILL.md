---
name: memory-file-system
description: The full OpenClaw memory stack — daily logs, handoff, hot-context, corrections, MEMORY.md, QUICK-REF.
category: meta
---

# OpenClaw Memory File System

## When to Use
Every session. These files are Alo's continuity across fresh-context sessions. Read them at startup; write them throughout.

## The Stack

| File | Purpose | Who Writes | When |
|------|---------|------------|------|
| `memory/YYYY-MM-DD.md` | Raw session log | Every session | Append throughout |
| `memory/handoff-current.md` | Active task RIGHT NOW | Main session | Every task switch |
| `memory/hot-context.md` | Last 3 decisions + blockers | Main session | Auto-update |
| `memory/corrections.md` | Rule violations + fixes | Main session | Never delete |
| `MEMORY.md` | Curated long-term memory | Main session only | Key insights only |
| `QUICK-REF.md` | Never-ask-again facts | Main session | When fact is confirmed |

## Steps (Session Startup)
1. Read `memory/QUICK-REF.md` FIRST — fast facts
2. Read `SOUL.md`, `USER.md`
3. Read today + yesterday daily log (last 50 lines first)
4. Read `memory/handoff-current.md` (ignore if >2h old or says "HEARTBEAT_OK")
5. Read `memory/corrections.md` — non-negotiable
6. Read `memory/hot-context.md`
7. Main session only: read `MEMORY.md`

## Key Patterns / Code

### Daily Log Entry (memory/YYYY-MM-DD.md)
```md
## 14:32 — Built Stripe webhook handler
- Added checkout.session.completed → provisioned org access
- Stored stripe_customer_id in supabase organizations table
- Tested with stripe CLI: events firing correctly
- Next: wire up customer portal link in settings page
```

### Handoff Format (handoff-current.md)
```md
# Handoff — [timestamp]
## Active Task
Building ITP client portal — Stripe billing page

## Status
- Webhook handler done ✓
- Customer portal link done ✓
- BLOCKING: Supabase RLS policy needs org_id claim in JWT

## Next Step
Add org_id to Clerk JWT template (clerk-organizations-saas skill)

## Context Files
- /Users/mattbender/.openclaw/workspace/projects/itp-portal/
```

### Hot Context Format (hot-context.md)
```md
# Hot Context — [timestamp]
## Last 3 Decisions
1. Using Clerk Organizations (not custom auth) for ITP portal tenant isolation
2. Supabase RLS via org_id JWT claim — not application-level filtering
3. Resend for email (not SendGrid) — better DX, already have key

## Active Blockers
- 10DLC still IN_PROGRESS — no SMS until VERIFIED
```

### Corrections Entry
```md
## [2026-04-15] — Sent partial feature list instead of complete list
Rule violated: "Anything else?" = give everything in one shot
Fix: always check if the answer is the complete answer before sending
Never delete this entry.
```

### QUICK-REF Pattern
```md
## Credentials & Keys
- RESEND_API_KEY: re_UqojquC9_... (voice-server/.env)
- TWILIO_10DLC_STATUS: IN_PROGRESS (update when VERIFIED)
- ITP Stripe: live mode keys in voice-server/.env

## Never Ask Again
- Cal link: cal.com/matt-bender-ai/30min
- Telegram chat_id: 8465598242
- ITP setup fee: $5,000 all tiers
```

## Gotchas
- Write `handoff-current.md` BEFORE `/new` — not after (too late)
- `MEMORY.md` is main session only — never load in Discord/group chats (security)
- Daily log = append only — never rewrite or summarize old entries
- `corrections.md` = never delete entries — accumulates forever as rule history
- If handoff contradicts daily log tail → trust the daily log