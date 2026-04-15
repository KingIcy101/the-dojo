---
name: fireflies-webhook
description: Process Fireflies meeting transcripts via webhook — store in Supabase, extract action items, enable on-demand memory query.
category: meta
---

# Fireflies Webhook Integration

## When to Use
Setting up automatic processing of sales or ops calls recorded by Fireflies. Enables meeting memory, action item extraction, and post-call automation triggers.

## Fireflies Payload Structure
```js
{
  title: "Call with Prospect Name",
  participants: [{ displayName: "Matt Bender", email: "matt@inthepast.ai" }],
  date: "2026-04-15T14:00:00Z",
  summary: {
    overview: "Discussion of CAO framework and pricing...",
    action_items: ["Send proposal by Friday", "Schedule follow-up for next week"],
    keywords: ["CAO", "pricing", "timeline"],
  },
  transcript: [
    { speaker: "Matt Bender", content: "So tell me about your current ops..." },
    { speaker: "Prospect", content: "We're running everything manually..." },
  ],
}
```

## Steps

1. Register webhook URL in Fireflies dashboard (Settings > Integrations > Webhooks)
2. Handle `POST /webhook/fireflies` in Express
3. Verify `X-Fireflies-Signature` header
4. Parse and store to Supabase `meetings` table
5. Extract action items → create tasks
6. Trigger downstream automations (Dex post-call flow, etc.)

## Key Patterns / Code

### Webhook Handler
```js
import crypto from 'crypto';

app.post('/webhook/fireflies', express.raw({ type: 'application/json' }), async (req, res) => {
  // Auth
  const sig = req.headers['x-fireflies-signature'];
  const expected = crypto
    .createHmac('sha256', process.env.FIREFLIES_WEBHOOK_SECRET)
    .update(req.body)
    .digest('hex');
  if (sig !== expected) return res.status(401).send('Invalid signature');

  res.sendStatus(200); // ack before processing

  const data = JSON.parse(req.body);
  await processMeeting(data);
});
```

### Store Meeting in Supabase
```js
async function processMeeting(data) {
  const { title, participants, date, summary, transcript } = data;

  // Store meeting
  const { data: meeting } = await supabase.from('meetings').insert({
    title,
    participants: JSON.stringify(participants),
    date,
    overview: summary?.overview,
    action_items: summary?.action_items || [],
    keywords: summary?.keywords || [],
    transcript: JSON.stringify(transcript),
  }).select().single();

  // Create action item tasks
  for (const item of (summary?.action_items || [])) {
    await supabase.from('tasks').insert({
      meeting_id: meeting.id,
      description: item,
      status: 'open',
    });
  }

  // Trigger post-call automation if sales call
  const isSalesCall = summary?.keywords?.includes('CAO') || summary?.keywords?.includes('pricing');
  if (isSalesCall) {
    await triggerDexFlow(data);
  }
}
```

### Supabase Schema
```sql
CREATE TABLE meetings (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT,
  participants JSONB,
  date TIMESTAMPTZ,
  overview TEXT,
  action_items TEXT[],
  keywords TEXT[],
  transcript JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE tasks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  meeting_id UUID REFERENCES meetings(id),
  description TEXT,
  status TEXT DEFAULT 'open',
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### On-Demand Memory Query
```js
// Query meetings by keyword or date
const { data: meetings } = await supabase
  .from('meetings')
  .select('title, date, overview, action_items')
  .contains('keywords', ['CAO'])
  .order('date', { ascending: false })
  .limit(5);
```

## Gotchas
- Use `express.raw()` for the webhook route — signature verification requires the raw body buffer
- Register the tunnel/prod URL in Fireflies dashboard before testing — Fireflies doesn't retry failed deliveries
- `X-Fireflies-Signature` format: plain hex HMAC-SHA256 (no `sha256=` prefix like GitHub)
- `summary` object may be null if Fireflies hasn't finished processing — check before accessing
- `transcript` array can be large (500+ entries for 1hr call) — store as JSONB, don't stringify for search
- Fireflies sends webhook on meeting end, not on manual upload — test with a real quick call
