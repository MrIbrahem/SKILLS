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

| Skill         | Type       | Purpose                                        |
| ------------- | ---------- | ---------------------------------------------- |
| **mwclient**  | Parent     | Interact with MediaWiki APIs (Wikipedia, etc.) |
| **scrapling** | Standalone | Web scraping with anti-bot protection          |

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

## Sub-skill Map

| Sub-skill        | Invocation          | When to use                                               |
| ---------------- | ------------------- | --------------------------------------------------------- |
| mwclient         | `/mwclient`         | Overview, installation, common patterns                   |
| mwclient-site    | `/mwclient:site`    | Connecting to a site, login, auth, session setup          |
| mwclient-page    | `/mwclient:page`    | Reading & editing pages, get wikitext, save, move, delete |
| mwclient-images  | `/mwclient:images`  | Images & file uploads, download, get image info           |
| mwclient-listing | `/mwclient:listing` | Listings & iterators, categories, search, recent changes  |
| mwclient-errors  | `/mwclient:errors`  | Error handling, catching and recovering from exceptions   |
| scrapling        | `/scrapling`        | Web scraping, bypassing anti-bot protection               |
