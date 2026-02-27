# Static Fetcher (Fetcher)

The `Fetcher` class provides rapid and lightweight HTTP requests using the high-performance `curl_cffi` library with TLS fingerprinting and stealth capabilities.

## Import

```python
from scrapling import Fetcher, AsyncFetcher
```

## HTTP Methods

### GET

```python
# Basic GET
page = Fetcher.get('https://example.com')

# With parameters
page = Fetcher.get('https://example.com/search', params={'q': 'query'})

# With all options
page = Fetcher.get(
    'https://example.com',
    stealthy_headers=True,
    follow_redirects=True,
    proxy='http://username:password@localhost:8030',
    impersonate='chrome',
    http3=True
)
```

### POST

```python
# Form-encoded data
page = Fetcher.post(
    'https://example.com/submit',
    data={'username': 'user', 'password': 'pass'}
)

# JSON data
page = Fetcher.post(
    'https://example.com/api',
    json={'key': 'value'}
)

# With params and all options
page = Fetcher.post(
    'https://example.com/post',
    data={'key': 'value'},
    params={'q': 'query'},
    stealthy_headers=True,
    proxy='http://username:password@localhost:8030',
    impersonate='chrome'
)
```

### PUT

```python
page = Fetcher.put(
    'https://example.com/update',
    data={'status': 'updated'}
)
```

### DELETE

```python
page = Fetcher.delete('https://example.com/resource/123')
```

## Parameters

### Common Parameters (All Methods)

| Parameter          | Type   | Default  | Description                                      |
| ------------------ | ------ | -------- | ------------------------------------------------ |
| `url`              | str    | required | Target URL                                       |
| `stealthy_headers` | bool   | True     | Generate realistic browser headers automatically |
| `follow_redirects` | bool   | True     | Follow HTTP redirections                         |
| `timeout`          | float  | 30       | Request timeout in seconds                       |
| `retries`          | int    | 3        | Number of retries for failed requests            |
| `retry_delay`      | float  | 1        | Seconds to wait between retry attempts           |
| `impersonate`      | str    | 'chrome' | Browser TLS fingerprint to impersonate           |
| `http3`            | bool   | False    | Use HTTP/3 protocol                              |
| `cookies`          | dict   | None     | Cookies to send with request (name→value)        |
| `proxy`            | str    | None     | Proxy URL: 'http://user:pass@host:port'          |
| `proxy_auth`       | tuple  | None     | HTTP basic auth: (username, password)            |
| `proxies`          | dict   | None     | Dict of proxies: {'http': url, 'https': url}     |
| `proxy_rotator`    | object | None     | ProxyRotator instance for automatic rotation     |
| `headers`          | dict   | None     | Custom HTTP headers (can override generated)     |
| `max_redirects`    | int    | 30       | Maximum redirects (-1 for unlimited)             |
| `verify`           | bool   | True     | Verify HTTPS certificates                        |
| `cert`             | tuple  | None     | Client certificate (cert, key) filenames         |
| `selector_config`  | dict   | None     | Custom parsing arguments for Response            |

### GET-Specific Parameters

| Parameter | Type | Default | Description          |
| --------- | ---- | ------- | -------------------- |
| `params`  | dict | None    | URL query parameters |

### POST/PUT-Specific Parameters

| Parameter | Type | Default | Description       |
| --------- | ---- | ------- | ----------------- |
| `data`    | dict | None    | Form-encoded data |
| `json`    | dict | None    | JSON request body |

## Impersonate Browser Options

| Browser | Available Values                              |
| ------- | --------------------------------------------- |
| Chrome  | 'chrome', 'chrome110', 'chrome_android', etc. |
| Firefox | 'firefox', 'firefox102', etc.                 |
| Safari  | 'safari', 'safari15_5', 'safari_ios', etc.    |
| Edge    | 'edge', 'edge101', etc.                       |
| Tor     | 'tor'                                         |

Pass a list to randomly rotate: `impersonate=['chrome', 'firefox', 'safari']`

## Async Usage

All methods have async equivalents:

```python
from scrapling import AsyncFetcher

# Async GET
page = await AsyncFetcher.get('https://example.com')

# Async POST
page = await AsyncFetcher.post(
    'https://example.com/api',
    json={'key': 'value'}
)

# Concurrent requests
import asyncio

urls = ['https://site1.com', 'https://site2.com', 'https://site3.com']
tasks = [AsyncFetcher.get(url) for url in urls]
pages = await asyncio.gather(*tasks)
```

## Examples

### Product Scraping

```python
from scrapling import Fetcher

page = Fetcher.get('https://example.com/products')
products = page.css('.product')

results = []
for product in products:
    results.append({
        'title': product.css_first('.title::text').get(),
        'price': product.css_first('.price::text').re_first(r'\d+\.\d{2}'),
        'description': product.css_first('.description::text').get(),
        'in_stock': product.has_class('in-stock')
    })
```

### Pagination Handling

```python
from scrapling import Fetcher

def scrape_all_pages():
    base_url = 'https://example.com/products?page={}'
    page_num = 1
    all_products = []

    while True:
        page = Fetcher.get(base_url.format(page_num))

        products = page.css('.product')
        if not products:
            break

        for product in products:
            all_products.append({
                'name': product.css_first('.name::text').get(),
                'price': product.css_first('.price::text').get(),
            })

        page_num += 1

    return all_products
```

### Form Submission

```python
from scrapling import Fetcher

response = Fetcher.post(
    'https://example.com/login',
    data={
        'username': 'user@example.com',
        'password': 'password123'
    }
)

if response.status == 200:
    user_name = response.css_first('.user-name::text').get()
    print(f"Logged in as: {user_name}")
```

### Downloading Files

```python
from scrapling import Fetcher

page = Fetcher.get('https://example.com/file.pdf')

with open('file.pdf', 'wb') as f:
    f.write(page.body)
```

## When to Use

Use `Fetcher` when:

-   Need rapid HTTP requests
-   Want minimal overhead
-   Don't need JavaScript execution
-   Target website can be scraped through requests
-   Need basic stealth (TLS fingerprinting)

Use `FetcherSession` when:

-   Making multiple requests to same or different sites
-   Need cookie persistence between requests
-   Want connection pooling for better performance
-   Require consistent configuration across requests
-   Working with APIs requiring session state
