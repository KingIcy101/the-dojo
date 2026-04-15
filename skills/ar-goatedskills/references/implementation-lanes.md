# Implementation Lanes

The core differentiator of Deep Build. How parallel implementation with cross-model
verification works at the subphase level.

---

## Lane Architecture

Each subphase gets its own **named implementation lane**:

```
Subphase A (independent)     Subphase B (independent)     Subphase C (depends on A)
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│  impl-a (Opus)       │    │  impl-b (Opus)       │    │  (waits for A)       │
│  ↓ implements        │    │  ↓ implements        │    │  impl-c (Opus)       │
│  ↓ commits           │    │  ↓ commits           │    │  ↓ implements        │
│  codex-verify-a      │    │  codex-verify-b      │    │  ↓ commits           │
│  ↓ reviews diff      │    │  ↓ reviews diff      │    │  codex-verify-c      │
│  ↓ findings → fix    │    │  ↓ findings → fix    │    │  ↓ reviews diff      │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘
         │                           │                           │
         └──────────┬────────────────┘                           │
                    ↓                                            │
            cross-monitor                                        │
            (after every 2nd                                     │
             subphase completes)                                 │
                    │                                            │
                    └────────────────────────────────────────────┘
```

## Spawning the Implementation Agent

Each Opus implementation agent follows the terminus-maximus pattern:

```
Agent(
  name: "impl-{sub}",
  model: "opus",
  subagent_type: "general-purpose",
  prompt: "
    You are implementing subphase {sub} of phase {N}.

    ## Context
    Working directory: {working_directory}
    Phase plan: docs/planning/phase-{N}/plan.md
    Subphase plan: docs/planning/phase-{N}/{sub}/plan.md

    ## Your Task
    1. Read the subphase plan thoroughly
    2. Read all files you'll modify (current state, not cached)
    3. Implement the changes described in the plan
    4. Run lint and build after changes
    5. Write tests for new functionality
    6. Update the subphase plan with Output and Handoff sections

    ## Rules
    - Follow $karpathy-guidelines: minimal changes, explicit assumptions
    - Re-read files before modifying (don't rely on cached content)
    - Run $skill-oracle if you need capabilities you don't have
    - Check git status before and after your changes
    - Only modify files in scope for this subphase
    - If blocked, document why in the subphase plan and STOP

    ## Output
    When done, report:
    - Files modified (list)
    - Tests written (list)
    - Lint/build status
    - Any concerns or open questions
  "
)
```

## Codex Diff Verification

After each implementation agent completes and commits:

```bash
# Get the diff for this subphase's work — write to file, don't pipe via stdin
git diff HEAD~{N_commits}..HEAD > /tmp/deep-build-diff-{sub}.patch

# Run Codex verification — reads diff from disk in read-only sandbox
codex exec --model gpt-5.4 \
  -c model_reasoning_effort=high \
  --sandbox read-only \
  --skip-git-repo-check \
  "Read /tmp/deep-build-diff-{sub}.patch. You are reviewing a code diff produced by another AI model implementing subphase '{sub}'.

   Find:
   1. Bugs — logic errors, off-by-ones, null/undefined risks
   2. Edge cases — unhandled inputs, race conditions, boundary values
   3. Security — injection, XSS, auth bypass, secrets exposure
   4. Type safety — incorrect types, unsafe casts, missing validation
   5. API contracts — does the implementation match the plan?
   6. Test gaps — what scenarios aren't tested?

   For each finding: severity (CRITICAL/HIGH/MEDIUM/LOW), file:line, description, fix.
   If no issues found, say VERIFIED CLEAN.
  " 2>/dev/null
```

## Cross-Subphase Monitor

Runs after every 2nd subphase completes (or after all complete):

```
Agent(
  name: "cross-monitor",
  model: "opus",
  subagent_type: "general-purpose",
  prompt: "
    You are monitoring parallel implementation lanes for conflicts.

    ## Completed Subphases
    {list of completed subphases with their diffs}

    ## Check For
    1. File conflicts — did two subphases modify the same file incompatibly?
    2. Type conflicts — did one subphase change a type another depends on?
    3. Import conflicts — circular dependencies introduced?
    4. Test conflicts — do tests from different subphases interfere?
    5. Migration conflicts — database migration ordering issues?
    6. API contract breaks — did one subphase break another's assumptions?

    ## Output
    For each conflict: affected subphases, severity, description, resolution.
    If no conflicts: LANES CLEAR.
  "
)
```

## Dependency Ordering

Before launching lanes, analyze subphase dependencies:

```
IF all subphases are independent:
  → Launch ALL lanes in a single message (maximum parallelism)

IF some subphases have dependencies:
  → Build dependency graph
  → Launch Tier 1 (no dependencies) in parallel
  → After Tier 1 completes + Codex verifies: launch Tier 2
  → Continue until all tiers complete

IF circular dependency found:
  → STOP. This is a plan structure problem.
  → Either merge the coupled subphases or extract shared dependency.
  → Update plan before proceeding.
```

## Handling Codex Findings

```
FOR EACH Codex finding:
├── CRITICAL?
│   └── MUST fix before proceeding to next gear
│       ├── impl-{sub} agent still running? → SendMessage with fix request
│       └── Agent done? → Spawn fix agent for that subphase
├── HIGH?
│   └── Fix before next gear (batch fixes after all subphases)
├── MEDIUM?
│   └── Fix if easy, otherwise note in plan for follow-up
└── LOW?
    └── Note in plan, don't block
```

## Maximum Concurrency

The theoretical maximum parallelism for a 5-subphase plan:
- 5 Opus implementation agents (1 per subphase)
- 5 Codex verification calls (1 per subphase, after impl completes)
- 2-3 cross-monitor checks
- Total: ~12-13 agent invocations

Practical limit: Agent tool handles up to ~8 parallel agents well.
For 8+ subphases, batch into groups of 5-6.
