# Tuple operations

Tuples are immutable sequences. They support fewer methods than lists because they cannot be modified after creation.

## Tuple methods

### `count()`

```python
tuple.count(value)
```

Return the number of times a value appears in the tuple.

```python
numbers = (1, 2, 2, 3, 2)
print(numbers.count(2))  # 3
```

### `index()`

```python
tuple.index(value, start=0, stop=len(tuple))
```

Return the index of the first occurrence of a value. Raises `ValueError` if the value is not found.

```python
colours = ("red", "green", "blue")
print(colours.index("green"))  # 1
```

## Creating tuples

### Literal syntax

```python
point = (3, 4)
```

### Single-element tuple

A trailing comma is required to distinguish a single-element tuple from a grouped expression:

```python
single = (42,)     # This is a tuple
not_tuple = (42)   # This is an integer
```

### Without parentheses

Python recognises tuples by the commas:

```python
coordinates = 51.5074, -0.1278
```

### The `tuple()` constructor

Convert any iterable to a tuple:

```python
from_list = tuple([1, 2, 3])
from_string = tuple("abc")  # ("a", "b", "c")
empty = tuple()
```

## Supported operations

### Indexing and slicing

```python
colours = ("red", "green", "blue", "yellow")
print(colours[0])      # "red"
print(colours[-1])     # "yellow"
print(colours[1:3])    # ("green", "blue")
```

### Concatenation

```python
a = (1, 2)
b = (3, 4)
print(a + b)  # (1, 2, 3, 4)
```

### Repetition

```python
print((0,) * 5)  # (0, 0, 0, 0, 0)
```

### Membership testing

```python
print(2 in (1, 2, 3))      # True
print(5 not in (1, 2, 3))  # True
```

### Unpacking

```python
x, y, z = (1, 2, 3)
first, *rest = (1, 2, 3, 4, 5)
```

### Built-in functions

```python
numbers = (3, 1, 4, 1, 5)

len(numbers)       # 5
min(numbers)       # 1
max(numbers)       # 5
sum(numbers)       # 14
sorted(numbers)    # [1, 1, 3, 4, 5] (returns a list)
```

### Comparison

Tuples are compared element by element from left to right:

```python
print((1, 2, 3) < (1, 2, 4))   # True
print((1, 2) < (1, 2, 0))      # True (shorter tuple is less)
print((1, 2, 3) == (1, 2, 3))  # True
```

## Named tuples

### `collections.namedtuple`

Create a tuple subclass with named fields:

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)    # 3 4
print(p[0], p[1])  # 3 4 (indexing still works)
```

### `typing.NamedTuple`

A class-based syntax with type annotations:

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

p = Point(3.0, 4.0)
print(p.x, p.y)
```

Both forms create immutable, hashable objects that support all standard tuple operations.
