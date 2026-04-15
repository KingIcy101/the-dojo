---
name: n8n
description: >
  n8n — workflow automation platform. Already running on Mac mini (PM2 id:13).
  Use for multi-step automations that connect apps without custom code.
  Connects GHL, Slack, Gmail, Notion, Stripe, webhooks — all visual, no-code.
---

# n8n — Workflow Automation

## Status
**Already running** on Mac mini — PM2 process id:13
```bash
# Check status
pm2 status n8n

# Access UI (local)
http://localhost:5678

# Default credentials: check voice-server/.env for N8N_BASIC_AUTH_USER/PASS
```

## What to Use n8n For
Instead of writing custom Node.js scripts for every integration, use n8n for:
- **Multi-step automations** (Webhook → Transform → GHL → Slack notify)
- **Scheduled data syncs** (Notion → Google Sheets every morning)
- **Event-driven workflows** (New Stripe payment → Create GHL contact → Send welcome email)
- **Error retry logic** — built in, no code needed

## Key Nodes We Use

### Webhook (trigger)
```
POST https://localhost:5678/webhook/your-path
→ triggers workflow with request body as data
```

### HTTP Request (call any API)
```
Method: POST
URL: https://rest.gohighlevel.com/v1/contacts/
Authentication: Header Auth (Bearer GHL_LOCATION_API_KEY)
Body: {{ $json.contact_data }}
```

### Slack (notify)
```
Channel: #orders-amz-walmart
Message: New order from {{ $json.contact.name }}: ${{ $json.amount }}
```

### Gmail / Email
```
To: {{ $json.email }}
Subject: Welcome to Halo Marketing
Body: [template]
```

### Notion
```
Database: [DB ID]
Operation: Create Item
Properties: { Name: {{ $json.name }}, Status: "Active" }
```

### Code Node (custom logic)
```js
// When no built-in node exists
const items = $input.all()
return items.map(item => ({
  json: {
    ...item.json,
    fullName: `${item.json.firstName} ${item.json.lastName}`,
    formattedAmount: `$${item.json.amount.toLocaleString()}`
  }
}))
```

### IF / Switch (branching)
```
Condition: {{ $json.amount }} >= 1950
True → Send to "Standard Plan" workflow
False → Send to "Exception Plan" workflow
```

### Wait (delays)
```
Wait 2 hours after no-show before retry call
Wait until next Monday 9am for weekly report
```

## Workflows to Build for Halo

### New Client Onboarding
```
Stripe payment received
→ Create GHL contact
→ Add to "Active Clients" pipeline
→ Send welcome email (Resend)
→ Notify Slack #team
→ Create Notion record
```

### Daily Appointment Reminders
```
Cron: every day at 9am
→ Fetch tomorrow's appointments from GHL
→ For each patient: trigger Bland.ai call
→ Log results to Notion
→ Send summary to Slack
```

### Lead Notification
```
GHL Webhook: new contact created
→ Check if from Facebook ad (tag check)
→ Post to Slack #new-leads
→ Assign to pipeline stage "New Lead"
→ Schedule follow-up call (Bland.ai) in 5 minutes
```

## API (Trigger from Code)
```js
// Execute an n8n workflow via webhook
await fetch('http://localhost:5678/webhook/onboard-client', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    clientId: 'pierce_123',
    email: 'pierce@example.com',
    plan: 'standard',
    amount: 1950
  })
})
```

## Skill Injection for Codex/Claude Code
```
n8n running at http://localhost:5678 (PM2 id:13).
Use for multi-step automations — don't write custom scripts for what n8n handles.
Trigger via webhook: POST http://localhost:5678/webhook/{path}.
Key integrations: GHL (HTTP Request node), Slack, Gmail, Notion, Stripe webhooks.
Build: new client onboarding, appointment reminders, lead notifications.
```


## Learned In Use

- **2026-03-16:** Timezone-aware cron expressions require explicit timezone configuration in trigger settings — PST/UTC offsets can cause scheduled workflows to fire hours late without America/New_York or equivalent timezone specification.
- **2026-03-16:** Reserve n8n for scheduled/recurring workflows only — use direct skill execution or other tools for one-off tasks to avoid over-engineering simple operations.
- **2026-03-18:** n8n cron expressions use UTC timezone — when scheduling for EST/EDT, convert to UTC offset (e.g., 7:30pm EDT = 23:30 UTC, cron `30 23 * * *`) rather than relying on system timezone settings.
- **2026-03-19:** Twitter/X automation cron timing must account for timezone conversion — 7:30 PM ET needs to be 8am PT (11am ET cron: `0 11 * * *`), and Claude voice prompts should match brand tone (direct, no fluff, entrepreneurial, no corporate speak).
- **2026-03-21:** When enabling bot-to-bot messaging in Discord integrations, explicitly set `allowBots: true` in the message filtering config — default filtering blocks agent-to-agent communication.

## Learned from Use (2026-03-22)
SKIP

The session logs contain no meaningful mentions of the n8n skill being used. The activity focuses on Vercel deployments, frontend rendering issues with Agent Lounge, Obsidian sync tasks, and build/review workflows. There are no n8n-specific actions, decisions, corrections, or patterns documented that would generate actionable lessons about using the n8n skill.

- **2026-03-22:** Context pruning and model separation in n8n agent configs requires explicit TTL/turn limits and NEW TASK prefix protocol to prevent rate limit conflicts and session context bleed across channel messages; group chat sessions still accumulate context from all channels despite fixes.

## Learned from Use (2026-03-29)
SKIP

The session logs provided show no usage of the "n8n" skill. The logs document a Client Portal v1 build cycle involving Clerk authentication, Vapi API integration, typography fixes, and QA audits—but there is no mention of n8n (the workflow automation platform) being deployed, configured, or used in any of the memory snapshots or corrections.

To extract lessons about n8n usage, I would need logs that show actual n8n workflow construction, execution, or integration within these agent sessions.


## Learned from Use (2026-04-05)
SKIP

The session logs provided contain no mentions of n8n being used, tested, or discussed. The logs focus on OpenClaw agents (Pixel, Forge, Judge, Core, etc.), Gemini API configuration, Discord integration, and the Halo Portal project. Without documented n8n skill usage or corrections related to n8n, there are no specific, actionable lessons to extract for this skill.
