# Podhi gear map: gstack takeaways -> local skills

This is the concrete adaptation plan for Podhi. We keep the operating model, not the repo cosplay.

## Core decision

**Keep explicit gears. Do not copy gstack's install model, symlink setup, or Bun browser binary.**

Podhi already has:
- a persistent browser tool
- skill routing
- planning/review skills
- commit/push skills
- agent orchestration

So the right move is to map gstack's ideas onto our native stack.

## Mapping table

| gstack mode | Keep? | Podhi-native mapping | Why |
|---|---|---|---|
| `plan-ceo-review` | partial | `plan` + scope challenge in phase docs | we want the taste/risk challenge, not the interactive Claude-only wrapper |
| `plan-eng-review` | yes | `phase-gaps` | same job: architecture, gaps, tests, failure modes |
| `review` | yes | `phase-review` + `code-review` when needed | keep the paranoid review behavior |
| `browse` | yes, strongly | new `browse-qa` skill using OpenClaw browser tool | best gstack idea, adapted to our native browser runtime |
| `ship` | partial | `commit-work` + repo-specific ship path | keep release discipline, skip one-size-fits-all PR automation |
| `retro` | light | doctrine + learnings update after major runs | useful, but not a first blocker for build mode |

## Podhi command plan

### Canonical entrypoint

- `/build "<goal>"`

This remains the one command AR uses most often.

### Gear-aware usage

- `/build --gear plan "<goal>"`
- `/build --gear eng-review --phase docs/planning/phase-N`
- `/build --gear implement --phase docs/planning/phase-N`
- `/build --gear review --phase docs/planning/phase-N`
- `/build --gear browse-qa --url <target> --routes ...`
- `/build --gear ship`
- `/build --gear retro`

This gives us explicit modes without exploding the command surface.

## What not to copy from gstack

- project/user symlink install pattern
- Bun-compiled local browser binary
- Claude-specific `AskUserQuestion` interaction model
- assuming one repo's `ship` flow fits every project
- replacing our browser tool with a sidecar CLI

## What to keep aggressively

- explicit mode switching
- screenshot-driven browser QA
- treating review as distinct from implementation
- keeping ship/release steps separate from "figure out what to build"
- retro/learning as a real lane after large work

## Build chain after adaptation

```text
plan -> skill-oracle -> phase-gaps -> terminus-maximus -> phase-review/code-review -> browse-qa -> commit-work
```

This is the Podhi build chain. gstack was the spark, not the blueprint.
