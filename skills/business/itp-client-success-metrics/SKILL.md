---
name: itp-client-success-metrics
description: Use when Mara needs to check client health, identify churn risk, trigger renewals, or flag upsell opportunities.
category: business
---
# ITP Client Success Metrics

## When to Use
Weekly health checks. Monthly check-in prep. Any time a client's status changes. Renewal/upsell triggers. Mara uses this as the monitoring framework.

## Primary Metrics (check weekly)
| Metric | Target | Churn Signal |
|--------|--------|--------------|
| Call answer rate | >95% | <85% |
| Appointment conversion rate | >30% | <15% |
| Missed call recovery rate | >80% | <60% |

## Secondary Metrics (check monthly)
- Avg call duration (baseline by industry, flag if drops >30%)
- Escalation rate (target <10% — high = script issue or wrong use case)
- Client NPS (monthly check-in, target 8+)

## Key Patterns / Code

```ts
// Weekly health check query
const { data: metrics } = await supabase
  .from('call_logs')
  .select('status, duration, outcome, created_at')
  .eq('client_id', clientId)
  .gte('created_at', new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString());

const totalCalls = metrics.length;
const answeredCalls = metrics.filter(c => c.status === 'answered').length;
const bookedCalls = metrics.filter(c => c.outcome === 'booked').length;
const escalations = metrics.filter(c => c.outcome === 'escalated').length;

const answerRate = totalCalls > 0 ? answeredCalls / totalCalls : 0;
const conversionRate = answeredCalls > 0 ? bookedCalls / answeredCalls : 0;
const escalationRate = answeredCalls > 0 ? escalations / answeredCalls : 0;
```

```ts
// Churn signal detection
function detectChurnSignals(metrics: ClientMetrics): ChurnSignal[] {
  const signals: ChurnSignal[] = [];

  if (metrics.answerRate < 0.85)
    signals.push({ type: 'ANSWER_RATE_LOW', severity: 'HIGH', value: metrics.answerRate });

  if (metrics.callCount === 0 && daysSinceLastCall(metrics) > 7)
    signals.push({ type: 'NO_CALLS_7_DAYS', severity: 'HIGH', note: 'Script issue or forwarding broken' });

  if (metrics.escalationsThisWeek >= 3)
    signals.push({ type: 'HIGH_ESCALATIONS', severity: 'MEDIUM', value: metrics.escalationsThisWeek });

  if (metrics.lastCheckInResponseDays > 30)
    signals.push({ type: 'CHECK_IN_NO_RESPONSE', severity: 'MEDIUM' });

  return signals;
}
```

```ts
// Renewal trigger — 30 days before contract end
const renewalDate = new Date(client.contract_end);
renewalDate.setDate(renewalDate.getDate() - 30);

if (new Date() >= renewalDate && !client.renewal_initiated) {
  await triggerRenewalSequence(client);
  // Resend email: renewal offer + updated results summary
}
```

```ts
// Upsell trigger — >80% minute allocation for 2 consecutive months
if (client.monthlyMinutesUsed[0] > client.minuteAllocation * 0.8 &&
    client.monthlyMinutesUsed[1] > client.minuteAllocation * 0.8) {
  await flagForUpsell(client, 'Usage consistently over 80% — upgrade to next tier');
}
```

## Action Triggers
| Signal | Action |
|--------|--------|
| Answer rate < 85% | Mara checks phone forwarding, pings Matt |
| No calls 7 days | Mara checks Vapi + phone setup, pings Matt |
| 3+ escalations/week | Flag for Scribe script revision |
| Missed check-in | Send follow-up email, schedule call if no response in 48hrs |
| 30 days to renewal | Start renewal sequence |
| >80% minutes x2 months | Propose tier upgrade |

## Gotchas
- Zero calls for 7 days is almost always a phone forwarding issue, not a cancellation intent
- High escalation rate = script not handling a common question — review transcript, update Scribe
- Monthly check-in timing: same day each month, from hello@inthepast.ai
- NPS below 7 = immediate call from Matt — don't automate the recovery, make it human
- Upsell conversation should come from Matt, not automated email — flag, don't trigger automatically
