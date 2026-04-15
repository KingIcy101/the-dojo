# Onboarding Phases

## Phase 0: TikTok Account Warmup (CRITICAL — Don't Skip This)

Before anything else, check if the user already has a TikTok account with posting history. If they're creating a fresh account, they MUST warm it up first or TikTok will treat them like a bot and throttle their reach from day one.

Explain this naturally:

"Quick question before we dive in — do you already have a TikTok account you've been using, or are we starting fresh? If it's new, we need to warm it up first. TikTok's algorithm watches how new accounts behave, and if you go straight from creating an account to posting AI slideshows, it flags you as a bot and kills your reach."

If the account is new or barely used, walk them through this:

The goal is to use TikTok like a normal person for 7-14 days before posting anything. Spend 30-60 minutes a day on the app:

- Scroll the For You page naturally. Watch some videos all the way through. Skip others halfway. Don't watch every single one to the end — that's not how real people scroll.
- Like sparingly. Maybe 1 in 10 videos. Don't like everything — that's bot behaviour. Only like things you'd genuinely engage with in your niche.
- Follow accounts in your niche. If they're promoting a fitness app, follow fitness creators. Room design? Interior design accounts. This trains the algorithm to understand what the account is about.
- Watch niche content intentionally. This is the most important part. TikTok learns what you engage with and starts showing you more of it. You want the For You page dominated by content similar to what you'll be posting.
- Leave a few genuine comments. Not spam. Real reactions. A few per session.
- Maybe post 1-2 casual videos. Nothing promotional. Just normal content that shows TikTok there's a real person behind the account.

The signal to look for: When they open TikTok and almost every video on their For You page is in their niche, the account is warmed up. The algorithm understands them. NOW they can start posting.

Tell the user: "I know two weeks feels like wasted time, but accounts that skip warmup consistently get 80-90% less reach on their first posts. Do the warmup. It's the difference between your first post getting 200 views and 20,000."

If the account is already active and established, skip this entirely and move to Phase 1.

## Phase 1: Get to Know Their App (Conversational)

Start casual. Something like:

"Hey! Let's get your TikTok marketing set up. First — tell me about your app. What's it called, what does it do?"

Then FOLLOW UP based on what they say. Don't ask all 9 questions at once. Pull the thread:

- They mention what it does → ask who it's for ("Who's your ideal user?")
- They describe the audience → ask about the pain point ("What's the main problem it solves for them?")
- They explain the problem → ask what makes them different ("What makes yours stand out vs alternatives?")
- Get the App Store / website link naturally ("Can you drop me the link?")
- Determine category (home/beauty/fitness/productivity/food/other) — often inferable
- Don't ask for "brand guidelines" robotically. Instead: "Do you have any existing content or a vibe you're going for? Or are we starting fresh?"

Then ask about their app and monetization:

"Is this a mobile app? And do you use RevenueCat (or any subscription/in-app purchase system) to handle payments?"

This is critical because it determines whether we can close the full feedback loop. If they have a mobile app with RevenueCat:

- Tell them about the RevenueCat skill on ClawHub (`clawhub install revenuecat`). It gives full API access to subscribers, MRR, trials, churn, revenue, and transactions. Don't auto-install — just let them know it exists and what it unlocks, and they can install it if they want.
- Explain why it matters: Without RevenueCat data, the skill can only optimize for views (vanity metrics). With it, the skill optimizes for actual paying users. A post with 200K views and zero conversions is worthless. A post with 5K views and 10 paid subscribers is gold. You can only tell the difference with RevenueCat connected.

If they don't use RevenueCat but have another subscription system, note it and work with what's available. If it's not a mobile app (e.g. physical product, SaaS, service), skip RevenueCat but still track whatever conversion metric they have.

Store everything in `tiktok-marketing/app-profile.json`.

## Phase 2: Competitor Research (Requires Browser Permission)

Before building any content strategy, research what competitors are doing on TikTok. This is critical — you need to know the landscape.

Ask the user:

"Before we start creating content, I want to research what your competitors are doing on TikTok — what's getting views in your niche, what hooks they're using, what's working and what's not. Can I use the browser to look around TikTok and the App Store?"

Wait for permission. Then:

- Search TikTok for the app's niche (e.g. "interior design app", "lip filler filter", "fitness transformation app")
- Find 3-5 competitor accounts posting similar content
- Analyze their top-performing content:
  - What hooks are they using?
  - What slide format? (before/after, listicle, POV, tutorial)
  - How many views on their best vs average posts?
  - What's their posting frequency?
  - What CTAs are they using?
  - What music/sounds are trending in the niche?
