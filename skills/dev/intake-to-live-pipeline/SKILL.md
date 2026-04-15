---
name: intake-to-live-pipeline
description: The ITP client onboarding pipeline from intake form submission to live Vapi agent.
category: dev
---

# Intake-to-Live Pipeline (ITP)

## When to Use
Building, debugging, or extending the automated client onboarding system that takes a new client from form submission to a live AI receptionist.

## Pipeline Overview

```
Intake Form (Next.js)
  -> Supabase: intake_submissions
    -> Iris: welcome email + Clerk org creation
      -> Scribe: script/system prompt generation
        -> Echo: Vapi agent build + test call
          -> Live (status = 'active')
```

## Steps

1. **Intake Form** — client fills Next.js form (business name, type, hours, FAQs, transfer number)
2. **Supabase insert** — row added to `intake_submissions` with `status: 'pending'`
3. **Iris polls** — detects pending -> sends welcome email (Resend) -> creates Clerk org -> updates `status: 'iris_complete'`
4. **Scribe polls** — detects iris_complete -> generates system prompt from intake data -> stores in `client_scripts` -> updates `status: 'scribe_complete'`
5. **Echo polls** — detects scribe_complete -> creates Vapi assistant -> runs test call -> updates `status: 'active'`

## Key Patterns / Code

### Supabase Project
```
Project ID: skmzjnxkoxdogntqbesu
Table: intake_submissions
Key columns: id, status, business_name, business_type, hours, transfer_number, script_id, vapi_assistant_id
```

### Agent Polling Pattern
```js
const { data: pending } = await supabase
  .from('intake_submissions')
  .select('*')
  .eq('status', 'pending')
  .limit(5);

for (const submission of pending) {
  try {
    await processSubmission(submission);
    await supabase
      .from('intake_submissions')
      .update({ status: 'iris_complete', updated_at: new Date() })
      .eq('id', submission.id);
  } catch (err) {
    await supabase.from('intake_submissions')
      .update({ status: 'error', error_msg: err.message })
      .eq('id', submission.id);
  }
}
```

### Status Flow
```
pending -> iris_complete -> scribe_complete -> active -> [churned | paused]
```

## Gotchas
- Each agent polls independently — no direct agent-to-agent calls, Supabase is the bus
- Status field is the handoff contract — never skip a status or two agents may double-process
- Scribe needs business_type + FAQs to generate a quality prompt — validate intake completeness upfront
- Echo must store vapi_assistant_id back to Supabase before marking active
- Test call on Echo step — never mark active until test call completes without error
- Service role key required for server-side Supabase writes (bypasses RLS)
- If a row gets stuck in error, fix root cause and manually reset status to re-trigger
