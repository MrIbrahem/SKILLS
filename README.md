# Skills Repository

A collection of Claude Code skills for specialized tasks.

## Skills Tree

```
skills/
├── mwclient/                          # MediaWiki API Client
│   ├── site/                          #     Site connection & authentication
│   ├── page/                          #     Page operations
│   ├── images/                        #     File/image operations
│   ├── listing/                       #     Pagination & iteration
│   └── errors/                        #     Exception handling
│
└── scrapling/                         # Web scraping library
    ├── reference.md                   #     API reference
    └── examples.md                    #     Extended examples
```

## Skill Overview

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **mwclient** | Interact with MediaWiki APIs (Wikipedia, etc.) | Building wiki bots, automating edits, scraping wiki content |
| **scrapling** | Extract data from websites | Web scraping, bypassing anti-bot protection, handling JavaScript-heavy sites |

---

## mwclient

A skill family for working with MediaWiki instances like Wikipedia.

### Hierarchy

```
mwclient/
├── site
│   └── Connect to wikis and authenticate (OAuth, login, tokens)
│
├── page
│   └── Read, edit, move, and delete wiki pages
│
├── images
│   └── Upload, download, and manage files
│
├── listing
│   └── Iterate through large result sets with pagination
│
└── errors
    └── Handle exceptions and error conditions
```

### Sub-Skills

| Sub-Skill | Responsibility |
|-----------|----------------|
| `site` | Connection setup, authentication methods, site metadata, API tokens |
| `page` | Content retrieval, editing operations, page management, relationships |
| `images` | File metadata, upload/download, duplicates, usage tracking |
| `listing` | Lazy pagination, generators vs lists, result iteration |
| `errors` | Exception hierarchy, permission errors, edit conflicts |

---

## scrapling

A skill for web scraping with multiple fetcher strategies.

### Fetcher Types

| Fetcher | Best For |
|---------|----------|
| `Fetcher` | Static HTML, simple sites |
| `DynamicFetcher` | JavaScript-rendered content |
| `StealthyFetcher` | Protected sites, Cloudflare |

### Capabilities

- **Parsing**: CSS selectors, XPath, BeautifulSoup-style, text/regex search
- **Adaptive**: Automatically relocates elements when websites change structure
- **Anti-Detection**: TLS fingerprinting, browser automation, Camoufox integration
- **Async**: Concurrent request handling

---

## Reference

| Skill | Invocation |
|-------|------------|
| mwclient | `/mwclient` |
| mwclient:site | `/mwclient:site` |
| mwclient:page | `/mwclient:page` |
| mwclient:images | `/mwclient:images` |
| mwclient:listing | `/mwclient:listing` |
| mwclient:errors | `/mwclient:errors` |
| scrapling | `/scrapling` |
