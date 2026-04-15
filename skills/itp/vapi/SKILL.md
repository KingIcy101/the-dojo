---
name: vapi
description: "Vapi — AI phone calling platform. Build, configure, and manage AI voice agents for inbound and outbound calls. Used by Echo to configure AI receptionists for In The Past AI clients."
---

# Vapi — AI Voice Agent Platform

## What Vapi Does
Vapi hosts AI voice agents that handle real phone calls. An agent can:
- Answer inbound calls 24/7
- Run a conversation flow (qualify, book, gather info)
- Transfer to a human when conditions are met
- Make outbound calls (appointment reminders, follow-ups)
- Integrate with calendars and CRMs

## API Base URL
```
https://api.vapi.ai
```

## Authentication
```
Authorization: Bearer ${VAPI_API_KEY}
```
Store key in voice-server/.env as `VAPI_API_KEY`

---

## Core Concepts

### Assistant
The AI voice persona. Has a name, voice, system prompt, and conversation model.

### Call
A phone call routed through Vapi. Can be inbound (client's number forwards to Vapi) or outbound (Vapi dials out).

### Phone Number
A Vapi-managed number, or a number forwarded from the client's carrier.

### Tool
A function the assistant can call during a conversation (e.g., book appointment, look up availability, send SMS).

### Workflow (Squad)
Multiple assistants chained together. Used for complex call routing (e.g., receptionist → specialist).

---

## Create an Assistant

```bash
curl -X POST https://api.vapi.ai/assistant \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Smith Dental - Receptionist",
    "model": {
      "provider": "openai",
      "model": "gpt-4o",
      "systemPrompt": "[SCRIBE SCRIPT GOES HERE]"
    },
    "voice": {
      "provider": "11labs",
      "voiceId": "rachel"
    },
    "firstMessage": "Thank you for calling Dr. Smith Dental. This is Sarah, how can I help you today?",
    "endCallMessage": "Thank you for calling. Have a great day!",
    "endCallPhrases": ["goodbye", "bye", "that'\''s all"],
    "transcriber": {
      "provider": "deepgram",
      "model": "nova-2",
      "language": "en"
    },
    "silenceTimeoutSeconds": 30,
    "maxDurationSeconds": 1800,
    "backgroundSound": "office"
  }'
```

**Returns:** `{ "id": "asst_xxx", ... }` — save the assistant ID

---

## Voice Options (11Labs — Recommended)

| Voice ID | Tone | Best For |
|----------|------|----------|
| `rachel` | Warm, professional | Medical, dental, general |
| `adam` | Confident, clear | Construction, home services |
| `bella` | Friendly, upbeat | Salons, retail |
| `josh` | Authoritative | Law firms, finance |
| `elli` | Calm, reassuring | Healthcare, therapy |

Other providers: `openai` (alloy, echo, fable, nova, onyx, shimmer), `deepgram`, `playht`

---

## System Prompt Structure (From Scribe's Script)

```
You are [Name], the AI receptionist for [Business Name].

## Your Role
[1-2 sentences about what you do]

## Conversation Flow
[Scribe's full script — opening, intent detection, qualifying, booking, after-hours, FAQ, close]

## Rules
- Never say you are an AI unless directly asked
- If asked if you are an AI, say "I'm an AI assistant for [Business]"
- Never make up information
- If you don't know something, say "Let me have someone from our team follow up with you"
- Keep responses concise — this is a phone call, not a chat

## Transfer Conditions
Transfer to [NUMBER] when:
- Caller says "speak to a human" or "talk to someone"
- Emergency or urgent medical situation
- Caller is upset or angry
- [Other client-specific conditions]
```

---

## Add a Tool (Calendar Booking)

```bash
curl -X PATCH https://api.vapi.ai/assistant/{assistantId} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": {
      "tools": [{
        "type": "function",
        "function": {
          "name": "bookAppointment",
          "description": "Book an appointment for the caller",
          "parameters": {
            "type": "object",
            "properties": {
              "name": {"type": "string", "description": "Caller full name"},
              "phone": {"type": "string", "description": "Caller phone number"},
              "date": {"type": "string", "description": "Requested date (YYYY-MM-DD)"},
              "time": {"type": "string", "description": "Requested time (HH:MM)"},
              "service": {"type": "string", "description": "Type of appointment"}
            },
            "required": ["name", "phone", "date", "time"]
          }
        },
        "server": {
          "url": "https://[CLIENT-WEBHOOK-URL]/book",
          "timeoutSeconds": 10
        }
      }]
    }
  }'
```

---

## Transfer to Human

```json
{
  "model": {
    "tools": [{
      "type": "transferCall",
      "destinations": [{
        "type": "number",
        "number": "+1XXXXXXXXXX",
        "message": "Please hold while I connect you with our team."
      }]
    }]
  }
}
```

---

## Inbound Call Setup (Client Forwards Their Number)

1. Create assistant → get `assistantId`
2. Give client this webhook URL format: `https://api.vapi.ai/call/phone`
3. Client sets their carrier call forwarding to Vapi's inbound number
4. OR: Buy a Vapi number and have client forward to it:

```bash
# Buy a phone number
curl -X POST https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{"provider": "twilio", "areaCode": "XXX"}'

# Assign assistant to number
curl -X PATCH https://api.vapi.ai/phone-number/{numberId} \
  -d '{"assistantId": "asst_xxx"}'
```

---

## Make a Test Call

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "asst_xxx",
    "phoneNumberId": "num_xxx",
    "customer": {
      "number": "+1XXXXXXXXXX"
    }
  }'
