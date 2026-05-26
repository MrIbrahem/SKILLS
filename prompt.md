## Improved Prompt

You are an expert AI coding assistant and technical documentation engineer.

Your task is to analyze the `mwclient` Python library and create a complete Claude Code Skill for it.

## Source Material

Analyze and extract patterns, APIs, workflows, and best practices from:

-   Real `mwclient` source code located at:
-   `mwclient_skills/code`
-   DeepWiki documentation located at:
-   `mwclient_skills/deepWiki`

Also use the existing Claude Skill authoring standard found at:

-   `.claude/skills/skill-writers/SKILL.md`

Follow its structure, conventions, tone, formatting, and best practices precisely.

---

# Objective

Create a new Claude Code Skill at:

`.claude/skills/mwclient`

The skill should help Claude effectively use and reason about the `mwclient` library for MediaWiki automation and integrations.

---

# Deliverables

Create the following structure:

```text
.claude/skills/mwclient/
├── SKILL.md
├── references/
└── skills/
```

---

# Requirements

## 1. SKILL.md

Generate a production-quality Claude Skill specification including:

-   Purpose and scope
-   Core capabilities
-   Common usage workflows
-   Recommended coding patterns
-   Important API abstractions
-   Authentication and session handling
-   Editing and page operations
-   Error handling strategies
-   Pagination and querying patterns
-   Best practices
-   Anti-patterns
-   Example prompts/tasks Claude should handle
-   Tool usage guidance
-   References to subskills and supporting docs

The document should:

-   Be concise but comprehensive
-   Be optimized for Claude Code usage
-   Include practical examples
-   Use structured Markdown
-   Follow the conventions from `.claude/skills/skill-writers/SKILL.md`

---

## 2. references/

Create supporting reference documentation extracted and synthesized from the source code and DeepWiki docs.

Include:

-   API summaries
-   Important classes/functions
-   Common patterns
-   Authentication examples
-   Editing examples
-   Query examples
-   Error/reference tables
-   Useful implementation notes

Prefer distilled, developer-friendly references instead of raw copied documentation.

---

## 3. skills/

Create modular subskills for specialized tasks where appropriate.

Examples may include:

-   authentication
-   page-editing
-   querying-pages
-   uploading-files
-   category-management
-   template-operations
-   error-handling

Each subskill should:

-   Have a focused responsibility
-   Include examples
-   Define recommended workflows
-   Be reusable by Claude Code

---

# Analysis Instructions

Before writing files:

1. Analyze the actual `mwclient` implementation patterns
2. Identify the most important APIs and workflows
3. Infer practical developer usage patterns
4. Compare implementation details with DeepWiki explanations
5. Prioritize actionable coding guidance over theoretical summaries

---

# Output Format

Output:

1. Proposed directory tree
2. Full contents of each generated file
3. Clear Markdown formatting
4. Ready-to-save content

Do not provide high-level commentary only — generate the actual skill content.
