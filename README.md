# The Dojo

The shared skill library for all OpenClaw AI agents.

Every skill is a markdown file an agent can load mid-task to get expert-level context on a tool, pattern, or workflow — without building from scratch.

---

## Structure

```
skills/
├── dev/          # Next.js, Supabase, Stripe, Vapi, Clerk, Vercel, PM2, etc.
├── design/       # Tailwind, shadcn, GSAP, Framer Motion, Three.js, UI/UX
├── business/     # CAO framework, ZTA, contracts, voice standards, pricing
├── sales/        # Hormozi suite, cold email, closing, leads, pricing, proof
├── itp/          # In The Past AI — Vapi, Bland AI, GHL
├── meta/         # Agent infra — setup, memory, heartbeat, cron, harness
├── infra/        # Deployment, monitoring, brain vault
└── ar-goatedskills/  # 460+ skills from Ar's goatedskills library
```

---

## Usage

Load a skill in any agent:
```bash
cat ~/.openclaw/workspace/.agents/skills/<name>/SKILL.md
```

Search the full index:
```bash
cat ~/.openclaw/workspace/.agents/skills-index.md | grep "keyword"
```

Add a new skill after a build:
```bash
bash ~/.openclaw/workspace/scripts/auto-skill.sh \
  --name "skill-name" \
  --category "dev|design|sales|business|itp|infra|meta" \
  --description "one sentence" \
  --content "$(cat /path/to/SKILL.md)"
```

Sync index to all agent workspaces:
```bash
python3 ~/.openclaw/workspace/scripts/rebuild-skills-index.py
```

---

## Auto-Learning

Daily cron (2am ET) reads the session log, detects novel patterns, generates SKILL.md files automatically, and pushes. No manual step needed.

---

Built for the OpenClaw agent stack — Forge, Pixel, Judge, Core, Dex, Mara, Iris, Scribe, Echo.
