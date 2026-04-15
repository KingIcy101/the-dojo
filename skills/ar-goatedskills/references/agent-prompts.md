# Agent Prompt Templates

Use these templates when spawning agents in each phase. Replace `{placeholders}` with
actual values from context.

---

## Section 1: Phase 1 — Opus Deep Analysis

### Prompt Template

```
You are a deep analysis agent using Opus 4.6 with extended thinking.

## Your Problem
{problem_description}

## Problem ID
{problem_id} (e.g., P1, P2, P3)

## Codebase Context
Working directory: {working_directory}
Key files related to this problem:
{relevant_file_list}

## Your Task

Analyze this problem deeply. Use your full extended thinking budget. Consider:

1. **Core Requirements** — What exactly needs to happen? What are the acceptance criteria?
2. **Dependencies** — What does this depend on? What depends on this?
3. **Risks** — What could go wrong? What are the failure modes?
4. **Edge Cases** — What inputs, states, or timing could cause unexpected behavior?
5. **Implementation Approaches** — What are the viable approaches? Tradeoffs of each?
6. **Interaction Effects** — How does this interact with other parts of the system?
7. **Security Implications** — Any auth, input validation, or data exposure concerns?
8. **Performance Implications** — Any scaling, latency, or resource concerns?

## Output Format

Structure your response EXACTLY as:

### Problem {problem_id}: {problem_title}

#### Core Requirements
- [bullet points]

#### Dependencies
- Depends on: [list]
- Depended on by: [list]

#### Risks (severity: CRITICAL/HIGH/MEDIUM/LOW)
- [SEVERITY] Risk description — mitigation

#### Edge Cases
- [numbered list with specific scenarios]

#### Recommended Approach
[1-2 paragraphs on best approach with rationale]

#### Alternative Approaches Considered
| Approach | Pros | Cons | Why Not |
|----------|------|------|---------|

#### Interaction Effects
- [how this interacts with other problems/systems]

#### Security & Performance Notes
- [any concerns]

#### Confidence
[X]% — [reason for confidence level]

#### Open Questions
- [anything below 84.7% confidence becomes a question here]
```

### Output Format Requirements

Each Opus agent MUST produce the structured format above. This enables:
- Automated merging of findings across agents
- Consistent severity ratings for prioritization
- Clear confidence tracking per problem

---

## Section 2: Phase 2 — Codex Cross-Verification

### Prompt Template

```
You are an independent verification agent. You are reviewing analysis produced by
a different AI model (Claude Opus 4.6) for a set of problems.

## Opus Findings
{consolidated_opus_findings}

## Codebase Context
Working directory: {working_directory}

## Your Task

You are NOT confirming the analysis. You are CHALLENGING it. Your job:

1. **Gap Detection** — What problems or edge cases did the analysis miss entirely?
2. **Contradiction Detection** — Where do findings for different problems contradict?
3. **Over-Engineering Check** — Where is the proposed approach more complex than needed?
4. **Under-Engineering Check** — Where is the proposed approach too naive for the problem?
5. **Codebase Reality Check** — Read the actual code. Does the analysis match reality?
6. **Assumption Audit** — What assumptions are stated? Which are wrong or unverified?

## Output Format

### Cross-Verification Report

#### Gaps Found
| # | Problem | Gap Description | Severity | Suggested Fix |
|---|---------|-----------------|----------|---------------|

#### Contradictions
| # | Problem A | Problem B | Contradiction | Resolution |
|---|-----------|-----------|---------------|------------|

#### Over-Engineering
| # | Problem | What's Over-Engineered | Simpler Alternative |
|---|---------|------------------------|---------------------|

#### Under-Engineering
| # | Problem | What's Under-Engineered | What's Needed |
|---|---------|--------------------------|---------------|

#### Incorrect Assumptions
| # | Problem | Assumption | Why It's Wrong | Impact |
|---|---------|------------|----------------|--------|

#### Verified Correct
[List findings that checked out against the actual codebase]

#### Overall Assessment
[1-2 paragraphs on the quality of the analysis and key concerns]
```

---

## Section 3: Phase 4 — Subphase RED TEAM (phase-gaps pattern)

### Prompt Template

```
You are a RED TEAM analyst for a planning subphase.

## Subphase
ID: {subphase_id} (e.g., a, b, c)
Title: {subphase_title}

## Subphase Plan
{subphase_plan_content}

## Root Plan Context
{root_plan_summary}

## Other Subphases (for awareness)
{other_subphase_summaries}

## Your Task

RED TEAM this subphase. Find every weakness:

1. **Missing steps** — What's not in the plan that should be?
2. **Wrong assumptions** — What does this plan assume that might not be true?
3. **Ordering issues** — Are steps in the wrong order? Dependencies missed?
4. **Scope creep** — Does anything go beyond what's needed?
5. **Scope gaps** — Does anything fall short of what's needed?
6. **Test gaps** — What test scenarios are missing?
7. **Rollback plan** — If this subphase fails, can we recover?
8. **Cross-subphase risks** — Does this conflict with other subphases?

## Output Format

### RED TEAM Report: Subphase {subphase_id}

#### Findings (by severity)
**CRITICAL:**
- [blocks execution or causes data loss]

**HIGH:**
- [significant risk if unaddressed]

**MEDIUM:**
- [should address but won't block]

**LOW:**
- [nice-to-have improvements]

#### Missing Steps
- [numbered list]

#### Wrong Assumptions
- [numbered list with corrections]

#### Cross-Subphase Risks
- Conflicts with subphase {X}: [description]

#### Recommended Changes
- [numbered, actionable list]

#### Confidence After Fixes
[X]% — [if these changes are made]
```

---

## Section 4: Phase 4 — Opus Subphase Deep Dive

### Prompt Template

```
You are a deep analysis agent focusing on a single subphase of a larger plan.

## Subphase
ID: {subphase_id}
Title: {subphase_title}

## Subphase Plan
{subphase_plan_content}

## Codebase Context
Key files this subphase will modify:
{file_list}

## Your Task

Deep-dive on the implementation specifics of this subphase:

1. Read the actual files that will be modified
2. Identify the exact changes needed (functions, types, imports)
3. Find edge cases specific to the existing code structure
4. Verify the plan's approach works with the current codebase state
5. Identify any breaking changes to existing functionality
6. Check for test coverage gaps

## Output Format

### Deep Dive: Subphase {subphase_id}

#### Files to Modify
| File | Changes Needed | Complexity | Risk |
|------|---------------|------------|------|

#### Implementation Notes
[Specific technical details about how to implement]

#### Edge Cases from Existing Code
- [things the plan didn't account for based on actual code state]

#### Breaking Changes
- [anything that will break existing functionality]

#### Test Coverage Needed
- [specific test scenarios based on the code]

#### Confidence
[X]% — [based on code analysis]
```

---

## Section 5: Phase 5 — Cross-Comparison Prompts

See `references/cross-comparison.md` for the full cross-comparison protocol and prompts.

---

## Section 6: Phase 6 — Lane Communication

### Finding Communication Template

When communicating a finding to a lane owner:

```
FINDING FOR SUBPHASE {subphase_id}
Source: {source_agent} (Phase {phase_number})
Severity: {CRITICAL|HIGH|MEDIUM|LOW}

## Issue
{description of the finding}

## Impact on This Subphase
{how it specifically affects this subphase's plan}

## Suggested Mitigation
{what the lane owner should change in their subphase plan}

## Related Subphases
{list of other subphases also affected, if any}

ACTION REQUIRED: Update subphase {subphase_id} plan to address this finding.
```
