# GoHighLevel Integration Plan

_Prepared by Halo, 2026-02-21. Research + architecture for automating Halo Marketing's CRM._

---

## Overview

GoHighLevel (GHL) has a solid REST API. The goal is to connect incoming leads from outreach campaigns directly into GHL — reducing manual work, ensuring nothing falls through the cracks, and giving Matt/Preston visibility into the full pipeline.

**Key API base URL:** `https://services.leadconnectorhq.com` (GHL's v2 API)  
**Auth:** OAuth 2.0 (preferred) or API Key (simpler for internal tools)  
**Docs:** https://highlevel.stoplight.io/docs/integrations/

---

## What the GHL API Can Do

### Core Resources (most relevant for Halo)

| Resource | What It Does |
|---|---|
| **Contacts** | Create/update/search contacts — the core CRM record |
| **Opportunities** | Deals in the pipeline — create, move stage, update value |
| **Pipelines** | Read your pipeline stages (e.g., Lead → Discovery Call → Proposal → Closed) |
| **Calendars / Appointments** | Create bookings directly into GHL calendar |
| **Conversations** | SMS, email, phone log threads per contact |
| **Tags** | Add/remove tags on contacts |
| **Custom Fields** | Read/write any custom field you've defined in GHL |
| **Webhooks** | Receive events FROM GHL (e.g., form submission, appointment booked, status change) |
| **Notes** | Add notes to contacts/opportunities |
| **Tasks** | Create follow-up tasks on any contact |

---

## Priority Integrations for Halo Marketing

### 1. Lead Auto-Import (Highest Priority)

**Problem:** Cold email replies and inbound leads from ads land in various places (Saleshandy, Facebook Leads, landing page forms). They need to get into GHL without manual entry.

**Solution:** 
- **Facebook Lead Ads → GHL**: Already natively supported in GHL. Just connect the account in GHL → Integrations. No code needed.
- **Saleshandy replies → GHL**: Saleshandy has webhooks. When someone replies or books, fire a webhook → custom handler → GHL Contacts API to create/update the contact.
- **Landing page forms → GHL**: GHL has native form builder — already in the stack. Just make sure forms are embedded on landing pages.

**API calls needed:**
```
POST /contacts/             # Create new contact from lead
PUT  /contacts/{id}         # Update if contact already exists
POST /opportunities/        # Create deal in pipeline
POST /contacts/{id}/notes   # Add note with lead source + context
POST /contacts/{id}/tags    # Tag: "cold-email-reply" or "facebook-lead"
```

### 2. Discovery Call Booking → Pipeline Stage Update

**Problem:** When an SDR books a discovery call, the pipeline stage should auto-update. Currently requires manual CRM update.

**Solution:** GHL's native calendar booking can trigger a webhook. Build a tiny listener that receives the booking event and moves the opportunity to "Discovery Call Booked" stage.

```
Webhook: appointment.booked → 
  GET /opportunities/?contactId={id} →
  PUT /opportunities/{id} with pipelineStageId = "discovery-call-booked"
```

### 3. Post-Call Follow-up Automation

**Problem:** After a discovery call, someone needs to follow up. Currently manual.

**Solution:** On stage change to "Discovery Called" → trigger GHL workflow (already possible inside GHL — no API needed, just native automations). Or via API:
```
POST /contacts/{id}/tasks  # Create: "Send proposal to [Name] by [date]"
```

### 4. Activity Logging

Track all SDR activity — calls made, emails sent — so Matt/Preston have visibility.
```
POST /contacts/{id}/notes  # Log: "Called 2026-02-21. Left VM. Follow up Thu."
```

### 5. Reporting Webhook Listener (Future)

Receive GHL events to build a simple dashboard:
- New lead added
- Discovery call booked
- Proposal sent
- Client signed / won

---

## Architecture Plan

```
[Saleshandy webhook] ─────┐
[Facebook Lead Ad]  ─────┤
[GHL Form submit]   ─────┤──→ [Router / Lambda / Cloudflare Worker] ──→ [GHL API]
[SDR logs manually] ─────┘          ↓
                               [GHL Workflows]
                                    ↓
                             [Notifications → Slack/Telegram]
```

**Options for the router:**

1. **Cloudflare Workers** (recommended) — free tier, deploys in seconds, handles webhooks, no server to manage
2. **Railway.app** — $5/month, can run Node.js/Python, good for more complex logic
3. **n8n** (self-hosted on Mac mini) — visual workflow builder, many GHL nodes built-in, great if Matt doesn't want to touch code
4. **Zapier/Make** — no-code, but $$/month and less flexible; fine as a bridge while code isn't ready

---

## Getting Started Checklist

1. **Get GHL API key or set up OAuth app**
   - GHL Dashboard → Settings → Business Profile → API keys (Location-level)
   - Or: create an OAuth app in the GHL Marketplace for cleaner access
   
2. **Map the pipeline stages** (need stage IDs for API calls)
   - `GET /pipelines/` to list all pipelines and stage IDs
   - Document: Lead → Reached → Discovery Call Booked → Discovery Called → Proposal → Closed Won / Closed Lost

3. **Build lead intake webhook** (small Node.js script or Cloudflare Worker)
   - Input: name, email, phone, lead source, notes
   - Output: GHL Contact + Opportunity created in correct pipeline stage

4. **Test with a real lead** — create one manually via API, confirm it appears in GHL

5. **Connect Saleshandy webhook** — paste endpoint URL into Saleshandy's webhook settings

6. **Connect Facebook Lead Ads** — native GHL integration, just OAuth connect

---

## API Auth: Getting a Token

**Simple approach (Location API Key):**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://services.leadconnectorhq.com/contacts/?limit=10
```

Matt needs to get the Location-level API key from GHL Settings. I can then test calls against their API.

**OAuth approach (if building as a proper app):**
- Register app in GHL Marketplace (private app)
- Redirect URI: can be anything (even localhost for internal tools)
- Scopes needed: `contacts.write`, `opportunities.write`, `calendars.read`, `conversations.write`

---

## Estimated Build Time

| Phase | Time |
|---|---|
| API auth + pipeline mapping | 30 min |
| Lead intake webhook | 2–3 hours |
| Saleshandy → GHL bridge | 2–3 hours |
| Facebook Leads (native GHL) | 30 min |
| Post-call automation | 1–2 hours |
| Testing + debugging | 2–4 hours |
| **Total** | **~1–2 days of focused work** |

---

## Immediate Next Step

**Matt needs to:**
1. Pull the GHL Location API Key (Settings → API Keys in GHL dashboard)
2. Confirm the pipeline name and rough stages you're already using
3. Decide: do you want to start with **n8n** (visual, no code) or a **custom script** (faster, more flexible)?

Once I have the API key and pipeline structure, I can build the first integration in a few hours.

---

_This is a high-leverage project. Once leads flow automatically into GHL, the whole sales machine becomes measurable._
