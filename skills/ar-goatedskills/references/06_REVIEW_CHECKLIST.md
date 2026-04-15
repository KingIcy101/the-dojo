# Review Checklist

Use this checklist every time.

## Repo + plan hygiene

- Phase selected correctly (highest N if unspecified).
- Root `plan.md` exists and Subphase Index matches folders.
- All subphase `plan.md` files exist.
- Subphase completion state is recorded (Output/Handoff present or missing).

## What shipped (evidence)

- `git status` captured (or equivalent evidence if not a git checkout).
- `git diff --name-only` captured.
- Key changed files referenced in the review.

## Quality gates

- `npm run lint` executed and result recorded.
- `npm run build` executed and result recorded.
- If Prisma schema changed: `npm run db:push` attempted and result recorded.

## Success criteria mapping

- Each success criterion has an explicit status: met / partial / not met.
- Each criterion has evidence (file path, command output summary, or repro steps).

## Implementation correctness (CRITICAL)

- For each subphase with code changes, verify that the implementation matches what was planned:
  - Check that planned files were actually created/modified.
  - Verify planned functions/models exist and have the documented behavior.
  - Confirm integrations are wired correctly (e.g., if plan says "call X from Y", verify X is actually called from Y).
  - Check that data flows as described (e.g., if plan says "upsert on positive sentiment", verify the condition is implemented).
- If deviations exist, document them explicitly as "planned vs implemented" in the review.
- Do NOT mark criteria as "met" based solely on plan documentation — verify the actual code.

## Observability / telemetry (when relevant)

- If the phase touches AI features: verify telemetry identifiers (featureId/promptKey) are present and referenced.

## Follow-ups

- Any partial/not-met items have concrete next steps.
- Optional: suggest a next phase when follow-ups are substantial.

## Multi-agent coordination (when applicable)

- Checked last 10 phases for file overlaps with this phase.
- Verified that concurrent changes from other phases don't conflict.
- If merges occurred, verified merge correctness.
- Coordination notes (if any) match what actually happened.
- Build/lint verified against combined state of all concurrent work.
- Documented any integration issues encountered and how they were resolved.
