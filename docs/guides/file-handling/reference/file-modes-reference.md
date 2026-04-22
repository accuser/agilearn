# File modes reference

When opening files in Python, the mode parameter determines how the file is opened and what operations are available. This reference covers all file modes and their combinations.

## Mode overview

| Mode | Access | Creates file | Truncates | Position | Description |
|------|--------|--------------|-----------|----------|-------------|
| `"r"` | Read only | No | No | Start | Open for reading (default) |
| `"w"` | Write only | Yes | Yes | Start | Open for writing (creates or truncates) |
| `"a"` | Write only | Yes | No | End | Open for appending |
| `"x"` | Write only | Yes (error if exists) | No | Start | Exclusive creation |
| `"r+"` | Read + Write | No | No | Start | Open for reading and writing |
| `"w+"` | Read + Write | Yes | Yes | Start | Open for writing and reading |
| `"a+"` | Read + Write | Yes | No | End | Open for appending and reading |
| `"rb"` | Read only (binary) | No | No | Start | Read binary data |
| `"wb"` | Write only (binary) | Yes | Yes | Start | Write binary data |
| `"ab"` | Append only (binary) | Yes | No | End | Append binary data |
| `"xb"` | Write only (binary) | Yes (error if exists) | No | Start | Exclusive creation (binary) |
| `"r+b"` | Read + Write (binary) | No | No | Start | Read and write binary data |
| `"w+b"` | Read + Write (binary) | Yes | Yes | Start | Write and read binary data |
| `"a+b"` | Read + Write (binary) | Yes | No | End | Append and read binary data |

## Mode characters

### Access modes

- `"r"` -- **Read.** The file must exist. This is the default mode.
- `"w"` -- **Write.** Creates the file if it does not exist. **Truncates (empties) the file if it already exists.**
- `"a"` -- **Append.** Creates the file if it does not exist. Writes are always added to the end of the file.
- `"x"` -- **Exclusive creation.** Creates a new file. Raises `FileExistsError` if the file already exists.

### Modifier characters

- `"b"` -- **Binary mode.** Data is read and written as `bytes` objects. Do not specify `encoding` in binary mode.
- `"t"` -- **Text mode** (default). Data is read and written as `str` objects. Specify `encoding` for consistent behaviour.
- `"+"` -- **Update mode.** Opens the file for both reading and writing.

## Detailed mode descriptions

### Read mode (`"r"`)

**When to use:** reading existing text files.

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

- The file must already exist -- `FileNotFoundError` is raised otherwise
- The file position starts at the beginning
- Only read operations are available

### Write mode (`"w"`)

**When to use:** creating a new file or replacing the contents of an existing file.

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("New content\n")
```

- Creates the file if it does not exist
- **Truncates the file if it already exists** -- all existing content is deleted
- The file position starts at the beginning
- Only write operations are available

!!! warning

    Write mode deletes all existing content. If you want to add to a file, use append mode (`"a"`) instead.

### Append mode (`"a"`)

**When to use:** adding content to the end of an existing file, or creating a new file if it does not exist.

```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")
```

- Creates the file if it does not exist
- Does not truncate the file
- The file position starts at the end
- All writes go to the end of the file, regardless of calls to `seek()`

### Exclusive creation mode (`"x"`)

**When to use:** creating a new file safely, ensuring you do not accidentally overwrite an existing file.

```python
try:
    with open("output.txt", "x", encoding="utf-8") as f:
        f.write("Safely created\n")
except FileExistsError:
    print("File already exists.")
```

- Creates a new file
- Raises `FileExistsError` if the file already exists
- Only write operations are available

### Read-write mode (`"r+"`)

**When to use:** reading and modifying an existing file.

```python
with open("data.txt", "r+", encoding="utf-8") as f:
    content = f.read()
    f.seek(0)
    f.write("Modified content\n")
```

- The file must already exist
- The file position starts at the beginning
- Both read and write operations are available
- Does not truncate the file

### Write-read mode (`"w+"`)

**When to use:** creating a new file (or replacing an existing one) that you want to both write to and read from.

```python
with open("data.txt", "w+", encoding="utf-8") as f:
    f.write("Hello\n")
    f.seek(0)
    content = f.read()
```

- Creates the file if it does not exist
- **Truncates the file if it already exists**
- Both read and write operations are available

### Append-read mode (`"a+"`)

**When to use:** appending to a file while also being able to read its contents.

```python
with open("log.txt", "a+", encoding="utf-8") as f:
    f.write("New entry\n")
    f.seek(0)
    content = f.read()
```

- Creates the file if it does not exist
- Does not truncate the file
- The file position starts at the end
- Both read and write operations are available

### Binary read mode (`"rb"`)

**When to use:** reading non-text files such as images, PDFs, or compressed archives.

```python
with open("image.png", "rb") as f:
    data = f.read()
```

- Works with `bytes` objects, not strings
- Do not specify `encoding`
- No newline translation

### Binary write mode (`"wb"`)

**When to use:** writing non-text data.

```python
with open("output.bin", "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n")
```

- Works with `bytes` objects
- Creates the file if it does not exist
- Truncates the file if it already exists

## Text mode versus binary mode

| Feature | Text mode | Binary mode |
|---------|-----------|-------------|
| Data type | `str` | `bytes` |
| Encoding | Specified (for example, `"utf-8"`) | Not applicable |
| Newline translation | Yes (platform-dependent) | No |
| Use for | Text files (`.txt`, `.csv`, `.json`, `.xml`) | Images, PDFs, audio, compressed archives |

## Newline handling

In text mode, Python handles newlines differently depending on the platform:

- **Reading:** platform-specific line endings (such as `\r\n` on Windows) are translated to `\n`
- **Writing:** `\n` is translated to the platform-specific line ending

The `newline` parameter in `open()` controls this behaviour:

| Value | Reading behaviour | Writing behaviour |
|-------|-------------------|-------------------|
| `None` (default) | Universal newline mode &ndash; all line endings become `\n` | `\n` is translated to the platform default |
| `""` | No translation &ndash; all line endings are returned as-is | No translation -- `\n` is written as-is |
| `"\n"` | Only `\n` is recognised as a line ending | No translation |
| `"\r\n"` | Only `\r\n` is recognised as a line ending | `\n` is written as `\r\n` |

For CSV files, always use `newline=""` to prevent double newlines.

## Decision guide

| Task | Recommended mode |
|------|-----------------|
| Read a text file | `"r"` |
| Write a new text file (or replace existing) | `"w"` |
| Add to the end of a text file | `"a"` |
| Create a new file safely (no overwrite) | `"x"` |
| Read and modify a text file | `"r+"` |
| Read an image, PDF, or binary file | `"rb"` |
| Write binary data | `"wb"` |
| Read a CSV file | `"r"` with `newline=""` |
| Write a CSV file | `"w"` with `newline=""` |

## See also

- [`open()` function reference](open-function-reference.md)
- [`pathlib` quick reference](pathlib-quick-reference.md)
- [Official Python documentation for `open()`](https://docs.python.org/3/library/functions.html#open)
