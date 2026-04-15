# Templates

## Root Plan Template

```md
# Phase <N> — <derived title>

## Original User Request (verbatim)
(Paste the full original user request that triggered /phase-plan with no edits)

## Purpose
(One or two sentences summarizing the user's objective)

## Context
(Extract key reasoning from the conversation so intent/rationale is preserved)

## Skills Available for Implementation
- `find-local-skills`: <run and summarize relevant skills>
- `find-skills`: <run and summarize relevant skills>
- Selected implementable skills: <list>

## Concurrent Phases
(Optional — include if overlaps detected during conflict check)

| Phase | Status | Overlap | Coordination |
|-------|--------|---------|--------------|
| Phase N-1 | Active/Complete | Files: X, Y | Wait for completion / Merge changes |
| Phase N-2 | Active | Domain: Z | Independent, no action needed |

## Objectives
* [ ] Identify subtasks necessary to resolve this phase
* [ ] Execute subtasks in sequence
* [ ] Produce measurable outputs

## Constraints
(Include relevant technical/architectural rules mentioned in the discussion)

## Success Criteria
(Concrete closure conditions for this phase)

## Subphase Index
* a — <generated subtask name>
* b — <generated subtask name>
* c — ...
```

## Subphase Plan Template

```md
# Phase <N><letter> — <Subtask Name>

## Focus
(What this subphase is doing and why)

## Inputs
(Artifacts or reasoning from prior subphases or root context)

## Skills Available for This Subphase
- `find-local-skills` output: <high-signal skills that can be invoked>
- `find-skills` output: <high-signal skills that can be invoked>
- Planned invocations: <only include confirmed available skills>

## Work
(Steps/decisions needed; include any checks or validations)

## Output
(Clear conclusion or artifact reference)

## Handoff
(Explicit instruction for the next subphase)
```
