# Intent

## Definition

“Never stop” means: do not yield early. Continue working until the phase is complete or you are genuinely blocked (missing input, missing secrets, missing infra connectivity, etc.).

## Composition (use existing phase skills as subroutines)

- Use `$phase-implement` to execute the active phase sequentially (subphase-by-subphase).
- Use `$phase-gaps` as a RED TEAM wrap-up every turn to tighten the plan and surface assumptions + questions.
- Use `$phase-review` when the phase is complete to verify quality gates and document evidence.
- Use `$phase-plan` only when **no phase exists** and the user explicitly wants you to create one (default behavior is “always resume latest”).
- Apply `$karpathy-guidelines` at the start of every turn (simplicity + surgical changes + explicit assumptions + verification loop discipline).
- Use `$recursive-reasoning-operator` whenever you are grounding decisions in provided materials (phase plans, reference docs, pasted excerpts), then synthesize back into the Terminus Maximus progress updates and user-facing response skeleton.
- If documentation is requested/mentioned (or behavior is version-sensitive), use `$context7-docs` to fetch current docs via Context7 MCP (resolve then query), then synthesize back into Terminus Maximus outputs.

## Done definition

A phase is “done” when:

- Every subphase plan has non-empty **Output** and non-empty **Handoff**.
- The root plan’s **Success Criteria** are checked/updated and a Phase Summary exists.
- The phase has been reviewed via `$phase-review` (including `npm run lint`, `npm run build`, and `npm run db:push` if Prisma schema changed).
