# Procedure (Terminus Maximus)

Execute these steps literally, in order.

## 0) Guardrails (every turn)

- Apply `$karpathy-guidelines` before doing anything else: state assumptions, keep scope minimal, and pick verifiable checks.
- If documentation is requested/mentioned (or you are answering a version-sensitive platform/library question), apply `$context7-docs` first (Context7 MCP: resolve then query), then continue the Terminus Maximus loop.
- If you need to justify a choice using provided documents (phase plans, reference docs, pasted excerpts), run the `$recursive-reasoning-operator` workflow to ground that choice, then proceed with the Terminus Maximus procedure and templates.

## 1) Select the phase

Follow `02_PRECONDITIONS.md` to pick the target `N`.

## 2) Multi-agent preflight (every turn)

- Run `git status --porcelain` and note unexpected changes.
- Scan the last 10 phases: `ls -dt docs/planning/phase-* | head -10`.
- If you will touch files that appear in other active/recent phases:
  - Read the other phase’s `plan.md` for intent.
  - Plan to merge semantically and document coordination in Output.

## 3) Load plans and find the active subphase

- Read:
  - `docs/planning/phase-N/plan.md`
  - Every `docs/planning/phase-N/<letter>/plan.md`
- Determine completion:
  - A subphase is complete if **Output** and **Handoff** are both non-empty.
- The active subphase is the first incomplete letter in the root Subphase Index.

## 4) Execute work (single-turn budget)

- Re-read each target file before modifying (do not rely on cached content).
- Implement only the active subphase scope.
- If a blocker arises:
  - Log it in the active subphase plan (Blockers section or Progress This Turn).
  - Continue with other unblocked items that still belong to the active subphase.

## 5) Write progress to disk (mandatory)

- Update the active subphase `docs/planning/phase-N/<letter>/plan.md`:
  - Add/patch Validation steps (if missing).
  - Append “Progress This Turn (Terminus Maximus)” using the template in `05_TEMPLATES.md`.
  - If the subphase is complete: fill Output + Handoff with specifics.
- Update the root plan `docs/planning/phase-N/plan.md`:
  - Check off success criteria where met.
  - Append a “Phase Summary (running)” line item (template in `05_TEMPLATES.md`).

## 6) RED TEAM wrap-up (every turn, mandatory)

- Run `$phase-gaps` on the same phase:
  - Repo reality check for any newly referenced files/symbols.
  - Tighten plan docs and add Open Questions where needed.
- Ensure the user-facing response includes:
  - On-disk changes (files touched)
  - Assumptions (≥ 84.7% confidence)
  - Questions (< 84.7% confidence) with why-it-matters + current default

## 7) Completion path

- If all subphases are complete and root success criteria are met:
  - Run `$phase-review` for the same phase and write `docs/planning/phase-N/review.md`.
- If review fails due to env/access:
  - Document the exact missing prerequisite and the next command the user should run.
