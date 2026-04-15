---
name: twilio-a2p-10dlc
description: Register a brand and SMS campaign for A2P 10DLC so Twilio can send US SMS without filtering or rejection.
category: dev
---

# Twilio A2P 10DLC Registration

## When to Use
Any time you send SMS via Twilio from a US long code. Without registration messages are filtered/blocked.
No SMS can be sent until campaign status is VERIFIED — return 403 from any send attempt until then.

## Steps

### 1. Brand Registration
- Console → Messaging → Regulatory Compliance → A2P 10DLC → Register a Brand
- Required: legal business name, EIN, address, vertical (PROFESSIONAL), website
- Brand SID: `BN...` | Status: PENDING → APPROVED (24-48h)

### 2. Campaign Registration
- Console → Messaging → A2P 10DLC → Campaigns → Add Campaign
- Use case: `LOW_VOLUME_MIXED` (mixed marketing + transactional, <3K msg/day)
- Other options: `APPOINTMENT_REMINDER`, `CUSTOMER_CARE`, `NOTIFICATIONS`
- Campaign SID: `QE2c...` | Status: IN_PROGRESS → VERIFIED (1-5 business days)

### 3. Associate Phone Number
- After VERIFIED: Campaigns → [campaign] → Phone Numbers → Add Number
- Phone number must be in same Twilio account

### 4. Guard Sends in Code
```js
async function safeSend(to, body) {
  if (process.env.TWILIO_10DLC_STATUS !== 'VERIFIED') {
    throw { status: 403, message: 'SMS unavailable — 10DLC pending approval' };
  }
  return twilioClient.messages.create({ to, from: process.env.TWILIO_NUMBER, body });
}
```

## Key Patterns / Code

```js
// Use Messaging Service SID (MG...) not Campaign SID in sends
await twilioClient.messages.create({
  to: '+17035551234',
  messagingServiceSid: process.env.TWILIO_MESSAGING_SERVICE_SID,
  body: 'Your appointment is confirmed. Reply STOP to unsubscribe.'
});

// Webhook to auto-update status (set in console)
app.post('/webhooks/twilio-campaign', (req, res) => {
  const { CampaignStatus, CampaignSid } = req.body;
  if (CampaignStatus === 'VERIFIED') {
    process.env.TWILIO_10DLC_STATUS = 'VERIFIED'; // or update DB
  }
  res.sendStatus(200);
});
```

## Common Rejection Reasons & Resubmission
- **BRAND_REJECTED**: EIN mismatch — recheck IRS records, resubmit brand
- **CAMPAIGN_REJECTED**: Opt-in description too vague — be explicit: "User enters phone on web form and checks consent checkbox"
- **SAMPLE_MESSAGES_REJECTED**: Must match use case + include opt-out: "Reply STOP to unsubscribe"
- Fix: delete failed campaign → create new one (cannot edit rejected campaigns)

## Gotchas
- Messaging Service SID (`MG...`) ≠ Campaign SID (`QE2c...`) — use MG in `messages.create()`
- Short codes bypass 10DLC but cost $500-1K/mo to lease
- Toll-free numbers have separate verification (~3 days, often faster)
- Canada/UK/AU have their own registration — 10DLC is US-only
- Always include STOP opt-out language in sample messages and actual sends