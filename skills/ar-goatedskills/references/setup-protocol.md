# Setup Protocol

Complete installation and configuration procedures for GitNexus across all
supported environments. The skill's Phase 0-1 follows this protocol.

---

## Prerequisites

| Requirement | Minimum | Check Command |
|-------------|---------|---------------|
| Node.js | >= 20.0.0 | `node --version` |
| npm | >= 9.0.0 | `npm --version` |
| Git repo | recommended | `git rev-parse --git-dir` |

If Node.js is below 20:
- macOS: `brew install node@24` or `nvm install 24`
- Linux: `nvm install 24` or package manager
- STOP if Node.js cannot be upgraded — GitNexus requires native Tree-sitter bindings

---

## Installation

### Global Install (Preferred)

```bash
npm install -g gitnexus
gitnexus --version  # Verify
```

### npx Fallback

If global install fails (permissions, corporate environment):
```bash
npx gitnexus --version  # Verify npx path works
```

All subsequent commands use `npx gitnexus` instead of `gitnexus`.

### Verify Binary

```bash
which gitnexus                    # Should return a path
gitnexus --version                # Should print version
gitnexus --help                   # Should list commands
```

---

## MCP Configuration

### Claude Code

```bash
# One command — registers GitNexus as MCP server (use global binary, NOT npx)
claude mcp add -s user gitnexus -- gitnexus mcp
```

Verify:
```bash
claude mcp list | grep -i gitnexus
```

Expected output: `gitnexus: gitnexus mcp - Connected`

**WARNING:** Do NOT use `npx -y gitnexus@latest mcp` — npx caches corrupt frequently
and cause `MODULE_NOT_FOUND` errors. Always use the global binary.

### Codex CLI

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.gitnexus]
command = "gitnexus"
args = ["mcp"]
```

Verify: Restart Codex, check that `gitnexus` tools appear.

### Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "gitnexus": {
      "command": "npx",
      "args": ["-y", "gitnexus@latest", "mcp"]
    }
  }
}
```

### Auto-Setup (All Editors)

```bash
gitnexus setup
```

Auto-detects installed editors (Claude Code, Cursor, Codex, Windsurf, OpenCode)
and writes MCP configuration to each. Idempotent — safe to run multiple times.

---

## Repository Indexing

### First-Time Index

```bash
cd /path/to/project
gitnexus analyze --embeddings --skills
```

Flags:
- `--embeddings` — Build vector embeddings for semantic search (slower, recommended)
- `--skills` — Generate per-cluster skill files in `.claude/skills/generated/`
- `--force` — Force full re-index (ignore staleness check)
- `--skip-agents-md` — Don't modify AGENTS.md
- `--skip-git` — Allow indexing without .git directory
- `-v` / `--verbose` — Log skipped files

### What Gets Created

```
.gitnexus/
├── lbug/           # LadybugDB graph database
├── meta.json       # Index metadata (last commit, stats, timestamp)
└── ...

# If --skills flag used:
.claude/skills/generated/
├── cluster-auth.md
├── cluster-api.md
└── ...

# If AGENTS.md doesn't have --skip-agents-md:
AGENTS.md           # Updated with GitNexus tool usage section
```

### Re-Indexing

Check staleness:
```bash
gitnexus status
```

If stale (new commits since last index):
```bash
gitnexus analyze
```

Omit `--embeddings` on re-index for speed if embeddings were built on first run
and no new files were added.

---

## Ignore Patterns

Create `.gitnexusignore` in project root (same syntax as `.gitignore`):

```
# Typical patterns
node_modules/
dist/
build/
.next/
coverage/
*.generated.*
*.min.js
vendor/
```

GitNexus also respects `.gitignore` by default.

---

## Multi-Repo Setup

GitNexus serves all indexed repos from a single MCP server via a global registry.

```bash
# Index multiple repos
cd /path/to/repo-a && gitnexus analyze --embeddings
cd /path/to/repo-b && gitnexus analyze --embeddings

# Check registry
cat ~/.gitnexus/registry.json

# Create a group for cross-repo queries
gitnexus group create my-platform
gitnexus group add my-platform repo-a
gitnexus group add my-platform repo-b
gitnexus group sync my-platform    # Extract cross-repo contracts
```

---

## Verification Checklist

After setup, verify each layer:

```bash
# 1. Binary works
gitnexus --version

# 2. Index exists
ls .gitnexus/meta.json

# 3. Index is current
gitnexus status

# 4. MCP is configured (Claude Code)
claude mcp list 2>/dev/null | grep -i gitnexus

# 5. MCP tools respond (test query)
# In Claude Code, try: mcp__gitnexus__list_repos
# Or via CLI:
gitnexus query "main entry point"
```

All 5 checks must pass before the skill proceeds to Phase 3 (Leverage).

---

## Troubleshooting

### "gitnexus: command not found"
```bash
# Check npm global bin is in PATH
npm config get prefix    # e.g., /usr/local
ls $(npm config get prefix)/bin/gitnexus
# If missing, reinstall:
npm install -g gitnexus
```

### "Cannot find module 'tree-sitter'"
Node.js version too old. Upgrade to >= 20.0.0.

### Index takes too long
- Add patterns to `.gitnexusignore` (vendor dirs, generated code)
- Skip embeddings on re-index: `gitnexus analyze` (without `--embeddings`)
- Check heap: CLI auto-allocates 8GB but may need more for very large repos

### MCP tools not appearing in Claude Code
```bash
# Remove and re-add
claude mcp remove gitnexus
claude mcp add gitnexus -- npx -y gitnexus@latest mcp
# Restart Claude Code session
```

### Stale index warnings
```bash
gitnexus analyze  # Re-index to HEAD
```

### LadybugDB migration error
Old indexes used KuzuDB. Delete `.gitnexus/` and re-index:
```bash
rm -rf .gitnexus
gitnexus analyze --embeddings --skills
```

---

## New Device Quickstart

For setting up a fresh machine after cloning goatedskills:

```bash
# 1. Install GitNexus
npm install -g gitnexus

# 2. Auto-configure all detected editors
gitnexus setup

# 3. Index whatever repo you're working in
cd /path/to/project
gitnexus analyze --embeddings --skills

# 4. Verify
gitnexus status
```

The skill handles all of this automatically when invoked. These manual steps
are only needed if you want to set up before the first skill invocation.
