---
name: supabase-realtime
description: Use when adding live data subscriptions to any app using Supabase — call logs, status updates, notifications.
category: dev
---
# Supabase Realtime

## When to Use
Live updates in Mission Control or client portal — call logs streaming in, status changes, agent activity feeds. Any time polling feels hacky and you need push-based updates.

## Steps
1. Enable Realtime on the table: Supabase Dashboard → Table Editor → select table → toggle Realtime ON
2. Add RLS SELECT policy for the user/role (subscriptions respect RLS)
3. Create channel and subscribe in component
4. Unsubscribe on component unmount to prevent memory leaks

## Key Patterns / Code

```ts
// Basic postgres_changes subscription
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!);

const channel = supabase
  .channel('call-logs-live')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'call_logs' },
    (payload) => {
      if (payload.eventType === 'INSERT') {
        setCallLogs(prev => [payload.new as CallLog, ...prev]);
      }
      if (payload.eventType === 'UPDATE') {
        setCallLogs(prev => prev.map(c => c.id === payload.new.id ? payload.new as CallLog : c));
      }
    }
  )
  .subscribe();

// Cleanup on unmount
return () => { supabase.removeChannel(channel); };
```

```ts
// Filter to specific client — avoid broadcasting all rows
.on('postgres_changes', {
  event: 'INSERT',
  schema: 'public',
  table: 'call_logs',
  filter: `client_id=eq.${clientId}`,  // server-side filter
}, callback)
```

```ts
// React hook pattern
function useRealtimeCallLogs(clientId: string) {
  const [logs, setLogs] = useState<CallLog[]>([]);

  useEffect(() => {
    // Initial load
    supabase.from('call_logs').select('*')
      .eq('client_id', clientId).order('created_at', { ascending: false })
      .then(({ data }) => setLogs(data ?? []));

    // Realtime subscription
    const channel = supabase.channel(`call-logs-${clientId}`)
      .on('postgres_changes', {
        event: 'INSERT', schema: 'public', table: 'call_logs',
        filter: `client_id=eq.${clientId}`,
      }, payload => setLogs(prev => [payload.new as CallLog, ...prev]))
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, [clientId]);

  return logs;
}
```

## Gotchas
- **Realtime toggle must be ON in dashboard** — it's off by default per table
- RLS SELECT policy required — if user can't SELECT the row, they won't receive the event
- `filter` param uses PostgREST syntax: `column=eq.value`, `column=in.(a,b,c)`
- Each client subscription is a WebSocket — don't create channels in render loops
- Channel names must be unique per supabase client instance — use `${table}-${id}` pattern
- `payload.old` is empty on INSERT, `payload.new` is empty on DELETE (unless `REPLICA IDENTITY FULL` is set)
- Supabase project: skmzjnxkoxdogntqbesu (used in Mission Control + client portal)
