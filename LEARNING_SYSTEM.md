# Alo's Self-Learning Loop System

A sophisticated feedback system that ensures Alo learns from corrections automatically, rather than requiring Matt to repeat himself.

---

## Overview

The learning system has four layers:

1. **Correction Detection** — Auto-capture when Matt corrects Alo
2. **Pattern Recognition** — Identify repeated mistakes (3+ times = critical)
3. **Learning Enforcement** — Force Alo to check past lessons before similar tasks
4. **Effectiveness Tracking** — Measure if Alo is actually improving

This is NOT optional. It's mandatory enforcement that blocks task start if corrections aren't reviewed.

---

## System Architecture

### Layer 1: Correction Detection (`correction-detector.js`)

**What it does:**
- Runs every 5 minutes
- Watches for correction signals in Matt's messages ("wrong", "not right", "fix that", etc.)
- Auto-extracts rules from corrections using Haiku
- Saves to `memory/corrections.md`

**Signals it detects:**
```
wrong, not right, incorrect, no alo, that's wrong, you forgot,
you missed, not what i, that's not, fix that, you're wrong,
not quite, you got it wrong, you don't remember, you lost
```

**Output example:**
```
- [2026-03-05 14:22] RULE: Notifications — ALWAYS notify when builds complete | Context: "you finished that but didn't tell me"
- [2026-03-05 14:23] RULE: Testing — verify fixes on live URL before saying done | Context: "you said done but it's still broken"
```

---

### Layer 2: Repeat Mistake Detection (`repeat-mistake-detector.js`)

**What it does:**
- Runs every 5 minutes (integrated into fast cycle)
- Counts corrections by category from `corrections.md`
- Flags critical patterns when 3+ corrections exist in same category
- Tracks escalation: is the pattern getting worse or improving?
- Saves to `memory/repeat-patterns.md`

**Critical threshold:** 3+ corrections in same category
- Status changes to `⚠️ Critical` and blocks further work in that area
- Logs to daily notes with escalation warnings
- Tracks if pattern is improving (corrections stopped) or worsening (count increased)

**Example:**
```
## Build & Shipping Rules (4 occurrences)
- First seen: 2026-03-01
- Detected: 2026-03-05 14:30
- Status: ⚠️ Critical pattern requiring Alo focus
- Trend: Worsening (was 2, now 4)
```

---

### Layer 3: Pre-Task Enforcement (`pre-task-checker.js`)

**What it does:**
- **MANDATORY** check before starting similar tasks
- Searches `corrections.md` for rules relevant to the task
- If relevant corrections exist: blocks task and requires acknowledgment
- If no relevant corrections: allows task to proceed

**How it works:**

```bash
# Check corrections before starting a task
node pre-task-checker.js "build a dashboard UI"

# Output options:
# Option 1: No corrections apply → proceed freely
# ✅ PRE-TASK CHECK: No past corrections apply to this task.

# Option 2: Corrections apply → BLOCKED
# 🔴 TASK BLOCKED: Corrections must be reviewed before proceeding.
# ⚠️  [list of relevant corrections]
# To proceed: node pre-task-checker.js --ack "build a dashboard UI"

# Option 3: Already acknowledged today → proceed
# ✅ PRE-TASK CHECK: Corrections already reviewed today. Proceed.

# Option 4: Force bypass (emergency only)
# node pre-task-checker.js --force "build a dashboard UI"
# ⏭️  FORCED BYPASS: --force used. Proceeding without enforcement.
```

**Enforcement model:**

1. Check for relevant corrections
2. If none: ✅ proceed
3. If yes and not acknowledged today: 🔴 **BLOCK** and require `--ack` flag
4. If already acknowledged: ✅ proceed
5. If `--force`: proceed but log the bypass (Alo takes responsibility)

**Integration into Alo's workflow:**

Before ANY task, Alo should run:
```bash
node /Users/mattbender/.openclaw/workspace/memory-stack/pre-task-checker.js "task description"
```

If blocked, acknowledge and retry:
```bash
node /Users/mattbender/.openclaw/workspace/memory-stack/pre-task-checker.js --ack "task description"
```

---

### Layer 4: Learning Effectiveness Tracking (`learning-effectiveness-tracker.js`)

**What it does:**
- Runs every 2 hours in the slow cycle
- Counts corrections this week vs. last week
- Calculates trend: improving, stable, or worsening
- Saves weekly reports to `memory/learning-effectiveness.md`

**Key metrics:**
- Corrections per week
- Week-over-week trend (percentage change)
- Status: Strong improvement / Improving / Stable / More mistakes

**Example report:**
```
## Learning Effectiveness Report — 2026-03-05 14:30

### Weekly Comparison
- This week: 3 corrections
- Last week: 8 corrections
- Trend: -62% → 📉 Improving

### Key Metrics
- Total corrections logged: 47
- Corrections/day (this week): 0.4
- Status: ✅ Strong improvement
```

**Interpretation:**
- **Trend < -15%** → Alo is learning well, improvements happening
- **Trend > 15%** → Alo is making more mistakes, enforcement needed
- **Trend -15% to +15%** → Stable, baseline maintained

---

## The Complete Flow

### 1. Matt corrects Alo

```
Matt: "You said done but didn't verify on the live URL"
```

### 2. Correction detector auto-captures (5 min cycle)

```
correction-detector.js runs:
- Detects "done" + "didn't verify" signals
- Extracts rule via Haiku: "RULE: Verification — test on live URL before saying done"
- Saves to corrections.md
```

### 3. Repeat pattern detector checks (5 min cycle)

