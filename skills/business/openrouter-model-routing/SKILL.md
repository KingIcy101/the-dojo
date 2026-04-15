---
name: openrouter-model-routing
description: Use when deciding which LLM to route a specific agent task to — maps task types to optimal models with fallback chains.
category: business
---
# OpenRouter Model Routing Strategy

## When to Use
Before making any LLM call from an agent. Pick the right model for the task. Wrong model = wasted money or poor quality. This is the routing decision layer.

## Model Assignment

| Model | Provider Key | Best For |
|-------|-------------|----------|
| Claude Sonnet 4.6 | `anthropic/claude-sonnet-4-6` | Judgment calls, writing, complex reasoning, code review |
| Gemini 2.5 Pro | `google/gemini-2.5-pro-preview` | Large codebases, 100k+ token context, document analysis |
| GPT-4o | `openai/gpt-4o` | Echo/Dex voice agent work, tool use, structured output |
| GPT-4o-mini | `openai/gpt-4o-mini` | High-volume cheap tasks, classification, simple extraction |

## Fallback Chains

```ts
// In openclaw.json or agent config — always use provider prefix
const ROUTING = {
  judgment: {
    primary: 'anthropic/claude-sonnet-4-6',
    fallback: 'openai/gpt-4o',
  },
  longContext: {
    primary: 'google/gemini-2.5-pro-preview',
    fallback: 'anthropic/claude-sonnet-4-6',
  },
  voice: {
    primary: 'openai/gpt-4o',
    fallback: 'anthropic/claude-sonnet-4-6',
  },
  cheap: {
    primary: 'openai/gpt-4o-mini',
    fallback: 'openai/gpt-4o',
  },
};
```

```ts
// Routing function
async function routedCall(taskType: keyof typeof ROUTING, messages: Message[]) {
  const route = ROUTING[taskType];
  try {
    return await callOpenRouter(route.primary, messages);
  } catch (err) {
    console.error(`Primary model failed (${route.primary}):`, err);
    try {
      return await callOpenRouter(route.fallback, messages);
    } catch (fallbackErr) {
      // Both failed — alert Matt
      await alertMattTelegram(`Model routing failure: ${taskType} — both ${route.primary} and ${route.fallback} failed`);
      throw fallbackErr;
    }
  }
}
```

```ts
// Rate limit handling — 429 → exponential backoff, max 3 retries
async function callOpenRouter(model: string, messages: Message[], attempt = 0): Promise<any> {
  const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
      'HTTP-Referer': 'https://inthepast.ai',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model, messages }),
  });

  if (res.status === 429 && attempt < 3) {
    await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
    return callOpenRouter(model, messages, attempt + 1);
  }

  if (!res.ok) throw new Error(`OpenRouter ${res.status}: ${await res.text()}`);
  return res.json();
}
```

## Task → Model Quick Reference
- Script generation (Scribe) → `anthropic/claude-sonnet-4-6`
- Codebase review (Judge) → `google/gemini-2.5-pro-preview`
- Voice agent config (Echo) → `openai/gpt-4o`
- Lead classification (Dex) → `openai/gpt-4o-mini`
- Complex reasoning (Forge) → `anthropic/claude-sonnet-4-6`

## Gotchas
- Never bare model name in openclaw.json: `gemini-2.5-pro-preview` → breaks; `google/gemini-2.5-pro-preview` → works
- Alert Matt if BOTH primary and fallback fail — don't silently swallow
- Gemini 2.5 Pro: slower to respond, higher latency — don't use for real-time tasks
- GPT-4o-mini: fast and cheap but reasoning depth is limited — don't use for judgment calls
- Max 3 retries on 429 — after that, escalate; don't hammer the API
