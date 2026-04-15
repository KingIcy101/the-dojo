---
name: fireflies-webhook
description: Fireflies.ai webhook integration — transcripts hit voice-server, route to Dex for follow-up drafting
category: meta
---

# Fireflies Webhook — ZTA Pipeline

## When to Use
Fireflies detects meeting transcripts, webhook fires immediately after call ends. Triggers Dex to draft post-call follow-up email. Part of ZeroToAgent sales ops flow.

## Current Implementation (April 15, 2026)

**Webhook URL:** `https://supervisors-satellite-climb-designer.trycloudflare.com/webhook/fireflies`

**Flow:**
1. Fireflies records call → transcript ready
2. `POST /webhook/fireflies` hits voice-server
3. Parse meeting title, participants, duration, transcript, summary
4. Send Discord message to Dex channel (`1493317773970112743`) with:
   - Meeting title & duration
   - Participant names
   - Summary excerpt
   - Full transcript (first 1500 chars)
5. Dex reads message → loads matt-voice skill → drafts follow-up email → posts to #zta-sales-drafts
6. Matt reviews & approves → Dex sends

## Payload Format (what Fireflies sends)
```json
{
  "event": "transcript_ready",
  "data": {
    "meeting_id": "abc123",
    "transcript": "Full text of the meeting...",
    "title": "Call with Prospect XYZ",
    "summary": "High-level summary...",
    "participants": [
      { "name": "Matt Bender", "email": "matt@inthepast.ai" },
      { "name": "Prospect", "email": "prospect@company.com" }
    ],
    "duration_seconds": 1234,
    "created_at": "2026-04-15T14:00:00Z"
  }
}
```

## Implementation in server.js

Located at `/Users/mattbender/.openclaw/workspace/voice-server/server.js` around line 1880:

```js
app.post('/webhook/fireflies', async (req, res) => {
  res.sendStatus(200); // ack immediately
  const payload = req.body;
  if (payload.event !== 'transcript_ready') return;

  const data = payload.data || {};
  const { meeting_id, transcript, title, summary, participants, duration_seconds } = data;
  
  // Extract participant names
  const participantNames = participants?.map(p => p.name).filter(Boolean) || [];
  
  // Build Discord message for Dex
  const discordPayload = {
    content: `🔗 New Fireflies transcript ready\n\n**Meeting:** ${title || 'Untitled'}\n**Duration:** ${Math.round(duration_seconds / 60)} min\n**Participants:** ${participantNames.join(', ') || 'Unknown'}\n\n**Summary:**\n${summary || 'No summary'}\n\n---\n\n**Transcript:**\n${transcript.substring(0, 1500)}${transcript.length > 1500 ? '...' : ''}\n\nReady to draft follow-up email.`
  };
  
  // Send to Dex Discord
  const dexChannelId = process.env.DEX_CHANNEL_ID || '1493317773970112743';
  await axios.post(
    `https://discordapp.com/api/channels/${dexChannelId}/messages`,
    discordPayload,
    { headers: { 'Authorization': `Bot ${process.env.DISCORD_BOT_TOKEN}` } }
  );
});
```

## Fireflies Setup

1. Log into Fireflies.ai dashboard
2. Settings → Integrations → Webhooks
3. Add webhook URL: `https://supervisors-satellite-climb-designer.trycloudflare.com/webhook/fireflies`
4. Select "Transcript Ready" event
5. Optionally filter by meeting type or participant (leave blank for all meetings)
6. Save

## Env vars needed
- `DEX_CHANNEL_ID` — Discord channel ID where Dex sits (default: 1493317773970112743)
- `DISCORD_BOT_TOKEN` — Alo's Discord bot token (already in .env)
- `FIREFLIES_API_KEY` — For API calls (not strictly needed for webhook, but useful for future pulls)

## What happens next
- Dex receives transcript in Discord
- Loads matt-voice skill for proper tone
- Drafts 3-industry-use-case follow-up email (per Dex AGENTS.md rule)
- Posts to #zta-sales-drafts
- Matt reviews + "send" → email ships

## Testing
Once Fireflies webhook is set up, place a test call through Fireflies or have a real one recorded. Transcript should arrive within 30s, Dex should see it in Discord immediately.

## Future: Team-level routing
Phase 2 will route transcripts to Slack for broader team visibility and triage by agent. For now, Dex channel is the single source.

---
*Last updated: 2026-04-15*
