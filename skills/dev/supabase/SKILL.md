---
name: supabase
description: >
  Supabase — open source Firebase alternative. Postgres DB, Auth, Realtime, Storage, Edge Functions.
  Use for every client portal, multi-tenant app, and SaaS build. The backend stack for AI agency.
  Stack with Clerk (auth) and Stripe (payments) for full SaaS infrastructure.
---

# Supabase — Full Backend Stack

## ⚠️ RLS IS MANDATORY — DAY ONE (non-negotiable, agreed 2026-03-18)
Before writing any data or building any UI on top of Supabase:
1. Enable RLS on EVERY table immediately after creation
2. Write read/insert/update/delete policies before any data goes in
3. Test with a second account to confirm user isolation
4. Never rely on frontend checks — enforce at DB level only
5. Multi-tenant: user A must never see or affect user B's data
6. Permissions/pricing tiers must be DB-enforced — users cannot edit their own tier

Not doing this is not an option.

## What It Is
Supabase is the backend for every serious app we build. Postgres database + real-time subscriptions + auth + file storage + edge functions — all in one. Used by Vercel, GitHub, Mozilla. Free tier is generous.

## Setup
```bash
npm install @supabase/supabase-js
```
```js
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
)
```

## Core Operations

### Database (CRUD)
```js
// SELECT
const { data, error } = await supabase
  .from('clients')
  .select('id, name, mrr, status')
  .eq('status', 'active')
  .order('mrr', { ascending: false })

// INSERT
const { data, error } = await supabase
  .from('clients')
  .insert({ name: 'Renee', mrr: 950, status: 'active' })
  .select()

// UPDATE
await supabase.from('clients').update({ mrr: 1950 }).eq('id', clientId)

// DELETE
await supabase.from('clients').delete().eq('id', clientId)

// UPSERT (insert or update)
await supabase.from('clients').upsert({ id: 1, name: 'Renee', mrr: 1950 })
```

### Auth
```js
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'client@example.com',
  password: 'securepassword',
})

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'client@example.com',
  password: 'securepassword',
})

// Get current user
const { data: { user } } = await supabase.auth.getUser()

// Sign out
await supabase.auth.signOut()

// OAuth (Google, GitHub)
await supabase.auth.signInWithOAuth({ provider: 'google' })
```

### Realtime (live updates)
```js
// Subscribe to table changes
const channel = supabase
  .channel('clients-changes')
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'clients' },
    (payload) => {
      console.log('Change:', payload)
      // Update UI in real time
    }
  )
  .subscribe()

// Cleanup
supabase.removeChannel(channel)
```

### Storage (file uploads)
```js
// Upload
const { data, error } = await supabase.storage
  .from('assets')
  .upload('avatars/client-1.jpg', file, { upsert: true })

// Get public URL
const { data: { publicUrl } } = supabase.storage
  .from('assets')
  .getPublicUrl('avatars/client-1.jpg')

// Download
const { data, error } = await supabase.storage
  .from('assets')
  .download('report.pdf')
```

### Row Level Security (RLS) — Multi-tenant pattern
```sql
-- Enable RLS
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;

-- Users only see their own org's data
CREATE POLICY "org_isolation" ON clients
  FOR ALL USING (org_id = auth.jwt() ->> 'org_id');
```

## Multi-Tenant Pattern (AI Agency Portals)
```js
// Each client gets their own org_id
// All queries automatically scoped via RLS
// No manual filtering needed — Postgres handles it

const supabase = createClient(url, key, {
  global: {
    headers: { 'x-org-id': orgId } // injected from Clerk JWT
  }
})
```

## Environment Variables
```env
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_ANON_KEY=eyJ...  (safe to expose in browser)
SUPABASE_SERVICE_KEY=eyJ... (server-side only, full access)
```

## Best Use Cases for Our Builds
- **AI agency client portals** — multi-tenant, each client isolated via RLS
- **Mission Control** — replace JSON files with real Postgres
- **Lead database** — store + query scraped leads
- **Halo Marketing CRM** — clients, campaigns, metrics
- **Velora dashboard** — Vanessa's project data

## Skill Injection for Codex/Claude Code
```
Use Supabase (@supabase/supabase-js) for all database/auth/storage.
Multi-tenant: RLS policies on every table, org_id from Clerk JWT.
Realtime: postgres_changes subscriptions for live dashboards.
Env: SUPABASE_URL + SUPABASE_ANON_KEY (browser) / SUPABASE_SERVICE_KEY (server).
```


## Learned from Use (2026-03-22)
SKIP

The session logs contain no mentions of Supabase being used, configured, queried, or troubleshot. The "supabase" skill tag appears to be applied to this session, but the actual activity documented focuses on Vercel deployments, Three.js rendering, Forge builds, and Obsidian sync—none of which involved Supabase interactions.

There are no corrections, errors, or decisions related to Supabase usage to extract lessons from.


## Learned In Use

- **2026-03-24:** Voice agent startup sequences must read 6 files in exact order (QUICK-REF → MEMORY → hot-context → handoff → daily log → corrections) for proper context recovery, especially post-compaction.

## Learned from Use (2026-03-29)
SKIP

The session logs show extensive work on the Client Portal v1 build (typography fixes, Clerk authentication, Vapi API integration, security hardening, RLS migration), but there are no specific mentions of the "supabase" skill being used, tested, corrected, or creating issues. The logs reference "Core RLS SQL for scoped access" and "RLS migration SQL" as blockers/completed tasks, but no actual supabase skill execution, errors, or feedback loops are documented. Without concrete evidence of the skill being applied and either succeeding or failing in a way that generated a correction or learning, there's nothing actionable to extract for a lessons section.

- **2026-03-29:** When auto-linking Clerk users to Supabase records, the email match must be exact — clients created in Iris must have email matching portal sign-up email character-for-character.

## Learned from Use (2026-04-05)
SKIP

The session logs provided contain no mentions of the "supabase" skill being used. The logs focus on Gemini API configuration, OpenClaw agent setup, Discord integrations, and the Halo Portal project—none of which involve Supabase interactions. There are no correction patterns, approval notes, or use cases documented for the supabase skill in these recent sessions.


## Learned from Use (2026-04-12)
SKIP

**Reason:** The session logs contain no mentions of Supabase skill usage, errors, corrections, or patterns. The logs focus on AI model provider issues (Anthropic, Google, Discord/Telegram sessions), project management blockers (Auralux, Cyrus, ZTA), and context/handoff procedures. There is no data showing how Supabase was actually used, what worked or failed, or what corrections were applied to its usage.
