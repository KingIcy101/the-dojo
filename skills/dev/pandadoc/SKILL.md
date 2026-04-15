---
name: pandadoc
description: >
  PandaDoc API — create, send, and track proposals/contracts programmatically.
  Already using PandaDoc for Halo client contracts. Automate proposal generation from templates.
  Use for auto-generating proposals when a prospect is ready to close.
---

# PandaDoc — Proposals & Contracts

## Setup
```js
const PANDADOC_API = 'https://api.pandadoc.com/public/v1'
const headers = {
  'Authorization': `API-Key ${process.env.PANDADOC_API_KEY}`,
  'Content-Type': 'application/json',
}
```

## Create Document from Template
```js
// Auto-generate Halo proposal for a prospect
const doc = await fetch(`${PANDADOC_API}/documents`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    name: `Halo Marketing Proposal — Dr. Pierce`,
    template_uuid: process.env.PANDADOC_HALO_TEMPLATE_ID,
    recipients: [
      {
        email: 'pierce@example.com',
        first_name: 'Dr.',
        last_name: 'Pierce',
        role: 'Client',
      }
    ],
    tokens: [
      { name: 'Client.Name', value: 'Dr. Pierce' },
      { name: 'Client.Practice', value: 'Pierce Family Dental' },
      { name: 'Service.Plan', value: 'Standard — $1,950/mo' },
      { name: 'Contract.StartDate', value: 'March 10, 2026' },
    ],
    fields: {
      monthly_retainer: { value: '$1,950' },
      contract_term: { value: '3 months minimum' },
    }
  })
}).then(r => r.json())

console.log(doc.id, doc.status)
```

## Send for Signature
```js
// Send document to recipients
await fetch(`${PANDADOC_API}/documents/${docId}/send`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    message: 'Hi Dr. Pierce, please review and sign your Halo Marketing proposal.',
    silent: false,  // sends email notification
  })
})
```

## Check Document Status
```js
const doc = await fetch(`${PANDADOC_API}/documents/${docId}`, { headers }).then(r => r.json())
console.log(doc.status)
// draft | sent | viewed | waiting_for_payment | approved | rejected | completed
```

## Webhook (Status Changes)
```js
// POST /api/webhooks/pandadoc
export async function POST(req) {
  const event = await req.json()

  if (event.event === 'document_completed') {
    const { name, recipients } = event.data
    // Contract signed — trigger onboarding workflow
    await triggerClientOnboarding({
      clientName: recipients[0].first_name,
      email: recipients[0].email,
    })
    // Update GHL pipeline stage
    await moveGHLPipelineStage(event.data.id, 'signed')
  }
}
```

## List Documents
```js
const docs = await fetch(`${PANDADOC_API}/documents?status=sent&count=20`, { headers })
  .then(r => r.json())

docs.results.forEach(doc => {
  console.log(doc.name, doc.status, doc.date_modified)
})
```

## Environment Variables
```env
PANDADOC_API_KEY=              # From PandaDoc → Settings → API
PANDADOC_HALO_TEMPLATE_ID=    # Template UUID from PandaDoc dashboard
```

## Halo Automation Workflow
```
Prospect ready to close (GHL stage = "Proposal Sent")
→ Auto-generate PandaDoc proposal from template
→ Send for signature
→ Webhook: doc completed → trigger n8n onboarding workflow
→ Create Stripe subscription → Send welcome email (Resend) → Create GHL active client
```

## Skill Injection for Codex/Claude Code
```
PandaDoc API: https://api.pandadoc.com/public/v1
Auth: Authorization: API-Key {PANDADOC_API_KEY}
Create from template: POST /documents with template_uuid + recipients + tokens.
Send: POST /documents/{id}/send.
Webhook: event=document_completed → trigger onboarding.
Full automation: GHL stage change → PandaDoc → Stripe → Resend → GHL update.
```


## Learned from Use (2026-03-22)
SKIP

The session logs provided contain no mentions of the "pandadoc" skill being used. The logs document Vercel deployments, Agent Lounge frontend issues, Forge build handoffs, and Obsidian sync tasks—but no PandaDoc document generation, template usage, or document automation activity.

To extract learned lessons about pandadoc, I would need session logs that actually show pandadoc skill invocations, corrections related to document generation, or decisions about when/how to use pandadoc for agent workflows.


## Learned from Use (2026-03-29)
SKIP

The session logs contain no mentions of the "pandadoc" skill being used. The logs focus on Portal v1 QA cycles, typography fixes, agent coordination, and deployment pipeline corrections, but do not reference pandadoc at all. Without evidence of pandadoc usage, corrections involving it, or outcomes tied to it, there are no specific, actionable lessons to extract about this skill.


## Learned from Use (2026-04-05)
SKIP

The session logs provided contain no mentions of the "pandadoc" skill being used. The logs document work on AI agents (OpenClaw, Pixel, Gemini), Discord integration, the Halo Portal project, and billing setup — but do not reference pandadoc at all. Without actual usage data, corrections, or outcomes related to pandadoc, there are no specific, actionable lessons to extract.


## Learned from Use (2026-04-12)
SKIP

The session logs provided contain no mentions of the "pandadoc" skill being used, tested, or corrected. The logs focus on infrastructure issues (rate limits, model availability, billing), project status (Auralux, Cyrus, ZTA), and general context management practices. There are no specific incidents, corrections, or patterns related to pandadoc usage to extract.
