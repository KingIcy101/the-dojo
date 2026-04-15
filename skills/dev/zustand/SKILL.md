---
name: zustand
description: >
  Zustand — lightweight React state management. 1KB, no boilerplate, no providers.
  Use for global app state in every React/Next.js build — replaces Context API + useReducer.
  Stack with TanStack Query for server state.
---

# Zustand — React State Management

## Install
```bash
npm install zustand
```

## Basic Store
```js
import { create } from 'zustand'

const useStore = create((set, get) => ({
  // State
  user: null,
  theme: 'dark',
  sidebarOpen: true,
  
  // Actions
  setUser: (user) => set({ user }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
  
  // Computed via get()
  isAdmin: () => get().user?.role === 'admin',
}))

// Use in any component — no provider needed
function Header() {
  const { user, sidebarOpen, toggleSidebar } = useStore()
  return <button onClick={toggleSidebar}>{sidebarOpen ? 'Close' : 'Open'}</button>
}
```

## Async Actions (API calls)
```js
const useClientStore = create((set) => ({
  clients: [],
  loading: false,
  error: null,
  
  fetchClients: async () => {
    set({ loading: true, error: null })
    try {
      const res = await fetch('/api/clients')
      const clients = await res.json()
      set({ clients, loading: false })
    } catch (err) {
      set({ error: err.message, loading: false })
    }
  },
  
  addClient: (client) => set((state) => ({
    clients: [...state.clients, client]
  })),
  
  updateClient: (id, updates) => set((state) => ({
    clients: state.clients.map(c => c.id === id ? { ...c, ...updates } : c)
  })),
  
  removeClient: (id) => set((state) => ({
    clients: state.clients.filter(c => c.id !== id)
  })),
}))
```

## Persist to localStorage
```js
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useSettingsStore = create(
  persist(
    (set) => ({
      theme: 'dark',
      calendarView: 'week',
      setTheme: (theme) => set({ theme }),
      setCalendarView: (view) => set({ calendarView: view }),
    }),
    { name: 'halo-settings' } // localStorage key
  )
)
```

## Devtools (debug in browser)
```js
import { devtools } from 'zustand/middleware'

const useStore = create(devtools((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 }), false, 'increment'),
})))
```

## Split Stores by Domain
```js
// stores/useAuthStore.js — user/session
// stores/useUIStore.js — sidebar, modals, theme
// stores/useClientStore.js — Halo clients data
// stores/useCalendarStore.js — calendar events

// Combine in component
function Dashboard() {
  const user = useAuthStore((state) => state.user)
  const clients = useClientStore((state) => state.clients)
  const theme = useUIStore((state) => state.theme)
}
```

## Zustand vs Context API
```
Context API: re-renders all consumers on any change → perf issues at scale
Zustand: selective subscriptions → only re-renders what changed
Zustand: no Provider wrapper needed → cleaner tree
Zustand: devtools, persist, immer all built-in
```

## Skill Injection for Codex/Claude Code
```
Use Zustand (zustand) for all React global state. npm install zustand.
create() returns a hook — no providers needed.
Persist with persist middleware for settings/preferences.
Split stores by domain: useAuthStore, useUIStore, useDataStore.
Selector pattern: useStore((state) => state.value) prevents unnecessary re-renders.
```


## Learned from Use (2026-03-22)
SKIP

The session logs provided contain no mentions of the "zustand" skill being used, tested, or corrected. The activity centers on Vercel deployments, Agent Lounge frontend rendering, Forge build issues, and Obsidian syncing—none of which involve zustand (a state management library).

To extract learned lessons about zustand usage, I would need session logs that actually document:
- Zustand store implementations or modifications
- State management decisions or failures
- Corrections related to zustand patterns or syntax

Without zustand-specific activity in these logs, there are no actionable lessons to extract.
