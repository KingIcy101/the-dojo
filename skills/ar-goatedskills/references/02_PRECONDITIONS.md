# Preconditions

## Phase selection (deterministic)

1. If the user explicitly says “Phase N”, use that `N`.
2. Otherwise, choose the highest numbered `docs/planning/phase-*` directory.

If **no** `docs/planning/phase-*` exists:

- Do **not** create a new phase automatically.
- Ask the user if they want you to run `$phase-plan` to create a new phase.
  - If yes: run `$phase-plan`, then continue execution.
  - If no: proceed without phases and explain that you cannot follow the “resume latest phase” loop without a phase.

## Reasoning guardrails (always-on)

- Apply `$karpathy-guidelines` before choosing defaults or making edits: state assumptions explicitly and avoid speculative work.
- If you are selecting a phase/subphase based on a provided document, use `$recursive-reasoning-operator` to ground the choice, then continue with the Terminus Maximus procedure.

## Environment blocker checks (use when relevant)

Only run checks that are relevant to the work you need to do.

- If builds/tests require env:
  - Verify `.env.local` exists and is non-empty.
  - If missing/empty: instruct the user to run `vercel env pull .env.local` (or provide the required env vars another way).
- If Vercel linkage is required:
  - Verify `.vercel/` exists for the repo.
  - If missing: instruct the user to run `vercel link`.
- If Supabase connectivity is required:
  - Look for a project ref/config in repo docs or tooling config.
  - If missing: ask the user for the Supabase project ref and whether it is prod or dev.
