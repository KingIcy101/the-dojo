---
name: rive
description: Rive — state-driven interactive animations. Better than Lottie for complex motion with logic. Used by Linear, Vercel, Stripe for hero sections and interactive product demos. Use when an animation needs to respond to user input or state changes.
---

# Rive — Interactive Animations

## When to Use
- Hero animations that respond to hover/click
- Product demos with interactive states
- Loading animations with multiple states
- Anything where Lottie would be "play and loop" but you need branching logic

## Install
```bash
npm install @rive-app/react-canvas
```

## Basic Usage
```tsx
import { useRive } from '@rive-app/react-canvas'

export function RiveAnimation() {
  const { RiveComponent } = useRive({
    src: '/animations/hero.riv',
    autoplay: true,
  })

  return <RiveComponent style={{ width: 500, height: 500 }} />
}
```

## With State Machine (interactive)
```tsx
import { useRive, useStateMachineInput } from '@rive-app/react-canvas'

export function InteractiveAnimation() {
  const { rive, RiveComponent } = useRive({
    src: '/animations/button.riv',
    stateMachines: 'State Machine 1',
    autoplay: true,
  })

  const isHover = useStateMachineInput(rive, 'State Machine 1', 'isHover')

  return (
    <RiveComponent
      onMouseEnter={() => isHover && (isHover.value = true)}
      onMouseLeave={() => isHover && (isHover.value = false)}
    />
  )
}
```

## Workflow
1. Designer creates animation in Rive editor (rive.app) — free
2. Export as .riv file
3. Drop in /public/animations/
4. Use @rive-app/react-canvas to embed

## Rules
- Use for hero sections that need "wow" factor
- Use for product feature demos with interactive states
- Don't use for simple CSS animations — overkill
- .riv files live in /public/animations/
- Canvas renderer is more performant than WebGL renderer for most cases


## Learned from Use (2026-03-22)
SKIP

The session logs contain no mentions of the "rive" skill being used. The logs document Vercel deployments, Forge build issues, Agent Lounge frontend work, and Obsidian sync tasks—but no activity involving the rive skill. Without actual usage data, I cannot extract lessons about what worked, what caused corrections, or patterns specific to rive skill application.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

• **Pipeline enforcement prevents cascading corrections** — Skipping Judge audit after Forge's fix pass led to Round 2 rejection (typography), then Round 3 (more typography), then Round 4 (Clerk styling). Running full Pixel → Forge → Judge cycle before any deployment eliminated rejection loops.

• **Agent coordination channel routing is load-bearing** — Posting dev syncs to Forge's private channel (#forge) instead of #dev-team-chat blocked cross-agent execution; Judge couldn't see work items and couldn't audit. Critical coordination must always route through #dev-team-chat (ID: 1484725229723844758).

• **Memory size ceiling is hard-blocking** — MEMORY.md at 45,920 chars (61% truncation) caused session start lag and lost context. Rule enforced: under 15KB essentials only; archive overflow to Vault and use memory_search for recall.

• **"Looks done" is the exact moment to audit, not deploy** — Portal appeared feature-complete after Forge's fix pass; deploying without Judge verification revealed security gaps (anon key exposure, rate limiting missing), auth gaps (Clerk Orgs), and rendering bugs. Completion triggers QA, not shipping.