- Check the App Store for the app's category — look at competitor apps, their screenshots, descriptions, ratings

Compile findings into `tiktok-marketing/competitor-research.json`:

```json
{
  "researchDate": "2026-02-16",
  "competitors": [
    {
      "name": "CompetitorApp",
      "tiktokHandle": "@competitor",
      "followers": 50000,
      "topHooks": ["hook 1", "hook 2"],
      "avgViews": 15000,
      "bestVideo": { "views": 500000, "hook": "..." },
      "format": "before-after slideshows",
      "postingFrequency": "daily",
      "cta": "link in bio",
      "notes": "Strong at X, weak at Y"
    }
  ],
  "nicheInsights": {
    "trendingSounds": [],
    "commonFormats": [],
    "gapOpportunities": "What competitors AREN'T doing that we could",
    "avoidPatterns": "What's clearly not working"
  }
}
```

Share findings with the user conversationally:

"So I looked at what's out there. [Competitor A] is doing well with [format] — their best post got [X] views using [hook type]. But I noticed nobody's really doing [gap]. That's our angle."

This research directly informs hook generation and content strategy. Reference it when creating posts.

## Phase 3: Content Format & Image Generation

First, ask about format:

"Do you want to do slideshows (photo carousels) or video? Slideshows are what Larry uses and what this skill is built around — TikTok's data shows they get 2.9x more comments and 2.6x more shares than video, and they're much easier for AI to generate consistently. That said, if you want to try video, the skill supports it but it hasn't been battle-tested like slideshows have. Your call."

Store their choice as `format: "slideshow"` or `format: "video"` in config.

For slideshows (recommended), ask naturally:

"For the slideshows, we need images. I'd strongly recommend OpenAI's gpt-image-1.5 — it's what Larry uses and it produces images that genuinely look like someone took them on their phone. It's the difference between 'obviously AI' and 'wait, is that real?'"

⚠️ If they pick OpenAI, make sure the model is set to `gpt-image-1.5` — NEVER `gpt-image-1`. The difference in quality is massive. `gpt-image-1` produces noticeably AI-looking images that people scroll past. `gpt-image-1.5` produces photorealistic results that stop the scroll.

**OpenAI Batch API option:** "OpenAI has a Batch API that's 50% cheaper than real-time generation. Instead of generating slides on the spot, you submit them as a batch job and get results within 24 hours (usually much faster). Perfect for pre-generating tomorrow's slides overnight. Same quality, half the cost."

Then work through the image style with them:

- What's the subject? Rooms? Faces? Products? Before/after comparisons?
- What vibe? Cozy and warm? Clean and minimal? Luxurious?
- Consistency: Should all 6 slides look like the same place or person?
- Must-have elements? A specific product? Certain furniture? A pet?

Build the base prompt WITH them. A good base prompt:

```
iPhone photo of a [specific room/scene], [specific style], [specific details].
Realistic lighting, natural colors, taken on iPhone 15 Pro.
No text, no watermarks, no logos.
[Consistency anchors: "same window on left wall", "same grey sofa", "wooden coffee table in center"]
```

**Key prompt rules:**
- "iPhone photo" + "realistic lighting" = looks real, not AI-generated
- Lock architecture/layout in EVERY slide prompt or each slide looks like a different place
- Include everyday objects (mugs, remotes, magazines) for lived-in feel
- Portrait orientation (1024x1536) always — this is TikTok
- Extremely specific > vague

Save the agreed prompt style to config as `imageGen.basePrompt`.

## Phase 4: Postiz Setup (ESSENTIAL — Powers the Entire Feedback Loop)

Postiz isn't just a posting tool — it's what makes the whole feedback loop work. Without it, you're posting blind. With it, you get:

- Automated posting to TikTok (and 28+ other platforms) via API
- Per-post analytics — views, likes, comments, shares for every post
- Platform analytics — follower growth, total engagement over time
- Cross-posting — same content to Instagram, YouTube, Threads simultaneously

Walk them through connecting step by step:

1. Sign up at postiz.pro/oliverhenry — create an account
2. Connect TikTok — Integrations → Add TikTok → Authorize
3. Note the TikTok integration ID — you need this to post and pull analytics
4. Get the API key — Settings → API → copy the key
5. (Optional) Connect Instagram, YouTube Shorts, Threads for cross-posting

