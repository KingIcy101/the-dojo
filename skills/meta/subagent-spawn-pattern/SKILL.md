---
name: subagent-spawn-pattern
description: How to spawn and manage subagents in OpenClaw — context injection, runtime modes, completion handling.
category: meta
---

# Subagent Spawn Pattern

## When to Use
Delegating coding, research, or long-running tasks without blocking the main session.
Subagents have ZERO context by default — always prepend SUBAGENT_BRIEF.md.

## Steps
1. Read SUBAGENT_BRIEF.md content
2. Prepend brief to task prompt
3. Spawn with `sessions_spawn` (runtime=subagent)
4. Choose mode: run (one-shot) or session (persistent)
5. Let completion auto-announce — don't poll
6. Always include Telegram notification in the task so Matt gets pinged on finish

## Key Patterns / Code

### Prepend Brief Pattern
```js
const brief = fs.readFileSync(
  '/Users/mattbender/.openclaw/workspace/SUBAGENT_BRIEF.md',
  'utf8'
);
const fullPrompt = `${brief}

---

${taskDescription}`;
```

### sessions_spawn (via OpenClaw MCP)
```js
// One-shot task (run mode)
await sessions_spawn({
  runtime: 'subagent',
  mode: 'run',
  task: fullPrompt,
  timeoutSeconds: 300,
});

// Persistent agent (session mode)
await sessions_spawn({
  runtime: 'subagent',
  mode: 'session',
  task: fullPrompt,
});
```

### streamTo NOT supported
```js
// ❌ This will fail
sessions_spawn({ runtime: 'subagent', streamTo: 'telegram' });

// ✅ Use delivery in task instead
// Include in task prompt: "Send Telegram notification when done"
```

### Completion is Push-Based
```
// ✅ Correct — fire and let it announce
spawn subagent → continue other work → subagent announces when done

// ❌ Wrong — busy polling
spawn subagent → subagents(list) every 30s → check status
```

### Telegram Notification (include in task prompt)
```bash
BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN /Users/mattbender/.openclaw/workspace/voice-server/.env | cut -d= -f2)
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"   -d chat_id=8465598242   -d "text=✅ [Task name] complete. [One line summary of what was done]."
```

### Kill a Subagent
```js
await subagents({ action: 'kill', target: 'subagent-session-id' });
```

### What to Include in Task Prompt
```
1. Full SUBAGENT_BRIEF.md contents
2. Specific task with all required context
3. File paths, API keys, credentials needed
4. Expected output format
5. Where to write results
6. Telegram notification command at the end
```

## Gotchas
- Subagents cannot access main session memory — all context must be in the prompt
- `streamTo` param is not supported for subagent runtime — use Telegram ping instead
- Mode `run` = one-shot, self-terminates after task. Mode `session` = stays alive for follow-up
- Don't spawn more than 3-4 concurrent subagents — memory/CPU pressure on Mac mini
- If subagent needs to write to workspace, give exact absolute paths
- Subagent depth limit: 1 (subagents cannot spawn sub-subagents)