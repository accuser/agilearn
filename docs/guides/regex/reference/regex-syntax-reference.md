# Regex syntax reference

This reference covers the complete regular expression syntax supported by Python's `re` module. Use it as a lookup resource when building patterns.

For the official documentation, see the [Python Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) and the [`re` module documentation](https://docs.python.org/3/library/re.html).

## Literal characters

Most characters match themselves literally. For example, the pattern `hello` matches the text `hello`.

The following characters have special meanings and must be escaped with a backslash (`\`) to match them literally:

```
. ^ $ * + ? { } [ ] \ | ( )
```

```python
import re

re.search(r'3\.14', '3.14')     # Matches literal dot
re.search(r'\$100', '$100')     # Matches literal dollar sign
re.search(r'file\(1\)', 'file(1)')  # Matches literal parentheses
```

## Metacharacters

### The dot (`.`)

| Pattern | Matches |
|---|---|
| `.` | Any single character except a newline (unless `re.DOTALL` is set) |

```python
import re

re.findall(r'h.t', 'hat hot hut hit')  # ['hat', 'hot', 'hut', 'hit']
```

### Anchors

Anchors match positions, not characters.

| Pattern | Matches |
|---|---|
| `^` | Start of the string (or start of each line with `re.MULTILINE`) |
| `$` | End of the string (or end of each line with `re.MULTILINE`) |
| `\b` | Word boundary (between `\w` and `\W`, or at the start/end of the string) |
| `\B` | Non-word boundary |
| `\A` | Start of the string (not affected by `re.MULTILINE`) |
| `\Z` | End of the string (not affected by `re.MULTILINE`) |

```python
import re

re.search(r'^Hello', 'Hello world')     # Matches at start
re.search(r'world$', 'Hello world')     # Matches at end
re.findall(r'\bcat\b', 'cat concatenate')  # ['cat']
```

## Character classes

Character classes match a single character from a defined set.

### Custom character classes

| Pattern | Matches |
|---|---|
| `[abc]` | Any one of `a`, `b`, or `c` |
| `[a-z]` | Any lowercase letter |
| `[A-Z]` | Any uppercase letter |
| `[0-9]` | Any digit |
| `[a-zA-Z0-9]` | Any letter or digit |
| `[^abc]` | Any character except `a`, `b`, or `c` |
| `[^0-9]` | Any non-digit character |

**Special rules inside character classes:**

- Most metacharacters lose their special meaning inside `[...]`
- The caret `^` has special meaning only at the start: `[^abc]`
- The hyphen `-` indicates a range, except at the start or end: `[-abc]` or `[abc-]`
- The closing bracket `]` must be first if included literally: `[]abc]`
- The backslash `\` still works as an escape character

### Shorthand character classes

| Pattern | Equivalent | Matches |
|---|---|---|
| `\d` | `[0-9]` | Any digit |
| `\D` | `[^0-9]` | Any non-digit |
| `\w` | `[a-zA-Z0-9_]` | Any word character (letter, digit, or underscore) |
| `\W` | `[^a-zA-Z0-9_]` | Any non-word character |
| `\s` | `[ \t\n\r\f\v]` | Any whitespace character |
| `\S` | `[^ \t\n\r\f\v]` | Any non-whitespace character |

!!! note
    With the `re.UNICODE` flag (the default in Python 3), `\d`, `\w`, and `\s` match Unicode equivalents as well. Use the `re.ASCII` flag to restrict them to ASCII characters only.

## Quantifiers

Quantifiers control how many times the preceding element is matched.

### Greedy quantifiers

Greedy quantifiers match as much text as possible.

| Pattern | Matches |
|---|---|
| `*` | Zero or more times |
| `+` | One or more times |
| `?` | Zero or one time |
| `{n}` | Exactly `n` times |
| `{n,}` | At least `n` times |
| `{n,m}` | Between `n` and `m` times (inclusive) |

### Lazy quantifiers

Lazy quantifiers match as little text as possible. They are created by appending `?` to a greedy quantifier.

| Pattern | Matches |
|---|---|
| `*?` | Zero or more times (lazy) |
| `+?` | One or more times (lazy) |
| `??` | Zero or one time (lazy) |
| `{n,}?` | At least `n` times (lazy) |
| `{n,m}?` | Between `n` and `m` times (lazy) |

```python
import re

