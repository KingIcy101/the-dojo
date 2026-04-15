---
name: framer-motion
description: >
  Framer Motion (now "Motion") — React animation library with physics-based springs, layout animations,
  gesture handling, and shared element transitions. Use for all React/Next.js builds.
  The React equivalent of GSAP — declarative, physics-first, zero boilerplate.
---

# Framer Motion (Motion) — React Animation

## What It Is
Framer Motion is the standard animation library for React in 2026. Rebranded to "Motion" but `framer-motion` package still works. Powers Aceternity UI, many shadcn components, and most React SaaS UIs.

**Why over CSS animations for React:**
- Layout animations (FLIP) built-in — `layout` prop
- Shared element transitions — `layoutId`
- Physics springs — natural, not robotic
- Gesture handling — drag, hover, tap with physics
- Exit animations — `AnimatePresence`

## Install
```bash
npm install framer-motion
# or new package name:
npm install motion
```

## Core API

### Basic Animation
```jsx
import { motion } from 'framer-motion';

// Fade in on mount
<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, ease: 'easeOut' }}>
  Content
</motion.div>

// Scale on hover + tap
<motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.97 }}
  transition={{ type: 'spring', stiffness: 400, damping: 17 }}>
  Click me
</motion.button>
```

### Spring Physics (most important)
```jsx
// Spring transition — replaces cubic-bezier
transition={{ type: 'spring', stiffness: 300, damping: 20 }}
// stiffness: how tight (100=loose, 500=snappy)
// damping: how bouncy (10=very bouncy, 30=no bounce)

// Common presets:
// Snappy button: stiffness: 400, damping: 17
// Gentle panel: stiffness: 200, damping: 25
// Bouncy modal: stiffness: 260, damping: 20
```

### Stagger Children
```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.08 }
  }
};
const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 300, damping: 24 } }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i.id} variants={item}>{i.name}</motion.li>
  ))}
</motion.ul>
```

### Exit Animations (AnimatePresence)
```jsx
import { AnimatePresence, motion } from 'framer-motion';

<AnimatePresence>
  {isOpen && (
    <motion.div key="modal"
      initial={{ opacity: 0, scale: 0.95, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95, y: 10 }}
      transition={{ type: 'spring', stiffness: 300, damping: 24 }}>
      Modal content
    </motion.div>
  )}
</AnimatePresence>
```

### Layout Animations (FLIP)
```jsx
// Animate reorder/resize automatically
<motion.div layout>
  {/* Content can change size — animates smoothly */}
</motion.div>

// Shared element transition (like magic move)
<motion.div layoutId="card-1">...</motion.div>
// On next screen:
<motion.div layoutId="card-1">...</motion.div>
// Same layoutId = animates between positions across renders
```

### Drag with Physics
```jsx
<motion.div
  drag="x"
  dragConstraints={{ left: -100, right: 100 }}
  dragElastic={0.1}
  whileDrag={{ scale: 1.05, boxShadow: '0 20px 60px rgba(0,0,0,0.3)' }}
>
  Draggable card
</motion.div>
```

### useAnimation (programmatic control)
```jsx
import { useAnimation } from 'framer-motion';
const controls = useAnimation();

// Trigger from event
await controls.start({ opacity: 1, y: 0, transition: { duration: 0.4 } });
controls.stop();

<motion.div animate={controls}>...</motion.div>
```

### useScroll + useTransform
```jsx
import { useScroll, useTransform } from 'framer-motion';

const { scrollYProgress } = useScroll();
const opacity = useTransform(scrollYProgress, [0, 0.3], [1, 0]);
const scale = useTransform(scrollYProgress, [0, 0.3], [1, 0.8]);

<motion.div style={{ opacity, scale }}>
  Fades out as you scroll
</motion.div>
```

## Best Use Cases for Our Builds
- **All React/Next.js builds** — default animation layer
- **Card grids** — stagger entrance
- **Modals/drawers** — AnimatePresence exit animations
- **Calendar events** — layout animations for drag/drop
- **Dashboard KPIs** — count-up with spring
- **AI agency client portal** — shared element transitions between pages

## Skill Injection for Codex/Claude Code
```
Use Framer Motion (framer-motion) for all React animations.
Default spring: { type: 'spring', stiffness: 300, damping: 24 }
AnimatePresence for exit animations on modals/toasts/routes.
layout prop for FLIP — auto-animates DOM reorder.
Stagger children: staggerChildren: 0.08 in parent variants.
```


## Learned from Use (2026-03-22)
SKIP

The session logs contain no meaningful mentions of framer-motion usage, decisions, or corrections. The framer-motion skill appears only in the header but is not actually discussed or applied anywhere in the session activity. All logged work focuses on Vercel deployment issues, Three.js canvas rendering, UI skeleton building, and Obsidian sync — none of which involve framer-motion-specific patterns, gotchas, or learning moments.


## Learned from Use (2026-03-29)
SKIP

The session logs contain no mentions of framer-motion being used, tested, corrected, or causing issues. The logs focus on typography fixes (font sizes), Clerk authentication theming, deployment pipeline corrections, and agent coordination—but do not reference framer-motion animations or motion library implementation at any point.

To extract learned lessons about framer-motion specifically, there would need to be session evidence of the skill being applied, debugged, or reviewed.


## Learned from Use (2026-04-05)
SKIP

The session logs provided contain no mentions of "framer-motion" being used, tested, corrected, or discussed. The logs focus on OpenClaw agent configuration, Gemini API setup, Discord integration, and Halo Portal deployment — but do not document any framer-motion skill applications or related corrections.

To extract actionable lessons about framer-motion usage, I would need session logs that actually contain framer-motion work, corrections, or interactions.
