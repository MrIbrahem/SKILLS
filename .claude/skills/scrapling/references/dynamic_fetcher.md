# Dynamic Fetcher (DynamicFetcher)

The `DynamicFetcher` class provides flexible browser automation with Playwright, supporting multiple configuration options and under-the-hood stealth improvements.

## Import

```python
from scrapling import DynamicFetcher, AsyncDynamicFetcher
```

## Basic Usage

```python
# Basic fetch (uses Chromium)
page = DynamicFetcher.fetch('https://example.com')

# Use real Chrome browser
page = DynamicFetcher.fetch('https://example.com', real_chrome=True)

# Connect to remote browser via CDP
page = DynamicFetcher.fetch('https://example.com', cdp_url='ws://localhost:9222')
```

## Run Options

### 1. Vanilla Playwright

```python
DynamicFetcher.fetch('https://example.com')
```

Opens Chromium with optimizations and basic stealth. No extra features unless enabled.

### 2. Real Chrome

```python
DynamicFetcher.fetch('https://example.com', real_chrome=True)
```

Uses your locally installed Google Chrome for more authentic requests.

Install Chrome for Playwright:

```bash
playwright install chrome
```

### 3. CDP Connection

```python
DynamicFetcher.fetch('https://example.com', cdp_url='ws://localhost:9222')
```

Connects to a remote browser through Chrome DevTools Protocol.

## Parameters

| Parameter             | Type     | Default    | Description                                            |
| --------------------- | -------- | ---------- | ------------------------------------------------------ |
| `url`                 | str      | required   | Target URL                                             |
| `headless`            | bool     | True       | Run browser in headless/hidden mode                    |
| `disable_resources`   | bool     | False      | Drop unnecessary resource requests for speed           |
| `cookies`             | dict     | None       | Set cookies for the request                            |
| `useragent`           | str      | None       | Custom user agent (auto-generated if not set)          |
| `network_idle`        | bool     | False      | Wait until no network connections for 500ms            |
| `load_dom`            | bool     | True       | Wait for DOMContentLoaded state                        |
| `timeout`             | int      | 30000      | Timeout in milliseconds for all operations             |
| `wait`                | int      | 0          | Extra wait time after page loads (milliseconds)        |
| `page_action`         | callable | None       | Function for browser automation                        |
| `wait_selector`       | str      | None       | CSS selector to wait for                               |
| `wait_selector_state` | str      | 'attached' | State to wait for: attached, detached, visible, hidden |
| `init_script`         | str      | None       | Path to JS file executed on page creation              |
| `google_search`       | bool     | True       | Set referer as Google search                           |
| `extra_headers`       | dict     | None       | Extra headers to add to request                        |
| `proxy`               | str/dict | None       | Proxy string or dict with server/user/pass             |
| `real_chrome`         | bool     | False      | Use locally installed Chrome                           |
| `locale`              | str      | None       | User locale (e.g., 'en-GB', 'de-DE')                   |
| `timezone_id`         | str      | None       | Browser timezone                                       |
| `cdp_url`             | str      | None       | Connect to remote browser via CDP                      |
| `user_data_dir`       | str      | None       | Path to browser session data (sessions only)           |
| `extra_flags`         | list     | None       | Additional browser launch flags                        |
| `additional_args`     | dict     | None       | Additional Playwright context settings                 |
| `selector_config`     | dict     | None       | Custom parsing arguments for Response                  |
| `blocked_domains`     | set      | None       | Domains to block (subdomains also matched)             |
| `proxy_rotator`       | object   | None       | ProxyRotator instance for automatic rotation           |
| `retries`             | int      | 3          | Number of retry attempts                               |
| `retry_delay`         | int      | 1          | Seconds between retries                                |

## Browser Automation

### Page Action Function

```python
from playwright.sync_api import Page

def scroll_page(page: Page):
    page.mouse.wheel(10, 0)
    page.mouse.move(100, 400)
    page.mouse.up()
    return page

page = DynamicFetcher.fetch(
    'https://example.com',
    page_action=scroll_page
)
```

### Async Page Action

```python
from playwright.async_api import Page

async def scroll_page(page: Page):
    await page.mouse.wheel(10, 0)
    await page.mouse.move(100, 400)
    await page.mouse.up()
    return page

page = await DynamicFetcher.async_fetch(
    'https://example.com',
    page_action=scroll_page
)
```

