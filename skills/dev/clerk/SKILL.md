---
name: clerk
description: >
  Clerk — user authentication and management for multi-tenant SaaS apps.
  Handles sign-up, sign-in, organizations, roles, and JWT tokens.
  Stack with Supabase (database) and Stripe (payments). Already in AI agency tech stack.
---

# Clerk — Auth & User Management

## What It Is
Clerk is the auth layer for every multi-tenant app we build. Handles everything — sign-up/sign-in flows, social OAuth, magic links, MFA, organizations, roles, and JWT tokens that integrate directly with Supabase RLS. Already locked into the AI agency stack.

## Setup
```bash
npm install @clerk/nextjs  # Next.js
npm install @clerk/clerk-sdk-node  # Node.js backend
```

### Next.js (App Router)
```jsx
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html><body>{children}</body></html>
    </ClerkProvider>
  )
}
```

```js
// middleware.ts — protect routes
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isPublicRoute = createRouteMatcher(['/sign-in(.*)', '/sign-up(.*)', '/'])

export default clerkMiddleware((auth, request) => {
  if (!isPublicRoute(request)) auth().protect()
})
```

## Core API

### Auth State (client-side)
```jsx
import { useUser, useAuth, UserButton, SignInButton } from '@clerk/nextjs'

function Header() {
  const { isSignedIn, user } = useUser()
  const { signOut } = useAuth()

  return (
    <header>
      {isSignedIn ? (
        <>
          <span>Hi {user.firstName}</span>
          <UserButton afterSignOutUrl="/" />
        </>
      ) : (
        <SignInButton />
      )}
    </header>
  )
}
```

### Get User Server-Side
```js
import { auth, currentUser } from '@clerk/nextjs/server'

export default async function Page() {
  const { userId, orgId } = auth()
  const user = await currentUser()

  if (!userId) redirect('/sign-in')

  return <div>Hello {user.firstName}</div>
}

// In API routes
export async function GET(req) {
  const { userId } = auth()
  if (!userId) return new Response('Unauthorized', { status: 401 })
  // ... handle request
}
```

### Organizations (Multi-Tenant)
```jsx
// Each client = their own Clerk Organization
import { useOrganization, OrganizationSwitcher } from '@clerk/nextjs'

function Dashboard() {
  const { organization } = useOrganization()
  // organization.id = used to scope all DB queries
  return <div>Org: {organization?.name}</div>
}

// In server: get org ID from JWT
const { orgId, orgRole } = auth()
// orgRole: 'org:admin' | 'org:member'
```

### Custom JWT Claims → Supabase Integration
```js
// In Clerk Dashboard → JWT Templates → Supabase template:
// Adds org_id to JWT so Supabase RLS can use it
{
  "org_id": "{{org.id}}",
  "role": "{{org.role}}"
}

// Supabase client with Clerk token
const supabase = createClient(url, anonKey, {
  global: {
    headers: {
      Authorization: `Bearer ${await getToken({ template: 'supabase' })}`
    }
  }
})
```

### Roles & Permissions
```js
// Check role server-side
const { orgRole } = auth()
if (orgRole !== 'org:admin') return new Response('Forbidden', { status: 403 })

// Client-side
import { useAuth } from '@clerk/nextjs'
const { has } = useAuth()
const canManageClients = has({ role: 'org:admin' })
```

## Environment Variables
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_...
CLERK_SECRET_KEY=sk_live_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/onboarding
```

## Best Use Cases for Our Builds
- **AI agency client portals** — each client = Clerk org, isolated data
- **Halo Marketing** — practitioner login to their patient dashboard
- **SourceDart** — user accounts for sourcing tool
- **Mission Control** — replace PIN auth with proper Clerk auth

## Skill Injection for Codex/Claude Code
```
Use Clerk (@clerk/nextjs) for all auth. Multi-tenant via Clerk Organizations.
Protect routes via clerkMiddleware in middleware.ts.
Get user: auth() server-side, useUser() client-side.
JWT → Supabase: use 'supabase' JWT template, pass token as Authorization header.
orgId from auth() scopes all DB queries via Supabase RLS.
```


## Learned from Use (2026-03-22)
## Learned from Use (2026-03-22)

- **Handoff clarity requires real mentions, not text substitutes** — Forge's use of `@Pixel` as plain text instead of actual mentions broke the handoff workflow. When delegating to other agents, ensure the clerk explicitly formats mentions/IDs in a way that systems recognize, not just human-readable text.

- **Gating and auth issues require production deploys as workaround** — Preview URLs being auth-gated forced Matt to switch strategy to `--prod` deploys to unblock Pixel's review. When clerk delegates build tasks, note if preview access is blocked and pre-authorize production deployment as the faster path.

- **Brief quality directly impacts agent execution** — Forge built a skeleton UI that was 60% compliant because the brief didn't emphasize visual requirements were mandatory. When creating Codex briefs or delegating specs, clerk should explicitly flag non-negotiable vs. nice-to-have elements to avoid partial implementations.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Clerk Organizations auth refactor was a blocker until completed** — Listed as a dependency in early snapshots, then resolved in the Forge fix pass. Clerk Orgs plan confirmation from Matt was critical path; coordinate org setup timing early to avoid QA delays.

- **Clerk dark theme bleeding into sign-in component required appearance prop override** — Default ClerkProvider theme cascaded into the sign-in UI (white background, dark text failed contrast). Solution: Use `appearance` prop to explicitly override at the ClerkProvider level, not component-level styling.

- **Clerk sign-in UI must be audited as part of QA pipeline** — Font size violations were caught in Judge's rounds, but sign-in styling (branding, contrast, theme isolation) wasn't explicitly called out until the final deployment. Include Clerk-provided UI components in pixel/accessibility review passes.


## Learned In Use

- **2026-03-29:** Environment variables from Vercel can have trailing newlines (e.g., `/sign-in
`) — always .trim() Clerk URL config vars before use.
- **2026-03-29:** Clerk's `appearance` prop with class name overrides (using `!important`) can override dark theme bleeding into sign-in components — use this pattern for styling fixes.

## Learned from Use (2026-04-05)
SKIP

The session logs show "clerk" skill was not actively used during these sessions. The logs document memory snapshots, status checks, and context management, but there are no instances where the clerk skill was invoked, corrected, or produced measurable outcomes that would generate actionable lessons about its use.
