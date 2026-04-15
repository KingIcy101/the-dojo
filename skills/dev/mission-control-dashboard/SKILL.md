---
name: mission-control-dashboard
description: Internal ops dashboard — Express + vanilla JS, PM2 monitoring, Supabase data, Cloudflare tunnel URL, PIN auth.
category: dev
---

# Mission Control Dashboard

## When to Use
Building or modifying the internal ops dashboard that shows PM2 process health, Supabase data, and current Cloudflare tunnel URL. No framework — plain Express + HTML/CSS/JS.

## Config
- **Port:** 7900
- **Auth:** PIN `2146`
- **PM2 ID:** 17 (name: `mission-control`)
- **Static files:** `public/` directory

## Steps

1. Express serves static files from `public/`
2. API routes expose PM2 list, Supabase data, tunnel URL
3. Frontend polls API every 30s and renders
4. PIN check on load — stored in sessionStorage

## Key Patterns / Code

### Express Server
```js
const express = require('express');
const pm2 = require('pm2');
const app = express();

app.use(express.static('public'));
app.use(express.json());

// PIN auth middleware
app.use('/api', (req, res, next) => {
  const pin = req.headers['x-pin'];
  if (pin !== '2146') return res.status(401).json({ error: 'Unauthorized' });
  next();
});

app.get('/api/processes', (req, res) => {
  pm2.connect((err) => {
    if (err) return res.status(500).json({ error: err.message });
    pm2.list((err, list) => {
      pm2.disconnect();
      if (err) return res.status(500).json({ error: err.message });
      const formatted = list.map(p => ({
        id: p.pm_id,
        name: p.name,
        status: p.pm2_env.status,
        restarts: p.pm2_env.restart_time,
        uptime: p.pm2_env.pm_uptime,
        memory: p.monit.memory,
        cpu: p.monit.cpu,
      }));
      res.json(formatted);
    });
  });
});

app.listen(7900, () => console.log('Mission Control on :7900'));
```

### Frontend Poll Pattern (public/app.js)
```js
const PIN = sessionStorage.getItem('pin') || prompt('Enter PIN:');
sessionStorage.setItem('pin', PIN);

async function fetchProcesses() {
  const res = await fetch('/api/processes', { headers: { 'x-pin': PIN } });
  if (res.status === 401) { sessionStorage.clear(); location.reload(); }
  const data = await res.json();
  renderProcesses(data);
}

setInterval(fetchProcesses, 30_000);
fetchProcesses();
```

### Supabase Data Endpoint
```js
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);

app.get('/api/clients', async (req, res) => {
  const { data } = await supabase.from('intake_submissions').select('*').eq('status', 'active');
  res.json(data);
});
```

### Tunnel URL Endpoint
```js
const { execSync } = require('child_process');
app.get('/api/tunnel-url', (req, res) => {
  try {
    const url = execSync('bash /path/to/get-url.sh').toString().trim();
    res.json({ url });
  } catch {
    res.json({ url: null });
  }
});
```

## Gotchas
- `pm2.connect` must always be paired with `pm2.disconnect` — never leave PM2 connection open
- No hot reload — restart PM2 process after server.js changes
- `public/app.js` and `public/style.css` — bump `?v=N` query string in index.html after changes (cache bust)
- PIN in sessionStorage clears on tab close — intentional
- Service role key in server env only — never in public/ JS files
