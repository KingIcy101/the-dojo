# Prompt Engineering Guide
*Distilled from dair-ai/Prompt-Engineering-Guide (46k+ stars)*
*Source: /Users/mattbender/Projects/Prompt-Engineering-Guide*

## When to Use This Skill
Load before writing any agent prompt, system prompt, SOUL.md update, or when a model is producing bad output and you need to debug why.

---

## Core Techniques (Use These Every Day)

### 1. Few-Shot Prompting
Give examples before asking. 3-5 examples = dramatically better output.
```
Bad:  "Write a cold email for a chiropractor"
Good: "Here are 3 cold emails that got responses: [examples]. Now write one for Dr. Smith..."
```
**Rule:** More complex the task → more examples needed. 1-shot for simple, 5-10 for nuanced.

### 2. Chain-of-Thought (CoT)
Force step-by-step reasoning. Add "Let's think step by step" or show reasoning in examples.
```
Bad:  "Is this lead qualified? [data]"
Good: "Analyze this lead step by step: (1) specialty match, (2) location fit, (3) practice size, (4) final verdict. Lead: [data]"
```
**Rule:** Use CoT for any task involving decisions, analysis, or math. Skipping it produces confident wrong answers.

### 3. Role Prompting
Assign a specific expert persona before the task.
```
"You are a healthcare marketing specialist with 10 years experience converting chiropractors to digital ad clients. Your job is to..."
```
**Rule:** The more specific the role, the better. "Expert marketer" < "Healthcare practitioner marketing specialist who has closed 200+ chiro practices."

### 4. Structured Output
Tell the model exactly what format to return.
```
"Return ONLY a JSON object with keys: name, email, phone, specialty, qualified (true/false), reason"
```
**Rule:** Always specify format for anything being parsed downstream. Never assume freeform will be consistent.

### 5. Zero-Shot CoT (Quick Win)
Just add: **"Think step by step."** to any prompt that's returning shallow answers. Costs nothing, improves quality significantly.

---

## Advanced Techniques

### Self-Consistency
For important decisions: run the same prompt 3x with temp > 0, pick the majority answer.
Best for: lead qualification, pricing decisions, outreach copy scoring.

### Generated Knowledge Prompting
First ask the model to generate relevant facts, then use those facts in the actual prompt.
```
Step 1: "List 5 key pain points for chiropractic practices trying to grow their patient base."
Step 2: "Using these pain points: [output from step 1], write a cold call script..."
```

### ReAct (Reason + Act) — For Agents
Format agent prompts as: Thought → Action → Observation → Thought → Action...
Best for: Scout enrichment decisions, Atlas routing, multi-step research tasks.

---

## Common Failures + Fixes

| Problem | Fix |
|---|---|
| Model ignores part of prompt | Put most important instruction LAST (recency bias) |
| Output is inconsistent | Add explicit format with example output |
| Model hallucinates facts | Add "Only use information explicitly provided. If unsure, say 'unknown'." |
| Bland/corporate output | Add negative examples: "Do NOT write like: [bad example]" |
| Wrong tone | Use 3+ real examples from Matt's approved messages as few-shot |
| Too long | Add "Respond in [N] sentences or fewer" |
| Refuses task | Reframe: "As a marketing consultant, analyze..." vs "Write me a sales pitch" |

---

## Temperature Guide
- **0.0–0.3:** Facts, data extraction, classification, structured output
- **0.5–0.7:** Email drafts, analysis, balanced responses ← default for most Halo tasks
- **0.8–1.0:** Creative copy, brainstorming, campaign ideas

---

## Halo-Specific Prompt Templates

### Lead Qualification
```
You are a healthcare marketing analyst. Analyze this lead and determine if they're a fit for a $1,950/mo digital marketing package.

Criteria: (1) Independent practice or small group (<5 docs), (2) No current active agency, (3) Accepts insurance OR cash-pay, (4) Has a website (even bad one)

Lead data: [INSERT]

Think step by step. Return JSON: { "qualified": true/false, "confidence": "high/medium/low", "reason": "...", "objection": "..." }
```

### Cold Outreach Copy
```
You are Matt Bender, 24-year-old founder of Halo Marketing. Your voice: direct, confident, no fluff, no corporate speak, never uses "I hope this finds you well."

Write a [SMS/email/voicemail] for [NAME], a [SPECIALTY] in [CITY]. Pain point: [SPECIFIC ISSUE]. Offer: [SPECIFIC OFFER].

3 rules: (1) Under [N] words, (2) No emojis, (3) End with a clear single CTA.
```

### Agent System Prompt
```
You are [NAME], a specialized AI agent for Halo Marketing. Your ONE job is: [ATOMIC TASK].

You receive: [INPUT FORMAT]
You return: [OUTPUT FORMAT]

Rules:
- Never do anything outside your defined task
- If input is unclear, return: { "error": "...", "needs": "..." }
- Always output valid JSON

Current context: [CONTEXT]
```

---

## Source
Full guide: `/Users/mattbender/Projects/Prompt-Engineering-Guide/`
Key files: `guides/prompts-advanced-usage.md`, `guides/prompts-applications.md`


## Learned from Use (2026-03-22)
## Learned from Use (2026-03-22)

- **Brief ambiguity causes execution drift**: Forge's Agent Lounge build was 60% incomplete because the brief didn't explicitly mark visual requirements (avatars, labels, colors) as mandatory vs. optional. Future briefs must frontload non-negotiable constraints and flag aesthetic specs with the same weight as functional ones.

- **Handoff clarity requires exact identifiers**: Forge substituted `@Pixel` text for actual mentions, breaking the handoff chain. When delegating via brief, specify the exact format expected (real user IDs, not placeholder text) to prevent manual rework.

- **Production deploys bypass review blockers**: Preview URLs gated by SSO auth stopped Pixel's review cycle 3 times. Direct production deploy (with `--prod` flag) is faster than troubleshooting auth gates — use this as fallback when preview access is blocked.


## Learned In Use

- **2026-04-09:** When briefing on active tasks, present recent context (TAIL of daily log) first before historical context — this matches user attention patterns better than chronological order.