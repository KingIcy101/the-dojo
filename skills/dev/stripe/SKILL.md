---
name: stripe
description: >
  Stripe — payments, subscriptions, invoicing. Use for any app that charges money.
  Covers one-time payments, recurring subscriptions, webhooks, customer portal.
  Stack with Supabase (database) and Clerk (auth) for full SaaS billing.
---

# Stripe — Payments & Subscriptions

## Setup
```bash
npm install stripe @stripe/stripe-js
```
```js
// Server-side
import Stripe from 'stripe'
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)

// Client-side (browser)
import { loadStripe } from '@stripe/stripe-js'
const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY)
```

## Core Patterns

### One-Time Payment (Checkout Session)
```js
// Server: create session
const session = await stripe.checkout.sessions.create({
  payment_method_types: ['card'],
  line_items: [{
    price_data: {
      currency: 'usd',
      product_data: { name: 'Halo Marketing Setup Fee' },
      unit_amount: 195000, // $1,950.00 in cents
    },
    quantity: 1,
  }],
  mode: 'payment',
  success_url: `${domain}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${domain}/cancel`,
  customer_email: client.email,
})

// Redirect client
res.redirect(303, session.url)
```

### Recurring Subscription
```js
// Create subscription
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{ price: 'price_monthly_1950' }], // price ID from Stripe dashboard
  payment_behavior: 'default_incomplete',
  expand: ['latest_invoice.payment_intent'],
})
```

### Customer Portal (self-serve billing)
```js
const session = await stripe.billingPortal.sessions.create({
  customer: customerId,
  return_url: `${domain}/dashboard`,
})
res.redirect(303, session.url)
```

### Webhooks (critical — sync Stripe → DB)
```js
// Next.js API route: /api/webhooks/stripe
import { headers } from 'next/headers'

export async function POST(req) {
  const body = await req.text()
  const signature = headers().get('stripe-signature')

  let event
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET)
  } catch (err) {
    return new Response(`Webhook error: ${err.message}`, { status: 400 })
  }

  switch (event.type) {
    case 'checkout.session.completed':
      // Payment received — activate client
      await activateClient(event.data.object)
      break
    case 'invoice.payment_failed':
      // Payment failed — notify + pause service
      await handleFailedPayment(event.data.object)
      break
    case 'customer.subscription.deleted':
      // Cancelled — downgrade/remove access
      await cancelSubscription(event.data.object)
      break
  }

  return new Response('OK', { status: 200 })
}
```

### Create Customer
```js
const customer = await stripe.customers.create({
  email: 'client@example.com',
  name: 'Dr. Renee Smith',
  metadata: { halo_client_id: '123', practice: 'chiro' }
})
```

### Retrieve Payment Info
```js
// Get all subscriptions for a customer
const subscriptions = await stripe.subscriptions.list({
  customer: customerId,
  status: 'active',
})

// Get upcoming invoice
const invoice = await stripe.invoices.retrieveUpcoming({
  customer: customerId,
})
```

## Halo Marketing Pricing Config
```js
// Prices to create in Stripe dashboard:
const PRICES = {
  standard: 'price_standard_1950',    // $1,950/mo — dental, chiro
  telehealth: 'price_telehealth_2950', // $2,950/mo — telehealth
  exception: 'price_exception_950',    // $950/mo — existing exceptions
}
```

## Environment Variables
```env
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Best Use Cases for Our Builds
- **Halo Marketing** — client subscriptions ($950–$2,950/mo)
- **AI agency** — project payments + monthly retainers
- **SourceDart** — user subscriptions for sourcing tool
- **Any SaaS** — payment + subscription + customer portal

## Skill Injection for Codex/Claude Code
```
Use Stripe for all payments. npm install stripe @stripe/stripe-js.
Always implement webhooks — never trust client-side payment confirmation.
Prices in cents (1950 USD = 195000). Use Checkout Sessions for simplicity.
Webhook events: checkout.session.completed, invoice.payment_failed, customer.subscription.deleted.
```


## Learned from Use (2026-03-22)
SKIP

The session logs contain no mentions of the "stripe" skill being used. The logs document deployment issues with Vercel, Agent Lounge frontend development, Obsidian sync tasks, and Codex briefing corrections—but there are no references to Stripe payments, billing, subscriptions, or any Stripe-related operations that would provide actionable lessons about using the stripe skill.


## Learned from Use (2026-03-29)
SKIP

The session logs contain no mentions of the "stripe" skill being used. The logs document work on Client Portal v1 (typography fixes, Clerk authentication, QA audits, deployment), but do not reference Stripe or any payment-related functionality. Without actual usage data for the stripe skill, I cannot extract specific lessons about what worked, what caused corrections, or patterns discovered during its use.


## Learned from Use (2026-04-05)
SKIP

**Reason:** The session logs provided contain no mentions of the "stripe" skill being used, tested, or discussed. The logs focus on OpenClaw agent configuration, Gemini API setup, Halo Portal builds, and Discord integration. There are no corrections, failures, or approvals related to stripe functionality. Cannot extract actionable lessons about a skill with zero recorded usage in these sessions.


## Learned from Use (2026-04-12)
SKIP

The session logs provided contain no mentions of the "stripe" skill being used, tested, or corrected. The logs focus on infrastructure issues (rate limits, model availability, billing), project management status (Auralux, Cyrus, ZTA), and general workflow corrections (handoff documentation, task context). There are no specific interactions, failures, or successes with stripe to extract lessons from.
