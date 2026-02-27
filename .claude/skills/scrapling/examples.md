# Scrapling Examples

Extended examples and use cases for Scrapling.

## Table of Contents

1. [Basic Scraping](#basic-scraping)
2. [E-commerce Scraping](#e-commerce-scraping)
3. [Authentication & Sessions](#authentication--sessions)
4. [Anti-Bot Bypass](#anti-bot-bypass)
5. [Advanced Browser Automation](#advanced-browser-automation)
6. [Adaptive Parsing Workflows](#adaptive-parsing-workflows)
7. [Concurrent Scraping](#concurrent-scraping)
8. [Data Export Patterns](#data-export-patterns)
9. [Error Handling](#error-handling)

---

## Basic Scraping

### Extract Article Content

```python
from scrapling import Fetcher

page = Fetcher.get('https://news.example.com/article-123')

# Extract article metadata
title = page.css_first('h1.article-title::text', default='No title')
author = page.css_first('.author-name::text', default='Unknown')
date = page.css_first('time::attr(datetime)', default='')

# Extract article body (multiple paragraphs)
paragraphs = page.css('.article-body p::text')
content = '\n\n'.join([p.clean() for p in paragraphs])

print(f"Title: {title}")
print(f"Author: {author}")
print(f"Published: {date}")
print(f"\n{content}")
```

### Extract Table Data

```python
from scrapling import Fetcher

page = Fetcher.get('https://example.com/data-table')

table_rows = page.css('table.data tbody tr')
data = []

for row in table_rows:
    cells = row.css('td::text')
    if cells:
        data.append({
            'name': cells[0].clean(),
            'value': cells[1].clean(),
            'date': cells[2].clean()
        })

print(data)
```

### Extract Links with Filtering

```python
from scrapling import Fetcher

page = Fetcher.get('https://example.com')

# Get all external links
all_links = page.css('a::attr(href)')
external_links = [
    link for link in all_links
    if link and link.startswith('http') and 'example.com' not in link
]

# Get links with specific text
contact_links = page.css('a').filter(lambda s: 'contact' in s.text.lower())
```

---

## E-commerce Scraping

### Product Catalog Scraping

```python
from scrapling import Fetcher
from urllib.parse import urljoin

base_url = 'https://shop.example.com'
page = Fetcher.get(f'{base_url}/products')

products = page.css('.product-card')
results = []

for product in products:
    name = product.css_first('.product-name::text', default='N/A')
    price_text = product.css_first('.price::text', default='0')
    price = price_text.re_first(r'[\d,.]+', default='0')

    relative_url = product.css_first('a::attr(href)', default='')
    url = urljoin(base_url, relative_url)

    image = product.css_first('img::attr(src)', default='')
    rating = product.css_first('.rating::attr(data-rating)', default='0')

    results.append({
        'name': name.clean(),
        'price': float(price.replace(',', '')),
        'url': url,
        'image': urljoin(base_url, image),
        'rating': float(rating)
    })

print(f"Found {len(results)} products")
for p in results[:5]:
    print(f"  - {p['name']}: ${p['price']}")
```

### Multi-Page Product Scraping

```python
from scrapling import FetcherSession

def scrape_product_pages(base_url, max_pages=5):
    all_products = []

    with FetcherSession() as session:
        for page_num in range(1, max_pages + 1):
            url = f"{base_url}/products?page={page_num}"
            page = session.get(url)

            products = page.css('.product-item')
            if not products:
                break  # No more products

            for product in products:
                all_products.append({
                    'name': product.css_first('.name::text', default=''),
                    'price': product.css_first('.price::text', default=''),
                })

    return all_products
```

### Amazon Product Scraping (Protected Site)

```python
from scrapling import StealthyFetcher

def scrape_amazon_product(url):
    # Use StealthyFetcher to bypass protection
    page = StealthyFetcher.fetch(url)

    # Extract product details
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

---

## Authentication & Sessions

### Login and Scrape Protected Content

```python
from scrapling import FetcherSession

with FetcherSession() as session:
    # Login
    login_response = session.post(
        'https://example.com/login',
        data={
            'username': 'myuser',
            'password': 'mypassword'
        }
    )

    # Check if login successful
    if 'dashboard' in login_response.url or login_response.status == 200:
        print("Login successful")

        # Access protected pages
        profile = session.get('https://example.com/profile')
        orders = session.get('https://example.com/orders')

        # Extract data from protected pages
        username = profile.css_first('.username::text')
        order_count = len(orders.css('.order-item'))
        print(f"User: {username}, Orders: {order_count}")
```

### Cookie-Based Authentication

```python
from scrapling import Fetcher

# Use existing cookies
cookies = {
    'session_id': 'abc123',
    'auth_token': 'xyz789'
}

page = Fetcher.get(
    'https://example.com/dashboard',
    cookies=cookies
)
```

### Browser Session with Cookie Persistence

```python
from scrapling import DynamicSession

with DynamicSession(
    headless=True,
    disable_resources=True,
    real_chrome=True
) as session:
    # Login through browser
    login_page = session.fetch('https://example.com/login')

    def do_login(page):
        page.fill('input[name="username"]', 'myuser')
        page.fill('input[name="password"]', 'mypassword')
        page.click('button[type="submit"]')
        page.wait_for_selector('.dashboard')
        return page

    dashboard = session.fetch(
        'https://example.com/login',
        page_action=do_login
    )

    # Subsequent requests maintain cookies
    profile = session.fetch('https://example.com/profile')
```

---

## Anti-Bot Bypass

### Cloudflare-Protected Site

```python
from scrapling import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://protected-site.com',
    solve_cloudflare=True,
    block_webrtc=True,
    real_chrome=True,
    headless=True,
    timeout=60000  # 60 seconds for Cloudflare
)

# Check if bypass successful
if page.status == 200:
    content = page.get_all_text()
    print(f"Successfully fetched {len(content)} characters")
```

### Stealth Mode with Full Protection

```python
from scrapling import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://bot-check.example.com',
    solve_cloudflare=True,
    block_webrtc=True,
    hide_canvas=True,
    real_chrome=True,
    headless=True,
    google_search=True,
    proxy='http://username:password@host:port'
)

# Verify stealth
user_agent = page.css_first('meta[name="user-agent"]::attr(content)', default='')
print(f"Detected as: {user_agent}")
```

### Rotating Proxies with Stealth

```python
from scrapling import StealthyFetcher
from scrapling.fetchers import ProxyRotator

# Set up proxy rotation
rotator = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
    "http://proxy3:8080",
])

# Use with session
with StealthyFetcher.session(proxy_rotator=rotator, headless=True) as session:
    page1 = session.fetch('https://example1.com')
    page2 = session.fetch('https://example2.com')

    # Override rotator for specific request
    page3 = session.fetch('https://example3.com', proxy='http://specific-proxy:8080')
```

### Stealthy Session with Multiple Protections

```python
from scrapling import StealthySession

with StealthySession(
    headless=True,
    real_chrome=True,
    block_webrtc=True,
    solve_cloudflare=True,
    timeout=60000
) as session:
    # Make multiple requests with the same browser instance
    page1 = session.fetch('https://example1.com')
    page2 = session.fetch('https://example2.com')
    page3 = session.fetch('https://nopecha.com/demo/cloudflare')
```

---

## Advanced Browser Automation

### Form Submission

```python
from scrapling import DynamicFetcher
from playwright.sync_api import Page

def fill_and_submit_form(page: Page):
    # Fill form fields
    page.fill('input[name="firstname"]', 'John')
    page.fill('input[name="lastname"]', 'Doe')
    page.fill('input[name="email"]', 'john.doe@example.com')
    page.fill('input[name="phone"]', '555-1234')

    # Select dropdown
    page.select_option('select[name="country"]', 'US')

    # Check checkbox
    page.check('input[name="newsletter"]')

    # Submit form
    page.click('button[type="submit"]')

    # Wait for result
    page.wait_for_selector('.confirmation-message')

    return page

page = DynamicFetcher.fetch(
    'https://example.com/contact-form',
    headless=True,
    page_action=fill_and_submit_form
)

confirmation = page.css_first('.confirmation-message::text')
print(f"Result: {confirmation}")
```

### Infinite Scroll Handling

```python
from scrapling import DynamicFetcher
from playwright.sync_api import Page

def scroll_to_bottom(page: Page):
    # Get initial height
    last_height = page.evaluate('() => document.body.scrollHeight')

    while True:
        # Scroll to bottom
        page.evaluate('() => window.scrollTo(0, document.body.scrollHeight)')

        # Wait for content to load
        page.wait_for_timeout(2000)

        # Check if new content loaded
        new_height = page.evaluate('() => document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

    return page

page = DynamicFetcher.fetch(
    'https://example.com/infinite-scroll',
    headless=True,
    network_idle=True,
    page_action=scroll_to_bottom
)

# Now all content is loaded
items = page.css('.scroll-item')
print(f"Total items: {len(items)}")
```

### Mouse Automation

```python
from scrapling import DynamicFetcher
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

### Wait Conditions

```python
from scrapling import DynamicFetcher

# Wait for specific selector to be visible
page = DynamicFetcher.fetch(
    'https://example.com',
    wait_selector='.content',
    wait_selector_state='visible'
)

# Wait for element to be removed
page = DynamicFetcher.fetch(
    'https://example.com',
    wait_selector='.loading-spinner',
    wait_selector_state='detached'
)

# Combined with network idle
page = DynamicFetcher.fetch(
    'https://example.com',
    network_idle=True,
    wait_selector='h1'
)
```

### Screenshot and PDF Generation

```python
from scrapling import DynamicFetcher
from playwright.sync_api import Page

def take_screenshot(page: Page):
    page.screenshot(path='screenshot.png', full_page=True)
    return page

page = DynamicFetcher.fetch(
    'https://example.com',
    headless=True,
    page_action=take_screenshot
)
```

### Downloading Files

```python
from scrapling import Fetcher

# Static file download
page = Fetcher.get('https://raw.githubusercontent.com/D4Vinci/Scrapling/main/images/main_cover.png')
with open(file='main_cover.png', mode='wb') as f:
    f.write(page.body)

# Dynamic file download
from scrapling import DynamicFetcher
from playwright.sync_api import Page

def download_file(page: Page):
    with page.expect_download() as download_info:
        page.click('a#download-link')
    download = download_info.value
    download.save_as('/path/to/save/file.pdf')
    return page

page = DynamicFetcher.fetch(
    'https://example.com/download-page',
    page_action=download_file
)
```

---

## Adaptive Parsing Workflows

### Initial Setup with Auto-Save

```python
from scrapling import StealthyFetcher

# Enable adaptive parsing globally
StealthyFetcher.adaptive = True

# First scrape - save element properties
page = StealthyFetcher.fetch('https://example.com/products')

# Save important elements with auto_save
products = page.css('.product-item', auto_save=True)
prices = page.css('.product-price', auto_save=True)
names = page.css('.product-name', auto_save=True)

for product in products:
    name = product.css_first('.product-name::text')
    price = product.css_first('.product-price::text')
    print(f"Saved: {name} - {price}")
```

### Adaptive Retrieval After Site Changes

```python
from scrapling import StealthyFetcher

StealthyFetcher.adaptive = True

# Later, after website redesign changes CSS classes...
page = StealthyFetcher.fetch('https://example.com/products')

# These will find elements even if selectors changed
products = page.css('.product-item', adaptive=True)  # May have changed to .item
prices = page.css('.product-price', adaptive=True)   # May have changed to .price

print(f"Found {len(products)} products using adaptive matching")

for product in products:
    name = product.css_first('.product-name::text', adaptive=True)
    price = product.css_first('.product-price::text', adaptive=True)
    print(f"Located: {name} - {price}")
```

### Custom Identifiers for Critical Elements

```python
from scrapling import Fetcher

page = Fetcher.get('https://example.com')

# Save with custom identifiers
main_price = page.css_first('.price', auto_save=True, identifier='main_price')
add_to_cart = page.css_first('.add-to-cart', auto_save=True, identifier='cart_button')

# Later retrieve by same identifier
page2 = Fetcher.get('https://example.com')
price = page2.css('.price', adaptive=True, identifier='main_price')
cart_btn = page2.css('.add-to-cart', adaptive=True, identifier='cart_button')
```

---

## Concurrent Scraping

### Async with Semaphore (Rate Limiting)

```python
import asyncio
from scrapling import AsyncFetcher

async def scrape_with_limit(urls, max_concurrent=5):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url):
        async with semaphore:
            page = await AsyncFetcher.get(url)
            await asyncio.sleep(1)  # Rate limiting
            return {
                'url': url,
                'title': page.css_first('title::text', default=''),
                'status': page.status
            }

    tasks = [fetch_one(url) for url in urls]
    return await asyncio.gather(*tasks)

urls = [f'https://example.com/page/{i}' for i in range(1, 101)]
results = asyncio.run(scrape_with_limit(urls, max_concurrent=5))

print(f"Scraped {len(results)} pages")
```

### Browser Tab Pool for Concurrent Scraping

```python
import asyncio
from scrapling import AsyncDynamicSession

async def scrape_multiple(urls):
    async with AsyncDynamicSession(max_pages=5) as session:
        tasks = [session.fetch(url) for url in urls]
        pages = await asyncio.gather(*tasks)

        results = []
        for page in pages:
            results.append({
                'title': page.css_first('title::text', default=''),
                'h1': page.css_first('h1::text', default=''),
                'status': page.status
            })

        return results

urls = ['https://site1.com', 'https://site2.com', 'https://site3.com']
results = asyncio.run(scrape_multiple(urls))
```

### Async Stealthy Session

```python
import asyncio
from scrapling import AsyncStealthySession

async def scrape_protected_sites():
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

results = asyncio.run(scrape_protected_sites())
```

---

## Data Export Patterns

### Export to JSON

```python
from scrapling import Fetcher
import json

page = Fetcher.get('https://example.com/products')
products = page.css('.product')

data = []
for product in products:
    data.append({
        'name': str(product.css_first('.name::text', default='')),
        'price': str(product.css_first('.price::text', default='')),
        'url': str(product.css_first('a::attr(href)', default=''))
    })

with open('products.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Export to CSV

```python
from scrapling import Fetcher
import csv

page = Fetcher.get('https://example.com/data')
rows = page.css('table tr')[1:]  # Skip header

with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Value', 'Date'])  # Header

    for row in rows:
        cells = row.css('td::text')
        writer.writerow([str(c.clean()) for c in cells])
```

### Export to Markdown

```python
from scrapling import Fetcher

page = Fetcher.get('https://example.com/article')

# Extract and format as markdown
title = page.css_first('h1::text', default='Untitled')
author = page.css_first('.author::text', default='Unknown')
content = page.css('.content p::text')

markdown = f"""# {title}

**Author:** {author}

"""

for para in content:
    markdown += f"{para.clean()}\n\n"

with open('article.md', 'w') as f:
    f.write(markdown)
```

---

## Error Handling

### Graceful Degradation

```python
from scrapling import Fetcher, DynamicFetcher

def scrape_robust(url):
    try:
        # Try static fetcher first
        page = Fetcher.get(url, timeout=10)
        if page.status == 200 and len(page.css('body')) > 0:
            return page
    except Exception:
        pass

    try:
        # Fall back to dynamic fetcher
        page = DynamicFetcher.fetch(url, headless=True, network_idle=True)
        return page
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

page = scrape_robust('https://example.com')
if page:
    print(f"Success: {page.css_first('title::text')}")
```

### Retry with Exponential Backoff

```python
import asyncio
from scrapling import AsyncFetcher

async def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            page = await AsyncFetcher.get(url, timeout=30)
            if page.status == 200:
                return page
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # 1, 2, 4 seconds
            await asyncio.sleep(wait_time)

    return None
```

### Handling Missing Elements

```python
from scrapling import Fetcher

page = Fetcher.get('https://example.com')

# Use default parameter
price = page.css_first('.price::text', default='N/A')

# Or check if element exists
price_elem = page.css_first('.price')
if price_elem:
    price = price_elem.text
else:
    price = 'Not available'

# Check collection length
products = page.css('.product')
if len(products) == 0:
    print("No products found")
```

### Pagination with Error Handling

```python
from scrapling import Fetcher

def scrape_all_pages(base_url):
    page_num = 1
    all_products = []

    while True:
        try:
            url = f"{base_url}?page={page_num}"
            page = Fetcher.get(url, timeout=30)

            if page.status != 200:
                print(f"Failed to fetch page {page_num}: {page.status}")
                break

            products = page.css('.product')
            if not products:
                break

            for product in products:
                all_products.append({
                    'name': product.css_first('.name::text', default=''),
                    'price': product.css_first('.price::text', default=''),
                })

            page_num += 1

        except Exception as e:
            print(f"Error on page {page_num}: {e}")
            break

    return all_products
```
