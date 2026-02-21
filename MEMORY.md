# MEMORY.md - Long-Term Memory

## About Matt
- 24 years old, lives in Virginia
- From Hagerstown, Maryland; went to Hood College in Frederick, MD
- Graduated 2023, went full-time on Amazon business
- Currently building Halo Marketing as his primary focus
- Amazon FBA: ~$40K/month profit (provides runway + removes sales desperation)
- Amazon/Walmart business is largely automated (has VA)
- Wants to exit SourceDart (sourcedart.io) in 2026
- Works out nearly daily, has family + girlfriend
- Wants to scale hard in his 20s

## His Businesses
- **Halo Marketing** — marketing agency for healthcare practitioners (FB/Google ads, appt reminders, websites, social). Partner: Preston. MAIN FOCUS.
- **Amazon/Walmart** — name brand + supplement products, mostly automated. Partner: Mateo.
- **SourceDart** (sourcedart.io) — Walmart sourcing tool, wants to exit 2026.

## Halo Marketing - 12-Month Goals
- 150 active clients
- ~$300K MRR (150 × $2K retainer)
- Run paid ads to accelerate growth
- Scale fast

## Halo Marketing - Current State (from full intel doc)
- Official launch: January 19, 2026 | HQ: Maryland (remote)
- 1 paying client: Renee (chiropractor, $1K/month)
- Client: Jacek (supplement company) — added per Matt
- 1 strategic partnership: Alex (3 locations, free trial — learning competitor's system)
- Pipeline rebuilding: Suzanne (dental) and Mike/Andy (telehealth brain injury) fell off
- Former team member: Vanessa Herrera (Client Success Manager, departed — big gap)
- Monthly burn: UNKNOWN — $20K figure in doc is NOT accurate per Matt
- Break-even: TBD (depends on actual burn)
- NOTE: Intel doc has inaccuracies — weight direct conversations with Matt over doc

## Halo Marketing - Pricing
- Standard: $1,950/month (dental, chiro)
- Telehealth/specialized: $2,950/month
- Discounted: $1,000/month (case-by-case)
- 3-month minimum commitment
- Payment BEFORE service begins (no exceptions)

## Halo Marketing - Services
- Facebook/Google ads + creative
- Landing pages (GoHighLevel)
- AI call center (Bland.ai) — positioned as "dedicated appointment reminder team" (never as AI)
- Automated SMS/email follow-up
- CRM setup + pipeline management
- HIPAA-compliant infrastructure
- Appointment booking integration

## Halo Marketing - Tech Stack
- GoHighLevel (GHL): CRM, landing pages, pipelines, client dashboards
- Saleshandy: cold email outreach (domain: trygohalomarketing.com)
- Bland.ai: AI calling (positioned as human team)
- Slack: internal comms
- Tally: client intake forms
- Trello: task management

## Halo Marketing - Sales Flow
- Cold outreach (calls + email) → book discovery call
- Discovery call (consultative, problem-solving) → if interest → close call
- Close call: proposal + contracts → payment → onboarding
- Account manager handles ongoing client relationship
- Former AM: Vanessa (gone) — role currently unassigned
- Matt + Preston running discovery calls themselves currently
- Sales rep comp: 20% of retainer ($400/close) until 50 active clients + 5% residuals 6 months
- Daily cold call target: 50+ calls/day
- Cold email: multi-touch sequences, "confused patient" approach
- CRM: GoHighLevel (leads not fully mapped in yet — needs dev work)

## Halo Marketing - Immediate Priorities
1. Rebuild pipeline (Suzanne + Mike/Andy fell off)
2. Fill outreach gap (Vanessa's role unassigned)
3. Deliver results for Renee (first client, proof of concept)
4. Document Alex's competitive intel (free trial)
5. Follow up with Suzanne + Mike/Andy to learn why they didn't close

## Halo Marketing - Hiring Plan
- Cold outreach specialist (HIGH priority — replace Vanessa)
- Account managers (trigger: when Preston hits 20-25 clients)
- Sales closers (trigger: when Matt is at discovery call capacity)
- Colombia for sales talent (SDR/outreach role)
- **Research done**: Colombia SDR hiring research in `memory/colombia-sdr-research.md`
- **JD ready**: Job description draft in `memory/sdr-job-description.md` (needs email before posting)
- Recommended comp: $800–$1,000 base + $100–$150/booked-and-held discovery call

## Voice Call System - Plan
- Goal: Matt or Preston can call a number and have a natural voice conversation with Halo
- Also want me "in a meeting" — could be a conference line they add me to
- Smart cost idea: use existing memory/workspace files as context instead of sending everything via API each call (reduces token costs)
- Tech stack: Twilio + either OpenAI Realtime API OR cheaper pipeline (Deepgram STT + Claude + ElevenLabs TTS)
- Need: Twilio account + Deepgram (or similar) — not yet set up
- On the backlog — needs dedicated accounts first
- Matt only has Anthropic API key currently (powers me)
- Matt wants separate logins for everything Halo uses — key principle

## Accounts & Access - Key Principle
- Matt wants dedicated accounts for Halo's tools — separate from his personal ones
- Currently I only have access via: Anthropic API key (already set up)
- To-do: set up dedicated accounts for Twilio, Deepgram, ElevenLabs, etc. as needed
- Security priority: separate logins for everything

## GHL Integration - Plan Written, Ready to Build
- Full integration plan in `memory/ghl-integration-plan.md`
- Can auto-import leads from Saleshandy, Facebook Ads, GHL forms
- Can auto-update pipeline stages on booking + stage changes
- Architecture: Cloudflare Worker or n8n (self-hosted) as the router
- **Blocker**: Matt needs to provide GHL Location API Key + pipeline stage names
- Estimated build: 1–2 days once I have the API key

## Marketing Knowledge Base
- Full research library in `memory/marketing-mastery/` (14 files)
- Covers: industry landscape, Facebook ads, Google ads, agency scaling, patient funnel, cold outreach, niche playbooks (chiro/dental/telehealth), sales framework, agency owner lessons, ad creative swipe file, client onboarding/retention, marketing Halo itself, full financial model
- Ask me anything about digital marketing for healthcare and I'll have the answer
- Key lesson: Halo's differentiator = full-funnel (ads + AI follow-up). No competitor does this at the mid-market price point.
- Lead scraper: `tools/lead_scraper.py` — pulls from NPI Registry. Pre-built: 500 VA chiros + 500 VA dentists in `tools/`

## My Role
- Personal assistant → eventually managing agent teams for his business
- Priority: Halo Marketing growth
- Upcoming: security setup (personal + business)
- Matt may share Halo Marketing cloud/Notion info for deeper context

## Name
- I'm named Halo (Matt chose it)
- Coincidentally same name as his marketing agency — Halo Marketing

## Matt's Rules for Me
- **Always ask before downloading anything** — no surprise installs
- **Always ask before using personal info** — flag it, don't assume
- Security measures coming at some point (TBD)

## Setup Notes
- Telegram is the main channel
- WhatsApp also connected (but was having connectivity issues)
- ffmpeg installed at ~/bin/ffmpeg (arm64 static build)
- Whisper installed (Python 3.9) at ~/Library/Python/3.9/bin/whisper
- No Homebrew installed (needs admin password); workaround: ~/bin/ for binaries
- Memory search: LIVE — OpenAI text-embedding-3-small, 4 files indexed, 32 chunks, vector + FTS
- Cron jobs: morning brief (9am ET) + nightly memory (11pm ET) — written to ~/.openclaw/cron/jobs.json
- **web_search broken**: needs Brave API key (`openclaw configure --section web`). Matt doesn't have one yet.
- CLI pairing: FIXED 2026-02-21 — approved pending repair via `openclaw devices approve`. `openclaw cron list`, `openclaw gateway call`, all commands working.

## First Session: 2026-02-20
- Did bootstrap, got name, set up identity
- Transcribed voice message to learn about Matt
