---
name: cal-com-booking-embed
description: Embed a Cal.com booking modal in Next.js with custom branding, CTA trigger, and post-booking redirect.
category: dev
---

# Cal.com Booking Embed

## When to Use
Any page with a "Book a Call" or "Schedule Demo" CTA. Matt's link: cal.com/matt-bender-ai/30min.
Use modal embed for best UX — keeps user on page. Full embed for dedicated booking pages.

## Steps
1. `npm install @calcom/embed-react`
2. Set `NEXT_PUBLIC_CAL_LINK=matt-bender-ai/30min` in .env
3. Add `<CalProvider>` wrapper (or use `getCalApi` directly)
4. Trigger modal on CTA button click
5. Handle `bookingSuccessful` callback for redirect/confirmation

## Key Patterns / Code

### Modal Embed (Recommended)
```tsx
// components/BookingModal.tsx
'use client';
import { useEffect } from 'react';
import { getCalApi } from '@calcom/embed-react';

export function BookCallButton({ label = 'Book a Call' }) {
  useEffect(() => {
    (async () => {
      const cal = await getCalApi({ namespace: 'itp-demo' });
      cal('ui', {
        theme: 'dark',
        styles: { branding: { brandColor: '#6366f1' } },
        hideEventTypeDetails: false,
      });
    })();
  }, []);

  return (
    <button
      data-cal-namespace="itp-demo"
      data-cal-link={process.env.NEXT_PUBLIC_CAL_LINK}
      data-cal-config='{"layout":"month_view"}'
      className="btn-primary"
    >
      {label}
    </button>
  );
}
```

### Cal Atoms (Headless — more control)
```tsx
// For fully custom UI with Cal.com logic
import { CalProvider, Booker } from '@calcom/atoms';

export function BookingPage() {
  return (
    <CalProvider
      clientId={process.env.NEXT_PUBLIC_CAL_CLIENT_ID}
      options={{ apiUrl: 'https://api.cal.com/v2', refreshUrl: '/api/cal/refresh' }}
    >
      <Booker
        eventSlug="30min"
        username="matt-bender-ai"
        onCreateBooking={(booking) => {
          // Redirect or show confirmation
          router.push(`/booking-confirmed?id=${booking.uid}`);
        }}
      />
    </CalProvider>
  );
}
```

### Post-Booking Redirect via URL Param
```
https://cal.com/matt-bender-ai/30min?redirect_url=https://app.inthepast.ai/onboarding
```

### Mobile Full-Screen Overlay
```css
/* Cal modal is fullscreen on mobile by default */
/* Override via cal('ui', ...) styles if needed */
@media (max-width: 768px) {
  [data-cal-namespace] { width: 100vw !important; }
}
```

## Gotchas
- `namespace` must be unique per page if you embed multiple event types
- `getCalApi` must be called client-side only (`'use client'` or useEffect)
- Cal Atoms requires OAuth app setup in Cal.com dashboard (separate from API key)
- Embed script auto-injects — no need to add `<script>` tags manually with `@calcom/embed-react`
- For ITP demo booking, use `NEXT_PUBLIC_CAL_LINK=matt-bender-ai/30min` across all apps