---
name: resend
description: >
  Resend — developer-first transactional email API. Clean API, React Email templates, high deliverability.
  Use for all app emails: welcome, invoices, notifications, client reports. Better than SendGrid for devs.
---

# Resend — Transactional Email

## Setup
```bash
npm install resend react-email @react-email/components
```
```js
import { Resend } from 'resend'
const resend = new Resend(process.env.RESEND_API_KEY)
```

## Send Email (Simple)
```js
const { data, error } = await resend.emails.send({
  from: 'Halo Marketing <hello@gohalomarketing.com>',
  to: ['client@example.com'],
  subject: 'Your Campaign Report is Ready',
  html: '<h1>Hi Dr. Smith,</h1><p>Your report is ready.</p>',
})
```

## React Email Templates (Pro Pattern)
```jsx
// emails/CampaignReport.tsx
import { Html, Head, Body, Container, Text, Button, Hr } from '@react-email/components'

export function CampaignReportEmail({ clientName, leads, spend, cpl }) {
  return (
    <Html>
      <Head />
      <Body style={{ fontFamily: 'Inter, sans-serif', background: '#f9fafb' }}>
        <Container style={{ maxWidth: '600px', margin: '0 auto', padding: '40px 20px' }}>
          <Text style={{ fontSize: '24px', fontWeight: '700', color: '#111' }}>
            Your Monthly Report
          </Text>
          <Text style={{ color: '#6b7280' }}>Hi {clientName},</Text>
          <Hr />
          <Text>Leads generated: <strong>{leads}</strong></Text>
          <Text>Ad spend: <strong>${spend}</strong></Text>
          <Text>Cost per lead: <strong>${cpl}</strong></Text>
          <Button href="https://dashboard.gohalomarketing.com" style={{
            background: '#6366f1', color: 'white', padding: '12px 24px',
            borderRadius: '8px', textDecoration: 'none'
          }}>
            View Full Dashboard
          </Button>
        </Container>
      </Body>
    </Html>
  )
}

// Send with template
import { render } from '@react-email/render'

const html = render(<CampaignReportEmail clientName="Dr. Smith" leads={47} spend={1950} cpl={41} />)

await resend.emails.send({
  from: 'Halo Marketing <reports@gohalomarketing.com>',
  to: client.email,
  subject: `Your ${month} Campaign Report`,
  html,
})
```

## Batch Sending
```js
// Send to multiple recipients at once
await resend.batch.send([
  { from: '...', to: 'client1@...', subject: '...', html: '...' },
  { from: '...', to: 'client2@...', subject: '...', html: '...' },
])
```

## Scheduled Emails
```js
// Schedule for future delivery
await resend.emails.send({
  from: '...',
  to: '...',
  subject: '...',
  html: '...',
  scheduledAt: '2026-03-10T09:00:00Z', // ISO 8601
})
```

## Environment Variables
```env
RESEND_API_KEY=re_...
```

## Domain Setup
- Add DNS records in Resend dashboard for gohalomarketing.com
- Enables sending from @gohalomarketing.com addresses
- Improves deliverability significantly vs generic domains

## Best Use Cases for Our Builds
- **Halo client reports** — monthly campaign summary emails
- **AI agency** — welcome, onboarding, invoices
- **Mission Control** — alert emails for important events
- **Client portals** — account notifications

## Skill Injection for Codex/Claude Code
```
Use Resend (resend) for all transactional email. npm install resend react-email.
React Email for templates — render(<Template />) → html string → resend.emails.send().
from: 'Name <email@gohalomarketing.com>'. Always verify domain in Resend dashboard.
Batch send available. Schedule with scheduledAt ISO timestamp.
```


## Learned from Use (2026-03-22)
SKIP

The session logs provided contain no mentions of the "resend" skill being used. The logs document deployment workflows, build issues, task handoffs, and corrections related to image reading and Codex briefing processes — but do not show any usage patterns, failures, or successes with a "resend" skill that would generate actionable lessons about how to use it effectively.


## Learned In Use

- **2026-03-24:** Resend API keys must be explicitly set in environment or .env files for voice agents — missing keys cause silent failures in agent workflows.

## Learned from Use (2026-03-29)
SKIP

The session logs do not contain any mentions of the "resend" skill being used. The logs discuss build processes, QA audits, typography fixes, deployment, and agent coordination, but there are no references to a "resend" action, function, or skill being executed or corrected. Without evidence of actual "resend" skill usage, corrections related to it, or patterns specific to that skill, I cannot extract actionable lessons about it.
