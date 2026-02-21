# Patient Acquisition Funnel — Full System Design

_How to turn ad spend into booked patients. Halo's core product._
_Research by Halo. 2026-02-21._

---

## The Problem Every Practice Has (That Halo Solves)

Most practices have a marketing AWARENESS problem — they're invisible. But when Halo runs ads, a new problem emerges: they have a CONVERSION problem. Leads come in but don't become patients.

Why leads don't convert:
1. **No immediate follow-up** — lead submits form, waits 2 hours for a call, already booked elsewhere
2. **Poor phone handling** — receptionist is busy, doesn't call back
3. **No follow-up sequence** — after first failed contact, the lead is forgotten
4. **Bad booking process** — too many steps to get an appointment
5. **No-shows** — patients book but don't show up

Halo's system addresses ALL five. This is the product differentiation.

---

## The Full Funnel (End-to-End)

```
[Facebook/Google Ad]
       ↓
[Landing Page — GHL]
       ↓
[Lead Form Submission]
       ↓
[Immediate SMS (within 60 seconds)]
       ↓
[Bland.ai Call (within 2–5 minutes)]
       ↓
[Appointment Booked in GHL Calendar]
       ↓
[Confirmation SMS + Email]
       ↓
[Reminder Sequence (24hr + 2hr)]
       ↓
[Patient Shows Up]
       ↓
[Post-Visit Review Request]
       ↓
[Reactivation Sequence (30/60/90 days)]
```

---

## Stage 1: The Ad (Top of Funnel)

The ad has ONE job: stop the scroll and generate a click.

**What it's NOT:** An ad is not a brochure. It's not "About Us." It's not a list of services.

**What it IS:** A specific message to a specific person about a specific problem you solve.

Best-performing framework: **Problem → Solution → CTA**

Example for chiropractor:
> "Still waking up with back pain every morning? You're not alone — and it's not something you just have to live with. At Dr. Smith Chiropractic, we've helped 200+ [City] residents finally get lasting relief. New patients: schedule your $49 first visit this week."

---

## Stage 2: The Landing Page

The landing page has ONE job: convert the click into a lead submission.

**Critical rules:**
- No navigation menu (remove it — it gives people a way to leave)
- One offer, one CTA, one form — no distractions
- Above-the-fold content: headline + subheadline + form (everything visible without scrolling)
- Load in < 3 seconds (GHL pages load fast — good)
- Mobile-first (80%+ of traffic is mobile)

**The perfect landing page structure:**

```
[HERO SECTION]
Headline: "Finally Get Rid of Back Pain — Book Your New Patient Exam"
Subheadline: "Dr. [Name] has helped 200+ [City] patients find lasting relief. Your first visit is just $49."
Form: Name / Phone / (optional: what's your main concern?) / [Book My Appointment]

[TRUST BAR]
★★★★★ 4.9 Stars | 300+ Reviews | Google Verified

[SOCIAL PROOF]
2–3 testimonials with patient photos + first name + condition

[HOW IT WORKS]
Step 1: Submit form → Step 2: We call you to confirm → Step 3: Come in, feel better

[FAQ]
"Do you accept insurance?" "How long is the first visit?" "What should I expect?"

[SECONDARY CTA]
"Still have questions? Call us at [number]" + [Book Now] button again

[FOOTER]
HIPAA notice | Privacy policy | Address
```

**The form:** Keep it short. Name + Phone is enough. Every additional field reduces conversions ~10%. If you need to qualify, use the Bland.ai call for that.

---

## Stage 3: Immediate Follow-Up (The Money Step)

MIT research (widely cited in sales): contacting a lead within 5 minutes makes you **21x more likely to convert** vs. waiting 30 minutes. Most practices call back in 2–4 hours, if at all.

**Halo's automation sequence:**

**T+0 (form submitted):**
- GHL captures lead, triggers automation
- Lead tagged: "new-facebook-lead" or "new-google-lead"
- Opportunity created in pipeline: "New Lead"

**T+30 seconds:**
- SMS fires: "Hi [First Name]! Thanks for reaching out to [Practice Name]. Our scheduling team will call you in just a few minutes to get you set up. — [Practice Name] Team"

**T+2–5 minutes:**
- Bland.ai call triggers
- AI script: "Hi, is this [First Name]? Great! This is [Team Name] calling from [Practice Name]. I saw you were interested in scheduling — do you have just 2 minutes to get that set up for you?"
- Handles: "Yes" (books appointment), "I'm busy right now" (schedules callback), "I have questions" (captures and routes to practice), "Not interested" (marks in GHL)

**T+30 minutes (if no answer):**
- Second SMS: "Hi [First Name], we just tried to reach you. We'd love to get your appointment scheduled! Here's a link to book online: [GHL booking link]"

---

## Stage 4: The 7-Day Follow-Up Sequence

