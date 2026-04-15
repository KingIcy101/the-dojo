---
name: website-builder
description: Landing pages, client websites, and marketing sites. Conversion-focused layout, hero section anatomy, section ordering, CTA strategy, and design brief generation. Use before ANY website or landing page build — read this first, write the design brief, then hand to Codex.
---

# Website Builder

## Stack (always use this for new sites)
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Animation:** Framer Motion (scroll reveals, hero entrance) + GSAP (complex sequences)
- **Components:** shadcn/ui (base) + Aceternity UI (premium effects) + Magic UI (animated elements)
- **Fonts:** Geist Sans (UI) + Cal Sans or Plus Jakarta Sans (headings)
- **Deploy:** Vercel
- **Icons:** Lucide React (via shadcn) or Iconify for extended sets

## Design Brief Workflow (MANDATORY before any build)

Before writing a single line of code:
1. Read `ui-ux-pro-max` skill for design system rules
2. Ask Matt: reference URL? screenshot? brand colors?
3. Write the design brief (see template below)
4. Get Matt's approval
5. Then write the Codex spec

## Design Brief Template

```
## [Project Name] — Design Brief

**Feel:** [e.g., dark premium SaaS / clean medical / bold agency]
**Primary color:** [hex]
**Accent color:** [hex]
**Font:** [heading / body]
**Animation level:** [subtle / medium / heavy]

### Sections (in order)
1. Hero — [headline concept, CTA text, background treatment]
2. Social proof — [logos / testimonials / stats]
3. [Service/Feature section]
4. [How it works]
5. [Testimonials]
6. CTA — [final push copy]
7. Footer

### Key components
- [List shadcn/Aceternity/Magic UI components to use]
```

## Landing Page Anatomy (Conversion-Optimized)

### Section Order (proven sequence)
1. **Navbar** — logo left, nav center, CTA button right. Sticky. Blur backdrop.
2. **Hero** — H1 above fold, subheadline, primary CTA + secondary CTA, social proof signal (e.g., "50+ clients")
3. **Problem/Pain** — name the problem they have. Short. Emotional.
4. **Solution** — how you fix it. Feature grid or 3-column cards.
5. **How It Works** — 3-step process. Numbered. Simple icons.
6. **Social Proof** — testimonials, before/after stats, client logos
7. **FAQ** — handle objections before they arise
8. **Final CTA** — repeat the offer, lower friction ("Book a free call")
9. **Footer** — minimal. Legal links, social icons.

### Hero Patterns (pick one)
- **Centered hero:** H1 centered, gradient text on key word, subtext, two buttons, floating UI mockup below
- **Split hero:** Left text, right visual/mockup
- **Video hero:** Full-bleed background video with overlay text
- **Particle/WebGL hero:** Three.js or Aceternity Spotlight for premium feel

### High-Converting CTA Principles
- Primary CTA: action verb + outcome ("Get More Patients", "Start Free Trial")
- Secondary CTA: lower commitment ("See How It Works")
- Reduce friction: "No credit card" / "Free consultation" beneath button
- Color: CTA button should be accent color, high contrast

## Halo Marketing Site Conventions
- **Industry:** Healthcare practitioners (chiropractors, dentists, telehealth)
- **Tone:** Professional but approachable. Results-focused. Trust-heavy.
- **Must-haves:** Patient testimonials, before/after stats, "how it works" section
- **Avoid:** Overly corporate language, generic stock photos, cluttered layouts

## AI Agency Site Conventions
- **Tone:** Bold, modern, tech-forward. Premium.
- **Must-haves:** Live demos if possible, case studies, clear ROI framing
- **Aesthetic:** Dark theme, gradient accents, motion-heavy hero

## Performance Rules
- Images: WebP format, next/image for optimization
- Fonts: next/font (no layout shift)
- Animations: `will-change: transform`, framer-motion `viewport` prop for scroll triggers
- LCP target: < 2.5s. Avoid heavy above-fold animations without preload.

## Codex Spec Format
When writing the spec for Codex, be surgical:
- Name exact components: "Use Aceternity UI `<Spotlight>` for hero background"
- Name exact colors: "bg-zinc-950 / text-white / accent #6c63ff"
- Name exact fonts: "font-cal for H1, font-geist for body"
- Describe layout with Tailwind classes where possible
- Include responsive behavior: "stack to single column below md:"
