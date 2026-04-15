---
name: iconify
description: >
  Iconify — unified API for every icon set (Lucide, Phosphor, Heroicons, Tabler, Material, etc.).
  200,000+ icons in one package. Use instead of installing multiple icon libraries.
  Works in React, Vue, vanilla JS, and CSS.
---

# Iconify — Universal Icon System

## Install
```bash
npm install @iconify/react    # React
npm install @iconify/tailwind # Tailwind CSS plugin
```

## React Usage
```jsx
import { Icon } from '@iconify/react'

// Format: 'set:icon-name'
<Icon icon="lucide:calendar" className="w-5 h-5" />
<Icon icon="ph:user-circle-bold" className="w-6 h-6 text-indigo-400" />
<Icon icon="heroicons:chart-bar-16-solid" width={20} height={20} />
<Icon icon="tabler:brand-slack" className="text-xl" />

// With color and size props
<Icon icon="lucide:check-circle" color="#10b981" width={20} />
```

## Key Icon Sets
```
lucide:           Lucide — clean, minimal (our default)
ph:               Phosphor — more expressive variants
heroicons:        Tailwind's set — solid/outline variants
tabler:           Tabler — 5000+ clean stroke icons
material-symbols: Google Material
ri:               RemixIcon — comprehensive set
mdi:              Material Design Icons
carbon:           IBM Carbon — data/enterprise
logos:            Brand logos (Slack, Stripe, etc.)
```

## Tailwind CSS Plugin
```js
// tailwind.config.js
const { addDynamicIconSelectors } = require('@iconify/tailwind')

module.exports = {
  plugins: [addDynamicIconSelectors()],
}
```
```html
<!-- Use as CSS masks (pure CSS, no JS) -->
<span class="icon-[lucide--calendar] w-5 h-5 bg-current"></span>
<span class="icon-[ph--user-bold] w-6 h-6 text-indigo-400"></span>
```

## Search Icons
```
https://icon-sets.iconify.design/
Type any keyword → browse all sets → copy icon name
```

## Our Standard Icons (Reference)
```
Navigation:     lucide:layout-dashboard, lucide:calendar, lucide:users, lucide:settings
Actions:        lucide:plus, lucide:edit-2, lucide:trash-2, lucide:search, lucide:filter
Status:         lucide:check-circle, lucide:alert-circle, lucide:clock, lucide:x-circle
Data:           lucide:trending-up, lucide:bar-chart-2, lucide:pie-chart
Communication:  lucide:mail, lucide:message-square, lucide:phone
Files:          lucide:file-text, lucide:download, lucide:upload
Arrows:         lucide:chevron-right, lucide:arrow-left, lucide:external-link
Brands:         logos:slack, logos:stripe, logos:notion, logos:google-gmail
Agents:         ph:robot-bold, ph:brain-bold, ph:lightning-bold
```

## Vanilla JS (CDN — no install)
```html
<script src="https://code.iconify.design/iconify-icon/2.1.0/iconify-icon.min.js"></script>
<iconify-icon icon="lucide:calendar" width="20" height="20"></iconify-icon>
```

## Skill Injection for Codex/Claude Code
```
Use Iconify (@iconify/react) for all icons. npm install @iconify/react.
Format: 'set:icon-name' — e.g. 'lucide:calendar', 'ph:user-bold', 'heroicons:chart-bar-solid'.
Default set: lucide: for standard UI. ph: for expressive variants. logos: for brands.
Search: icon-sets.iconify.design. No multiple icon libraries needed.
```
