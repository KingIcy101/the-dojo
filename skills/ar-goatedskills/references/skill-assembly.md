# Skill Assembly Template for Book-Derived Skills

## Purpose

This file defines how to turn chapter summaries into a final `mo-book-[slug]` skill.
The job is not to dump summaries into a folder. The job is to convert a book into a reusable decision system that an LLM agent can load fast and apply correctly.

A strong book-derived skill has two layers:
1. **Fast-load orchestration** in `SKILL.md`
2. **Deep reference knowledge** in `chapters/*.md`

`SKILL.md` should help the agent act immediately.
The chapter files should hold the dense supporting knowledge.

---

## Assembly Principles

### 1. Optimize for Agent Use, Not Human Reading
The skill should answer:
- When should this knowledge be loaded?
- Which chapter file should the agent read next?
- What are the core frameworks and decision rules from the book?
- What can the agent do with this knowledge right now?

### 2. Keep the Main Skill Lean
`SKILL.md` should stay under 500 lines.
Do not paste entire chapter summaries into `SKILL.md`.
Summarize the book's operating system in the main skill, then route deeper reading into `chapters/`.

### 3. Preserve Named Knowledge Atoms
If the author names a framework, model, law, rule, ladder, pyramid, checklist, or method, preserve it.
Named ideas are the highest-value retrieval handles for future agent use.

### 4. Convert Theory Into Runtime Decisions
Every major idea from the book should be rewritten into one of these forms:
- **Decision rule:** If X, do Y
- **Diagnostic lens:** If problem Z appears, inspect A, B, C
- **Build sequence:** Do 1, then 2, then 3
- **Constraint:** Never do X without Y
- **Tradeoff:** Choose A when speed matters, B when precision matters

---

## Canonical Book Skill Structure

```text
mo-book-[slug]/
├── SKILL.md
├── book-meta.md
└── chapters/
    ├── index.md
    ├── ch-01-[slug].md
    ├── ch-02-[slug].md
    └── ...
```

Optional additions for bigger books:

```text
mo-book-[slug]/
├── references/
│   ├── frameworks-index.md
│   ├── tactics-index.md
│   └── glossary.md
```

Add these only when the book is large enough to justify extra navigation.

---

## What `SKILL.md` Must Contain

### Required Sections

```markdown
---
name: mo-book-[slug]
description: >
  [What the book-based skill does]. Use when the user asks to [trigger 1],
  [trigger 2], or needs help with [domain]. Covers [capabilities].
metadata:
  author: itsAR-VR
  version: 1.0.0
---

# [Book Title] Skill

## What This Skill Is
[2-4 sentences: the central promise of the skill]

## When to Use
- [Trigger pattern 1]
- [Trigger pattern 2]
- [Trigger pattern 3]

## Core Thesis of the Book
[3-6 bullets: the big ideas that organize the whole book]

## Primary Frameworks
| Framework | What it does | Load deeper at |
|-----------|--------------|----------------|
| [Name] | [Purpose] | chapters/ch-03-...md |

## How to Use This Skill at Runtime
1. [First decision the agent should make]
2. [Which chapter files to load based on task type]
3. [How to synthesize the answer]
4. [What not to do]

## Quick Decision Rules
- If [situation], use [framework] from [chapter]
- If [problem], inspect [factors]
- Never [bad pattern] without [required step]

## Chapter Guide
| Situation | Best chapter to load |
|-----------|----------------------|
| [Need] | chapters/ch-02-...md |

## Execution Pattern
[How the agent should apply the book's knowledge in real tasks]

## Quality Bar
- [What a good output from this skill should include]
- [What a bad output misses]

## References
- [chapters/index.md](chapters/index.md)
- [book-meta.md](book-meta.md)
```

---

## Recommended `SKILL.md` Composition

### Section 1: What This Skill Is
State the practical use of the book in plain language.

Example:
- This skill turns a book on email strategy into a reusable operating system for lifecycle, segmentation, deliverability, and campaign decision-making.
- It is not a quote retriever. It is a decision framework and tactic library.

### Section 2: When to Use
Include realistic trigger phrases from Mo's working style.

Examples:
- "build this from the book"
- "what are the key frameworks here"
- "turn this into a skill"
- "use the book to guide the strategy"

### Section 3: Core Thesis of the Book
Do not summarize chapter by chapter here.
Instead, extract the 5 to 10 book-level truths that organize the whole work.

### Section 4: Primary Frameworks
Create a tight table that lets the agent route quickly.

