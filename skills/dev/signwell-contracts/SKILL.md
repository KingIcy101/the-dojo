---
name: signwell-contracts
description: Create, send, and track contracts via SignWell API — template-based doc creation, field pre-fill, webhook on completion.
category: dev
---

# SignWell Contract API

## When to Use
Generating and sending client contracts programmatically. Create from template, pre-fill fields (name, price, date),
send for e-signature, receive webhook when signed, store PDF URL in Supabase.

## Steps
1. Create template in SignWell dashboard, note template ID
2. Map field names in template (e.g. `client_name`, `monthly_price`)
3. POST to `/api/v1/documents` with template_id + field values + signer email
4. Webhook fires `document.completed` → extract signed PDF URL → store in DB
5. Optionally redirect signer after signing via `redirect_url`

## Key Patterns / Code

### Create Document from Template
```js
const response = await fetch('https://api.signwell.com/api/v1/documents', {
  method: 'POST',
  headers: {
    'X-Api-Key': process.env.SIGNWELL_API_KEY,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    test_mode: process.env.NODE_ENV !== 'production', // won't count toward billing
    template_ids: [process.env.SIGNWELL_TEMPLATE_ID],
    subject: `ITP Services Agreement — ${clientName}`,
    message: 'Please review and sign your services agreement.',
    signers: [{
      id: '1',
      name: clientName,
      email: clientEmail,
      redirect_url: 'https://app.inthepast.ai/onboarding/contract-signed',
    }],
    fields: [
      { api_id: 'client_name', value: clientName },
      { api_id: 'business_name', value: businessName },
      { api_id: 'monthly_price', value: `$${monthlyPrice}/mo` },
      { api_id: 'start_date', value: new Date().toLocaleDateString() },
      { api_id: 'setup_fee', value: '$5,000' },
    ],
  }),
});

const doc = await response.json();
// doc.id = document ID for tracking
// doc.signers[0].sign_url = direct signing link (skip email if needed)
await supabase.from('contracts').insert({
  org_id: orgId,
  signwell_doc_id: doc.id,
  status: 'sent',
});
```

### Webhook Handler
```js
app.post('/webhooks/signwell', express.json(), (req, res) => {
  const { event_type, document } = req.body;

  if (event_type === 'document.completed') {
    const pdfUrl = document.completed_pdf_url;
    const docId = document.id;

    // Store signed PDF URL in Supabase
    supabase.from('contracts').update({
      status: 'signed',
      signed_pdf_url: pdfUrl,
      signed_at: new Date().toISOString(),
    }, { where: { signwell_doc_id: docId } });

    // Trigger next onboarding step
    triggerOnboarding(docId);
  }

  res.sendStatus(200);
});
```

### Check Document Status
```js
const doc = await fetch(`https://api.signwell.com/api/v1/documents/${documentId}`, {
  headers: { 'X-Api-Key': process.env.SIGNWELL_API_KEY }
}).then(r => r.json());

console.log(doc.status); // 'pending', 'completed', 'declined', 'expired'
console.log(doc.completed_pdf_url); // only set when status === 'completed'
```

## Gotchas
- `test_mode: true` in dev — doesn't send real emails and doesn't count toward billing limit
- `completed_pdf_url` is a temporary signed S3 URL — download and store in Supabase Storage ASAP (expires ~7 days)
- Field `api_id` must exactly match the field name set in the template editor
- SignWell webhook doesn't include a signature for verification — validate by re-fetching document status
- `redirect_url` only fires after the *last* signer completes — not after each signer
- Template field types: text, date, checkbox, initials, signature — each has different `value` format