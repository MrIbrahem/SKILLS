---
name: wikitextparser
description: >
    Parse, extract, and manipulate MediaWiki wikitext using the wikitextparser Python library.
    Use this skill whenever the user wants to work with wikitext, Wikipedia markup, or MediaWiki
    content — including extracting templates, wikilinks, tables, sections, lists, tags, or
    parser functions; modifying wikitext structure; cleaning markup; or building any pipeline
    that reads or writes MediaWiki-formatted text. Trigger even for partial tasks like
    "get all templates from this wiki page", "extract table data", "find wikilinks", or
    "remove markup from wikitext".
---

# WikiTextParser Skill

A guide for parsing and manipulating MediaWiki wikitext using the `wikitextparser` Python library.

## Installation

```bash
pip install wikitextparser --break-system-packages
```

## Core Import

```python
import wikitextparser as wtp
```

---

## Key Objects & How to Get Them

| Object         | How to access                                | Common use                      |
| -------------- | -------------------------------------------- | ------------------------------- |
| `Template`     | `parsed.templates`                           | Extract/modify template calls   |
| `WikiLink`     | `parsed.wikilinks`                           | Extract/modify `[[links]]`      |
| `Section`      | `parsed.sections` or `parsed.get_sections()` | Navigate headings               |
| `Table`        | `parsed.tables` or `parsed.get_tables()`     | Extract table data              |
| `WikiList`     | `parsed.get_lists()`                         | Work with bullet/numbered lists |
| `Tag`          | `parsed.get_tags()`                          | Work with HTML/extension tags   |
| `ExternalLink` | `parsed.external_links`                      | Work with `[url text]` links    |
| `Parameter`    | `parsed.parameters`                          | Work with `{{{param}}}`         |
| `Comment`      | `parsed.comments`                            | Access `<!-- comments -->`      |

---

## Templates

```python
parsed = wtp.parse("{{Infobox|name=Alice|age=30}}")
templates = parsed.templates          # list of Template objects
t = templates[0]

t.name                                # 'Infobox'
t.arguments                           # list of Argument objects
t.get_arg('name').value               # 'Alice'
t.set_arg('age', '31')               # modify argument
t.has_arg('name')                     # True
t.del_arg('age')                      # remove argument

# Pretty-print a template
print(t.pformat())

# Clean duplicate args (safe: only removes true dupes)
t.rm_dup_args_safe()
# Clean duplicate args (aggressive: removes first occurrence)
t.rm_first_of_dup_args()

# Normalized template name (strips namespace, underscores, etc.)
t.normal_name(code='en')
```

### Template Parameters (`{{{param}}}`)

```python
param = wtp.parse('{{{name|default}}}').parameters[0]
param.name       # 'name'
param.default    # 'default'
param.default = 'new_default'
param.append_default('fallback')   # adds another level: {{{name|{{{fallback|default}}}}}}
```

---

## WikiLinks

```python
wl = wtp.parse('[[Article title#Section|display text]]').wikilinks[0]
wl.title      # 'Article title'
wl.fragment   # 'Section'
wl.text       # 'display text'

wl.title = 'New Title'
wl.text = 'New Text'
del wl.text   # removes pipe and text, leaves [[New Title#Section]]
```

### Extracting Categories

```python
categories = [
    wl for wl in parsed.wikilinks
    if wl.title.partition(':')[0].strip().lower() in ["category", "κατηγορία"]
]
```

---

## Sections

```python
parsed = wtp.parse("== Heading ==\nContent\n=== Sub ==\nMore")
sections = parsed.sections        # includes lead section (index 0)

s = sections[1]
s.title                           # 'Heading'
s.level                           # 2
s.contents                        # text body of section

s.title = 'New Heading'
del s.title                       # removes heading line entirely

# Filtered access
parsed.get_sections(level=2)                        # only h2
parsed.get_sections(include_subsections=False)      # no nested content
parsed.get_sections(top_levels_only=True)           # no subsections of subsections
```

---

## Tables

```python
t = wtp.parse("""{|
|-
| A || B
|-
| C || D
|}""").tables[0]

t.data()                          # [['A', 'B'], ['C', 'D']]
t.data(span=False)                # ignores colspan/rowspan
t.data(row=0)                     # ['A', 'B']
t.data(row=0, column=1)           # 'B'

# Cell objects (richer than data())
cell = t.cells(row=0, column=0)
cell.attrs                        # dict of HTML attributes
cell.set('colspan', '2')

t.caption                         # table caption string or None
t.row_attrs                       # list of dicts per row
```