```

Call your own number to test. Listen to the full conversation. Check recordings in the dashboard.

---

## Get Call Recordings + Transcripts

```bash
# List recent calls
curl https://api.vapi.ai/call?limit=10 \
  -H "Authorization: Bearer $VAPI_API_KEY"

# Get specific call (includes transcript + recording URL)
curl https://api.vapi.ai/call/{callId} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

Response includes:
- `transcript` — full text of the conversation
- `recordingUrl` — audio file URL
- `summary` — AI-generated summary of the call
- `successEvaluation` — did the call achieve its goal?

---

## Update an Assistant (After Client Feedback)

```bash
curl -X PATCH https://api.vapi.ai/assistant/{assistantId} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": {"systemPrompt": "[UPDATED SCRIPT]"}}'
```

---

## Outbound Reminders (Appointment Reminders)

```bash
curl -X POST https://api.vapi.ai/call \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d '{
    "assistantId": "asst_reminder_xxx",
    "phoneNumberId": "num_xxx",
    "customer": {"number": "+1XXXXXXXXXX", "name": "John"},
    "assistantOverrides": {
      "firstMessage": "Hi John, this is a reminder from Dr. Smith Dental about your appointment tomorrow at 2pm. Press 1 to confirm or 2 to reschedule."
    }
  }'
```

---

## Dashboard
https://dashboard.vapi.ai — view all assistants, calls, recordings, analytics

## Pricing (as of 2026)
~$0.05/minute for calls (varies by voice provider). Check dashboard for current rates.

## Docs
https://docs.vapi.ai

---

## Realism Settings — What Makes It Sound Human (Echo Must Set These)

These are the difference between a robotic bot and a convincing AI receptionist. Set them on every assistant.

```json
{
  "backchannelingEnabled": true,
  "backgroundDenoising": true,
  "modelOutputInRealtime": true,
  "responseDelaySeconds": 0.4,
  "llmRequestDelaySeconds": 0.1,
  "numWordsToInterruptAssistant": 3,
  "backgroundSound": "office",
  "fillersEnabled": true
}
```

| Setting | Value | Why |
|---------|-------|-----|
| `backchannelingEnabled` | true | Says "mm-hmm", "I see", "got it" — sounds like listening |
| `backgroundDenoising` | true | Cleans up caller audio so agent understands better |
| `modelOutputInRealtime` | true | Starts speaking faster, less dead air |
| `responseDelaySeconds` | 0.4 | Tiny natural pause before responding. 0 = robotic. 1+ = slow |
| `numWordsToInterruptAssistant` | 3 | Caller must say 3 words to interrupt — prevents accidental cutoffs |
| `backgroundSound` | "office" | Subtle office ambience — makes it feel like a real front desk |
| `fillersEnabled` | true | Occasional "um", "let me check" — more human |
| `hipaaEnabled` | true | **Required for any healthcare client** — enables HIPAA compliance mode |

