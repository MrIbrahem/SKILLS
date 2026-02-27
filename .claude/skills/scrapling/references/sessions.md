# Sessions in Scrapling

Sessions provide persistent connections, cookie handling, and resource reuse across multiple requests.

## Session Types

| Session Class     | Use Case                              | Async Version            |
| ----------------- | ------------------------------------- | ------------------------ |
| `FetcherSession`  | HTTP requests with cookie persistence | Same class (auto-detect) |
| `DynamicSession`  | Browser automation                    | `AsyncDynamicSession`    |
| `StealthySession` | Anti-bot protected browsing           | `AsyncStealthySession`   |

## FetcherSession

HTTP session using `curl_cffi` with cookie persistence and connection pooling.

### Basic Usage

```python
from scrapling import FetcherSession

with FetcherSession() as session:
    page1 = session.get('https://example.com')
    page2 = session.get('https://example.com/page2')  # Cookies maintained
```

### With Configuration

```python
with FetcherSession(
    impersonate='chrome',
    http3=True,
    stealthy_headers=True,
    timeout=30,
    retries=3
) as session:
    page1 = session.get('https://scrapling.requestcatcher.com/get')
    page2 = session.post('https://scrapling.requestcatcher.com/post', data={'key': 'value'})
```

### Proxy Rotation

```python
from scrapling.fetchers import ProxyRotator

rotator = ProxyRotator([
    'http://proxy1:8080',
    'http://proxy2:8080',
    'http://proxy3:8080',
])

with FetcherSession(proxy_rotator=rotator, impersonate='chrome') as session:
    # Each request uses next proxy in rotation
    page1 = session.get('https://example.com/page1')
    page2 = session.get('https://example.com/page2')

    # Check which proxy was used
    print(page1.meta['proxy'])
```

### Per-Request Overrides

```python
with FetcherSession(proxy='http://default-proxy:8080') as session:
    # Uses session proxy
    page1 = session.get('https://example.com/page1')

    # Override for specific request
    page2 = session.get('https://example.com/page2', proxy='http://special-proxy:9090')
```

### Async Usage

```python
async with FetcherSession(impersonate='firefox', http3=True) as session:
    response = await session.get('https://example.com')
    response = await session.post('https://example.com/api', json={'data': 'value'})
```

### Benefits

-   **10x faster** than creating sessions per request
-   **Cookie persistence** across requests
-   **Resource efficiency** with connection pooling
-   **Centralized configuration**

## DynamicSession

Browser session with tab pool management for JavaScript-heavy sites.

### Basic Usage

```python
from scrapling import DynamicSession

with DynamicSession(
    headless=True,
    disable_resources=True,
    real_chrome=True
) as session:
    page1 = session.fetch('https://example1.com')
    page2 = session.fetch('https://example2.com')
```

### With Tab Pool

```python
with DynamicSession(max_pages=3) as session:
    # Creates up to 3 concurrent tabs
    page1 = session.fetch('https://site1.com')
    page2 = session.fetch('https://site2.com')
    page3 = session.fetch('https://site3.com')
```

### Per-Request Overrides

```python
with DynamicSession(headless=True) as session:
    # Uses session defaults
    page1 = session.fetch('https://example1.com')

    # Override for specific request
    page2 = session.fetch(
        'https://example2.com',
        wait_selector='.content',
        timeout=60000
    )
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

## StealthySession

Stealth browser session with anti-bot protection.

### Basic Usage

```python
from scrapling import StealthySession

with StealthySession(
    headless=True,
    real_chrome=True,
    block_webrtc=True,
    solve_cloudflare=True
) as session:
    page1 = session.fetch('https://example1.com')
    page2 = session.fetch('https://example2.com')
    page3 = session.fetch('https://nopecha.com/demo/cloudflare')
```

### With Tab Pool

```python
with StealthySession(
    headless=True,
    solve_cloudflare=True,
    max_pages=2
) as session:
    page1 = session.fetch('https://site1.com')
    page2 = session.fetch('https://site2.com')
```

### AsyncStealthySession

```python
import asyncio
from scrapling import AsyncStealthySession

async def scrape_protected():
    async with AsyncStealthySession(
        real_chrome=True,
        block_webrtc=True,
        solve_cloudflare=True,
        timeout=60000,
        max_pages=3
    ) as session:
        pages = await asyncio.gather(
            session.fetch('https://site1.com'),
            session.fetch('https://site2.com'),
            session.fetch('https://protected-site.com')
        )
        return pages
```

## Tab Pool (max_pages)

The `max_pages` argument creates a rotating pool of browser tabs:

### How It Works

1. Each request creates a new tab
2. Finished tabs are automatically closed
3. If `max_pages` reached, waits up to 60 seconds
4. Allows concurrent URL fetching in same browser

### Example

```python
with DynamicSession(max_pages=5) as session:
    # All these can run concurrently
    tasks = [
        session.fetch('https://site1.com'),
        session.fetch('https://site2.com'),
        session.fetch('https://site3.com'),
        session.fetch('https://site4.com'),
        session.fetch('https://site5.com'),
    ]
```

### Benefits

-   **Resource efficiency**: Reuse same browser instance
-   **Speed**: Concurrent tab execution
-   **Memory management**: Old tabs cleaned up automatically
-   **Consistency**: Same browser fingerprint across tabs

## ProxyRotator

Automatic proxy rotation for sessions.

### Setup

```python
from scrapling.fetchers import ProxyRotator

rotator = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
    "http://proxy3:8080",
])
```

### Usage with Sessions

```python
# HTTP session
with FetcherSession(proxy_rotator=rotator) as session:
    page1 = session.get('https://example1.com')  # Uses proxy1
    page2 = session.get('https://example2.com')  # Uses proxy2

# Browser session
with DynamicSession(proxy_rotator=rotator) as session:
    page1 = session.fetch('https://example1.com')
    page2 = session.fetch('https://example2.com')
```

### Important Notes

-   Cannot be combined with `proxy` parameter
-   Each request uses the next proxy in rotation
-   Check `page.meta['proxy']` to see which was used
-   With browser sessions: creates separate context per proxy (browsers can't set proxy per tab)

## Session Benefits Summary

| Benefit             | Description                                            |
| ------------------- | ------------------------------------------------------ |
| Cookie Persistence  | Automatic cookie and session state handling            |
| Connection Reuse    | Much faster subsequent requests                        |
| Consistent Config   | Same settings applied to all requests                  |
| Resource Efficiency | Better memory/CPU usage vs new connections per request |
| Tab Pool Management | Concurrent requests with controlled resource usage     |
| Proxy Rotation      | Automatic proxy switching across requests              |

## When to Use Sessions

Use sessions when:

-   Making multiple requests to same or different sites
-   Need cookie persistence between requests
-   Want connection pooling for better performance
-   Require consistent configuration across requests
-   Working with APIs requiring session state
-   Need concurrent browser tab management
-   Want automatic proxy rotation
