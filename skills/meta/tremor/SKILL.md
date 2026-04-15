---
name: tremor
description: >
  Tremor — copy-paste React chart and dashboard components. Built on Recharts + Tailwind + Radix UI.
  Acquired by Vercel. Use for all data visualization — line charts, bar charts, donuts, area charts, KPI cards.
  The fastest way to add beautiful charts to any React/Next.js dashboard.
---

# Tremor — Dashboard Charts & Components

## Install
```bash
npm install @tremor/react
```

## Setup (Tailwind config)
```js
// tailwind.config.js
module.exports = {
  content: [
    './node_modules/@tremor/**/*.{js,ts,jsx,tsx}',
    // ... your files
  ],
}
```

## Core Components

### KPI Cards (Most Used)
```jsx
import { Card, Metric, Text, Flex, BadgeDelta } from '@tremor/react'

<Card>
  <Text>MRR</Text>
  <Metric>$1,900</Metric>
  <Flex>
    <Text>vs last month</Text>
    <BadgeDelta deltaType="increase">+$950</BadgeDelta>
  </Flex>
</Card>
```

### Line Chart
```jsx
import { LineChart } from '@tremor/react'

const data = [
  { date: 'Jan', Leads: 23, Spend: 1950 },
  { date: 'Feb', Leads: 47, Spend: 1950 },
  { date: 'Mar', Leads: 61, Spend: 1950 },
]

<LineChart
  data={data}
  index="date"
  categories={['Leads', 'Spend']}
  colors={['indigo', 'rose']}
  valueFormatter={(v) => `$${v.toLocaleString()}`}
  className="h-72 mt-4"
/>
```

### Bar Chart
```jsx
import { BarChart } from '@tremor/react'

<BarChart
  data={data}
  index="month"
  categories={['Revenue']}
  colors={['indigo']}
  valueFormatter={(v) => `$${v.toLocaleString()}`}
  className="h-64"
/>
```

### Donut / Pie Chart
```jsx
import { DonutChart, Legend } from '@tremor/react'

const breakdown = [
  { name: 'Facebook Ads', value: 65 },
  { name: 'Google Ads', value: 25 },
  { name: 'Organic', value: 10 },
]

<DonutChart
  data={breakdown}
  category="value"
  index="name"
  colors={['indigo', 'violet', 'slate']}
  className="h-40"
/>
<Legend categories={['Facebook Ads', 'Google Ads', 'Organic']} colors={['indigo', 'violet', 'slate']} />
```

### Area Chart (Trend Over Time)
```jsx
import { AreaChart } from '@tremor/react'

<AreaChart
  data={data}
  index="date"
  categories={['Leads']}
  colors={['indigo']}
  className="h-72"
/>
```

### Spark Chart (Mini Inline Trend)
```jsx
import { SparkAreaChart } from '@tremor/react'

// Inline inside a KPI card
<SparkAreaChart
  data={sparkData}
  categories={['value']}
  index="date"
  colors={['indigo']}
  className="h-10 w-24"
/>
```

### Progress Bar
```jsx
import { ProgressBar } from '@tremor/react'

<ProgressBar value={66} color="indigo" className="mt-2" />
// 66% toward $300K goal
```

### Tracker (Status Over Time)
```jsx
import { Tracker } from '@tremor/react'

// Good for: client health, uptime, campaign status
const statusData = [
  { color: 'emerald', tooltip: 'Active' },
  { color: 'emerald', tooltip: 'Active' },
  { color: 'yellow', tooltip: 'Warning' },
  { color: 'rose', tooltip: 'Issue' },
]

<Tracker data={statusData} className="mt-2" />
```

## Dark Theme Override
```css
/* Tremor uses CSS variables — override for dark */
:root {
  --tremor-brand: 99 102 241;  /* indigo */
  --tremor-background-default: 18 18 30;
  --tremor-background-subtle: 15 15 26;
  --tremor-border-default: 255 255 255 / 0.06;
}
```

## Best Use Cases for Our Builds
- **Mission Control** — MRR, lead count, spend trends
- **Client portals** — campaign performance charts
- **Sellerboard dashboard** — Amazon/Walmart sales trends
- **Halo analytics** — leads per client, CPL over time

## Skill Injection for Codex/Claude Code
```
Use Tremor (@tremor/react) for all charts and KPI cards.
LineChart for trends, BarChart for comparisons, DonutChart for breakdowns, SparkAreaChart inline KPIs.
BadgeDelta for trend indicators (increase/decrease/unchanged).
Add to tailwind.config content array. Dark theme via CSS variable overrides.
```


## Learned from Use (2026-03-22)
SKIP

The session logs provided contain no mentions of the "tremor" skill being used. The logs document deployment issues, UI rendering problems, and task management around the Agent Lounge project, but do not reference or demonstrate any use of a "tremor" skill. Without evidence of tremor being employed in these sessions, I cannot extract genuine, specific lessons about its usage.
