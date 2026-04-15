# Edge Cases

## No phases exist

If `docs/planning/` has no `phase-*` folders, you can’t run this skill.

- Ask the user if they want `phase-plan` first.

## Lint/build fails due to missing env

Some Next.js builds require env vars.

- Record failure clearly.
- List the exact missing env var(s) or error summary.
- Suggest rerunning after `vercel env pull .env.local` (if that’s the repo’s standard) or after configuring required vars.

## Prisma schema changed but db:push can’t run

If `npm run db:push` fails (missing `DIRECT_URL`/DB access):

- Record failure.
- Note what envs are required.
- Do not claim the phase is complete if schema wasn’t applied.

## Subphase plans not updated during implementation

If Output/Handoff are missing:

- Fill them using evidence.
- If evidence is insufficient, write “unknown” and add a follow-up asking for missing context.

## User wants rollout validation

If the user asks to verify live deploy behavior:

- Stop and switch to the appropriate live testing skill (e.g., Playwright live-env skill) before marking success criteria as met.