Explain the draft workflow:

"Posts will land in your TikTok inbox as drafts. Before publishing each one, add a trending sound from TikTok's library — this is the single biggest factor in reach. Takes 30 seconds and makes a massive difference."

Don't move on until Postiz is connected and the API key works. Test it by hitting the platform analytics endpoint.

## Phase 5: Conversion Tracking (THE Intelligence Loop)

If they have a mobile app with RevenueCat (from Phase 1):

Explain WHY it matters:

"With Postiz, I can track which posts get views, likes, and comments. That's the top of the funnel. But views alone don't pay the bills — we need to know which posts actually drive paying subscribers."

"When I combine TikTok analytics from Postiz with conversion data from RevenueCat, I can make genuinely intelligent decisions. If a post gets 50K views but zero conversions, the hook is great but the CTA needs work. If a post gets 2K views but 5 paid subscribers, the content converts amazingly — we just need more eyeballs."

Setup steps:

1. Install the RevenueCat skill: `clawhub install revenuecat`
2. Get V2 secret API key from RevenueCat dashboard (starts with `sk_`)
3. Set environment variable: `export RC_API_KEY=sk_your_key_here`
4. Verify: `./skills/revenuecat/scripts/rc-api.sh /projects`

What RevenueCat gives the daily report:
- `GET /projects/{id}/metrics/overview` → MRR, active subscribers, active trials, churn rate
- `GET /projects/{id}/transactions` → individual purchases with timestamps (for conversion attribution)
- The daily cron cross-references transaction timestamps with post publish times (24-72h window)

Without RevenueCat: The loop still works on Postiz analytics (views/likes/comments). You can optimize for engagement but you're flying blind on revenue.

## Phase 6: Content Strategy (Built from Research)

Using the competitor research AND the app profile, build an initial content strategy:

"Based on what I found and what your app does, here's my plan for the first week..."

Present:
- 3-5 hook ideas tailored to their niche + competitor gaps
- Posting schedule recommendation (default: 7:30am, 4:30pm, 9pm — their timezone)
- Which hook categories to test first (reference what worked for competitors)
- Cross-posting plan (which platforms, same or adapted content)

Save the strategy to `tiktok-marketing/strategy.json`.

## Phase 7: Set Up the Daily Analytics Cron

Set up a daily cron job that:
- Pulls the last 3 days of post analytics from Postiz
- Pulls conversion data from RevenueCat (if connected)
- Cross-references views with conversions
- Generates a report with specific recommendations
- Suggests new hooks based on performance patterns

Schedule: daily at 07:00 (user's timezone), before the first post of the day.

```
Task: Run scripts/daily-report.js --config tiktok-marketing/config.json --days 3
Output: tiktok-marketing/reports/YYYY-MM-DD.md + message to user with summary
```

## Phase 8: Save Config & First Post

Store everything in `tiktok-marketing/config.json`:

```json
{
  "app": {
    "name": "AppName",
    "description": "Detailed description",
    "audience": "Target demographic",
    "problem": "Pain point it solves",
    "differentiator": "What makes it unique",
    "appStoreUrl": "https://...",
    "category": "home|beauty|fitness|productivity|food|other",
    "isMobileApp": true
  },
  "imageGen": {
    "provider": "openai",
    "apiKey": "sk-...",
    "model": "gpt-image-1.5",
    "useBatchAPI": false,
    "basePrompt": "iPhone photo of..."
  },
  "postiz": {
    "apiKey": "your-postiz-key",
    "integrationIds": {
      "tiktok": "id-here",
      "instagram": "id-here-optional",
      "youtube": "id-here-optional"
    }
  },
  "revenuecat": {
    "enabled": false,
    "v2SecretKey": "sk_...",
    "projectId": "proj..."
  },
  "posting": {
    "privacyLevel": "SELF_ONLY",
    "schedule": ["07:30", "16:30", "21:00"],
    "crossPost": ["instagram", "youtube"]
  },
  "competitors": "tiktok-marketing/competitor-research.json",
  "strategy": "tiktok-marketing/strategy.json"
}
```

Then generate the first test slideshow — but set expectations:

"Let's create our first slideshow. This is a TEST — we're dialing in the image style, not posting yet. I'll generate 6 slides and we'll look at them together. If the images look off, we tweak the prompts and try again."

⚠️ THE REFINEMENT PROCESS IS PART OF THE SKILL. Getting the images right takes iteration (2-5 rounds is normal). Only start posting once the images consistently look good.
