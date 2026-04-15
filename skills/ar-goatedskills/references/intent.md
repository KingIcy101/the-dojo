# Intent: GitNexus Skill

## Why This Exists

AI coding agents today navigate codebases by reading files one at a time. They discover
dependencies iteratively — read a file, find an import, read that file, find a call,
read that file. This is like exploring a city without a map.

GitNexus pre-computes the entire relationship graph: every function, every call chain,
every import, every execution flow. Agents query this graph instantly instead of
iteratively discovering structure. The difference is GPS vs. wandering.

## Design Decisions

### Why self-bootstrapping?
The user clones goatedskills on a new machine and needs everything to just work. The
skill checks its own prerequisites, installs what's missing, configures what needs
configuring, and verifies the result. No manual setup steps to remember.

### Why MCP over CLI?
MCP tools are available inside agent context without spawning a shell. An agent can
call `mcp__gitnexus__impact` mid-reasoning without interrupting its thought process.
CLI requires a Bash tool call, output parsing, and context switching.

### Why index with embeddings by default?
Embeddings enable semantic search — finding code by meaning, not just keywords.
The indexing cost is paid once; every subsequent query benefits. For the workflows
in deep-sweep and deep-build where agents search for related code, semantic search
catches what keyword search misses.

### Why per-cluster skills with --skills?
GitNexus can generate `.claude/skills/generated/` files that describe each functional
module in the codebase. These skills give agents domain-specific context about each
area of the code without reading every file.

### Why global install over npx?
npx downloads the package on every invocation. Global install runs instantly.
For a tool that's called frequently (re-index, queries, status checks), the
speed difference adds up. npx is the fallback for environments where global
install isn't available.

## What This Is NOT

- Not a code search tool — it's a relationship graph (search is one feature)
- Not a documentation generator — it's structural intelligence
- Not a replacement for reading code — it's a map for knowing WHERE to read
- Not an editor plugin — it's an MCP server that any editor can consume
- Not cloud-based — everything runs locally, no data leaves the machine
