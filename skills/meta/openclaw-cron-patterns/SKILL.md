---
name: openclaw-cron-patterns
description: Configure OpenClaw cron and scheduled jobs — isolated vs main session, delivery modes, timing patterns.
category: meta
---

# OpenClaw Cron Patterns

## When to Use
Any time you need to schedule a task: daily reports, appointment reminders, heartbeat checks, one-shot at a specific time.
Use cron for exact timing; use heartbeat for context-aware batching.

## Steps
1. Choose sessionTarget: isolated (fresh context) or main (injects into live session)
2. Choose delivery: none (silent run), announce (Telegram/Discord), webhook (POST to URL)
3. Choose schedule kind: at (one-shot), every (interval), cron (expression)
4. Always include task context in isolated job messages — they have zero memory
5. Set timeoutSeconds on all agentTurn jobs to prevent runaway

## Key Patterns / Code

### Schedule Kinds
```js
// One-shot at specific time
{ kind: 'at', value: '2026-04-20T14:00:00-04:00' }

// Interval (every N minutes/hours)
{ kind: 'every', value: '30m' }   // 30 minutes
{ kind: 'every', value: '6h' }    // 6 hours

// Cron expression
{ kind: 'cron', value: '0 9 * * 1-5' }  // 9am weekdays
```

### sessionTarget Options
```js
// Isolated — fresh context, separate model instance
{
  sessionTarget: { type: 'isolated' },
  agentTurn: {
    message: 'Read SUBAGENT_BRIEF.md at /Users/mattbender/.openclaw/workspace/SUBAGENT_BRIEF.md. Then: [FULL TASK CONTEXT HERE]. Do not ask for clarification — complete the task.',
    timeoutSeconds: 120,
    delivery: { type: 'announce', channel: 'telegram', chatId: '8465598242' }
  }
}

// Main session — injects as systemEvent (only works when session is active)
{
  sessionTarget: { type: 'main' },
  systemEvent: {
    message: '[HEARTBEAT] Check email for urgent items',
  }
}
```

### Silent Background Job (no delivery)
```js
{
  schedule: { kind: 'every', value: '1h' },
  sessionTarget: { type: 'isolated' },
  agentTurn: {
    message: 'Update /tmp/status.json with current PM2 process health',
    timeoutSeconds: 60,
    delivery: { type: 'none' }
  }
}
```

### Webhook Delivery
```js
{
  delivery: {
    type: 'webhook',
    url: 'https://n8n.inthepast.ai/webhook/daily-report',
    method: 'POST'
  }
}
```

## Heartbeat vs Cron Decision
| Use Case | Use |
|----------|-----|
| Email check, calendar, rotating checks | Heartbeat |
| Daily report at 8am sharp | Cron |
| One-time reminder | at |
| Recurring fixed interval | every |
| Matt is in a live session | main + systemEvent |
| Background task, no live session needed | isolated + agentTurn |

## Gotchas
- Isolated jobs wake up with zero context — put EVERYTHING they need in the message
- Main + systemEvent only fires if main session is active — use isolated for reliability
- timeoutSeconds defaults to none — always set it to prevent zombie jobs
- `every` intervals reset on gateway restart — prefer `cron` for daily tasks
- Cron expressions: seconds NOT supported, starts with minute (5 fields, not 6)