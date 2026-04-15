# GSD (Get Shit Done) — Meta-Prompting & Spec-Driven Development

## What It Is
GSD is a meta-prompting, context engineering, and spec-driven development system for Claude Code by TÂCHES. It forces a planning-first approach before writing any code — you define a spec, GSD validates it, then Claude executes against it.

## When to Use
- Starting a new feature or app build (forces proper spec before coding)
- Complex multi-file refactors where direction matters
- Any time Codex keeps going off-track (GSD keeps it on-rails)
- Building repeatable dev workflows

## Install
```bash
npx get-shit-done-cc
```

Or globally:
```bash
npm install -g get-shit-done-cc
```

## How It Works
1. **Spec phase** — GSD asks you to define what you're building, why, and success criteria before touching code
2. **Context engineering** — automatically loads relevant files and context into Claude's window
3. **Execution** — Claude codes against the spec, not vibes
4. **Validation** — checks output against defined success criteria

## Core Workflow
```bash
# Start a new task with GSD
npx get-shit-done-cc "Build a to-do list component for the AI Agency page"

# GSD will prompt:
# - What is the task?
# - What does done look like?
# - What files are relevant?
# Then passes structured context to Claude Code
```

## Why It Matters
Without GSD, Claude Code drifts — especially on large codebases. GSD is essentially a forcing function for the BRIEF.md pattern we already use, but automated and enforced at the tool level.

## Halo/AI Agency Use Cases
- Starting any new portal feature (forces scope before code)
- Agent pipeline builds where order of operations matters
- Onboarding Codex to an existing codebase faster

## Notes
- Works with Claude Code (claude) — not just any LLM
- The spec it generates is reusable across sessions
- Pairs well with BRIEF.md pattern already in use
- v1.0.1 as of March 2026
