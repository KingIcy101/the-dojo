# Chapter Summary Format

## Purpose

Chapter summary files are the primary knowledge storage for book-derived skills.
They are written for LLM agents to load and apply — not for humans to read.

Write as if you are handing a fully briefed expert to the agent.
Dense. Precise. Action-oriented. Zero filler.

---

## Standard Chapter Summary Template

```markdown
# Chapter [N]: [Full Chapter Title]

**Book:** [Book Title] by [Author]
**Pages:** [X-Y]
**Priority:** [high | medium | low]
**Extraction date:** [YYYY-MM-DD]

---

## Core Argument

[What is the central point of this chapter? 2-4 sentences. State it as a claim, not a description.
Wrong: "This chapter discusses email frequency."
Right: "Sending frequency must be determined by subscriber engagement tier, not a fixed calendar schedule.
       Active subscribers can absorb daily sends; cold subscribers should be suppressed from campaigns entirely."]

---

## Key Concepts

**[Concept Name]**
[1-2 sentences defining it precisely. What is it? Why does it matter?]

**[Concept Name]**
[1-2 sentences.]

[Continue for every significant concept introduced in the chapter]

---

## Named Frameworks and Models

### [Framework Name]
**What it is:** [1-sentence definition]
**Components:**
- [Component 1]: [what it means]
- [Component 2]: [what it means]
- [Component 3]: [what it means]

**How to apply it:**
[Step-by-step or conditions for applying this framework. Be specific.]

**When to use it:**
[What business situation calls for this framework?]

---

### [Second Framework Name if present]
[Same structure]

---

## Rules / Laws / Principles

[If the author states numbered or named rules, list every single one.
Format each as a directive the agent can apply.]

- **Rule [N]:** [Statement of the rule] — [Brief implication or application context]
- **Rule [N]:** [Statement]
...

[If the chapter has no named rules, write "No explicit rules stated. See Actionable Tactics."]

---

## Actionable Tactics

[Specific, concrete things to DO. Written as directives: "Do X when Y" or "Always X before Y."
Not descriptions. Not observations. Actions.]

1. **[Tactic name or short label]**
   [Do X. When Y happens, the outcome is Z.]

2. **[Tactic name]**
   [Specific action + specific condition + expected outcome]

3. [Continue — aim for 5-10 tactics per high-priority chapter]

---

## Key Distinctions / Watch-Outs

[Common mistakes, false assumptions, or things the author explicitly warns against.
Format: "Not X — instead Y" or "The mistake most people make is X. The correct approach is Y."]

- [Distinction 1]
- [Distinction 2]

---

## Memorable Language / Key Terminology

[Phrases or vocabulary the author uses that are important to know.
These may be used in the author's other work or in the industry.
Do not quote verbatim — synthesize the language.]

- **[Term]:** [What it means in the context of this book]
- **[Term]:** [Definition]

---

## Cross-Chapter Connections

[Does this chapter reference ideas from other chapters? 
Does it build on or contradict something from earlier?
List connections briefly so agents can find related knowledge.]

- Builds on: Chapter [N] — [short description of connection]
- Referenced in: Chapter [N] — [short description]
- Contrasts with: [If applicable]

---

## How an LLM Agent Should Use This Chapter

[2-5 sentences. Explicit: in what situations should an agent pull knowledge from this specific chapter?
What decisions does this chapter help make? What questions does it answer?]

Example: "Load this chapter when: (1) building an email frequency policy, (2) diagnosing rising unsubscribe rates, 
(3) designing send suppression logic. The key decision this chapter informs: who to suppress and when."
```

---

## Completeness Checklist

Before finalizing any chapter file:

- [ ] Core Argument states a claim (not just a description)
- [ ] Every named framework has all components listed
- [ ] Rules are stated as directives, not descriptions
- [ ] Tactics are actionable ("Do X") not observational ("The author suggests X")
- [ ] Key distinctions capture what NOT to do (often most valuable)
- [ ] "How an LLM Agent Should Use This" is explicit about when to load this file
- [ ] Word count is 300+ for high-priority chapters
- [ ] File is saved to: `chapters/ch-[NN]-[chapter-slug].md`

---

## Chapter Index File Format

After all chapter files are written, create `chapters/index.md`:

```markdown
# Chapter Index: [Book Title]

| # | File | Chapter Title | Priority | Key Frameworks | Word Count |
|---|------|---------------|----------|---------------|------------|
| 1 | ch-01-[slug].md | [Title] | high | [Framework A, B] | [N] |
| 2 | ch-02-[slug].md | [Title] | high | [Framework C] | [N] |
| 3 | ch-03-[slug].md | [Title] | medium | none | [N] |
...

## Quick Framework Lookup

| Framework name | Chapter | File |
|---------------|---------|------|
| [Framework A] | Ch. 1 | ch-01.md |
| [Framework B] | Ch. 3 | ch-03.md |

## Quick Tactic Lookup

| Situation | Best chapter to load |
|-----------|---------------------|
| [Situation 1] | ch-02.md |
| [Situation 2] | ch-05.md |
```

The index file is the navigator. An agent can load the index to find which chapter file to load next, rather than loading all chapters at once.

---

## Writing Style for Chapter Files

**Do:**
- Write in second person for tactics: "Segment your list by..." / "Run the test for..."
- Use tables to organize rules, comparisons, or multi-column data
- Bold every named framework, concept, and rule on first use
- End each tactic with the expected outcome

**Do not:**
- Use em dashes
- Write passive voice ("it is suggested that...")
- Summarize for a human reader (no "the author argues that...")
- Add filler phrases ("This is an important concept because...")
- Leave vague phrases like "depending on context" without specifying what context
