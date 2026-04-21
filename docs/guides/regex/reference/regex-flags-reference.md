# Regex flags reference

This reference describes all flags available in Python's `re` module. Flags modify the behaviour of pattern matching and can be passed to `re.compile()`, `re.search()`, and other `re` functions.

For the official documentation, see the [Python `re` module documentation](https://docs.python.org/3/library/re.html#flags).

## Using flags

Flags can be passed as the `flags` parameter to any `re` function, or combined with the bitwise OR operator (`|`).

```python
import re

# Single flag
re.search(r'hello', 'HELLO', re.IGNORECASE)

# Multiple flags combined
re.search(r'hello.world', 'HELLO\nWORLD', re.IGNORECASE | re.DOTALL)
```

Flags can also be set within a pattern using **inline flag syntax**: `(?flags)` at the start of the pattern.

```python
import re

# Inline flag for case-insensitive matching
re.search(r'(?i)hello', 'HELLO')
```

## Flag reference

### `re.IGNORECASE` (short form: `re.I`)

**Inline syntax:** `(?i)`

Makes the pattern match regardless of case. Both uppercase and lowercase characters match.

```python
import re

re.findall(r'python', 'Python PYTHON python', re.IGNORECASE)
# ['Python', 'PYTHON', 'python']
```

**Effect on character classes:**

- `[a-z]` with `re.IGNORECASE` also matches uppercase letters
- `[A-Z]` with `re.IGNORECASE` also matches lowercase letters

---

### `re.MULTILINE` (short form: `re.M`)

**Inline syntax:** `(?m)`

Changes the behaviour of `^` and `$`:

| Anchor | Without `re.MULTILINE` | With `re.MULTILINE` |
|---|---|---|
| `^` | Matches only at the start of the string | Matches at the start of each line |
| `$` | Matches only at the end of the string | Matches at the end of each line |

```python
import re

text = """Line one
Line two
Line three"""

# Without MULTILINE
re.findall(r'^Line \w+', text)
# ['Line one']

# With MULTILINE
re.findall(r'^Line \w+', text, re.MULTILINE)
# ['Line one', 'Line two', 'Line three']
```

!!! note
    The `\A` and `\Z` anchors always match the start and end of the entire string, regardless of the `re.MULTILINE` flag.

---

### `re.DOTALL` (short form: `re.S`)

**Inline syntax:** `(?s)`

Makes the dot (`.`) match **any** character, including newlines. Without this flag, `.` matches everything except `\n`.

```python
import re

text = 'first\nsecond'

# Without DOTALL
re.search(r'first.second', text)
# None

# With DOTALL
re.search(r'first.second', text, re.DOTALL).group()
# 'first\nsecond'
```

---

### `re.VERBOSE` (short form: `re.X`)

**Inline syntax:** `(?x)`

Allows you to write more readable patterns by:

- Ignoring whitespace (spaces, tabs, and newlines) unless escaped or inside a character class
- Allowing comments with `#` (everything from `#` to the end of the line is ignored)

```python
import re

# Without VERBOSE: compact but hard to read
pattern_compact = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# With VERBOSE: readable with comments
pattern_verbose = re.compile(r"""
    [a-zA-Z0-9._%+-]+    # Local part
    @                      # @ symbol
    [a-zA-Z0-9.-]+        # Domain name
    \.                     # Literal dot
    [a-zA-Z]{2,}          # Top-level domain
""", re.VERBOSE)
```

!!! tip
    The `re.VERBOSE` flag is especially useful for complex patterns. It makes patterns self-documenting and easier to maintain.

---

### `re.ASCII` (short form: `re.A`)

**Inline syntax:** `(?a)`

Restricts `\w`, `\W`, `\b`, `\B`, `\d`, `\D`, `\s`, and `\S` to match ASCII characters only. In Python 3, these sequences match Unicode characters by default.

| Sequence | Default (Unicode) | With `re.ASCII` |
|---|---|---|
| `\d` | All Unicode digits | Only `[0-9]` |
| `\w` | All Unicode word characters | Only `[a-zA-Z0-9_]` |
| `\s` | All Unicode whitespace | Only `[ \t\n\r\f\v]` |

```python
import re

# Default: Unicode digits match
re.findall(r'\d+', 'Price: ١٢٣')
# ['١٢٣'] (Arabic-Indic digits)

# With ASCII: only 0-9 match
re.findall(r'\d+', 'Price: ١٢٣', re.ASCII)
# []
```

---

### `re.UNICODE` (short form: `re.U`)

**Inline syntax:** `(?u)`

In Python 3, this flag is enabled by default and has no additional effect for string patterns. It exists for compatibility with Python 2.

For byte patterns, `re.UNICODE` is not available.

---

### `re.LOCALE` (short form: `re.L`)

**Inline syntax:** `(?L)`

Makes `\w`, `\W`, `\b`, `\B`, and case-insensitive matching dependent on the current locale. This flag is discouraged because locale settings can vary between systems and produce inconsistent results.

!!! warning
    The use of `re.LOCALE` is discouraged. Use `re.UNICODE` (the default) or `re.ASCII` instead.

## Combining flags

Combine multiple flags using the bitwise OR operator (`|`).

```python
import re

# Case-insensitive, multiline, verbose
pattern = re.compile(r"""
    ^error:    # Match 'error:' at start of line
    \s+        # One or more whitespace characters
    (.+)       # Capture the error message
""", re.IGNORECASE | re.MULTILINE | re.VERBOSE)

text = """Info: all good
Error: something broke
Error: another issue"""

matches = pattern.findall(text)
print(matches)  # ['something broke', 'another issue']
```

## Inline flags

Flags can be set within the pattern itself using the `(?flags)` syntax at the beginning of the pattern.

| Inline syntax | Equivalent flag |
|---|---|
| `(?i)` | `re.IGNORECASE` |
| `(?m)` | `re.MULTILINE` |
| `(?s)` | `re.DOTALL` |
| `(?x)` | `re.VERBOSE` |
| `(?a)` | `re.ASCII` |
| `(?u)` | `re.UNICODE` |
| `(?L)` | `re.LOCALE` |

Multiple inline flags can be combined: `(?im)` sets both `re.IGNORECASE` and `re.MULTILINE`.

### Scoped inline flags

You can apply flags to part of a pattern using the syntax `(?flags:...)`.

```python
import re

# Only the part inside the group is case-insensitive
re.search(r'(?i:hello) world', 'HELLO world')
# <re.Match object; match='HELLO world'>

re.search(r'(?i:hello) world', 'HELLO WORLD')
# None (world is still case-sensitive)
```

## Flags summary table

| Flag | Short | Inline | Description |
|---|---|---|---|
| `re.IGNORECASE` | `re.I` | `(?i)` | Case-insensitive matching |
| `re.MULTILINE` | `re.M` | `(?m)` | `^` and `$` match at line boundaries |
| `re.DOTALL` | `re.S` | `(?s)` | `.` matches newlines |
| `re.VERBOSE` | `re.X` | `(?x)` | Allow comments and whitespace in patterns |
| `re.ASCII` | `re.A` | `(?a)` | ASCII-only matching for `\w`, `\d`, `\s`, and so on |
| `re.UNICODE` | `re.U` | `(?u)` | Unicode matching (default in Python 3) |
| `re.LOCALE` | `re.L` | `(?L)` | Locale-dependent matching (discouraged) |
