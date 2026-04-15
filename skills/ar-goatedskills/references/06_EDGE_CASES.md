# Edge Cases

## No phases exist / planning folder missing

- If `docs/planning/` is missing: ask the user if you should create it (do not assume).
- If `docs/planning/phase-*` is empty: do not auto-create a phase. Ask if you should run `$phase-plan`.
- Apply `$karpathy-guidelines` here: stop and ask instead of guessing, and keep questions to the smallest set that unblocks progress.

## Latest phase is complete

- If the highest numbered phase is complete:
  - Ask the user whether to create a new phase (via `$phase-plan`) or stop.

## Another agent changed files you need

- Re-read the current file state.
- Identify who changed it (recent phases + `git log`).
- Merge semantically (do not overwrite).
- Document coordination in the active subphase Output.
- If resolving conflicts depends on a specific plan’s text, use `$recursive-reasoning-operator` to ground the merge decision, then continue the Terminus Maximus loop.

## Missing env vars / infra connectivity

- If env vars are missing for lint/build/test:
  - Record the blocker in phase docs.
  - Instruct `vercel env pull .env.local` (or specify exactly which vars are needed).
- If Vercel is not linked:
  - Record the blocker and instruct `vercel link`.

## Time/compute limits

- Do the smallest high-signal validation you can.
- Document what remains and why.
- Still run the per-turn wrap-up: update phase docs + `$phase-gaps` + ask targeted questions.
