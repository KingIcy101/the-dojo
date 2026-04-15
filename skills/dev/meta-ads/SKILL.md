---
name: meta-ads
description: >
  Meta Ads API (Facebook/Instagram) — read campaign performance, ad sets, spend, leads.
  Critical for Halo Marketing — we run FB ads for clients and need to pull data programmatically.
  Use for client dashboards, automated reporting, campaign monitoring.
---

# Meta Ads API

## Setup
```bash
npm install facebook-nodejs-business-sdk
```
```js
const bizSdk = require('facebook-nodejs-business-sdk')
const api = bizSdk.FacebookAdsApi.init(process.env.META_ACCESS_TOKEN)
```

## Get Campaign Performance
```js
const { AdAccount, Campaign } = bizSdk

const account = new AdAccount(`act_${process.env.META_AD_ACCOUNT_ID}`)

// Get all campaigns with insights
const campaigns = await account.getCampaigns(
  [Campaign.Fields.id, Campaign.Fields.name, Campaign.Fields.status],
  {
    fields: ['insights{spend,impressions,clicks,cpc,cpm,cpp,reach,leads,actions}'],
    time_range: { since: '2026-03-01', until: '2026-03-31' },
  }
)

campaigns.forEach(campaign => {
  const insights = campaign._data.insights?.data[0]
  console.log({
    name: campaign.name,
    spend: insights?.spend,
    leads: insights?.actions?.find(a => a.action_type === 'lead')?.value || 0,
    cpl: insights?.cost_per_action_type?.find(a => a.action_type === 'lead')?.value,
  })
})
```

## Simpler: Graph API via fetch
```js
// No SDK — just fetch (easier for simple reads)
const BASE = 'https://graph.facebook.com/v21.0'
const TOKEN = process.env.META_ACCESS_TOKEN

// Get account insights
const res = await fetch(
  `${BASE}/act_${AD_ACCOUNT_ID}/insights?` +
  `fields=campaign_name,spend,impressions,clicks,actions,cost_per_action_type&` +
  `time_range={"since":"2026-03-01","until":"2026-03-31"}&` +
  `level=campaign&` +
  `access_token=${TOKEN}`
)
const data = await res.json()
```

## Get Leads (Lead Gen Forms)
```js
// Get leads from a Lead Gen form
const leads = await fetch(
  `${BASE}/${FORM_ID}/leads?` +
  `fields=id,created_time,field_data&` +
  `access_token=${TOKEN}`
).then(r => r.json())

leads.data.forEach(lead => {
  const name = lead.field_data.find(f => f.name === 'full_name')?.values[0]
  const email = lead.field_data.find(f => f.name === 'email')?.values[0]
  const phone = lead.field_data.find(f => f.name === 'phone_number')?.values[0]
  // Sync to GHL contact
})
```

## Webhook (Real-time Lead Notifications)
```js
// Subscribe to leadgen webhook in Meta Business Manager
// POST /api/webhooks/meta
export async function POST(req) {
  const body = await req.json()

  if (body.object === 'page') {
    body.entry.forEach(entry => {
      entry.changes.forEach(change => {
        if (change.field === 'leadgen') {
          const leadId = change.value.leadgen_id
          // Fetch lead details + sync to GHL
          syncLeadToGHL(leadId)
        }
      })
    })
  }
  return new Response('OK')
}
```

## Auth (Long-Lived Token)
```js
// Short-lived tokens expire in 1hr — always use long-lived (60 days)
// Exchange in Meta Business Manager → System Users → Generate Token
// Or: GET /oauth/access_token?grant_type=fb_exchange_token&...
```

## Environment Variables
```env
META_ACCESS_TOKEN=       # Long-lived system user token (60 days)
META_AD_ACCOUNT_ID=      # Without 'act_' prefix
META_APP_ID=
META_APP_SECRET=
META_WEBHOOK_VERIFY_TOKEN=  # For webhook verification
```

## Halo Use Cases
- **Client dashboards** — pull spend/leads/CPL per client automatically
- **Lead webhooks** — instant GHL sync when Facebook lead comes in
- **Monthly reports** — automated campaign performance data
- **Spend monitoring** — alert if daily spend exceeds budget

## Skill Injection for Codex/Claude Code
```
Meta Ads API: GET https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/insights
Required: access_token, fields, time_range (JSON), level=campaign.
Lead gen: /{FORM_ID}/leads → field_data array with name/email/phone.
Webhook for real-time leads: subscribe via Meta Business Manager.
Long-lived tokens only — short tokens expire in 1hr.
```
