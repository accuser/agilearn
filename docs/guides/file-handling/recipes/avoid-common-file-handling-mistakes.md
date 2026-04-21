# Avoid common file handling mistakes

File handling is one of the most practical skills in Python, but several common mistakes can lead to bugs, data loss, or code that behaves differently across platforms. This guide covers the most frequent pitfalls and how to avoid them.

## Mistake 1: forgetting to close files

**Problem:** opening a file without ensuring it is closed.

```python
# Problem: file may stay open if an error occurs
f = open("data.txt", "r", encoding="utf-8")
content = f.read()
# f.close() is never called if an error occurs above
```

**Solution:** use a `with` statement.

```python
# Solution: file is automatically closed
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

Open files consume system resources, data may not be flushed to disc, and other programs may not be able to access the file. The `with` statement guarantees the file is closed, even if an error occurs.

## Mistake 2: not specifying encoding

**Problem:** relying on the platform default encoding.

```python
# Problem: uses platform-dependent default encoding
with open("data.txt", "r") as f:
    content = f.read()
```

**Solution:** always specify encoding explicitly.

```python
# Solution: consistent behaviour across platforms
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

Without explicit encoding, Python uses the system default, which varies between operating systems. This can lead to `UnicodeDecodeError` or garbled text when your code runs on a different platform.

## Mistake 3: using `"w"` mode when you mean `"a"`

**Problem:** accidentally overwriting an entire file.

```python
# Problem: overwrites the entire file!
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("New log entry\n")
```

**Solution:** use append mode.

```python
# Solution: adds to the end of the file
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")
```

Write mode `"w"` truncates the file to zero length before writing. If you want to add to an existing file, use `"a"` mode instead.

## Mistake 4: using string concatenation for paths

**Problem:** hard-coding path separators.

```python
# Problem: platform-dependent separator
path = "data" + "/" + "reports" + "/" + "summary.txt"
```

**Solution:** use `pathlib.Path`.

```python
from pathlib import Path

# Solution: platform-independent paths
path = Path("data") / "reports" / "summary.txt"
```

Hard-coded path separators break on different operating systems. The `pathlib` module handles separators automatically.

## Mistake 5: not handling `FileNotFoundError`

**Problem:** assuming the file always exists.

```python
# Problem: crashes if file does not exist
with open("config.txt", "r", encoding="utf-8") as f:
    config = f.read()
```

**Solution:** check first or handle the exception.

```python
from pathlib import Path

# Option 1: check before reading
config_path = Path("config.txt")
if config_path.exists():
    config = config_path.read_text(encoding="utf-8")
else:
    config = "default settings"

# Option 2: handle the exception
try:
    with open("config.txt", "r", encoding="utf-8") as f:
        config = f.read()
except FileNotFoundError:
    config = "default settings"
```

Always consider what happens if the file does not exist. Either check with `Path.exists()` or handle the `FileNotFoundError` exception.

## Mistake 6: reading entire large files into memory

**Problem:** loading a very large file all at once.

```python
# Problem: loads entire file into memory
with open("huge-file.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()  # could be gigabytes!
```

**Solution:** iterate line by line.

```python
# Solution: constant memory usage
with open("huge-file.txt", "r", encoding="utf-8") as f:
    for line in f:
        process(line)
```

The `readlines()` and `read()` methods load the entire file into memory. For large files, iterate line by line to keep memory usage constant.

## Mistake 7: forgetting `newline=""` for CSV files

**Problem:** extra blank lines in CSV output.

```python
import csv

# Problem: may produce extra blank lines on Windows
with open("data.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
```

**Solution:** always use `newline=""`.

```python
import csv

# Solution: correct newline handling
with open("data.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
```

Without `newline=""`, Python may double up newlines when writing CSV files, resulting in blank rows between data rows.

## Mistake 8: assuming the current working directory

**Problem:** using relative paths that depend on where the script is run from.

```python
# Problem: depends on where the script is run from
with open("config.txt", "r", encoding="utf-8") as f:
    config = f.read()
```

**Solution:** use a path relative to the script location.

```python
from pathlib import Path

# Solution: path relative to the script file
script_dir = Path(__file__).parent
config_path = script_dir / "config.txt"
with config_path.open("r", encoding="utf-8") as f:
    config = f.read()
```

Relative paths are resolved from the current working directory, which may not be the directory containing your script. Use `Path(__file__).parent` to get the directory of the current script.

## Quick reference table

| Mistake | Solution |
|---------|----------|
| Forgetting to close files | Use `with` statements |
| Not specifying encoding | Always use `encoding="utf-8"` |
| Using `"w"` instead of `"a"` | Check the mode before writing |
| String concatenation for paths | Use `pathlib.Path` with the `/` operator |
| Not handling missing files | Use `Path.exists()` or `try`/`except` |
| Loading large files into memory | Iterate line by line |
| Missing `newline=""` for CSV | Always use `newline=""` with CSV files |
| Assuming working directory | Use `Path(__file__).parent` |

## See also

- [Why context managers matter](../concepts/why-context-managers-matter.md)
- [Understanding file encodings](../concepts/understanding-file-encodings.md)
- [File modes reference](../reference/file-modes-reference.md)
