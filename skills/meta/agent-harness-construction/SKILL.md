---
name: agent-harness-construction
description: Custom Claude Code agent harness — 35 tools, 6 phases, Judge scoring, Cyrus dispatcher, and cross-session memory.
category: meta
---

# Agent Harness Construction

## When to Use
Building or modifying the custom agent harness that wraps Claude Code with ITP-specific tools, multi-model routing, Judge scoring, and the Cyrus pipeline dispatcher.

## Architecture

```
35 tools across 6 phases:
  Phase 1: Core file ops (read, write, edit, exec, search)
  Phase 2: Multi-model routing (Claude, Gemini, GPT-4o)
  Phase 3: ITP-specific tools (Vapi, Supabase, Resend, PandaDoc)
  Phase 4: Pipeline (Pixel -> Forge -> Judge -> Core)
  Phase 5: Cyrus dispatcher
  Phase 6: LSP / MCP integrations
```

## Key Components

### Cyrus Dispatcher
```bash
node cyrus.js --pipeline "task description" --workdir /path/to/project
```
Routes tasks to correct agent based on task type:
- Design/UI → Pixel
- Build/code → Forge
- QA/review → Judge
- Orchestration → Core

### Pipeline Flow
```
Pixel  — visual/design decisions, mockup planning
Forge  — implementation, file writing, code execution
Judge  — scoring, review, IMPROVEMENTS list
Core   — orchestrates, reads Judge output, decides next step
```

### Judge Scoring
```js
// Judge returns:
{
  score: 0.87,          // 0.0 - 1.0
  pass: true,           // score >= 0.8 = pass
  improvements: [
    "Missing error handling in webhook handler",
    "Rate limiter doesn't persist across restarts",
  ],
  summary: "Strong implementation, minor gaps in resilience.",
}
// Core loops Forge until score >= 0.8 or 3 attempts
```

### program.md — Standing Instructions
```markdown
# program.md
Instructions that persist across agent sessions.
- Always run Judge before marking task complete
- Never commit .env files
- Always check pm2 status after restart
- Use service role for Supabase writes in pipeline
```

### AgentMemoryTool
```js
// Cross-session persistence — stores to Supabase
await agentMemory.save({ key: 'last_client_built', value: 'Sunrise Dental', ttl: 30 }); // days
const val = await agentMemory.get('last_client_built');
```

### SkillTool
```js
// Load a skill mid-build
const skill = await skillTool.load('vapi-agent-build');
// Returns full SKILL.md content injected into context
```

### Bash Validation (19 submodules)
```js
// Validates bash commands before execution
const result = await bashValidation.check('rm -rf /important/dir');
// Returns: { safe: false, reason: 'Destructive delete on important path' }
```

## Key Patterns / Code

### Multi-Model Routing
```js
const MODEL_MAP = {
  judgment: 'anthropic/claude-sonnet-4-6',
  execution: 'google/gemini-2.5-pro',
  fast: 'anthropic/claude-3-5-haiku-20241022',
};

async function routeToModel(task, type = 'execution') {
  const model = MODEL_MAP[type];
  return await llm.complete({ model, prompt: task });
}
```

### File: cyrus.js Entry Point
```js
const { Command } = require('commander');
const program = new Command();

program
  .option('--pipeline <task>', 'Task to run through pipeline')
  .option('--workdir <path>', 'Working directory')
  .option('--agent <name>', 'Force specific agent (pixel|forge|judge|core)')
  .parse(process.argv);

const opts = program.opts();
await runPipeline(opts.pipeline, opts.workdir, opts.agent);
```

## Gotchas
- Judge score threshold is 0.8 — below that, Forge retries with IMPROVEMENTS as context
- Max 3 Judge-Forge loops before escalating to Core for human review
- program.md is read at the start of every harness session — keep it concise (under 50 lines)
- AgentMemoryTool uses Supabase `agent_memory` table with `key`, `value`, `expires_at` columns
- SkillTool looks in `~/.openclaw/workspace/.agents/skills/` — skills must be synced there
- bash-validation's 19 submodules cover: file ops, network, git, package installs, process kills, env exposure, and 13 more
