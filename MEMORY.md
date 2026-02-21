# MEMORY.md - Long-Term Memory

## About Matt
- 24 years old, Virginia, entrepreneur
- Graduated 2023, went full-time on Amazon business
- Currently building Halo Marketing as his primary focus
- Amazon/Walmart business is largely automated (has VA)
- Wants to exit Source Start (sourcestart.io) in 2026
- Works out nearly daily, has family + girlfriend
- Wants to scale hard in his 20s

## His Businesses
- **Halo Marketing** — marketing agency for healthcare practitioners (FB/Google ads, appt reminders, websites, social). Partner: Preston. MAIN FOCUS.
- **Amazon/Walmart** — name brand + supplement products, mostly automated. Partner: Mateo.
- **SourceDart** (sourcedart.io) — Walmart sourcing tool, wants to exit 2026.

## Halo Marketing - Current State
- 2 clients, both referrals, both at $1k/month (standard retainer is $2k)
- Biggest bottleneck: building front-end sales team
- Looking at Colombia for sales talent (SDR/booking role)
- Fulfillment is solid — main gap is lead gen + sales
- Goal: booked discovery calls that convert to closes

## Halo Marketing - Sales Flow
- Leads found manually → tracked in Google Sheet
- Sales rep cold calls to book discovery call (call 1)
- Discovery call: gauge interest, if yes → book close call (call 2)
- Close call: proposal + contracts sent
- Then moved to onboarding → account manager handles
- Had an account manager, had to let her go — need a new one
- Matt + Preston running discovery calls themselves for now (too few clients to need hand-off yet)
- Plan: train sales reps to run discovery calls once volume picks up
- Sales rep comp: 20% of $2K retainer ($400/close) until 50 active clients + 5% residuals for 6 months per active client
- Sales rep handles full process: outreach → meeting → close → hand off to account manager
- CRM: GoHighLevel (GHL) — set up but leads not fully mapped in yet (needs dev work)
- GHL is the goal for central CRM for everything

## Voice Call System - Plan
- Goal: Matt or Preston can call a number and have a natural voice conversation with Halo
- Also want me "in a meeting" — could be a conference line they add me to
- Smart cost idea: use existing memory/workspace files as context instead of sending everything via API each call (reduces token costs)
- Tech stack: Twilio + either OpenAI Realtime API OR cheaper pipeline (Deepgram STT + Claude + ElevenLabs TTS)
- Need: Twilio account + OpenAI API key to build
- On the backlog — Matt wants full cost breakdown first

## GHL Integration - On the List
- Connect leads and pipeline into GoHighLevel automatically
- Their API is solid, can build automations
- High-leverage project for Halo Marketing

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

## First Session: 2026-02-20
- Did bootstrap, got name, set up identity
- Transcribed voice message to learn about Matt
