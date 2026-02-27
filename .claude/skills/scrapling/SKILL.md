---
name: scrapling
description: Web scraping library with adaptive parsing, stealth browsing, and multiple fetcher strategies. Use when scraping websites, extracting data from HTML, bypassing anti-bot protection, or automating browser interactions. Supports CSS/XPath selectors, JavaScript rendering, Cloudflare bypass, and automatic element relocation when sites change.
---

# Scrapling

Scrapling is a Python web scraping library (Python 3.10+) that distinguishes itself through **adaptive parsing** - the ability to automatically relocate HTML elements after website structure changes.

## Quick Start

```python
from scrapling import Fetcher

# Basic scraping
page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text')
for quote in quotes:
    print(quote.clean())
```

## Instructions

When helping users with Scrapling, follow these steps:

### 1. Choose the Right Fetcher

Scrapling provides three fetcher types for different scenarios:

| Fetcher                                    | Use When                                  | Import                                  |
| ------------------------------------------ | ----------------------------------------- | --------------------------------------- |
| `Fetcher` / `AsyncFetcher`                 | Static HTML, APIs, simple sites           | `from scrapling import Fetcher`         |
| `DynamicFetcher` / `AsyncDynamicFetcher`   | JavaScript-heavy sites, need real browser | `from scrapling import DynamicFetcher`  |
| `StealthyFetcher` / `AsyncStealthyFetcher` | Cloudflare, advanced anti-bot systems     | `from scrapling import StealthyFetcher` |

**Decision flow:**

1. Start with `Fetcher` for speed - most sites work with HTTP/3 + TLS fingerprinting
2. Upgrade to `DynamicFetcher` if JavaScript rendering is required
3. Use `StealthyFetcher` when facing Cloudflare Turnstile or device fingerprinting

See detailed fetcher comparisons and all parameters in the reference files linked below.

### 2. Extract Data with Selectors

All fetchers return a `Response` object with unified parsing methods:

```python
# CSS selectors (Scrapy-compatible with ::text and ::attr())
page.css('.product::text')           # All matching text
page.css_first('.product::text')     # First match only

# XPath selectors
page.xpath('//div[@class="product"]')
page.xpath_first('//h1/text()')

# BeautifulSoup-style
page.find_all('div', class_='product')
page.find('div', {'data-id': '123'})

# Text and regex search
page.find_by_text('Add to Cart')
page.find_by_regex(r'\$\d+\.\d{2}')
```

### 3. Work with TextHandler Results

Text content is returned as `TextHandler` objects with enhanced methods:

```python
text = page.css_first('.price::text')
text.clean()           # Remove extra whitespace
text.re(r'\d+')        # Apply regex
text.re_first(r'\d+')  # First regex match
text.json()            # Parse as JSON
```

### 4. Use Adaptive Parsing for Resilient Scrapers

Enable adaptive parsing to automatically relocate elements when websites change:

```python
from scrapling import StealthyFetcher

# Enable adaptive globally
StealthyFetcher.adaptive = True

# First run - save element properties
page = StealthyFetcher.fetch('https://example.com')
products = page.css('.product', auto_save=True)

# Later runs - automatically relocated if selectors break
page = StealthyFetcher.fetch('https://example.com')
products = page.css('.product', adaptive=True)
```

### 5. Handle Anti-Bot Protection

For protected sites, use StealthyFetcher with appropriate options:

```python
page = StealthyFetcher.fetch(
    'https://protected-site.com',
    solve_cloudflare=True,   # Solve Cloudflare challenges
    timeout=60000           # 60 seconds for Cloudflare
)
```

## Common Patterns

### Extract List of Items

```python
page = Fetcher.get('https://example.com/products')
products = page.css('.product')

for product in products:
    name = product.css_first('.name::text', default='N/A')
    price = product.css_first('.price::text', default='N/A')
    url = product.css_first('a').attrib.get('href')
    print(f"{name}: {price} - {url}")
```

### Async Concurrent Requests

```python
import asyncio
from scrapling import AsyncFetcher

async def scrape_urls(urls):
    tasks = [AsyncFetcher.get(url) for url in urls]
    pages = await asyncio.gather(*tasks)
    return pages

pages = asyncio.run(scrape_urls(['https://site1.com', 'https://site2.com']))
```

### Session with Cookie Persistence

```python
from scrapling import FetcherSession

with FetcherSession() as session:
    login = session.post('https://site.com/login', data={'user': 'admin', 'pass': 'secret'})
    profile = session.get('https://site.com/profile')  # Cookies maintained
```

### Browser Automation

```python
from scrapling import DynamicFetcher
from playwright.sync_api import Page

def perform_login(page: Page):
    page.fill('input[name="username"]', 'myuser')
    page.fill('input[name="password"]', 'mypassword')
    page.click('button[type="submit"]')
    page.wait_for_selector('.dashboard')
    return page

page = DynamicFetcher.fetch(
    'https://example.com/login',
    page_action=perform_login
)
```

### Proxy Rotation

```python
from scrapling.fetchers import FetcherSession, ProxyRotator

rotator = ProxyRotator([
    'http://proxy1:8080',
    'http://proxy2:8080',
])

with FetcherSession(proxy_rotator=rotator) as session:
    page1 = session.get('https://example.com/page1')
    page2 = session.get('https://example.com/page2')
```

## Response Object

All fetchers return `Response` objects with HTTP metadata:

```python
page = Fetcher.get('https://example.com')

page.status           # HTTP status code
page.cookies          # Response cookies as dict
page.headers          # Response headers
page.url              # Final URL after redirects
page.body             # Raw response body as bytes

# Inherited from Selector
page.css('title::text')
page.xpath('//h1')
```

## Best Practices

1. **Start simple**: Use `Fetcher` first, only upgrade if needed
2. **Use `::text` pseudo-element**: Extract text directly with CSS selectors
3. **Handle missing elements**: Use `default=` parameter
4. **Enable adaptive for production**: Use `auto_save=True` on initial scrapes
5. **Use sessions for multiple requests**: Better performance with cookie persistence
6. **Set timeout appropriately**: Use at least 60 seconds when using Cloudflare solver

## Installation

```bash
# Core only (parser engine)
pip install scrapling

# With fetchers (includes curl_cffi, playwright)
pip install "scrapling[fetchers]"
playwright install  # Download browsers

# Everything (includes AI/MCP, shell features)
pip install "scrapling[all]"
```

## Requirements

-   Python 3.10+
-   For browser features: `playwright install` after package installation

## Reference Documentation

For detailed API reference, all parameters, and advanced examples:

-   **[reference.md](reference.md)** - Comprehensive API reference for all classes
-   **[examples.md](examples.md)** - Extended use cases and patterns

### Detailed Fetcher Guides

-   **[references/static_fetcher.md](references/static_fetcher.md)** - HTTP fetcher (Fetcher/AsyncFetcher)
-   **[references/dynamic_fetcher.md](references/dynamic_fetcher.md)** - Browser automation (DynamicFetcher)
-   **[references/stealthy_fetcher.md](references/stealthy_fetcher.md)** - Anti-bot protection (StealthyFetcher)
-   **[references/sessions.md](references/sessions.md)** - Session management and proxy rotation
-   **[references/adaptive_parsing.md](references/adaptive_parsing.md)** - Resilient element relocation
