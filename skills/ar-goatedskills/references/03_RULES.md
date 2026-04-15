# Rules (Hard)

- Keep going until the phase is **done** or you are **blocked**.
- If blocked, do all independent work first, then ask the minimum set of high-leverage questions.
- Start each turn with `$karpathy-guidelines`: confirm assumptions, keep changes surgical, and define/verify success criteria.
- If docs are mentioned or the answer depends on current platform/library behavior, use `$context7-docs` to fetch up-to-date docs via Context7 MCP before answering.
- When making claims/decisions grounded in provided documents (phase plans, skill references, pasted excerpts), use `$recursive-reasoning-operator` to extract supporting snippets and verify logic, then synthesize back into Terminus Maximus updates.
- Always update phase docs **before replying**:
  - Active subphase: keep Work concrete; record changes and commands; fill Output/Handoff when complete.
  - Root plan: check success criteria when met; append a short “Phase Summary (running)” update.
- Always run `$phase-gaps` **every turn** after updating progress to tighten the plan and surface questions/assumptions.
- Never silently skip quality gates. If you can’t run `npm run lint` / `npm run build`, record why and what the user must do next.
- Never auto-create a new phase unless the user explicitly asks.
- Keep questions to the user **≤ 3 per turn**; use the UI question tool when available.
