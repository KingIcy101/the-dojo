---
name: pm2-service-stack
description: Manage the full PM2 process stack — naming, ecosystem config, log tailing, and key service IDs.
category: dev
---

# PM2 Service Stack

## When to Use
Starting, stopping, restarting, or debugging any service in Matt's Mac mini PM2 stack. Always check process status after changes.

## Key Services

| ID | Name | Role |
|----|------|------|
| 0 | voice-server | Main ITP Vapi webhook handler |
| 13 | n8n | Workflow automation |
| 17 | mission-control | Internal dashboard (port 7900) |
| 26 | discord-bot | Multi-agent Discord bot |

## Steps

### After Any Code Change
1. `pm2 restart <name>`
2. `pm2 show <name>` — confirm `status: online`
3. `pm2 logs <name> --lines 50` — check for crash/error

## Key Patterns / Code

### Daily Commands
```bash
pm2 list                        # all processes + status
pm2 show voice-server           # detailed info
pm2 logs voice-server --lines 50
pm2 restart voice-server
pm2 stop discord-bot
pm2 start ecosystem.config.js   # start from config
pm2 save                        # persist current list across reboots
pm2 startup                     # generate startup script
```

### ecosystem.config.js Template
```js
module.exports = {
  apps: [
    {
      name: 'voice-server',
      script: 'server.js',
      cwd: '/Users/mattbender/.openclaw/workspace/voice-server',
      env: { NODE_ENV: 'production', PORT: 3001 },
      autorestart: true,
      max_memory_restart: '500M',
      error_file: './logs/err.log',
      out_file: './logs/out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
    },
    {
      name: 'mission-control',
      script: 'server.js',
      cwd: '/Users/mattbender/.openclaw/workspace/mission-control',
      env: { PORT: 7900 },
      autorestart: true,
    },
  ],
};
```

### Log Tailing
```bash
pm2 logs                        # all processes
pm2 logs voice-server           # specific process
pm2 logs voice-server --lines 100 --nocolor  # clean output for parsing
pm2 flush                       # clear all logs
```

### Crash Recovery
```bash
pm2 show voice-server           # check restart count + uptime
# If restart count is high = crash loop
# Fix the code/env issue first, then:
pm2 stop voice-server
# Fix issue
pm2 start voice-server
```

### Naming Convention
- Use kebab-case: `voice-server`, `discord-bot`, `mission-control`
- Agent-specific: `agent-iris`, `agent-echo`, `agent-scribe`
- Tunnels: `cloudflare-tunnel`

## Gotchas
- Always run `pm2 show <name>` after restart — don't assume it's running
- `pm2 save` after adding new processes or they won't survive reboot
- Process IDs can change if stack is fully killed and restarted — use names, not IDs in scripts
- `max_memory_restart` prevents runaway memory leaks — set on long-running servers
- Logs aren't infinite — `pm2 flush` if disk space issues; set `max_size` in logrotate
- `pm2 kill` nukes everything including PM2 daemon — only use for nuclear reset
