---
name: magic-ui
description: >
  Magic UI — open source animated component library. Shimmer buttons, animated gradients, number tickers,
  particle fields, meteor effects, typing animations. Mix into any codebase. Stack with Aceternity UI.
  Use for dashboard animations, landing pages, interactive data displays.
---

# Magic UI — Animated Effect Components

## What It Is
Magic UI (magicui.design) is the open-source companion to Aceternity UI. Where Aceternity does dramatic full-section effects, Magic UI does component-level polish — the shimmer on a button, the ticker on a number, the particle field in the background.

**Key effects:**
- Shimmer/shine buttons
- Animated number counter
- Typing animation (typewriter)
- Meteor shower background
- Particle system (canvas-based)
- Marquee (infinite scroll ticker)
- Animated gradient border
- Ripple effect
- Retro grid background
- Globe (interactive 3D globe)

## Installation
```bash
npm install framer-motion clsx tailwind-merge
# Then copy components from magicui.design
```

## Key Components & Code

### Shimmer Button
```jsx
// Gives any button a moving light sheen
.shimmer-button {
  background: linear-gradient(
    110deg, #000103 45%, #1e2631 55%, #000103
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s linear infinite;
}
@keyframes shimmer {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}
```

### Animated Number Counter
```jsx
import { NumberTicker } from "@/components/magicui/number-ticker";

// Counts up from 0 to value on mount
<NumberTicker value={1950} className="text-4xl font-bold" />
// Perfect for: MRR display, lead counts, KPI cards
```

### Typewriter / Typing Animation
```jsx
import { TypingAnimation } from "@/components/magicui/typing-animation";
<TypingAnimation className="text-2xl font-bold" duration={100}>
  Built for healthcare growth.
</TypingAnimation>
```

### Marquee (Infinite Ticker)
```jsx
import Marquee from "@/components/magicui/marquee";
<Marquee pauseOnHover className="[--duration:20s]">
  {clients.map(client => <ClientCard key={client.name} {...client} />)}
</Marquee>
// Use for: client logos, testimonials, feature lists
```

### Meteor Shower
```jsx
import { Meteors } from "@/components/magicui/meteors";
<div className="relative overflow-hidden">
  <Meteors number={20} />
  <div className="relative z-10">Content</div>
</div>
```

### Particle Field (Canvas)
```js
// Vanilla JS version
function initParticles(canvas) {
  const ctx = canvas.getContext('2d');
  const particles = Array.from({length: 80}, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.5,
    vy: (Math.random() - 0.5) * 0.5,
    r: Math.random() * 2 + 1,
    alpha: Math.random() * 0.5 + 0.1,
  }));

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(99,102,241,${p.alpha})`;
      ctx.fill();
    });
    // Draw connections
    particles.forEach((a, i) => {
      particles.slice(i+1).forEach(b => {
        const dist = Math.hypot(a.x-b.x, a.y-b.y);
        if (dist < 100) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(99,102,241,${0.15 * (1 - dist/100)})`;
          ctx.stroke();
        }
      });
    });
    requestAnimationFrame(draw);
  }
  draw();
}
```

### Animated Gradient Border
```css
.gradient-border {
  position: relative;
  border-radius: 12px;
  background: var(--bg-card);
}
.gradient-border::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: 13px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899, #6366f1);
  background-size: 300% 300%;
  animation: gradient-spin 4s linear infinite;
  z-index: -1;
}
@keyframes gradient-spin {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

### Retro Grid Background
```css
.retro-grid {
  background-image:
    linear-gradient(rgba(99,102,241,0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99,102,241,0.08) 1px, transparent 1px);
  background-size: 40px 40px;
}
```

## Best Use Cases for Our Builds
- **Mission Control KPIs** — NumberTicker for MRR, lead counts
- **Halo landing** — Marquee for client logos, Shimmer CTA button
- **Dashboard cards** — Gradient border on featured cards
- **Agent office** — Particle field background
- **AI agency site** — Globe component, Meteor shower hero

## Skill Injection for Codex/Claude Code
```
Use Magic UI (magicui.design) for component-level animations.
Key: NumberTicker for KPIs, Marquee for logos/testimonials, Shimmer buttons for CTAs.
Vanilla: gradient-border animation, retro-grid background, particle field canvas.
Stack with Aceternity UI for full-page + component-level coverage.
```


## Learned from Use (2026-03-22)
SKIP

The session logs contain no meaningful usage of the "magic-ui" skill itself. The mentions are contextual only (Agent Lounge is *built with* magic-ui components, but the logs document deployment, auth, canvas rendering, and Forge build issues—not how magic-ui was actually applied, configured, or what worked/failed about using it specifically).

To extract genuine lessons about the magic-ui skill, I'd need logs showing:
- Component selection decisions
- Configuration or customization attempts
- Issues with specific magic-ui components
- Corrections to how magic-ui was integrated

None of these appear in the provided session data.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Font size enforcement needs grep verification, not visual spot-checks** — Judge caught 12px violations in typography that passed initial review; Forge later fixed all remaining instances via grep search across the codebase. Always grep the constraint (e.g., `grep -r "12px"`) after component updates rather than relying on manual audit.

- **Clerk's `appearance` prop overrides dark theme bleed** — Sign-in UI inherited dark theme from ClerkProvider wrapper and broke readability; fixed via explicit `appearance` prop on ClerkProvider to enforce white background + dark text + amber button. Document this when integrating Clerk into themed portals.

- **Magic-UI component violations compound across related components** — outcome-badge.tsx, calls-bar-chart.tsx, and chart tooltip all had the same 12px font issue in a single round. When one violation is found, search for the same pattern in sibling/related components (badges, charts, tooltips) before redeployment.
