---
name: openrouter
description: Route LLM API calls through OpenRouter for cost efficiency, model selection, and fallback. Use when: deciding which model to use for a task, making API calls from voice-server or scripts, or when direct Anthropic/Google API calls are failing.
---

# OpenRouter Model Routing Skill

OpenRouter gives us access to every major LLM through one API key with automatic fallback. Key is in `voice-server/.env` as `OPENROUTER_API_KEY`.

---

## Model Routing Decision Tree

```
Is it a quick task (classify, format, summarize <500 tokens)?
  → google/gemini-flash-1.5 (fastest, cheapest, ~$0.075/1M tokens)

Is it a main reasoning task (write, analyze, plan, draft)?
  → anthropic/claude-sonnet-4-5 (default, best balance)

Is it a voice call response (must be <300ms)?
  → anthropic/claude-haiku-4-5 (DIRECT Anthropic only — NOT via OpenRouter)
  ⚠️ haiku via OpenRouter sometimes adds latency — use direct API for voice

Is it a complex multi-step task (agent orchestration, long context)?
  → anthropic/claude-opus-4-5 (rare, expensive — flag before using)

Is it image generation?
  → openai/dall-e-3 via OpenRouter OR nano-banana-pro skill

Is it a coding task?
  → anthropic/claude-sonnet-4-5 or openai/gpt-4o
```

---

## API Usage

```js
const OPENROUTER_KEY = process.env.OPENROUTER_API_KEY;

async function callLLM(messages, options = {}) {
  const model = options.model || 'anthropic/claude-sonnet-4-5';
  
  const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENROUTER_KEY}`,
      'Content-Type': 'application/json',
      'HTTP-Referer': 'https://gohalomarketing.com',
      'X-Title': 'Halo AI Stack',
    },
    body: JSON.stringify({
      model,
      messages,
      max_tokens: options.maxTokens || 1000,
      temperature: options.temperature ?? 0.7,
    }),
  });
  
  const data = await res.json();
  return data.choices?.[0]?.message?.content || '';
}
```

## With Fallback
```js
async function callWithFallback(messages, options = {}) {
  const models = [
    options.model || 'anthropic/claude-sonnet-4-5',
    'google/gemini-flash-1.5',
    'openai/gpt-4o-mini',
  ];
  
  for (const model of models) {
    try {
      const result = await callLLM(messages, { ...options, model });
      if (result) return result;
    } catch (e) {
      console.warn(`Model ${model} failed:`, e.message);
    }
  }
  throw new Error('All models failed');
}
```

---

## Cost Reference (approximate, per 1M tokens)

| Model | Input | Output | Best for |
|-------|-------|--------|----------|
| gemini-flash-1.5 | $0.075 | $0.30 | Classify, format, quick tasks |
| claude-haiku-4-5 | $0.80 | $4.00 | Voice responses, fast replies |
| gpt-4o-mini | $0.15 | $0.60 | Code snippets, structured output |
| claude-sonnet-4-5 | $3.00 | $15.00 | Main tasks, writing, analysis |
| gpt-4o | $5.00 | $15.00 | Complex reasoning |
| claude-opus-4-5 | $15.00 | $75.00 | Only for critical complex tasks |

## ⚠️ Known Issues
- `openrouter/anthropic/claude-haiku-4-5` prefix = WRONG, returns 404
- Correct format: `anthropic/claude-haiku-4-5` (no openrouter/ prefix)
- Voice call system uses DIRECT Anthropic API (`ANTHROPIC_API_KEY`), not OpenRouter — keep it that way for latency
- Gemini key in .env is empty — Gemini calls must go through OpenRouter

## Available Models (check openrouter.ai/models for current list)
- `anthropic/claude-sonnet-4-6` (latest)
- `anthropic/claude-haiku-4-5`
- `google/gemini-flash-1.5`
- `google/gemini-pro-1.5`
- `openai/gpt-4o`
- `openai/gpt-4o-mini`
- `meta-llama/llama-3.1-70b-instruct` (free tier available)
- `mistralai/mistral-large`


## Learned from Use (2026-03-22)
SKIP

The session logs provided contain no mentions of the "openrouter" skill being used. The logs focus on Vercel deployments, Forge build issues, Agent Lounge frontend work, and Obsidian sync tasks. The corrections log addresses image reading and Codex briefing processes, not openrouter usage.

To extract lessons about openrouter skill usage, I would need session logs that actually document openrouter being invoked, decisions made through it, or corrections applied to how it was used.


## Learned In Use

- **2026-03-25:** For high-volume, low-complexity tasks like welcome emails and intake handoffs, gpt-4o is cost-inefficient; gpt-5.4-mini provides 10x cheaper input and 9x cheaper output with acceptable quality.

## Learned from Use (2026-03-29)
SKIP

The session logs provided detail agent coordination, QA processes, build pipeline management, and memory optimization—but contain no specific information about the "openrouter" skill itself (its usage patterns, failures, gotchas, or what worked well in execution). The corrections logged are about dev process rules and channel discipline, not about how the openrouter skill was applied or should be used differently.

To extract learned lessons about openrouter, I would need session details showing: skill invocation patterns, API response handling, model selection decisions, prompt engineering results, or specific failures/successes when using openrouter.


## Learned from Use (2026-04-12)
SKIP

The logs show infrastructure/provider issues (rate limits, model availability, billing) and project management patterns, but contain no specific insights about **how the openrouter skill itself was used, what worked, what failed, or what corrections were applied to its usage**. The "Learning Effectiveness Check" entries show 0 corrections across all sessions, indicating no actual skill usage patterns to extract from.

- **2026-04-13:** anthropic/gemini-2.5-pro-preview model is unavailable or has routing issues — pixel cron jobs using this model fail with unknown model errors as of March 29, 2026.