---

## Lists

```python
parsed = wtp.parse("* item a\n* item b\n** sub-item\n* item c")
wl = parsed.get_lists()[0]

wl.items          # [' item a', ' item b', ' item c']  (no sub-items)
wl.fullitems      # includes sub-item lines
wl.level          # nesting depth (1-based)

wl.sublists()                     # all sub-lists
wl.sublists(1)                    # sub-lists of item at index 1
wl.sublists(pattern=r'\*')        # filter sub-list pattern

# Convert list type
wl.convert('#')                   # change * to # (unordered → ordered)

# Ordered list
ol = wtp.WikiList('#a\n#b\n##ba', r'\#')
ol.sublists()
```

---

## Tags

```python
p = wtp.parse('<ref name="src">citation text</ref>\n<references/>')
tags = p.get_tags()
ref = p.get_tags('ref')[0]

ref.name                          # 'ref'
ref.contents                      # 'citation text'
ref.get_attr('name')              # 'src'
ref.set_attr('name', 'new-src')
ref.has_attr('name')              # True
ref.del_attr('name')

ref.name = 'X'                    # rename tag
```

---

## External Links

```python
el = wtp.parse('[https://example.com Example Site]').external_links[0]
el.url            # 'https://example.com'
el.text           # 'Example Site'
el.in_brackets    # True

el.url = 'https://new.example.com'
del el.text       # makes it a bare link
```

---

## Stripping Markup

```python
from wikitextparser import remove_markup, parse

# Function approach
remove_markup("'''bold''' [[link|text]] <!-- comment -->")
# → 'bold text '

# Method approach
parse("'''bold''' [[link|text]]").plain_text()
# → 'bold text'

# plain_text() accepts fine-grained control:
parse(s).plain_text(
    replace_templates=False,       # keep {{templates}}
    replace_wikilinks=True,        # replace [[links]] with text
    unescape_html_entities=True,   # &amp; → &
    replace_bolds_and_italics=True
)
```

---

## Tree Navigation

```python
# Find parent / ancestors
t = wtp.parse("{{a|{{b|{{c}}}}}}").templates[2]  # {{c}}
t.parent()             # Template('{{b|{{c}}}}')
t.ancestors()          # [{{b|...}}, {{a|...}}]
t.ancestors(type_='Template')   # filter by type

# Supported types: 'Template', 'ParserFunction', 'WikiLink',
#                  'Comment', 'Parameter', 'ExtensionTag'
```

---

## Modifying Content In-Place

All objects share the same underlying string — edits to child objects update the root:

```python
parsed = wtp.parse("{{t|a=old}}")
parsed.templates[0].set_arg('a', 'new')
str(parsed)    # '{{t|a=new}}'
```

To delete a node:

```python
del node[:]         # or
del node.string
```

---

## Common Patterns

### Extract all template names

```python
[t.name.strip() for t in parsed.templates]
```

### Get all wikilinks pointing to a namespace

```python
[wl for wl in parsed.wikilinks if wl.title.startswith('File:')]
```

### Replace template argument values

```python
for t in parsed.templates:
    if t.normal_name() == 'Infobox person':
        t.set_arg('birth_date', '1990-01-01')
```

### Extract table as list of dicts (with header row)

```python
table = parsed.tables[0]
rows = table.data()
headers = rows[0]
records = [dict(zip(headers, row)) for row in rows[1:]]
```

### Strip all markup for plain-text search

```python
plain = wtp.parse(wikitext).plain_text()
```

---

## Known Limitations

-   Localized namespace names (e.g. `[[Archivo:...]]` for `[[File:...]]`) are treated as normal wikilinks — use Pywikibot for namespace resolution.
-   Parser functions and magic words are **not** evaluated.
-   Extension tag list is based on English Wikipedia; other wikis may differ.
-   No `ast.walk`-equivalent; use `.ancestors()` / `.parent()` to traverse.
-   Offline parsers can't resolve template contents — `[[{{template}}]]` is guessed as a wikilink.
