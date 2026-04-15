---
name: aceternity-ui
description: >
  Aceternity UI — stunning motion-forward component library (Tailwind + Framer Motion). Glowing cards, beam effects,
  spotlight hover, parallax, animated gradients. Free. Use in every UI build that needs premium visual effects.
  Stack with Magic UI for maximum design impact.
---

# Aceternity UI — Premium Motion Components

## What It Is
Aceternity UI (ui.aceternity.com) is the go-to library for expensive-looking web effects in 2026. Built on Tailwind CSS + Framer Motion. Free. Copy-paste components directly into projects — no package install required (though npm available).

**Signature effects:**
- Spotlight cards (cursor follows light source)
- Glowing borders that animate
- Beam/aurora backgrounds
- 3D card tilt with perspective
- Animated gradient text
- Background grid/dot patterns
- Floating labels
- Timeline components
- Bento grid layouts

## Installation
```bash
# npm
npm install framer-motion clsx tailwind-merge

# or just copy-paste from ui.aceternity.com — no install needed
```

## Key Components & Code

### Spotlight Card (most used)
```jsx
import { Spotlight } from "@/components/ui/spotlight";

<div className="relative overflow-hidden rounded-2xl border border-white/10 bg-black/40 p-8">
  <Spotlight className="-top-40 left-0 md:-top-20 md:left-60" fill="white" />
  <h2>Your content here</h2>
</div>
```

### Glowing Card Border
```jsx
// CSS-only version (no React needed)
.card-glow {
  background: linear-gradient(var(--bg-card), var(--bg-card)) padding-box,
              linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899) border-box;
  border: 1px solid transparent;
  border-radius: 12px;
}
```

### Aurora Background
```jsx
import { AuroraBackground } from "@/components/ui/aurora-background";

<AuroraBackground>
  <div className="relative z-10">Your hero content</div>
</AuroraBackground>
```

### 3D Card Tilt
```jsx
import { CardBody, CardContainer, CardItem } from "@/components/ui/3d-card";

<CardContainer className="inter-var">
  <CardBody className="bg-gray-50 relative group/card dark:bg-black border-black/[0.1] w-[30rem] h-auto rounded-xl p-6 border">
    <CardItem translateZ="50" className="text-xl font-bold">
      Make things float in air
    </CardItem>
    <CardItem translateZ="100" className="w-full mt-4">
      <img src="..." className="h-60 w-full object-cover rounded-xl" />
    </CardItem>
  </CardBody>
</CardContainer>
```

### Animated Gradient Text
```jsx
import { TextGenerateEffect } from "@/components/ui/text-generate-effect";

<TextGenerateEffect words="Built for the bold." />
```

### Background Beams
```jsx
import { BackgroundBeams } from "@/components/ui/background-beams";

<div className="relative">
  <BackgroundBeams />
  <div className="relative z-10">Content above beams</div>
</div>
```

### Bento Grid
```jsx
import { BentoGrid, BentoGridItem } from "@/components/ui/bento-grid";

<BentoGrid className="max-w-4xl mx-auto">
  {items.map((item, i) => (
    <BentoGridItem key={i} title={item.title} description={item.description}
      className={i === 3 || i === 6 ? "md:col-span-2" : ""} />
  ))}
</BentoGrid>
```

## Vanilla JS / No-Framework Versions
Most effects can be replicated without React:
```js
// Spotlight effect — pure JS
document.addEventListener('mousemove', (e) => {
  const cards = document.querySelectorAll('.card-spotlight');
  cards.forEach(card => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty('--mouse-x', `${x}px`);
    card.style.setProperty('--mouse-y', `${y}px`);
  });
});
```
```css
.card-spotlight {
  background: radial-gradient(
    600px circle at var(--mouse-x) var(--mouse-y),
    rgba(99,102,241,0.15), transparent 40%
  );
}
```

## Best Use Cases for Our Builds
- **Mission Control dashboard** — spotlight cards for KPI sections
- **Halo Marketing landing** — aurora background, glowing CTA buttons
- **AI agency site** — beam backgrounds, 3D card tilt for services
- **Client portals** — bento grid for dashboard sections
- **Calendar** — animated gradient text for date headers

## Skill Injection for Codex/Claude Code
```
Use Aceternity UI (ui.aceternity.com) for premium visual effects.
Key components: Spotlight cards, Aurora background, Background Beams, 3D Card tilt, Bento Grid.
Vanilla JS spotlight: mousemove → radial-gradient at cursor position.
Stack with Magic UI for maximum impact.
```


## Learned from Use (2026-03-22)
SKIP

The session logs contain no mentions of aceternity-ui being used, tested, or causing issues. The skill name appears only in the analysis prompt header but never in the actual session activity. All logged work involves Vercel deployments, Three.js canvas rendering, Forge builds, and Obsidian sync—none of which involve aceternity-ui component library.


## Learned from Use (2026-03-29)
SKIP

The session logs show aceternity-ui was not a focal point of corrections or learning. The skill was mentioned only in context ("Build: Portal v1 in QA") but the actual corrections and lessons centered on:

1. **Dev pipeline discipline** (Pixel → Forge → Pixel → Judge → Core)
2. **Agent coordination channels** (#dev-team-chat vs private channels)
3. **Memory file management** (15KB limit, vault archiving)
4. **Clerk theming specifics** (`appearance` prop override)

None of the corrections, blockers, or critical rules involved aceternity-ui itself. To extract a genuine "Learned from Use" section, there would need to be a correction tied directly to how aceternity-ui components were built, styled, or debugged—but the logs show typography fixes were applied to existing components without surfacing aceternity-ui-specific gotchas or patterns.
