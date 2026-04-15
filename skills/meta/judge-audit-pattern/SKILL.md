---
name: judge-audit-pattern
description: Judge's visual audit workflow — score pages 0-1, SHIP at ≥0.85, REJECT triggers Forge fix pass, one verdict post.
category: meta
---

# Judge Visual Audit Pattern

## When to Use
Before any UI/frontend deploy. Forge completes build → tags Judge → Judge audits → posts verdict.
Never deploy on REJECT. Never spam #dev-team-chat with partial updates.

## Steps
1. Spawn Judge as subagent with test credentials + live/preview URL
2. Judge screenshots every page state: empty, loaded, error, mobile
3. Judge scores each view 0.0-1.0
4. SHIP (avg ≥0.85) → done, Core triggers deploy
5. REJECT → Judge lists IMPROVEMENTS → Forge fixes in ONE pass → re-audit

## Key Patterns / Code

### Spawn Judge (from Forge or Alo)
```js
const brief = fs.readFileSync('SUBAGENT_BRIEF.md', 'utf8');
const auditTask = `${brief}

---

## YOUR TASK: Visual Audit — ITP Client Portal v1.2

**URL:** https://itp-portal-preview.vercel.app
**Credentials:** test@inthepast.ai / TestPass123!

**Pages to audit:**
1. /dashboard (empty state + loaded state)
2. /settings/billing (Stripe portal link)
3. /onboarding (step 1-3 flow)
4. Mobile: /dashboard at 375px width

**Score each 0.0-1.0. Criteria:**
- No overflow/clipping
- No emojis in UI text
- Data accuracy (no hardcoded values)
- Mobile responsive
- Empty states handled

**Verdict format:**
SHIP if avg ≥0.85 → post one message to #dev-team-chat
REJECT if avg <0.85 → post IMPROVEMENTS list tagging @Forge

**Telegram at end:** [standard notification command]
`;

sessions_spawn({ runtime: 'subagent', mode: 'run', task: auditTask });
```

### Judge Verdict Format (Discord)
```
✅ SHIP — ITP Portal v1.2 (avg: 0.91)
- /dashboard loaded: 0.95
- /dashboard empty: 0.88
- /settings/billing: 0.90
- /onboarding: 0.92
- Mobile /dashboard: 0.88

Ready for production deploy.
```

```
❌ REJECT — ITP Portal v1.2 (avg: 0.74)
- /dashboard loaded: 0.90
- /dashboard empty: 0.45 ← hardcoded "0 clients" not handled
- /settings/billing: 0.72 ← billing portal link 404s
- Mobile: 0.88

IMPROVEMENTS (fix in one pass):
1. Empty state: show "No clients yet" card when array is empty
2. Billing: fix STRIPE_CUSTOMER_PORTAL_URL env var (not set in prod)
@Forge — fix and re-tag when done
```

### Judge Does NOT
- Request Core to deploy (that's Core's trigger on SHIP)
- Post multiple messages during audit (one consolidated verdict only)
- Audit without test credentials + URL in prompt
- Approve anything scoring <0.85

### Scoring Rubric
| Score | Meaning |
|-------|---------|
| 0.95-1.0 | Perfect — pixel perfect, no issues |
| 0.85-0.94 | SHIP — minor cosmetic issues, no blockers |
| 0.70-0.84 | REJECT — noticeable issues, fix required |
| <0.70 | REJECT — significant bugs or broken states |

## Gotchas
- Judge needs real preview URL with data — staging with seed data preferred
- Always specify mobile viewport (375px) as separate audit point
- Empty states are commonly missed — explicitly ask Judge to check them
- Judge scoring is subjective — calibrate with examples in SUBAGENT_BRIEF.md over time
- One verdict post per audit — never interim updates that clutter the channel