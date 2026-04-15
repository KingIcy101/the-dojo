---
name: echo-test-call-pattern
description: Use when Echo needs to test a newly built Vapi agent before marking it live — never skip this step.
category: meta
---
# Echo Test Call Pattern

## When to Use
After Echo builds or updates a Vapi agent. Required before marking any agent live. No exceptions — even small script changes need a test call.

## Steps
1. POST to Vapi `/call/phone` with agent details + Matt's test number
2. Wait 60 seconds for call to complete
3. Retrieve call record from Vapi API
4. Check transcript against 4 pass criteria
5. Pass → mark agent live; Fail → post failure to Discord + flag Scribe

## Key Patterns / Code

```ts
// Step 1: Trigger test call
const callRes = await fetch('https://api.vapi.ai/call/phone', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.VAPI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    phoneNumberId: process.env.VAPI_PHONE_NUMBER_ID,
    assistantId: agentId,
    customer: {
      number: process.env.TEST_PHONE_NUMBER,  // Matt's test number
      name: 'Test Caller',
    },
  }),
});
const { id: callId } = await callRes.json();
```

```ts
// Step 2: Wait for completion
await new Promise(r => setTimeout(r, 60000)); // 60s

// Step 3: Retrieve call
const callData = await fetch(`https://api.vapi.ai/call/${callId}`, {
  headers: { 'Authorization': `Bearer ${process.env.VAPI_API_KEY}` },
}).then(r => r.json());

const transcript = callData.transcript ?? '';
```

```ts
// Step 4: Check transcript against pass criteria
const checks = [
  {
    name: 'Greeting used correct business name',
    pass: transcript.toLowerCase().includes(businessName.toLowerCase()),
  },
  {
    name: 'Gathered caller name',
    pass: /your name|may i ask|who (am i|is this)/i.test(transcript),
  },
  {
    name: 'Offered appointment',
    pass: /appointment|schedule|book|availab/i.test(transcript),
  },
  {
    name: 'No banned phrases',
    pass: !/(sure thing|yeah\.|hm\b)/i.test(transcript),
  },
];

const allPassed = checks.every(c => c.pass);
const failures = checks.filter(c => !c.pass);
```

```ts
// Step 5: Report result
if (allPassed) {
  await discordPost('#agency-team-chat', `✅ Test call passed for **${businessName}** — agent marked live`);
  await markAgentLive(agentId);
} else {
  const failList = failures.map(f => `• ${f.name}`).join('\n');
  await discordPost('#agency-team-chat',
    `❌ Test call FAILED for **${businessName}**:\n${failList}\nFlagged for Scribe revision.`);
  await flagForScribeRevision(agentId, failures);
}
```

## Pass Criteria (all 4 required)
1. Greeting includes exact business name
2. Agent asked for caller's name
3. Agent offered to book an appointment
4. No banned phrases: "Sure thing", "Yeah.", "Hm"

## Gotchas
- Wait the full 60s before retrieving — Vapi needs time to process + transcribe
- If call status is `failed` after 60s, check phoneNumberId is active in Vapi dashboard
- Transcript may be null if call was very short — treat as automatic fail
- Banned phrases are case-insensitive — regex with `/i` flag
- Never mark agent live manually without running this pattern — Scribe errors compound
- Test phone number is Matt's personal number — don't leak it to logs/Discord
