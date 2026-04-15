# Agent Skills — The Dojo

Reusable skill files for OpenClaw AI agents. Every skill we build or discover goes here.

## Structure

```
skills/
  dev/        — Forge: Next.js, React, Supabase, Stripe, Vercel, testing
  design/     — Pixel: UI/UX, animation, typography, component libraries
  infra/      — Core: deploy, CI/CD, security, monitoring
  itp/        — ITP team: Vapi, intake, onboarding, voice agents
  sales/      — Dex: cold email, objection handling, Hormozi frameworks
  business/   — Mara/Iris/Scribe: retention, copywriting, content
  meta/       — Agent setup, memory systems, skill creation
docs/         — Reference material, playbooks, guides
```

## How Skills Work

A skill is a `SKILL.md` file that teaches an agent exactly how to perform a specific task. Drop it in an agent's `.agents/skills/` directory and OpenClaw surfaces it automatically when relevant.

Skills are Git-backed, versioned, and reviewed. Every breakthrough one person figures out becomes a baseline for everyone.

## Usage

Copy any skill folder into your agent's workspace:
```bash
cp -r skills/dev/nextjs ~/.openclaw/workspace-forge/.agents/skills/
```

Or sync all at once — see `scripts/sync.sh`

## Contributing

1. Build something. Figure out the best way to do it.
2. Package it as a `SKILL.md` — description, when to use, step-by-step.
3. Drop it in the right `skills/` subfolder.
4. Push. Everyone benefits.

---

Inspired by Ramp's Dojo. Built by the Zero to Agent team.
