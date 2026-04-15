---
name: shadcn
description: >
  shadcn/ui — copy-paste component library built on Radix UI + Tailwind. The base layer
  that Aceternity UI and Magic UI build on top of. Use for forms, dialogs, dropdowns,
  toasts, tables, and all standard UI primitives.
---

# shadcn/ui — Component Primitives

## What It Is
shadcn/ui is NOT a package — it's a CLI that copies components directly into your codebase. You own the code. Built on Radix UI (accessible headless) + Tailwind CSS. The foundation everything else builds on.

## Init
```bash
npx shadcn@latest init
# Installs Tailwind, Radix primitives, utility functions
# Creates components/ui/ directory
```

## Add Components
```bash
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add form
npx shadcn@latest add table
npx shadcn@latest add toast
npx shadcn@latest add dropdown-menu
npx shadcn@latest add command  # command palette (Cmd+K)
npx shadcn@latest add calendar
npx shadcn@latest add data-table
```

## Core Components We Use

### Button
```jsx
import { Button } from '@/components/ui/button'

<Button>Primary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Delete</Button>
<Button size="sm">Small</Button>
<Button disabled>Loading...</Button>
```

### Dialog / Modal
```jsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'

<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent className="bg-[#12121e] border-white/10">
    <DialogHeader>
      <DialogTitle>Add Client</DialogTitle>
    </DialogHeader>
    {/* form content */}
  </DialogContent>
</Dialog>
```

### Toast (Notifications)
```jsx
import { useToast } from '@/components/ui/use-toast'
import { Toaster } from '@/components/ui/toaster'

// In layout: <Toaster />

function MyComponent() {
  const { toast } = useToast()
  const handleSuccess = () => {
    toast({
      title: 'Client added',
      description: 'Dr. Pierce has been added to the pipeline.',
    })
  }
}
```

### Form (with React Hook Form + Zod)
```jsx
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

const form = useForm({ resolver: zodResolver(clientSchema) })

<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)}>
    <FormField control={form.control} name="email"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Email</FormLabel>
          <FormControl>
            <Input placeholder="client@example.com" {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  </form>
</Form>
```

### Command Palette (Cmd+K)
```jsx
import { CommandDialog, CommandInput, CommandList, CommandItem } from '@/components/ui/command'

<CommandDialog open={open} onOpenChange={setOpen}>
  <CommandInput placeholder="Search clients, commands..." />
  <CommandList>
    <CommandItem onSelect={() => navigate('/clients')}>Clients</CommandItem>
    <CommandItem onSelect={() => navigate('/calendar')}>Calendar</CommandItem>
  </CommandList>
</CommandDialog>
```

### Data Table (with TanStack Table)
```bash
npx shadcn@latest add table
npm install @tanstack/react-table
```
```jsx
// Full sortable, filterable, paginated table
// See shadcn.com/docs/components/data-table for full example
```

## Dark Theme Config
```js
// components.json (created by init)
{
  "style": "default",
  "tailwind": {
    "cssVariables": true,
    "baseColor": "slate"
  },
  "rsc": true
}

// globals.css — override with our dark theme
.dark {
  --background: 10 10 15;
  --foreground: 232 232 240;
  --card: 18 18 30;
  --primary: 99 102 241;
  --border: 255 255 255 / 0.06;
  --ring: 99 102 241;
}
```

## Skill Injection for Codex/Claude Code
```
shadcn/ui is the component base. Init: npx shadcn@latest init.
Add components: npx shadcn@latest add [component].
Key: button, dialog, form, toast, command, dropdown-menu, data-table.
Integrates with React Hook Form + Zod (Form component).
Override dark theme via CSS variables in globals.css.
Aceternity UI and Magic UI build on top of shadcn primitives.
```


## Learned In Use

- **2026-03-21:** Physical file copying of skills (including ui-ux-pro-max) across agent workspaces is more reliable than symlinking — symlinks don't properly resolve in all tool contexts.

## Learned from Use (2026-03-22)
SKIP

The session logs contain no meaningful usage of the "shadcn" skill. The mentions are tangential (Agent Lounge UI built with Forge, CSS/HTML bugs, canvas rendering issues) but do not document:
- Specific shadcn component decisions or implementation patterns
- Corrections related to shadcn usage
- Design system or theming lessons with shadcn
- Problems solved or avoided using shadcn

The corrections logged are about image reading, Codex briefing process, and deployment workflows — none tied to shadcn skill application.


## Learned from Use (2026-03-29)
## Learned from Use (2026-03-29)

- **Font size violations in shadcn components require explicit minimum enforcement**: Judge caught multiple 12px typography issues across outcome-badge.tsx, calls-bar-chart.tsx, and dashboard-chart.tsx. Grep verification of all components was necessary to prevent redeployment cycles — establish 13px minimum as non-negotiable in component specs before Forge builds.

- **Clerk's dark theme bleeds into shadcn sign-in UI without explicit `appearance` prop override**: The ClerkProvider dark theme setting cascaded into the sign-in component, requiring a targeted `appearance` prop fix. Document this as a required override when using ClerkProvider in production portals.

- **Empty states and component composition need Judge audit before deployment**: Multiple rounds were needed because empty states weren't updated alongside feature additions, and Vapi integration wiring was incomplete. shadcn components work but the system design around them (error states, loading states) must be audited as a unit with the dev pipeline — never assume visual components are "done" until Judge verifies rendered output in a real session.
