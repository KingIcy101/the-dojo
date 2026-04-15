---
name: agent-discord-pipeline
description: How OpenClaw agents communicate via Discord webhooks — posting, mentions, pipeline coordination, escalations.
category: meta
---

# Agent Discord Pipeline

## When to Use
Any inter-agent communication. Pixel specs → #pixel, Forge builds → tags Judge, Judge verdicts → #dev-team-chat.
All agent-to-agent handoffs happen via Discord. Escalations always go to Matt's channel.

## Steps
1. Each agent posts to its own dedicated channel via webhook
2. Use `{content, username}` POST to DISCORD_WEBHOOK_URL
3. Mentions: numeric user ID only (`<@USER_ID>`)
4. No markdown tables — bullet lists only
5. One message per handoff — no spam

## Key Patterns / Code

### Post via Webhook
```js
async function discordPost(webhookUrl, content, username = 'Alo') {
  await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, username }),
  });
}

// Usage
await discordPost(process.env.DISCORD_FORGE_WEBHOOK, '✅ ITP Portal v1.2 built. Tagging Judge for audit.', 'Forge');
```

### Mention Format
```js
// ✅ Correct — numeric ID
`<@8465598242> — build complete, ready for review`

// ❌ Wrong — username mention doesn't work in webhooks
`@mattbendr — build complete`

// Agent mention IDs (from .env)
// Matt: 8465598242 (Telegram, not Discord — use DISCORD_MATT_ID for Discord)
```

### Pipeline Coordination
```
Pixel (design) → posts spec to #pixel channel
  ↓
Forge (build) reads spec → builds → posts to #forge → tags Judge
  ↓
Judge (audit) screenshots all states → scores → posts ONE verdict to #dev-team-chat
  ↓
  SHIP → Core reads verdict → triggers production deploy
  REJECT → Forge reads IMPROVEMENTS → fixes in one pass → tags Judge again
```

### Channel Webhook Env Vars
```bash
DISCORD_WEBHOOK_ALO=https://discord.com/api/webhooks/xxx/yyy
DISCORD_WEBHOOK_FORGE=https://discord.com/api/webhooks/aaa/bbb
DISCORD_WEBHOOK_PIXEL=https://discord.com/api/webhooks/ccc/ddd
DISCORD_WEBHOOK_JUDGE=https://discord.com/api/webhooks/eee/fff
DISCORD_WEBHOOK_DEVTEAM=https://discord.com/api/webhooks/ggg/hhh
```

### Escalation Channel
```js
// ALL escalations → channel 1487259107407826964
const ESCALATION_CHANNEL_ID = '1487259107407826964';

// Via webhook (if you have it) or via bot token
await discordPost(process.env.DISCORD_WEBHOOK_ESCALATION,
  '⚠️ ESCALATION: Voice server down — PM2 process crashed at 14:32. Last restart failed. Manual intervention needed.',
  'Core'
);
```

### No Tables Rule
```
// ❌ Wrong — tables don't render well in Discord mobile
| Page | Score |
|------|-------|
| /dashboard | 0.95 |

// ✅ Correct — bullet list
- /dashboard: 0.95
- /settings: 0.88
- /mobile: 0.92
```

### Multi-line Message
```js
const lines = [
  '✅ Build complete — ITP Portal v1.2',
  '- Stripe billing: done',
  '- Clerk org creation: done',
  '- Supabase RLS: done',
  '',
  'Tagging <@JUDGE_DISCORD_ID> for audit.',
];
await discordPost(forgeWebhook, lines.join('\n'), 'Forge');
```

## Gotchas
- Webhook `username` field overrides the bot name in chat — use agent names (Forge, Judge, Pixel)
- No attachments via simple webhook — use bot token + Discord API for file uploads
- Webhook rate limit: 5 requests/2 seconds per webhook — don't spam
- Embeds require `embeds` array in body, not `content` — use only for structured verdicts
- Discord mobile: test readability without tables, with bullet lists only