# Tool Patterns

How to use each GitNexus MCP tool effectively. These patterns guide agents on which
tool to reach for in each situation.

---

## Tool Selection Decision Tree

```
What do you need?

├── "What repos are indexed?"
│   └── mcp__gitnexus__list_repos
│
├── "How does [feature] work?"
│   └── mcp__gitnexus__query → search by feature keyword
│       └── Follow up: mcp__gitnexus__context on key symbols
│
├── "What calls this function / what does it call?"
│   └── mcp__gitnexus__context → 360° view of the symbol
│
├── "What breaks if I change X?"
│   └── mcp__gitnexus__impact → blast radius analysis
│
├── "What did this git diff affect?"
│   └── mcp__gitnexus__detect_changes → map diff to symbols
│
├── "Can I safely rename X?"
│   └── mcp__gitnexus__rename → dry-run with all affected files
│
├── "Complex graph question"
│   └── mcp__gitnexus__cypher → raw Cypher query
│
└── "Cross-repo flow analysis"
    └── mcp__gitnexus__group_query
```

---

## Tool Reference

### list_repos

**Purpose:** Discover what's indexed. Always start here in a new session.

**When:** First interaction with GitNexus in a conversation. Orientation.

**Output:** YAML with repo name, path, file count, node count, edge count,
community count, process count.

**Example use:**
```
mcp__gitnexus__list_repos()
```

---

### query

**Purpose:** Find execution flows matching a keyword or concept.

**When:** Exploring how a feature works. Understanding a domain.

**Parameters:**
- `query` (string) — Natural language or keyword search
- `repo` (string, optional) — Target repo name (defaults to current)

**Output:** Ranked execution flows with symbols, file locations, confidence.

**Example uses:**
```
mcp__gitnexus__query(query: "authentication login flow")
mcp__gitnexus__query(query: "payment processing", repo: "kynship-forecast")
mcp__gitnexus__query(query: "database migration")
```

**Pattern:** Start broad, then drill into specific symbols with `context`.

---

### context

**Purpose:** 360-degree view of a specific symbol — who calls it, what it calls,
which processes it belongs to, what cluster it's in.

**When:** Deep understanding of a specific function, class, or method.

**Parameters:**
- `symbol` (string) — Symbol name or qualified name
- `repo` (string, optional) — Target repo name

**Output:** Incoming calls (callers), outgoing calls (callees), processes,
community membership, file location with line numbers.

**Example uses:**
```
mcp__gitnexus__context(symbol: "UserService.authenticate")
mcp__gitnexus__context(symbol: "handlePayment", repo: "kynship-forecast")
```

**Pattern:** Use after `query` to drill into specific symbols of interest.

---

### impact

**Purpose:** Blast radius analysis — what breaks if you modify a symbol.

**When:** Before modifying shared code. Before refactoring. Risk assessment.

**Parameters:**
- `symbol` (string) — Symbol to analyze impact of
- `repo` (string, optional) — Target repo name
- `depth` (number, optional) — How many hops to trace (default: 2)

**Output:** Upstream dependents (grouped by depth), affected processes,
confidence tiers, risk level.

**Example uses:**
```
mcp__gitnexus__impact(symbol: "UserService")
mcp__gitnexus__impact(symbol: "calculateRevenue", depth: 3)
```

**Output structure:**
```yaml
TARGET: Class UserService (src/services/user.ts)

UPSTREAM (what depends on this):
  Depth 1 (WILL BREAK):
    - handleLogin [CALLS 90%] → src/api/auth.ts:45
  Depth 2 (LIKELY AFFECTED):
    - authRouter [IMPORTS] → src/routes/auth.ts

CONFIDENCE: 90%+
PROCESSES AFFECTED: LoginFlow, RegistrationFlow
RISK LEVEL: medium
```

**Pattern:** Always run impact BEFORE modifying shared code. If risk is high,
discuss with user before proceeding.

---

### detect_changes

**Purpose:** Map a git diff to the symbols and processes it affects.

**When:** Pre-commit analysis. PR review. Understanding what changed.

**Parameters:**
- `repo` (string, optional) — Target repo name
- `diff` (string, optional) — Git diff to analyze (defaults to working changes)

