---
name: brain-vault-obsidian
description: Write to and search Matt's Obsidian brain vault at ~/brain using brain-ingest.sh and brain-search.sh.
category: meta
---

# Brain Vault / Obsidian System

## When to Use
Any time something needs to persist beyond the current session: decisions, new tools, todos, corrections, plans.
MANDATORY: write to vault AND update MEMORY.md in the same response — never silo them.

## Steps
1. Run brain-ingest.sh with title, content, tags, source
2. In the same response, add one-liner to MEMORY.md under `## Recently Saved`
3. For retrieval, use brain-search.sh before starting any task
4. Append only to existing notes — never rewrite

## Key Patterns / Code

### brain-ingest.sh (write to vault)
```bash
bash /Users/mattbender/brain/scripts/brain-ingest.sh   --title="ITP Portal — Stripe Billing Setup"   --content="## Summary
Wired Stripe webhooks for ITP portal. Webhook events: checkout.session.completed, invoice.payment_failed, customer.subscription.deleted. Org_id in subscription metadata for tenant lookup.

## Key Files
- /workspace/projects/itp-portal/app/api/webhooks/stripe/route.ts"   --tags="stripe,itp,billing,webhook"   --source="openclaw-session"
```
Writes to: `/Users/mattbender/brain/inbox/YYYY-MM-DD-itp-portal-stripe-billing-setup.md`

### brain-search.sh (retrieve)
```bash
bash /Users/mattbender/brain/scripts/brain-search.sh "stripe webhook"
bash /Users/mattbender/brain/scripts/brain-search.sh "ITP pricing" --dir=openclaw
bash /Users/mattbender/brain/scripts/brain-search.sh "Clerk JWT" --dir=sessions
```

### MEMORY.md update (same response as vault write)
```md
## Recently Saved
- [2026-04-15] Saved to vault: ITP Portal Stripe billing webhook setup → brain/inbox/2026-04-15-itp-portal-stripe-billing-setup.md
```

### Recall Protocol
```
User: "what did I save about X?" OR "what did I tell you about Y?"
→ 1. Check ~/brain/inbox/ by date FIRST (ls -lt ~/brain/inbox/ | head -20)
→ 2. Then brain-search.sh "keyword"
→ 3. THEN check MEMORY.md
→ NEVER start with semantic search for recall questions
```

### Note Formatting Rules
```md
# Note Title

## Summary
[What was learned/decided]

## Key Details
[Bullet points — dense, factual]

## See Also
[[Linked Note]]  ← WikiLinks ONLY here, never inline in body
```

## Vault Structure
```
~/brain/
  inbox/          ← brain-ingest.sh writes here
  sessions/
    openclaw/     ← daily session logs (YYYY-MM-DD.md)
  knowledge/
    memory/
      openclaw-memory.md    ← long-term curated
      openclaw-decisions.md ← key decisions
      openclaw-patterns.md  ← recurring patterns
  Topics/         ← topic-based notes
```

## Gotchas
- No WikiLinks (`[[...]]`) inline in note body — only in `## See Also` section
- Never overwrite existing notes — append only (`>> file` not `> file`)
- Vault write without MEMORY.md update = violation — both must happen in same response
- `brain-ingest.sh` auto-creates the inbox file with proper frontmatter
- For recall: check inbox by date first (sorted by time) — semantic search misses recent items