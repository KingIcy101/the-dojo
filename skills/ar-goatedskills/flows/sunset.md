# Sunset

## Overview

**Trigger:** Completed winback flow with zero engagement — OR — 90-120+ days of no email opens with no recent purchase
**Goal:** Protect sender reputation and deliverability by removing or suppressing permanently unengaged subscribers. A clean, engaged list outperforms a large inactive one on every metric.
**Length:** 2 emails over 7-14 days
**Reactivation target:** 5-10% of sunset-eligible subscribers

---

## Why Sunset Matters

| Without sunset | With sunset |
|----------------|-------------|
| High spam complaint rate | Low spam complaint rate |
| Low sender reputation | Strong sender reputation |
| Emails landing in promotions/spam | Emails landing in inbox |
| Inflated list size, low revenue per subscriber | Lean list, high revenue per subscriber |
| Domain/IP reputation degrading over time | Domain/IP health maintained |

Every unengaged subscriber on your list actively drags down deliverability for the people who actually want to hear from you.

---

## Email 1 — Day 0 (trigger fires)
**Subject angle:** Preference check / "Still want to hear from us?"
**Preview text:** "We want to make sure we're sending you the right things"

**Copy angle:**
- Direct and respectful: "We've noticed you haven't opened our emails in a while"
- No guilt, no pressure — acknowledge that email preferences change
- Give them a clear choice:
  - Option A: Stay subscribed (click to confirm or update preferences)
  - Option B: Unsubscribe easily and clearly
  - Option C: Downgrade to a lower-frequency list ("just the important stuff")
- State what happens if they don't click: "If we don't hear from you, we'll remove you from our list in [X] days"

**CTA buttons (2):**
- "Yes, keep me subscribed"
- "No thanks, unsubscribe me"

**Tone:** Calm, respectful, zero pressure. Preference conversation, not a sales pitch.

---

## Email 2 — Day 7-14 (if no engagement on Email 1)
**Subject angle:** "This is goodbye (for now)"
**Preview text:** "We're removing you from our list — but you're always welcome back"

**Copy angle:**
- Brief, warm, no drama
- "Since we haven't heard from you, we're removing you from our list today"
- Include a re-subscribe link — leave the door open
- Optional: final offer (best incentive) for one last reactivation attempt
- Thank them for having been on the list

**CTA:** Re-subscribe / Come back anytime

**After this email:** Move to suppressed list. Do not continue emailing.

---

## Technical Implementation

### Klaviyo Setup
1. Build "Sunset-eligible" segment: no opens in 90 days + completed winback with no engagement
2. Trigger sunset flow on segment membership
3. On Email 1 "Keep me subscribed" click → tag as "Re-engaged," exit flow, add to active segment
4. On Email 2 completion with no engagement → suppress profile, remove from all active flows
5. Use "Suppressed" status — do not hard delete (retain for lookalike audiences)

### Suppression vs. Unsubscribe
- **Unsubscribe:** Customer-initiated. They opted out.
- **Suppression:** Marketer-initiated. You stop sending — they can return via form.
- Use suppression for sunset so the door stays open.

---

## List Hygiene Schedule

| Frequency | Action |
|-----------|--------|
| Ongoing (flow) | Sunset anyone completing winback with no engagement |
| Quarterly | Audit all profiles with 90+ day no-open |
| Monthly | Review spam complaint rate — target <0.1% |
| After major campaigns | Check for bounce spikes — remove hard bounces immediately |

---

## Suppression Logic

- Never sunset VIP customers — give them a dedicated VIP winback, no time limit
- Never sunset customers who purchase without opening email (buyer-not-opener segment — still valuable)
- Sunset email list only — does not affect SMS suppression

---

## Success Metrics

| Metric | Benchmark | Good |
|--------|-----------|------|
| Reactivation rate (click "keep me") | 5% | 8-12% |
| Post-sunset list open rate | Increasing | 30%+ on remaining active list |
| Spam complaint rate | <0.1% | <0.05% |
| Deliverability improvement | Measurable uplift within 30 days of running sunset |