## Voice Selection Guide (11Labs — Most Realistic)

Pick based on client industry and brand tone. Test via Vapi dashboard Voice Library before committing.

| Voice | Tone | Best Industries |
|-------|------|-----------------|
| `rachel` | Warm, calm, professional | Dental, medical, therapy |
| `adam` | Confident, direct | Construction, HVAC, auto repair |
| `bella` | Friendly, upbeat | Salons, spas, fitness |
| `josh` | Authoritative, trustworthy | Law, finance, insurance |
| `elli` | Gentle, reassuring | Healthcare, elder care, mental health |
| `charlotte` | Professional, British | High-end services, luxury |

Always ask client during intake: "What tone do you want — warm/friendly, professional, or authoritative?" Map their answer to a voice.

## Dashboard Test (Before Assigning Phone Number)
1. Create assistant
2. Hit **Test** button (top right in dashboard)
3. Talk to it in the browser — simulate a real caller
4. Listen for: dead air, robotic pauses, misunderstandings, wrong transfers
5. Adjust system prompt + settings until it passes
6. THEN assign the phone number

## Checklist Before Calling an Assistant "Ready"
- [ ] Greeting sounds natural, says business name + persona name
- [ ] Correctly identifies caller intent within 2 exchanges
- [ ] Books appointment OR correctly says after-hours message
- [ ] Transfers to human when asked — no failure
- [ ] Handles a confused/off-topic caller gracefully
- [ ] `hipaaEnabled: true` if healthcare client
- [ ] `backgroundSound: "office"` set
- [ ] `backchannelingEnabled: true` set
- [ ] 3 test calls minimum — different scenarios each time


## Learned In Use

- **2026-03-24:** Voice agents using 11Labs voices can silently degrade to OpenAI Nova fallback — always verify actual voice output in test calls, don't assume configured voice was used.
- **2026-03-25:** Voice agent task routing via sessions_send captures API response in JSON but 'announce' delivery mode routes to Telegram only, not Discord; must use direct bot token REST calls for Discord delivery.
- **2026-03-27:** Twilio A2P 10DLC campaign submission is a prerequisite step for SMS receptionist features and should be documented in the setup workflow.

## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Vapi wiring must happen in Forge phase, not post-deploy** — Pixel's round 2 audit caught that Vapi API wasn't connected for promotions + knowledge sources. Waiting until after deployment to verify integrations creates rework cycles. Check Vapi setup during code review before build handoff to Judge.

- **Security config for Vapi is non-negotiable** — When Vapi was wired in the fix pass, anon key + rate limiting + error sanitization + limit cap were all configured together. Core would have flagged missing security layering if any piece was incomplete. Treat Vapi API credentials and access controls as a single atomic concern, not follow-up items.

- **Vapi knowledge sources require explicit deployment verification** — The skill was mentioned as "wired" but only confirmed working after full pipeline (Forge → Judge → deploy). Don't assume Vapi knowledge sources are live until Judge can audit the rendered output showing correct source behavior in the portal.


## Learned from Use (2026-04-05)
SKIP

The session logs do not contain any mentions of the "vapi" skill being used or tested. The logs discuss OpenClaw agents, Gemini API configuration, Discord integration, and the Halo Portal project, but there are no vapi-specific interactions, corrections, or usage patterns documented that would support extracting actionable lessons about this skill.


## Learned from Use (2026-04-12)
SKIP

The session logs show no mentions of the "vapi" skill being used, tested, or corrected. The logs reference embedded agents, provider issues (Anthropic, Google), model errors, and session management problems—but no specific vapi skill usage, failures, or corrections that would generate actionable lessons about how vapi was employed.

To extract learned lessons about vapi, I would need logs showing: vapi being called, vapi errors occurring, vapi corrections being made, or vapi patterns being noted. None of these appear in the provided data.
