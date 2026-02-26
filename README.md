# Skills Repository

A collection of Claude Code skills for specialized tasks. These skills provide domain-specific knowledge and capabilities to assist with API interactions, web scraping, and more.

## Skills Tree

```
skills/
├── mwclient/                          # MediaWiki API Client
│   ├── site/                          # └── Site connection & authentication
│   ├── page/                          # └── Page operations (read/edit/move)
│   ├── images/                        # └── File/image operations
│   ├── listing/                       # └── Pagination & iteration
│   └── errors/                        # └── Exception handling
│
└── scrapling/                         # Web scraping library
    ├── reference.md                   # └── API reference
    └── examples.md                    # └── Extended examples
```

## Skill Overview

| Skill | Description | Use When |
|-------|-------------|----------|
| **[mwclient](#mwclient)** | Python client for the MediaWiki API | Automating wiki edits, scraping wiki content, uploading files, or building bots for MediaWiki instances |
| **[scrapling](#scrapling)** | Web scraping with adaptive parsing | Scraping websites, extracting data from HTML, bypassing anti-bot protection, or automating browser interactions |

---

## mwclient

Python client for the MediaWiki API. Provides a high-level interface for interacting with wikis (like Wikipedia).

**Core abstractions:** Site (connection), Page (wiki pages), and Image (files)

### Sub-Skills Hierarchy

```
mwclient/
├── Site Level
│   └── site          # Connection, authentication, site-level queries
│       ├── OAuth, HTTP Basic, clientlogin
│       ├── Token management
│       └── Site metadata (namespaces, version)
│
├── Content Level
│   ├── page          # Page operations
│   │   ├── Read/edit/append/prepend
│   │   ├── Move/delete/purge
│   │   └── Backlinks, categories, links
│   │
│   └── images        # File operations
│       ├── Download/upload
│       ├── Image metadata (imageinfo)
│       └── File history & usage
│
├── Infrastructure
│   └── listing       # Pagination & iteration
│       ├── List, GeneratorList, PageList
│       ├── api_chunk_size vs max_items
│       └── Continuation tokens
│
└── Error Handling
    └── errors        # Exception hierarchy
        ├── MwClientError (base)
        ├── APIError, EditError, LoginError
        └── InsufficientPermission, ProtectedPageError
```

### Quick Start

```python
import mwclient

# Connect to a wiki
site = mwclient.Site('en.wikipedia.org')

# Read a page
page = site.pages['Python (programming language)']
print(page.text())

# Edit a page (requires login)
site.login('username', 'password')
page.edit('New content', summary='Updated via mwclient')
```

### Installation

```bash
pip install mwclient
```

---

## Scrapling

Web scraping library with adaptive parsing, stealth browsing, and multiple fetcher strategies.

**Key Features:**
- CSS/XPath selectors with Scrapy-compatible pseudo-elements (`::text`, `::attr()`)
- JavaScript rendering via Playwright/Patchright
- Cloudflare bypass and anti-bot protection
- Automatic element relocation when sites change
- Async support for concurrent requests

### Fetcher Types

```
scrapling/
├── Fetcher              # Static HTML, APIs, simple sites
├── DynamicFetcher       # JavaScript-heavy sites
└── StealthyFetcher      # Cloudflare, advanced anti-bot
```

### Quick Start

```python
from scrapling import Fetcher

# Basic scraping
page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text')
for quote in quotes:
    print(quote.clean())
```

### Decision Flow

1. Start with `Fetcher` for speed - most sites work with HTTP/3 + TLS fingerprinting
2. Upgrade to `DynamicFetcher` if JavaScript rendering is required
3. Use `StealthyFetcher` when facing Cloudflare Turnstile or device fingerprinting

### Installation

```bash
# Core only (parser engine)
pip install scrapling

# With fetchers (includes curl_cffi, playwright, camoufox)
pip install "scrapling[fetchers]"
scrapling install  # Download browsers

# Everything (includes AI/MCP, shell features)
pip install "scrapling[all]"
```

---

## Skill Reference Table

| Skill | User-Invocable | Namespace | Description |
|-------|----------------|-----------|-------------|
| `mwclient` | Yes | - | Main MediaWiki API client |
| `mwclient:site` | Yes | `site` | Site connection & authentication |
| `mwclient:page` | Yes | `page` | Page read/edit operations |
| `mwclient:images` | Yes | `images` | File upload/download operations |
| `mwclient:listing` | Yes | `listing` | Pagination and list iteration |
| `mwclient:errors` | Yes | `errors` | Exception handling |
| `scrapling` | Yes | `scrapling` | Web scraping library |

---

## Usage in Claude Code

To use a skill, reference it by name:

```
/mwclient
/scrapling
```

Or use sub-skills directly:

```
/mwclient:site
/mwclient:page
/mwclient:errors
```

---

## Resources

- **mwclient Documentation:** https://mwclient.readthedocs.io
- **mwclient Source:** https://github.com/mwclient/mwclient
- **Scrapling Repository:** https://github.com/d4sein/Scrapling
