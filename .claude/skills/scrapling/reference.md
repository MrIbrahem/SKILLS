# Scrapling API Reference

Complete reference for Scrapling classes, methods, and configuration options.

## Table of Contents

1. [Fetchers](#fetchers)
2. [Selectors](#selectors)
3. [Custom Types](#custom-types)
4. [Sessions](#sessions)
5. [Response Object](#response-object)
6. [Configuration Options](#configuration-options)

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

#### Parameters

| Parameter          | Type   | Description                                                    |
| ------------------ | ------ | -------------------------------------------------------------- |
| `url`              | str    | Target URL                                                     |
| `impersonate`      | str    | Browser to impersonate ('chrome', 'firefox', 'safari', 'edge') |
| `stealthy_headers` | bool   | Generate realistic browser headers (default: True)             |
| `timeout`          | float  | Request timeout in seconds (default: 30)                       |
| `retries`          | int    | Number of retries for failed requests (default: 3)             |
| `retry_delay`      | float  | Seconds between retries (default: 1)                           |
| `follow_redirects` | bool   | Follow HTTP redirects (default: True)                          |
| `max_redirects`    | int    | Maximum redirects (default: 30, -1 for unlimited)              |
| `headers`          | dict   | Custom HTTP headers                                            |
| `cookies`          | dict   | Cookies to send with request                                   |
| `proxy`            | str    | Proxy URL: 'http://username:password@host:port'                |
| `proxies`          | dict   | Dict of proxies: {'http': proxy_url, 'https': proxy_url}       |
| `proxy_auth`       | tuple  | HTTP basic auth for proxy: (username, password)                |
| `proxy_rotator`    | object | ProxyRotator instance for automatic rotation                   |
| `http3`            | bool   | Use HTTP/3 protocol (default: False)                           |
| `verify`           | bool   | Verify HTTPS certificates (default: True)                      |
| `cert`             | tuple  | Client certificate (cert, key) filenames                       |
| `selector_config`  | dict   | Custom parsing arguments for Response/Selector                 |

#### POST/PUT Specific Parameters

| Parameter | Type | Description       |
| --------- | ---- | ----------------- |
| `data`    | dict | Form-encoded data |
| `json`    | dict | JSON data         |

#### GET Specific Parameters

| Parameter | Type | Description          |
| --------- | ---- | -------------------- |
| `params`  | dict | URL query parameters |

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

| Parameter             | Type     | Description                                            |
| --------------------- | -------- | ------------------------------------------------------ |
| `url`                 | str      | Target URL                                             |
| `headless`            | bool     | Run browser without GUI (default: True)                |
| `real_chrome`         | bool     | Use locally installed Chrome instead of Chromium       |
| `network_idle`        | bool     | Wait for network to be idle (500ms no connections)     |
| `load_dom`            | bool     | Wait for DOM content loaded (default: True)            |
| `timeout`             | int      | Maximum wait time in milliseconds (default: 30000)     |
| `wait`                | int      | Extra wait after page loads (milliseconds)             |
| `wait_selector`       | str      | Wait for specific CSS selector                         |
| `wait_selector_state` | str      | Selector state: attached, detached, visible, hidden    |
| `disable_resources`   | bool     | Block fonts, images, media, stylesheets for speed      |
| `blocked_domains`     | set      | Domain names to block (subdomains also matched)        |
| `page_action`         | callable | Function to execute on Playwright page object          |
| `init_script`         | str      | Path to JS file executed on page creation              |
| `proxy`               | str/dict | Proxy string or dict with server/username/password     |
| `proxy_rotator`       | object   | ProxyRotator instance for automatic rotation           |
| `locale`              | str      | User locale (e.g., 'en-GB', 'de-DE')                   |
| `timezone_id`         | str      | Browser timezone                                       |
| `cdp_url`             | str      | Connect to remote browser via Chrome DevTools Protocol |
| `user_data_dir`       | str      | Path to browser session data (sessions only)           |
| `extra_flags`         | list     | Additional browser launch flags                        |
| `extra_headers`       | dict     | Dictionary of extra headers to add                     |
| `google_search`       | bool     | Set referer as Google search (default: True)           |
| `useragent`           | str      | Custom user agent string                               |
| `cookies`             | dict     | Cookies to set for the request                         |
| `retries`             | int      | Number of retry attempts (default: 3)                  |
| `retry_delay`         | int      | Seconds between retries (default: 1)                   |
| `selector_config`     | dict     | Custom parsing arguments for Response/Selector         |
| `additional_args`     | dict     | Additional Playwright context settings                 |

### StealthyFetcher (Anti-Detection)

Advanced anti-bot fetcher for bypassing protection systems.

```python
from scrapling import StealthyFetcher, AsyncStealthyFetcher
```

#### Methods

| Method        | Signature                                | Description                 |
| ------------- | ---------------------------------------- | --------------------------- |
| `fetch`       | `fetch(url, **kwargs) -> Response`       | Stealth fetch with anti-bot |
| `async_fetch` | `async_fetch(url, **kwargs) -> Response` | Async stealth fetch         |

#### Parameters

All DynamicFetcher parameters plus:

| Parameter          | Type | Description                               |
| ------------------ | ---- | ----------------------------------------- |
| `solve_cloudflare` | bool | Automatically solve Cloudflare challenges |
| `block_webrtc`     | bool | Block WebRTC to prevent IP leaks          |
| `hide_canvas`      | bool | Add random noise to canvas operations     |
| `allow_webgl`      | bool | Enable WebGL support (default: True)      |

**Important Notes:**

-   `solve_cloudflare` requires timeout of at least 60 seconds
-   Works with proxies and other stealth options
-   Use `wait_selector` after solving to wait for real content

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

HTTP session with cookie persistence and connection pooling.

```python
from scrapling import FetcherSession

with FetcherSession() as session:
    session.get('https://example.com')
    session.get('https://example.com/page2')  # Cookies maintained
```

**Benefits:**

-   10x faster than creating sessions per request
-   Automatic cookie handling across requests
-   Better memory and CPU usage
-   Centralized configuration

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

**Parameters:**

| Parameter   | Type | Description                                  |
| ----------- | ---- | -------------------------------------------- |
| `max_pages` | int  | Maximum concurrent browser tabs (default: 1) |

**How max_pages works:**

-   Creates a rotating pool of browser tabs
-   Each request gets a new tab (old tabs closed after use)
-   If max_pages reached, waits up to 60 seconds for availability
-   Allows concurrent URL fetching in the same browser

### StealthySession / AsyncStealthySession

Stealth browser session with consistent fingerprint.

```python
from scrapling import StealthySession

with StealthySession(
    headless=True,
    real_chrome=True,
    block_webrtc=True,
    solve_cloudflare=True
) as session:
    page = session.fetch('https://protected-site.com')
```

**Session Benefits:**

-   Browser reuse: Much faster subsequent requests
-   Cookie persistence: Automatic session state handling
-   Consistent fingerprint: Same browser fingerprint across requests
-   Memory efficiency: Better resource usage than new browsers per fetch

### ProxyRotator

Automatic proxy rotation for sessions.

```python
from scrapling.fetchers import ProxyRotator

rotator = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
    "http://proxy3:8080",
])

# Use with any session
with FetcherSession(proxy_rotator=rotator) as session:
    page1 = session.get('https://example1.com')  # Uses proxy1
    page2 = session.get('https://example2.com')  # Uses proxy2
```

**Notes:**

-   Cannot be combined with `proxy` parameter
-   Each request automatically uses the next proxy in rotation
-   Check `page.meta['proxy']` to see which proxy was used
-   With browser-based sessions, creates separate context per proxy

---

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

**Notes:**

-   `body` is always bytes (since v0.4)
-   `meta` contains useful info like proxy used, mainly for spider systems

---

## Configuration Options

### Parser Configuration

All fetchers share parser configuration:

```python
from scrapling import Fetcher

# Global configuration
Fetcher.configure(adaptive=True, keep_comments=False, keep_cdata=False)

# Or direct assignment
Fetcher.adaptive = True
Fetcher.keep_comments = False
Fetcher.huge_tree = True

# Display current config
Fetcher.display_config()
```

**Available Options:**

| Parameter         | Description                               |
| ----------------- | ----------------------------------------- |
| `adaptive`        | Enable adaptive element relocation        |
| `adaptive_domain` | Domain for adaptive storage               |
| `huge_tree`       | Enable huge tree mode for large documents |
| `keep_comments`   | Keep HTML comments in parsed tree         |
| `keep_cdata`      | Keep CDATA sections in parsed tree        |
| `storage`         | Custom storage backend for adaptive       |
| `storage_args`    | Arguments for custom storage              |

### Per-Request Configuration

```python
# Pass selector_config for per-request parsing options
page = Fetcher.get('https://example.com', selector_config={'adaptive': True})
```

### Browser Configuration

DynamicFetcher and StealthyFetcher support extensive browser configuration:

```python
page = DynamicFetcher.fetch(
    'https://example.com',
    # Network
    disable_resources=True,  # Block fonts, images, media
    blocked_domains={'ads.example.com', 'tracker.net'},
    network_idle=True,

    # Wait conditions
    wait_selector='.content',
    wait_selector_state='visible',
    timeout=30000,
    wait=1000,

    # Browser settings
    headless=True,
    real_chrome=True,
    locale='en-US',
    timezone_id='America/New_York',

    # Headers/Identity
    useragent='Mozilla/5.0...',
    extra_headers={'X-Custom': 'value'},
    google_search=True,

    # Automation
    page_action=my_function,
    init_script='/path/to/script.js',

    # Proxy
    proxy='http://user:pass@host:port',
    # OR
    proxy={'server': 'http://host:port', 'username': 'user', 'password': 'pass'},
)
```

---

## Impersonate Browser Options

For `Fetcher` class, available impersonate options:

| Browser | String values                                 |
| ------- | --------------------------------------------- |
| Chrome  | 'chrome', 'chrome110', 'chrome_android', etc. |
| Firefox | 'firefox', 'firefox102', etc.                 |
| Safari  | 'safari', 'safari15_5', 'safari_ios', etc.    |
| Edge    | 'edge', 'edge101', etc.                       |
| Tor     | 'tor'                                         |

Pass a list to randomly choose: `impersonate=['chrome', 'firefox', 'safari']`

---

## Wait Selector States

For `wait_selector_state` parameter:

| State      | Description                                                                     |
| ---------- | ------------------------------------------------------------------------------- |
| `attached` | Wait for element to be present in DOM (default)                                 |
| `detached` | Wait for element to not be present in DOM                                       |
| `visible`  | Wait for element to have non-empty bounding box and no visibility:hidden        |
| `hidden`   | Wait for element to be detached or have empty bounding box or visibility:hidden |
