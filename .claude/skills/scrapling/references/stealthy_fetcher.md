# Stealthy Fetcher (StealthyFetcher)

The `StealthyFetcher` class provides advanced anti-bot protection bypass capabilities, handling most protections automatically under the hood.

## Import

```python
from scrapling import StealthyFetcher, AsyncStealthyFetcher
```

## What It Does

1. **Cloudflare Bypass**: Automatically solves all types of Cloudflare's Turnstile/Interstitial
2. **CDP Protection**: Bypasses CDP runtime leaks
3. **WebRTC Protection**: Prevents local IP address leaks
4. **JS Execution Isolation**: Isolates JS execution and removes Playwright fingerprints
5. **Canvas Noise**: Generates canvas noise to prevent fingerprinting
6. **Headless Detection**: Patches known methods to detect running in headless mode
7. **Timezone Mismatch**: Option to defeat timezone mismatch attacks
8. **Google Referer**: Makes requests look like they came from Google search

## Basic Usage

```python
# Basic stealth fetch
page = StealthyFetcher.fetch('https://protected-site.com')

# With Cloudflare solver
page = StealthyFetcher.fetch(
    'https://nopecha.com/demo/cloudflare',
    solve_cloudflare=True
)
```

## Parameters

All DynamicFetcher parameters plus:

| Parameter          | Type | Default | Description                                        |
| ------------------ | ---- | ------- | -------------------------------------------------- |
| `solve_cloudflare` | bool | False   | Solve Cloudflare Turnstile/Interstitial challenges |
| `block_webrtc`     | bool | False   | Force WebRTC to respect proxy settings             |
| `hide_canvas`      | bool | False   | Add random noise to canvas operations              |
| `allow_webgl`      | bool | True    | Enable WebGL support (disable = more stealth)      |

### Notes

-   `solve_cloudflare`: Requires timeout of at least 60 seconds
-   `disable_resources`: Same as DynamicFetcher (~25% faster but may break some sites)
-   `google_search`: Enabled by default, sets referer from Google search

## Cloudflare Solver

The `solve_cloudflare` parameter handles:

-   JavaScript challenges (managed)
-   Interactive challenges (clicking verification boxes)
-   Invisible challenges (automatic background verification)
-   Custom pages with embedded captcha

### Important Notes

1. **Wait for content**: Some sites need `wait_selector` to wait for real content after solving
2. **Timeout**: Should be at least 60 seconds when using Cloudflare solver
3. **Proxy support**: Works seamlessly with proxies and other stealth options

### Example with Cloudflare

```python
page = StealthyFetcher.fetch(
    'https://protected-site.com',
    solve_cloudflare=True,
    timeout=60000,
    wait_selector='.main-content'  # Wait for real content
)
```

## Stealth Options

### Full Protection

```python
page = StealthyFetcher.fetch(
    'https://protected-site.com',
    solve_cloudflare=True,
    block_webrtc=True,
    hide_canvas=True,
    real_chrome=True,
    headless=True,
    google_search=True,
    proxy='http://username:password@host:port'
)
```

### Stealth with Locale/Timezone

```python
page = StealthyFetcher.fetch(
    'https://protected-site.com',
    solve_cloudflare=True,
    block_webrtc=True,
    locale='en-US',
    timezone_id='America/New_York',
    useragent='Mozilla/5.0...'
)
```

## Sessions

### StealthySession

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

## Real-World Examples

### Amazon Product Scraping

```python
def scrape_amazon_product(url):
    page = StealthyFetcher.fetch(url)

    return {
        'title': page.css_first('#productTitle::text').get().clean(),
        'price': page.css_first('.a-price .a-offscreen::text').get(),
        'rating': page.css_first('[data-feature-name="averageCustomerReviews"] .a-popover-trigger .a-color-base::text').get(),
        'reviews_count': page.css_first('#acrCustomerReviewText::text').re_first(r'[\d,]+'),
        'features': [
            li.get().clean() for li in page.css('#feature-bullets li span::text')
        ],
        'availability': page.css_first('#availability').get_all_text(strip=True),
        'images': [
            img.attrib['src'] for img in page.css('#altImages img')
        ]
    }
```

### Protected Site with Proxy

```python
page = StealthyFetcher.fetch(
    'https://bot-check.example.com',
    solve_cloudflare=True,
    block_webrtc=True,
    hide_canvas=True,
    real_chrome=True,
    headless=True,
    proxy='http://user:pass@proxy.com:8080'
)

# Check if bypassed
if page.status == 200:
    print(f"Success! Page length: {len(page.body)}")
```

## Camoufox Integration (Optional)

Before v0.3.13, StealthyFetcher used Camoufox as the engine. You can still use it:

### Install Camoufox

```bash
pip install camoufox
playwright install-deps firefox
camoufox fetch
```

### Custom StealthySession with Camoufox

```python
from scrapling.fetchers import StealthySession
from playwright.sync_api import sync_playwright
from camoufox.utils import launch_options as generate_launch_options

class CamoufoxSession(StealthySession):
    def start(self):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            launch_options = generate_launch_options(**{
                "geoip": False,
                "proxy": self._config.proxy,
                "headless": self._config.headless,
                "humanize": True if self._config.solve_cloudflare else False,
                "i_know_what_im_doing": True,
                "allow_webgl": self._config.allow_webgl,
                "block_webrtc": self._config.block_webrtc,
                "os": None,
                "user_data_dir": self._config.user_data_dir,
            })
            self.context = self.playwright.firefox.launch_persistent_context(**launch_options)
        else:
            raise RuntimeError("Session has been already started")

# Usage
with CamoufoxSession(solve_cloudflare=True, headless=True) as session:
    page = session.fetch('https://protected-site.com')
```

## When to Use

Use StealthyFetcher when:

-   Bypassing anti-bot protection (Cloudflare, DataDome, etc.)
-   Need reliable browser fingerprint
-   Full JavaScript support needed
-   Want automatic stealth features
-   Need browser automation with protections
-   Dealing with Cloudflare Turnstile/Interstitial

## Comparison with DynamicFetcher

| Feature           | DynamicFetcher | StealthyFetcher |
| ----------------- | -------------- | --------------- |
| Speed             | Medium         | Medium          |
| Stealth Level     | Moderate       | Maximum         |
| Cloudflare Solver | No             | Yes             |
| WebRTC Blocking   | No             | Yes             |
| Canvas Noise      | No             | Yes             |
| Setup Complexity  | Simple         | Simple          |

Both use Playwright/Patchright under the hood. StealthyFetcher adds anti-detection layers.
