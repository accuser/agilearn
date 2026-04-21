# `open()` function reference

The built-in `open()` function is the primary way to open files in Python. This reference covers all parameters, return values, and common usage patterns.

## Function signature

```python
open(file, mode='r', buffering=-1, encoding=None, errors=None,
     newline=None, closefd=True, opener=None)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file` | `str` or path-like | (required) | The file path to open |
| `mode` | `str` | `'r'` | The file mode (see [File modes reference](file-modes-reference.md)) |
| `buffering` | `int` | `-1` | Buffering policy: 0 = unbuffered, 1 = line buffered, >1 = buffer size in bytes |
| `encoding` | `str` or `None` | `None` | The encoding for text mode (always specify `"utf-8"` explicitly) |
| `errors` | `str` or `None` | `None` | How encoding and decoding errors are handled |
| `newline` | `str` or `None` | `None` | How newlines are handled (use `""` for CSV files) |
| `closefd` | `bool` | `True` | Whether to close the file descriptor when the file object is closed |
| `opener` | callable or `None` | `None` | A custom opener function |

## Return value

The `open()` function returns a file object. The type depends on the mode:

| Mode | Return type |
|------|-------------|
| Text mode (`"r"`, `"w"`, `"a"`) | `io.TextIOWrapper` |
| Buffered binary (`"rb"`, `"wb"`) | `io.BufferedReader`, `io.BufferedWriter`, or `io.BufferedRandom` |
| Unbuffered binary (`buffering=0`) | `io.FileIO` |

## File modes

| Mode | Description | Creates file | Truncates | Position |
|------|-------------|--------------|-----------|----------|
| `"r"` | Read (text) | No | No | Start |
| `"w"` | Write (text) | Yes | Yes | Start |
| `"a"` | Append (text) | Yes | No | End |
| `"x"` | Exclusive creation (text) | Yes (fails if exists) | No | Start |
| `"rb"` | Read (binary) | No | No | Start |
| `"wb"` | Write (binary) | Yes | Yes | Start |
| `"ab"` | Append (binary) | Yes | No | End |
| `"r+"` | Read and write | No | No | Start |
| `"w+"` | Write and read | Yes | Yes | Start |
| `"a+"` | Append and read | Yes | No | End |

For a detailed explanation of each mode, see the [File modes reference](file-modes-reference.md).

## Error handling strategies

The `errors` parameter controls how encoding and decoding errors are handled.

| Strategy | Description |
|----------|-------------|
| `"strict"` | Raise `UnicodeDecodeError` or `UnicodeEncodeError` (default) |
| `"ignore"` | Silently skip characters that cannot be decoded or encoded |
| `"replace"` | Replace unencodable characters with `?` (encoding) or `\ufffd` (decoding) |
| `"backslashreplace"` | Replace with Python backslash escape sequences |
| `"xmlcharrefreplace"` | Replace with XML character references (encoding only) |

## Common usage patterns

### Reading a text file

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### Writing a text file

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, world!\n")
```

### Appending to a file

```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")
```

### Reading a binary file

```python
with open("image.png", "rb") as f:
    data = f.read()
```

### Reading line by line

```python
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

### Safe file creation

```python
try:
    with open("output.txt", "x", encoding="utf-8") as f:
        f.write("New content\n")
except FileExistsError:
    print("File already exists.")
```

## File object methods

| Method | Description | Applicable modes |
|--------|-------------|-----------------|
| `read(size=-1)` | Read up to `size` characters (or bytes). Read all if `size` is -1. | Read modes |
| `readline()` | Read a single line | Read modes |
| `readlines()` | Read all lines as a list | Read modes |
| `write(s)` | Write a string (or bytes) to the file | Write and append modes |
| `writelines(lines)` | Write a list of strings (does not add newlines) | Write and append modes |
| `seek(offset, whence=0)` | Move to a position in the file | All modes (behaviour varies) |
| `tell()` | Return the current position in the file | All modes |
| `close()` | Close the file | All modes |
| `flush()` | Flush the write buffer | Write and append modes |
| `readable()` | Return `True` if the file is readable | All modes |
| `writable()` | Return `True` if the file is writable | All modes |
| `seekable()` | Return `True` if the file supports seeking | All modes |
| `truncate(size=None)` | Truncate the file to `size` bytes | Write modes |

## Common exceptions

| Exception | When raised |
|-----------|-------------|
| `FileNotFoundError` | The file does not exist (read mode) |
| `FileExistsError` | The file already exists (exclusive creation mode `"x"`) |
| `PermissionError` | Insufficient permissions to open the file |
| `IsADirectoryError` | The path is a directory, not a file |
| `UnicodeDecodeError` | Content cannot be decoded with the specified encoding |
| `UnicodeEncodeError` | Content cannot be encoded with the specified encoding |
| `ValueError` | Invalid mode string or operation on a closed file |

## Best practices

- Always use `with` statements for automatic file closing
- Always specify `encoding="utf-8"` for text files
- Use `"rb"` or `"wb"` for binary files (images, PDFs, and so on)
- Use `newline=""` when opening CSV files
- Prefer `pathlib.Path.open()` over the built-in `open()` when using `pathlib`
- Handle `FileNotFoundError` when the file may not exist

## See also

- [File modes reference](file-modes-reference.md)
- [`pathlib` quick reference](pathlib-quick-reference.md)
- [Official Python documentation for `open()`](https://docs.python.org/3/library/functions.html#open)
