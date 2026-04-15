---
name: zta-landing-page
description: Zero to Agent landing page architecture — dark theme, section order, amber accent, no frameworks.
category: business
---

# ZTA Landing Page

## When to Use
Building or updating the Zero to Agent marketing landing page. Reference: zerotoagent-builds.vercel.app. Pure HTML/CSS — no frameworks.

## Design System
```
Background:  #000000
Accent:      #D4944A (amber)
Text:        #FFFFFF
Muted:       #A0A0A0
Border:      #1A1A1A
Font:        Inter (Google Fonts)
```

## Section Order

1. **Hero** — headline + subhead + dual CTA
2. **Social Proof Bar** — stats strip
3. **Problem/Pain** — why businesses need this now
4. **Features Grid** — what the CAO delivers
5. **Agent Team Departments** — 8 lanes visual
6. **Use Cases Callout** — industry-specific examples
7. **Pricing** — 2 tiers, clean card layout
8. **Footer** — links + copyright

## Key Patterns / Code

### Hero Section
```html
<section class="hero">
  <h1>Your Business Deserves a <span class="accent">Full Agent Team</span></h1>
  <p class="subhead">The Chief Agent Officer system — 4 layers, 8 departments, built in 1-2 weeks.</p>
  <div class="cta-group">
    <a href="#pricing" class="btn-primary">Get Your CAO — $4,950</a>
    <a href="#how-it-works" class="btn-secondary">See How It Works</a>
  </div>
</section>
```

### Social Proof Bar
```html
<div class="proof-bar">
  <span>2,500+ founders</span>
  <span>4x sold out</span>
  <span>Delivered in 1-2 weeks</span>
  <span>No hiring. No payroll.</span>
</div>
```

### 8 Agent Department Cards
```
Sales | Operations | Finance | HR
Marketing | Customer Success | Legal | Research
```

### CSS Variables
```css
:root {
  --bg: #000;
  --accent: #D4944A;
  --text: #fff;
  --muted: #a0a0a0;
  --border: #1a1a1a;
  --radius: 8px;
}

.btn-primary {
  background: var(--accent);
  color: #000;
  padding: 14px 28px;
  border-radius: var(--radius);
  font-weight: 700;
  text-decoration: none;
}

.btn-secondary {
  border: 1px solid var(--border);
  color: var(--text);
  padding: 14px 28px;
  border-radius: var(--radius);
  text-decoration: none;
}

.accent { color: var(--accent); }
```

### Pricing Cards
```html
<div class="pricing-grid">
  <div class="pricing-card">
    <h3>Remote CAO</h3>
    <div class="price">$4,950</div>
    <ul>
      <li>Full 4-layer system</li>
      <li>8 specialist lanes</li>
      <li>Delivered virtually</li>
    </ul>
    <a href="#contact" class="btn-primary">Get Started</a>
  </div>
  <div class="pricing-card featured">
    <h3>Shipped CAO</h3>
    <div class="price">$9,450</div>
    <!-- ... -->
  </div>
</div>
```

## Gotchas
- No frameworks — pure HTML/CSS, deployed to Vercel as static
- All inter-section links use anchor IDs, not JS routing
- Proof bar numbers must match current actual numbers — update when milestones hit
- Mobile: stack pricing cards to 1 column below 768px
- No emojis in section headers — looks amateur on dark backgrounds
- Compress all images to WebP before adding
