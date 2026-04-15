# The Feedback Loop

This is what separates "posting TikToks" from "running a marketing machine." The daily cron pulls data from two sources:

- **Postiz** → per-post TikTok analytics (views, likes, comments, shares)
- **RevenueCat** (if connected) → conversion data (trial starts, paid subscriptions, revenue)

## The Daily Cron

Every morning before the first post, the cron runs `scripts/daily-report.js`:

1. Pulls the last 3 days of posts from Postiz (posts peak at 24-48h)
2. Fetches per-post analytics for each (views, likes, comments, shares)
3. If RevenueCat is connected, pulls conversion events in the same window (24-72h attribution)
4. Cross-references: which posts drove views AND which drove paying users
5. Applies the diagnostic framework to determine what's working
6. Generates `tiktok-marketing/reports/YYYY-MM-DD.md` with findings
7. Messages the user with a summary + suggested hooks for today

## The Diagnostic Framework

Two axes: views (are people seeing it?) and conversions (are people paying?).

### 🟢 High Views + High Conversions → SCALE IT
- This is working. Make 3 variations of the winning hook immediately
- Test different posting times to find the sweet spot
- Cross-post to more platforms for extra reach
- Don't change anything about the CTA — it's converting

### 🟡 High Views + Low Conversions → FIX THE CTA
- The hook is doing its job — people are watching. But they're not downloading/subscribing
- Try different CTAs on slide 6 (direct vs subtle, "download" vs "search on App Store")
- Check if the app landing page matches the promise in the slideshow
- Test different caption structures — maybe the CTA is buried
- The hook is gold — don't touch it. Fix everything downstream

### 🟡 Low Views + High Conversions → FIX THE HOOKS
- The people who DO see it are converting — the content and CTA are great
- But not enough people are seeing it, so the hook/thumbnail isn't stopping the scroll
- Test radically different hooks (person+conflict, POV, listicle, mistakes format)
- Try different posting times and different slide 1 images
- Keep the CTA and content structure identical — just change the hook

### 🔴 Low Views + Low Conversions → FULL RESET
- Neither the hook nor the conversion path is working
- Try a completely different format or approach
- Research what's trending in the niche RIGHT NOW (use browser)
- Consider a different target audience angle
- Test new hook categories from scratch
- Reference competitor research for what's working for others

### 🔴 High Views + High Downloads + Low Paying Subscribers → APP ISSUE
- The marketing is working. People are watching AND downloading. But they're not paying.
- This is NOT a content problem — the app onboarding, paywall, or pricing needs fixing.
- Check: Is the paywall shown at the right time? Is the free experience too generous?
- Check: Does the onboarding guide users to the "aha moment" before the paywall?
- Check: Is the pricing right? Too expensive for the perceived value?
- This is a signal to pause posting and fix the app experience first

### 🟡 High Views + Low Downloads → CTA ISSUE
- People are watching but not downloading. The hooks work, the CTAs don't.
- Rotate through different CTAs: "link in bio", "search on App Store", app name only, "free to try"
- Check the App Store page — does it match what the TikTok shows?
- Check that "link in bio" actually works and goes to the right place

## Hook Performance Tracking

Track in `tiktok-marketing/hook-performance.json`:

```json
{
  "hooks": [
    {
      "postId": "postiz-id",
      "text": "My boyfriend said our flat looks like a catalogue",
      "app": "snugly",
      "date": "2026-02-15",
      "views": 45000,
      "likes": 1200,
      "comments": 45,
      "shares": 89,
      "conversions": 4,
      "cta": "Download Snugly — link in bio",
      "lastChecked": "2026-02-16"
    }
  ],
  "ctas": [
    {
      "text": "Download [App] — link in bio",
      "timesUsed": 5,
      "totalViews": 120000,
      "totalConversions": 8,
      "conversionRate": 0.067
    }
  ],
  "rules": {
    "doubleDown": ["person-conflict-ai"],
    "testing": ["listicle", "pov-format"],
    "dropped": ["self-complaint", "price-comparison"]
  }
}
```

## Decision Rules

- **50K+ views** → DOUBLE DOWN — make 3 variations immediately
- **10K-50K** → Good — keep in rotation
- **1K-10K** → Try 1 more variation
- **<1K twice** → DROP — try something radically different
