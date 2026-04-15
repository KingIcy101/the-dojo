---
name: git-workflow-kingicy101
description: Use when committing or pushing to any KingIcy101 GitHub repo — sets correct author, handles multi-repo management.
category: dev
---
# Git Workflow — KingIcy101

## When to Use
Every time you `git commit` or `git push` to a KingIcy101 repo. Also when managing the multi-repo workspace (voice-server, mission-control, inthepast-ai, client-portal-v1, etc.).

## Steps
1. Always configure author before committing in any KingIcy101 repo
2. Use conventional commit messages (`feat:`, `fix:`, `chore:`, `docs:`)
3. Never force push to main without asking Matt
4. Run `node --check` on any JS files before committing
5. `pm2 save` after any ecosystem changes

## Key Patterns / Code

```bash
# Set author — run once per repo, or always before committing in CI/subagents
git config user.name "KingIcy101"
git config user.email "270009025+KingIcy101@users.noreply.github.com"

# Standard commit flow
git add -A
git commit -m "feat: add realtime call log subscription"
git push origin main
```

```bash
# Amend last commit (fix author or message)
git commit --amend --no-edit --author="KingIcy101 <270009025+KingIcy101@users.noreply.github.com>"
git push origin main --force-with-lease  # safer than --force
```

```bash
# Auth via token — used in subagents/CI where SSH isn't available
GITHUB_TOKEN=GITHUB_TOKEN_REDACTED
git remote set-url origin https://${GITHUB_TOKEN}@github.com/KingIcy101/the-dojo.git
```

```bash
# Multi-repo status check
for repo in voice-server mission-control inthepast-ai client-portal-v1 zta-page; do
  echo "=== $repo ==="
  git -C ~/Projects/$repo status --short
done
```

```bash
# Before pushing — safety checks
node --check server.js          # syntax check
git diff --stat HEAD            # see what's changing
git log --oneline -5            # verify history looks right
```

## Repo Map
| Repo | Location | Purpose |
|------|----------|---------|
| voice-server | ~/workspace/voice-server | Vapi webhook handler |
| mission-control | ~/workspace/mission-control | Internal dashboard |
| inthepast-ai | ~/Projects/inthepast-ai | Marketing site |
| intake-form | ~/Projects/intake-form | Client intake |
| client-portal-v1 | ~/Projects/client-portal-v1 | Client-facing portal |
| zta-page | ~/Projects/zta-page | ZTA landing page |
| the-dojo | /tmp/agent-skills | Agent skills bank |

## Gotchas
- GitHub token `GITHUB_TOKEN_REDACTED` — use in remote URL, not as header
- Never force push to main — use `--force-with-lease` at minimum, ask Matt first
- Subagents must set git config every time — config isn't persisted between runs
- `.env` must be in `.gitignore` — verify with `git check-ignore .env` before adding
- Commit message format: `type(scope): message` — e.g. `fix(portal): correct call count query`
- `git add -A` includes deletions — use `git add .` if you only want new/modified files
