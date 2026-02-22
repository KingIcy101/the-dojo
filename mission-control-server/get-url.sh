#!/bin/bash
# Gets the current Mission Control public URL from the tunnel log
URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' \
  /Users/mattbender/.openclaw/workspace/mission-control-server/tunnel.log \
  | tail -1)

if [ -n "$URL" ]; then
  echo "$URL" > /Users/mattbender/.openclaw/workspace/mission-control-server/mc-url.txt
  echo "✅ Mission Control: $URL"
else
  echo "⚠️  Tunnel URL not found yet — try again in a few seconds"
fi
