# Edge Cases

## Missing planning directory

If `docs/planning/` does not exist, create it, then proceed.

## Non-standard folders

Ignore anything not matching `phase-<number>`.

## Gaps in numbering

If phase-1 and phase-3 exist (gap at 2), still pick `max + 1` (phase-4).

## Ambiguous subtasks

Derive the smallest reasonable set from the conversation. Prefer fewer, clearer subphases over many vague ones.

## User wants no files

If the user asks for planning but explicitly wants no files written, do not run this skill. Produce an in-chat plan instead.

## Examples

### Existing phases

If `docs/planning/phase-29/` exists, create:

- `docs/planning/phase-30/`
- `docs/planning/phase-30/plan.md`
- `docs/planning/phase-30/a/plan.md`, `b/plan.md`, ...

### No phases yet

If `docs/planning/` exists but contains no `phase-*` directories, create:

- `docs/planning/phase-1/` and scaffolds
