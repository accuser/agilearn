# Choosing data structures

The data structure you choose shapes your code in fundamental ways. It affects readability, correctness, and performance. This discussion explores the trade-offs between Python's built-in data structures and helps you develop intuition for making the right choice.

## Understanding the trade-offs

Every data structure makes trade-offs. There is no single "best" structure — only the best structure for a given situation. The key dimensions to consider are:

- **Ordered versus unordered** — does the position of items matter?
- **Mutable versus immutable** — do you need to change the collection after creating it?
- **Unique versus duplicate** — should the collection allow repeated items?
- **Index-based versus key-based** — how will you access the data?

## Lists

Lists are the workhorse of Python. They are ordered, mutable, and allow duplicates.

**Choose lists when:**

- You need to maintain items in a specific order
- You access items by position (index)
- The collection will grow or shrink over time
- Duplicates are acceptable or even meaningful

**Be cautious with lists when:**

- You frequently check whether an item exists — membership testing is O(n) because Python must scan the entire list
- You frequently insert or remove items at the beginning — this is O(n) because all other items must shift
- You need key-based lookups — a dictionary is more appropriate

## Tuples

Tuples are ordered and immutable. They signal that the data should not change.

**Choose tuples when:**

- The collection represents a fixed record (for example, coordinates, a date, or a colour)
- You need to use the data as a dictionary key or set member (tuples are hashable)
- You are returning multiple values from a function
- You want to prevent accidental modification

**Consider named tuples** when the tuple has more than two or three elements, so that you can access fields by name rather than by index.

## Dictionaries

Dictionaries provide fast key-value lookups and preserve insertion order.

**Choose dictionaries when:**

- You need to associate values with unique keys
- You need fast lookups by key — average O(1)
- You are counting, grouping, or categorising data
- You are building configuration or settings objects

**Be cautious with dictionaries when:**

- You only need to check membership without associated values — a set is simpler
- You need to maintain sorted order — dictionaries preserve insertion order, not sorted order

## Sets

Sets are unordered, mutable collections of unique items with fast membership testing.

**Choose sets when:**

- You need to eliminate duplicates
- You need fast membership testing — average O(1)
- You need to perform mathematical set operations (union, intersection, difference)
- The order of items does not matter

**Be cautious with sets when:**

- You need to maintain insertion order — sets do not preserve order
- You need to store key-value pairs — use a dictionary instead
- Items are not hashable (for example, lists or other sets)

## Combining data structures

Real-world problems often call for combinations of data structures. Here are some common patterns.

### List of dictionaries

Ideal for storing a collection of records, similar to rows in a database table:

```python
employees = [
    {"name": "Alice", "department": "Engineering"},
    {"name": "Bob", "department": "Marketing"},
]
```

### Dictionary of lists

Useful for grouping items by category:

```python
students_by_subject = {
    "Maths": ["Alice", "Bob", "Charlie"],
    "English": ["Diana", "Eve"],
}
```

### Set for deduplication, list for ordering

Use a set to remove duplicates, then convert to a sorted list:

```python
raw_data = [3, 1, 4, 1, 5, 9, 2, 6, 5]
unique_sorted = sorted(set(raw_data))
```

## Anti-patterns

### Using a list when you need a dictionary

If you find yourself searching through a list to find an item by some attribute, you probably need a dictionary:

```python
# Inefficient — O(n) lookup each time
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
for user in users:
    if user["id"] == target_id:
        break

# Better — O(1) lookup
users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
user = users[target_id]
```

### Using a list for membership testing

If you frequently check `item in collection`, use a set instead of a list:

```python
# Slow for large collections — O(n)
allowed = ["alice", "bob", "charlie"]
if username in allowed: ...

# Fast — O(1)
allowed = {"alice", "bob", "charlie"}
if username in allowed: ...
```

### Using a dictionary when a set would do

If your dictionary values are all `True` or `None` and you only check key membership, use a set:

```python
# Unnecessary complexity
seen = {"alice": True, "bob": True}
if name in seen: ...

# Simpler
seen = {"alice", "bob"}
if name in seen: ...
```

## Summary

Choosing the right data structure is about understanding your data and your access patterns. Lists are for ordered sequences, tuples for fixed records, dictionaries for key-value mappings, and sets for unique collections. When you match the structure to the problem, your code becomes clearer, more correct, and more efficient.
