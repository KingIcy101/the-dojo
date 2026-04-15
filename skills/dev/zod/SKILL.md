---
name: zod
description: >
  Zod — TypeScript schema validation. Validate API inputs, form data, environment variables.
  Use in every API route and form handler. Prevents bad data from entering the system.
  Stack with React Hook Form for complete form validation.
---

# Zod — Schema Validation

## Install
```bash
npm install zod
```

## Basic Schemas
```js
import { z } from 'zod'

// String
const nameSchema = z.string().min(1).max(100)

// Email
const emailSchema = z.string().email()

// Number
const amountSchema = z.number().min(0).max(100000)

// Enum
const planSchema = z.enum(['standard', 'telehealth', 'exception'])

// Object
const clientSchema = z.object({
  name: z.string().min(1, 'Name required'),
  email: z.string().email('Invalid email'),
  phone: z.string().regex(/^\+1\d{10}$/, 'Must be +1XXXXXXXXXX'),
  plan: z.enum(['standard', 'telehealth']),
  mrr: z.number().min(950).max(2950),
})

// Parse (throws on invalid)
const client = clientSchema.parse(rawData)

// Safe parse (returns { success, data, error })
const result = clientSchema.safeParse(rawData)
if (!result.success) {
  console.log(result.error.issues) // array of validation errors
}
```

## API Route Validation (Next.js)
```js
// app/api/clients/route.ts
import { z } from 'zod'

const createClientSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  plan: z.enum(['standard', 'telehealth']),
  monthlyBudget: z.number().min(950),
})

export async function POST(req: Request) {
  const body = await req.json()
  
  const result = createClientSchema.safeParse(body)
  if (!result.success) {
    return Response.json(
      { error: 'Invalid data', issues: result.error.issues },
      { status: 400 }
    )
  }
  
  const { name, email, plan, monthlyBudget } = result.data
  // Safe to use — guaranteed valid
}
```

## Environment Variable Validation
```js
// lib/env.ts — validate .env at startup
import { z } from 'zod'

const envSchema = z.object({
  SUPABASE_URL: z.string().url(),
  SUPABASE_ANON_KEY: z.string().min(1),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  BLAND_API_KEY: z.string().min(1),
  NODE_ENV: z.enum(['development', 'production', 'test']),
})

export const env = envSchema.parse(process.env)
// App won't start if any required env var is missing/wrong
```

## React Hook Form Integration
```jsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const formSchema = z.object({
  clientName: z.string().min(2, 'At least 2 characters'),
  email: z.string().email('Valid email required'),
  plan: z.enum(['standard', 'telehealth']),
})

type FormData = z.infer<typeof formSchema>

function ClientForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  })
  
  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register('clientName')} />
      {errors.clientName && <span>{errors.clientName.message}</span>}
      
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
    </form>
  )
}
```

## Advanced Patterns
```js
// Optional fields
z.object({ bio: z.string().optional() })

// Default values
z.object({ status: z.string().default('active') })

// Transform (normalize data)
z.string().transform(s => s.toLowerCase().trim())

// Refine (custom validation)
z.object({ password: z.string(), confirmPassword: z.string() })
  .refine(data => data.password === data.confirmPassword, {
    message: 'Passwords must match',
    path: ['confirmPassword'],
  })

// Union (multiple valid types)
z.union([z.string(), z.number()])

// Array
z.array(z.string()).min(1).max(10)

// Nested
const orderSchema = z.object({
  items: z.array(z.object({
    productId: z.string(),
    qty: z.number().int().positive(),
  })),
  total: z.number().positive(),
})
```

## Type Inference (TypeScript)
```ts
const clientSchema = z.object({ name: z.string(), mrr: z.number() })
type Client = z.infer<typeof clientSchema>
// Client = { name: string; mrr: number }
// Single source of truth — schema IS the type
```

## Skill Injection for Codex/Claude Code
```
Use Zod (zod) for all validation. npm install zod.
Every API route: parse request body with schema.safeParse(), return 400 on failure.
Env validation: z.object({...}).parse(process.env) at app startup.
React forms: zodResolver from @hookform/resolvers/zod.
Type inference: type T = z.infer<typeof schema> — schema IS the type definition.
```
