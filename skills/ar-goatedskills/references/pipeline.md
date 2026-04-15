# Book-to-Skill Pipeline: Full Detail

## Phase 1: Intake + Structure Mapping

### Tool Call Pattern

```python
# First call: no page range — gets front matter + TOC
pdf(
  pdf="/path/to/book.pdf",
  prompt="Extract the full table of contents with chapter titles, part titles, and page numbers. Also extract: title, author, edition, and the core thesis or premise of this book in 2-3 sentences."
)
```

If TOC not returned clearly on first call, try pages `1-20`:
```python
pdf(
  pdf="/path/to/book.pdf",
  pages="1-20",
  prompt="Extract the complete table of contents with all chapter numbers, titles, and page numbers."
)
```

### What to Capture in book-meta.md

```markdown
# Book Metadata

## Identification
- Title: [full title]
- Subtitle: [if any]
- Author: [full name]
- Edition: [e.g., 3rd Edition]
- Publisher: [if shown]
- Year: [if shown]
- Total pages: [N]
- PDF path: [local path]

## Core Thesis
[2-3 sentences: what is this book fundamentally about?
What is the author's central claim or argument?]

## Who This Book Is For
[The intended audience of the book — affects how we extract + apply knowledge]

## Key Themes
[3-5 bullet themes — the recurring ideas the whole book revolves around]

## Skill Output
- Skill name: mo-book-[slug]
- Skill dir: ~/.openclaw/skills/mo-book-[slug]/
- Repo target: itsAR-VR/goatedskills/skills/mo-book-[slug]/
- Extraction date: [YYYY-MM-DD]

## Chapter Map
| # | Title | Pages | Priority | Status |
|---|-------|-------|----------|--------|
| 1 | ... | 1-25 | high | pending |
| 2 | ... | 26-48 | high | pending |
...
```

Priority guidelines:
- **high** = core argument, frameworks, rules/laws, tactics — must extract
- **medium** = examples, case studies, application — extract if time allows
- **low** = intro, acknowledgements, author bio, index — skim only


---

## Phase 2: Chapter Extraction — Prompt Library

Use these prompt templates for sub-agent chapter extraction tasks.

### Standard Chapter Prompt
```
Using the pdf tool with pages="[X-Y]", read Chapter [N]: "[Chapter Title]" 
from [Book Title] by [Author].

Produce a chapter summary following this exact format:

## Chapter [N]: [Title]
**Pages:** [X-Y]
**Priority:** [high/medium/low]

### Core Argument
[What is the author's main point in this chapter? 2-4 sentences.]

### Key Concepts
[Bulleted list of the most important ideas introduced in this chapter.
Each bullet: concept name in bold + 1-2 sentence explanation.]

### Named Frameworks / Models
[Any framework or model the author names or introduces.
Include: name, definition, components, and how to apply it.]

### Rules / Laws / Principles
[If the author states rules or principles, list every single one verbatim 
or as close to verbatim as possible. These are high-value knowledge atoms.]

### Actionable Tactics
[Specific things a person or business can DO based on this chapter.
Written as directives: "Do X when Y" — not descriptions.]

### Memorable Phrases / Key Language
[Any phrases or language the author uses that are particularly potent.
Not verbatim quotes — synthesized language that captures the idea.]

### How an LLM Agent Should Use This
[2-4 sentences: in what situations should an agent pull from this chapter?
What decisions does this chapter help make?]

Write output to: [skill-dir]/chapters/ch-[NN]-[slug].md
Return: { chapter: "[title]", path: "[path]", word_count: N, 
          frameworks_found: ["..."], status: "complete" }
```

### Synthesis-Mode Prompt (When Verbatim Extraction Is Blocked)
```
I need you to analyze and synthesize the key knowledge from pages [X-Y] of 
[Book Title]. Do not extract verbatim text. Instead:

1. Identify every named framework, model, or system the author introduces
2. List every rule, law, or principle the author states
3. Extract every actionable tactic — specific things readers are told to do
4. Capture the core argument of this section in 2-4 sentences
5. Note any key vocabulary or proprietary terms the author uses

Format your output following the chapter summary template. Focus on 
maximum knowledge density for an LLM agent that will use this to advise 
on [book's topic].
```

### Batch Prompt (Multiple Short Chapters Together)
```
Using the pdf tool with pages="[X-Y]", read Chapters [N], [N+1], and [N+2] 
from [Book Title]. These are shorter chapters covering [topic area].

For EACH chapter separately, produce a chapter summary following the standard 
format. Write each to its own file:
- ch-[NN]-[slug].md
- ch-[NN+1]-[slug].md  
- ch-[NN+2]-[slug].md

Return one object per chapter.
```

### Re-run Prompt (Thin Extract Recovery)
```
The previous extraction of Chapter [N] was too thin — [N] words, missing 
frameworks/tactics. Re-run with pages="[X-Y]" (narrowed range).

This time, prioritize:
- Every framework or named model (even if mentioned briefly)
- Every rule, principle, or recommendation the author makes
- Every concrete tactic, with enough context to apply it

The minimum acceptable output is 400 words with at least 3 actionable tactics.
```

---

## Phase 3: Quality Gate — Evaluation Criteria

Run this check against each chapter file before proceeding to assembly:

### Minimum Thresholds

| Criterion | Minimum | How to check |
|-----------|---------|-------------|
| Word count | 200 words (skim chapters), 400+ (high-priority) | `wc -w ch-XX.md` |
| Sections present | Core Argument, Key Concepts, Actionable Tactics | Grep for headers |
| Frameworks named | 0+ (some chapters have none) | Check "Named Frameworks" section |
| Tactics specificity | At least 3 actionable directives in "do X" form | Manual review |
| LLM-utility section | Present | Grep for "LLM Agent" header |

### Failure Modes and Recovery

| Symptom | Cause | Fix |
|---------|-------|-----|
| File < 200 words | PDF copyright block | Re-run with synthesis-mode prompt |
| No tactics listed | Extraction was too abstract | Re-run emphasizing "specific actions" |
| Only descriptions, no directives | Agent summarized for a human | Re-run with "write for LLM, not human" instruction |
| Missing named frameworks | Skimmed too fast | Re-run that specific chapter alone |
| Files missing entirely | Sub-agent failed silently | Check sub-agent status; re-spawn |

---

## Phase 6: Deployment — Full Commands

### Local Install
```bash
# Create skill dir if it doesn't exist
mkdir -p ~/.openclaw/skills/mo-book-[slug]/chapters

# Copy all files
cp -r /tmp/skill-build/mo-book-[slug]/* ~/.openclaw/skills/mo-book-[slug]/

# Verify
ls -la ~/.openclaw/skills/mo-book-[slug]/
ls -la ~/.openclaw/skills/mo-book-[slug]/chapters/
```

### Repo Push
```bash
cd /tmp/goatedskills

# Pull latest
git pull origin main

# Copy to repo
cp -r ~/.openclaw/skills/mo-book-[slug] skills/

# Stage all
git add skills/mo-book-[slug]

# Commit
git commit -m "feat: add mo-book-[slug]

Book: [Title] by [Author]
Chapters: [N] summary files
Frameworks: [list top 3]
Tactics: [N] actionable tactics extracted"

# Push
git push origin main
```

### Git Identity (Required)
```bash
git config user.email "112514620+itsAR-VR@users.noreply.github.com"
git config user.name "itsAR-VR"
```

Always verify git config is set before committing to goatedskills.
