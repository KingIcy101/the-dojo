---
name: dex-post-call-automation
description: Post-call sales automation — Fireflies transcript to personalized follow-up email draft in Discord, never sends without approval.
category: meta
---

# Dex — Post-Call Sales Automation

## When to Use
Building or modifying Dex's post-call workflow that turns a Fireflies meeting transcript into a personalized CAO follow-up email draft ready for Matt's approval.

## Flow

```
Fireflies webhook (meeting end)
  -> Extract prospect industry
    -> Generate 3 industry-specific use cases
      -> Draft personalized CAO follow-up email
        -> Post draft to Discord #dex-drafts
          -> Wait for Matt's "send" command
            -> Send via Resend from hello@inthepast.ai
```

**NEVER auto-send. Always requires explicit Matt approval.**

## Key Patterns / Code

### Webhook Handler (Express)
```js
app.post('/webhook/fireflies', async (req, res) => {
  res.sendStatus(200); // ack immediately

  const { title, participants, summary, transcript } = req.body;
  const overview = summary?.overview || '';
  const actionItems = summary?.action_items || [];

  // Extract prospect info
  const prospectName = participants.find(p => p.email !== 'matt@inthepast.ai')?.displayName;
  const prospectEmail = participants.find(p => p.email !== 'matt@inthepast.ai')?.email;

  // Identify industry from transcript
  const industry = await extractIndustry(overview + transcript.map(t => t.content).join(' '));

  // Generate use cases
  const useCases = await generateUseCases(industry);

  // Draft email
  const emailDraft = await draftFollowUp({ prospectName, industry, useCases, overview });

  // Post to Discord for approval
  await postDraftForApproval({ prospectName, prospectEmail, emailDraft });
});
```

### Industry Extraction (LLM call)
```js
async function extractIndustry(text) {
  // Think: what does this person do ALL DAY, not a static category map
  const prompt = `Based on this conversation, what industry/business type is the prospect in?
  Think about their day-to-day operations, pain points, and vocabulary.
  Respond with: industry name | key daily activities | main pain points
  Text: ${text.slice(0, 2000)}`;

  const response = await anthropic.messages.create({
    model: 'claude-3-5-haiku-20241022',
    max_tokens: 200,
    messages: [{ role: 'user', content: prompt }],
  });
  return response.content[0].text;
}
```

### Discord Draft Posting
```js
async function postDraftForApproval({ prospectName, prospectEmail, emailDraft }) {
  const message = `**NEW FOLLOW-UP DRAFT** — ${prospectName} (${prospectEmail})\n\n` +
    `\`\`\`\n${emailDraft}\n\`\`\`\n\n` +
    `Reply **send** to send this email.`;

  await fetch(process.env.DISCORD_WEBHOOK_DEX_DRAFTS, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: message }),
  });

  // Store pending draft in Supabase for "send" command lookup
  await supabase.from('email_drafts').insert({
    prospect_email: prospectEmail,
    draft: emailDraft,
    status: 'pending',
  });
}
```

### Send Handler (Discord slash command or message trigger)
```js
// When Matt types "send" in #dex-drafts
async function sendApprovedEmail(draftId) {
  const { data: draft } = await supabase.from('email_drafts').select('*').eq('id', draftId).single();

  await resend.emails.send({
    from: 'hello@inthepast.ai',
    to: draft.prospect_email,
    subject: 'Following up on our call',
    html: draft.draft_html,
  });

  await supabase.from('email_drafts').update({ status: 'sent', sent_at: new Date() }).eq('id', draftId);
}
```

### Auth — Verify Fireflies Webhook
```js
import crypto from 'crypto';
const sig = req.headers['x-fireflies-signature'];
const expected = crypto.createHmac('sha256', process.env.FIREFLIES_SECRET).update(rawBody).digest('hex');
if (sig !== expected) return res.status(401).send('Invalid signature');
```

## Gotchas
- Industry reasoning: think about what the prospect does all day — not a static lookup table
- NEVER auto-send — always post to Discord and wait for explicit "send" from Matt
- Store draft in Supabase immediately — Discord messages don't persist reliably
- Resend from address: hello@inthepast.ai (verify domain in Resend dashboard)
- Fireflies payload: `summary.overview` and `transcript` array with `{speaker, content}` objects
- Rate: one draft per call — don't batch or Matt loses context
