---
name: resend-transactional-email
description: Send transactional emails via Resend API with React Email templates, error handling, and webhook support.
category: dev
---

# Resend Transactional Email

## When to Use
Any app email: welcome, appointment confirmation, invoice, notification, client report.
From address: hello@inthepast.ai. Key: re_UqojquC9_GRB9qnvaqdn1Mo1S8WZYKKHi (in .env as RESEND_API_KEY).

## Steps
1. `npm install resend @react-email/components`
2. Create React Email template in `emails/` directory
3. Use `send-email.js` helper (see pattern below)
4. Handle 429/422/5xx errors appropriately
5. Set up webhook in Resend dashboard for bounces/complaints

## Key Patterns / Code

### send-email.js (voice-server pattern)
```js
import { Resend } from 'resend';
const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendEmail({ to, subject, html, from = 'hello@inthepast.ai' }) {
  try {
    const { data, error } = await resend.emails.send({ from, to, subject, html });
    if (error) throw error;
    return { success: true, id: data.id };
  } catch (err) {
    if (err.statusCode === 429) {
      // Rate limited — wait and retry
      await new Promise(r => setTimeout(r, 5000));
      return sendEmail({ to, subject, html, from });
    }
    if (err.statusCode === 422) {
      // Invalid address — log and skip, don't retry
      console.error('Invalid email address:', to);
      return { success: false, reason: 'invalid_address' };
    }
    // 5xx — retry once after delay
    throw err;
  }
}
```

### React Email Template
```tsx
// emails/AppointmentConfirm.tsx
import { Html, Body, Heading, Text, Button } from '@react-email/components';

export function AppointmentConfirm({ name, date, businessName }) {
  return (
    <Html>
      <Body style={{ fontFamily: 'sans-serif' }}>
        <Heading>Your appointment is confirmed</Heading>
        <Text>Hi {name}, you're booked at {businessName} on {date}.</Text>
        <Button href="https://cal.com/matt-bender-ai/30min">Reschedule</Button>
      </Body>
    </Html>
  );
}

// Render to HTML for sending
import { render } from '@react-email/render';
const html = render(<AppointmentConfirm name="Jane" date="Apr 20" businessName="Smile Dental" />);
await sendEmail({ to: 'jane@example.com', subject: 'Appointment Confirmed', html });
```

### Webhook (bounces/complaints)
```js
app.post('/webhooks/resend', express.raw({ type: 'application/json' }), (req, res) => {
  const event = JSON.parse(req.body);
  if (event.type === 'email.bounced') {
    // Mark email as invalid in DB
    db.contacts.update({ email: event.data.to }, { emailBounced: true });
  }
  if (event.type === 'email.complained') {
    // Unsubscribe user
    db.contacts.update({ email: event.data.to }, { unsubscribed: true });
  }
  res.sendStatus(200);
});
```

## Gotchas
- Rate limits: 100 emails/day (free), 50K/mo (pro $20/mo)
- Must verify domain in Resend dashboard (DNS records) before sending from custom domain
- `from` must match verified domain — hello@inthepast.ai requires inthepast.ai verified
- React Email render happens at call time — don't cache HTML with dynamic data
- Webhook secret: verify `resend-signature` header to prevent spoofing