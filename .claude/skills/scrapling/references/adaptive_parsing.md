# Adaptive Parsing

Adaptive parsing automatically relocates HTML elements when website structure changes, making scrapers more resilient.

## Overview

When websites redesign, CSS selectors often break. Adaptive parsing saves element properties on first run, then uses similarity scoring to find elements even if their HTML structure changes.

## How It Works

1. **Save Phase**: Extract and save element properties (text, attributes, position)
2. **Match Phase**: When selector fails, find elements by similarity to saved properties
3. **Relearn**: Update saved properties as needed

## Enabling Adaptive Parsing

### Global Configuration

```python
from scrapling import StealthyFetcher

# Enable for all requests
StealthyFetcher.adaptive = True

# Or with configure()
StealthyFetcher.configure(adaptive=True)
```

### Per-Request Configuration

```python
page = Fetcher.get(
    'https://example.com',
    selector_config={'adaptive': True}
)
```

## Using Adaptive Parsing

### Save Elements (First Run)

```python
from scrapling import StealthyFetcher

StealthyFetcher.adaptive = True

page = StealthyFetcher.fetch('https://example.com/products')

# Save elements with auto_save
products = page.css('.product-item', auto_save=True)
prices = page.css('.product-price', auto_save=True)
names = page.css('.product-name', auto_save=True)

for product in products:
    name = product.css_first('.product-name::text')
    price = product.css_first('.product-price::text')
    print(f"Saved: {name} - {price}")
```

### Retrieve Elements (After Site Changes)

```python
from scrapling import StealthyFetcher

StealthyFetcher.adaptive = True

# Later, after website redesign...
page = StealthyFetcher.fetch('https://example.com/products')

# Finds elements even if CSS classes changed
products = page.css('.product-item', adaptive=True)
prices = page.css('.product-price', adaptive=True)

print(f"Found {len(products)} products using adaptive matching")

for product in products:
    name = product.css_first('.product-name::text', adaptive=True)
    price = product.css_first('.product-price::text', adaptive=True)
    print(f"Located: {name} - {price}")
```

## Custom Identifiers

Use custom identifiers for critical elements:

```python
from scrapling import Fetcher

page = Fetcher.get('https://example.com')

# Save with custom identifier
main_price = page.css_first('.price', auto_save=True, identifier='main_price')
cart_button = page.css_first('.add-to-cart', auto_save=True, identifier='cart_button')

# Later retrieve by same identifier
page2 = Fetcher.get('https://example.com')
price = page2.css('.price', adaptive=True, identifier='main_price')
cart = page2.css('.add-to-cart', adaptive=True, identifier='cart_button')
```

## Manual Save/Retrieve

```python
from scrapling import Selector

# Create selector
selector = Selector(html=html, adaptive=True)

# Manually save element
element = selector.css_first('.important')
element.save('important_element')

# Later retrieve
selector2 = Selector(html=new_html, adaptive=True)
retrieved = selector2.css('.important', adaptive=True, identifier='important_element')
```

## Configuration Options

| Parameter         | Description                        |
| ----------------- | ---------------------------------- |
| `adaptive`        | Enable adaptive element relocation |
| `adaptive_domain` | Domain for adaptive storage        |
| `storage`         | Custom storage backend             |
| `storage_args`    | Arguments for custom storage       |

## Custom Storage Backend

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

## Best Practices

1. **Enable for production**: Use `auto_save=True` on initial scrapes
2. **Use custom identifiers**: For critical elements that must be found
3. **Test after site changes**: Verify adaptive matching still works
4. **Update saved properties**: Periodically re-save as sites evolve
5. **Combine with good selectors**: Adaptive is a fallback, not primary strategy

## When to Use

Use adaptive parsing when:

-   Building long-running scrapers
-   Target sites change frequently
-   Critical elements must always be found
-   Maintenance overhead needs to be minimized
