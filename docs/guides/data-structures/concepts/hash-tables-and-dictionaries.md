# Hash tables and dictionaries

Dictionaries are one of the most powerful and frequently used data structures in Python. Understanding how they work under the hood helps you use them effectively and appreciate why certain rules exist.

## What is a hash table?

A **hash table** is a data structure that maps keys to values using a **hash function**. The hash function converts a key into a number (the hash value), which determines where the value is stored in memory. This allows lookups to happen in constant time on average — you do not need to search through every item.

Python dictionaries are built on hash tables.

## How hashing works

When you add a key-value pair to a dictionary, Python does the following:

1. Calls `hash()` on the key to produce an integer hash value
2. Uses that hash value to calculate a position (bucket) in an internal array
3. Stores the key-value pair at that position

When you look up a key, the same process runs in reverse: Python hashes the key, finds the bucket, and retrieves the value.

```python
# The hash() function returns an integer
print(hash("hello"))    # A large integer
print(hash(42))         # 42
print(hash((1, 2, 3)))  # A large integer
```

## Why keys must be hashable

For this system to work, a key must produce the same hash value every time. If the key could change (that is, if it were mutable), its hash value could change, and the dictionary would not be able to find it again.

This is why only **immutable** types can be dictionary keys:

- Strings, numbers, and tuples — **can** be dictionary keys
- Lists, sets, and dictionaries — **cannot** be dictionary keys

```python
# This works
locations = {(51.5, -0.1): "London"}

# This raises TypeError
# locations = {[51.5, -0.1]: "London"}
```

## Why dictionary lookups are fast

In a list, finding an item requires checking each element one by one — this takes O(n) time. In a dictionary, the hash function jumps directly to the right position — this takes O(1) time on average.

This difference becomes significant with large collections. Looking up a key in a dictionary of one million items is roughly as fast as looking up a key in a dictionary of ten items.

## Hash collisions

Occasionally, two different keys produce the same hash value. This is called a **hash collision**. Python handles collisions by probing — if the calculated bucket is already occupied by a different key, Python looks for the next available bucket using a deterministic algorithm.

Collisions slow things down slightly because Python needs to do extra comparisons, but they are uncommon enough that average-case performance remains O(1).

## The `__hash__` and `__eq__` relationship

For an object to work as a dictionary key, it must implement both `__hash__()` (to compute the hash value) and `__eq__()` (to check equality when collisions occur).

The fundamental rule is: **if two objects are equal, they must have the same hash value.** The reverse does not need to hold — two objects with the same hash value can be unequal.

```python
# Equal values always have the same hash
print(hash(1) == hash(1.0))  # True, because 1 == 1.0
```

## Dictionary ordering

### Before Python 3.7

Dictionaries did not guarantee any particular order. Iterating over a dictionary could yield items in any order.

### Python 3.7 and later

Dictionaries are guaranteed to preserve **insertion order**. Items are yielded in the order they were added.

```python
person = {}
person["name"] = "Alice"
person["age"] = 30
person["city"] = "London"

# Always prints: name, age, city
for key in person:
    print(key)
```

This ordering is a property of the dictionary implementation, not of the hash table concept in general.

## Performance characteristics

| Operation | Average case | Worst case |
|-----------|-------------|------------|
| Lookup (`d[key]`) | O(1) | O(n) |
| Insert (`d[key] = value`) | O(1) | O(n) |
| Delete (`del d[key]`) | O(1) | O(n) |
| Iteration | O(n) | O(n) |
| Membership (`key in d`) | O(1) | O(n) |

The worst case of O(n) occurs only when there are many hash collisions, which is rare in practice.

## Memory trade-off

Dictionaries use more memory than lists because they need to store the hash table structure alongside the data. This is a deliberate trade-off: extra memory buys faster lookup performance.

For small collections (fewer than a dozen items), the overhead matters little. For large collections where fast lookups are important, the extra memory is well worth it.

## When to use dictionaries

Dictionaries are the right choice when:

- You need to look up values by key
- You need fast membership testing for keys
- You are counting, grouping, or categorising data
- You need a mapping from identifiers to objects

Dictionaries are overkill when:

- You just need an ordered sequence of items (use a list)
- You only need to check membership without associated values (use a set)
- You have a small, fixed set of named fields (use a named tuple)

## Summary

Python dictionaries are built on hash tables, which provide fast average-case lookups by converting keys into array positions using a hash function. This design requires keys to be immutable and hashable. Understanding these internals helps explain why dictionaries behave the way they do and guides you in choosing the right data structure for your needs.
