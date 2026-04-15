---
name: heartbeat-system
description: OpenClaw heartbeat pattern — rotating checks, HEARTBEAT.md config, quiet hours, and when to reach out.
category: meta
---

# OpenClaw Heartbeat System

## When to Use
Background checks while Matt is away. Heartbeat = context-aware check; different from cron (exact timing).
Load HEARTBEAT.md at start of each heartbeat. Reply HEARTBEAT_OK if nothing needs attention.

## Steps
1. Read `memory/HEARTBEAT.md` — the checklist
2. Check `memory/heartbeat-state.json` for lastChecks timestamps
3. Run only the checks due (don't run all every beat)
4. Reply HEARTBEAT_OK if nothing urgent
5. Reach out only when: urgent email, event <2h away, interesting find, >8h silence

## Key Patterns / Code

### HEARTBEAT.md Format
```md
# Heartbeat Checklist

## Rotate Through (pick 2-3 per beat)
- [ ] Email: any urgent items? (check Gmail via Ember)
- [ ] Calendar: any events in next 2-4h?
- [ ] Todos: any overdue items in memory?
- [ ] 10DLC status: still IN_PROGRESS? (check Twilio)
- [ ] PM2: all processes online?

## Always Check
- [ ] heartbeat-state.json updated

## Quiet Hours
23:00-08:00 ET — no outreach unless critical (server down, urgent client)
```

### heartbeat-state.json
```json
{
  "lastChecks": {
    "email": "2026-04-15T14:30:00Z",
    "calendar": "2026-04-15T12:00:00Z",
    "todos": "2026-04-15T10:00:00Z",
    "pm2": "2026-04-15T14:30:00Z"
  },
  "lastOutreach": "2026-04-15T11:00:00Z",
  "sessionStatus": "idle"
}
```

### Rotation Logic
```js
const INTERVALS = {
  email: 30 * 60 * 1000,     // 30 min
  calendar: 60 * 60 * 1000,  // 1 hour
  todos: 4 * 60 * 60 * 1000, // 4 hours
  pm2: 30 * 60 * 1000,       // 30 min
};

function shouldCheck(key, lastChecks) {
  const last = new Date(lastChecks[key] || 0);
  return Date.now() - last > INTERVALS[key];
}
```

### Reach-Out Decision Tree
```
Is it quiet hours (23:00-08:00 ET)? → HEARTBEAT_OK (unless server down)
Was there outreach in last 30 min? → HEARTBEAT_OK
Found urgent email? → Reach out with summary
Event in <2h? → Reach out with reminder
Interesting find (new lead, etc.)? → Reach out
Nothing notable? → HEARTBEAT_OK
```

### Telegram Outreach Pattern
```bash
BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN voice-server/.env | cut -d= -f2)
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"   -d chat_id=8465598242   -d "text=Heartbeat: email from prospective client (Smile Dental). Subject: AI Receptionist Inquiry. Want me to draft a reply?"
```

## Heartbeat vs Cron
| Heartbeat | Cron |
|-----------|------|
| Context-aware (can reason) | Exact timing only |
| Batches multiple checks | Single task |
| Timing can drift ±minutes | Fires exactly on schedule |
| Needs session context | Works isolated |
| Use for: email/calendar checks | Use for: daily 8am reports |

## Gotchas
- Don't check everything every beat — rotate to avoid rate limits and noise
- `heartbeat-state.json` must be updated AFTER each check or rotation logic breaks
- If Matt is in an active session, heartbeat can inject via main + systemEvent
- Never reach out for minor things — only escalate what requires a decision
- >8h since last message = check in even if nothing new (human contact maintenance)