---
name: bland-ai
description: >
  Bland.ai — AI phone calling platform. Used by Halo Marketing as "appointment reminder team."
  Outbound calls for appointment reminders, follow-ups, no-show rescheduling.
  Has a REST API for triggering calls, managing agents, and reading call transcripts.
---

# Bland.ai — AI Phone Calling

## What It Is
Bland.ai is our AI calling infrastructure for Halo Marketing. Marketed to clients as the "appointment reminder team." Handles outbound calls for appointment reminders, confirmation calls, and no-show rescheduling — all automated.

## API Base
```
https://api.bland.ai/v1
Authorization: YOUR_BLAND_API_KEY
```

## Trigger a Call
```js
const response = await fetch('https://api.bland.ai/v1/calls', {
  method: 'POST',
  headers: {
    'Authorization': process.env.BLAND_API_KEY,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    phone_number: '+17039999999',
    task: `You are calling on behalf of Dr. Smith's chiropractic clinic. 
           The patient has an appointment tomorrow at 2pm. 
           Confirm they're still coming, or reschedule if needed.
           Be warm, professional, and brief.`,
    voice: 'Lindsey',   // consistent voice across all Halo calls
    language: 'en-US',
    max_duration: 3,    // minutes
    record: true,
    webhook: 'https://your-server.com/api/bland-webhook',
    metadata: {
      client_id: 'renee_123',
      patient_name: 'John Smith',
      appointment_time: '2026-03-05 14:00'
    }
  })
})
const { call_id } = await response.json()
```

## Get Call Status
```js
const call = await fetch(`https://api.bland.ai/v1/calls/${callId}`, {
  headers: { 'Authorization': process.env.BLAND_API_KEY }
}).then(r => r.json())

console.log(call.status)       // 'completed' | 'failed' | 'in-progress'
console.log(call.transcript)   // full conversation text
console.log(call.summary)      // AI-generated summary
console.log(call.answered)     // true/false
```

## Webhook Handler
```js
// POST /api/bland-webhook
export async function POST(req) {
  const event = await req.json()

  switch (event.status) {
    case 'completed':
      // Log transcript to GHL contact note
      // If not confirmed → schedule follow-up
      await logCallToGHL(event.metadata.client_id, event.transcript)
      if (!event.confirmed) await scheduleFollowUp(event)
      break
    case 'no-answer':
      // Try again in 2 hours
      await scheduleRetry(event.phone_number, 2)
      break
    case 'voicemail':
      // Leave voicemail, don't retry
      break
  }
}
```

## Batch Calls (Multiple Patients)
```js
// Send reminder calls to all patients with appointments tomorrow
const patients = await getAppointmentsTomorrow()

await Promise.all(patients.map(patient =>
  fetch('https://api.bland.ai/v1/calls', {
    method: 'POST',
    headers: { 'Authorization': process.env.BLAND_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      phone_number: patient.phone,
      task: buildReminderScript(patient),
      voice: 'Lindsey',
      max_duration: 2,
      metadata: { patient_id: patient.id, client_id: patient.clinic_id }
    })
  })
))
```

## Script Templates

### Appointment Reminder
```
You're calling from [Clinic Name] to remind [Patient] about their appointment 
tomorrow at [Time] with [Doctor]. Ask if they can still make it. 
If yes, confirm. If no, offer to reschedule for [Alternative Times].
Keep it under 60 seconds. Be warm and friendly.
```

### No-Show Follow-up
```
You're calling from [Clinic Name]. [Patient] missed their appointment today at [Time].
Express concern for their health, offer to reschedule.
Suggest [2-3 time slots]. Keep it empathetic, not transactional.
```

## Environment Variables
```env
BLAND_API_KEY=   # Get from app.bland.ai → API Keys
```

## Halo Marketing Integration
- Trigger calls via GHL webhook when appointment is booked
- Log call results back to GHL contact notes
- Track: confirmed / rescheduled / no-answer / declined
- KPI: confirmation rate per client (target: 85%+)

## Skill Injection for Codex/Claude Code
```
Bland.ai API: POST https://api.bland.ai/v1/calls with Authorization header.
Required: phone_number, task (script), voice: 'Lindsey', record: true.
Always include webhook URL for async results. Use metadata for client/patient tracking.
Webhook events: completed (has transcript+summary), no-answer, voicemail.
```


## Learned from Use (2026-03-22)
SKIP

The session logs contain deployment troubleshooting, build issues, and task coordination, but show no evidence of the "bland-ai" skill being used or corrected. The logs document:
- Vercel deployment/auth problems
- Forge build handoffs
- Canvas rendering bugs
- UI specification mismatches

There are no moments where bland-ai was applied, failed, succeeded, or required correction. The "SKIP" markers in the memory snapshots and the absence of bland-ai in the corrections log confirm this skill was not exercised during this session.
