# Avoid common file-handling mistakes

**The question.** You're reviewing file-handling code and something smells — an `open()` without `with`, a missing `encoding`, a `'w'` where you meant `'a'`, a `readlines()` on a log that could be multi-gigabyte. You want the short list of traps and the fix for each.

The short list is below, then each trap in detail.

## The answer

## The answer

| Looks like… | Why it bites | Fix |
| --- | --- | --- |
| `f = open(...); f.read()` | file never closed if `read()` raises | `with open(...) as f:` |
| `open('data.txt', 'r')` — no encoding | default varies by platform; UnicodeDecodeError on Windows | always pass `encoding='utf-8'` |
| `open('log.txt', 'w')` when you meant append | truncates the file before writing | use `'a'` for append |
| `'data/' + 'reports/' + 'summary.txt'` | hard-coded separator breaks on Windows | `Path('data') / 'reports' / 'summary.txt'` |
| `open('config.txt')` with no fallback | `FileNotFoundError` crashes the caller | check `Path.exists()` or catch `FileNotFoundError` |
| `f.readlines()` on a log file | loads everything into memory | `for line in f:` iterates lazily |
| `csv.writer(f)` without `newline=''` | extra blank rows on Windows | always open with `newline=''` for CSVs |
| `open('config.txt')` from a script | resolves against CWD, not script dir | `Path(__file__).parent / 'config.txt'` |
| `open('img.png', 'r')` for binary | encoding and newline translation corrupt the file | binary mode: `'rb'` / `'wb'` |

Each in detail below.

## Why each one bites

### 1. Forgetting to close

```python
# Wrong — if f.read() raises, close never runs
f = open('data.txt', encoding='utf-8')
content = f.read()
f.close()

# Right — guaranteed close on exit, even via exception
with open('data.txt', encoding='utf-8') as f:
    content = f.read()
```

Open file handles are a finite resource on every OS. Leaked handles break long-running processes and (on Windows) prevent other programs from opening the file. `with` blocks guarantee cleanup.

### 2. Not specifying encoding

Without `encoding=...`, Python uses `locale.getencoding()` — usually UTF-8 on Linux/macOS but *cp1252* on Windows in an English locale. The same script then behaves differently across machines, and a file that reads fine locally blows up on a colleague's laptop. From Python 3.15 this will warn by default; you may as well start now.

```python
# Wrong
open('data.txt').read()

# Right
open('data.txt', encoding='utf-8').read()
```

### 3. Write mode vs. append

`'w'` truncates the file to zero before you write a single byte. If you meant to add to the end, you wanted `'a'`. Easy mistake on log files — one stray `'w'` and the whole history is gone.

### 4. String concatenation for paths

```python
# Wrong — breaks on Windows, awkward if 'data' already ends with /
path = 'data' + '/' + 'reports' + '/' + 'summary.txt'

# Right
from pathlib import Path
path = Path('data') / 'reports' / 'summary.txt'
```

`Path` handles separators and trailing-slash normalisation for you. The `/` operator reads naturally once you've used it a few times.

### 5. No fallback for a missing file

Either check first or catch the exception — but pick one deliberately.

```python
from pathlib import Path

# Option A — check first (fine when race conditions don't matter)
if Path('config.txt').exists():
    config = Path('config.txt').read_text(encoding='utf-8')
else:
    config = DEFAULTS

# Option B — EAFP (cleaner when you were going to read anyway)
try:
    config = Path('config.txt').read_text(encoding='utf-8')
except FileNotFoundError:
    config = DEFAULTS
```

### 6. `readlines()` on a large file

`f.readlines()` and `f.read()` both load the entire file. For a log of any size this is either slow (few MB) or fatal (multi-GB). `for line in f` iterates lazily — one line at a time, O(longest line) in memory.

### 7. CSVs without `newline=''`

CSV writers assume they control line termination. When the file object is also translating newlines, you get extra blank rows between data rows on Windows. `newline=''` disables Python's newline translation so the CSV module can produce output that's consistent across platforms.

### 8. Relative paths vs. script directory

`open('config.txt')` resolves against the *current working directory* — wherever the user ran the script from — which is almost never the directory containing your script. Build paths from `Path(__file__).parent` when the file lives next to the code.

### 9. Text mode for binary data

`open('image.png', 'r')` will either corrupt the image (via newline translation on Windows) or raise `UnicodeDecodeError` immediately. Any non-text file — image, audio, archive, custom binary format — wants `'rb'` or `'wb'`.

## When the pattern is fine

Some of these are genuine trade-offs, not absolutes. `f.read()` is fine for a file you know is small. `'w'` is correct when you *really do* want to overwrite. A bare `except` over an `open()` is fine if you immediately log and fall back.

The traps bite when the shortcut is applied reflexively to a case where the defaults don't match the intent — Windows when you tested only on Linux, a log file where you meant to append, a PNG that happened to start with UTF-8-safe bytes on your machine.

## Related reading

- [Process large files](process-large-files.ipynb) — the lazy-iteration pattern in detail.
- [Work with binary files](work-with-binary-files.ipynb) — `'rb'`/`'wb'` and `struct`.
- [Manage temporary files](manage-temporary-files.ipynb) — atomic-write and cleanup patterns.
- [pathlib quick reference](../reference/pathlib-quick-reference.md) — the `Path` API in one place.
- [File modes reference](../reference/file-modes-reference.md) — every mode combination and what it does.
