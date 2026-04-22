# Memory and performance

Understanding how data structure choice affects memory usage and execution speed helps you write efficient Python code. This discussion covers the time complexity of common operations and the memory characteristics of each built-in data structure.

## Time complexity in practical terms

**Big O notation** describes how the time for an operation grows as the size of the data increases. Here is what the common complexities mean in practice:

- **O(1)** — constant time. The operation takes the same time regardless of size. Looking up a dictionary key is O(1).
- **O(n)** — linear time. The operation time grows proportionally with size. Searching a list for an item is O(n).
- **O(n log n)** — linearithmic time. Sorting a list is O(n log n).

## Lists

Lists in Python are implemented as dynamic arrays — contiguous blocks of references to objects.

| Operation | Time complexity |
|-----------|----------------|
| Access by index (`lst[i]`) | O(1) |
| Append (`lst.append(x)`) | O(1) amortised |
| Insert at beginning (`lst.insert(0, x)`) | O(n) |
| Delete from beginning (`lst.pop(0)`) | O(n) |
| Membership test (`x in lst`) | O(n) |
| Search (`lst.index(x)`) | O(n) |
| Sort (`lst.sort()`) | O(n log n) |
| Length (`len(lst)`) | O(1) |

**Key insight:** Appending to the end of a list is fast, but inserting at or removing from the beginning is slow because all other items must shift.

### Memory

Lists over-allocate space to make appending efficient. A list with four items may have space allocated for eight. This means lists use slightly more memory than the items themselves require.

## Tuples

Tuples are fixed-size arrays. They have the same O(1) indexing as lists but use less memory because they do not need to over-allocate.

| Operation | Time complexity |
|-----------|----------------|
| Access by index (`tpl[i]`) | O(1) |
| Membership test (`x in tpl`) | O(n) |
| Length (`len(tpl)`) | O(1) |

**Key insight:** Tuples are faster to create and use slightly less memory than lists of the same size, making them a good choice for data that does not change.

## Dictionaries

Dictionaries are implemented as hash tables, which provide fast key-based operations at the cost of additional memory.

| Operation | Average case | Worst case |
|-----------|-------------|------------|
| Lookup (`d[key]`) | O(1) | O(n) |
| Insert (`d[key] = value`) | O(1) | O(n) |
| Delete (`del d[key]`) | O(1) | O(n) |
| Membership (`key in d`) | O(1) | O(n) |
| Iteration | O(n) | O(n) |

The worst case of O(n) arises from hash collisions and is extremely rare in practice.

**Key insight:** Dictionaries trade memory for speed. They use significantly more memory than lists but provide constant-time lookups.

## Sets

Sets share the same hash table implementation as dictionaries (without storing values), so their performance characteristics are similar.

| Operation | Average case |
|-----------|-------------|
| Add (`s.add(x)`) | O(1) |
| Remove (`s.remove(x)`) | O(1) |
| Membership (`x in s`) | O(1) |
| Union (`a \ b`) | O(len(a) + len(b)) |
| Intersection (`a & b`) | O(min(len(a), len(b))) |

**Key insight:** Use sets instead of lists when you primarily need to test membership. A membership test that takes O(n) in a list takes O(1) in a set.

## Comparison table

| Operation | List | Tuple | Dict | Set |
|-----------|------|-------|------|-----|
| Access by index | O(1) | O(1) | — | — |
| Access by key | — | — | O(1) | — |
| Membership test | O(n) | O(n) | O(1) | O(1) |
| Append/add | O(1) | — | O(1) | O(1) |
| Insert at start | O(n) | — | — | — |
| Delete | O(n) | — | O(1) | O(1) |
| Sort | O(n log n) | — | — | — |

## Memory comparison

You can use `sys.getsizeof()` to see the memory used by each structure:

```python
import sys

lst = list(range(1000))
tpl = tuple(range(1000))
dct = {i: i for i in range(1000)}
st = set(range(1000))

print(f"List:       {sys.getsizeof(lst):,} bytes")
print(f"Tuple:      {sys.getsizeof(tpl):,} bytes")
print(f"Dictionary: {sys.getsizeof(dct):,} bytes")
print(f"Set:        {sys.getsizeof(st):,} bytes")
```

In general, tuples use the least memory, followed by lists, then sets and dictionaries.

## When performance matters

### Premature optimisation

For most programs, the choice of data structure matters far more for **correctness and readability** than for performance. A dictionary with 100 items is fast no matter what operations you perform on it. Performance differences only become meaningful with large datasets or in tight loops.

As a general rule: write clear code first, then optimise the parts that are actually slow.

### Readability versus speed

Choosing a more complex data structure to save a few microseconds is rarely worth the loss in readability. If a list comprehension is clear and the dataset is small, use it — even if a generator expression would be slightly more memory-efficient.

### The right structure for the job

The most impactful performance decision is usually choosing the right data structure in the first place. Using a set for membership testing instead of a list can turn an O(n) operation into O(1) — a far greater improvement than any micro-optimisation.

## Generators and lazy evaluation

When working with very large datasets, consider using **generators** instead of building entire lists in memory:

```python
# This creates a list of one million items in memory
squares = [x ** 2 for x in range(1_000_000)]

# This generates items one at a time
squares = (x ** 2 for x in range(1_000_000))
```

Generator expressions use parentheses instead of square brackets and produce items lazily — one at a time as they are needed. This is useful when you only need to iterate over the items once.

## Summary

Each data structure offers different performance characteristics. Lists provide fast indexing but slow membership testing. Dictionaries and sets provide fast lookups but use more memory. Tuples are lightweight and immutable. Understanding these trade-offs helps you make informed decisions, but remember that clarity and correctness should come first — optimise only when you have evidence that performance is a problem.
