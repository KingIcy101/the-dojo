# Next.js + Sentry Instrumentation (Guidance)

Use this as guidance when adding or updating Sentry instrumentation in a Next.js app.

## Exception Catching

Use `Sentry.captureException(error)` to capture an exception and log it to Sentry.

- Use inside `try/catch` blocks (or other places where errors are expected)
- Prefer attaching context (tags/extra) rather than stringifying large objects into the message

Example:

```ts
import * as Sentry from "@sentry/nextjs";

try {
  await doWork();
} catch (error) {
  Sentry.captureException(error);
  throw error;
}
```

## Tracing (Spans)

Create spans for meaningful actions like button clicks, API calls, and important function calls.

- Use `Sentry.startSpan` to create a span
- Child spans can exist within a parent span
- `op` and `name` should be meaningful and stable
- Add attributes for relevant context/metrics

### Component action instrumentation

```tsx
import * as Sentry from "@sentry/nextjs";

function TestComponent() {
  const handleTestButtonClick = () => {
    Sentry.startSpan(
      {
        op: "ui.click",
        name: "Test Button Click",
      },
      (span) => {
        const value = "some config";
        const metric = "some metric";

        span.setAttribute("config", value);
        span.setAttribute("metric", metric);

        doSomething();
      },
    );
  };

  return (
    <button type="button" onClick={handleTestButtonClick}>
      Test Sentry
    </button>
  );
}
```

### API call instrumentation

```ts
import * as Sentry from "@sentry/nextjs";

async function fetchUserData(userId: string) {
  return Sentry.startSpan(
    {
      op: "http.client",
      name: `GET /api/users/${userId}`,
    },
    async () => {
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();
      return data;
    },
  );
}
```

## Logs

When using logs, import Sentry with:

```ts
import * as Sentry from "@sentry/nextjs";
```

Enable logs in Sentry initialization:

```ts
Sentry.init({
  // dsn: process.env.SENTRY_DSN,
  enableLogs: true,
});
```

Reference the logger:

```ts
const { logger } = Sentry;
```

Sentry offers `consoleLoggingIntegration` to send specific console call types as logs without instrumenting individual logger calls:

```ts
Sentry.init({
  // dsn: process.env.SENTRY_DSN,
  enableLogs: true,
  integrations: [
    Sentry.consoleLoggingIntegration({ levels: ["log", "warn", "error"] }),
  ],
});
```

### Logger examples

`logger.fmt` is a template-literal function you can use to capture variables as structured log fields.

```ts
const { logger } = Sentry;

logger.trace("Starting database connection", { database: "users" });
logger.debug(logger.fmt`Cache miss for user: ${userId}`);
logger.info("Updated profile", { profileId: 345 });
logger.warn("Rate limit reached for endpoint", {
  endpoint: "/api/results/",
  isEnterprise: false,
});
logger.error("Failed to process payment", {
  orderId: "order_123",
  amount: 99.99,
});
logger.fatal("Database connection pool exhausted", {
  database: "users",
  activeConnections: 100,
});
```

## Configuration Locations (Next.js)

In Next.js, Sentry initialization typically belongs in:

- Client: `instrumentation-client.(js|ts)`
- Server: `sentry.server.config.ts`
- Edge: `sentry.edge.config.ts`

Avoid duplicating `Sentry.init(...)` in other files; initialize once in the appropriate Sentry config files and import `@sentry/nextjs` to use Sentry APIs elsewhere.

