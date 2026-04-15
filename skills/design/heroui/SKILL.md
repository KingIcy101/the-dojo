---
name: heroui
description: HeroUI (rebranded NextUI) — premium React component library built on Tailwind + Framer Motion. Beautiful defaults, smooth animations out of the box. Use when you want more pre-built polish than shadcn. Great for auth pages, dashboards, forms.
---

# HeroUI — Premium React Components

## Install
```bash
npm install @heroui/react framer-motion
```

## Setup (Next.js)
```tsx
// app/providers.tsx
'use client'
import { HeroUIProvider } from '@heroui/react'

export function Providers({ children }: { children: React.ReactNode }) {
  return <HeroUIProvider>{children}</HeroUIProvider>
}
```

```js
// tailwind.config.js
const { heroui } = require('@heroui/react')
module.exports = {
  content: [
    './node_modules/@heroui/theme/dist/**/*.{js,ts,jsx,tsx}'
  ],
  plugins: [heroui()]
}
```

## Key Components
```tsx
import { Button, Card, CardBody, Input, Modal, Chip, Avatar, Tabs } from '@heroui/react'

// Button variants
<Button color="primary" variant="shadow">Get Started</Button>
<Button color="default" variant="bordered">Learn More</Button>

// Cards with hover effects
<Card isHoverable isPressable>
  <CardBody>Content</CardBody>
</Card>

// Inputs with built-in validation UI
<Input label="Email" type="email" variant="bordered" />
```

## When to Use vs shadcn
- **HeroUI**: more opinionated, beautiful defaults, less customization needed, better for auth/onboarding flows
- **shadcn**: more flexible, you own the code, better for custom design systems
- Can mix both — shadcn for layout primitives, HeroUI for interactive components

## Rules
- Use for: auth pages, modals, forms, interactive UI with animation
- Don't use for: heavily customized design systems (shadcn owns that)
- Always pair with Tailwind config setup or styles break


## Learned from Use (2026-03-22)
SKIP

The session logs contain no meaningful information about "heroui" skill usage. The mentions reference Vercel deployments, Three.js canvas rendering, UI components, and Forge builds, but no specific instances where the heroui skill was directly applied, tested, or corrected. There are no logged corrections, failures, or decision points tied to heroui itself—only general deployment and build issues.
