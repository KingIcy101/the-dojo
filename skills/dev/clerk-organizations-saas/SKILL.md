---
name: clerk-organizations-saas
description: Set up Clerk Organizations for multi-tenant SaaS — create orgs on intake, JWT for Supabase, role-based access.
category: dev
---

# Clerk Organizations for Multi-Tenant SaaS

## When to Use
Any SaaS app where one account = one business (client portal, agency dashboard, multi-location).
Clerk Organizations handle tenant isolation. Pair with Supabase RLS using org_id claim.

## Steps
1. Enable Organizations in Clerk dashboard → Organizations
2. Create org on user signup (webhook or intake flow)
3. Add JWT template with org_id claim for Supabase
4. Use `getAuth()` server-side, `useAuth()` client-side
5. Add `<OrganizationSwitcher>` for multi-org users

## Key Patterns / Code

### Create Org on Intake
```ts
// app/api/onboard/route.ts
import { auth, clerkClient } from '@clerk/nextjs/server';

export async function POST(req: Request) {
  const { userId } = auth();
  const { businessName } = await req.json();

  // Create org
  const org = await clerkClient.organizations.createOrganization({
    name: businessName,
    createdBy: userId,
  });

  // Set plan metadata
  await clerkClient.organizations.updateOrganizationMetadata(org.id, {
    publicMetadata: { plan: 'standard', setupComplete: false },
  });

  // Auto-create Supabase row
  await supabase.from('organizations').insert({
    clerk_org_id: org.id,
    name: businessName,
    plan: 'standard',
  });

  return Response.json({ orgId: org.id });
}
```

### JWT Template for Supabase (include org_id)
In Clerk Dashboard → JWT Templates → New → Supabase:
```json
{
  "role": "authenticated",
  "sub": "{{user.id}}",
  "email": "{{user.primary_email_address}}",
  "org_id": "{{org.id}}",
  "org_role": "{{org.role}}"
}
```

### Server-side Auth (App Router)
```ts
import { auth } from '@clerk/nextjs/server';

export async function GET() {
  const { userId, orgId, orgRole } = auth();
  if (!orgId) return Response.json({ error: 'No org' }, { status: 403 });
  // Query Supabase with orgId for tenant isolation
}
```

### Client-side Auth
```tsx
import { useAuth, useOrganization } from '@clerk/nextjs';

export function Dashboard() {
  const { orgId, orgRole } = useAuth();
  const { organization, membership } = useOrganization();
  // orgRole: 'org:admin' | 'org:member'
}
```

### OrganizationSwitcher (Multi-org portals)
```tsx
import { OrganizationSwitcher } from '@clerk/nextjs';
<OrganizationSwitcher
  afterSelectOrganizationUrl="/dashboard"
  afterCreateOrganizationUrl="/onboarding"
/>
```

### Webhook: user.created → Supabase row
```ts
// app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix';
export async function POST(req: Request) {
  const evt = webhook.verify(body, headers); // verify with CLERK_WEBHOOK_SECRET
  if (evt.type === 'user.created') {
    await supabase.from('users').insert({ clerk_id: evt.data.id, email: evt.data.email_addresses[0].email_address });
  }
}
```

## Gotchas
- JWT template name must match what Supabase client uses: `supabase.auth.setSession({ access_token: await getToken({ template: 'supabase' }) })`
- `org.role` in JWT is `org:admin` not just `admin` — check prefix in RLS policies
- OrganizationSwitcher requires `afterSelectOrganizationUrl` or page won't reload on switch
- `publicMetadata` is readable client-side; `privateMetadata` is server-only
- Supabase RLS: `auth.jwt()->>'org_id' = organizations.clerk_org_id`