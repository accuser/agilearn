# Built-in functions

This reference covers the Python built-in functions most commonly used when working with functions, higher-order programming, and introspection. Functions are grouped by category for quick lookup.

## Numeric functions

These functions operate on numbers or return numeric results.

| Function | Signature | Description |
|----------|-----------|-------------|
| `abs()` | `abs(x)` | Return the absolute value of a number. |
| `max()` | `max(iterable)` or `max(a, b, ...)` | Return the largest item. Accepts an optional `key` function. |
| `min()` | `min(iterable)` or `min(a, b, ...)` | Return the smallest item. Accepts an optional `key` function. |
| `round()` | `round(number, ndigits=None)` | Round to `ndigits` decimal places. Returns an `int` when `ndigits` is omitted. |
| `sum()` | `sum(iterable, start=0)` | Return the sum of items plus `start`. |

### Examples

```python
abs(-7)           # 7
max(3, 1, 4, 1)   # 4
min([10, 20, 5])   # 5
round(3.14159, 2)  # 3.14
sum([1, 2, 3])     # 6
```

### Using `key` with `max()` and `min()`

The `key` parameter accepts a function that transforms each item before comparison.

```python
words = ["apple", "fig", "banana"]
max(words, key=len)   # "banana"
min(words, key=len)   # "fig"
```

## Iterable functions

These functions create, transform, or consume iterables.

| Function | Signature | Description |
|----------|-----------|-------------|
| `enumerate()` | `enumerate(iterable, start=0)` | Return pairs of `(index, item)` from an iterable. |
| `filter()` | `filter(function, iterable)` | Return items for which `function` returns `True`. |
| `iter()` | `iter(object)` | Return an iterator from an iterable. |
| `len()` | `len(s)` | Return the number of items in a container. |
| `map()` | `map(function, iterable, ...)` | Apply `function` to every item and return an iterator of results. |
| `next()` | `next(iterator, default)` | Retrieve the next item from an iterator. Return `default` if exhausted. |
| `range()` | `range(stop)` or `range(start, stop, step)` | Return an immutable sequence of integers. |
| `reversed()` | `reversed(seq)` | Return a reverse iterator over a sequence. |
| `sorted()` | `sorted(iterable, key=None, reverse=False)` | Return a new sorted list from the items in an iterable. |
| `zip()` | `zip(*iterables, strict=False)` | Aggregate items from each iterable into tuples. |

### `enumerate()`

```python
for index, colour in enumerate(["red", "green", "blue"]):
    print(f"{index}: {colour}")
# 0: red
# 1: green
# 2: blue
```

### `filter()`

`filter()` returns an iterator of items for which the given function returns a truthy value. Pass `None` as the function to filter out falsy values.

```python
numbers = [0, 1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [0, 2, 4]

# Filter out falsy values
values = [0, "", "hello", None, 42]
truthy = list(filter(None, values))
# ["hello", 42]
```

### `map()`

`map()` applies a function to every item in one or more iterables and returns an iterator of results.

```python
numbers = [1, 2, 3, 4]
squared = list(map(lambda x: x ** 2, numbers))
# [1, 4, 9, 16]

# With multiple iterables
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
# [11, 22, 33]
```

### `sorted()`

```python
words = ["banana", "apple", "cherry"]
sorted(words)                        # ["apple", "banana", "cherry"]
sorted(words, key=len)               # ["apple", "banana", "cherry"]
sorted(words, key=len, reverse=True) # ["banana", "cherry", "apple"]
```

### `zip()`

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
paired = list(zip(names, scores))
# [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
```

In Python 3.10 and later, the `strict` parameter raises a `ValueError` if the iterables have different lengths.

```python
# Python 3.10+
list(zip([1, 2], [10, 20, 30], strict=True))
# ValueError: zip() has arguments with different lengths
```

### `range()`

```python
list(range(5))         # [0, 1, 2, 3, 4]
list(range(2, 8))      # [2, 3, 4, 5, 6, 7]
list(range(0, 10, 3))  # [0, 3, 6, 9]
```

### `reversed()`

```python
list(reversed([1, 2, 3]))  # [3, 2, 1]
list(reversed(range(5)))   # [4, 3, 2, 1, 0]
```

### `iter()` and `next()`

```python
it = iter([10, 20, 30])
next(it)          # 10
next(it)          # 20
next(it)          # 30
next(it, "done")  # "done" (default returned when exhausted)
```

## Boolean and comparison functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `all()` | `all(iterable)` | Return `True` if all items are truthy (or the iterable is empty). |
| `any()` | `any(iterable)` | Return `True` if any item is truthy. Return `False` for an empty iterable. |

### Examples

```python
all([True, True, True])    # True
all([True, False, True])   # False
all([])                    # True (vacuous truth)

