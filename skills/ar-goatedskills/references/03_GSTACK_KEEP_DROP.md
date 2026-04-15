# gstack keep / drop notes

## Tested locally

Repo inspected locally from GitHub: `garrytan/gstack`

Observed structure:
- `plan-ceo-review/`
- `plan-eng-review/`
- `review/`
- `browse/`
- `ship/`
- `retro/`
- Bun/Playwright browser daemon under `browse/src/`

## Worth keeping

1. **Explicit gears**
   - This is the main win.
   - Planning, review, QA, and shipping are different cognitive jobs.

2. **Browse as a dedicated lane**
   - The strongest part of the repo.
   - Keeps browser checks fast, structured, and repeatable.

3. **Review is separate from implementation**
   - Good discipline. Prevents the builder from grading its own homework.

4. **Ship is separate from planning**
   - Also correct. Release automation should run on already-shaped work.

## Not worth copying directly

1. **The Bun browser binary itself**
   - Good for Claude Code. Redundant for OpenClaw.

2. **Claude-specific setup/symlink assumptions**
   - Irrelevant to Podhi.

3. **Their exact command surface**
   - We can get the same value with one canonical `/build` command plus `--gear`.

4. **Interactive review ergonomics built around AskUserQuestion**
   - Useful in Claude Code, not the right primitive here.

## Bottom line

Steal the gears.
Steal the browse philosophy.
Do not import the scaffolding just because it looks impressive.
