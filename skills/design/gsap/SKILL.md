---
name: gsap
description: >
  GSAP (GreenSock Animation Platform) — professional JS animation library. Timelines, scroll triggers, text splitting,
  spring physics, SVG morphing. Industry gold standard for complex sequences and scroll-driven animations.
  Use whenever CSS transitions aren't enough — page transitions, scroll reveals, complex UI choreography.
---

# GSAP — Professional Animation Platform

## What It Is
GSAP is the animation backbone of the modern web. Used by NASA, Google, Apple, Awwwards sites. The most performant JS animation library — 20x faster than jQuery, handles CSS, SVG, Canvas, WebGL.

**Core strengths:**
- Timeline sequencing (chain animations with precision)
- ScrollTrigger (scroll-driven animations)
- SplitText (animate individual characters/words)
- Spring physics (natural, bouncy motion)
- SVG morphing
- Flip (animate layout changes smoothly)

## CDN (No Install)
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
```

## npm
```bash
npm install gsap
```
```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);
```

## Core API

### Basic Tween
```js
// from → to
gsap.from('.hero-title', { opacity: 0, y: 40, duration: 0.6, ease: 'power3.out' });
gsap.to('.card', { scale: 1.05, duration: 0.2, ease: 'power2.out' });
gsap.fromTo('.btn', { opacity: 0 }, { opacity: 1, duration: 0.4 });
```

### Timeline (sequence multiple animations)
```js
const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

tl.from('.nav', { y: -60, opacity: 0, duration: 0.5 })
  .from('.hero-title', { y: 40, opacity: 0, duration: 0.7 }, '-=0.2')
  .from('.hero-sub', { y: 30, opacity: 0, duration: 0.6 }, '-=0.4')
  .from('.hero-btn', { scale: 0.8, opacity: 0, duration: 0.4 }, '-=0.3')
  .from('.hero-cards', { y: 60, opacity: 0, stagger: 0.1, duration: 0.6 }, '-=0.2');
// '-=0.2' = start 0.2s before previous ends (overlap)
```

### Stagger (animate list items)
```js
gsap.from('.card', {
  opacity: 0, y: 30,
  duration: 0.5,
  stagger: { each: 0.08, from: 'start' }, // 80ms between each
  ease: 'power2.out'
});
```

### ScrollTrigger
```js
// Animate on scroll into view
gsap.from('.section-title', {
  opacity: 0, y: 50, duration: 0.8,
  scrollTrigger: {
    trigger: '.section-title',
    start: 'top 80%',    // when top of element hits 80% of viewport
    end: 'top 30%',
    toggleActions: 'play none none reverse',
  }
});

// Pinned scroll section (scroll story)
gsap.to('.panel', {
  xPercent: -100 * (panels.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '.container',
    pin: true,
    scrub: 1,  // smooth lag (seconds)
    snap: 1 / (panels.length - 1),
  }
});
```

### SplitText (animate characters)
```js
// Requires GSAP Club membership OR use split manually
const split = new SplitText('.headline', { type: 'chars,words' });

gsap.from(split.chars, {
  opacity: 0, y: 50, rotateX: -90,
  stagger: 0.02, duration: 0.5,
  ease: 'back.out(1.7)'
});

// Free alternative (manual split)
const text = 'Your headline';
el.innerHTML = text.split('').map(c => `<span>${c === ' ' ? '&nbsp;' : c}</span>`).join('');
gsap.from(el.querySelectorAll('span'), { opacity: 0, y: 20, stagger: 0.03, duration: 0.4 });
```

### Spring/Elastic Eases
```js
// Built-in elastic eases (no extra import)
gsap.to('.modal', { scale: 1, ease: 'elastic.out(1, 0.3)', duration: 0.8 });
gsap.to('.btn', { y: -4, ease: 'back.out(3)', duration: 0.3 });
// back.out = slight overshoot
// elastic.out = bouncy settle
// power3.out = snappy deceleration (most used)
```

### FLIP (animate layout changes)
```js
import { Flip } from 'gsap/Flip';
gsap.registerPlugin(Flip);

// Capture state before DOM change
const state = Flip.getState('.items');
// Make DOM change (reorder, resize, etc.)
container.appendChild(movedItem);
// Animate from old state to new
Flip.from(state, { duration: 0.5, ease: 'power2.inOut', stagger: 0.05 });
```

## Easing Reference (Most Used)
```
power1/2/3.out  → standard decelerate (power3.out is default choice)
power1/2/3.in   → accelerate (use for exits)
back.out(1.7)   → slight bounce overshoot
elastic.out(1, 0.3) → spring bounce
expo.out        → very fast start, long smooth settle
sine.inOut      → smooth wave (good for loops)
none / linear   → constant speed (use with scrub)
```

## Best Use Cases for Our Builds
- **Page transitions** — timeline sequences between routes
- **Dashboard load** — stagger cards in on mount
- **Hero sections** — headline character animation
- **Scroll reveals** — ScrollTrigger on every section
- **Calendar drag** — spring physics on drop
- **Office animations** — complex SVG choreography
- **Halo landing** — scroll story pinned sections

## Skill Injection for Codex/Claude Code
```
Use GSAP for all complex animations. CDN: cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js
ScrollTrigger for scroll-driven reveals. Timeline for sequenced entrance animations.
Stagger: 0.08s between items. Default ease: power3.out (enter), power3.in (exit).
SplitText alternative: manual span-wrap each character.
```


## Learned In Use

- **2026-03-15:** GSAP was used in the Three.js Agent Space build (Halo HQ) for animation orchestration alongside Three.js and OrbitControls for 3D sprite visualization.

## Learned from Use (2026-03-22)
SKIP

**Reason:** The session logs contain no mentions of actual `gsap` skill usage, errors, corrections, or outcomes. The logs discuss Vercel deployments, Three.js canvas rendering, UI builds, and Obsidian sync tasks—but no GSAP (GreenSock Animation Platform) interactions. Without evidence of how the skill was applied, what failed, or what succeeded, there are no actionable lessons to extract for a learned-from-use section.


## Learned from Use (2026-03-29)
SKIP

The session logs show no mentions of GSAP (GreenSock Animation Platform) being used, tested, or causing any corrections. The logs focus on typography fixes, font sizes, Clerk authentication UI, QA pipeline management, and agent coordination—but contain no references to GSAP animations or animation library implementation.

To extract genuine lessons about gsap usage, there would need to be evidence of:
- GSAP being applied to fix or build animations
- Animation-related corrections or failures
- Specific gotchas with GSAP in this codebase

None of these appear in the provided session logs.
