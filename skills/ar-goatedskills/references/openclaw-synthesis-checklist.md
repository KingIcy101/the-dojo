# OpenClaw Guide Synthesis Reference

## Source Priorities (highest → lowest)
1. Verified runtime artifacts and outputs (`openclaw status`, `openclaw security audit --deep`, successful setup logs)
2. Primary docs in this repo / playbooks
3. Synthesized thread digest (`OPENCLAW_THREADS_DIGEST.md`)
4. User’s direct notes and decisions

## Source Ingestion Format
For each source, capture:
- Source type (tweet/thread/playbook/command output)
- Timestamp or commit
- Key claim(s)
- Concrete action(s)
- Confidence score

## Evidence Template
- Claim: “Set groupPolicy to allowlist.”
- Evidence: security audit warning + config change output
- Confidence: high
- Action: apply config, validate with rerun

## OpenClaw Setup Research Matrix
| Area | What to confirm | Primary source | Default value |
|---|---|---|---|
| Identity | SOUL/IDENTITY loaded | memory + docs | SOUL.md + USER.md |
| Security | Telegram allowlist | security audit output | allowlist with AR/Mo only |
| Drive | OAuth and MCP auth | upload pipeline + folder IDs | token + script sync |
| Workflow | Start-up scripts and cron | WORKFLOW_AUTO (or fallback from memory) | fixed morning run |
| Ops visibility | Cron + heartbeat | cron list + run results | daily heartbeat + run status |

## Quality Rubric
- **Accuracy (0-4):** each statement matched to source
- **Completeness (0-4):** required sections present
- **Usability (0-4):** first action within 10 minutes
- **Safety (0-4):** risk + rollback covered

## Suggested Outputs
- `OpenClaw Guide vX.Y.md`
- `OpenClaw Security Hardening.md`
- `Daily Operating Runbook.md`
- `Guide Change Log.md` with version + source deltas
