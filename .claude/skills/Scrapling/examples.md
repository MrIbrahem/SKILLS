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

---

## Anti-Bot Bypass

### Cloudflare-Protected Site

```python
from scrapling import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://protected-site.com',
    solve_cloudflare=True,
    humanize=True,
    geoip=True,
    headless=True,
    block_webrtc=True
)

# Check if bypass successful
if page.status == 200:
    content = page.get_all_text()
    print(f"Successfully fetched {len(content)} characters")
```

### Stealth Mode with Custom Fingerprint

```python
from scrapling import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://bot-check.example.com',
    solve_cloudflare=True,
    humanize=True,
    os='windows',           # Windows fingerprint
    block_images=True,      # Faster loading
    disable_ads=True,       # Block ads
    google_search=True      # Simulate from Google
)

# Verify stealth
user_agent = page.css_first('meta[name="user-agent"]::attr(content)', default='')
print(f"Detected as: {user_agent}")
```

### Rotating Proxies with Stealth

```python
from scrapling import StealthyFetcher
import random

proxies = [
    'http://user:pass@proxy1.com:8080',
    'http://user:pass@proxy2.com:8080',
    'http://user:pass@proxy3.com:8080',
]

for url in urls_to_scrape:
    proxy = random.choice(proxies)

    page = StealthyFetcher.fetch(
        url,
        proxy=proxy,
        solve_cloudflare=True,
        humanize=True,
        geoip=True  # Auto-match timezone to proxy location
    )

    # Process page...
```

---

## Advanced Browser Automation

### Form Submission

```python
from scrapling import DynamicFetcher

def fill_and_submit_form(page):
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

def scroll_to_bottom(page):
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

### Screenshot and PDF Generation

```python
from scrapling import DynamicFetcher

def take_screenshot(page):
    page.screenshot(path='screenshot.png', full_page=True)
    return page

page = DynamicFetcher.fetch(
    'https://example.com',
    headless=True,
    page_action=take_screenshot
)
```

---

## Adaptive Parsing Workflows

### Initial Setup with Auto-Save

```python
from scrapling import StealthyFetcher

# Enable adaptive parsing globally
StealthyFetcher.auto_match = True

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

StealthyFetcher.auto_match = True

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

## Error Handling Patterns

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
