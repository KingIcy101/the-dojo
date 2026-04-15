---
name: ui-ux-pro-max
description: >
  Master UI/UX design system for all visual builds — dashboards, web apps, landing pages, calendars, office visualizations.
  Load this skill before ANY frontend/UI build. Covers: dark design systems, motion/animation, glassmorphism, competitor research,
  typography, spacing, component patterns, and the philosophy that makes UIs feel expensive.
---

# UI/UX Pro Max — Master Design Skill

Load this before every UI build. This is the accumulated design intelligence from every session.

---

## The Philosophy (Read First)

**Cheap UI feels like a template. Expensive UI feels inevitable.**

The difference:
- Cheap: uniform spacing, flat color, no depth, no motion, no state feedback
- Expensive: deliberate rhythm, layered depth, purposeful motion, every interaction responds

**10-Point Checklist Before Shipping Any UI:**
1. Does every interactive element have a hover AND active state?
2. Is there visual hierarchy — does the eye know where to go first?
3. Are transitions smooth (200–400ms, ease-out for enter, ease-in for exit)?
4. Does it work at 375px mobile width?
5. Is every font size ≥11px labels, ≥13px body, ≥14px inputs?
6. Zero emojis in UI chrome (titles, badges, status labels, headers)
7. Are loading/empty states handled gracefully?
8. Does dark mode have proper contrast (not just inverted light mode)?
9. Are field names pulling from real API shape — not assumed?
10. After any restart — does the "now" state reflect real data?

---

## Design System — Core Variables

### Color Tokens (Dark Theme — Matt's Standard)
```css
:root {
  --bg-primary: #0a0a0f;
  --bg-secondary: #0f0f1a;
  --bg-card: #12121e;
  --bg-elevated: #1a1a2e;
  --border: rgba(255,255,255,0.06);
  --border-active: rgba(255,255,255,0.12);
  --text: #e8e8f0;
  --t2: #8888a8;
  --t3: #555570;
  --accent: #6366f1;        /* Indigo — Halo primary */
  --accent-glow: rgba(99,102,241,0.15);
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --surface-blur: blur(24px);
}
```

### Industry Color Themes (AI Agency)
```
Healthcare   → #10b981 (emerald)
Legal        → #d97706 (gold)
Home Services → #f97316 (orange)
Finance      → #3b82f6 (blue)
Real Estate  → #8b5cf6 (violet)
Fitness      → #ec4899 (pink)
Education    → #06b6d4 (cyan)
Restaurant   → #ef4444 (red)
```

---

## Typography

```css
/* Scale */
--text-xs: 11px;    /* labels, tags, meta */
--text-sm: 13px;    /* secondary body, captions */
--text-base: 14px;  /* primary body, inputs, buttons */
--text-lg: 16px;    /* card titles */
--text-xl: 20px;    /* section headers */
--text-2xl: 28px;   /* page titles, KPI numbers */
--text-3xl: 36px+;  /* hero numbers */

/* Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Letter spacing */
/* Labels/caps: 0.06em tracking */
/* Body: -0.01em (slightly tight) */
/* Hero numbers: -0.03em (tight) */

/* Font stack (no Google Fonts needed) */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
/* Mono */
font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
```

---

## Spacing Rhythm

Use 4px base grid. Common values:
```
4px  — icon gap, tight inline
8px  — compact padding
12px — card inner padding (small)
16px — standard padding
20px — card padding
24px — section gap
32px — major section break
48px — page-level spacing
```

**Consistency rule:** If you used 16px gap in one card row, use 16px everywhere. Never mix 14px and 16px gaps on the same component.

---

## Component Patterns

### Cards
```css
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  transition: border-color 200ms ease, box-shadow 200ms ease;
}
.card:hover {
  border-color: var(--border-active);
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
```

### Glassmorphism (Premium Panels)
```css
.glass {
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
}
/* Colored top accent border */
.glass-accent {
  border-top: 2px solid var(--accent);
}
```

### Squircle Icons (iOS-style agent/app icons)
```css
.squircle {
  width: 40px; height: 40px;
  border-radius: 30% 30% 30% 30% / 30% 30% 30% 30%;
  /* Or use SVG clip-path for true squircle */
  background: linear-gradient(135deg, var(--color-a), var(--color-b));
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 13px; letter-spacing: 0.02em;
}
```

