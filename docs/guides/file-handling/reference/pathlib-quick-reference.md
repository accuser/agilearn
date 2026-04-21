# `pathlib` quick reference

The `pathlib` module provides an object-oriented interface for working with file system paths. This reference covers the most commonly used methods and properties of `pathlib.Path`.

## Creating `Path` objects

```python
from pathlib import Path

p = Path("file.txt")                        # From a string
p = Path("directory") / "file.txt"          # Using the / operator
p = Path.home()                              # Home directory
p = Path.cwd()                               # Current working directory
p = Path.home() / "Documents" / "file.txt"  # Combined
```

## Path properties

Using the example path `Path("documents/reports/annual.tar.gz")`:

| Property | Description | Example result |
|----------|-------------|----------------|
| `name` | Final component (file name with extension) | `"annual.tar.gz"` |
| `stem` | File name without the last extension | `"annual.tar"` |
| `suffix` | Last file extension (including the dot) | `".gz"` |
| `suffixes` | List of all extensions | `[".tar", ".gz"]` |
| `parent` | Logical parent directory | `Path("documents/reports")` |
| `parents` | Immutable sequence of all parent paths | (iterable) |
| `parts` | Tuple of path components | `("documents", "reports", "annual.tar.gz")` |
| `anchor` | Drive and root combined | `""` (relative path) |

## Querying methods

These methods check the status of a path on the file system.

| Method | Description | Return type |
|--------|-------------|-------------|
| `exists()` | Check whether the path exists | `bool` |
| `is_file()` | Check whether the path is a regular file | `bool` |
| `is_dir()` | Check whether the path is a directory | `bool` |
| `is_symlink()` | Check whether the path is a symbolic link | `bool` |
| `is_absolute()` | Check whether the path is absolute | `bool` |
| `stat()` | Return file status (size, timestamps, and so on) | `os.stat_result` |
| `resolve()` | Make the path absolute, resolving symbolic links | `Path` |
| `samefile(other)` | Check whether two paths refer to the same file | `bool` |

```python
from pathlib import Path

path = Path("example.txt")
path.write_text("Hello", encoding="utf-8")

print(path.exists())       # True
print(path.is_file())      # True
print(path.is_dir())       # False
print(path.stat().st_size) # 5
print(path.resolve())      # /absolute/path/to/example.txt
```

## Reading and writing methods

| Method | Description |
|--------|-------------|
| `read_text(encoding=None)` | Read the file contents as a string |
| `read_bytes()` | Read the file contents as bytes |
| `write_text(data, encoding=None)` | Write a string to the file (overwrites) |
| `write_bytes(data)` | Write bytes to the file (overwrites) |
| `open(mode="r", encoding=None)` | Open the file (like the built-in `open()`) |

```python
from pathlib import Path

# Simple read and write
Path("file.txt").write_text("Hello, world!", encoding="utf-8")
content = Path("file.txt").read_text(encoding="utf-8")

# Using open() for more control
with Path("file.txt").open("r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

## Directory operations

| Method | Description |
|--------|-------------|
| `iterdir()` | Iterate over the contents of the directory |
| `glob(pattern)` | Glob the given pattern in the directory |
| `rglob(pattern)` | Recursive glob (searches subdirectories) |
| `mkdir(parents=False, exist_ok=False)` | Create the directory |
| `rmdir()` | Remove an empty directory |

```python
from pathlib import Path

# Create directories
Path("project/src").mkdir(parents=True, exist_ok=True)

# List contents
for item in Path("project").iterdir():
    print(item)

# Find files by pattern
for py_file in Path("project").rglob("*.py"):
    print(py_file)
```

## File operations

| Method | Description |
|--------|-------------|
| `rename(target)` | Rename the file or directory to `target` |
| `replace(target)` | Rename, overwriting `target` if it exists |
| `unlink(missing_ok=False)` | Remove the file |
| `touch(exist_ok=True)` | Create the file or update its modification time |
| `chmod(mode)` | Change the file permissions |

## Path manipulation methods

| Method | Description | Example |
|--------|-------------|---------|
| `joinpath(*args)` | Combine path components | `Path("a").joinpath("b", "c")` |
| `with_name(name)` | Return a path with the name changed | `Path("a/b.txt").with_name("c.txt")` → `a/c.txt` |
| `with_stem(stem)` | Return a path with the stem changed | `Path("a/b.txt").with_stem("c")` → `a/c.txt` |
| `with_suffix(suffix)` | Return a path with the suffix changed | `Path("a/b.txt").with_suffix(".md")` → `a/b.md` |
| `relative_to(other)` | Compute a relative path | `Path("/a/b/c").relative_to("/a")` → `b/c` |
| `match(pattern)` | Match against a glob pattern | `Path("data.csv").match("*.csv")` → `True` |

```python
from pathlib import Path

p = Path("documents/report.txt")
print(p.with_suffix(".md"))      # documents/report.md
print(p.with_name("notes.txt"))  # documents/notes.txt
print(p.with_stem("summary"))    # documents/summary.txt
```

## The `/` operator

`Path` objects support the `/` operator for joining path components. This is equivalent to `joinpath()` but more readable.

```python
from pathlib import Path

base = Path("home")
full = base / "user" / "documents" / "file.txt"
# Result: home/user/documents/file.txt
```

## `PurePath` versus `Path`

The `pathlib` module provides two types of path classes:

- **`PurePath`** -- provides path manipulation without any I/O operations. Use `PurePosixPath` or `PureWindowsPath` to work with paths for a specific operating system without needing to be on that system.
- **`Path`** -- inherits from `PurePath` and adds I/O operations (`exists()`, `read_text()`, `mkdir()`, and so on). This is the class you will use most often.

## Common patterns

### Find all Python files recursively

```python
from pathlib import Path

for py_file in Path(".").rglob("*.py"):
    print(py_file)
```

### Get the size of a file

```python
from pathlib import Path

size = Path("data.txt").stat().st_size
print(f"File size: {size} bytes")
```

### Check whether a directory is empty

```python
from pathlib import Path

is_empty = not any(Path("my-directory").iterdir())
```

### Create a directory tree

```python
from pathlib import Path

Path("project/src/utils").mkdir(parents=True, exist_ok=True)
```

### Get the home directory

```python
from pathlib import Path

home = Path.home()
config = home / ".config" / "myapp" / "settings.json"
```

## See also

- [`open()` function reference](open-function-reference.md)
- [File modes reference](file-modes-reference.md)
- [Official `pathlib` documentation](https://docs.python.org/3/library/pathlib.html)
