---
name: sentry
description: >
  Sentry — error monitoring, performance tracking, session replay. Catches crashes before clients do.
  Add to every app we ship. Free tier: 5K errors/mo. One-line setup in Next.js.
---

# Sentry — Error Monitoring

## Setup
```bash
npx @sentry/wizard@latest -i nextjs
# Automated setup — adds config files, installs package, updates next.config.js
```

## Manual Setup
```bash
npm install @sentry/nextjs
```

```js
// sentry.client.config.js
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  enabled: process.env.NODE_ENV === 'production',
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.2,          // 20% performance monitoring
  replaysSessionSampleRate: 0.1,  // 10% session replay
  replaysOnErrorSampleRate: 1.0,  // 100% replay on error
  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,   // privacy
      blockAllMedia: true,
    }),
    Sentry.browserTracingIntegration(),
  ],
  ignoreErrors: [
    'ResizeObserver loop limit exceeded',
    'Non-Error exception captured',
  ],
  release: process.env.npm_package_version,
})
```

```js
// sentry.server.config.js
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  enabled: process.env.NODE_ENV === 'production',
  tracesSampleRate: 0.2,
})
```

## Manual Error Capture
```js
// Capture any error manually
try {
  await riskyOperation()
} catch (err) {
  Sentry.captureException(err, {
    tags: { component: 'payment', client_id: clientId },
    extra: { amount: 1950, email: client.email }
  })
  throw err
}

// Capture a message (non-error event)
Sentry.captureMessage('GHL sync failed', 'warning')

// Add context (shows in Sentry dashboard)
Sentry.setUser({ id: userId, email: user.email })
Sentry.setTag('org', orgId)
Sentry.setContext('client', { name: clientName, plan: 'pro' })
```

## Next.js Error Boundary
```jsx
// app/global-error.tsx (auto-created by wizard)
'use client'
import * as Sentry from '@sentry/nextjs'
import { useEffect } from 'react'

export default function GlobalError({ error }) {
  useEffect(() => {
    Sentry.captureException(error)
  }, [error])

  return <html><body><h2>Something went wrong</h2></body></html>
}
```

## Performance Monitoring
```js
// Manual transaction
const transaction = Sentry.startTransaction({ name: 'generate-report' })
try {
  await generateReport()
} finally {
  transaction.finish()
}
```

## Environment Variables
```env
NEXT_PUBLIC_SENTRY_DSN=https://...@sentry.io/...
SENTRY_AUTH_TOKEN=   # for source map uploads (get from Sentry dashboard)
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project
```

## next.config.js Integration
```js
import { withSentryConfig } from '@sentry/nextjs'

export default withSentryConfig(nextConfig, {
  org: 'your-org',
  project: 'your-project',
  authToken: process.env.SENTRY_AUTH_TOKEN,
  tunnelRoute: '/monitoring', // bypass ad blockers
  silent: !process.env.CI,
})
```

## Skill Injection for Codex/Claude Code
```
Add Sentry to every production app. npx @sentry/wizard@latest -i nextjs for auto-setup.
Capture errors: Sentry.captureException(err) in all catch blocks.
Set user context after auth: Sentry.setUser({ id, email }).
tracesSampleRate: 0.2, replaysOnErrorSampleRate: 1.0 (always replay on errors).
DSN from NEXT_PUBLIC_SENTRY_DSN env var.
```


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Sentry caught pipeline skips before production damage** — Portal was deployed without Pixel review or Judge audit; sentry role (Judge agent) caught 3 font violations + Vapi wiring gaps + security issues. The correction rule now enforces: every build must complete Pixel → Forge → Pixel → Judge → Core, no exceptions, even when "build looks done."

- **Sentry execution depends on routing** — Judge couldn't act on #dev-team-chat messages because they don't trigger agent tool access; only private channel messages do. Workaround was spawning Judge as subagent with test credentials. Future: Cyrus routing system will fix this, but sentry effectiveness is blocked by message routing until then.

- **Sentry role clarity prevents coordination failures** — Initially tried posting pipeline sync to Forge's private channel (#forge) instead of #dev-team-chat; agents couldn't coordinate. Rule: #dev-team-chat for cross-agent coordination, private channels for agent's own work only. Sentry needs visibility into the right channel to catch issues.

- **Sentry approval gates deployment** — Round 3 and 4 Judge audits found fixable violations (font sizes, Clerk theme bleed) before ship. Pattern: if sentry hasn't signed off, deployment doesn't proceed — this prevented shipping broken state twice.