### Buttons
```css
.btn-primary {
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px; font-weight: 500;
  cursor: pointer;
  transition: opacity 150ms, transform 100ms;
}
.btn-primary:hover { opacity: 0.9; }
.btn-primary:active { transform: scale(0.98); }

.btn-ghost {
  background: transparent;
  color: var(--t2);
  border: 1px solid var(--border);
  /* same sizing */
}
.btn-ghost:hover { background: rgba(255,255,255,0.04); color: var(--text); }
```

### Inputs
```css
.input {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px; color: var(--text);
  transition: border-color 150ms;
  outline: none;
  width: 100%;
}
.input:focus { border-color: var(--accent); }
.input::placeholder { color: var(--t3); }
```

### Badges / Status Pills
```css
.badge {
  display: inline-flex; align-items: center;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 11px; font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.badge-green  { background: rgba(16,185,129,0.15); color: #10b981; }
.badge-yellow { background: rgba(245,158,11,0.15);  color: #f59e0b; }
.badge-red    { background: rgba(239,68,68,0.15);   color: #ef4444; }
.badge-blue   { background: rgba(99,102,241,0.15);  color: #818cf8; }
```

---

## Motion & Animation

### Golden Rules
1. **Enter:** ease-out (fast start, slow settle) — things arriving feel weightless
2. **Exit:** ease-in (slow start, fast exit) — things leaving feel intentional
3. **Duration:** 150ms micro, 200ms standard, 300-400ms complex, 600ms+ only for dramatic reveals
4. **Never animate:** color, font-size, border-radius alone (always pair with transform/opacity)

### Spring Physics Pattern (premium feel)
```css
/* CSS approximation */
transition: transform 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
/* Bouncy overshoot — use for: modals, drawers, tooltips */

/* Snappy settle */
transition: transform 300ms cubic-bezier(0.16, 1, 0.3, 1);
/* Use for: dropdowns, panel slides */
```

### Keyframe Library
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(20px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0); }
  50%       { box-shadow: 0 0 16px 4px rgba(99,102,241,0.3); }
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}
/* Shimmer usage — skeleton loaders */
background: linear-gradient(90deg, var(--bg-card) 25%, var(--bg-elevated) 50%, var(--bg-card) 75%);
background-size: 200% 100%;
animation: shimmer 1.5s infinite;
```

### Staggered List Entrance
```js
// Stagger children by 40ms each
items.forEach((el, i) => {
  el.style.animationDelay = `${i * 40}ms`;
  el.classList.add('fade-in');
});
```

### Drag & Drop (Premium Feel)
```js
// Ghost element — elevated, semi-transparent, cursor-tracking
const ghost = el.cloneNode(true);
ghost.style.cssText = `
  position: fixed; pointer-events: none; z-index: 9999;
  opacity: 0.85; transform: scale(1.03) rotate(1deg);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  transition: transform 150ms, box-shadow 150ms;
`;
// Show live time label on ghost during drag
// Snap to 15-min grid intervals
// Drop zone: dashed border + accent color flash on enter
```

---

## Canvas / WebGL Patterns

### Particle System
```js
// Use requestAnimationFrame — never setInterval
function tick() {
  ctx.clearRect(0, 0, W, H);
  particles.forEach(p => {
    p.x += p.vx; p.y += p.vy; p.life -= 0.02;
    ctx.globalAlpha = p.life;
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fill();
  });
  particles = particles.filter(p => p.life > 0);
  if (particles.length) requestAnimationFrame(tick);
  else ctx.clearRect(0, 0, W, H); // cleanup!
}
```

### Glow Effects on Canvas
```js
ctx.shadowBlur = 20;
ctx.shadowColor = 'rgba(99,102,241,0.8)';
// Always reset after:
ctx.shadowBlur = 0;
```

---

## SVG Illustration Techniques

### Depth & Perspective
- Foreground: full opacity, sharp edges, brighter colors
- Midground: 85% opacity, slight blur
- Background: 60-70% opacity, lighter/hazier

### Organic Curves
```svg
<!-- Use cubic bezier paths for furniture, walls, organic shapes -->
<path d="M x1,y1 C cx1,cy1 cx2,cy2 x2,y2" />
<!-- Never use straight lines for soft objects (sofas, plants, rugs) -->
```

### Lighting Tricks
```svg
<!-- Radial gradient for light sources -->
<radialGradient id="lamp">
  <stop offset="0%" stop-color="#fff8e0" stop-opacity="0.4"/>
  <stop offset="100%" stop-color="#fff8e0" stop-opacity="0"/>
