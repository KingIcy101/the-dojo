---
name: nextjs
description: Next.js 14 App Router patterns, file structure, routing, server vs client components, API routes, environment setup, and Vercel deployment. Use for any Next.js build to ensure correct architecture from the start.
---

# Next.js 14 (App Router)

## Project Setup
```bash
npx create-next-app@latest app-name --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd app-name
```

## File Structure
```
src/
├── app/
│   ├── layout.tsx          # Root layout (fonts, metadata, providers)
│   ├── page.tsx            # Home page
│   ├── globals.css         # Global styles + Tailwind imports
│   ├── (marketing)/        # Route group (no URL segment)
│   │   ├── about/page.tsx
│   │   └── pricing/page.tsx
│   └── api/
│       └── route.ts        # API route handlers
├── components/
│   ├── ui/                 # shadcn components (auto-generated)
│   └── [feature]/          # Feature components
├── lib/
│   └── utils.ts            # cn() helper + shared utilities
└── types/                  # TypeScript types
```

## Server vs Client Components

**Default = Server Component.** Only add `"use client"` when needed.

Use client when:
- useState / useEffect
- onClick / onChange handlers
- Browser APIs (window, localStorage)
- Framer Motion animations

```tsx
// Server Component (default) — no directive needed
export default async function Page() {
  const data = await fetch('...') // fetch directly, no useEffect
  return <div>{data}</div>
}

// Client Component
"use client"
import { useState } from 'react'
export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

## Routing
```
app/page.tsx              → /
app/about/page.tsx        → /about
app/blog/[slug]/page.tsx  → /blog/:slug
app/api/users/route.ts    → GET/POST /api/users
app/(auth)/login/page.tsx → /login (route group, no URL segment)
```

## API Routes
```ts
// app/api/contact/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  const body = await req.json()
  // ... logic
  return NextResponse.json({ ok: true })
}
```

## Environment Variables
```
.env.local          # local dev only, never committed
.env.example        # committed, shows required vars without values

NEXT_PUBLIC_*       # exposed to browser
Everything else     # server-only (never leaked to client)
```

## Metadata & SEO
```tsx
// app/layout.tsx
export const metadata = {
  title: { default: 'Site Name', template: '%s | Site Name' },
  description: '...',
  openGraph: { images: ['/og.png'] }
}

// Per-page metadata
export async function generateMetadata({ params }) {
  return { title: params.slug }
}
```

## Font Setup (next/font — no layout shift)
```tsx
import { GeistSans } from 'geist/font/sans'

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={GeistSans.className}>
      <body>{children}</body>
    </html>
  )
}
```

## Image Optimization
```tsx
import Image from 'next/image'
// Always use next/image, never <img>
<Image src="/hero.webp" alt="Hero" width={1200} height={600} priority />
// priority on above-fold images for LCP
```

## Common Patterns

### Loading UI
```tsx
// app/dashboard/loading.tsx — auto-shown during page load
export default function Loading() {
  return <Skeleton />
}
```

### Error Boundary
```tsx
// app/error.tsx
"use client"
export default function Error({ error, reset }) {
  return <button onClick={reset}>Try again</button>
}
```

### Middleware (auth redirects)
```ts
// middleware.ts (root)
import { NextResponse } from 'next/server'
export function middleware(req) {
  // check auth, redirect if needed
}
export const config = { matcher: ['/dashboard/:path*'] }
```

## Deployment (Vercel)
```bash
vercel          # preview deploy
vercel --prod   # production deploy
```
- Set env vars in Vercel dashboard, not in code
- `NEXT_PUBLIC_*` vars must be set at build time in Vercel

## Key Libraries We Use
| Need | Package |
|------|---------|
| UI components | shadcn/ui |
| Styling | tailwindcss |
| Animation | framer-motion |
| Icons | lucide-react |
| Forms | react-hook-form + zod |
| State | zustand |
| Server state | @tanstack/react-query |
| Auth | @clerk/nextjs |
| DB | @supabase/supabase-js |
| Email | resend |
| Payments | stripe |
| Analytics | posthog-js |
| Error tracking | @sentry/nextjs |


## Learned In Use

- **2026-03-13:** Static section divs (page-finances, page-commerce, page-meetings, page-analytics) must be defined in index.html rather than dynamically created — dynamic creation is unreliable.
- **2026-03-17:** Next.js localhost:3100 dev server with canvas-based isometric city grid generator maintains 65fps with 7 neighborhoods, dynamic road/sidewalk/building rendering — no performance issues with frequent state updates or canvas redraws in dev mode.

## Learned from Use (2026-03-22)
## Learned from Use (2026-03-22)

- **Preview URLs get auth-gated by SSO at team level** — even after disabling SSO on individual projects, Vercel preview URLs remained blocked. Workaround: deploy directly to production with `--prod` flag to get public URLs for review handoffs.

- **CSS canvas sizing bugs break Three.js rendering** — Agent Lounge's 3D scene stuck at 300x150px due to CSS/HTML in the build output, not the Three.js code itself. Always inspect final deployed HTML dimensions when canvas rendering fails, not just the scene initialization.

- **Build output visual validation must happen before handoff** — Forge's skeleton UI deployed functionally correct (camera, layout, activity dots) but missing entire visual layer (avatars, labels, colors, background). Briefs emphasizing "visual requirements are mandatory" need to be reinforced at task assignment, not discovered after deployment to reviewer.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Font size enforcement requires grep verification post-fix** — Fixed 12px violations in account/page.tsx and dashboard-chart.tsx, but Judge's Round 3 audit still caught 3 more (outcome-badge.tsx, calls-bar-chart.tsx). Now grep the entire codebase after typography fixes to catch scattered violations before QA.

- **Clerk appearance prop overrides are critical for sign-in UI isolation** — Dark theme from ClerkProvider was bleeding into the sign-in component. Use the `appearance` prop to explicitly override and isolate sign-in styling instead of relying on global theme inheritance.

- **Empty states and error messages must be part of the fix pass checklist** — The security/sanitization audit surfaced that error messages weren't being sanitized and empty states weren't updated. Include these in scope whenever doing a component fix pass, not as afterthoughts.

- **Dev pipeline (Pixel → Forge → Pixel review → Judge → Core) cannot be skipped after "build complete"** — Portal was deployed after Forge's fix pass without Pixel review or Judge audit. Judge caught font violations, Pixel found unwired Vapi, Core found security gaps. The moment Forge finishes is when the pipeline matters most.

- **2026-03-29:** Next.js 16 uses `proxy.ts` instead of `middleware.ts` — having both files causes build conflicts; remove `middleware.ts` if upgrading.

## Learned from Use (2026-04-05)
SKIP

The session logs show Next.js deployment activity (Halo Portal project with Vercel deployment at https://halo-portal-two.vercel.app) but contain no skill usage corrections, gotchas, approval patterns, or specific interactions that reveal lessons about *how* to use Next.js effectively. The logs focus on agent configuration, API management, and scheduling rather than Next.js skill application itself.
