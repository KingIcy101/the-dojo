# RED TEAM Checklist (use every time)

This is a **RED TEAM** checklist. Treat every unchecked item as a likely future bug.

## RED TEAM: Repo reality

- RED TEAM: Do referenced files exist?
- RED TEAM: Do referenced functions/symbols exist?
- RED TEAM: Are file paths correct (no stale filenames)?
- RED TEAM: Are environment variables real and named correctly?

## RED TEAM: Data model & migrations

- RED TEAM: Does the plan change `prisma/schema.prisma`? If yes, does it include `db:push` and verification?
- RED TEAM: Is there a backfill/upgrade path for existing rows?
- RED TEAM: Is there a rollback strategy?

## RED TEAM: API/webhooks/cron

- RED TEAM: Are request auth/secret checks specified?
- RED TEAM: Is input treated as untrusted (validation + sanitization)?
- RED TEAM: Are timeouts and retries explicitly planned?
- RED TEAM: Is idempotency/dedupe planned for repeated events?

## RED TEAM: AI/LLM specifics

- RED TEAM: Is output shape enforceable (json_schema) when needed?
- RED TEAM: Are parse failures handled and recorded (telemetry)?
- RED TEAM: Are budgets set so reasoning doesn’t consume output tokens?
- RED TEAM: Does the plan prevent “template drift” (variation driver beyond temperature)?

## RED TEAM: Permissions & admin gating

- RED TEAM: Are settings changes gated appropriately (admin-only vs user-level)?
- RED TEAM: Are there explicit authorization checks in server actions/routes?

## RED TEAM: Observability

- RED TEAM: Are telemetry featureId/promptKey names defined?
- RED TEAM: Are errors surfaced/logged in a debuggable way?

## RED TEAM: QA & success criteria

- RED TEAM: Are success criteria measurable and falsifiable?
- RED TEAM: Do test steps match how the system is actually triggered (webhook, UI, cron)?
- RED TEAM: Are edge cases included (timeouts, partial failures, duplicates)?

## RED TEAM: Spec clarity & human input

- RED TEAM: Are unresolved decisions captured as **Open Questions (Need Human Input)**?
- RED TEAM: Does each open question include "why it matters" + a default assumption?
- RED TEAM: Are key assumptions listed so humans can correct them quickly?

## RED TEAM: Multi-agent coordination

- RED TEAM: Have you scanned the last 10 phases for file/domain overlaps?
- RED TEAM: Are there uncommitted changes from other agents that affect this plan?
- RED TEAM: Does the plan depend on work from another active phase?
- RED TEAM: If overlaps exist, is there a coordination strategy documented?
- RED TEAM: Are shared files (schema, lib utilities) handled with awareness of concurrent changes?
- RED TEAM: Is there a conflict resolution strategy for merge scenarios?
