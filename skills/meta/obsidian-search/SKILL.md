# Skill: obsidian-search

## What It Does
MCP server that exposes the `~/brain/` Obsidian vault to Claude Code via three tools:

| Tool | What it does |
|------|-------------|
| `vault_search` | Full-text keyword search across all `.md` files. Returns scored, sorted results with excerpts. |
| `vault_recent` | Lists recently modified files (optionally scoped to a subfolder). |
| `vault_read` | Reads a specific file by path (relative to `~/brain/`). |

No external dependencies beyond `@modelcontextprotocol/sdk` — pure `fs` + recursive walk + keyword matching.

## When to Use
- Before starting any task: check if prior context exists in the vault
- When working with sessions, topics, or knowledge files
- As a replacement for manually `cat`-ing files in `~/brain/`

## Vault Root
`/Users/mattbender/brain/`

Key subdirectories:
- `Topics/` — evergreen notes
- `sessions/claude-code/` — auto-archived session logs
- `inbox/` — scratch notes
- `knowledge/` — structured knowledge base
- `OpenClaw/` — OpenClaw-specific notes

## How to Run

### As MCP Server (registered in Claude Code)
Already wired in `~/.claude/settings.json` as `obsidian-search`. Restart Claude Code to activate.

### Manual test
```bash
cd /Users/mattbender/.openclaw/workspace/.agents/skills/obsidian-search
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | node server.js
```

### Search example
```bash
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"vault_search","arguments":{"query":"openclaw memory","limit":5}}}' | node server.js
```

## Claude Code Config
```json
"obsidian-search": {
  "command": "node",
  "args": ["/Users/mattbender/.openclaw/workspace/.agents/skills/obsidian-search/server.js"]
}
```


## Learned In Use

- **2026-03-19:** Strategic changes must be written to daily memory file immediately in the same turn — deferring Obsidian writes or claiming 'saved/logged' without verification creates gaps in agent decision-making and memory accuracy.
- **2026-03-20:** MCP servers (obsidian-search and obsidian-mcp) spin up on demand when Claude Code starts via stdio and then exit — they are not persistent daemons, so stateful caching strategies won't work.
- **2026-03-21:** The memory_search tool only searches *.md files directly in the memory/ folder, not subdirectories — symlinked brain vault folders won't be indexed, requiring consolidation scripts instead.

## Learned from Use (2026-03-22)
SKIP

The session logs contain no mentions of the `obsidian-search` skill being used. The logs reference Obsidian Sync setup tasks (logging in to restore Mac mini graph sync), but these are manual UI operations, not uses of an "obsidian-search" skill. There are no corrections, failures, or patterns associated with this skill to extract.

- **2026-03-22:** Semantic search in Obsidian is most effective for retrieving past decisions when using full document content via `--file=/path` rather than truncated summaries; brain-ingest with default settings truncates to one-line summaries and loses context value.
- **2026-03-25:** Memory lookup rule: never declare something 'doesn't exist' without (1) broad memory_search first, (2) reading full config structure before drilling down, (3) trying alternate paths, (4) only then concluding — this prevents false negatives on nested config queries.
- **2026-03-27:** Agent files stored in workspace-* directories are not synced to Obsidian directly — only manual ingestions to vault work, requiring explicit sync verification steps.

## Learned from Use (2026-03-29)
SKIP

**Reasoning:** The session logs provided contain no mentions of the "obsidian-search" skill being used. The logs document build pipeline corrections, agent coordination issues, font size fixes, and deployment processes, but there is no evidence that obsidian-search was invoked, tested, or learned from during these sessions. To extract meaningful lessons about this specific skill's usage, I would need logs showing actual obsidian-search invocations and their outcomes.

- **2026-04-09:** Session handoff files (handoff-current.md) should be checked for stale context older than 2 hours — Matt's preference indicates this is a critical refresh boundary for context accuracy.
- **2026-04-13:** Session handoff workflows benefit from a hot-context.md file pattern that summarizes active state across workspace sessions, enabling quick context reloading without re-reading full memory files.