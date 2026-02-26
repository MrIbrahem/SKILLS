# Skills Repository

A collection of Claude Code skills for specialized tasks.

## Directory Structure

```
.claude/skills/
├── mwclient/            # MediaWiki API client (parent skill)
│   └── SKILL.md
├── mwclient-site/       # Site connection & authentication
│   └── SKILL.md
├── mwclient-page/       # Page operations
│   └── SKILL.md
├── mwclient-images/     # File/image operations
│   └── SKILL.md
├── mwclient-listing/    # Pagination & iteration
│   └── SKILL.md
├── mwclient-errors/     # Exception handling
│   └── SKILL.md
└── Scrapling/           # Web scraping library
    ├── SKILL.md
    ├── reference.md
    └── examples.md
```

## Skill Overview

| Skill | Type | Purpose |
|-------|------|---------|
| **mwclient** | Parent | Interact with MediaWiki APIs (Wikipedia, etc.) |
| **scrapling** | Standalone | Web scraping with anti-bot protection |

---

## mwclient

A skill family for working with MediaWiki instances like Wikipedia.

**Core concepts:** Site (connection), Page (wiki pages), Image (files), Listings (pagination), Errors (exception handling)

---

## scrapling

A standalone skill for web scraping with multiple fetcher strategies.

| Capability | Description |
|------------|-------------|
| **Parsing** | CSS selectors, XPath, BeautifulSoup-style, text/regex search |
| **Adaptive** | Automatically relocates elements when websites change structure |
| **Anti-Detection** | TLS fingerprinting, browser automation, Cloudflare bypass |
| **Async** | Concurrent request handling |

### Fetcher Types

| Fetcher | Best For |
|---------|----------|
| `Fetcher` | Static HTML, simple sites |
| `DynamicFetcher` | JavaScript-rendered content |
| `StealthyFetcher` | Protected sites, Cloudflare |

---

## Reference

| Skill | Invocation | Description |
|-------|------------|-------------|
| mwclient | `/mwclient` | Overview, installation, common patterns |
| mwclient-site | `/mwclient:site` | Connection setup, OAuth, HTTP Basic, tokens, site metadata |
| mwclient-page | `/mwclient:page` | Content retrieval, editing, page management, backlinks |
| mwclient-images | `/mwclient:images` | File metadata, upload/download, duplicates, usage tracking |
| mwclient-listing | `/mwclient:listing` | Lazy pagination, generators vs lists, result iteration |
| mwclient-errors | `/mwclient:errors` | Exception hierarchy, permission errors, edit conflicts |
| scrapling | `/scrapling` | Web scraping with anti-bot protection |
