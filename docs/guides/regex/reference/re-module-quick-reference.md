# `re` module quick reference

This reference provides a comprehensive summary of all functions and key objects in Python's `re` module.

For the official documentation, see the [Python `re` module documentation](https://docs.python.org/3/library/re.html).

## Module-level functions

All module-level functions accept an optional `flags` parameter. See the [Regex flags reference](regex-flags-reference.md) for details.

### Searching and matching

| Function | Description |
|---|---|
| `re.search(pattern, string, flags=0)` | Scan through `string` for the first location where `pattern` matches. Returns a match object or `None`. |
| `re.match(pattern, string, flags=0)` | Check for a match only at the **beginning** of `string`. Returns a match object or `None`. |
| `re.fullmatch(pattern, string, flags=0)` | Check whether the **entire** `string` matches `pattern`. Returns a match object or `None`. |

```python
import re

re.search(r'\d+', 'abc 123 def')    # <re.Match object; match='123'>
re.match(r'\d+', 'abc 123 def')     # None (no match at start)
re.match(r'\d+', '123 def')         # <re.Match object; match='123'>
re.fullmatch(r'\d+', '123')         # <re.Match object; match='123'>
re.fullmatch(r'\d+', '123 def')     # None (not entire string)
```

### Finding all matches

| Function | Description |
|---|---|
| `re.findall(pattern, string, flags=0)` | Return a list of all non-overlapping matches. If the pattern has groups, returns a list of groups (or tuples of groups). |
| `re.finditer(pattern, string, flags=0)` | Return an iterator of match objects for all non-overlapping matches. |

```python
import re

re.findall(r'\d+', 'a1 b22 c333')
# ['1', '22', '333']

re.findall(r'(\w)(\d+)', 'a1 b22 c333')
# [('a', '1'), ('b', '22'), ('c', '333')]

for m in re.finditer(r'\d+', 'a1 b22 c333'):
    print(m.group(), m.span())
# 1 (1, 2)
# 22 (4, 6)
# 333 (8, 11)
```

### Substitution

| Function | Description |
|---|---|
| `re.sub(pattern, repl, string, count=0, flags=0)` | Replace all occurrences of `pattern` in `string` with `repl`. If `count` is given, replace at most `count` occurrences. `repl` can be a string or a function. |
| `re.subn(pattern, repl, string, count=0, flags=0)` | Same as `re.sub()`, but returns a tuple `(new_string, number_of_replacements)`. |

```python
import re

re.sub(r'\d+', 'X', 'a1 b22 c333')
# 'aX bX cX'

re.sub(r'(\w+), (\w+)', r'\2 \1', 'Smith, Alice')
# 'Alice Smith'

re.subn(r'\d+', 'X', 'a1 b22 c333')
# ('aX bX cX', 3)
```

**Using a function as the replacement:**

```python
import re

def double(match: re.Match) -> str:
    return str(int(match.group()) * 2)

re.sub(r'\d+', double, 'a1 b2 c3')
# 'a2 b4 c6'
```

### Splitting

| Function | Description |
|---|---|
| `re.split(pattern, string, maxsplit=0, flags=0)` | Split `string` by occurrences of `pattern`. If `maxsplit` is given, at most `maxsplit` splits are made. If the pattern contains capturing groups, the group text is included in the result. |

```python
import re

re.split(r'\s+', 'one  two   three')
# ['one', 'two', 'three']

re.split(r'([,;])', 'a,b;c')
# ['a', ',', 'b', ';', 'c']

re.split(r'\s+', 'one two three', maxsplit=1)
# ['one', 'two three']
```

### Compiling patterns

| Function | Description |
|---|---|
| `re.compile(pattern, flags=0)` | Compile a pattern string into a pattern object. The pattern object has the same methods as the `re` module (`search()`, `match()`, `findall()`, and so on). |
| `re.escape(pattern)` | Escape all metacharacters in `pattern` so that it can be used as a literal match. |
| `re.purge()` | Clear the internal pattern cache. |

```python
import re

pattern = re.compile(r'\d+')
pattern.search('abc 123')       # <re.Match object; match='123'>
pattern.findall('a1 b22 c333')  # ['1', '22', '333']

re.escape('price: $5.00 (USD)')
# 'price:\\ \\$5\\.00\\ \\(USD\\)'
```

## Pattern object methods

A compiled pattern object (returned by `re.compile()`) provides the following methods. They behave identically to the corresponding module-level functions, except that the pattern does not need to be passed as an argument.

| Method | Description |
|---|---|
| `pattern.search(string, pos=0, endpos=len(string))` | Search for a match, optionally within a slice of `string`. |
| `pattern.match(string, pos=0, endpos=len(string))` | Match at the beginning, optionally within a slice. |
| `pattern.fullmatch(string, pos=0, endpos=len(string))` | Match the entire string, optionally within a slice. |
| `pattern.findall(string, pos=0, endpos=len(string))` | Find all non-overlapping matches. |
| `pattern.finditer(string, pos=0, endpos=len(string))` | Iterate over all matches. |
| `pattern.sub(repl, string, count=0)` | Replace matches. |
| `pattern.subn(repl, string, count=0)` | Replace matches and return the count. |
| `pattern.split(string, maxsplit=0)` | Split on matches. |

### Pattern object attributes

| Attribute | Description |
|---|---|
| `pattern.pattern` | The original pattern string. |
| `pattern.flags` | The flags used to compile the pattern. |
| `pattern.groups` | The number of capturing groups in the pattern. |
| `pattern.groupindex` | A dictionary mapping named group names to group numbers. |

## Match object methods

A match object (returned by `search()`, `match()`, `fullmatch()`, or from `finditer()`) provides the following methods and attributes.

### Methods

| Method | Description |
|---|---|
| `match.group(n=0)` | Return the text matched by group `n`. Group 0 is the entire match. |
| `match.group(name)` | Return the text matched by the named group `name`. |
| `match.groups(default=None)` | Return a tuple of all captured groups. |
| `match.groupdict(default=None)` | Return a dictionary of all named groups. |
| `match.start(group=0)` | Return the start position of the match for the given group. |
| `match.end(group=0)` | Return the end position of the match for the given group. |
| `match.span(group=0)` | Return a tuple `(start, end)` for the given group. |
| `match.expand(template)` | Return the string obtained by performing backreference substitution on `template`. |

### Attributes

| Attribute | Description |
|---|---|
| `match.re` | The pattern object that produced this match. |
| `match.string` | The string passed to `search()` or `match()`. |
| `match.pos` | The value of `pos` passed to the search method. |
| `match.endpos` | The value of `endpos` passed to the search method. |
| `match.lastindex` | The index of the last matched capturing group, or `None`. |
| `match.lastgroup` | The name of the last matched named group, or `None`. |

```python
import re

match = re.search(r'(?P<first>\w+) (?P<last>\w+)', 'Alice Smith')

match.group()          # 'Alice Smith'
match.group(1)         # 'Alice'
match.group('last')    # 'Smith'
match.groups()         # ('Alice', 'Smith')
match.groupdict()      # {'first': 'Alice', 'last': 'Smith'}
match.start()          # 0
match.end()            # 11
match.span()           # (0, 11)
match.span(1)          # (0, 5)
```

## Backreferences in replacement strings

When using `re.sub()`, the replacement string can reference captured groups:

| Syntax | Description |
|---|---|
| `\1`, `\2`, and so on | Reference numbered groups |
| `\g<1>`, `\g<2>`, and so on | Reference numbered groups (unambiguous form) |
| `\g<name>` | Reference named groups |
| `\g<0>` | Reference the entire match |

```python
import re

# Swap first and last names using numbered backreferences
re.sub(r'(\w+) (\w+)', r'\2 \1', 'Alice Smith')
# 'Smith Alice'

# Convert date format using named backreferences
re.sub(
    r'(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})',
    r'\g<year>-\g<month>-\g<day>',
    '25/12/2026',
)
# '2026-12-25'
```

## Exceptions

| Exception | Description |
|---|---|
| `re.error` | Raised when a pattern string is not a valid regular expression. The exception has `msg`, `pattern`, `pos`, `lineno`, and `colno` attributes. |

```python
import re

try:
    re.compile(r'[invalid')
except re.error as e:
    print(f'Error: {e.msg} at position {e.pos}')
```