Recommended columns:
- Framework
- Purpose
- Best use case
- Deep file

### Section 5: Runtime Instructions
Teach the agent how to work with the reference files.

Example runtime logic:
1. Identify the task type
2. Load the most relevant chapter file(s)
3. Pull the decision rules and tactics
4. Tailor output to the user's context
5. Keep the answer compact unless depth is requested

### Section 6: Quick Decision Rules
This is the highest-value section after the description.
Compress the book into 10 to 20 rules.
Each rule should help an agent choose an action.

Examples:
- If the user needs diagnosis, load framework chapters before tactic chapters.
- If the book contains a maturity model, first place the user's situation on the model before giving advice.
- If the book distinguishes strategy from execution, keep them separate in the response.

### Section 7: Chapter Guide
This is the navigation table that prevents overloading context.
Use it to tell the agent exactly where to go.

### Section 8: Execution Pattern
Describe how the skill should shape actual outputs.
Examples:
- Start with diagnosis, then apply framework, then give tactics
- Use the author's terminology when it improves clarity
- Prefer the book's named structures over generic advice

### Section 9: Quality Bar
Define what good outputs must contain.
This keeps future runs aligned with the book instead of drifting into generic LLM advice.

---

## Building `chapters/index.md`

The index is the navigation layer.
An agent should often read `chapters/index.md` before opening any specific chapter file.

Use this format:

```markdown
# Chapter Index: [Book Title]

| # | File | Chapter | Priority | Frameworks | Best For |
|---|------|---------|----------|------------|----------|
| 1 | ch-01-...md | [Title] | high | [Framework A] | [Use case] |
| 2 | ch-02-...md | [Title] | medium | [Framework B] | [Use case] |

## Framework Lookup
| Framework | File | Use when |
|-----------|------|----------|
| [Name] | ch-03-...md | [Condition] |

## Situation Lookup
| Situation | Best file |
|-----------|-----------|
| [Need] | ch-02-...md |
| [Need] | ch-05-...md |
```

---

## Single-Skill vs Multi-Skill Split Rules

### Keep as One Skill When
- The book has one coherent domain
- The frameworks build on each other
- The user will likely want the whole book's worldview together

### Split Into Multiple Skills When
- The book covers clearly separable domains
- Different chapters solve unrelated problem types
- Loading the whole skill would waste context repeatedly
- The book naturally decomposes into several operating systems

### Naming for Split Skills
If split is necessary, preserve the `mo-book-` prefix:
- `mo-book-[slug]-strategy`
- `mo-book-[slug]-diagnostics`
- `mo-book-[slug]-tactics`

Do not create unnecessary fragmentation. Default to one strong parent skill unless the split adds real runtime value.

---

## Compression Rules

To retain maximum knowledge while keeping the skill usable:

### Keep
- Named frameworks
- Decision rules
- Checklists
- Sequences
- Constraints
- Tradeoffs
- Diagnostic patterns
- Vocabulary the author uses repeatedly

### Compress Aggressively
- Anecdotes
- Repeated examples
- Long stories that only illustrate a simple point
- Motivational filler
- Redundant case studies

### Preserve as References, Not Main Skill
- Long chapter walkthroughs
- Detailed examples
- Extended comparisons
- Supporting nuance that is useful but not always needed

---

## Final Assembly Checklist

Before calling the skill complete:

### Structure
- [ ] `SKILL.md` exists
- [ ] `book-meta.md` exists
- [ ] `chapters/index.md` exists
- [ ] Every chapter file follows the standard format

### Content
- [ ] Main skill includes the book's core thesis
- [ ] Main skill includes the primary frameworks table
- [ ] Main skill includes runtime usage instructions
- [ ] Main skill includes a chapter guide
- [ ] Main skill includes quick decision rules
- [ ] Named frameworks from the book are preserved
- [ ] Tactics are written as actions, not observations

### Quality
- [ ] No em dashes
- [ ] No brand-specific contamination unless explicitly intended
- [ ] No missing file references
- [ ] Main skill stays under 500 lines
- [ ] The skill is useful even if only `SKILL.md` is loaded

### Deployment
- [ ] Installed locally in `~/.openclaw/skills/`
- [ ] Copied into `/tmp/goatedskills/skills/`
- [ ] Committed and pushed with correct git identity

---

## Rule of Thumb

If an agent loaded only `SKILL.md`, it should still get 70 to 80 percent of the value.
If it then loads the right chapter files, it should reach 95 percent plus of the book's practical knowledge.
