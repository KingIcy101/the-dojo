---
name: vapi-agent-build
description: Full end-to-end Vapi voice agent creation — squad config, voice, tools, backoff, and test call.
category: dev
---

# Vapi Agent Build

## When to Use
Building or modifying a Vapi AI phone agent for ITP clients. Covers creation, voice config, system prompt, tools, backoff tuning, and live test call.

## Steps

1. **Create the assistant** via `POST /assistant`
2. **Set voice** to Cartesia Patricia
3. **Write system prompt** — load from Scribe output
4. **Add tools** (transferCall, endCall, custom function calls)
5. **Configure backoff** and banned words
6. **Assign to squad** if multi-agent flow
7. **Test call** via `POST /call/phone`

## Key Patterns / Code

### Create Assistant
```js
const assistant = await fetch('https://api.vapi.ai/assistant', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.VAPI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'ClientName Receptionist',
    model: {
      provider: 'anthropic',
      model: 'claude-3-5-sonnet-20241022',
      systemPrompt: SYSTEM_PROMPT,
    },
    voice: {
      provider: 'cartesia',
      voiceId: 'e5a6cd18-d552-4192-9533-82a08cac8f23', // Patricia
    },
    firstMessage: 'Thank you for calling [Business]. How can I help you today?',
    silenceTimeoutSeconds: 20,
    maxDurationSeconds: 600,
    backgroundDenoisingEnabled: true,
    stopSpeakingPlan: {
      backoffSeconds: 1.5,   // 1.0 for demo, 1.5 for live phone
      numWords: 5,
      voiceSeconds: 0.5,
    },
  }),
});
```

### Banned Words (add to system prompt)
```
NEVER say: "Sure thing", "Yeah.", "Hm"
USE INSTEAD: "Of course,", "Right,", [natural pause]
```

### Test Call
```js
await fetch('https://api.vapi.ai/call/phone', {
  method: 'POST',
  headers: { Authorization: `Bearer ${VAPI_API_KEY}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phoneNumberId: '9c4b42ed-1c8a-4b14-b3b2-432d5b606d61',
    customer: { number: '+1TESTPHONE' },
    assistantId: ASSISTANT_ID,
  }),
});
```

### Credentials
```
VAPI_API_KEY=32a82f37-de70-418f-ba38-7cb94514c6e1
PHONE_NUMBER_ID=9c4b42ed-1c8a-4b14-b3b2-432d5b606d61
```

## Gotchas
- `backoffSeconds: 1.0` for demo, `1.5` for live phone — never lower than 1.0 or agent interrupts caller
- "Hm" in TTS sounds like "Ham" — always banned
- "Yeah." with a period causes audio volume spike artifact
- First message must be under 20 words, warm, no filler
- Spell out "twenty-four seven" not "24/7" — TTS reads digits awkwardly
- ElevenLabs Rachel (F) / Adam (M) are acceptable voice fallbacks if Cartesia issues
- Always verify assistant status is active before handing off to client
