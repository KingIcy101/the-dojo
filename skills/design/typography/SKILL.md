---
name: typography
description: >
  Typography system for all builds — font pairings, variable fonts, loading patterns, sizing scale.
  Covers Inter, Geist, Cal Sans, Fontshare, and Google Fonts. Use on every UI build alongside ui-ux-pro-max.
  Defines the font stack that makes interfaces look expensive vs amateur.
---

# Typography — Font System

## The Rule
**Font choice is the fastest way to make a UI look cheap or expensive.** System fonts are safe but generic. The right pairing at the right weight creates instant perceived quality.

---

## Recommended Stacks by Use Case

### SaaS Dashboard / Agency (Matt's Primary Stack)
```css
/* Heading: Geist (Vercel's font — clean, technical, modern) */
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&display=swap');

/* Body: Inter (industry standard — readable at any size) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --font-heading: 'Geist', -apple-system, sans-serif;
  --font-body: 'Inter', -apple-system, sans-serif;
  --font-mono: 'Geist Mono', 'SF Mono', monospace;
}
```

### Premium / High-End (AI Agency Site, Client Portals)
```css
/* Heading: Cal Sans (used by Cal.com, clean + confident) */
/* Get from: https://github.com/calcom/font */

/* Body: Inter */
/* Result: instantly feels like a $10K site */
```

### Editorial / Content (Newsletters, Blog)
```css
/* Heading: Playfair Display — editorial, luxury feel */
/* Body: Source Serif 4 — readable long-form */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Source+Serif+4:wght@400;500&display=swap');
```

### Technical / Developer Tool
```css
/* Heading: JetBrains Mono — technical authority */
/* Body: Inter */
/* Great for: dashboards, dev tools, analytics */
```

### Healthcare (Halo Clients)
```css
/* Heading: Nunito — friendly, approachable, medical */
/* Body: Open Sans — highly readable, clean */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800&family=Open+Sans:wght@400;500;600&display=swap');
```

---

## Fontshare (Free Premium Fonts — Better than Google)
```
https://www.fontshare.com

Top picks:
- Satoshi     — geometric sans, modern SaaS feel
- General Sans — clean, versatile, professional
- Cabinet Grotesk — bold headings, strong personality
- Clash Display — impactful hero text
- Switzer     — clean body text, excellent readability
```
```css
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@700,500,400&display=swap');
```

---

## Type Scale (Use This Every Build)
```css
:root {
  /* Scale */
  --text-xs:   11px;  /* tags, labels, captions */
  --text-sm:   13px;  /* secondary body */
  --text-base: 14px;  /* primary body, inputs, buttons */
  --text-md:   16px;  /* card titles */
  --text-lg:   18px;  /* section intros */
  --text-xl:   20px;  /* sub-headers */
  --text-2xl:  24px;  /* section headers */
  --text-3xl:  30px;  /* page titles */
  --text-4xl:  36px;  /* KPI numbers */
  --text-5xl:  48px+; /* hero headlines */

  /* Line heights */
  --lh-tight:  1.2;  /* headings */
  --lh-normal: 1.5;  /* body */
  --lh-loose:  1.75; /* readable paragraphs */

  /* Letter spacing */
  --ls-tight:  -0.03em; /* large numbers, hero text */
  --ls-normal: -0.01em; /* body (slightly tight = modern) */
  --ls-wide:    0.06em; /* ALL CAPS labels, badges */

  /* Weights */
  --fw-normal:   400;
  --fw-medium:   500;
  --fw-semibold: 600;
  --fw-bold:     700;
  --fw-black:    800;
}
```

---

## Variable Fonts (Performance Wins)
```css
/* Variable font = one file, all weights. Faster load. */
/* Inter Variable */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');

/* Use font-variation-settings for fine control */
.hero-number {
  font-variation-settings: 'wght' 750, 'slnt' 0;
}
```

---

## Loading Pattern (No Flash of Unstyled Text)
```css
/* 1. Define fallback that matches final font metrics */
@font-face {
  font-family: 'Inter-fallback';
  src: local('Arial');
  ascent-override: 90%;
  descent-override: 22.43%;
  line-gap-override: 0%;
  size-adjust: 107.64%;
}

/* 2. Font stack with fallback */
body {
  font-family: 'Inter', 'Inter-fallback', -apple-system, sans-serif;
}
```

---

## Font Pairing Rules
1. **Contrast** — pair a geometric sans (Geist) with a humanist sans (Inter), not two similar fonts
2. **Weight separation** — heading 700-800, body 400-500. Don't both be 600.
3. **Max 2 typefaces** per project. 3 is the absolute limit.
4. **Mono for code/data** — always use a dedicated mono font for numbers/code
5. **Test at size** — check heading at 14px and body at 48px; good fonts work at both

---

## Quick Reference: Font → Vibe
```
Inter         → neutral, professional, universal
Geist         → technical, modern, clean
Cal Sans      → confident, startup, premium
Satoshi       → geometric, contemporary, SaaS
Nunito        → friendly, approachable, healthcare
Playfair      → editorial, luxury, sophistication
JetBrains Mono → developer, technical authority
Clash Display → bold, disruptive, agency
```

---

## Skill Injection for Codex/Claude Code
```
Typography stack: Geist (heading) + Inter (body) + Geist Mono (code/numbers).
Scale: 11/13/14/16/20/24/30/36/48px. Never below 11px.
Letter spacing: -0.03em hero, -0.01em body, 0.06em ALL-CAPS labels.
Line height: 1.2 headings, 1.5 body. Font weight: 700-800 heading, 400-500 body.
Fontshare for premium free fonts: Satoshi, General Sans, Cabinet Grotesk.
```


## Learned from Use (2026-03-22)
SKIP

The session logs contain no meaningful uses of the "typography" skill. The entries discuss deployment workflows, UI rendering bugs (canvas sizing, missing visual elements), and communication handoffs—but no instances where typography decisions, font selection, spacing, hierarchy, or text styling were applied, evaluated, or corrected. The single mention of text ("Forge used text `@Pixel` instead of real mentions") is about mention syntax, not typography.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Minimum font size enforcement prevents QA rejection cycles** — Judge's round 2 verdict rejected on two 12px violations (Agent ID label, chart tooltip). Establishing 13px minimum across all components eliminated font size violations in rounds 3–4. Grep verification of the entire codebase before final deploy caught remaining violations that would have failed shipping.

- **Typography fixes in isolation require full pipeline validation** — Forge's typography pass (font sizes, empty states) looked complete at 18:38, but Judge's round 3 audit still found 3 additional font size violations in different components (outcome-badge.tsx, calls-bar-chart.tsx). Never assume a fix pass is complete without rendering audit; pixel-level typography issues hide in multiple file locations.

- **Clerk theme overrides bleed into typography unexpectedly** — Dark theme setting in ClerkProvider bled into the sign-in component's text contrast, creating a hidden typography problem (white text on white background). The `appearance` prop override was the fix, revealing that third-party component theming can silently corrupt font/text rendering in dependent UI.
