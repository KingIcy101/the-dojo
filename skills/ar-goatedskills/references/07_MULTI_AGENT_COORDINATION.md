# Multi-Agent Coordination

Follow the same coordination procedure as `$phase-implement` and `$phase-gaps`.

## Standard commands

- `git status --porcelain`
- `ls -dt docs/planning/phase-* | head -10`
- `git log --oneline -5 -- <file>`

## Guardrails

- Apply `$karpathy-guidelines` before merging: avoid drive-by refactors, touch only what the active subphase requires, and state assumptions explicitly.
- If coordination depends on interpreting written intent (plans, notes, pasted excerpts), use `$recursive-reasoning-operator` to ground that interpretation before making edits.
