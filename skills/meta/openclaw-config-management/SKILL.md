---
name: openclaw-config-management
description: Manage openclaw.json safely — valid keys, invalid patterns, bot token rules, and post-change verification.
category: meta
---

# OpenClaw Config Management

## When to Use
Any time you need to add or change openclaw.json settings — model selection, subagent permissions, workspace config.
Wrong keys silently break the gateway. Always verify after changes.

## Steps
1. Read current `openclaw.json` before editing
2. Check schema for valid keys (run `config.schema.lookup` or check docs)
3. Make minimal targeted edit
4. Run `openclaw gateway restart`
5. Verify all agents come back online

## Key Patterns / Code

### Valid Agent Config Keys
```json
{
  "agents": {
    "alo": {
      "workspace": "/Users/mattbender/.openclaw/workspace",
      "model": "anthropic/claude-sonnet-4-6",
      "subagents": {
        "allowAgents": ["forge", "pixel", "judge"]
      }
    }
  }
}
```

### INVALID — Breaks Gateway
```json
// ❌ Wrong nesting — this silently breaks the gateway
{
  "agents": {
    "defaults": {
      "subagents": {
        "allowAgents": ["forge"]  // INVALID path
      }
    }
  }
}

// ✅ Correct — agent-level, not defaults-level
{
  "agents": {
    "alo": {
      "subagents": { "allowAgents": ["forge"] }
    }
  }
}
```

### Post-Change Verification
```bash
openclaw gateway restart

# Wait 5 seconds, then verify
sleep 5
openclaw gateway status

# Check agents are online (should show all agents as connected)
```

### Bot Tokens — .env Only
```bash
# ✅ Correct — .env file only
DISCORD_BOT_TOKEN=MTQ4N...
TELEGRAM_BOT_TOKEN=7234...

# ❌ Never in openclaw.json
# ❌ Never in memory files (MEMORY.md, daily logs, etc.)
# ❌ Never committed to git
```

### Discord Bot Token Invalidation
If a Discord bot token stops working:
1. Go to discord.com/developers → Applications → [Bot] → Bot → Reset Token
2. Update in .env (NOT in openclaw.json)
3. `openclaw gateway restart`
4. Verify bot comes online in Discord server

### Common Config Edits
```json
// Change model for an agent
{ "agents": { "forge": { "model": "anthropic/claude-opus-4-5" } } }

// Restrict subagent spawning
{ "agents": { "alo": { "subagents": { "allowAgents": ["forge", "judge"] } } } }

// Change workspace path
{ "agents": { "pixel": { "workspace": "/Users/mattbender/.openclaw/workspace" } } }
```

## Gotchas
- `agents.defaults.*` path is INVALID — breaks gateway silently (no error, agents just don't load)
- Always run `openclaw gateway restart` after any config change — hot reload not supported
- If gateway crashes after edit, check logs: `openclaw gateway logs --tail 50`
- Bot tokens in openclaw.json = security risk (config may be logged or shared)
- Model strings must be exact — typo = agent falls back to default or fails