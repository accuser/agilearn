# Dictionary methods

This reference documents all methods available on Python `dict` objects.

## `clear()`

```python
dict.clear()
```

Remove all items from the dictionary.

```python
data = {"a": 1, "b": 2}
data.clear()
# data is now {}
```

## `copy()`

```python
dict.copy()
```

Return a shallow copy of the dictionary.

```python
original = {"a": 1, "b": 2}
duplicate = original.copy()
```

## `fromkeys()`

```python
dict.fromkeys(iterable, value=None)
```

Create a new dictionary with keys from an iterable and all values set to the same value.

```python
keys = ["name", "age", "city"]
template = dict.fromkeys(keys, "unknown")
# {"name": "unknown", "age": "unknown", "city": "unknown"}
```

## `get()`

```python
dict.get(key, default=None)
```

Return the value for a key if it exists, otherwise return the default value. Does not raise `KeyError`.

```python
person = {"name": "Alice", "age": 30}
print(person.get("name"))          # "Alice"
print(person.get("email"))         # None
print(person.get("email", "N/A"))  # "N/A"
```

## `items()`

```python
dict.items()
```

Return a view object containing `(key, value)` tuples. The view reflects changes to the dictionary.

```python
person = {"name": "Alice", "age": 30}
for key, value in person.items():
    print(f"{key}: {value}")
```

## `keys()`

```python
dict.keys()
```

Return a view object containing the dictionary keys. Supports set operations such as `&`, `|`, and `-`.

```python
person = {"name": "Alice", "age": 30}
print(list(person.keys()))  # ["name", "age"]
```

## `pop()`

```python
dict.pop(key, default)
```

Remove and return the value for a key. If the key is not found and a default is provided, return the default. If no default is provided, raises `KeyError`.

```python
person = {"name": "Alice", "age": 30}
age = person.pop("age")       # 30
email = person.pop("email", "N/A")  # "N/A"
```

## `popitem()`

```python
dict.popitem()
```

Remove and return the last inserted `(key, value)` pair. Raises `KeyError` if the dictionary is empty.

```python
person = {"name": "Alice", "age": 30}
last = person.popitem()  # ("age", 30)
```

## `setdefault()`

```python
dict.setdefault(key, default=None)
```

If the key exists, return its value. If it does not exist, insert the key with the default value and return the default.

```python
counts = {"apples": 3}
counts.setdefault("apples", 0)   # Returns 3 (key exists)
counts.setdefault("bananas", 0)  # Returns 0 (key added)
# counts is now {"apples": 3, "bananas": 0}
```

## `update()`

```python
dict.update(mapping_or_iterable)
```

Update the dictionary with key-value pairs from another dictionary or an iterable of `(key, value)` pairs. Existing keys are overwritten.

```python
config = {"debug": False, "port": 8080}
config.update({"debug": True, "host": "localhost"})
# {"debug": True, "port": 8080, "host": "localhost"}
```

## `values()`

```python
dict.values()
```

Return a view object containing the dictionary values.

```python
prices = {"apples": 1.50, "bread": 1.20}
print(list(prices.values()))  # [1.50, 1.20]
```

## Operators

### Merge with `|` (Python 3.9+)

Create a new dictionary by merging two dictionaries. Values from the right-hand dictionary take precedence:

```python
defaults = {"colour": "blue", "size": "medium"}
overrides = {"size": "large"}
config = defaults | overrides
# {"colour": "blue", "size": "large"}
```

### Update with `|=` (Python 3.9+)

Update a dictionary in place:

```python
config = {"colour": "blue"}
config |= {"size": "large"}
```

### Unpacking with `**`

Merge dictionaries using unpacking:

```python
merged = {**defaults, **overrides}
```

## Built-in functions

### `len()`

Return the number of key-value pairs in the dictionary.

```python
print(len({"a": 1, "b": 2}))  # 2
```

### `dict()`

Create a dictionary from keyword arguments or an iterable of pairs.

```python
person = dict(name="Alice", age=30)
prices = dict([("apples", 1.50), ("bread", 1.20)])
```
