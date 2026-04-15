# Browse QA blueprint

This is the part of gstack worth stealing hardest.

## Keep the philosophy

- browser QA is a first-class lane, not an afterthought
- sessions should be persistent enough to preserve auth and flow state
- verification should be screenshot-driven, not code-vibe-driven
- console inspection and visible-error checks belong in the same pass
- the browser lane should be repeatable, not artisanal clicking

## Adapt it to OpenClaw

We do **not** need gstack's Bun browser daemon because OpenClaw already gives us the important primitives:

- persistent browser profile: `openclaw`
- stable tab targeting via `targetId`
- snapshots with refs
- screenshots
- console logs
- structured actions (`click`, `fill`, `press`, `evaluate`, `close`)

## Podhi browse-qa workflow

1. Open/focus the target in the `openclaw` profile.
2. Capture a snapshot and keep the returned `targetId` for the whole flow.
3. Take a desktop screenshot.
4. Resize or reopen for mobile and take a mobile screenshot.
5. Run the critical path interactions for the impacted feature.
6. Check console output.
7. Call pass/fail explicitly.
8. Close task tabs immediately after the pass.

## Evidence bar

A valid browse QA pass should include:
- target URL(s)
- what path/flow was exercised
- at least one screenshot per important state
- console check status
- any visible failure shell / blank state / 4xx/5xx semantic failure
- cleanup confirmation

## Failure semantics

Treat these as FAIL, not "probably fine":
- blank or obviously broken shell
- 404 / 500 / framework error screen
- missing primary UI on the target route
- console errors tied to the changed flow
- interaction path cannot complete

## Why this matters to build mode

The build chain should no longer jump from implementation straight to commit on UI-facing work.
The correct order is:

```text
implement -> review -> browse-qa -> ship
```

That is the whole point of adding a dedicated browse gear.
