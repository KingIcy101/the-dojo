---
name: vercel-deploy-patterns
description: Deploy Next.js apps to Vercel via CLI or deploy hooks, manage env vars, and debug build failures.
category: dev
---

# Vercel Deployment Patterns

## When to Use
Deploying any Next.js/frontend app to production. Use CLI for one-off deploys, deploy hooks for CI/automation.
GitHub auto-deploy requires dashboard linking — the API doesn't support it.

## Steps

### One-off Deploy (CLI)
```bash
npm i -g vercel
vercel --prod --yes --token $VERCEL_TOKEN
```

### CI/GitHub Actions Deploy
```yaml
- name: Deploy to Vercel
  run: vercel --prod --yes --token ${{ secrets.VERCEL_TOKEN }}
  env:
    VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
    VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

### Deploy Hooks (trigger without auth)
1. Vercel Dashboard → Project → Settings → Git → Deploy Hooks
2. Create hook → copy URL (contains secret)
3. Trigger: `curl -X POST https://api.vercel.com/v1/integrations/deploy/prj_xxx/yyy`
4. Store in .env as `VERCEL_DEPLOY_HOOK_URL` — POST to it from n8n, cron, etc.

## Key Patterns / Code

### Add Env Vars via CLI
```bash
# Add to production
echo "my-value" | vercel env add MY_SECRET production

# Add to all environments
vercel env add MY_SECRET production preview development

# Pull all env vars to local .env.local
vercel env pull .env.local
```

### Get Project/Org IDs
```bash
vercel link  # creates .vercel/project.json with projectId and orgId
cat .vercel/project.json
```

### Check Build Logs Before Deploying
```bash
vercel build --debug  # local build with verbose output
# Common env var errors: "Variable X is not defined" → add via CLI before deploy
```

### List Deployments
```bash
vercel ls           # recent deployments
vercel inspect URL  # deployment details
```

### Rollback
```bash
vercel rollback [deployment-url]  # instantly promote previous deployment
```

### Team vs Personal Token
- Personal token: works for personal projects
- Team token: `vercel --token $TEAM_TOKEN --scope team-slug`
- Tokens: vercel.com/account/tokens

### Custom Domain
```bash
vercel domains add inthepast.ai
vercel alias set deployment-url.vercel.app inthepast.ai
```

## Gotchas
- GitHub auto-deploy (on push) requires linking in the dashboard — not available via API or CLI alone
- `vercel --prod` without `--yes` prompts interactively — always add `--yes` in automation
- `.vercelignore` works like `.gitignore` — use it to skip large folders (e.g. `node_modules`, `.next/cache`)
- Build errors about missing env vars: run `vercel env pull` locally to debug
- Preview deploys get unique URLs — great for Judge to audit before production
- Edge functions have 1MB size limit — don't bundle heavy libs