---
name: posthog
description: >
  PostHog — product analytics, session recording, feature flags, A/B testing.
  Use in every client portal and app we build. Understand how users actually use the product.
  Self-hostable. Has a generous free tier. Replaces Mixpanel + LaunchDarkly + Hotjar.
---

# PostHog — Product Analytics

## What It Is
PostHog does what used to require 4 tools: analytics (Mixpanel), session recording (Hotjar), feature flags (LaunchDarkly), and A/B testing. One SDK, one dashboard, free tier handles 1M events/mo.

## Setup
```bash
npm install posthog-js  # browser
npm install posthog-node  # server/Node.js
```

### Browser (vanilla JS / HTML)
```js
import posthog from 'posthog-js'

posthog.init('phc_YOUR_PROJECT_API_KEY', {
  api_host: 'https://us.i.posthog.com',
  person_profiles: 'identified_only',
})
```

### Next.js (App Router)
```jsx
// providers/posthog.tsx
'use client'
import { usePathname, useSearchParams } from 'next/navigation'
import { useEffect } from 'react'
import posthog from 'posthog-js'
import { PostHogProvider } from 'posthog-js/react'

export function PHProvider({ children }) {
  useEffect(() => {
    posthog.init('phc_...', { api_host: 'https://us.i.posthog.com' })
  }, [])
  return <PostHogProvider client={posthog}>{children}</PostHogProvider>
}
```

## Core Tracking

### Identify Users
```js
// Call after login
posthog.identify(userId, {
  email: user.email,
  name: user.name,
  plan: 'pro',
  org: orgName,
})
```

### Track Events
```js
// Custom events
posthog.capture('campaign_viewed', {
  client_id: clientId,
  campaign_type: 'facebook_ads',
  spend: 1950,
})

posthog.capture('lead_generated', {
  source: 'facebook',
  cost_per_lead: 41,
})

posthog.capture('report_downloaded', {
  month: '2026-03',
  format: 'pdf',
})
```

### Feature Flags
```js
// Check flag
const showNewFeature = await posthog.isFeatureEnabled('new-dashboard-v2')

if (showNewFeature) {
  // Show new UI
} else {
  // Show old UI
}

// React hook
import { useFeatureFlagEnabled } from 'posthog-js/react'
function Component() {
  const enabled = useFeatureFlagEnabled('new-feature')
  return enabled ? <NewFeature /> : <OldFeature />
}
```

### A/B Testing
```js
// Get variant
const variant = posthog.getFeatureFlag('cta-button-test')
// variant: 'control' | 'test-green' | 'test-large'

// Track conversion
posthog.capture('cta_clicked', { variant })
```

### Server-Side (Node.js)
```js
import { PostHog } from 'posthog-node'
const client = new PostHog('phc_...', { host: 'https://us.i.posthog.com' })

// Track server event
client.capture({
  distinctId: userId,
  event: 'payment_processed',
  properties: { amount: 1950, currency: 'usd' }
})

// Always flush before exit
await client.shutdown()
```

## Session Recording
```js
// Enabled by default after init
// Records user sessions — replay in PostHog dashboard
// Automatically masks sensitive inputs (passwords, credit cards)

// Manually start/stop recording
posthog.startSessionRecording()
posthog.stopSessionRecording()
```

## Key Events to Track (Our Builds)

### Mission Control
```js
posthog.capture('page_view', { page: 'dashboard' })
posthog.capture('brain_dump_submitted', { category: 'delegate', count: 3 })
posthog.capture('atlas_task_approved', { task_type: 'email' })
posthog.capture('pomo_started', { duration_min: 25 })
```

### Client Portals (Halo)
```js
posthog.capture('report_viewed', { client_id, month })
posthog.capture('lead_count_checked', { client_id, leads: 47 })
posthog.capture('support_message_sent', { client_id })
```

## Environment Variables
```env
NEXT_PUBLIC_POSTHOG_KEY=phc_...
NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
```

## Best Use Cases for Our Builds
- **Mission Control** — track which features Matt actually uses
- **Client portals** — understand how practitioners interact with their dashboards
- **AI agency** — funnel analytics, where users drop off in onboarding
- **Halo landing** — A/B test CTAs, headlines, pricing display

## Skill Injection for Codex/Claude Code
```
Use PostHog (posthog-js) for analytics. Init with NEXT_PUBLIC_POSTHOG_KEY.
Identify users after login. Track key actions with posthog.capture().
Feature flags for safe rollouts. Session recording enabled by default.
Key events: page_view, user_action, conversion events for each app.
```


## Learned In Use

- **2026-03-18:** Obsidian graph visualization (colors, layout) does not affect AI agent search or functionality — folder structure matters for organization, colors are purely for human readability in graph view.

## Learned from Use (2026-03-29)
SKIP

The session logs show extensive detail about Client Portal v1 development, QA cycles, agent coordination, and memory management—but there are no mentions of the "posthog" skill being used, tested, or causing any corrections. The logs reference Clerk authentication, Vapi API integration, RLS SQL, typography fixes, and deployment processes, but no PostHog analytics instrumentation or usage patterns.

To extract learned lessons about PostHog, I would need session records that actually invoke or discuss the skill.
