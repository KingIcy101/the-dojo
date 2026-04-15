---
name: tanstack-query
description: >
  TanStack Query (React Query) — data fetching, caching, sync for React.
  Replaces useEffect+fetch patterns. Auto-caching, background refetch, optimistic updates.
  Use in every React/Next.js app alongside Zustand (server state vs UI state).
---

# TanStack Query — Data Fetching & Caching

## Install
```bash
npm install @tanstack/react-query @tanstack/react-query-devtools
```

## Setup
```jsx
// app/providers.tsx
'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,     // 1 min fresh
      gcTime: 5 * 60 * 1000,    // 5 min cache
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

export function Providers({ children }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

## Fetch Data (useQuery)
```js
import { useQuery } from '@tanstack/react-query'

function ClientsList() {
  const { data: clients, isLoading, error, refetch } = useQuery({
    queryKey: ['clients'],   // cache key
    queryFn: () => fetch('/api/clients').then(r => r.json()),
    staleTime: 5 * 60 * 1000, // fresh for 5 min
  })

  if (isLoading) return <Spinner />
  if (error) return <ErrorState message={error.message} />

  return clients.map(c => <ClientCard key={c.id} client={c} />)
}

// With params
const { data } = useQuery({
  queryKey: ['client', clientId],
  queryFn: () => fetch(`/api/clients/${clientId}`).then(r => r.json()),
  enabled: !!clientId,  // only fetch when clientId exists
})
```

## Mutate Data (useMutation)
```js
import { useMutation, useQueryClient } from '@tanstack/react-query'

function AddClientButton() {
  const queryClient = useQueryClient()

  const addClient = useMutation({
    mutationFn: (newClient) =>
      fetch('/api/clients', {
        method: 'POST',
        body: JSON.stringify(newClient),
        headers: { 'Content-Type': 'application/json' }
      }).then(r => r.json()),

    onSuccess: () => {
      // Invalidate + refetch clients list
      queryClient.invalidateQueries({ queryKey: ['clients'] })
    },

    onError: (error) => {
      toast.error(`Failed: ${error.message}`)
    }
  })

  return (
    <button
      onClick={() => addClient.mutate({ name: 'New Client', plan: 'standard' })}
      disabled={addClient.isPending}
    >
      {addClient.isPending ? 'Adding...' : 'Add Client'}
    </button>
  )
}
```

## Optimistic Updates
```js
const updateMrr = useMutation({
  mutationFn: ({ id, mrr }) => fetch(`/api/clients/${id}`, {
    method: 'PATCH', body: JSON.stringify({ mrr })
  }),

  onMutate: async ({ id, mrr }) => {
    // Cancel in-flight queries
    await queryClient.cancelQueries({ queryKey: ['clients'] })
    // Snapshot previous value
    const previous = queryClient.getQueryData(['clients'])
    // Optimistically update UI
    queryClient.setQueryData(['clients'], old =>
      old.map(c => c.id === id ? { ...c, mrr } : c)
    )
    return { previous }
  },

  onError: (err, vars, context) => {
    // Roll back on error
    queryClient.setQueryData(['clients'], context.previous)
  },
})
```

## Parallel Queries
```js
const [clients, metrics, reports] = useQueries({
  queries: [
    { queryKey: ['clients'], queryFn: fetchClients },
    { queryKey: ['metrics'], queryFn: fetchMetrics },
    { queryKey: ['reports'], queryFn: fetchReports },
  ]
})
```

## Zustand + TanStack Query Split
```
TanStack Query → server state (API data, cache, sync)
Zustand        → UI state (sidebar open, theme, modals, user prefs)
Never mix them — keep concerns separate
```

## Skill Injection for Codex/Claude Code
```
Use TanStack Query (@tanstack/react-query) for all server/API data.
Wrap app in QueryClientProvider. useQuery for fetching, useMutation for writes.
queryKey array is the cache key — include all params that affect the data.
invalidateQueries after mutations to keep cache fresh.
Pair with Zustand: TanStack = server state, Zustand = UI state.
```


## Learned from Use (2026-03-22)
SKIP

The session logs contain no mentions of tanstack-query being used, tested, or causing issues. The activity focuses on Vercel deployment, Canvas rendering, Three.js scene building, and UI implementation — none of which reference tanstack-query specifically. There are no corrections, gotchas, or patterns related to this skill in the provided session data.
