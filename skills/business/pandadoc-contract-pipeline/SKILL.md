---
name: pandadoc-contract-pipeline
description: Auto-generate and send contracts via PandaDoc API from template, then trigger Stripe on signature.
category: business
---

# PandaDoc Contract Pipeline

## When to Use
Automating contract generation for ITP or ZTA clients — create from template, fill tokens, send for e-signature, trigger Stripe subscription on completion.

## Config
```
Template UUID: 5nQHucQwGkmyGrbjHSdG4G
API Base:      https://api.pandadoc.com/public/v1
Auth:          Bearer token in Authorization header
```

## Steps

1. Create document from template (fill tokens)
2. Send document for signature
3. Receive webhook on `document_state_changed` (status: `document.completed`)
4. Trigger Stripe subscription creation
5. Update Supabase client record

## Key Patterns / Code

### Create Document from Template
```js
const doc = await fetch('https://api.pandadoc.com/public/v1/documents', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.PANDADOC_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: `${clientName} — ITP Agreement`,
    template_uuid: '5nQHucQwGkmyGrbjHSdG4G',
    recipients: [
      {
        email: clientEmail,
        first_name: clientFirstName,
        last_name: clientLastName,
        role: 'Client',
      },
    ],
    tokens: [
      { name: 'client_name', value: clientName },
      { name: 'business_name', value: businessName },
      { name: 'tier', value: tier },              // 'Light' | 'Standard' | 'High Volume'
      { name: 'setup_fee', value: setupFee },      // e.g. '$5,000'
      { name: 'monthly_fee', value: monthlyFee },  // e.g. '$750'
      { name: 'start_date', value: startDate },    // e.g. 'April 15, 2026'
    ],
  }),
});
const { id: docId } = await doc.json();
```

### Send for Signature (wait ~2s after create)
```js
await new Promise(r => setTimeout(r, 2000)); // PandaDoc needs processing time

await fetch(`https://api.pandadoc.com/public/v1/documents/${docId}/send`, {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.PANDADOC_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ message: 'Please review and sign your agreement.' }),
});
```

### Webhook Handler (Express)
```js
app.post('/webhook/pandadoc', (req, res) => {
  const event = req.body;
  if (event.event === 'document_state_changed' && event.data.status === 'document.completed') {
    const docId = event.data.id;
    handleContractSigned(docId); // trigger Stripe + Supabase update
  }
  res.sendStatus(200);
});
```

### Trigger Stripe Subscription
```js
async function handleContractSigned(pandaDocId) {
  const { data: client } = await supabase
    .from('intake_submissions')
    .select('*')
    .eq('pandadoc_id', pandaDocId)
    .single();

  await stripe.subscriptions.create({
    customer: client.stripe_customer_id,
    items: [{ price: PRICE_IDS[client.tier] }],
  });

  await supabase.from('intake_submissions').update({ status: 'active' }).eq('id', client.id);
}
```

## Gotchas
- Must wait 2-3 seconds after document creation before calling send — PandaDoc needs processing time
- Token names must match template exactly (case-sensitive)
- Register webhook URL in PandaDoc dashboard under Settings > Integrations > Webhooks
- Document status flow: `draft` -> `sent` -> `viewed` -> `completed`
- Store `pandadoc_id` on the Supabase row immediately after creation for webhook lookup
- API rate limit: 100 req/min — batch creation jobs accordingly