```
repeat-mistake-detector.js runs:
- Counts "Verification" rules in corrections.md
- If 3+ occurrences: flags as critical pattern
- Saves to repeat-patterns.md with escalation status
- Logs warning to daily notes
```

### 4. Next similar task starts

```
Alo: "I'll build the new dashboard"
Alo runs: node pre-task-checker.js "build a dashboard UI"

pre-task-checker responds:
- Finds "Verification" rule is relevant to "build dashboard"
- Checks if already acknowledged today
- If not acknowledged: BLOCKS task, requires --ack flag
- Alo must acknowledge before proceeding
```

### 5. Alo acknowledges and proceeds

```
Alo: node pre-task-checker.js --ack "build a dashboard UI"
✅ Corrections acknowledged. You may proceed.

[Alo now builds dashboard WITH the verification rule in mind]
```

### 6. Weekly learning report (2 hour cycle)

```
learning-effectiveness-tracker.js runs:
- Counts corrections this week vs. last week
- Generates trend report
- Shows improvement, stability, or worsening
- Logs to learning-effectiveness.md
```

---

## Memory Files Generated

### `corrections.md`
- All corrections and extracted rules
- Format: `RULE: [Category] — [actionable rule]`
- Auto-updated by correction-detector and learning-engine

### `repeat-patterns.md`
- Critical patterns (3+ occurrences)
- Escalation tracking
- Status (improving vs worsening)
- Auto-updated by repeat-mistake-detector

### `correction-acknowledgments.md`
- Records when Alo acknowledges corrections before tasks
- Used to avoid redundant enforcement

### `learning-effectiveness.md`
- Weekly trend reports
- Metrics and interpretation
- Auto-updated every 2 hours

### `instant-feedback.md`
- High-priority real-time corrections (matt sends just "❌" or "wrong")
- Lower-latency than detection cycle
- Weighted 4x in pattern analysis

---

## Integration with AGENTS.md

The pre-task checker is now **mandatory** before any task. In AGENTS.md:

```markdown
### Before Any Task (MANDATORY Pre-Check)

Before starting ANY task, run:
node /Users/mattbender/.openclaw/workspace/memory-stack/pre-task-checker.js "task description"

If corrections apply and aren't acknowledged: TASK IS BLOCKED.
If blocked, acknowledge: node pre-task-checker.js --ack "task description"
```

---

## Example Scenario

**Scenario:** Alo has made 4 build verification mistakes over 2 weeks.

**Timeline:**

1. **Correction 1 (Day 1):** Matt: "You said done but didn't test it"
   - detector captures → `RULE: Verification — test on live URL before saying done`
   - count: 1

2. **Correction 2 (Day 3):** Matt: "Again, not tested"
   - detector captures → same rule category
   - count: 2

3. **Correction 3 (Day 5):** Matt: "Still not verifying!"
   - detector captures → same rule category
   - count: 3
   - **CRITICAL PATTERN TRIGGERED** ⚠️
   - repeat-mistake-detector escalates pattern to critical
   - logs to repeat-patterns.md

4. **Alo starts new task (Day 6):**
   ```
   node pre-task-checker.js "build new dashboard"
   
   🚨 PRE-TASK CHECK: CORRECTIONS APPLY TO THIS TASK
   
   Task: "build new dashboard"
   
   📋 RELEVANT PAST CORRECTIONS:
   ⚠️ RULE: Verification — test on live URL before saying done
   ⚠️ RULE: Testing — verify fixes on live URL before saying done
   
   🔴 TASK BLOCKED: Corrections must be reviewed before proceeding.
   ```

5. **Alo acknowledges:**
   ```
   node pre-task-checker.js --ack "build new dashboard"
   ✅ Corrections acknowledged. You may proceed.
   ```

6. **Alo builds WITH the rule in mind** (and actually tests this time)

7. **Day 7:** learning-effectiveness-tracker runs
   - This week: 1 correction (low!)
   - Last week: 4 corrections
   - Trend: -75% → 📉 Improving
   - Status: ✅ Strong improvement

---

## What This Solves

**Old problem:** Alo stores corrections but doesn't apply them. Matt has to repeat the same corrections multiple times.

**New solution:**
- ✅ Corrections are auto-captured immediately
- ✅ Repeated mistakes are flagged as critical patterns
- ✅ Alo is **forced** to review corrections before similar tasks
- ✅ Learning is **measured** — we can see if corrections are working
- ✅ Matt doesn't have to repeat himself

---

## Commands Reference

### Check corrections before a task
```bash
node memory-stack/pre-task-checker.js "task description"
```

### Acknowledge corrections and proceed
```bash
node memory-stack/pre-task-checker.js --ack "task description"
```

### Force bypass (emergency, logs for accountability)
```bash
node memory-stack/pre-task-checker.js --force "task description"
```

### View all captured corrections
```bash
cat memory/corrections.md
```

### View critical repeated patterns
```bash
cat memory/repeat-patterns.md
```

### View learning effectiveness trends
```bash
cat memory/learning-effectiveness.md
```

### Manually log instant feedback
```bash
node memory-stack/learning-engine.js --instant "what alo did" "matt's feedback"
```

### Run weekly pattern scan
```bash
node memory-stack/learning-engine.js --scan
```

---

## Notes for Alo

- Pre-task checker is **not optional** — use it every time
- If blocked, read the corrections, acknowledge them, then integrate them into your work
- If you use `--force`, you're taking responsibility for repeating mistakes
- The system is learning how to help you learn — embrace it

---

**Updated:** 2026-03-05
**Status:** Production-ready, integrated into memory-stack runner
