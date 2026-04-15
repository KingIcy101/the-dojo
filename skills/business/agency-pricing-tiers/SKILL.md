---
name: agency-pricing-tiers
description: ITP pricing structure — tier thresholds, setup fees, HIPAA add-on, upsell triggers, and discount policy.
category: business
---

# ITP Agency Pricing Tiers

## When to Use
Any time pricing comes up: quoting a prospect, building a pricing page, creating proposals, or deciding which tier a client fits.
Also covers upsell triggers, discount limits, and add-on pricing.

## Pricing Structure

### Monthly Tiers
| Tier | Minutes/mo | Monthly Price |
|------|-----------|---------------|
| Light | < 3,000 min | $750/mo |
| Standard | 3,000 – 6,000 min | $1,100/mo |
| High Volume | 6,000+ min | $1,500+/mo |

**Setup Fee:** $5,000 (ALL tiers, no exceptions)

### HIPAA Add-On
- **$1,000/mo flat per Vapi account** (not per client)
- One Vapi HIPAA account can serve multiple healthcare clients
- Baked into healthcare client pricing — quote $1,750+/mo for light healthcare
- Required for: dental, medical, mental health, any HIPAA-covered entity

### CAO Add-On (Custom AI Outreach)
- **Remote:** $4,950
- **Shipped (hardware):** $9,450
- Separate from receptionist — outbound call automation

## Key Patterns / Code

### Tier Assignment Logic
```js
function assignTier(monthlyMinutes) {
  if (monthlyMinutes < 3000) return { tier: 'light', price: 750 };
  if (monthlyMinutes < 6000) return { tier: 'standard', price: 1100 };
  return { tier: 'high_volume', price: 1500 }; // negotiate above 6K
}

function quoteClient({ monthlyMinutes, isHIPAA, includeCAO, caoShipped }) {
  const { tier, price } = assignTier(monthlyMinutes);
  let monthly = price;
  if (isHIPAA) monthly += 1000;
  let setup = 5000;
  if (includeCAO) setup += caoShipped ? 9450 : 4950;
  return { tier, monthly, setup, total: setup + (monthly * 12) };
}
```

### Upsell Triggers
1. **>80% of minute allocation used** → upgrade to next tier (add to onboarding automation)
2. **Client adding locations** → new setup fee per location + tier reassessment
3. **Client referrals** → offer referral credit ($100-200/mo for 3 months) — not a discount

### Discount Policy
| Item | Policy |
|------|--------|
| Setup fee | **No discounts** — $5,000 is non-negotiable |
| Monthly fee | Max 10% for annual commitment (pay 12 months upfront) |
| Referrals | Credit model only — not percentage off |
| HIPAA add-on | No discounts |

### Annual Commitment Example
```
Standard tier: $1,100/mo × 12 = $13,200/yr
With 10% annual discount: $13,200 × 0.90 = $11,880/yr ($990/mo effective)
Setup fee still: $5,000

Total year 1: $16,880
```

### Proposal Quick Math
```
Light (no HIPAA):     $5K setup + $750/mo
Standard (no HIPAA):  $5K setup + $1,100/mo
High Volume:          $5K setup + $1,500+/mo (custom)
Light + HIPAA:        $5K setup + $1,750/mo
Standard + HIPAA:     $5K setup + $2,100/mo
Light + HIPAA + CAO:  $5K setup + $9,950 CAO + $1,750/mo
```

## Gotchas
- HIPAA add-on is per Vapi HIPAA account — if multiple healthcare clients share one account, it's still $1K flat
- High Volume tier is negotiated — $1,500 is the floor, not ceiling
- Never quote without confirming minutes — ask: "About how many calls per month does your office get?"
- CAO is a completely separate product — don't bundle unless client asks
- Annual discount only applies if paid upfront — not monthly billing at reduced rate