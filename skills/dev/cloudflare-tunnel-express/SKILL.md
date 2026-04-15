---
name: cloudflare-tunnel-express
description: Expose a local Express server via Cloudflare tunnel (no account needed) and persist the URL across PM2 restarts.
category: dev
---

# Cloudflare Tunnel + Express

## When to Use
Need a public HTTPS URL for a local Express server (webhooks from Vapi, Fireflies, PandaDoc, etc.) without a static IP or paid ngrok plan.

## Steps

1. Start your Express server on a fixed local port
2. Run `npx cloudflare tunnel --url http://localhost:PORT` via PM2
3. Extract the tunnel URL from PM2 logs using `get-url.sh`
4. Register extracted URL as webhook with external service
5. On restart, re-run `get-url.sh` to get the new URL

## Key Patterns / Code

### Start Tunnel via PM2 (ecosystem.config.js)
```js
{
  name: 'cloudflare-tunnel',
  script: 'npx',
  args: ['cloudflare', 'tunnel', '--url', 'http://localhost:3001'],
  autorestart: true,
  watch: false,
}
```

### get-url.sh — Extract Current Tunnel URL
```bash
#!/bin/bash
# Usage: bash get-url.sh
# Extracts the current cloudflare tunnel URL from PM2 logs

LOG=$(pm2 logs cloudflare-tunnel --lines 100 --nocolor 2>&1)
URL=$(echo "$LOG" | grep -o 'https://[a-zA-Z0-9-]*\.trycloudflare\.com' | tail -1)

if [ -z "$URL" ]; then
  echo "ERROR: No tunnel URL found in PM2 logs"
  exit 1
fi

echo "$URL"
```

### Express Server — Webhook Route
```js
const express = require('express');
const app = express();
app.use(express.json());

app.post('/webhook/vapi', (req, res) => {
  console.log('Vapi event:', req.body.message?.type);
  res.sendStatus(200);
});

app.listen(3001, () => console.log('Server on :3001'));
```

### Register URL with External Service
```bash
TUNNEL_URL=$(bash get-url.sh)
curl -X PATCH https://api.vapi.ai/phone-number/PHONE_ID \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -d "{\"serverUrl\": \"$TUNNEL_URL/webhook/vapi\"}"
```

### Auto-Register on Restart (add to PM2 startup script)
```bash
#!/bin/bash
sleep 5  # wait for tunnel to initialize
TUNNEL_URL=$(bash /path/to/get-url.sh)
# update webhook URL in Vapi / Supabase / wherever
echo "Tunnel URL: $TUNNEL_URL"
```

## Gotchas
- URL changes every restart — must re-register webhooks after any PM2 restart
- Tunnel takes 3-5 seconds to initialize — add `sleep 5` before running get-url.sh
- Free tier has no custom domains — use paid Cloudflare account for stable URL
- `--url` flag is the quick tunnel flag; full tunnel setup requires `cloudflared` binary and config
- PM2 log rotation can purge the URL — increase `max_memory_restart` and log size
- `npx cloudflare` downloads `cloudflared` on first run — may be slow in environments with no cache
- For production webhooks, use a proper static URL (Vercel deployment or paid tunnel)