text = '<b>bold</b>'

re.search(r'<.+>', text).group()     # '<b>bold</b>' (greedy)
re.search(r'<.+?>', text).group()    # '<b>' (lazy)
```

## Groups

### Capturing groups

| Pattern | Description |
|---|---|
| `(...)` | Create a capturing group. The matched text is accessible through `.group(n)`. |

### Named groups

| Pattern | Description |
|---|---|
| `(?P<name>...)` | Create a named capturing group. Accessible through `.group('name')` or `.groupdict()`. |
| `(?P=name)` | Backreference to a named group within the same pattern. |

### Non-capturing groups

| Pattern | Description |
|---|---|
| `(?:...)` | Group without capturing. Useful for applying quantifiers to a group. |

### Backreferences

| Pattern | Description |
|---|---|
| `\1`, `\2`, and so on | Match the same text as the corresponding numbered group. |
| `(?P=name)` | Match the same text as the named group `name`. |

```python
import re

# Backreference: match repeated words
re.search(r'\b(\w+)\s+\1\b', 'the the cat').group()
# 'the the'

# Named backreference
re.search(r'(?P<word>\w+)\s+(?P=word)', 'the the cat').group()
# 'the the'
```

## Alternation

| Pattern | Description |
|---|---|
| `a\|b` | Match either `a` or `b`. Alternation has the lowest precedence of all operators. |

```python
import re

re.findall(r'cat|dog', 'I have a cat and a dog')
# ['cat', 'dog']

# Use groups to limit the scope of alternation
re.findall(r'col(?:ou|o)r', 'colour and color')
# ['colour', 'color']
```

## Lookahead and lookbehind

Lookahead and lookbehind assertions match a position without consuming characters. They are sometimes called **zero-width assertions**.

### Lookahead

| Pattern | Description |
|---|---|
| `(?=...)` | **Positive lookahead**: matches if `...` matches next, without consuming. |
| `(?!...)` | **Negative lookahead**: matches if `...` does **not** match next. |

```python
import re

# Positive lookahead: find words followed by a colon
re.findall(r'\w+(?=:)', 'name: Alice age: 30')
# ['name', 'age']

# Negative lookahead: find words NOT followed by a colon
re.findall(r'\w+(?!:)\b', 'name: Alice age: 30')
# ['nam', 'Alice', 'ag', '30']
```

### Lookbehind

| Pattern | Description |
|---|---|
| `(?<=...)` | **Positive lookbehind**: matches if `...` matches immediately before the current position. |
| `(?<!...)` | **Negative lookbehind**: matches if `...` does **not** match immediately before. |

!!! warning
    Lookbehind patterns must be **fixed-length** in Python. You cannot use variable-length quantifiers (`*`, `+`, `{n,m}` where n and m differ) inside a lookbehind.

```python
import re

# Positive lookbehind: find numbers preceded by £
re.findall(r'(?<=£)\d+\.?\d*', 'Prices: £5.99 and £12')
# ['5.99', '12']

# Negative lookbehind: find numbers NOT preceded by £
re.findall(r'(?<!£)\b\d+\.?\d*', 'Prices: £5.99 and 12 items')
# ['99', '12']
```

## Conditional patterns

| Pattern | Description |
|---|---|
| `(?(id)yes\|no)` | Match `yes` pattern if group `id` matched, otherwise match `no` pattern. The `no` part is optional. |

```python
import re

# Match an optionally quoted word
pattern = re.compile(r'(")?(\w+)(?(1)")')
print(pattern.search('"hello"').group())   # "hello"
print(pattern.search('hello').group())     # hello
```

## Special sequences summary

| Sequence | Description |
|---|---|
| `\d` | Digit |
| `\D` | Non-digit |
| `\w` | Word character |
| `\W` | Non-word character |
| `\s` | Whitespace |
| `\S` | Non-whitespace |
| `\b` | Word boundary |
| `\B` | Non-word boundary |
| `\A` | Start of string |
| `\Z` | End of string |
| `\1` ... `\9` | Backreference to group 1\u20139 |
| `\n`, `\t`, `\r` | Newline, tab, carriage return (in raw strings, use `\n` and so on directly) |
