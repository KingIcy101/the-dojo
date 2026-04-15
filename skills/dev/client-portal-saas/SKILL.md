---
name: client-portal-saas
description: Multi-tenant client portal using Next.js 14 App Router, Clerk Organizations, and Supabase RLS.
category: dev
---

# Client Portal SaaS

## When to Use
Building a multi-tenant SaaS portal where each client org sees only their own data. ITP's client dashboard pattern.

## Stack
- **Next.js 14** App Router (server components by default)
- **Clerk** Organizations for auth + multi-tenancy
- **Supabase** with RLS for data isolation
- **Rate limiting** in-memory (30 req / 60s per org)
- **Vercel** for deployment

## Steps

1. Install: `npm i @clerk/nextjs @supabase/supabase-js`
2. Wrap app in `<ClerkProvider>` in root layout
3. Middleware: protect routes with `authMiddleware`
4. Server layouts use `auth()` from `@clerk/nextjs/server`
5. Client components use `useAuth()` / `useOrganization()` hooks
6. Pass `org_id` as JWT claim → Supabase RLS enforces isolation
7. Rate limit middleware checks org_id + timestamp window

## Key Patterns / Code

### Middleware (middleware.ts)
```ts
import { authMiddleware } from '@clerk/nextjs';
export default authMiddleware({ publicRoutes: ['/', '/sign-in', '/sign-up'] });
export const config = { matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'] };
```

### Server Layout — get org_id
```ts
import { auth } from '@clerk/nextjs/server';

export default async function DashboardLayout({ children }) {
  const { orgId } = auth();
  if (!orgId) redirect('/select-org');
  return <>{children}</>;
}
```

### Supabase Client with JWT (server-side)
```ts
import { createClient } from '@supabase/supabase-js';
import { auth } from '@clerk/nextjs/server';

export async function getSupabaseClient() {
  const { getToken } = auth();
  const token = await getToken({ template: 'supabase' });
  return createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
    global: { headers: { Authorization: `Bearer ${token}` } },
  });
}
```

### Supabase RLS Policy
```sql
-- Enable RLS
ALTER TABLE call_logs ENABLE ROW LEVEL SECURITY;

-- Policy: org sees only their rows
CREATE POLICY "org_isolation" ON call_logs
  FOR ALL USING (
    auth.jwt() ->> 'org_id' = org_id
  );
```

### In-Memory Rate Limiter
```ts
const rateLimits = new Map<string, { count: number; resetAt: number }>();

export function checkRateLimit(orgId: string): boolean {
  const now = Date.now();
  const limit = rateLimits.get(orgId);
  if (!limit || now > limit.resetAt) {
    rateLimits.set(orgId, { count: 1, resetAt: now + 60_000 });
    return true;
  }
  if (limit.count >= 30) return false;
  limit.count++;
  return true;
}
```

## Gotchas
- Server components: use `auth()` from `@clerk/nextjs/server` — not hooks
- Client components: use `useAuth()` — never import server functions in client components
- Clerk JWT template named "supabase" must be configured in Clerk dashboard with org_id claim
- Service role key bypasses RLS — only use server-side, never expose to client
- Rate limiter resets on server restart (in-memory) — fine for Vercel, not for multi-instance
- Vercel env vars: set NEXT_PUBLIC_ prefix only for client-safe values
