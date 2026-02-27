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

| Feature            | Fetcher                                           | DynamicFetcher                                                                    | StealthyFetcher                                                                            |
| ------------------ | ------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Relative speed     | Fastest (HTTP only)                               | Medium (browser)                                                                  | Medium (browser with stealth)                                                              |
| Stealth            | Basic (TLS fingerprinting)                        | Moderate                                                                          | Maximum (anti-bot bypass)                                                                  |
| Anti-Bot options   | Basic                                             | Moderate                                                                          | Advanced (Cloudflare solver)                                                               |
| JavaScript loading | No                                                | Yes                                                                               | Yes                                                                                        |
| Memory Usage       | Low                                               | Medium                                                                            | Medium                                                                                     |
| Best used for      | Basic scraping when HTTP requests alone can do it | - Dynamically loaded websites <br/>- Small automation<br/>- Small-Mid protections | - Dynamically loaded websites <br/>- Small automation <br/>- Small-Complicated protections |
| Browser(s)         | None                                              | Chromium and Google Chrome                                                        | Chromium and Google Chrome                                                                 |
| Browser API used   | None                                              | PlayWright                                                                        | PlayWright                                                                                 |
| Setup Complexity   | Simple                                            | Simple                                                                            | Simple                                                                                     |

**Decision flow:**

1. Start with `Fetcher` for speed - most sites work with HTTP/3 + TLS fingerprinting
2. Upgrade to `DynamicFetcher` if JavaScript rendering is required
3. Use `StealthyFetcher` when facing Cloudflare Turnstile or device fingerprinting

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
products = page.css('.product', adaptive=True)  # Finds elements by similarity
```

### 5. Handle Anti-Bot Protection

For protected sites, use StealthyFetcher with appropriate options:

```python
page = StealthyFetcher.fetch(
    'https://protected-site.com',
    solve_cloudflare=True,   # Solve Cloudflare challenges
    block_webrtc=True,       # Prevent IP leaks
    hide_canvas=True,        # Prevent canvas fingerprinting
    real_chrome=True,        # Use real Chrome browser
    headless=True            # Run without visible browser
)
```

## Response Object

All fetchers return `Response` objects that extend `Selector` with HTTP metadata:

```python
page = Fetcher.get('https://example.com')

# HTTP metadata
page.status           # HTTP status code (200)
page.reason           # Status message ('OK')
page.cookies          # Response cookies as dict
page.headers          # Response headers
page.request_headers  # Request headers
page.history          # Response history of redirections
page.body             # Raw response body as bytes
page.encoding         # Response encoding
page.meta             # Response metadata dictionary
page.url              # Final URL after redirects

# Inherited from Selector
page.css('title::text')
page.xpath('//h1')
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

### Browser Session with Tab Pool

```python
from scrapling import DynamicSession, AsyncDynamicSession

# Synchronous
with DynamicSession(max_pages=3) as session:
    page1 = session.fetch('https://site1.com')
    page2 = session.fetch('https://site2.com')

# Asynchronous
async with AsyncDynamicSession(max_pages=5) as session:
    tasks = [session.fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
```

### Proxy Rotation

```python
from scrapling.fetchers import FetcherSession, ProxyRotator

rotator = ProxyRotator([
    'http://proxy1:8080',
    'http://proxy2:8080',
    'http://proxy3:8080',
])

with FetcherSession(proxy_rotator=rotator, impersonate='chrome') as session:
    # Each request automatically uses the next proxy in rotation
    page1 = session.get('https://example.com/page1')
    page2 = session.get('https://example.com/page2')

    # You can check which proxy was used via the response metadata
    print(page1.meta['proxy'])
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

### Wait Conditions

```python
from scrapling import DynamicFetcher

# Wait for specific selector state
page = DynamicFetcher.fetch(
    'https://example.com',
    wait_selector='h1',
    wait_selector_state='visible'  # attached, detached, visible, hidden
)

# Wait for network idle
page = DynamicFetcher.fetch(
    'https://example.com',
    network_idle=True  # No network connections for 500ms
)
```

## Fetcher Configuration

### Parser Configuration

Configure the parser globally for all requests:

```python
from scrapling import Fetcher

# Method 1: configure()
Fetcher.configure(adaptive=True, keep_comments=False, keep_cdata=False)

# Method 2: Direct assignment
Fetcher.adaptive = True
Fetcher.keep_comments = False
Fetcher.huge_tree = True

# Display current config
Fetcher.display_config()
```

Available config options: `adaptive`, `adaptive_domain`, `huge_tree`, `keep_comments`, `keep_cdata`, `storage`, `storage_args`.

### Per-Request Config

```python
# Pass selector_config for per-request parsing options
page = Fetcher.get('https://example.com', selector_config={'adaptive': True})
```

## Fetcher Reference

### Fetcher (Static HTTP)

```python
from scrapling import Fetcher, AsyncFetcher