</radialGradient>
<!-- Ellipse on floor = cast shadow -->
<ellipse cx="cx" cy="cy" rx="40" ry="8" fill="rgba(0,0,0,0.2)"/>
```

### Plant Technique
```svg
<!-- Stem: curved path -->
<!-- Leaves: multiple rotated ellipses with gradient fills -->
<!-- Add slight randomness to leaf sizes for organic feel -->
```

---

## Competitor Intelligence

### What They Do Well
| App | Strength |
|-----|----------|
| Linear | Micro-animations, keyboard-first, instant feedback |
| Cron/Notion Calendar | Natural language input, clean week grid |
| Akiflow | Drag from backlog to calendar, unlimited color picker |
| Fantastical | Natural language, smart event detection |
| Amie | Friendship-layer social context, joyful interactions |
| Motion | AI auto-scheduling, priority-based rescheduling |
| Reclaim | Habit blocks, meeting defense time |

### Market Gaps (Exploit These)
1. **Intelligence over features** — no calendar knows your work. Ours should.
2. **Offline + sync** — competitors break without internet
3. **Per-event time tracking** — nobody does this cleanly
4. **Task backlog unscheduled view** — missing from most
5. **Real delegation dispatch** — not just "share this"
6. **Meeting vs Event visual distinction** — meetings need glow/shimmer

---

## Mobile Responsiveness

### Breakpoints
```css
/* Mobile first */
@media (max-width: 900px) { /* catches WebView/tablet too */ }
@media (max-width: 600px) { /* phone */ }
```

### Mobile Rules
- Sidebar: `display: none` on mobile (NOT just hidden — iOS WebView needs `display:none`)
- Also add JS `body.is-mobile` class as fallback: `if (window.innerWidth <= 900) document.body.classList.add('is-mobile')`
- Grids: 2/3/4-col → 1-col on mobile
- Topbar: hide clock/status/secondary widgets; keep core nav
- Pomo/overlays: become bottom sheets on mobile
- Touch targets: minimum 44×44px

---

## Anti-Patterns (Never Do These)

| ❌ Don't | ✅ Do Instead |
|---------|--------------|
| Emojis in UI chrome | Text, icons, or Lucide SVGs |
| `animation: none` for state changes | Even 150ms opacity helps |
| Hardcoded pixel widths for text containers | `max-width` + `word-break: break-word` |
| `color: white` on dark bg | `color: var(--text)` for adaptability |
| `font-size: 10px` for labels | Min 11px — anything smaller = unreadable |
| `overflow: hidden` on scrollable containers | Check if content gets clipped first |
| Fake/seed data in production UI | Live API or clear "no data" empty state |
| Blocking the main thread in animation | `requestAnimationFrame`, `will-change: transform` |
| Multiple shadows with `box-shadow` stacked 5 deep | Max 2 shadows; use `filter: drop-shadow` for SVG |
| `!important` everywhere | Fix specificity properly |

---

## Mandatory Skill Stack — Load These Together

**Every UI build = this skill + the following. No exceptions.**

| Skill | When | What It Adds |
|-------|------|-------------|
| `gsap` | Always | Scroll reveals, timelines, text animation, stagger |
| `aceternity-ui` | Always | Spotlight cards, aurora bg, beams, 3D tilt, bento grid |
| `magic-ui` | Always | NumberTicker, shimmer buttons, marquee, particle fields |
| `rive` | Interactive elements | State-machine animations — buttons, loaders, characters |
| `spline` | Hero sections / 3D | 3D backgrounds, product showcases, physics |
| `framer-motion` | React/Next.js builds | Spring physics, layout animations, exit animations |
| `stitch` | Pre-build | Prototype layout in 5min before briefing Codex |
| `openai-figma` | Has Figma mockup | Pull design context into brief |
| `luma-ai` | Needs video | Cinematic video generation for marketing |
| `coding-agent` | Always | Launch Codex/Claude Code with all skills injected |

### Pre-Build Checklist (Run Every Time)
```
□ Open Stitch → prototype layout (5 min)
□ Read: ui-ux-pro-max + gsap + aceternity-ui + magic-ui
□ If React: add framer-motion
□ If 3D hero: add spline
□ If interactive animation: add rive
□ Inject all into CLAUDE.md before Codex launch
□ Brief includes: design tokens, animation patterns, component library refs
```

### CLAUDE.md Injection Template
Before any Codex/Claude Code build, prepend to the project's CLAUDE.md:
```markdown
## Design System (Alo — ui-ux-pro-max stack)

