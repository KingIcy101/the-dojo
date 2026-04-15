---
name: gohighlevel
description: >
  GoHighLevel (GHL) API — CRM, contacts, pipelines, calendars, messaging, workflows.
  Halo Marketing runs on GHL. Use for syncing client data, automating pipelines, reading campaign stats.
  Blocked until Matt provides GHL Location API Key.
---

# GoHighLevel API

## Status
**BLOCKED** — needs `GHL_LOCATION_API_KEY` from Matt (Settings → Business Profile → API Keys in GHL dashboard)

## Auth
```js
// All requests use Location API Key
const headers = {
  'Authorization': `Bearer ${process.env.GHL_LOCATION_API_KEY}`,
  'Content-Type': 'application/json',
  'Version': '2021-07-28'
}
const BASE = 'https://rest.gohighlevel.com/v1'
```

## Core Endpoints

### Contacts
```js
// Get all contacts
GET /contacts/?locationId={locationId}&limit=100

// Search contact
GET /contacts/search?locationId={locationId}&query=john@email.com

// Create contact
POST /contacts/
{
  "firstName": "John", "lastName": "Smith",
  "email": "john@clinic.com", "phone": "+17039999999",
  "locationId": process.env.GHL_LOCATION_ID,
  "tags": ["prospect", "chiro"],
  "customField": [{ "id": "field_id", "value": "value" }]
}

// Update contact
PUT /contacts/{contactId}

// Add tag
POST /contacts/{contactId}/tags
{ "tags": ["called", "interested"] }
```

### Pipelines & Opportunities
```js
// Get pipelines
GET /pipelines/?locationId={locationId}

// Get opportunities in pipeline
GET /pipelines/{pipelineId}/opportunities

// Create opportunity (add contact to pipeline)
POST /pipelines/{pipelineId}/opportunities
{
  "title": "Dr. Pierce - Discovery Call",
  "contactId": "contact_id",
  "status": "open",
  "stageId": "stage_id",
  "monetaryValue": 1950
}

// Move stage
PUT /pipelines/{pipelineId}/opportunities/{opportunityId}
{ "stageId": "new_stage_id" }
```

### Calendar / Appointments
```js
// Get calendar slots
GET /appointments/slots?calendarId={id}&startDate=2026-03-01&endDate=2026-03-31

// Book appointment
POST /appointments/
{
  "calendarId": "cal_id",
  "locationId": "loc_id",
  "contactId": "contact_id",
  "startTime": "2026-03-10T14:00:00Z",
  "endTime": "2026-03-10T14:30:00Z",
  "title": "Discovery Call - Dr. Pierce"
}

// Get appointments for contact
GET /contacts/{contactId}/appointments
```

### Messaging (SMS/Email)
```js
// Send SMS
POST /conversations/messages
{
  "type": "SMS",
  "contactId": "contact_id",
  "message": "Hi Dr. Smith, your campaign is live!"
}

// Send Email
POST /conversations/messages
{
  "type": "Email",
  "contactId": "contact_id",
  "subject": "Your Monthly Report",
  "html": "<p>...</p>"
}
```

### Webhooks (Real-time Events)
```js
// GHL fires webhooks for 50+ events
// Set in GHL: Settings → Integrations → Webhooks

// Events we care about:
// ContactCreate — new lead
// AppointmentCreate — new booking
// OpportunityCreate — new pipeline entry
// InboundMessage — client replied

// Verify webhook (GHL uses HMAC)
import crypto from 'crypto'
const sig = req.headers['x-ghl-signature']
const computed = crypto.createHmac('sha256', process.env.GHL_WEBHOOK_SECRET)
  .update(JSON.stringify(req.body)).digest('hex')
if (sig !== computed) return res.status(401).send('Unauthorized')
```

## Environment Variables
```env
GHL_LOCATION_API_KEY=      # ← NEEDED — get from GHL dashboard
GHL_LOCATION_ID=           # ← NEEDED — your location ID
GHL_WEBHOOK_SECRET=        # optional — for webhook verification
```

## Halo Use Cases
- **Auto-sync new clients** → create GHL contact + opportunity on payment
- **Pipeline automation** → move stages based on discovery call outcome
- **Appointment tracking** → read upcoming calls, alert if no-show
- **SMS automation** → trigger appointment reminders via Bland.ai webhook
- **Report generation** → pull contact/campaign data for monthly reports

## Skill Injection for Codex/Claude Code
```
GoHighLevel API base: https://rest.gohighlevel.com/v1
Auth: Bearer GHL_LOCATION_API_KEY header + Version: 2021-07-28
Key endpoints: /contacts, /pipelines/{id}/opportunities, /appointments, /conversations/messages
Webhook verification: HMAC SHA256 with GHL_WEBHOOK_SECRET.
BLOCKED until Matt provides GHL_LOCATION_API_KEY.
```
