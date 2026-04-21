# List methods

This reference documents all methods available on Python list objects and the built-in functions commonly used with lists.

## `append()`

```python
list.append(item)
```

Add an item to the end of the list. Modifies the list in place and returns `None`.

```python
fruits = ["apple", "banana"]
fruits.append("cherry")
# fruits is now ["apple", "banana", "cherry"]
```

## `clear()`

```python
list.clear()
```

Remove all items from the list, leaving it empty.

```python
numbers = [1, 2, 3]
numbers.clear()
# numbers is now []
```

## `copy()`

```python
list.copy()
```

Return a shallow copy of the list. Changes to the copy do not affect the original.

```python
original = [1, 2, 3]
duplicate = original.copy()
```

## `count()`

```python
list.count(value)
```

Return the number of times a value appears in the list.

```python
numbers = [1, 2, 2, 3, 2]
print(numbers.count(2))  # 3
```

## `extend()`

```python
list.extend(iterable)
```

Add all items from an iterable to the end of the list. This is equivalent to `list += iterable`.

```python
fruits = ["apple", "banana"]
fruits.extend(["cherry", "date"])
# fruits is now ["apple", "banana", "cherry", "date"]
```

## `index()`

```python
list.index(value, start=0, stop=len(list))
```

Return the index of the first occurrence of a value. Raises `ValueError` if the value is not found.

| Parameter | Description |
|-----------|-------------|
| `value`   | The value to search for |
| `start`   | Optional start index for the search |
| `stop`    | Optional stop index for the search |

```python
letters = ["a", "b", "c", "b"]
print(letters.index("b"))     # 1
print(letters.index("b", 2))  # 3
```

## `insert()`

```python
list.insert(index, item)
```

Insert an item at the given index. Items at and after the index are shifted to the right.

```python
fruits = ["apple", "cherry"]
fruits.insert(1, "banana")
# fruits is now ["apple", "banana", "cherry"]
```

## `pop()`

```python
list.pop(index=-1)
```

Remove and return the item at the given index. If no index is specified, removes and returns the last item. Raises `IndexError` if the list is empty or the index is out of range.

```python
fruits = ["apple", "banana", "cherry"]
last = fruits.pop()      # "cherry"
first = fruits.pop(0)    # "apple"
```

## `remove()`

```python
list.remove(value)
```

Remove the first occurrence of a value from the list. Raises `ValueError` if the value is not found.

```python
fruits = ["apple", "banana", "cherry"]
fruits.remove("banana")
# fruits is now ["apple", "cherry"]
```

## `reverse()`

```python
list.reverse()
```

Reverse the items of the list in place.

```python
numbers = [1, 2, 3]
numbers.reverse()
# numbers is now [3, 2, 1]
```

## `sort()`

```python
list.sort(key=None, reverse=False)
```

Sort the list in place. Returns `None`.

| Parameter | Description |
|-----------|-------------|
| `key`     | A function that extracts a comparison key from each item |
| `reverse` | If `True`, sort in descending order |

```python
numbers = [3, 1, 4, 1, 5]
numbers.sort()
# numbers is now [1, 1, 3, 4, 5]

words = ["banana", "apple", "cherry"]
words.sort(key=len)
# words is now ["apple", "banana", "cherry"]
```

## Built-in functions for lists

### `len()`

Return the number of items in the list.

```python
print(len([1, 2, 3]))  # 3
```

### `min()` and `max()`

Return the smallest or largest item in the list.

```python
numbers = [3, 1, 4, 1, 5]
print(min(numbers))  # 1
print(max(numbers))  # 5
```

### `sum()`

Return the sum of all items in the list.

```python
print(sum([1, 2, 3, 4]))  # 10
```

### `sorted()`

Return a new sorted list without modifying the original. Accepts the same `key` and `reverse` parameters as `sort()`.

```python
numbers = [3, 1, 4]
ordered = sorted(numbers)  # [1, 3, 4]
# numbers is still [3, 1, 4]
```

### `reversed()`

Return a reverse iterator. Use `list()` to convert it to a list.

```python
numbers = [1, 2, 3]
rev = list(reversed(numbers))  # [3, 2, 1]
# numbers is still [1, 2, 3]
```

### `enumerate()`

Return an iterator of `(index, item)` pairs.

```python
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

### `zip()`

Combine items from multiple lists into tuples.

```python
names = ["Alice", "Bob"]
ages = [30, 25]
for name, age in zip(names, ages):
    print(f"{name} is {age}")
```
