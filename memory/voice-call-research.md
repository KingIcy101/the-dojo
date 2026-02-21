# Voice Call System Research

## Goal
Matt calls a real phone number → has a natural voice conversation with Halo → feels like a casual phone call.

## Recommended Stack: Twilio + OpenAI Realtime API

### Why This Combo
- **Twilio** handles the actual phone call (real phone number, PSTN connectivity)
- **OpenAI Realtime API** handles speech-in → AI response → speech-out, all in real time, very low latency
- Together: you call a number, Twilio routes the audio stream to our server, OpenAI processes it, audio response streams back. No awkward pauses.

### What's Needed

#### Accounts / API Keys
1. **Twilio account** — twilio.com (free trial gives credit to start)
   - Phone number: ~$1/month (local US number)
   - Call cost: ~$0.01/min inbound + outbound
2. **OpenAI API key** — for Realtime API (gpt-4o-realtime)
   - Realtime API pricing: ~$0.06/min audio input + $0.24/min audio output (rough estimate)
   - A 10-min call ≈ ~$3 — not cheap but fine for personal use

#### Infrastructure
- A small server with a public URL to receive Twilio webhooks
  - Option A: Run locally + ngrok tunnel (free, great for dev/testing)
  - Option B: Deploy to a small VPS or cloud function (~$5/mo on Fly.io or Railway)
  - Option C: Run on the Mac mini with port forwarding (possible but more complex)

### How It Works (Flow)
1. Matt calls Twilio number
2. Twilio sends audio stream to our server via WebSocket
3. Server pipes audio to OpenAI Realtime API
4. OpenAI responds with audio in real time
5. Server pipes audio back to Twilio → Matt hears Halo's voice

### Build Effort
- Node.js or Python server (~200-300 lines)
- Twilio + OpenAI SDKs both well-documented
- Reference: https://github.com/twilio-samples/speech-assistant-openai-realtime-api-node
- Estimated build time: a few hours

## Simpler Alternative: Telegram Voice Notes (Current)
What we're already doing — voice memos back and forth via Telegram. Not a real phone call but works well for async. No extra cost or setup.

## Recommendation
1. Short term: keep using Telegram voice memos (working well)
2. When ready to build: Twilio + OpenAI Realtime API is the cleanest path
3. Need from Matt: Twilio account + OpenAI API key (or approval to set them up)

## Cost Estimate (Monthly)
- Twilio phone number: ~$1
- Call usage (light): ~$5-10
- OpenAI Realtime API: ~$5-20 depending on call volume
- **Total: ~$10-30/month** for casual use
