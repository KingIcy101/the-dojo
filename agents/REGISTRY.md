# Agent Registry

> Quick reference for Alo. Use trigger phrases or describe the task — I'll route to the right agent.

## Alo (Orchestrator)
**Me.** Handles everything, delegates to specialists, QAs output, manages Matt's personal life.  
**Always active.**

---

## Scout — Sales Intelligence
📁 `agents/sales/`  
**Job:** Pre-call research, post-discovery packages, proposal prep, pipeline health  
**Trigger:** "Research [name/website]" · "Just finished discovery with [name]" · "Prep proposal for [name]" · "Pipeline health check"

---

## Rex — Outreach
📁 `agents/outreach/`  
**Job:** Cold email sequences, cold call scripts, lead lists, follow-up cadences, handoff to Scout  
**Trigger:** "Build email sequence for [niche]" · "Cold call script for [niche]" · "Pull leads for [city] [niche]" · "Follow-up plan for [name]" · "Rex, prep handoff for [name]"

---

## Ember — Client Success
📁 `agents/client-success/`  
**Job:** Onboarding, monthly reports, retention risk, check-in prep, referral asks  
**Trigger:** "Ember, onboard [client]" · "Monthly report for [client]" · "Who's at risk of churning?" · "Prep check-in with [client]" · "Referral ask for [client]"

---

## Volt — Ads
📁 `agents/ads/`  
**Job:** Facebook/Google campaigns, ad copy, creative briefs, performance audits  
**Trigger:** "Build a campaign for [client]" · "Write Facebook ads for [niche]" · "Audit [client]'s ad performance" · "Write Google RSAs for [client]"

---

## Prism — Content
📁 `agents/content/`  
**Job:** Social posts, email copy, ad creative briefs, brand voice guides  
**Trigger:** "Write social posts for [topic]" · "Build content calendar for [month]" · "Email to prospect list about [topic]" · "Brand voice guide for [client]" · "Creative brief for [Volt's campaign]"

---

## Kargo — Amazon/Walmart
📁 `agents/amazon/`  
**Job:** Inventory health, pricing, P&L summaries, VA instructions, Mateo sync  
**Trigger:** "Inventory check" · "What needs restocking?" · "Monthly Amazon/Walmart summary" · "VA instructions for [situation]" · "Pricing review for [category]"

---

## Atlas — Chief of Staff
📁 `agents/atlas/`  
**Job:** 3 daily briefings (9am/1pm/7pm ET auto via cron), win logging, blocker detection, client health watch, streak tracking  
**Trigger:** "Atlas, where do things stand?" · "Log that as a win: [what]" · "What's been stuck?" · "Brief me" · Runs automatically 3x/day

---

## Oracle — Prediction Market Trader *(Build Last)*
📁 `agents/oracle/`  
**Job:** Scans Polymarket for mispriced outcomes, researches probability, executes trades with Matt's approval, tracks P&L  
**Status:** Blueprint ready — build after Halo agents are fully running  
**Needs:** Polygon wallet + USDC + Polymarket API key (Matt to set up when ready)  
**Trigger:** "Oracle, scan for edges" · "Oracle, research [market]" · "Oracle, portfolio review"

---

## Spawning an Agent
```
sessions_spawn(task: "[paste agent's IDENTITY.md + PLAYBOOK.md as context, then state the specific task]")
```
See `ORCHESTRATOR.md` for delegation rules and QA checklist.
