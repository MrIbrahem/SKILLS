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

## Skill Invocation

| Skill     | Invocation   | When to use                                               |
| --------- | ------------ | --------------------------------------------------------- |
| mwclient  | `/mwclient`  | MediaWiki API operations, installation, common patterns   |
| scrapling | `/scrapling` | Web scraping, bypassing anti-bot protection               |

## mwclient References

| Reference        | When to use                                               |
| ---------------- | --------------------------------------------------------- |
| [site](.claude/skills/mwclient/references/site.md)       | Connecting to a site, login, auth, session setup          |
| [page](.claude/skills/mwclient/references/page.md)       | Reading & editing pages, get wikitext, save, move, delete |
| [images](.claude/skills/mwclient/references/images.md)   | Images & file uploads, download, get image info           |
| [listing](.claude/skills/mwclient/references/listing.md) | Listings & iterators, categories, search, recent changes  |
| [errors](.claude/skills/mwclient/references/errors.md)   | Error handling, catching and recovering from exceptions   |
