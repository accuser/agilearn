# How to avoid common string mistakes

# What are the most common mistakes when working with strings?

Strings feel like the easiest type in Python — until they're the thing burning a half-day of your debugging budget. Most string bugs come from a small, well-known set of traps: forgetting that strings are immutable, comparing with `is`, ignoring encoding, building strings in a loop with `+=`. This is a quick reference to the patterns that catch people.

## The answer

| Trap | What happens | What to do instead |
|---|---|---|
| Calling `text.strip()` and expecting `text` to change | Strings are immutable; the return value is discarded | `text = text.strip()` — assign the result |
| Building a string with `s += word` in a loop | O(n²) — each concatenation copies the whole string | `"".join(parts)` — single pass, allocates once |
| Comparing strings with `is` | Works *sometimes* due to interning, then breaks on dynamic input | Always use `==` for value comparison |
| `open("file.txt")` with no encoding | Picks up the system default, breaks on Windows | `open("file.txt", encoding="utf-8")` |
| `key, value = line.split("=")` when `=` might be missing | `ValueError: not enough values to unpack` | `key, sep, value = line.partition("=")` |
| `text.split()[0]` on possibly-empty input | `IndexError` on empty or whitespace-only strings | Check `if not text.split(): ...` first |
| Building user-facing templates with f-strings or `eval` | Lets template authors run arbitrary Python | `string.Template` — name substitution only, no expressions |

## Why it works

Each of these traps has the same shape: a thing that *looks* like it works, that *does* work in your test data, and that breaks the moment real input arrives.

**Immutability.** Every string method returns a new string. `text.strip()` does not modify `text` — it returns a stripped copy and throws it away if you don't catch it. The same applies to `lower`, `upper`, `replace`, `casefold`, and every other "mutating-sounding" method. There is no in-place version. Treat strings like numbers: you wouldn't write `n + 1` and expect `n` to change.

**Concatenation in a loop.** Because strings are immutable, `s += word` allocates a new string every iteration and copies the entire previous contents into it. Build a million-character string this way and you allocate a million strings and copy half a trillion characters. `"".join(parts)` walks the list once to compute the total length, allocates once, and copies once.

**`is` versus `==`.** `is` asks "are these the same object in memory?". `==` asks "do these have the same value?". For strings the two answers usually coincide because of interning — Python caches short string literals and reuses the same object — but interning is a CPython optimisation, not a language guarantee. The moment a string is built dynamically (from `input()`, from `+`, from `read()`), interning doesn't apply, and `is` becomes a coin flip. Use `is` for `None` and not much else.

**Encoding.** A text file is bytes; reading it as text requires a decoder. `open("file.txt")` uses `locale.getpreferredencoding(False)`, which is `"utf-8"` on modern Linux and macOS but historically `"cp1252"` on Windows. Code that round-trips fine on your laptop garbles characters in production. Always pass `encoding="utf-8"` (or whatever your data actually is) explicitly.

**`split` versus `partition`.** `split("=")` returns a list whose length depends on the input — handy for "give me every chunk", lethal for "give me exactly two pieces". `partition("=")` always returns three values, with the separator slot empty if it wasn't found, so destructuring assignment never raises.

**Empty strings.** `"".split()` returns `[]`, not `[""]`. `text[0]` on `""` raises `IndexError`. Decide what empty input means for your function and handle it at the top of the function, not at the call site.

**Templates.** f-strings evaluate arbitrary Python expressions. That's perfect for hard-coded format strings in your source, and dangerous for templates loaded from anywhere a user can edit. `string.Template` does name substitution and nothing else, which is exactly the right power level for user-supplied templates.

## Trade-offs

A couple of these rules have edge cases worth knowing.

`+=` for string-building is fine for short, fixed-size combinations — `prefix + name + suffix` reads well and there's no measurable cost. The performance trap only bites when the loop count grows.

CPython has an optimisation that makes `s += word` in a tight loop *sometimes* run in linear time, by mutating the string in place when it's the only reference. Don't rely on it: it's CPython-specific, it doesn't apply to PyPy or other implementations, and it stops working the moment another reference exists.

`encoding="utf-8"` is the right default for almost everything you'll write today, but if you're reading a file that genuinely is `cp1252` (an old Excel export, say), passing the wrong encoding gives you garbage *and* no error. Know your input, or use the `chardet` library to detect.

`split` with `maxsplit=1` is a middle ground between `split` and `partition` — it raises if the separator is missing, which can be useful when you want a hard error rather than a fallback.

## Related

- [How to clean and normalise text](clean-and-normalise-text.ipynb) — the right place to handle whitespace, case, and Unicode together.
- [How to parse structured strings](parse-structured-strings.ipynb) — `split` versus `partition` in context.
- [How to use string templates](use-string-templates.ipynb) — when to drop f-strings for `string.Template`.
- [String methods reference](../reference/string-methods-reference.md) — the full set of `str` methods with what each one returns.
