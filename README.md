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
├── Scrapling/           # Web scraping library
│   ├── SKILL.md
│   ├── reference.md
│   └── examples.md
└── skill-writers/       # Skill creation & optimization
    └── SKILL.md
```

## Skill Overview

| Skill           | Purpose                                        |
| --------------- | ---------------------------------------------- |
| **mwclient**    | Interact with MediaWiki APIs (Wikipedia, etc.) |
| **scrapling**   | Web scraping with anti-bot protection          |
| **skill-writers** | Create, edit, and optimize skills            |

---

## mwclient

A skill family for working with MediaWiki instances like Wikipedia.

**Core concepts:** Site (connection), Page (wiki pages), Image (files), Listings (pagination), Errors (exception handling)

---

## scrapling

A standalone skill for web scraping with multiple fetcher strategies.

| Capability         | Description                                                     |
| ------------------ | --------------------------------------------------------------- |
| **Parsing**        | CSS selectors, XPath, BeautifulSoup-style, text/regex search    |
| **Adaptive**       | Automatically relocates elements when websites change structure |
| **Anti-Detection** | TLS fingerprinting, browser automation, Cloudflare bypass       |
| **Async**          | Concurrent request handling                                     |

### Fetcher Types

| Fetcher           | Best For                    |
| ----------------- | --------------------------- |
| `Fetcher`         | Static HTML, simple sites   |
| `DynamicFetcher`  | JavaScript-rendered content |
| `StealthyFetcher` | Protected sites, Cloudflare |

---

## Skill Invocation

| Skill         | Invocation       | When to use                                               |
| ------------- | ---------------- | --------------------------------------------------------- |
| mwclient      | `/mwclient`      | MediaWiki API operations, installation, common patterns   |
| scrapling     | `/scrapling`     | Web scraping, bypassing anti-bot protection               |
| skill-writers | `/skill-writers` | Create, edit, or optimize skills                          |

## mwclient References

| Reference        | When to use                                               |
| ---------------- | --------------------------------------------------------- |
| [site](.claude/skills/mwclient/references/site.md)       | Connecting to a site, login, auth, session setup          |
| [page](.claude/skills/mwclient/references/page.md)       | Reading & editing pages, get wikitext, save, move, delete |
| [images](.claude/skills/mwclient/references/images.md)   | Images & file uploads, download, get image info           |
| [listing](.claude/skills/mwclient/references/listing.md) | Listings & iterators, categories, search, recent changes  |
| [errors](.claude/skills/mwclient/references/errors.md)   | Error handling, catching and recovering from exceptions   |

---

## skill-writers

A skill for creating new skills and iteratively improving them.

| Capability              | Description                                              |
| ----------------------- | -------------------------------------------------------- |
| **Skill Creation**      | Draft skills from scratch, capture user workflows        |
| **Testing**             | Run evals, benchmark performance, compare iterations     |
| **Optimization**        | Improve descriptions for better triggering accuracy      |
| **Packaging**           | Bundle skills for distribution                           |

### Workflow

1. **Capture Intent** — Understand what the skill should do
2. **Draft** — Write the SKILL.md with frontmatter and instructions
3. **Test** — Run test prompts with and without the skill
4. **Evaluate** — Review outputs, grade assertions, analyze benchmarks
5. **Iterate** — Improve based on feedback and repeat
6. **Optimize** — Tune the description for reliable triggering
