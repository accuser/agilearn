# Sequence operations

This reference covers operations common to all sequence types in Python: lists, tuples, strings, and ranges.

## Common operations

| Operation | Syntax | Lists | Tuples | Strings | Ranges |
|-----------|--------|-------|--------|---------|--------|
| Indexing | `seq[i]` | Yes | Yes | Yes | Yes |
| Slicing | `seq[start:stop:step]` | Yes | Yes | Yes | Yes |
| Concatenation | `seq1 + seq2` | Yes | Yes | Yes | No |
| Repetition | `seq * n` | Yes | Yes | Yes | No |
| Membership | `item in seq` | Yes | Yes | Yes | Yes |
| Length | `len(seq)` | Yes | Yes | Yes | Yes |
| Minimum | `min(seq)` | Yes | Yes | Yes | Yes |
| Maximum | `max(seq)` | Yes | Yes | Yes | Yes |
| Index | `seq.index(value)` | Yes | Yes | Yes | Yes |
| Count | `seq.count(value)` | Yes | Yes | Yes | No |

## Indexing

Access a single item by its position. Python uses zero-based indexing.

```python
colours = ["red", "green", "blue"]
print(colours[0])    # "red" (first item)
print(colours[-1])   # "blue" (last item)
```

Negative indices count from the end: `-1` is the last item, `-2` is the second to last, and so on.

## Slicing

Extract a portion of a sequence using `[start:stop:step]`.

### Basic slicing

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

numbers[2:5]    # [2, 3, 4]
numbers[:3]     # [0, 1, 2]
numbers[7:]     # [7, 8, 9]
numbers[-3:]    # [7, 8, 9]
```

### Slicing with step

```python
numbers[::2]     # [0, 2, 4, 6, 8] (every second item)
numbers[1::2]    # [1, 3, 5, 7, 9] (odd indices)
numbers[::3]     # [0, 3, 6, 9] (every third item)
```

### Reversing

```python
numbers[::-1]    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

### Slice objects

You can create reusable slice objects:

```python
first_three = slice(0, 3)
print(numbers[first_three])  # [0, 1, 2]
```

## Unpacking

### Basic unpacking

Assign each item to a separate variable:

```python
x, y, z = [1, 2, 3]
```

The number of variables must match the number of items.

### Extended unpacking with `*`

Use `*` to collect remaining items into a list:

```python
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

first, *middle, last = [1, 2, 3, 4, 5]
# first = 1, middle = [2, 3, 4], last = 5
```

### Nested unpacking

Unpack nested structures in a single statement:

```python
(a, b), (c, d) = [1, 2], [3, 4]
```

### Swapping values

```python
a, b = b, a
```

### Ignoring values

Use `_` as a convention for values you do not need:

```python
_, second, _ = (1, 2, 3)
first, *_ = [1, 2, 3, 4, 5]
```

## Concatenation

Join two sequences of the same type:

```python
[1, 2] + [3, 4]          # [1, 2, 3, 4]
(1, 2) + (3, 4)          # (1, 2, 3, 4)
"hello " + "world"       # "hello world"
```

## Repetition

Repeat a sequence a given number of times:

```python
[0] * 5          # [0, 0, 0, 0, 0]
(1, 2) * 3       # (1, 2, 1, 2, 1, 2)
"ha" * 3         # "hahaha"
```

## Membership testing

Check whether an item exists in a sequence:

```python
print(3 in [1, 2, 3])        # True
print("x" not in "hello")    # True
```

## Comparison

Sequences of the same type can be compared. Comparison proceeds element by element:

```python
[1, 2, 3] < [1, 2, 4]     # True
(1, 2) < (1, 2, 0)        # True
"apple" < "banana"        # True
```
