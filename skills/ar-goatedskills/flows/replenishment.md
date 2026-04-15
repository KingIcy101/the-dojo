# Replenishment

## Overview

**Trigger:** Time-based — calculated from purchase date + average product usage cycle
**Goal:** Drive a reorder before the customer runs out and defaults to a competitor or grocery store alternative
**Length:** 3 emails centered around the predicted depletion date
**Exit:** Repeat purchase or subscription signup exits immediately
**CVR target:** 20-35%

**Primary insight:** Customers are lost at the point of running out. If you don't reach them before depletion, they make a passive decision — and it's usually not you.

---

## Timing Calculation

Before building this flow, establish:

1. **Average usage rate** — how often does a typical customer use the product?
2. **Units per package** — how many uses per unit purchased?
3. **Predicted depletion day** — units ÷ usage rate = days until empty
4. **Email trigger point** — send first email 7-10 days before predicted depletion

**Example framework:**
- Product lasts 30 days at average usage → Email 1 at Day 20, Email 2 at Day 27, Email 3 at Day 32

**Build this as a profile property in your ESP** so timing adjusts dynamically per customer based on quantity purchased.

---

## Email 1 — 7-10 days before predicted depletion
**Subject angle:** Anticipatory reminder — "You might be getting low"
**Preview text:** "Based on typical use, you're probably running low on [product]"

**Copy angle:**
- Helpful framing: "Based on normal use, you've got about [X] days of [product] left"
- No urgency yet — informational and friendly
- "Most customers who loved their first [package] order now so they don't have a gap"
- Subscribe-and-save pitch: primary CTA (highest-leverage subscription conversion moment)
- Easy one-click reorder: secondary CTA

**CTA (primary):** Subscribe and save [X]% / Never run out
**CTA (secondary):** Reorder [product]

---

## Email 2 — 2-4 days before predicted depletion
**Subject angle:** Urgency — "You're almost out"
**Preview text:** "Ships in [X] days — arrives just in time"

**Copy angle:**
- Direct: "Order today and it arrives before you run out"
- Loss framing: what happens when they run out (lose progress, break routine, restart from scratch)
- Results reinforcement: "You've been [benefit] for [X] days. Don't break the streak."
- Subscribe-and-save as primary option
- Shipping timeline clarity

**CTA:** Reorder now — ships today / Subscribe and never run out

---

## Email 3 — 1-2 days after predicted depletion
**Subject angle:** "Did you run out?" / Last call
**Preview text:** "We're ready to ship today"

**Copy angle:**
- Acknowledge they've probably already run out
- No guilt — practical and helpful
- "If you're using [competitor] while you wait — we get it. But we're ready to ship today."
- Best offer of the sequence: free shipping or small discount
- Subscribe-and-save pitch: "Solve this permanently — auto-ship delivers before you run low"

**CTA:** Reorder [product] — ships today / Get auto-ship set up

---

## Subscribe-and-Save Conversion Strategy

Replenishment flow is the highest-converting moment to turn one-time buyers into subscribers:

| Email | Subscription pitch |
|-------|-------------------|
| Email 1 | Lead with subscription as primary CTA |
| Email 2 | "Most customers who reorder twice switch to auto-ship" |
| Email 3 | Offer: discount OR free shipping unlocked with subscription signup |

Frame subscription around **convenience**, not savings: "Never run out" converts better than "Save 15%."

---

## Suppression Logic

- Suppress anyone already on active auto-ship / subscription for this product
- Suppress if they've already placed a repeat order for this product
- Suppress if they've been in this sequence in the last 90 days
- Suppress if they've entered the winback flow (prioritize winback)

---

## A/B Test Priorities

1. Email 1 timing: 10 days before depletion vs. 7 days before
2. Email 2 framing: Loss ("don't lose your progress") vs. Gain ("keep your results going")
3. Email 3: Discount vs. free shipping vs. bonus product
4. Subscribe-and-save CTA: Primary vs. secondary position in Email 1

---

## Success Metrics

| Metric | Benchmark | Good |
|--------|-----------|------|
| Flow CVR | 20% | 30-35%+ |
| Subscribe-and-save conversion | 5-10% | 15%+ |
| Time-to-next-order vs. baseline | Baseline | Shortening |
| Email 1 open rate | 40-50% | 55%+ |
