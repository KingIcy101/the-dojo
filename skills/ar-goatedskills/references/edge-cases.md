# Edge Cases and Recovery

Known failure modes for Deep Sweep and how to handle them.

---

## Codex Unavailable

**Symptom:** `codex` CLI not found or MCP tool fails.

**Recovery:**
1. Check: `which codex` — CLI is the ONLY supported method (no MCP fallback)
2. If CLI not found: inform user, offer **degraded mode**
3. Degraded mode: replace Codex passes with a second Opus agent using a
   "devil's advocate" system prompt — still cross-verification, just not cross-model
4. Note in plan: "Cross-verification was Opus-only (Codex unavailable)"
5. **Never pipe large content via stdin** — let Codex read from disk in `--sandbox read-only`

---

## Too Many Problems (Context Overflow)

**Symptom:** Problem set exceeds what can be analyzed in parallel.

**Threshold:** More than 8 problems.

**Recovery:**
1. Group related problems into clusters (max 8 clusters)
2. Run Deep Sweep on each cluster
3. Run a final cross-cluster comparison pass
4. Document clustering rationale in root plan

---

## Agent Timeout

**Symptom:** An Opus or Codex agent doesn't return within expected time.

**Recovery:**
1. Wait up to 10 minutes for Opus agents (extended thinking is slow)
2. Wait up to 5 minutes for Codex agents
3. If timeout: note the missing analysis, proceed with available results
4. Mark affected subphase with lower confidence rating
5. Consider re-running the timed-out agent after other phases complete

---

## Conflicting Cross-Comparison Findings

**Symptom:** Opus cross-comparison says X is fine, Codex says X is broken (or vice versa).

**Recovery:**
1. Default to the MORE CONSERVATIVE finding (assume it's broken)
2. Spawn a TIE-BREAKER agent:
   - New Opus agent that sees BOTH cross-comparison reports
   - Task: resolve the disagreement with evidence from the codebase
3. If tie-breaker can't resolve: escalate to user as Open Question
4. Document the disagreement in root plan's Risk Register

---

## Subphase Plan Too Thin

**Symptom:** A subphase scaffold has insufficient detail for meaningful analysis.

**Recovery:**
1. Before Phase 4, check each subphase plan for minimum content:
   - Scope defined
   - At least one acceptance criterion
   - At least one file path referenced
2. If too thin: use Opus agent to expand the subphase plan BEFORE analysis
3. If still too thin: merge with adjacent subphase or ask user for clarification

---

## Lane Owner Agent Already Completed

**Symptom:** Phase 6 needs to communicate a finding to `gaps-{sub}`, but that agent
has already completed and returned its result.

**Recovery:**
1. Cannot SendMessage to a completed agent
2. Instead: spawn a NEW agent specifically to update the subphase plan file
3. New agent reads current plan.md, incorporates finding, writes updated plan.md
4. Name: `lane-update-{sub}-{finding-number}`

---

## Circular Dependencies Between Subphases

**Symptom:** Cross-comparison reveals A depends on B AND B depends on A.

**Recovery:**
1. STOP — this is a plan structure problem, not an implementation problem
2. Options:
   a. Merge the two subphases into one (if small enough)
   b. Extract the shared dependency into its own subphase (a "foundation" subphase)
   c. Define an interface contract between them and implement in parallel
3. Update root plan with revised subphase structure
4. Re-run Phase 4 on affected subphases

---

## Rate Limiting (Codex API)

**Symptom:** Multiple Codex calls in Phase 4 hit rate limits.

**Recovery:**
1. Queue Codex calls instead of running all in parallel
2. Stagger with 2-second delays between calls
3. Opus and phase-gaps agents are NOT affected (different API)
4. Document any Codex calls that were skipped due to rate limits

---

## Git Conflicts with Active Work

**Symptom:** `git status` shows uncommitted changes that overlap with the problem set.

**Recovery:**
1. Warn user: "There are uncommitted changes that overlap with this analysis"
2. Options:
   a. Stash changes, run Deep Sweep on clean state, pop stash after
   b. Proceed with current state (analysis reflects dirty state)
   c. User commits first, then runs Deep Sweep
3. If proceeding: note in root plan that analysis was done on uncommitted state

---

## Single Problem (No Subphases Needed)

**Symptom:** User has only one problem — no subphase decomposition makes sense.

**Recovery:**
1. Still run the full pipeline — single subphase is fine
2. Skip Phase 5 cross-comparison (nothing to compare)
3. Phase 4 still runs all three agents on the single subphase
4. The value is the Opus + Codex cross-verification, not the subphase structure

---

## Context Degradation in Long-Running Sweep

**Symptom:** Later phases produce lower-quality analysis because early context
has been compressed or dropped.

**Prevention:**
1. Write ALL findings to disk as they're produced (phase plan files)
2. Later agents read from disk, not from conversation context
3. Keep conversation-level context minimal — point agents to file paths
4. Use the 84.7% confidence threshold to catch declining analysis quality

**Recovery:**
1. If quality drops: re-read the phase plan from disk to refresh context
2. If severe: start a new conversation with the phase plan as input
3. Use `$context-compression` techniques if needed
