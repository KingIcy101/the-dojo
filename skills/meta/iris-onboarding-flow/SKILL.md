---
name: iris-onboarding-flow
description: Use when Iris needs to onboard a new In The Past AI client — triggered by intake submission, runs 6-step sequence.
category: meta
---
# Iris Onboarding Flow

## When to Use
Triggered automatically when a new row appears in `intake_submissions` table (Supabase project: skmzjnxkoxdogntqbesu). Iris runs this sequence for every new client.

## Steps
1. Send welcome email via Resend (from hello@inthepast.ai)
2. Create Clerk organization (org name = `business_name`)
3. Invite client email to Clerk org
4. Create Supabase `clients` row with `org_id`
5. Notify Scribe to generate script (post to #scribe)
6. Post summary to Discord #agency-team-chat

**Error handling:** If Clerk org creation fails → retry once → if still fails, alert Matt via Telegram immediately.

## Key Patterns / Code

```ts
// Trigger: Supabase Realtime on intake_submissions INSERT
supabase.channel('intake-trigger')
  .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'intake_submissions' },
    async (payload) => { await runOnboarding(payload.new as IntakeSubmission); })
  .subscribe();
```

```ts
// Step 1: Welcome email
await resend.emails.send({
  from: 'hello@inthepast.ai',
  to: intake.email,
  subject: `Welcome to In The Past AI, ${intake.owner_name}!`,
  html: welcomeEmailHtml(intake),
});
```

```ts
// Step 2-3: Clerk org + invite
let orgId: string;
try {
  const org = await clerkClient.organizations.createOrganization({
    name: intake.business_name,
    createdBy: IRIS_CLERK_USER_ID,
  });
  orgId = org.id;
} catch (err) {
  // Retry once
  await new Promise(r => setTimeout(r, 2000));
  try {
    const org = await clerkClient.organizations.createOrganization({ name: intake.business_name, createdBy: IRIS_CLERK_USER_ID });
    orgId = org.id;
  } catch (retryErr) {
    await alertMattTelegram(`Iris: Clerk org creation failed for ${intake.business_name} — manual action needed`);
    throw retryErr;
  }
}

await clerkClient.organizations.createOrganizationInvitation({
  organizationId: orgId,
  emailAddress: intake.email,
  role: 'org:member',
  redirectUrl: 'https://portal.inthepast.ai',
});
```

```ts
// Step 4: Supabase client row
await supabase.from('clients').insert({
  org_id: orgId,
  business_name: intake.business_name,
  email: intake.email,
  owner_name: intake.owner_name,
  industry: intake.industry,
  intake_id: intake.id,
  status: 'onboarding',
});
```

```ts
// Steps 5-6: Notify Scribe + Discord
await discordPost('#scribe', `New client: ${intake.business_name} (${intake.industry}) — generate script for intake ${intake.id}`);
await discordPost('#agency-team-chat', `✅ Onboarding complete: **${intake.business_name}** — org created, invite sent, Scribe notified`);
```

## Gotchas
- Supabase project: `skmzjnxkoxdogntqbesu` — use this in env, not a different project
- Clerk org name = `business_name` exactly — no sanitization, Clerk handles special chars
- Always create Supabase row AFTER Clerk org — `org_id` foreign key required
- Welcome email from `hello@inthepast.ai` — Resend domain must be verified
- If intake has no `owner_name`, fall back to `email` in greeting
- Discord posts are non-blocking — fire and forget, don't await for critical path
