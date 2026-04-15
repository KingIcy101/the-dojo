# QA Protocol

4-layer QA verification using every available testing tool. Each layer catches
different classes of issues. Together they provide comprehensive coverage.

---

## Layer Architecture

```
Layer 1: Automated Tests          Layer 2: Visual QA
├── npm test / pytest             ├── Desktop screenshot (browse-qa)
├── Coverage >= 80%               ├── Mobile screenshot (375px)
├─�� Write missing tests           ├── Console error check
└── No flaky patterns             └── Pass/Fail with evidence

Layer 3: Functional QA            Layer 4: Codex Verification
├── Claude-in-Chrome MCP          ├── Test suite analysis
├── Computer Use control          ├── API contract verification
├── Playwright CLI                ├── Edge case detection
├── OpenClaw persistent profile   ├── Error path verification
└── End-to-end user flows         └── Cross-model test review
```

---

## Layer 1: Automated Tests

**Agent:** `qa-tests` (subagent_type: tdd-guide)

**Process:**
1. Run the project's test suite: `npm test`, `pytest`, `go test`, etc.
2. Check coverage: `npm run test:coverage` or equivalent
3. If coverage < 80%: identify uncovered new code, write tests
4. If tests fail: report failures with file:line + error message
5. Check for flaky patterns: tests that pass/fail inconsistently

**Output:** test results, coverage %, list of new tests written

---

## Layer 2: Visual QA

**Agent:** `qa-visual` (uses $browse-qa pattern)

**Process:**
1. Start dev server if not running
2. Open target URL in OpenClaw browser profile
3. Desktop screenshot (full page)
4. Resize to 375px → mobile screenshot
5. Read console messages → flag errors/warnings tied to changes
6. Exercise critical interaction path (click primary CTA, navigate)
7. Close test tabs

**Pass criteria:**
- No blank pages or 404/500
- Primary UI elements visible and positioned correctly
- No layout breaks on mobile
- No console errors tied to changed code

**Fail signals:**
- Blank page, missing primary UI, auth loop, console errors from changed code

**Output:** screenshots (desktop + mobile), console log excerpt, pass/fail verdict

---

## Layer 3: Functional QA

**Agent:** `qa-functional`

This is the most comprehensive QA layer. Actually interact with the app.

### Tool Selection Decision Tree

```
What are you testing?
├── Web app with UI?
│   ├── Simple page check → Claude-in-Chrome (navigate + read_page)
│   ├── Form submission → Claude-in-Chrome (form_input + computer)
│   ├── Complex multi-step flow → Computer Use (screenshot-based)
│   ├── Auth-gated pages → OpenClaw profile + Claude-in-Chrome
│   └── Repeatable regression → Playwright CLI (npx playwright test)
├── CLI tool?
│   └── Bash tool (run commands, check output)
├── API endpoint?
│   └��─ Bash tool (curl/httpie) + Codex verification
└── Background job / worker?
    └── Bash tool (trigger + check logs/DB)
```

### Claude-in-Chrome MCP Patterns

**Navigate and verify:**
```
mcp__claude-in-chrome__tabs_context_mcp  → get current tabs
mcp__claude-in-chrome__tabs_create_mcp   → open new tab
mcp__claude-in-chrome__navigate          → go to URL
mcp__claude-in-chrome__read_page         ��� verify content rendered
mcp__claude-in-chrome__read_console_messages → check for errors
```

**Interact with UI:**
```
mcp__claude-in-chrome__computer          → click, type, scroll (screenshot-based)
mcp__claude-in-chrome__form_input        → fill form fields
mcp__claude-in-chrome__javascript_tool   → check app state, validate data
mcp__claude-in-chrome__find              → locate elements on page
```

**Record for evidence:**
```
mcp__claude-in-chrome__gif_creator       → record multi-step interactions
```

### Computer Use Patterns

For complex flows that need screenshot-based interaction:

1. Take screenshot → identify target element
2. Click/type at coordinates
3. Wait for response
4. Take another screenshot → verify state changed
5. Repeat for each step in the flow

Best for:
- Drag-and-drop interactions
- Canvas/SVG-based UIs
- Multi-window workflows
- Hover states and tooltips

### Playwright CLI Integration

For repeatable, scriptable tests:

```bash
# Run existing Playwright tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/critical-flow.spec.ts

# Generate new test from interaction
npx playwright codegen http://localhost:3000
```

If Playwright is configured in the project (`playwright.config.ts` exists):
- Run the full suite
- Report failures with screenshots
- If no tests exist for new features: consider generating them

### OpenClaw Persistent Profile

For testing auth-gated flows:
- OpenClaw browser profile maintains login state across sessions
- Use for: dashboard pages, user settings, admin flows, API key management
- Pattern: navigate with OpenClaw profile → verify content → interact

### Functional QA Test Plan Template

For each changed feature, test:

1. **Happy path** — does the primary flow work?
2. **Error state** — what happens with bad input?
3. **Edge case** — boundary values, empty states, long strings
4. **Auth** — can unauthorized users access it? (if applicable)
5. **Persistence** — does data survive page reload?
6. **Mobile** — does the flow work on small screens?

---

## Layer 4: Codex Functional Verification

**Tool:** Codex CLI (gpt-5.4, read-only sandbox)

**Process:**
```bash
codex exec --model gpt-5.4 -c model_reasoning_effort=high --sandbox read-only \
  "Analyze the implementation and tests for this change:

   1. TEST SUITE ANALYSIS
   - Are all new functions/endpoints tested?
   - Are edge cases covered (null, empty, boundary, concurrent)?
   - Are error paths tested (network failure, invalid input, timeout)?
   - Any flaky test patterns (timing, external deps, shared state)?

   2. API CONTRACT VERIFICATION
   - Do endpoints match their type definitions?
   - Are request/response shapes validated?
   - Are error responses consistent?

   3. DATA FLOW VERIFICATION
   - Are transformations correct (input → processing → output)?
   - Are database operations safe (transactions, rollbacks)?
   - Are external API calls handled (retries, timeouts, errors)?

   4. SECURITY VERIFICATION
   - Input validation at boundaries?
   - Auth checks on protected routes?
   - No secrets in responses?

   Report findings by severity." 2>/dev/null
```

---

## QA Result Aggregation

After all 4 layers complete, aggregate results:

```
LAYER 1 (Tests):     PASS/FAIL — coverage: X% — N tests written
LAYER 2 (Visual):    PASS/FAIL — screenshots attached — N issues
LAYER 3 (Functional): PASS/FAIL — N flows tested — N issues
LAYER 4 (Codex):     PASS/FAIL — N findings by severity

OVERALL: PASS (all layers pass) / FAIL (any layer fails)
```

**Proceed to Ship only when OVERALL = PASS.**

If FAIL:
1. Fix issues found
2. Re-run only the failed layer(s)
3. Max 3 retry cycles per layer
4. If still failing after 3 retries → escalate to user

---

## When to Skip Layers

| Change Type | Layer 1 | Layer 2 | Layer 3 | Layer 4 |
|-------------|---------|---------|---------|---------|
| Backend only (no UI) | RUN | SKIP | CLI/API only | RUN |
| Frontend only | RUN | RUN | RUN | RUN |
| Full-stack | RUN | RUN | RUN | RUN |
| Config/env only | SKIP | SKIP | SKIP | RUN |
| Tests only | RUN | SKIP | SKIP | RUN |
| DB migration | RUN | SKIP | SKIP | RUN |
