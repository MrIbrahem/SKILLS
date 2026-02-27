# Scrapling API Reference

Complete reference for Scrapling classes, methods, and configuration options.

## Table of Contents

1. [Fetchers](#fetchers)
2. [Selectors](#selectors)
3. [Custom Types](#custom-types)
4. [Sessions](#sessions)
5. [Configuration Options](#configuration-options)

---

## Fetchers

### Fetcher (Static HTTP)

Synchronous HTTP fetcher using `curl_cffi` with browser impersonation.

```python
from scrapling import Fetcher, AsyncFetcher
```

#### Methods

| Method   | Signature                           | Description         |
| -------- | ----------------------------------- | ------------------- |
| `get`    | `get(url, **kwargs) -> Response`    | HTTP GET request    |
| `post`   | `post(url, **kwargs) -> Response`   | HTTP POST request   |
| `put`    | `put(url, **kwargs) -> Response`    | HTTP PUT request    |
| `delete` | `delete(url, **kwargs) -> Response` | HTTP DELETE request |

#### Common Parameters

| Parameter          | Type  | Description                                                    |
| ------------------ | ----- | -------------------------------------------------------------- |
| `url`              | str   | Target URL                                                     |
| `impersonate`      | str   | Browser to impersonate ('chrome', 'firefox', 'safari', 'edge') |
| `stealthy_headers` | bool  | Generate realistic browser headers automatically               |
| `timeout`          | float | Request timeout in seconds                                     |
| `headers`          | dict  | Custom HTTP headers                                            |
| `cookies`          | dict  | Cookies to send with request                                   |

### DynamicFetcher (Browser Automation)

Playwright-based browser automation for JavaScript-heavy sites.

```python
from scrapling import DynamicFetcher, AsyncDynamicFetcher
```

#### Methods

| Method        | Signature                                | Description                   |
| ------------- | ---------------------------------------- | ----------------------------- |
| `fetch`       | `fetch(url, **kwargs) -> Response`       | Fetch with browser automation |
| `async_fetch` | `async_fetch(url, **kwargs) -> Response` | Async browser fetch           |

#### Parameters

| Parameter           | Type     | Description                                            |
| ------------------- | -------- | ------------------------------------------------------ |
| `url`               | str      | Target URL                                             |
| `headless`          | bool     | Run browser without GUI (default: True)                |
| `stealth`           | bool     | Enable Patchright stealth patches                      |
| `real_chrome`       | bool     | Use locally installed Chrome instead of Chromium       |
| `network_idle`      | bool     | Wait for network to be idle                            |
| `load_dom`          | bool     | Wait for DOM content loaded                            |
| `wait_selector`     | str      | Wait for specific selector to appear                   |
| `wait_timeout`      | int      | Maximum wait time in milliseconds                      |
| `disable_resources` | bool     | Block images, fonts, media for speed                   |
| `hide_canvas`       | bool     | Inject random noise into canvas fingerprints           |
| `disable_webgl`     | bool     | Disable WebGL to reduce fingerprinting                 |
| `page_action`       | callable | Function to execute on Playwright page object          |
| `cdp_url`           | str      | Connect to remote browser via Chrome DevTools Protocol |

### StealthyFetcher (Anti-Detection)

Camoufox-based fetcher for bypassing advanced anti-bot systems.

```python
from scrapling import StealthyFetcher, AsyncStealthyFetcher
```

#### Methods

| Method        | Signature                                | Description                 |
| ------------- | ---------------------------------------- | --------------------------- |
| `fetch`       | `fetch(url, **kwargs) -> Response`       | Stealth fetch with Camoufox |
| `async_fetch` | `async_fetch(url, **kwargs) -> Response` | Async stealth fetch         |

#### Parameters

All DynamicFetcher parameters plus:

| Parameter          | Type | Description                                                    |
| ------------------ | ---- | -------------------------------------------------------------- |
| `solve_cloudflare` | bool | Automatically solve Cloudflare challenges                      |
| `humanize`         | bool | Add realistic mouse movements and timing                       |
| `geoip`            | bool | Auto-configure timezone/locale based on proxy IP               |
| `os`               | str  | OS fingerprint ('windows', 'macos', 'linux', 'android', 'ios') |
| `os_randomize`     | bool | Randomize OS fingerprint                                       |
| `block_webrtc`     | bool | Block WebRTC to prevent IP leaks                               |
| `block_images`     | bool | Block image loading                                            |
| `disable_ads`      | bool | Enable uBlock Origin ad blocker                                |
| `google_search`    | bool | Set Google as referer                                          |
| `addons`           | list | List of paths to Firefox addon extensions                      |

---

## Selectors

### Selector Class

Core parsing engine for HTML content.

```python
from scrapling import Selector

# From HTML string
selector = Selector(html='<div class="test">Content</div>')
```

#### Selection Methods

| Method                                   | Returns                | Description                       |
| ---------------------------------------- | ---------------------- | --------------------------------- |
| `css(selector)`                          | Selectors              | CSS selector query (all matches)  |
| `css_first(selector, default=None)`      | Selector \| default    | CSS selector (first match only)   |
| `xpath(selector)`                        | Selectors              | XPath query (all matches)         |
| `xpath_first(selector, default=None)`    | Selector \| default    | XPath query (first match only)    |
| `find_all(tag, attrs)`                   | Selectors              | BeautifulSoup-style search        |
| `find(tag, attrs)`                       | Selector \| None       | BeautifulSoup-style (first match) |
| `find_by_text(text)`                     | Selectors              | Find by exact text content        |
| `find_by_regex(pattern)`                 | Selectors              | Find by regex pattern             |
| `find_similar(similarity_threshold=0.7)` | Selectors              | Find similar elements             |
| `re(pattern)`                            | TextHandlers           | Apply regex to element content    |
| `re_first(pattern, default=None)`        | TextHandler \| default | First regex match                 |

#### Adaptive Parameters

| Parameter        | Description                                 |
| ---------------- | ------------------------------------------- |
| `auto_save=True` | Save element properties for later retrieval |
| `adaptive=True`  | Enable element relocation if selector fails |

#### Properties

| Property       | Type              | Description                |
| -------------- | ----------------- | -------------------------- |
| `text`         | TextHandler       | Direct text content        |
| `html_content` | TextHandler       | Inner HTML                 |
| `attrib`       | AttributesHandler | Element attributes mapping |
| `tag`          | str               | Tag name                   |
| `url`          | str               | Page URL                   |
| `encoding`     | str               | Page encoding              |
| `parent`       | Selector \| None  | Parent element             |
| `children`     | Selectors         | Child elements             |
| `siblings`     | Selectors         | Sibling elements           |
| `next`         | Selector \| None  | Next sibling               |
| `previous`     | Selector \| None  | Previous sibling           |

#### Utility Methods

| Method                      | Returns | Description                          |
| --------------------------- | ------- | ------------------------------------ |
| `prettify()`                | str     | Formatted HTML                       |
| `get_all_text(ignore_tags)` | str     | All text with optional tag filtering |
| `has_class(class_name)`     | bool    | Check for CSS class                  |
| `urljoin(url)`              | str     | Resolve relative URL                 |
| `json()`                    | dict    | Parse content as JSON                |
| `save(identifier)`          | None    | Manual element save for adaptive     |

### Selectors Class

Collection of Selector objects with chainable operations.

```python
results = page.css('.item')
```

#### Properties

| Property | Type     | Description                 |
| -------- | -------- | --------------------------- |
| `first`  | Selector | First element in collection |
| `last`   | Selector | Last element in collection  |

#### Methods

| Method              | Returns          | Description                         |
| ------------------- | ---------------- | ----------------------------------- |
| `css(selector)`     | Selectors        | Filter with CSS selector            |
| `xpath(selector)`   | Selectors        | Filter with XPath                   |
| `re(pattern)`       | TextHandlers     | Apply regex to all elements         |
| `re_first(pattern)` | TextHandler      | First regex match from all elements |
| `filter(func)`      | Selectors        | Filter with custom function         |
| `search(func)`      | Selector \| None | Find first matching element         |

---

## Custom Types

### TextHandler

Enhanced string type with scraping utilities.

```python
text = page.css_first('.title::text')  # Returns TextHandler
```

#### Methods

| Method                            | Returns        | Description             |
| --------------------------------- | -------------- | ----------------------- |
| `clean()`                         | TextHandler    | Remove extra whitespace |
| `re(pattern)`                     | list           | Find all regex matches  |
| `re_first(pattern, default=None)` | str \| default | First regex match       |
| `json()`                          | dict           | Parse as JSON           |

#### Inherited String Methods

All standard Python string methods are available: `split()`, `replace()`, `upper()`, `lower()`, `strip()`, etc.

### TextHandlers

Collection of TextHandler objects.

```python
texts = page.css('.item::text')  # Returns TextHandlers
```

#### Properties

| Property | Type        | Description              |
| -------- | ----------- | ------------------------ |
| `first`  | TextHandler | First text in collection |

#### Methods

| Method              | Returns      | Description                |
| ------------------- | ------------ | -------------------------- |
| `re(pattern)`       | TextHandlers | Apply regex to all texts   |
| `re_first(pattern)` | TextHandler  | First match from all texts |

### AttributesHandler

Mapping interface for HTML element attributes.

```python
attrs = page.css_first('a').attrib
```

#### Methods

| Method                   | Returns                | Description             |
| ------------------------ | ---------------------- | ----------------------- |
| `get(key, default=None)` | TextHandler \| default | Get attribute value     |
| `search_values(keyword)` | generator              | Search attribute values |

#### Properties

| Property      | Type | Description               |
| ------------- | ---- | ------------------------- |
| `json_string` | str  | Attributes as JSON string |

---

## Sessions

### FetcherSession

HTTP session with cookie persistence.

```python
from scrapling import FetcherSession

with FetcherSession() as session:
    session.get('https://example.com')
    session.get('https://example.com/page2')  # Cookies maintained
```

### DynamicSession / AsyncDynamicSession

Browser session with tab pool management.

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

### StealthySession / AsyncStealthySession

Stealth browser session with consistent fingerprint.

```python
from scrapling import StealthySession

with StealthySession(max_pages=2) as session:
    page = session.fetch('https://protected-site.com')
```

#### Session Parameters

| Parameter   | Type | Description                            |
| ----------- | ---- | -------------------------------------- |
| `max_pages` | int  | Maximum concurrent browser tabs (1-50) |

---

## Configuration Options

### Adaptive Configuration

```python
from scrapling import StealthyFetcher

# Enable globally
StealthyFetcher.auto_match = True

# Per-selector usage
page.css('.product', auto_save=True)   # Save for later
page.css('.product', adaptive=True)    # Use adaptive relocation
```

### Storage System

Custom storage backends for adaptive parsing:

```python
from scrapling import Selector
from scrapling.core.storage import StorageSystemMixin
from functools import lru_cache

@lru_cache(maxsize=128)
class RedisStorage(StorageSystemMixin):
    def save(self, element, identifier):
        # Custom save implementation
        pass

    def retrieve(self, identifier):
        # Custom retrieve implementation
        pass

selector = Selector(html=html, adaptive=True, storage=RedisStorage)
```

### Browser Configuration

DynamicFetcher and StealthyFetcher support extensive browser configuration through:

-   `playwright_config`: Custom Playwright launch options
-   `context_config`: Custom browser context options
-   `viewport`: Screen dimensions
-   `user_agent`: Custom user agent string

---

## Response Object

All fetchers return `Response` objects that extend `Selector` with HTTP metadata:

```python
page = Fetcher.get('https://example.com')

# HTTP metadata
page.status      # HTTP status code (200)
page.reason      # HTTP reason phrase ('OK')
page.headers     # Response headers (dict)
page.cookies     # Response cookies (dict)
page.url         # Final URL after redirects
page.history     # List of redirect responses

# Inherited from Selector
page.css('title::text')
page.xpath('//h1')
```

---

## CLI Commands

```bash
# Install browser dependencies
scrapling install

# Extract content from URL
scrapling extract get 'https://example.com' output.md

# Launch interactive shell
scrapling shell

# Start MCP server
scrapling mcp
```
