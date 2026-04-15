# Multi-Agent Coordination

When multiple agents work concurrently on the same codebase, conflicts and dependencies can arise. This reference provides procedures to detect and handle these situations.

## When to Apply

Apply multi-agent coordination checks whenever:

- You encounter unexpected file contents (file differs from what you read earlier)
- A file you need to modify has recent uncommitted changes
- You see merge conflict markers in files
- Work seems to overlap with another phase's scope
- You hit build/lint errors that appear unrelated to your changes

## Conflict Detection Procedure

### Step 1 — Scan Recent Phases

Before starting implementation work, scan the last 10 phases for potential overlaps:

```bash
# List last 10 phases by modification time
ls -dt docs/planning/phase-* | head -10
```

For each recent phase, check its `plan.md` for:

1. **Purpose** — Does it touch similar domain areas?
2. **Subphase Index** — Do any subphases mention files you plan to modify?
3. **Phase Summary** (if exists) — What files/artifacts were produced?

### Step 2 — Check Git Status for Uncommitted Changes

```bash
# See files with uncommitted modifications
git status --porcelain

# See which files have been modified recently (last 24 hours)
git diff --stat HEAD~10..HEAD
```

If files you need to modify appear in uncommitted changes:

1. Read the current file content (it may have changed since your last read)
2. Check `docs/planning/phase-*` directories to identify which phase made the changes
3. Align your implementation with those changes

### Step 3 — Check for Active Concurrent Work

Look for signals that another agent is actively working:

1. **Partially completed plan.md files** — Output/Handoff sections empty
2. **Recent file modifications** — `git log -1 --format="%ar" -- <filepath>` shows "seconds ago" or "minutes ago"
3. **Build failures** — May indicate incomplete work from another agent

## Conflict Resolution Strategies

### File-Level Conflicts

When you need to modify a file that another phase has changed:

1. **Read the current file state** — Your cached version may be stale
2. **Identify the other phase** — Check `git log --oneline -5 -- <filepath>` or scan recent phase plans
3. **Understand their changes** — Read the other phase's plan.md to understand intent
4. **Merge semantically** — Don't just resolve git conflicts; ensure the combined behavior is correct
5. **Document the merge** — Note in your Output section which phase's changes you integrated

### Dependency Conflicts

When your work depends on another phase's incomplete work:

1. **Wait or work around** — If the dependency is critical, wait for the other phase to complete
2. **Create interface contracts** — Define the expected interface and implement against it
3. **Add a dependency note** — Document in your plan.md that you depend on Phase N's completion
4. **Consider reordering** — If possible, do independent work first while waiting

### Semantic Conflicts

When multiple phases affect the same behavior (even in different files):

1. **Trace the data flow** — Identify how changes interact
2. **Test the combined behavior** — Don't assume changes are independent
3. **Coordinate through documentation** — Update your plan.md to note the interaction

## Standard Checks

Include these checks in your workflow:

### Before Starting a Subphase

```markdown
## Pre-Flight Conflict Check

- [ ] Ran `git status` — no unexpected modifications to files I'll touch
- [ ] Scanned last 10 phases — no overlap with my target files
- [ ] Read current state of files I'll modify (not relying on cached content)
```

### When You Encounter an Unexpected State

```markdown
## Conflict Resolution Log

**Issue:** <describe what was unexpected>
**Cause:** <Phase N modified file X for reason Y>
**Resolution:** <how you handled it>
**Files affected:** <list of files>
```

### After Completing Work

```markdown
## Coordination Notes

**Files modified:** <list of files you changed>
**Potential conflicts with:** <list any phases working on related areas>
**Integration notes:** <any special handling needed when merging>
```

## Quick Reference: Common Scenarios

| Scenario | Detection | Resolution |
|----------|-----------|------------|
| File I need has new content | Read file, compare to expectation | Re-read, understand changes, merge |
| Build fails unexpectedly | Check git status + recent commits | Identify source, coordinate or wait |
| Schema changes from another phase | Prisma generate fails | Run `npm run db:push`, align with new schema |
| API contract changed | TypeScript errors on imports | Check recent phases, update usage |
| Test failures on unrelated code | Tests reference shared fixtures | Coordinate fixture changes |

## Communication Pattern

When you detect a conflict, document it clearly:

```markdown
### Conflict Detected

**Phase:** 36 (Booking Process)
**Conflict Type:** File overlap
**File:** lib/ai-drafts.ts
**Their changes:** Added booking process instruction injection
**My planned changes:** Modify draft generation for X
**Resolution approach:** Read their changes first, build on top of them
```

This creates a paper trail for debugging integration issues later.
