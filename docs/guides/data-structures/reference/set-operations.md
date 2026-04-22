# Set operations

This reference documents all methods and operators available on Python `set` objects.

## Adding and removing

### `add()`

```python
set.add(elem)
```

Add an element to the set. Has no effect if the element is already present.

```python
colours = {"red", "green"}
colours.add("blue")
```

### `remove()`

```python
set.remove(elem)
```

Remove an element from the set. Raises `KeyError` if the element is not found.

```python
colours = {"red", "green", "blue"}
colours.remove("green")
```

### `discard()`

```python
set.discard(elem)
```

Remove an element from the set if it is present. Does not raise an error if the element is missing.

```python
colours = {"red", "green"}
colours.discard("blue")  # No error
```

### `pop()`

```python
set.pop()
```

Remove and return an arbitrary element. Raises `KeyError` if the set is empty.

```python
colours = {"red", "green", "blue"}
item = colours.pop()
```

### `clear()`

```python
set.clear()
```

Remove all elements from the set.

## Set algebra

### Union

Items in either set (or both).

| Form | Syntax |
|------|--------|
| Operator | `a | b` |
| Method | `a.union(b)` |
| In-place | `a |= b` or `a.update(b)` |

```python
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)  # {1, 2, 3, 4, 5}
```

### Intersection

Items in both sets.

| Form | Syntax |
|------|--------|
| Operator | `a & b` |
| Method | `a.intersection(b)` |
| In-place | `a &= b` or `a.intersection_update(b)` |

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)  # {2, 3}
```

### Difference

Items in the first set but not the second.

| Form | Syntax |
|------|--------|
| Operator | `a - b` |
| Method | `a.difference(b)` |
| In-place | `a -= b` or `a.difference_update(b)` |

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a - b)  # {1}
```

### Symmetric difference

Items in either set, but not both.

| Form | Syntax |
|------|--------|
| Operator | `a ^ b` |
| Method | `a.symmetric_difference(b)` |
| In-place | `a ^= b` or `a.symmetric_difference_update(b)` |

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a ^ b)  # {1, 4}
```

## Comparison

### `issubset()`

```python
set.issubset(other)
```

Return `True` if every element of the set is in the other set. Equivalent to `set <= other`.

Use `set < other` to test for a proper subset (subset but not equal).

```python
a = {1, 2}
b = {1, 2, 3}
print(a.issubset(b))  # True
print(a < b)          # True (proper subset)
```

### `issuperset()`

```python
set.issuperset(other)
```

Return `True` if every element of the other set is in this set. Equivalent to `set >= other`.

Use `set > other` to test for a proper superset.

```python
a = {1, 2, 3}
b = {1, 2}
print(a.issuperset(b))  # True
```

### `isdisjoint()`

```python
set.isdisjoint(other)
```

Return `True` if the two sets have no elements in common.

```python
evens = {2, 4, 6}
odds = {1, 3, 5}
print(evens.isdisjoint(odds))  # True
```

## Other operations

### `copy()`

```python
set.copy()
```

Return a shallow copy of the set.

### `frozenset`

A `frozenset` is an immutable version of a set. It supports all set operations except those that modify the set.

```python
vowels = frozenset({"a", "e", "i", "o", "u"})
```

Frozen sets can be used as dictionary keys or as elements of other sets.

## Summary of operators versus methods

| Operation              | Operator | Method                         |
|------------------------|----------|--------------------------------|
| Union                  | `|`     | `union()`                      |
| Intersection           | `&`      | `intersection()`               |
| Difference             | `-`      | `difference()`                 |
| Symmetric difference   | `^`      | `symmetric_difference()`       |
| Subset                 | `<=`     | `issubset()`                   |
| Proper subset          | `<`      | —                              |
| Superset               | `>=`     | `issuperset()`                 |
| Proper superset        | `>`      | —                              |
