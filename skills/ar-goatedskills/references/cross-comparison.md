# Cross-Comparison Protocol

The cross-comparison pair is the unique differentiator of Deep Sweep. While phase-gaps
analyzes subphases individually, the cross-comparison pair looks at ALL subphases
together to find **interaction effects** — things that pass every individual check
but fail when combined.

---

## Why This Matters

The #1 cause of production failures in multi-component changes is **emergent behavior** —
each piece works correctly in isolation, but the combination produces unexpected results.

Examples:
- Subphase A adds a database index. Subphase B adds a query that defeats the index.
- Subphase A assumes API returns are cached. Subphase B invalidates that cache.
- Subphase A modifies a shared type. Subphase B reads the old type shape.
- Subphase A and B both add migrations — ordering conflict.

---

## Cross-Comparison Opus Agent Prompt

```
You are a cross-subphase interaction analyst. Your ONLY job is to find things that
look fine in isolation but break when combined.

## All Subphase Plans
{all_subphase_plans_concatenated}

## Phase 4 Analysis Results
{all_phase_4_findings_per_subphase}

## Root Plan
{root_plan_content}

## Your Analysis Framework

For every PAIR of subphases (A,B), (A,C), (B,C), ..., analyze:

### 1. File Conflicts
Do any two subphases modify the same file? If yes:
- Will the modifications conflict?
- What's the merge order?
- Does one subphase's change invalidate another's?

### 2. Type/Interface Conflicts
Does one subphase change a type/interface that another reads?
- Type narrowing that breaks consumers
- New required fields that aren't populated by other subphases
- Enum additions that aren't handled in switch/match

### 3. Data Flow Conflicts
Does data flow from one subphase's domain to another's?
- Schema changes that break downstream consumers
- API contract changes without version negotiation
- Event/message format changes

### 4. Resource Conflicts
Do subphases compete for shared resources?
- Database connections, locks, or tables
- External API rate limits
- File system paths

### 5. Timing/Ordering Conflicts
Does execution order matter?
- Migration ordering
- Feature flag dependencies
- Cache invalidation timing

### 6. Assumption Conflicts
Does subphase A assume X while subphase B assumes NOT X?
- "This endpoint is authenticated" vs "This endpoint is public"
- "This table exists" vs "This table hasn't been created yet"
- "This feature flag is on" vs "This feature flag is off"

### 7. Boundary Gaps
Are there problems that fall BETWEEN subphase boundaries?
- Responsibility gaps (neither subphase handles it)
- Error propagation paths that cross boundaries
- Logging/monitoring gaps at boundaries

## Output Format

### Cross-Comparison Report

#### Interaction Matrix
| Subphase A | Subphase B | Interaction Type | Severity | Description |
|------------|------------|------------------|----------|-------------|

#### File Conflicts
- [list with specific files and conflicting changes]

#### Type/Interface Conflicts
- [list with specific types and breaking changes]

#### Data Flow Conflicts
- [list with data paths affected]

#### Assumption Conflicts
- [list with contradicting assumptions]

#### Boundary Gaps
- [list with unowned responsibilities]

#### Recommended Ordering
If subphases have dependencies, recommend execution order:
1. {subphase_id} — because {reason}
2. {subphase_id} — because {reason}
...

#### Cross-Cutting Concerns
Issues that affect ALL subphases:
- [list items that should go in root plan's Cross-Cutting Concerns section]

#### Overall Risk Assessment
[1-2 paragraphs on the combined risk profile and recommendation]
```

---

## Cross-Comparison Codex Agent Prompt

```
You are verifying a multi-subphase implementation plan against an actual codebase.
Focus on what the other analysis might have missed.

## All Subphase Plans
{all_subphase_plans}

## Phase 4 Findings
{phase_4_findings}

## Your Task

Read the actual codebase and verify:

1. Can these subphases actually be implemented in the planned order?
2. Are there hidden dependencies the plans don't account for?
3. Do the plans reference files/functions/types that actually exist?
4. Are there existing tests that will break from these combined changes?
5. Are there CI/CD pipeline considerations (build order, deploy order)?
6. What edge cases exist in the ACTUAL CODE that the plans missed?

## Output Format

### Codebase Verification Report

#### Implementation Feasibility
| Subphase | Feasible? | Blockers |
|----------|-----------|----------|

#### Hidden Dependencies Found
- [specific code-level dependencies not in the plans]

#### Phantom References (planned but don't exist)
- [files, functions, types referenced in plans but not in codebase]

#### Tests That Will Break
- [specific test files and what breaks them]

#### Edge Cases from Code
- [code-specific edge cases not covered by any subphase]

#### Recommended Changes
- [numbered, actionable list]
```

---

## Interpreting Cross-Comparison Results

### Severity Classification

| Finding Type | Default Severity | Escalation Condition |
|-------------|-----------------|---------------------|
| File conflict (same file, compatible changes) | MEDIUM | → HIGH if merge is non-trivial |
| File conflict (same file, incompatible changes) | HIGH | → CRITICAL if data loss possible |
| Type/interface conflict | HIGH | Always HIGH or CRITICAL |
| Data flow conflict | HIGH | → CRITICAL if affects production data |
| Assumption conflict | CRITICAL | Always CRITICAL |
| Boundary gap | MEDIUM | → HIGH if security-related |
| Ordering dependency | MEDIUM | → HIGH if irreversible operations |

### Communication Rules

- **CRITICAL findings** → Communicate to ALL affected lane owners + root plan
- **HIGH findings** → Communicate to primary affected lane owner + root plan
- **MEDIUM findings** → Record in root plan, communicate if it changes approach
- **LOW findings** → Record in root plan only
