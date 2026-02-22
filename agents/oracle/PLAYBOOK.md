# Oracle — Prediction Market Playbook

## The Core Mental Model

Polymarket is not gambling. It's finding mispricings.

The question Oracle asks on every market: **"Does the market price reflect reality, or is the crowd wrong?"**

Crowds are wrong when:
- Breaking news moves slower than the market should re-price (arbitrage window)
- A base rate is well-established but the market hasn't priced it in
- A market is thinly traded and driven by vibes, not research
- Resolution criteria are ambiguous and the crowd is pricing the wrong outcome

When Oracle finds a gap of 8+ percentage points between what the market says and what Oracle calculates, that's a trade.

---

## Edge Framework

### How to Calculate Edge
1. **Base rate** — what has this type of event resolved to historically?
2. **Current information** — what do the latest news/data say?
3. **Crowd bias** — is there a known psychological bias inflating/deflating the price? (recency bias, wishful thinking, etc.)
4. **Resolution rules** — read them carefully. Many traders bet on the wrong thing because they didn't read the fine print.
5. **Time to resolution** — edge decays as the event approaches and information improves

### Position Sizing (Kelly Criterion, conservative)
- Full Kelly is too aggressive for binary markets
- Use 1/4 Kelly or simpler: `position_size = (edge × bankroll) / max_loss`
- Never bet more than 5% of total portfolio on a single market

---

## Market Categories & Approach

### Current Events / News
**Best edge type:** React fast to breaking news before the market re-prices  
**Watch for:** Ambiguous resolution criteria that the crowd is ignoring  
**Time horizon:** Days to weeks  
**Example:** Market asks "Will X resign by March?" — new reporting breaks, market lags

### Crypto Prices
**Best edge type:** Macro trend analysis + technical levels  
**Watch for:** Markets priced on fear/greed rather than fundamentals  
**Time horizon:** Weeks to months  
**Example:** "Will BTC be above $X on date Y?" — assess based on macro + technicals

### Politics
**Best edge type:** Polling aggregates vs. market price discrepancies  
**Watch for:** Markets driven by partisan emotion rather than polling averages  
**Time horizon:** Weeks to months  
**Example:** Primary results — markets sometimes lag aggregated polling data  
**Caution:** High variance even with edge — keep sizes smaller

### Sports
**Best edge type:** Statistical models vs. narrative-driven crowd  
**Watch for:** Markets on high-volume events (major leagues only)  
**Time horizon:** Days  
**Caution:** Polymarket sports markets often have low volume — check before trading

---

## Trade Log Format

Every trade goes in `memory/oracle-trades.json`:
```json
{
  "date": "YYYY-MM-DD",
  "market": "Will X happen by Y?",
  "direction": "YES",
  "shares": 100,
  "price": 0.42,
  "cost": 42.00,
  "thesis": "Market pricing 42% but base rate for this event type is 55%+. Recent news supports YES.",
  "sources": ["source1", "source2"],
  "status": "open",
  "closePrice": null,
  "pnl": null,
  "notes": ""
}
```

---

## Paper Trade Mode (Phase 1)

Before real money, Oracle runs in simulation:
- Identifies markets and records trades in the log
- Marks them as `"paper": true`
- Tracks what the P&L would have been at resolution
- After 30 days and 10+ simulated trades: review with Matt
- If win rate > 55% and expected value is positive: go live

---

## Build Order

When the time comes to build Oracle, here's the sequence:

1. **Set up wallet** — Matt creates Polygon wallet, funds with USDC (start: $200–500)
2. **Connect Polymarket** — wallet → Polymarket account → generate API key
3. **Install py-clob-client** — official Polymarket Python SDK
4. **Build market scanner** — pull active markets, filter by volume, display current prices
5. **Build research tool** — for a given market, pull resolution criteria + recent relevant data
6. **Paper trade mode** — Oracle logs trades but doesn't execute. Run for 30 days.
7. **Review performance** — validate the approach
8. **Go live** — enable real trade execution with Matt's approved limits

**Estimated build time:** 3–5 days of focused work once accounts are set up.

---

## Reference Links (For When Building)
- Polymarket CLOB API: https://docs.polymarket.com
- Gamma Markets API: https://gamma-api.polymarket.com
- py-clob-client: https://github.com/Polymarket/py-clob-client
- Polymarket Discord: best place for edge cases and API help
