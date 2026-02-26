# Skills Repository

A collection of Claude Code skills for specialized tasks.

## Directory Structure

```
.claude/skills/
├── mwclient/            # MediaWiki API client (parent skill)
├── mwclient-site/       # Site connection & authentication
├── mwclient-page/       # Page operations
├── mwclient-images/     # File/image operations
├── mwclient-listing/    # Pagination & iteration
├── mwclient-errors/     # Exception handling
└── Scrapling/           # Web scraping library
```

## Skill Overview

| Skill | Type | Purpose |
|-------|------|---------|
| **mwclient** | Parent | Interact with MediaWiki APIs (Wikipedia, etc.) |
| **mwclient-site** | Sub-skill | Connect to wikis and authenticate |
| **mwclient-page** | Sub-skill | Read, edit, move, delete wiki pages |
| **mwclient-images** | Sub-skill | Upload, download, manage files |
| **mwclient-listing** | Sub-skill | Iterate through large result sets |
| **mwclient-errors** | Sub-skill | Handle exceptions and errors |
| **scrapling** | Standalone | Web scraping with anti-bot protection |

---

## mwclient Skill Family

A set of skills for working with MediaWiki instances like Wikipedia.

| Skill | Responsibility |
|-------|----------------|
| `mwclient` | Overview, installation, common patterns |
| `mwclient-site` | Connection setup, OAuth, HTTP Basic, tokens, site metadata |
| `mwclient-page` | Content retrieval, editing, page management, backlinks |
| `mwclient-images` | File metadata, upload/download, duplicates, usage tracking |
| `mwclient-listing` | Lazy pagination, generators vs lists, result iteration |
| `mwclient-errors` | Exception hierarchy, permission errors, edit conflicts |

---

## scrapling

A standalone skill for web scraping with multiple fetcher strategies.

| Capability | Description |
|------------|-------------|
| **Parsing** | CSS selectors, XPath, BeautifulSoup-style, text/regex search |
| **Adaptive** | Automatically relocates elements when websites change |
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

| Skill | Invocation |
|-------|------------|
| mwclient | `/mwclient` |
| mwclient-site | `/mwclient:site` |
| mwclient-page | `/mwclient:page` |
| mwclient-images | `/mwclient:images` |
| mwclient-listing | `/mwclient:listing` |
| mwclient-errors | `/mwclient:errors` |
| scrapling | `/scrapling` |
