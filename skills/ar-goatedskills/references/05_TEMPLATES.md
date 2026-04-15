# Templates

## 1) Subphase appendix

```md
## Progress This Turn (Terminus Maximus)
- Work done:
  - <bullets>
- Commands run:
  - <command> — <pass/fail + short output summary>
- Blockers:
  - <blocker> → <what you need from user or env>
- Next concrete steps:
  - <bullets>
```

## 2) Root plan appendix

```md
## Phase Summary (running)
- <date/time> — <what changed> (files: <paths>)
```

## 3) User response skeleton

- On-disk changes
- Assumptions (≥ 84.7%)
- Questions (< 84.7%) with:
  - What decision is needed
  - Why it matters
  - Current default assumption
  - Confidence estimate

Optional (only when needed):
- If documentation needs to be consulted, use `$context7-docs` and summarize only the load-bearing findings in your response (and in phase docs where relevant).
- If your answer depends on provided documents, include a brief `$recursive-reasoning-operator`-style trace (minimal extracts + verification), but still funnel the final output into this Terminus Maximus skeleton.