**Dark theme tokens:** --bg-primary: #0a0a0f | --accent: #6366f1 | --text: #e8e8f0
**Typography:** min 11px labels, 13px body, 14px inputs. -apple-system font stack.
**Spacing:** 4px base grid. Card padding: 20px. Section gap: 24-32px.
**Animations:** GSAP for sequences/scroll. Framer Motion for React. Rive for interactive.
**Effects:** Aceternity UI spotlight/aurora/beams. Magic UI shimmer/ticker/marquee.
**3D:** Spline for hero sections (no Three.js needed).
**Rules:** Zero emojis in UI chrome. Hover + active states on everything. 900px mobile breakpoint.
**Self-review:** Run 10-point checklist before shipping.
```

## Plugging This Skill Into Codex / Claude Code

When launching either agent for a UI build, Alo will:
1. Read this SKILL.md
2. Inject the relevant sections into the project's `CLAUDE.md`
3. Include the brief + skill context in the agent's opening prompt

**CLAUDE.md injection template:**
```markdown
## Design System (Injected from ui-ux-pro-max skill)

[paste relevant sections here based on task type]
```

**Priority injections by task type:**
- Dashboard → Core Variables + Cards + Typography + Anti-Patterns
- Calendar → Motion + Drag & Drop + Mobile + Competitor Intel
- Landing page → Glassmorphism + Animation keyframes + Typography
- Office/SVG → SVG Techniques + Canvas Patterns + Philosophy
- All builds → Anti-Patterns checklist (always)

---

## Quick Reference — Before Any UI Build

```
□ Dark theme variables set (--bg-primary, --accent, etc.)
□ Typography scale established (min 11/13/14px)
□ 4px spacing grid
□ Hover + active states on all interactive elements
□ Transitions: 150-300ms, ease-out enter / ease-in exit
□ Mobile breakpoint at 900px
□ Zero emojis in chrome
□ Empty states handled
□ Real data — not hardcoded seeds
□ Self-review checklist before shipping
```


## Learned from Use (2026-03-22)
## Learned from Use (2026-03-22)

- **Visual requirements must be explicit and mandatory in briefs** — Forge built a structurally correct skeleton UI but missed avatars, labels, and styling because the brief didn't emphasize these weren't optional. When handing UI work off, separate "structural correctness" from "visual completeness" clearly in the spec.

- **Auth-gated preview URLs block handoffs** — Vercel's SSO protection on preview URLs forced 3 review cycles to fail before Matt deployed to production. For UI review handoffs (especially with Pixel), deploy directly to `--prod` when preview URLs might be gated, not conditionally.

- **Canvas sizing bugs hide in build output, not source** — Agent Lounge's 300x150px stuck canvas was a CSS/HTML bug introduced by Forge's build process, not visible in the spec. Verify rendered output dimensions match intent before handing off for review.

- **Manual UI login steps can't be scripted or delegated** — Obsidian Sync required Matt to manually open the app and authenticate via Settings UI. Flag these as blockers upfront rather than assuming they can be automated or handed to others.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Font size violations bypass when skipping Judge audit**: Portal passed Forge's fix pass (13px minimum enforced via grep) but Judge still found 3 font size violations in components (outcome-badge.tsx, calls-bar-chart.tsx). Grep validation ≠ rendered UI audit — always run Judge review before marking typography complete.

- **Clerk theme overrides require explicit `appearance` prop**: Dark theme setting in ClerkProvider was bleeding into sign-in component despite being a child route. Fixed only by adding explicit `appearance` prop override, not by moving provider or adjusting theme scope — this is a gotcha specific to Clerk's theming cascade.

- **Typography minimum enforcement needs component-level verification, not codebase-wide**: Fixed all 12px instances via grep, but violations still appeared in new/modified components (badge, chart components). Rule: grep after Forge completes, then spot-check rendered audit trail from Judge before final deploy.
