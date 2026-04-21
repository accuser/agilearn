# Avoid common regex mistakes

This guide covers the most frequent mistakes people make when writing regular expressions in Python and how to avoid them. Each section describes a common pitfall, explains why it is a problem, and provides the correct approach.

## Prerequisites

- Familiarity with basic regex concepts (character classes, quantifiers, groups, and anchors)
- Python 3.12 or later

## Forgetting to use raw strings

**The mistake:** Writing regex patterns as ordinary strings, causing backslashes to be interpreted as Python escape sequences before the `re` module sees them.

```python
import re

# Wrong: \b is interpreted as a backspace character
match = re.search('\bword\b', 'a word here')
print(match)  # None (unexpected)

# Correct: use a raw string
match = re.search(r'\bword\b', 'a word here')
print(match)  # <re.Match object; span=(2, 6), match='word'>
```

**The fix:** Always use raw strings (`r'...'`) for regex patterns.

## Greedy matching when you want lazy

**The mistake:** Using a greedy quantifier (`*` or `+`) when you need a lazy one, causing the pattern to match more text than intended.

```python
import re

text = '<b>bold</b> and <i>italic</i>'

# Wrong: greedy .+ matches too much
match = re.search(r'<.+>', text)
print(match.group())  # '<b>bold</b> and <i>italic</i>'

# Correct: lazy .+? stops at the first >
match = re.search(r'<.+?>', text)
print(match.group())  # '<b>'
```

**The fix:** Append `?` to a quantifier to make it lazy (`+?`, `*?`, `??`). Use lazy quantifiers when you want the shortest possible match.

## Forgetting to escape metacharacters

**The mistake:** Using metacharacters (`.`, `*`, `+`, `?`, `(`, `)`, `[`, `]`, `{`, `}`, `^`, `$`, `|`, `\`) as literal characters without escaping them.

```python
import re

# Wrong: the dot matches any character
match = re.search(r'example.com', 'exampleXcom')
print(match)  # <re.Match object> (unexpected)

# Correct: escape the dot to match a literal dot
match = re.search(r'example\.com', 'exampleXcom')
print(match)  # None (as expected)
```

**The fix:** Escape metacharacters with a backslash when you want to match them literally. Alternatively, use `re.escape()` to escape an entire string.

```python
import re

user_input = 'price is $5.00 (USD)'
escaped = re.escape(user_input)
print(escaped)  # 'price\\ is\\ \\$5\\.00\\ \\(USD\\)'
```

## Using `re.match()` when you mean `re.search()`

**The mistake:** Using `re.match()` expecting it to find a pattern anywhere in the string. The `re.match()` function only checks at the **beginning** of the string.

```python
import re

text = 'The error code is 404'

# Wrong: re.match() only checks the beginning
match = re.match(r'\d+', text)
print(match)  # None

# Correct: re.search() scans the entire string
match = re.search(r'\d+', text)
print(match.group())  # '404'
```

**The fix:** Use `re.search()` to find a pattern anywhere in a string. Reserve `re.match()` for when you specifically need to check the beginning.

## Not anchoring validation patterns

**The mistake:** Using `re.search()` to validate input without anchoring the pattern, allowing partial matches to pass validation.

```python
import re

# Wrong: this matches the '123' inside the string
if re.search(r'\d{3}', 'abc123def'):
    print('Valid')  # Prints 'Valid' (unexpected)

# Correct: use anchors or re.fullmatch()
if re.fullmatch(r'\d{3}', 'abc123def'):
    print('Valid')
else:
    print('Invalid')  # Prints 'Invalid' (as expected)
```

**The fix:** Use `re.fullmatch()` or anchor your pattern with `^` and `$` when validating that an entire string matches a pattern.

## Catastrophic backtracking

**The mistake:** Writing patterns with nested quantifiers that cause the regex engine to explore an exponential number of possibilities on non-matching input.

```python
import re

# Dangerous pattern: nested quantifiers
# This can take a very long time on non-matching input
pattern = re.compile(r'(a+)+b')

# Fine for matching input
print(pattern.search('aaab'))  # Matches quickly

# Extremely slow for non-matching input with many 'a' characters
# pattern.search('a' * 25 + 'c')  # Do not run this!
```

**The fix:** Avoid nested quantifiers where possible. When you need them, use atomic grouping or possessive quantifiers (available in some regex engines), or restructure the pattern.

```python
import re

# Safe version: remove the unnecessary nesting
pattern = re.compile(r'a+b')
print(pattern.search('aaab'))  # Matches quickly
print(pattern.search('a' * 25 + 'c'))  # Returns None quickly
```

## Assuming `.` matches everything

**The mistake:** Expecting the dot (`.`) to match newline characters. By default, `.` matches any character **except** newlines.

```python
import re

text = 'line one\nline two'

# Without DOTALL: dot does not match newlines
match = re.search(r'one.line', text)
print(match)  # None

# With DOTALL: dot matches newlines too
match = re.search(r'one.line', text, re.DOTALL)
print(match.group())  # 'one\nline'
```

**The fix:** Use the `re.DOTALL` flag when you need `.` to match newline characters. Alternatively, use `[\s\S]` to match any character including newlines without changing the flag.

## Not compiling frequently used patterns

**The mistake:** Calling `re.search()` or `re.findall()` with a pattern string inside a loop, causing the pattern to be recompiled on every iteration.

```python
import re

texts = ['text one', 'text two', 'text three']

# Inefficient: pattern is compiled on every iteration
for text in texts:
    re.search(r'\b\w+\b', text)

# Better: compile once, use many times
pattern = re.compile(r'\b\w+\b')
for text in texts:
    pattern.search(text)
```

**The fix:** Use `re.compile()` to compile the pattern once before the loop. The `re` module does cache recently used patterns, but explicit compilation makes the intent clear and avoids cache limitations.

## Summary

| Mistake | Fix |
|---|---|
| Not using raw strings | Always use `r'...'` for patterns |
| Greedy when lazy is needed | Add `?` after the quantifier |
| Unescaped metacharacters | Use `\` or `re.escape()` |
| `re.match()` instead of `re.search()` | Use `re.search()` to find anywhere |
| Missing anchors for validation | Use `re.fullmatch()` or `^...$` |
| Catastrophic backtracking | Avoid nested quantifiers |
| Assuming `.` matches newlines | Use `re.DOTALL` when needed |
| Not compiling patterns | Use `re.compile()` in loops |
