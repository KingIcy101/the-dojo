---
name: github-actions
description: >
  GitHub Actions — CI/CD pipeline. Auto-deploy on push, run tests, lint, type-check.
  Use for all production apps — test before deploy, never ship broken code.
---

# GitHub Actions — CI/CD

## Basic Deploy Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install
        run: npm ci

      - name: Type Check
        run: npm run type-check

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm run test

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

## Preview on PR
```yaml
# .github/workflows/preview.yml
name: Preview Deployment

on:
  pull_request:
    branches: [main]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run build

      - name: Deploy Preview
        uses: amondnet/vercel-action@v25
        id: deploy
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

      - name: Comment Preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚀 Preview: ${{ steps.deploy.outputs.preview-url }}'
            })
```

## Run Playwright Tests in CI
```yaml
- name: Install Playwright
  run: npx playwright install --with-deps chromium

- name: Run E2E Tests
  run: npx playwright test
  env:
    BASE_URL: ${{ steps.deploy.outputs.preview-url }}

- name: Upload Test Results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: playwright-results
    path: playwright-report/
```

## Environment Secrets
```
# Add in GitHub: Settings → Secrets → Actions
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID
SUPABASE_URL
SUPABASE_SERVICE_KEY
STRIPE_SECRET_KEY
```

## Skill Injection for Codex/Claude Code
```
GitHub Actions CI/CD in .github/workflows/. Trigger on push to main.
Steps: checkout → setup-node → npm ci → type-check → lint → test → deploy.
Use amondnet/vercel-action for Vercel deployments.
Secrets via ${{ secrets.SECRET_NAME }} — never hardcode in YAML.
Run Playwright E2E on every PR before merging.
```


## Learned In Use

- **2026-03-20:** brain-ingest.sh sync scripts require explicit `exit 0` at the end to prevent early termination bugs that stop mid-execution; missing exit causes half the files to fail syncing.

## Learned from Use (2026-03-22)
SKIP

The session logs contain no meaningful usage of the "github-actions" skill itself. The mentions are entirely about Vercel deployments, SSO configuration, and manual deployment workflows. There are no GitHub Actions workflows being written, debugged, configured, or discussed—only Vercel CLI commands (`--prod` flag) and direct platform deployments. No corrections were made related to GitHub Actions usage, and no patterns emerged about how this skill was applied or should be applied differently.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Pipeline verification before deployment is non-negotiable** — Forge completed builds that appeared ready, but skipping Pixel review and Judge audit exposed font violations, unwired APIs, and security gaps. GitHub Actions CI must include automated font-size linting (min 13px) to catch violations before human review.

- **grep verification for codebase-wide fixes works at scale** — After fixing typography, `grep` confirmed all remaining 12px instances were eliminated across components. Use grep post-fix to validate consistency before redeployment rather than relying on spot-checks.

- **Vercel deployments need pre-flight checks for Clerk theme props** — Dark theme from ClerkProvider was bleeding into sign-in UI and required `appearance` prop override. GitHub Actions should validate Clerk provider config matches environment before deploy to catch theme inheritance issues early.