## Wait Conditions

### Wait for Selector

```python
page = DynamicFetcher.fetch(
    'https://example.com',
    wait_selector='h1',
    wait_selector_state='visible'
)
```

Available states:

-   `attached`: Element present in DOM (default)
-   `detached`: Element not present in DOM
-   `visible`: Element has non-empty bounding box and no visibility:hidden
-   `hidden`: Element is detached or has empty bounding box or visibility:hidden

### Network Idle

```python
page = DynamicFetcher.fetch(
    'https://example.com',
    network_idle=True
)
```

## Resource Control

### Disable Unnecessary Resources

```python
page = DynamicFetcher.fetch(
    'https://example.com',
    disable_resources=True  # Blocks fonts, images, media, etc.
)
```

Resources dropped: `font`, `image`, `media`, `beacon`, `object`, `imageset`, `texttrack`, `websocket`, `csp_report`, `stylesheet`

**Note:** Can make requests ~25% faster, but may cause some websites to never finish loading.

### Block Specific Domains

```python
page = DynamicFetcher.fetch(
    'https://example.com',
    blocked_domains={"ads.example.com", "tracker.net"}
)
```

## Proxy Configuration

### Single Proxy

```python
# As string
page = DynamicFetcher.fetch(
    'https://example.com',
    proxy='http://username:password@host:port'
)

# As dict
page = DynamicFetcher.fetch(
    'https://example.com',
    proxy={
        'server': 'http://host:port',
        'username': 'user',
        'password': 'pass'
    }
)
```

### Proxy Rotation

```python
from scrapling.fetchers import ProxyRotator

rotator = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
])

page = DynamicFetcher.fetch(
    'https://example.com',
    proxy_rotator=rotator
)
```

## Sessions

### DynamicSession

```python
from scrapling import DynamicSession

with DynamicSession(
    headless=True,
    disable_resources=True,
    real_chrome=True
) as session:
    page1 = session.fetch('https://example1.com')
    page2 = session.fetch('https://example2.com')
    page3 = session.fetch('https://dynamic-site.com')
```

### AsyncDynamicSession

```python
import asyncio
from scrapling import AsyncDynamicSession

async def scrape_multiple():
    async with AsyncDynamicSession(
        network_idle=True,
        timeout=30000,
        max_pages=3
    ) as session:
        pages = await asyncio.gather(
            session.fetch('https://spa-app1.com'),
            session.fetch('https://spa-app2.com'),
            session.fetch('https://dynamic-content.com')
        )
        return pages
```

### Session with Tab Pool

The `max_pages` argument enables a rotating pool of browser tabs:

```python
with DynamicSession(max_pages=5) as session:
    # Each fetch creates a new tab, closes old finished tabs
    # If max_pages reached, waits up to 60 seconds
    page1 = session.fetch('https://site1.com')
    page2 = session.fetch('https://site2.com')
```

## Examples

### General Dynamic Scraping

```python
from scrapling import DynamicFetcher

def scrape_dynamic_content():
    page = DynamicFetcher.fetch(
        'https://example.com/dynamic',
        network_idle=True,
        wait_selector='.content'
    )

    content = page.css('.content')

    return {
        'title': content.css('h1::text').get(),
        'items': [
            item.text for item in content.css('.item')
        ]
    }
```

### Downloading Files

```python
page = DynamicFetcher.fetch(
    'https://raw.githubusercontent.com/.../image.png'
)

with open('image.png', 'wb') as f:
    f.write(page.body)
```

### Form Automation

```python
from playwright.sync_api import Page

def fill_form(page: Page):
    page.fill('input[name="search"]', 'query')
    page.click('button[type="submit"]')
    page.wait_for_selector('.results')
    return page

page = DynamicFetcher.fetch(
    'https://example.com/search',
    page_action=fill_form
)

results = page.css('.result-item')
```

## When to Use

Use DynamicFetcher when:

-   Need browser automation
-   Want multiple browser options (Chromium/Chrome/CDP)
-   Using a real Chrome browser
-   Need custom browser configuration
-   Want basic stealth options
-   Website uses JavaScript to load content

If you need more stealth and control without much config, use StealthyFetcher.
