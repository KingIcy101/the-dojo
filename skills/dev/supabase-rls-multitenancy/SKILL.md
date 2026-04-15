---
name: supabase-rls-multitenancy
description: Row-level security patterns for multi-tenant SaaS on Supabase — JWT claims, isolation testing, Realtime.
category: dev
---

# Supabase RLS Multi-Tenancy

## When to Use
Any Supabase-backed SaaS with multiple orgs/clients sharing the same database tables. Ensures one tenant cannot read or write another's data.

## Steps

1. Enable RLS on every table
2. Configure JWT claim source (Clerk or custom)
3. Write policies for SELECT / INSERT / UPDATE / DELETE
4. Test isolation with two real users
5. Enable Realtime only on tables that need it (policies apply to subscriptions)

## Key Patterns / Code

### Enable RLS
```sql
ALTER TABLE call_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE intake_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE client_scripts ENABLE ROW LEVEL SECURITY;
-- Repeat for every table
```

### JWT Claim Policy (Clerk org_id)
```sql
-- SELECT isolation
CREATE POLICY "tenant_select" ON call_logs
  FOR SELECT USING (auth.jwt() ->> 'org_id' = org_id);

-- INSERT isolation
CREATE POLICY "tenant_insert" ON call_logs
  FOR INSERT WITH CHECK (auth.jwt() ->> 'org_id' = org_id);

-- UPDATE + DELETE
CREATE POLICY "tenant_update" ON call_logs
  FOR UPDATE USING (auth.jwt() ->> 'org_id' = org_id);

CREATE POLICY "tenant_delete" ON call_logs
  FOR DELETE USING (auth.jwt() ->> 'org_id' = org_id);
```

### Service Role Bypass (server-side only)
```ts
// NEVER send service key to browser
const adminClient = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);
// RLS is bypassed — use for pipeline agents, cron jobs, admin ops
```

### Anon Client (respects RLS)
```ts
const client = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
  global: { headers: { Authorization: `Bearer ${jwtFromClerk}` } },
});
```

### Testing Isolation (manual)
```
1. Create User A (org: org_aaa) — insert 3 rows
2. Create User B (org: org_bbb) — insert 3 rows
3. Log in as User A → SELECT * from table → should return 3 rows, not 6
4. Attempt INSERT with org_id = 'org_bbb' while authed as A → should fail
```

### Realtime + RLS
```sql
-- Must enable replication on the table
ALTER PUBLICATION supabase_realtime ADD TABLE call_logs;
-- Policies still apply — user only receives events for rows they can SELECT
```

### Check RLS is Enabled
```sql
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';
-- rowsecurity = true means RLS is on
```

## Gotchas
- Forgetting to enable RLS on a new table = all rows exposed to any authenticated user
- Service role bypasses ALL policies — never leak to client-side
- Realtime events respect RLS, but you must add the table to supabase_realtime publication
- `auth.jwt()` returns the full JWT; `->> 'org_id'` extracts string claim
- Clerk requires a custom JWT template in dashboard: add `org_id` from `{{org.id}}`
- Anonymous users have no JWT claims — deny all or add explicit anon policy
- Policy evaluation is per-row and adds query overhead — index org_id columns
