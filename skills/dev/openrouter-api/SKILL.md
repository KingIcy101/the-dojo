---
name: openrouter-api
description: Use when making LLM API calls via OpenRouter — model routing, auth, fallbacks, usage tracking.
category: dev
---
# OpenRouter API

## When to Use
Any time you're calling an LLM from server-side code and want unified access to Claude, Gemini, GPT-4o, etc. via one API key and one base URL.

## Steps
1. Set `OPENROUTER_API_KEY` in `.env`
2. Use base URL `https://openrouter.ai/api/v1`
3. Always include `HTTP-Referer: https://inthepast.ai` — missing this causes false 403s
4. Model format: `provider/model-name` (e.g. `anthropic/claude-sonnet-4-6`)
5. Add `fallbacks` array for resilience
6. Track usage from x-openrouter-* response headers

## Key Patterns / Code

```ts
// src/lib/openrouter.ts
const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
    'HTTP-Referer': 'https://inthepast.ai',   // REQUIRED — false 403 without it
    'X-Title': 'In The Past AI',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'anthropic/claude-sonnet-4-6',
    fallbacks: ['openai/gpt-4o'],             // auto-fallback on 5xx/timeout
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 1024,
  }),
});
const data = await res.json();
const text = data.choices[0].message.content;

// Usage tracking from headers
const cost = res.headers.get('x-openrouter-cost'); // USD string e.g. "0.000234"
const promptTokens = res.headers.get('x-openrouter-prompt-tokens');
```

```ts
// Exponential backoff on 429
async function callWithRetry(body: object, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
        'HTTP-Referer': 'https://inthepast.ai',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    if (res.status === 429) {
      await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
      continue;
    }
    return res.json();
  }
  throw new Error('OpenRouter: max retries exceeded — alert Matt');
}
```

## Key Models
| Model | Provider Key | Use Case |
|-------|-------------|----------|
| Claude Sonnet 4.6 | `anthropic/claude-sonnet-4-6` | Judgment, writing, reasoning |
| Gemini 2.5 Pro | `google/gemini-2.5-pro-preview` | Large context, long codebases |
| GPT-4o | `openai/gpt-4o` | Voice/Echo/Dex agent work |
| GPT-4o-mini | `openai/gpt-4o-mini` | High-volume cheap tasks |

## Gotchas
- Missing `HTTP-Referer` → false 403 — always include it, this is the #1 gotcha
- Model names must have provider prefix: `google/gemini-2.5-pro-preview` not `gemini-2.5-pro-preview`
- `fallbacks` only fires on 5xx/timeout — not on content refusals
- Response shape matches OpenAI spec: `data.choices[0].message.content`
- Free tier models have rate limits — check openrouter.ai model page before prod use
- Cost per token varies 10x between models — check pricing before switching
