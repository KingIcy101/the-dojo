---
name: lenis
description: Lenis — buttery smooth scroll library. Makes scrolling feel premium vs cheap. Use on every marketing site and landing page. Pairs with GSAP ScrollTrigger. Without it, scroll feels like a WordPress site.
---

# Lenis — Smooth Scroll

## Install
```bash
npm install lenis
```

## Basic Setup (Next.js App Router)
```tsx
// app/providers.tsx
'use client'
import Lenis from 'lenis'
import { useEffect } from 'react'

export function SmoothScroll({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    })

    function raf(time: number) {
      lenis.raf(time)
      requestAnimationFrame(raf)
    }
    requestAnimationFrame(raf)

    return () => lenis.destroy()
  }, [])

  return <>{children}</>
}
```

## With GSAP ScrollTrigger
```tsx
useEffect(() => {
  const lenis = new Lenis()

  lenis.on('scroll', ScrollTrigger.update)

  gsap.ticker.add((time) => {
    lenis.raf(time * 1000)
  })
  gsap.ticker.lagSmoothing(0)
}, [])
```

## Key Config Options
```ts
new Lenis({
  duration: 1.2,        // scroll duration (higher = slower/smoother)
  easing: (t) => ...,   // custom easing function
  smoothWheel: true,    // smooth mouse wheel
  smoothTouch: false,   // disable on touch (native feels better)
  infinite: false,      // infinite scroll
})
```

## Rules
- Always use on marketing sites + landing pages
- Disable on touch devices (`smoothTouch: false`) — native scroll feels better on mobile
- Pairs with GSAP ScrollTrigger — always wire together when using both
- Don't use on dashboards/apps — only scroll-narrative sites


## Learned from Use (2026-03-22)
SKIP

The session logs contain no mentions of the "lenis" skill being used, tested, or corrected. The logs document deployment issues, build problems, and task management related to Agent Lounge, Vercel, Forge, and Obsidian—but do not reference "lenis" at all. Without evidence of lenis skill usage or corrections, no learned lessons can be extracted for this skill.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Pipeline enforcement beats visual confidence**: Deployed Portal v1 assuming it was "done" after Forge's fix pass, skipping Judge audit. Judge found 3 font violations in round 2 that weren't caught. Every stage (Pixel → Forge → Pixel review → Judge → Core) catches different failure classes — skipping any one creates rework cycles.

- **Memory truncation breaks agent continuity**: MEMORY.md ballooned to 61% truncation due to duplicate Vera voice settings. Session restart loses critical context mid-build. Rule discovered: keep MEMORY.md under 15KB essentials-only; archive to Vault; use memory_search for recall to avoid losing coordination state during long sessions.

- **Communication channel routing is execution-blocking**: Posted pipeline sync to Forge's private channel (#forge) instead of #dev-team-chat. Judge couldn't execute audits because Discord messages in private channels don't trigger OpenClaw agent turns with tools — only #dev-team-chat messages do. Cross-agent coordination must always route through #dev-team-chat (ID: 1484725229723844758), not agent private channels.

- **Dark theme prop leakage creates silent UI breaks**: Clerk dark theme cascaded into the sign-in component despite being in light mode context. Fix required explicit `appearance` prop override in ClerkProvider. Check for theme inheritance side effects whenever third-party auth UI is customized.
