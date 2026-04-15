---
name: pm2-ecosystem-config
description: Use when managing, restarting, or adding services to the PM2 process stack on Matt's Mac mini.
category: dev
---
# PM2 Ecosystem Config

## When to Use
Any time you need to restart a service, add a new process, check logs, or configure the process stack. Always verify online status after restart.

## Steps
1. Syntax check any JS before restarting: `node --check server.js`
2. Restart: `pm2 restart <name>`
3. Verify online: `pm2 show <name>` — confirm status is `online`
4. Check logs: `pm2 logs <name> --lines 50`
5. After adding new process: `pm2 save`

## Key Patterns / Code

```bash
# Safety flow before any restart
node --check server.js && pm2 restart voice-server && sleep 3 && pm2 show voice-server
```

```bash
# Core commands
pm2 list                          # all processes + status
pm2 show voice-server             # full details — check status field
pm2 restart voice-server          # restart by name
pm2 logs voice-server --lines 50  # recent logs
pm2 save                          # persist process list across reboots
pm2 startup                       # generate startup script (run once on new machine)
```

```js
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'voice-server',
      script: './server.js',
      cwd: '/Users/mattbender/workspace/voice-server',
      env: { NODE_ENV: 'production', PORT: 3001 },
      watch: false,           // NEVER true in production
      max_memory_restart: '500M',
      error_file: './logs/err.log',
      out_file: './logs/out.log',
    },
    {
      name: 'mission-control',
      script: 'npm',
      args: 'start',
      cwd: '/Users/mattbender/workspace/mission-control',
      env: { NODE_ENV: 'production', PORT: 3002 },
      watch: false,
    },
  ],
};
```

```bash
# Log rotation (install once)
pm2 install pm2-logrotate
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

## Service Registry
| Name | ID | Port | Notes |
|------|----|------|-------|
| voice-server | 0 | 3001 | Vapi webhook handler |
| mission-control | 17 | 3002 | Internal dashboard |
| discord-bot | 26 | — | OpenClaw Discord bot |
| n8n | 13 | 5678 | Automation platform |
| pixel-cron | — | — | BROKEN — keep stopped |

## Gotchas
- `pixel-cron` is broken — do NOT restart it, leave stopped
- Always `pm2 show <name>` after restart — process can appear in list but be in `errored` state
- Watch mode (`watch: true`) causes restart loops in prod — never enable
- `pm2 save` is required after adding new apps or they won't survive reboot
- Node syntax errors crash immediately — always `node --check` before restart
- `pm2 kill` kills the daemon entirely — use `pm2 stop all` for graceful stop
- Logs are at `~/.pm2/logs/` if no custom log path set in config