# Methods: get, post, put, delete
page = Fetcher.get('https://example.com')
page = Fetcher.post('https://example.com/api', json={'key': 'value'})
```

**Common Parameters:**

| Parameter          | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| `impersonate`      | Browser to impersonate ('chrome', 'firefox', 'safari', 'edge')   |
| `stealthy_headers` | Generate realistic browser headers automatically (default: True) |
| `timeout`          | Request timeout in seconds (default: 30)                         |
| `retries`          | Number of retries for failed requests (default: 3)               |
| `retry_delay`      | Seconds to wait between retries (default: 1)                     |
| `follow_redirects` | Follow HTTP redirects (default: True)                            |
| `proxy`            | Proxy URL: 'http://username:password@host:port'                  |
| `proxy_rotator`    | ProxyRotator instance for automatic rotation                     |
| `cookies`          | Dict of cookies to send                                          |
| `headers`          | Custom HTTP headers                                              |
| `http3`            | Use HTTP/3 protocol (default: False)                             |

### DynamicFetcher (Browser Automation)

```python
from scrapling import DynamicFetcher, AsyncDynamicFetcher

page = DynamicFetcher.fetch('https://example.com')
```

**Parameters:**

| Parameter             | Description                                            |
| --------------------- | ------------------------------------------------------ |
| `headless`            | Run browser without GUI (default: True)                |
| `real_chrome`         | Use locally installed Chrome instead of Chromium       |
| `network_idle`        | Wait for network to be idle                            |
| `load_dom`            | Wait for DOM content loaded (default: True)            |
| `wait_selector`       | Wait for specific CSS selector                         |
| `wait_selector_state` | Selector state: attached, detached, visible, hidden    |
| `timeout`             | Maximum wait time in milliseconds (default: 30000)     |
| `wait`                | Extra wait time after page loads (milliseconds)        |
| `disable_resources`   | Block fonts, images, media for speed                   |
| `blocked_domains`     | Set of domains to block (and subdomains)               |
| `page_action`         | Function to execute on Playwright page object          |
| `proxy`               | Proxy string or dict with server/username/password     |
| `proxy_rotator`       | ProxyRotator instance for automatic rotation           |
| `locale`              | User locale (e.g., 'en-GB', 'de-DE')                   |
| `timezone_id`         | Browser timezone                                       |
| `cdp_url`             | Connect to remote browser via Chrome DevTools Protocol |
| `extra_headers`       | Dictionary of extra headers to add                     |
| `google_search`       | Set referer as Google search (default: True)           |
| `useragent`           | Custom user agent string                               |
| `retries`             | Number of retry attempts (default: 3)                  |
| `retry_delay`         | Seconds between retries (default: 1)                   |

### StealthyFetcher (Anti-Detection)

```python
from scrapling import StealthyFetcher, AsyncStealthyFetcher

page = StealthyFetcher.fetch('https://protected-site.com')
```

All DynamicFetcher parameters plus:

| Parameter          | Description                               |
| ------------------ | ----------------------------------------- |
| `solve_cloudflare` | Automatically solve Cloudflare challenges |
| `block_webrtc`     | Block WebRTC to prevent IP leaks          |
| `hide_canvas`      | Add random noise to canvas operations     |
| `allow_webgl`      | Enable WebGL support (default: True)      |

### Session Classes

-   **FetcherSession** - HTTP session with cookie persistence
-   **DynamicSession / AsyncDynamicSession** - Browser session with tab pool
-   **StealthySession / AsyncStealthySession** - Stealth browser session

**Session Parameters:**

| Parameter   | Description                            |
| ----------- | -------------------------------------- |
| `max_pages` | Maximum concurrent browser tabs (1-50) |

In sessions, pass per-request overrides to `fetch()` or HTTP methods.

## Best Practices

1. **Start simple**: Use `Fetcher` first, only upgrade if needed
2. **Use `::text` pseudo-element**: Extract text directly with CSS selectors
3. **Handle missing elements**: Use `default=` parameter or check `.first` attribute
4. **Enable adaptive for production**: Use `auto_save=True` on initial scrapes
5. **Use sessions for multiple requests**: Better performance with cookie persistence
6. **Filter early**: Narrow with CSS before using Python loops
7. **Set timeout appropriately**: Use at least 60 seconds when using Cloudflare solver
8. **Use proxy_rotator for large-scale scraping**: Automatic rotation with sessions

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

## Advanced Usage

For detailed API reference, advanced options, and complete examples:

-   See [reference.md](reference.md) for comprehensive API documentation
-   See [examples.md](examples.md) for extended use cases and patterns
-   See [references/static_fetcher.md](references/static_fetcher.md) for detailed HTTP fetcher documentation
-   See [references/dynamic_fetcher.md](references/dynamic_fetcher.md) for browser automation details
-   See [references/stealthy_fetcher.md](references/stealthy_fetcher.md) for anti-bot protection features
-   See [references/sessions.md](references/sessions.md) for session management and proxy rotation
-   See [references/adaptive_parsing.md](references/adaptive_parsing.md) for resilient element relocation

## Key Capabilities

**Fetching:**

-   HTTP/1.1, HTTP/2, HTTP/3 with TLS fingerprinting
-   Browser automation via Playwright/Patchright
-   Cloudflare challenge solver
-   Session management with browser tab pools
-   Automatic proxy rotation

**Parsing:**

-   CSS, XPath, BeautifulSoup-style, text/regex search
-   Scrapy-compatible pseudo-elements (`::text`, `::attr()`)
-   Adaptive element relocation via similarity scoring

**Performance:**

-   Outperforms BeautifulSoup, MechanicalSoup, Selectolax
-   `orjson` for 10x faster JSON serialization
-   92% test coverage with full type hints
