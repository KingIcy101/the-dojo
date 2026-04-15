---
name: nextjs-env-validation
description: Use when setting up environment variable validation in a Next.js project with Zod — prevents runtime surprises and broken Vercel builds.
category: dev
---
# Next.js Env Validation

## When to Use
Every Next.js project. Add this on day one. Catches missing env vars at startup rather than at runtime when a user hits the broken endpoint.

## Steps
1. `npm install zod`
2. Create `src/lib/env.ts` with server + client schemas
3. Replace all `process.env.X` references with `env.X`
4. Never use `process.env` directly in app code — always import from `env.ts`

## Key Patterns / Code

```ts
// src/lib/env.ts
import { z } from 'zod';

const serverSchema = z.object({
  // Required at runtime — will throw if missing when server starts
  OPENROUTER_API_KEY: z.string(),
  SUPABASE_SERVICE_ROLE_KEY: z.string(),
  RESEND_API_KEY: z.string(),
  STRIPE_SECRET_KEY: z.string(),
  CLERK_SECRET_KEY: z.string(),
  TELEGRAM_BOT_TOKEN: z.string(),

  // Has a safe default — NEVER block build for known URLs
  APP_URL: z.string().url().default('https://inthepast.ai'),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
});

const clientSchema = z.object({
  // Must be prefixed NEXT_PUBLIC_ or Next.js won't expose to client
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string(),
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: z.string(),
  NEXT_PUBLIC_APP_URL: z.string().url().default('https://inthepast.ai'),
});

// Parse — throws ZodError on missing/invalid vars
const serverEnv = serverSchema.parse(process.env);
const clientEnv = clientSchema.parse(process.env);

// Merge and export
export const env = { ...serverEnv, ...clientEnv };
```

```ts
// Usage in API route
import { env } from '@/lib/env';

const resend = new Resend(env.RESEND_API_KEY);
const appUrl = env.APP_URL; // typed, validated
```

```ts
// next.config.ts — expose to client bundle (redundant with NEXT_PUBLIC_ but explicit)
const nextConfig = {
  env: {
    APP_URL: process.env.APP_URL,
  },
};
```

## Vercel Build Rules
- Build-time required vars MUST have `.default()` or Vercel fails during `next build`
- Only add `.default()` when there's a real safe fallback — don't fake it
- Stripe secret key: leave as `z.string()` — if missing, build should fail
- Public URL: `z.string().url().default('https://inthepast.ai')` — safe default

## Gotchas
- `NEXT_PUBLIC_` prefix required for anything accessed in client components
- `env.ts` runs at module load time — import errors appear immediately on startup
- Don't call `z.parse()` inside a function — module-level parse catches it at boot
- Vercel: add all vars in Project Settings → Environment Variables before first deploy
- Local `.env.local` overrides `.env` — use `.env.local` for secrets, `.env` for defaults
- Never commit `.env.local` — it should be in `.gitignore` already