any([False, False, True])  # True
any([False, False, False]) # False
any([])                    # False
```

### With generator expressions

```python
numbers = [2, 4, 6, 8]
all(n % 2 == 0 for n in numbers)  # True (all are even)
any(n > 5 for n in numbers)       # True (6 and 8 are greater than 5)
```

## Type checking and introspection

These functions inspect the type or capabilities of objects.

| Function | Signature | Description |
|----------|-----------|-------------|
| `callable()` | `callable(object)` | Return `True` if the object appears callable. |
| `dir()` | `dir(object)` | Return a list of names in the object scope. Without an argument, return names in the current scope. |
| `getattr()` | `getattr(object, name, default)` | Return the value of the named attribute. Return `default` if the attribute does not exist. |
| `hasattr()` | `hasattr(object, name)` | Return `True` if the object has the named attribute. |
| `help()` | `help(object)` | Display the help page for an object (interactive use). |
| `id()` | `id(object)` | Return the unique identity (memory address) of an object. |
| `isinstance()` | `isinstance(object, classinfo)` | Return `True` if the object is an instance of the given class or a subclass thereof. |
| `issubclass()` | `issubclass(class, classinfo)` | Return `True` if the class is a subclass of the given class. |
| `type()` | `type(object)` | Return the type of an object. |

### `callable()`

```python
def greet():
    return "Hello!"

callable(greet)    # True
callable(42)       # False
callable(len)      # True
callable(lambda: None)  # True
```

### `isinstance()` and `type()`

```python
isinstance(42, int)          # True
isinstance("hello", str)     # True
isinstance(42, (int, float)) # True (checks against multiple types)

type(42)       # <class 'int'>
type("hello")  # <class 'str'>
```

`isinstance()` is generally preferred over `type()` for type checking because it respects inheritance.

### `getattr()` and `hasattr()`

```python
class Point:
    x = 10
    y = 20

p = Point()
getattr(p, "x")              # 10
getattr(p, "z", "missing")   # "missing"
hasattr(p, "x")              # True
hasattr(p, "z")              # False
```

### `dir()`

```python
def example():
    pass

# Show attributes of a function object
dir(example)
# ['__annotations__', '__call__', '__class__', '__closure__', ...]
```

## Output functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `print()` | `print(*objects, sep=" ", end="\n", file=sys.stdout)` | Print objects to the text stream. |

### Examples

```python
print("Hello", "World")          # Hello World
print("a", "b", "c", sep=", ")   # a, b, c
print("Loading", end="...")       # Loading... (no newline)
```

## Higher-order function patterns

Several built-in functions accept other functions as arguments, making them higher-order functions. The following table summarises these.

| Function | Accepts a function as | Purpose |
|----------|----------------------|---------|
| `filter()` | First argument | Select items from an iterable |
| `map()` | First argument | Transform items in an iterable |
| `max()` | `key` parameter | Determine the largest item |
| `min()` | `key` parameter | Determine the smallest item |
| `sorted()` | `key` parameter | Determine sort order |

### Example combining higher-order functions

```python
people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
]

# Names of people over 28, sorted alphabetically
names = sorted(
    map(
        lambda p: p["name"],
        filter(lambda p: p["age"] > 28, people)
    )
)
# ["Alice", "Charlie"]
```

## Summary table

| Category | Functions |
|----------|-----------|
| Numeric | `abs()`, `max()`, `min()`, `round()`, `sum()` |
| Iterable | `enumerate()`, `filter()`, `iter()`, `len()`, `map()`, `next()`, `range()`, `reversed()`, `sorted()`, `zip()` |
| Boolean | `all()`, `any()` |
| Type checking and introspection | `callable()`, `dir()`, `getattr()`, `hasattr()`, `help()`, `id()`, `isinstance()`, `issubclass()`, `type()` |
| Output | `print()` |
