---
name: stripe-saas-billing
description: Set up Stripe subscriptions, webhooks, and customer portal for SaaS billing with org_id metadata.
category: dev
---

# Stripe SaaS Billing

## When to Use
Any app that charges recurring fees. Covers product/price/payment link setup, webhook handling, customer portal,
and idempotent subscription creation. Always use metadata to link Stripe customers to your org_id.

## Steps
1. Create Product + Price in Stripe dashboard (or via API)
2. Add webhook endpoint, listen for key events
3. On `checkout.session.completed` → provision access in DB
4. On `invoice.payment_failed` → flag account, send dunning email
5. Customer portal for self-serve upgrades/cancellations

## Key Patterns / Code

### Create Product + Payment Link
```bash
# Via Stripe CLI
stripe products create --name="ITP Standard" --description="AI Receptionist - Standard Plan"
stripe prices create --product=prod_xxx --unit-amount=110000 --currency=usd --recurring[interval]=month
stripe payment_links create --line-items[0][price]=price_xxx --line-items[0][quantity]=1
```

### Webhook Handler
```ts
// app/api/webhooks/stripe/route.ts
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const sig = req.headers.get('stripe-signature')!;
  const body = await req.text();
  const event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;
      const orgId = session.metadata?.org_id;
      await db.orgs.update({ stripeCustomerId: session.customer, active: true }, { where: { id: orgId } });
      break;
    }
    case 'invoice.payment_succeeded':
      // Extend access period
      break;
    case 'invoice.payment_failed':
      // Flag account, trigger dunning sequence
      break;
    case 'customer.subscription.deleted':
      // Revoke access
      await db.orgs.update({ active: false }, { where: { stripeCustomerId: event.data.object.customer } });
      break;
  }
  return Response.json({ received: true });
}
```

### Subscription with Idempotency + Metadata
```ts
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: process.env.STRIPE_PRICE_ID }],
  metadata: { org_id: orgId },
  expand: ['latest_invoice.payment_intent'],
}, {
  idempotencyKey: `sub-create-${orgId}`, // prevents double charges on retry
});
```

### Customer Portal
```ts
const session = await stripe.billingPortal.sessions.create({
  customer: stripeCustomerId,
  return_url: 'https://app.inthepast.ai/settings/billing',
});
redirect(session.url);
```

### Test Mode vs Live Mode
```bash
# .env
STRIPE_SECRET_KEY=sk_test_xxx       # test
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx     # from `stripe listen --forward-to localhost:3000/api/webhooks/stripe`

# Production
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_yyy     # from Stripe dashboard webhook endpoint
```

## Gotchas
- Webhook secret is different for local (`stripe listen`) vs production (dashboard endpoint)
- Always use `req.text()` not `req.json()` for webhook body — signature verification requires raw bytes
- Idempotency keys expire after 24h — use a meaningful key tied to the action, not a random UUID
- `customer.subscription.deleted` fires on immediate cancel AND at period end — check `cancel_at_period_end`
- Payment links don't support metadata by default — use Checkout Sessions API for metadata
- Test cards: 4242 4242 4242 4242 (success), 4000 0000 0000 0002 (decline)