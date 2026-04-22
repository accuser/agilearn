# Avoid common regex mistakes

**The question.** You've written a pattern, it doesn't match what you expected, and you're staring at it wondering whether the bug is in the regex or in your assumptions about it. This page is the short list of the bugs that catch nearly everyone — each with the smallest code snippet that shows the trap and the fix.

## The answer

| If this sounds familiar … | Reach for … |
| --- | --- |
| `\b` or `\d` in a pattern did nothing | A raw string: `r'\bword\b'`, not `'\bword\b'` |
| `.+` or `.*` swallowed far more than you wanted | The lazy form: `.+?` or `.*?` |
| A dot matched characters you wanted to keep literal | Escape it: `\.` (or use `re.escape(str)`) |
| `re.match` returned `None` on input that clearly has the pattern | `re.search` (or anchor the pattern) |
| A validation pattern let partial matches through | `re.fullmatch` or `^...$` |
| A pattern that normally matches fast hangs on odd input | Flatten nested quantifiers |
| `.` refused to match across a newline | Pass `re.DOTALL` or use `[\s\S]` |
| A tight loop is spending all its time in `re` | `re.compile` once, reuse the compiled object |

## Why each of these bites

### Not using raw strings

Python strings interpret backslash escapes before the `re` module ever sees them. `'\b'` is already a backspace character by the time `re.compile` gets hold of it, so the `\b` word-boundary anchor never reaches the engine.

```python
import re

re.search('\bword\b', 'a word here')   # None — looking for literal \b
re.search(r'\bword\b', 'a word here')  # matches 'word'
```

Treat `r'...'` as mandatory for any pattern with a backslash in it.

### Greedy when you wanted lazy

`+` and `*` match **as much as they possibly can** and still allow the rest of the pattern to succeed. A `?` after the quantifier flips it to *as little as possible*.

```python
text = '<b>bold</b> and <i>italic</i>'
re.search(r'<.+>',  text).group()   # '<b>bold</b> and <i>italic</i>'
re.search(r'<.+?>', text).group()   # '<b>'
```

### Unescaped metacharacters

A bare `.` matches any character, a bare `+` is a quantifier, a bare `(` opens a group. When you want the literal character, escape it with `\` — or run the whole string through `re.escape`.

```python
re.search(r'example.com',  'exampleXcom')   # matches (unwanted)
re.search(r'example\.com', 'exampleXcom')   # None (correct)

re.escape('price is $5.00 (USD)')
# 'price\\ is\\ \\$5\\.00\\ \\(USD\\)'
```

### `re.match` only looks at the start

`re.match('\d+', 'error 404')` returns `None` because there's no digit at position zero. Use `re.search` for 'somewhere in the string' and reserve `re.match` for 'starts with …'.

### Not anchoring validation patterns

`re.search(r'\d{3}', 'abc123def')` matches the `123` in the middle. For validation, use `re.fullmatch` or wrap the pattern in `^...$`:

```python
re.fullmatch(r'\d{3}', 'abc123def')  # None
re.fullmatch(r'\d{3}', '123')        # matches
```

### Catastrophic backtracking

Nested quantifiers like `(a+)+b` create exponentially many ways to match any given input. On a non-match the engine tries all of them before giving up — on 25 `a`s followed by a `c`, that's minutes rather than microseconds.

```python
re.compile(r'a+b').search('aaab')            # fast, matches
re.compile(r'a+b').search('a' * 25 + 'c')    # fast, None
# re.compile(r'(a+)+b').search('a' * 25 + 'c')  # do not run
```

Flatten the repetition whenever you can.

### `.` doesn't match newlines by default

Pass `re.DOTALL` (or use `[\s\S]` in the pattern) when you genuinely need a wildcard that crosses line boundaries.

```python
text = 'line one\nline two'
re.search(r'one.line', text)               # None
re.search(r'one.line', text, re.DOTALL)    # matches
```

### Compiling inside a loop

```python
pattern = re.compile(r'\b\w+\b')
for text in texts:
    pattern.search(text)   # no re-compile, no cache lookup
```

The `re` module caches recent patterns, but the cache is small and shared across your whole program. Compiling once makes the cost explicit and predictable.

## Trade-offs and when to ignore this list

- **Greedy is sometimes the right default.** If you're matching against the *longest* sensible substring (everything up to the final separator, for instance), greedy quantifiers are what you want. Lazy is a choice, not a rule.
- **`re.match` vs `re.search` is a semantic choice.** `re.match` is the correct function for "does this string start with …". The bug is using it when you meant "contains", not using it at all.
- **`re.VERBOSE` tidies complex patterns.** If any one bullet above led you to write a longer, more defensive pattern, pass `re.VERBOSE` and break it across lines with inline comments — future you will be able to read it.
- **Compilation only matters when it matters.** For one-shot calls, the module-level cache makes `re.search` and `pattern.search` almost identical. Reach for `re.compile` in loops, library code, and anywhere the intent is worth making explicit.

## Related

- **Learn** — [Character classes and quantifiers](../learn/02-character-classes-and-quantifiers.ipynb) for the semantics of `*`, `+`, `?`, and their lazy variants.
- **Learn** — [Find and replace](../learn/04-find-and-replace.ipynb) for `re.sub` and the overlap between matching and substitution.
- **Reference** — [Regex flags](../reference/regex-flags-reference.md) for `DOTALL`, `MULTILINE`, `VERBOSE`, and friends.
- **Concepts** — [Understanding the regex engine](../concepts/understanding-the-regex-engine.md) for why backtracking is expensive.
