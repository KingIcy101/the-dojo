---
name: mara-csm-pattern
description: Autonomous CSM agent pattern — 7 cron jobs for churn monitoring, milestone check-ins, reporting, and renewal alerts.
category: meta
---

# Mara — Autonomous CSM Agent Pattern

## When to Use
Building a CSM (Customer Success Manager) agent that proactively monitors clients, identifies churn risk, and takes action without Matt's involvement.

## Architecture
Mara runs 7 cron jobs. All data comes from Supabase `call_logs`. Discord escalation channel for anything requiring human decision. Cost: ~$0.90/month in LLM API calls.

## 7 Cron Jobs

| Job | Schedule | Action |
|-----|----------|--------|
| Daily churn monitor | 9am ET daily | Query call_logs, score each client, flag risk |
| Daily milestone check-ins | 10am ET daily | Detect milestones (first 10 calls, first month), send congrats |
| Weekly learning | Sunday 10pm ET | Review patterns, update corrections.md |
| Weekly tier check | Monday 10am ET | Check if any client should be upgraded/downgraded |
| Nightly consolidate | 11:59pm ET | Write daily summary to memory file |
| Monthly client reports | 1st of month | Generate + send PDF-style report per client |
| Renewal alert | Monthly (before renewal date) | Flag renewals 30 days out, draft retention offer |

## Key Patterns / Code

### Churn Risk Scoring
```js
async function scoreChurnRisk(clientId) {
  const { data: logs } = await supabase
    .from('call_logs')
    .select('*')
    .eq('client_id', clientId)
    .gte('created_at', new Date(Date.now() - 7 * 86400000).toISOString())
    .order('created_at', { ascending: false });

  const callVolume = logs.length;
  const avgDuration = logs.reduce((s, l) => s + l.duration, 0) / (logs.length || 1);
  const recentComplaints = logs.filter(l => l.outcome === 'complaint').length;

  // Simple scoring — customize per ITP needs
  let risk = 0;
  if (callVolume < 5) risk += 3;          // low usage
  if (avgDuration < 30) risk += 2;        // very short calls
  if (recentComplaints > 0) risk += 5;    // any complaints

  return risk; // 0 = healthy, 5+ = at risk, 8+ = critical
}
```

### Discord Escalation
```js
async function escalate(message, urgency = 'normal') {
  const color = urgency === 'critical' ? '🔴' : '🟡';
  await fetch(process.env.DISCORD_WEBHOOK_ESCALATIONS, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: `${color} **MARA ESCALATION**\n${message}` }),
  });
}
```

### Milestone Detection
```js
const MILESTONES = [10, 50, 100, 500]; // call counts

async function checkMilestones(clientId) {
  const { count } = await supabase
    .from('call_logs')
    .select('id', { count: 'exact' })
    .eq('client_id', clientId);

  if (MILESTONES.includes(count)) {
    await sendMilestoneEmail(clientId, count);
  }
}
```

### Cron Setup (node-cron)
```js
const cron = require('node-cron');

// 9am ET = 14:00 UTC
cron.schedule('0 14 * * *', runChurnMonitor);
// 10am ET = 15:00 UTC
cron.schedule('0 15 * * *', runMilestoneChecks);
// Sunday 10pm ET = 03:00 UTC Monday
cron.schedule('0 3 * * 1', runWeeklyLearning);
// Nightly
cron.schedule('59 23 * * *', runNightlyConsolidate);
```

## Gotchas
- All proactive actions (emails, Slack messages) go through Mara's send functions — never direct API calls in cron callbacks
- Escalation channel is human decision point — Mara proposes, Matt approves via Discord reaction
- Monthly report cron runs on 1st at 8am ET — offset from midnight to avoid DB contention
- Churn scoring is a heuristic — tune thresholds based on real churn data after first 90 days
- Renewal date must be stored on the client record in Supabase — pull from `intake_submissions.created_at` + subscription length
- Weekly learning writes to corrections.md only if patterns are meaningful — don't auto-write noise
