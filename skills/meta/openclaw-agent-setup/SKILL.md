---
name: openclaw-agent-setup
description: Full 13-step OpenClaw agent build — workspace, identity files, skills, Discord, cron, and verification.
category: meta
---

# OpenClaw Agent Setup

## When to Use
Spinning up a new OpenClaw agent from scratch. Never skip Step 13 (verification).

## Model Selection
- **Judgment / orchestration:** claude-sonnet-4-6 (Anthropic)
- **Execution / long context:** Gemini 2.5 Pro

## 13 Steps

### Step 1 — Create Workspace
```bash
mkdir -p ~/.openclaw/agents/<agent-name>/workspace
mkdir -p ~/.openclaw/agents/<agent-name>/workspace/memory
```

### Step 2 — SOUL.md
Write identity file: who the agent is, tone, personality, self-review checklist.
Path: `workspace/SOUL.md`

### Step 3 — AGENTS.md
Mandatory startup sequence, memory rules, safety rules, heartbeat config.
Copy from main agent AGENTS.md and customize role-specific sections.
Path: `workspace/AGENTS.md`

### Step 4 — USER.md
Matt's profile, businesses, preferences.
Copy from main agent, keep unchanged.
Path: `workspace/USER.md`

### Step 5 — MEMORY.md
Initialize blank with headers: `## Key Facts`, `## Decisions`, `## Patterns`, `## Recently Saved`.
Path: `workspace/MEMORY.md`

### Step 6 — corrections.md
Initialize blank. This is where behavior corrections are logged.
Path: `workspace/memory/corrections.md`

### Step 7 — Copy Skills
```bash
cp -r ~/.openclaw/workspace/.agents/skills workspace/.agents/skills
```

### Step 8 — Brain Vault Lane
```bash
mkdir -p ~/brain/sessions/openclaw/<agent-name>
# Create initial context note
echo "# <Agent Name> — Initialized $(date)" > ~/brain/sessions/openclaw/<agent-name>/init.md
```

### Step 9 — Self-Learning Hook
Add weekly learning cron (Sunday 10pm ET):
```bash
# Reviews git history, extracts patterns, updates corrections.md
0 22 * * 0 cd /path/to/workspace && node scripts/weekly-learning.js
```

### Step 10 — Discord Bot Config
- Create webhook for agent's channel
- Add `DISCORD_WEBHOOK_<AGENT>` to .env
- Update discord-bot to route agent's messages to correct channel
- Set agent username and avatar URL in webhook calls

### Step 11 — Avatar Generation
- Generate 512x512 portrait via image model
- Upload to stable URL (GitHub raw / Cloudflare R2)
- Use in Discord webhook `avatar_url`

### Step 12 — Discord Channel Setup
```
#<agent-name>-updates  — agent's output channel
#<agent-name>-commands — slash command input (optional)
```
Pin agent description and avatar in channel.

### Step 13 — Verification (NEVER SKIP)
```bash
# Confirm all files exist
ls workspace/SOUL.md workspace/AGENTS.md workspace/USER.md workspace/MEMORY.md
ls workspace/memory/corrections.md
ls workspace/.agents/skills/

# Place a test message
# Agent should respond, reference SOUL.md, check MEMORY.md

# Confirm Discord webhook posts
curl -X POST $DISCORD_WEBHOOK_URL -H "Content-Type: application/json" \
  -d '{"content": "Agent online. Verification complete."}'
```

## Gotchas
- Skipping Step 13 = unknown if agent is actually functional
- Skills directory must be copied not symlinked — each agent needs its own copy
- `corrections.md` starts blank — don't pre-fill, let it grow from real sessions
- Brain vault lane = agent's long-term persistent memory across sessions
- Model selection matters: don't run Gemini for judgment calls — it's too agreeable
