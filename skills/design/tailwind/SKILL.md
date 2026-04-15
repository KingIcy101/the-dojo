---
name: tailwind
description: >
  Tailwind CSS — utility-first CSS framework. Patterns, config, dark mode, custom tokens, responsive design.
  Used in every web build. Stack with shadcn/ui, Aceternity UI, Magic UI, Tremor.
  This skill documents patterns and config — not basics.
---

# Tailwind CSS — Patterns & Config

## Config (tailwind.config.js)
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',  // toggle via class, not media query
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './node_modules/@tremor/**/*.{js,ts,jsx,tsx}',
    './node_modules/@shadcn/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Matt's design system tokens
        'bg-primary': '#0a0a0f',
        'bg-card': '#12121e',
        'bg-elevated': '#1a1a2e',
        'accent': '#6366f1',
        'accent-muted': 'rgba(99,102,241,0.15)',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        heading: ['Geist', '-apple-system', 'sans-serif'],
        mono: ['Geist Mono', 'SF Mono', 'monospace'],
      },
      fontSize: {
        'xs': ['11px', { lineHeight: '1.5' }],
        'sm': ['13px', { lineHeight: '1.5' }],
        'base': ['14px', { lineHeight: '1.5' }],
        'md': ['16px', { lineHeight: '1.4' }],
        'lg': ['20px', { lineHeight: '1.3' }],
        'xl': ['24px', { lineHeight: '1.2' }],
        '2xl': ['30px', { lineHeight: '1.1' }],
        '3xl': ['36px', { lineHeight: '1.05' }],
      },
      borderRadius: {
        'card': '12px',
        'btn': '8px',
        'pill': '9999px',
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'shimmer': 'shimmer 1.5s linear infinite',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '200% 0' },
          '100%': { backgroundPosition: '-200% 0' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(99,102,241,0)' },
          '50%': { boxShadow: '0 0 20px 4px rgba(99,102,241,0.3)' },
        },
      },
      boxShadow: {
        'card': '0 4px 24px rgba(0,0,0,0.3)',
        'card-hover': '0 8px 40px rgba(0,0,0,0.4)',
        'glow': '0 0 20px rgba(99,102,241,0.4)',
        'glow-sm': '0 0 10px rgba(99,102,241,0.2)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),  // prose classes for content
    require('@tailwindcss/forms'),       // form reset
  ],
}
```

## Key Utility Patterns

### Dark Cards
```html
<div class="bg-[#12121e] border border-white/[0.06] rounded-[12px] p-5
            hover:border-white/[0.12] hover:shadow-[0_8px_32px_rgba(0,0,0,0.3)]
            transition-all duration-200">
```

### Glassmorphism
```html
<div class="bg-white/[0.03] backdrop-blur-xl border border-white/[0.08]
            rounded-2xl backdrop-saturate-180">
```

### Accent Button
```html
<button class="bg-indigo-500 hover:bg-indigo-400 active:scale-[0.98]
               text-white font-medium text-sm px-4 py-2 rounded-lg
               transition-all duration-150 cursor-pointer">
```

### Ghost Button
```html
<button class="bg-transparent hover:bg-white/[0.04] text-white/60
               hover:text-white border border-white/[0.06]
               text-sm px-4 py-2 rounded-lg transition-all duration-150">
```

### Badge / Status Pill
```html
<span class="inline-flex items-center px-2 py-0.5 rounded-full
             text-[11px] font-semibold tracking-wide uppercase
             bg-emerald-500/15 text-emerald-400">Active</span>
```

### Responsive Grid
```html
<!-- 4 col → 2 col → 1 col -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
```

### Mobile-First Sidebar Hide (900px breakpoint)
```html
<!-- Custom breakpoint for WebView -->
<div class="sidebar hidden max-[900px]:hidden lg:block">
```
```js
// tailwind.config.js — add custom breakpoint
screens: { 'mobile': { max: '900px' } }
// Usage: mobile:hidden
```

### Stagger Animation
```html
<div class="flex flex-col gap-3">
  {items.map((item, i) => (
    <div key={i} class="animate-fade-in" style={{ animationDelay: `${i * 80}ms` }}>
      {item}
    </div>
  ))}
</div>
```

## CSS Variables Integration
```css
/* globals.css — bridge Tailwind with CSS variables */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --accent: 99 102 241;
    --bg-card: 18 18 30;
  }
}

/* Use with opacity modifier: bg-[rgb(var(--bg-card))/80] */
```

## Skill Injection for Codex/Claude Code
```
Tailwind config: darkMode:'class', custom colors/fonts/animations matching design system.
Key patterns: bg-[#12121e] cards, backdrop-blur glassmorphism, indigo-500 accent.
Mobile breakpoint: max-[900px]:hidden (not md: — catches WebView).
Animate with custom keyframes in config. Stagger via animationDelay inline style.
Plugins: @tailwindcss/typography, @tailwindcss/forms.
```


## Learned In Use

- **2026-03-13:** CSS specificity conflict: `.mcv2-page { display:flex }` overrides `section { display:none }` causing unintended section visibility — remove display property from parent container classes.
- **2026-03-17:** Color palette for isometric city simulation requires light cream/tan sidewalks (#636E72 light gray roads) and light backgrounds so buildings pop — avoid dark navy/purple base colors that reduce visual hierarchy and make details invisible.

## Learned from Use (2026-03-22)
SKIP

The session logs contain no mentions of the "tailwind" skill being used. The logs document deployment issues (Vercel auth, preview URLs, production builds), Three.js canvas rendering problems, and UI spec compliance—none of which involve Tailwind CSS or the tailwind skill specifically. Without evidence of tailwind skill application, corrections, or patterns in these logs, there are no actionable lessons to extract for that skill.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Font size enforcement via Tailwind classes must be verified across all component files** — Judge's round 2 audit found 12px violations in Agent ID label and chart tooltip that had been missed. Subsequent grep validation (round 3–4) revealed the pattern: audit → find → grep entire codebase → fix all instances at once, not piecemeal. Minimum 13px became the enforced floor.

- **Tailwind overrides in provider-level theming can leak into unintended components** — Clerk's dark theme bled into the sign-in UI until the `appearance` prop override in ClerkProvider was explicitly set. Lesson: when using Tailwind with third-party component libraries, isolate theme scope at injection point rather than relying on global Tailwind config.

- **Typography corrections must pass through the full QA pipeline (Pixel → Judge) before deployment** — Three separate rounds of font size fixes were needed because initial Forge pass didn't catch all violations. Skipping Pixel's visual review before Judge audit compounds the problem. The pipeline step exists for Tailwind styling specifically because pixel-level details don't surface in code review alone.