**Example uses:**
```
mcp__gitnexus__detect_changes()                    # Current working changes
mcp__gitnexus__detect_changes(repo: "my-project")  # Specific repo
```

**Pattern:** Run before committing to understand the full impact of changes.
Feed results into deep-build's Gear 4 (Review) for comprehensive review.

---

### rename

**Purpose:** Dry-run preview of a symbol rename — shows all files that would change.

**When:** Safe refactoring. Understanding symbol usage before renaming.

**Parameters:**
- `symbol` (string) — Current symbol name
- `new_name` (string) — Proposed new name
- `repo` (string, optional) — Target repo name

**Example uses:**
```
mcp__gitnexus__rename(symbol: "getUserData", new_name: "fetchUserProfile")
```

**Pattern:** Run rename dry-run first, review all affected files, THEN
perform the actual rename across the codebase.

---

### cypher

**Purpose:** Raw Cypher graph queries for advanced analysis.

**When:** Questions that don't fit other tools. Custom graph traversals.

**Parameters:**
- `query` (string) — Cypher query
- `repo` (string, optional) — Target repo name

**Example Cypher queries:**

```cypher
# All functions that call more than 5 other functions (complexity hotspots)
MATCH (f:Function)-[:CALLS]->(target:Function)
WITH f, COUNT(target) AS callCount
WHERE callCount > 5
RETURN f.name, f.file, callCount
ORDER BY callCount DESC

# All circular dependencies
MATCH (a:Function)-[:CALLS]->(b:Function)-[:CALLS]->(a)
RETURN a.name, a.file, b.name, b.file

# Entry points with no callers
MATCH (f:Function)
WHERE NOT ()-[:CALLS]->(f) AND f.isExport = true
RETURN f.name, f.file

# All symbols in a specific file
MATCH (n)-[:DEFINED_IN]->(f:File {path: 'src/auth/service.ts'})
RETURN n.name, labels(n), n.lineNumber
```

**Pattern:** Check `gitnexus://repo/{name}/schema` first to understand
available node types and relationship types before writing Cypher.

---

### group_query

**Purpose:** Cross-repo execution flow analysis.

**When:** Multi-repo projects where code flows across repository boundaries.

**Parameters:**
- `group` (string) — Repository group name
- `query` (string) — Search query

**Prerequisite:** Repos must be grouped:
```bash
gitnexus group create my-platform
gitnexus group add my-platform repo-a
gitnexus group add my-platform repo-b
gitnexus group sync my-platform
```

---

## MCP Resources

Read-only context that agents can access without tool calls:

| Resource URI | Content |
|-------------|---------|
| `gitnexus://repos` | List all indexed repos with stats |
| `gitnexus://repo/{name}/context` | Repo overview: stats, staleness, tools |
| `gitnexus://repo/{name}/clusters` | Functional clusters with cohesion scores |
| `gitnexus://repo/{name}/cluster/{name}` | Members and details of one cluster |
| `gitnexus://repo/{name}/processes` | All traced execution flows |
| `gitnexus://repo/{name}/process/{name}` | Full process trace with steps |
| `gitnexus://repo/{name}/schema` | Graph schema for Cypher queries |

---

## Workflow Recipes

### Explore an Unfamiliar Codebase

```
1. list_repos → see what's indexed
2. Read gitnexus://repo/{name}/clusters → understand high-level modules
3. query("main entry points") → find starting points
4. context(symbol) on each entry point → trace the architecture
```

### Pre-Commit Safety Check

```
1. detect_changes → map diff to affected symbols
2. impact(symbol) for each CRITICAL symbol → check blast radius
3. If risk HIGH+: flag to user before committing
```

### Safe Refactoring

```
1. rename(old, new) → dry-run preview
2. Review all affected files
3. impact(old) → check for indirect dependents
4. Perform rename
5. detect_changes → verify only expected files changed
```

### Architecture Deep Dive (for deep-sweep)

```
1. list_repos → confirm index is current
2. query(problem_area) → find relevant execution flows
3. context(key_symbols) → understand relationships
4. impact(symbols_to_change) → blast radius for planned changes
5. cypher(custom_query) → find interaction effects
```