Most leads require 5–8 touchpoints before converting. Most practices stop after 1–2.

**Sequence (assuming no answer to initial calls):**

| Day | Channel | Message |
|---|---|---|
| 0 | SMS | Thank you + we'll call |
| 0 | Call (Bland.ai) | Booking attempt |
| 1 | SMS | "Still interested? Here's our booking link" |
| 2 | Call | Second human/AI attempt |
| 3 | Email | Educational content + soft CTA (builds trust) |
| 5 | SMS | "We have a few openings left this week — want to grab one?" |
| 7 | Call | Final attempt |
| 7 | SMS | "We'll keep your info on file. If you ever decide you'd like to schedule, we're here." |

After day 7 → move to "Long-term nurture" (monthly touch, educational content, seasonal offers)

---

## Stage 5: Appointment Confirmation + Reminders

Even after someone books, they might not show. No-show rates in healthcare: 10–30% without reminders.

**Confirmation sequence:**

**Immediately after booking:**
- Email: Appointment confirmation with date/time, address, parking, what to bring
- SMS: "Your appointment at [Practice] is confirmed for [Date] at [Time]. See you then! [address link]"

**24 hours before:**
- SMS: "Reminder: You have an appointment tomorrow at [Time] with Dr. [Name]. Please reply YES to confirm or call us to reschedule."
- If no reply after 4 hours → second reminder

**2 hours before:**
- SMS: "Just a reminder — you have an appointment in 2 hours at [time]. We look forward to seeing you!"

**If they reply NO or don't confirm:**
- Immediate SMS: "No problem! Let's find another time that works. Here's our booking link: [link]"
- Or Bland.ai call to reschedule

**No-show follow-up:**
- SMS same day: "We missed you today! Let's get you rescheduled. Here's our booking link."
- Call next day (Bland.ai or human)

---

## Stage 6: Post-Visit — The Retention and Review Loop

**Review request (gold):**
- 2–4 hours after appointment (when the positive experience is fresh)
- SMS: "Hi [First Name]! How was your visit with Dr. [Name] today? If we did a great job, we'd really appreciate a quick Google review — it takes 30 seconds and helps other patients find us. [direct Google review link]"
- Email backup if SMS doesn't get click in 48 hours

**Reactivation for patients who haven't returned:**
- 30 days post-visit (for ongoing care patients): "Time for your next session? Here's our booking link."
- 60 days (gentle reminder): "We haven't seen you in a while — how are you feeling?"
- 90 days (win-back offer): "We miss you! Book this month and get 10% off your visit."

**For one-visit patients who didn't return:**
- This is a care plan conversion problem — Halo can consult on how practices present treatment plans to improve conversion from first visit to ongoing care

---

## GHL Setup Checklist for Each New Client

When a new client onboards, Halo should set up:

- [ ] GHL sub-account created (use niche template)
- [ ] Pipeline configured: New Lead → Contacted → Appointment Booked → Showed → Converted → Won / Lost
- [ ] Calendar connected to practice's booking system (or GHL calendar used)
- [ ] Landing page built (use niche template + client's brand colors, name, photos)
- [ ] Facebook Pixel installed on landing page
- [ ] Google Tag Manager installed on landing page
- [ ] Conversion events configured (form submission)
- [ ] Automation 1: Lead capture → SMS trigger
- [ ] Automation 2: Bland.ai call trigger
- [ ] Automation 3: 7-day follow-up sequence
- [ ] Automation 4: Appointment confirmation + reminders
- [ ] Automation 5: Post-visit review request
- [ ] Bland.ai script written and configured for this practice
- [ ] Google Ads account created or access granted
- [ ] Facebook Ads account created or access granted
- [ ] Initial campaigns launched
- [ ] Reporting dashboard configured (or monthly report template ready)
- [ ] Client added to Slack channel for comms
- [ ] Kickoff call scheduled

**Time to onboard (target):** 3–5 business days from signed contract to live ads

---

## The Lifetime Value Calculation (Per Client Niche)

This matters because it determines how much the practice should spend:

| Practice Type | Avg First Visit | Avg Ongoing/Year | Avg LTV (3 years) |
|---|---|---|---|
| Chiropractor | $75–$150 | $800–$2,400 | $1,500–$4,000 |
| Dentist | $150–$300 first | $500–$1,500/year | $2,000–$6,000 |
| Dental (cosmetic) | $500–$5,000 | $500/year | $3,000–$12,000 |
| Telehealth (chronic) | $100–$200 | $1,200–$3,600 | $2,500–$8,000 |
| Med spa | $200–$800 | $1,500–$5,000 | $4,000–$15,000 |

**Use this in the sales conversation:**
> "If you get 8 new chiropractic patients this month and each is worth $2,000 to your practice over the next 3 years, that's $16,000 from one month of our service. At $1,950/month management fee, you need just one new patient per month to break even — everything else is profit."

This math closes deals.
