# Choose the right data structure

Selecting the right data structure affects the readability, correctness, and performance of your code. This guide walks you through a series of questions and common scenarios to help you make the right choice.

## Decision questions

Work through the following questions to narrow down which data structure best fits your use case.

### Do you need ordered data?

If the order of items matters, use a **list** or a **tuple**.

- If you need to modify the collection, use a **list**.
- If the data should remain fixed after creation, use a **tuple**.

### Do you need key-value lookups?

If you need to associate values with unique keys for fast lookup, use a **dictionary**.

### Do you need unique items only?

If you need a collection that automatically eliminates duplicates, use a **set**.

### Do you need fast membership testing?

If your primary operation is checking whether an item exists in the collection, use a **set** or a **dictionary**. Both offer average O(1) lookup time, compared to O(n) for lists and tuples.

## Common scenarios

### Storing a sequence of items

Use a **list** when you need an ordered, modifiable collection.

```python
tasks = ["write report", "review code", "update tests"]
tasks.append("deploy release")
```

### Returning multiple values from a function

Use a **tuple** to return a fixed group of related values.

```python
def get_dimensions():
    return (1920, 1080)

width, height = get_dimensions()
```

### Counting occurrences

Use a **dictionary** to count items, or use `collections.Counter` for a convenient shortcut.

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(words)
```

### Removing duplicates

Use a **set** to strip duplicates. If you need to preserve insertion order, use `dict.fromkeys()`:

```python
# When order does not matter
unique = set([1, 2, 2, 3, 3])

# When order matters
unique_ordered = list(dict.fromkeys([1, 2, 2, 3, 3]))
```

### Configuration and settings

Use a **dictionary** to store named configuration values.

```python
config = {"debug": False, "max_retries": 3, "timeout_seconds": 30}
```

### Database-style records

Use a **list of dictionaries** when each item has the same set of fields.

```python
employees = [
    {"name": "Alice", "department": "Engineering", "salary": 55000},
    {"name": "Bob", "department": "Marketing", "salary": 48000},
]
```

### Grouping items by category

Use a **dictionary of lists** to group related items under a shared key.

```python
grouped = {}
for category, item in data:
    if category not in grouped:
        grouped[category] = []
    grouped[category].append(item)
```

### Fixed coordinates or records

Use a **named tuple** when you need a lightweight, immutable record with named fields.

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
origin = Point(0, 0)
```

## Summary table

| Feature            | `list`          | `tuple`         | `dict`                | `set`           |
|--------------------|-----------------|-----------------|----------------------|-----------------|
| Ordered            | Yes             | Yes             | Yes (insertion order) | No              |
| Mutable            | Yes             | No              | Yes                   | Yes             |
| Duplicates allowed | Yes             | Yes             | Keys: No              | No              |
| Syntax             | `[1, 2, 3]`    | `(1, 2, 3)`    | `{"a": 1}`           | `{1, 2, 3}`    |
| Best for           | Sequences       | Fixed data      | Key-value mappings    | Unique items    |

## Quick reference

1. **Need to look up values by key?** Use a `dict`.
2. **Need only unique items?** Use a `set`.
3. **Need an ordered collection you can change?** Use a `list`.
4. **Need an ordered collection that must not change?** Use a `tuple`.
5. **Need named fields on an immutable record?** Use a `namedtuple`.
6. **Need to count items?** Use `collections.Counter`.
7. **Need to group items by category?** Use a `dict` of lists.
8. **Need fast membership testing?** Use a `set` or `dict`.

When in doubt, start with a `list` or a `dict`. These two structures cover the majority of everyday use cases, and you can refactor to a more specialised structure later if needed.
