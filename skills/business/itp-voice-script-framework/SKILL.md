---
name: itp-voice-script-framework
description: Scribe's voice script structure for ITP AI receptionists — opening, qualification, objection handling, booking CTA.
category: business
---

# ITP Voice Script Framework

## When to Use
Building or reviewing Vapi voice scripts for In The Past AI clients. Scribe uses this structure when creating
industry-specific scripts. Covers dental, auto repair, law, medical, restaurants, contractors.

## Steps
1. Opening: warm greeting + number confirmation
2. Qualify: open-ended question about purpose of call
3. Gather info: name, concern, preferred time
4. Handle objections: doctor/owner not available → offer callback
5. Closing: confirm booking or callback, set expectation
6. Escalation: "Let me have [owner name] call you back personally"

## Key Patterns / Code

### Base Script Structure (4 turns max before CTA)
```
[OPENING]
"Thank you for calling [Business Name], this is [AI Name]. You've reached the right place!
How can I help you today?"

[QUALIFY — Turn 1]
"What brings you in today?" / "What can we help you with?"
→ Listen for: emergency vs routine, pain level, urgency

[GATHER INFO — Turn 2]
"I can definitely help with that. What's your name?"
→ Then: "And what's a good callback number?"
→ Then: "Do you have a preferred day or time for your appointment?"

[BOOK OR HANDLE OBJECTION — Turn 3]
Doctor/owner not available: "Dr. [Name] is with a patient right now,
but I can make sure they get your info and call you back within [timeframe].
Does that work for you?"

[CLOSING — Turn 4]
"Perfect, I've got you down for [time/callback]. You'll receive a
confirmation [text/call] shortly. Is there anything else I can help with?"

[ESCALATION (any turn)]
"Let me have [Dr./Owner Name] call you back personally — they'll want to hear about this directly."
```

### Industry-Specific Hooks

**Dental**
```
- Urgency trigger: "Are you experiencing any pain right now?" (pain = same-day slot)
- Info gather: tooth location, sensitivity to hot/cold, duration
- Closing hook: "We prioritize pain cases — I'll flag this as urgent for Dr. [Name]"
```

**Auto Repair**
```
- Qualify: "What year, make, and model is the vehicle?"
- Urgency: "Is it driveable right now?" (no = priority tow + appointment)
- Info gather: mileage, warning lights, symptoms
```

**Law Firm**
```
- Qualify: "What type of legal matter are you calling about?" (PI, family, criminal, etc.)
- Never give legal advice — always: "An attorney will review your case and call you back"
- Info gather: case type, incident date, opposing party
```

**Medical / Healthcare**
```
- HIPAA: don't repeat diagnosis or medical info back unnecessarily
- Urgency check: "Is this a medical emergency?" → 911 if yes
- Insurance: "Do you have insurance? Are we in-network?" → schedule callback for verification
```

**Restaurant**
```
- Reservation: party size, date, time, name, phone
- Takeout/delivery: full order, pickup time, name, phone
- Closing: "Your reservation is set for [time]. We'll see you then!"
```

## Objection Handling Patterns
| Objection | Response |
|-----------|---------|
| "I need to talk to a real person" | "I completely understand — let me have [Name] call you personally within [X]" |
| "Is this a robot?" | "I'm an AI receptionist — I handle scheduling and info so the team can focus on patients/clients" |
| "I'll call back later" | "Of course! May I grab your name and number so we can reach out too?" |
| "How much does it cost?" | "I want to make sure you get accurate pricing — [Name] will cover that when they call you back" |

## Gotchas
- Max 4 turns before booking CTA — longer scripts = higher hang-up rate
- Never confirm pricing or insurance coverage — always defer to human callback
- Always confirm what they'll receive after the call (text, confirmation call)
- Escalation phrase must include the owner/doctor's name — personal touch converts
- Test each script with real calls before going live — Vapi test call in dashboard