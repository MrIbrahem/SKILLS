# Skills Repository

A collection of Claude Code skills for specialized tasks.

## Directory Structure

```
.claude/skills/
├── mwclient/            # MediaWiki API client
│   ├── SKILL.md         # Entry point + routing table
│   └── references/
│       ├── site.md      # Site connection & authentication
│       ├── page.md      # Page operations
│       ├── images.md    # File/image operations
│       ├── listing.md   # Pagination & iteration
│       └── errors.md    # Exception handling
├── scrapling/           # Web scraping library
│   ├── SKILL.md
│   ├── reference.md
│   └── examples.md
└── skill-writers/       # Skill creation & optimization
    └── SKILL.md
```

## Skill Overview

| Skill             | Purpose                                        | Repository                                                |
| ----------------- | ---------------------------------------------- | --------------------------------------------------------- |
| **mwclient**      | Interact with MediaWiki APIs (Wikipedia, etc.) | [mwclient/mwclient](https://github.com/mwclient/mwclient) |
| **scrapling**     | Web scraping with anti-bot protection          | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) |
| **skill-writers** | Create, edit, and optimize skills              | —                                                         |
