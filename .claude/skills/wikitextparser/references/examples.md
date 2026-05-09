# wikitextparser — Practical Examples

> Load this file when the user needs end-to-end scripts, real-world patterns, or multi-step workflows beyond quick snippets.

## Table of Contents

1. [Parse a Wikipedia article dump](#1-parse-a-wikipedia-article-dump)
2. [Extract all Infobox data as a dict](#2-extract-all-infobox-data-as-a-dict)
3. [Find and replace template arguments at scale](#3-find-and-replace-template-arguments-at-scale)
4. [Export all wiki tables to CSV](#4-export-all-wiki-tables-to-csv)
5. [Build a wikilink graph](#5-build-a-wikilink-graph)
6. [Strip markup for NLP / full-text search](#6-strip-markup-for-nlp--full-text-search)
7. [Audit duplicate template arguments](#7-audit-duplicate-template-arguments)
8. [Extract citations (ref tags)](#8-extract-citations-ref-tags)
9. [Rewrite section headings](#9-rewrite-section-headings)
10. [Convert list types across an article](#10-convert-list-types-across-an-article)
11. [Validate template required fields](#11-validate-template-required-fields)
12. [Collect all categories from an article](#12-collect-all-categories-from-an-article)
13. [Pretty-print all templates in a page](#13-pretty-print-all-templates-in-a-page)
14. [Nested template traversal](#14-nested-template-traversal)
15. [Find broken / empty wikilinks](#15-find-broken--empty-wikilinks)

---

## 1. Parse a Wikipedia article dump

```python
import wikitextparser as wtp

# From a string (e.g. loaded from a .xml dump or API response)
with open('article.txt', encoding='utf-8') as f:
    raw = f.read()

parsed = wtp.parse(raw)

print(f"Templates  : {len(parsed.templates)}")
print(f"Wikilinks  : {len(parsed.wikilinks)}")
print(f"Tables     : {len(parsed.tables)}")
print(f"Sections   : {len(parsed.sections)}")
print(f"Ext. links : {len(parsed.external_links)}")
```

---

## 2. Extract all Infobox data as a dict

```python
import wikitextparser as wtp

def extract_infobox(wikitext: str, template_name: str = None) -> dict:
    """
    Return {arg_name: arg_value} for the first matching infobox template.
    If template_name is None, returns the first template found.
    """
    parsed = wtp.parse(wikitext)
    for t in parsed.templates:
        name = t.normal_name(code='en').lower()
        if template_name is None or template_name.lower() in name:
            return {
                arg.name.strip(): arg.value.strip()
                for arg in t.arguments
                if not arg.positional
            }
    return {}

# Usage
data = extract_infobox(raw, template_name='infobox person')
print(data.get('birth_date'))
print(data.get('nationality'))
```

---

## 3. Find and replace template arguments at scale

```python
import wikitextparser as wtp

def rename_template_arg(wikitext: str, template: str, old_arg: str, new_arg: str) -> str:
    """Rename an argument across all instances of a template."""
    parsed = wtp.parse(wikitext)
    for t in parsed.templates:
        if t.normal_name(code='en').lower() == template.lower():
            arg = t.get_arg(old_arg)
            if arg:
                value = arg.value
                t.del_arg(old_arg)
                t.set_arg(new_arg, value)
    return str(parsed)

# Usage
updated = rename_template_arg(raw, 'Infobox person', 'birth_place', 'birthplace')
```

---

## 4. Export all wiki tables to CSV

```python
import csv
import io
import wikitextparser as wtp

def tables_to_csv(wikitext: str) -> list[str]:
    """Return list of CSV strings, one per table."""
    parsed = wtp.parse(wikitext)
    results = []
    for table in parsed.tables:
        rows = table.data()
        if not rows:
            continue
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerows(rows)
        results.append(buf.getvalue())
    return results

# Usage
csvs = tables_to_csv(raw)
for i, csv_str in enumerate(csvs):
    with open(f'table_{i}.csv', 'w') as f:
        f.write(csv_str)
```

---

## 5. Build a wikilink graph

```python
import wikitextparser as wtp
from collections import defaultdict

def build_link_graph(pages: dict[str, str]) -> dict[str, list[str]]:
    """
    pages: {page_title: wikitext}
    Returns: {page_title: [linked_titles]}
    """
    graph = defaultdict(list)
    for title, wikitext in pages.items():
        parsed = wtp.parse(wikitext)
        for wl in parsed.wikilinks:
            # Normalize: strip fragment, strip leading/trailing spaces
            target = wl.title.strip().split('#')[0]
            if target:
                graph[title].append(target)
    return dict(graph)

# Usage
pages = {
    'Python': raw_python,
    'Guido van Rossum': raw_guido,
}
graph = build_link_graph(pages)
```

---

## 6. Strip markup for NLP / full-text search

```python
import wikitextparser as wtp

def to_plain_text(wikitext: str, keep_links: bool = False) -> str:
    """
    Convert wikitext to clean plain text.
    keep_links=True: preserve [[link]] display text but remove markup.
    """
    parsed = wtp.parse(wikitext)
    return parsed.plain_text(
        replace_templates=True,
        replace_parser_functions=True,
        replace_parameters=True,
        replace_tags=True,
        replace_external_links=True,
        replace_wikilinks=True,
        unescape_html_entities=True,
        replace_bolds_and_italics=True,
    ).strip()

# Usage
text = to_plain_text(raw)
words = text.split()
```

---

## 7. Audit duplicate template arguments

```python
import wikitextparser as wtp
from collections import Counter

def find_duplicate_args(wikitext: str) -> list[dict]:
    """Return list of {template, arg, count} for any duplicate arguments."""
    parsed = wtp.parse(wikitext)
    duplicates = []
    for t in parsed.templates:
        names = [arg.name.strip() for arg in t.arguments if not arg.positional]
        counts = Counter(names)
        for name, count in counts.items():
            if count > 1:
                duplicates.append({
                    'template': t.normal_name(code='en'),
                    'arg': name,
                    'count': count,
                })
    return duplicates

# Usage
dupes = find_duplicate_args(raw)
for d in dupes:
    print(f"  {d['template']}: '{d['arg']}' appears {d['count']}×")
```

---

## 8. Extract citations (ref tags)

```python
import wikitextparser as wtp

def extract_refs(wikitext: str) -> list[dict]:
    """Return list of {name, content} for all <ref> tags."""
    parsed = wtp.parse(wikitext)
    refs = []
    for tag in parsed.get_tags('ref'):
        refs.append({
            'name': tag.get_attr('name'),
            'content': (tag.contents or '').strip(),
        })
    return refs

# Usage
citations = extract_refs(raw)
named = [r for r in citations if r['name']]
inline = [r for r in citations if r['content']]
```

---

## 9. Rewrite section headings

```python
import wikitextparser as wtp

def rename_section(wikitext: str, old_title: str, new_title: str) -> str:
    """Rename a section heading (exact match, case-sensitive)."""
    parsed = wtp.parse(wikitext)
    for section in parsed.sections:
        if section.title and section.title.strip() == old_title:
            section.title = new_title
    return str(parsed)

def promote_sections(wikitext: str) -> str:
    """Promote all section levels by 1 (h3 → h2, etc.)."""
    parsed = wtp.parse(wikitext)
    for section in parsed.sections:
        if section.level > 1:
            section.level -= 1
    return str(parsed)
```

---

## 10. Convert list types across an article

```python
import wikitextparser as wtp

def convert_all_lists(wikitext: str, from_type: str, to_type: str) -> str:
    """
    Convert list items from one type to another across the whole article.
    from_type / to_type: '*' (unordered), '#' (ordered), ':' (definition)
    """
    import re
    parsed = wtp.parse(wikitext)
    pattern = re.escape(from_type)
    for wl in parsed.get_lists(pattern=pattern):
        wl.convert(to_type)
    return str(parsed)

# Usage: convert all unordered lists to ordered
result = convert_all_lists(raw, '*', '#')
```

---

## 11. Validate template required fields

```python
import wikitextparser as wtp

REQUIRED_FIELDS = {
    'infobox person': ['name', 'birth_date', 'nationality'],
    'infobox film':   ['name', 'director', 'released'],
}

def validate_templates(wikitext: str) -> list[dict]:
    """Return list of {template, missing_fields} for validation failures."""
    parsed = wtp.parse(wikitext)
    issues = []
    for t in parsed.templates:
        name = t.normal_name(code='en').lower()
        required = REQUIRED_FIELDS.get(name)
        if not required:
            continue
        missing = [f for f in required if not t.has_arg(f)]
        if missing:
            issues.append({'template': name, 'missing': missing})
    return issues
```

---

## 12. Collect all categories from an article

```python
import wikitextparser as wtp

CATEGORY_NS = {"category", "catégorie", "kategorie", "categoría", "κατηγορία"}

def get_categories(wikitext: str) -> list[str]:
    """Return list of category names (without 'Category:' prefix)."""
    parsed = wtp.parse(wikitext)
    categories = []
    for wl in parsed.wikilinks:
        ns, _, rest = wl.title.partition(':')
        if ns.strip().lower() in CATEGORY_NS:
            categories.append(rest.strip())
    return categories

# Usage
cats = get_categories(raw)
print(cats)  # ['Living people', 'American scientists', ...]
```

---

## 13. Pretty-print all templates in a page

```python
import wikitextparser as wtp

def pretty_print_templates(wikitext: str) -> str:
    """Return a report of all templates, pretty-printed."""
    parsed = wtp.parse(wikitext)
    lines = []
    for i, t in enumerate(parsed.templates, 1):
        lines.append(f"=== Template {i}: {t.normal_name(code='en')} ===")
        lines.append(t.pformat())
        lines.append('')
    return '\n'.join(lines)
```

---

## 14. Nested template traversal

```python
import wikitextparser as wtp

def find_templates_inside(wikitext: str, outer_name: str) -> list:
    """Find all templates nested directly inside a named template."""
    parsed = wtp.parse(wikitext)
    results = []
    for t in parsed.templates:
        if t.normal_name(code='en').lower() == outer_name.lower():
            # templates property on a Template returns its nested templates
            results.extend(t.templates)
    return results

# Using ancestors to find context
def which_template_contains(wikitext: str, target_name: str) -> list[str]:
    """Return names of all templates that directly contain target_name."""
    parsed = wtp.parse(wikitext)
    containers = []
    for t in parsed.templates:
        if t.normal_name(code='en').lower() == target_name.lower():
            parent = t.parent(type_='Template')
            if parent:
                containers.append(parent.normal_name(code='en'))
    return containers
```

---

## 15. Find broken / empty wikilinks

```python
import wikitextparser as wtp

def find_empty_links(wikitext: str) -> list[str]:
    """Return all wikilinks with empty or whitespace-only titles."""
    parsed = wtp.parse(wikitext)
    return [
        str(wl) for wl in parsed.wikilinks
        if not wl.title.strip()
    ]

def find_self_links(wikitext: str, page_title: str) -> list[str]:
    """Return wikilinks that point back to the current page (self-links)."""
    parsed = wtp.parse(wikitext)
    return [
        str(wl) for wl in parsed.wikilinks
        if wl.title.strip().lower() == page_title.lower()
    ]
```
