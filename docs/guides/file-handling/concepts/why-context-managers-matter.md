# Why context managers matter

## The problem: resource management

When you open a file, you are borrowing a resource from the operating system. Every operating system limits the number of files a process can have open simultaneously. If you do not close files properly, you risk running out of file descriptors, causing data corruption, or preventing other programs from accessing the file.

Think of it like borrowing a book from a library. If you forget to return it, other people cannot read it, and eventually the library runs out of copies to lend. The operating system is the library, and open files are the borrowed books.

## Life before context managers

Before the `with` statement was introduced in Python 2.5, file handling looked like this:

```python
f = open("data.txt", "r", encoding="utf-8")
content = f.read()
f.close()
```

This approach has several problems:

1. **It is easy to forget `close()`.** In a long function with multiple return paths, you might miss one.
2. **Errors leave files open.** If an exception occurs between `open()` and `close()`, the file is never closed.
3. **Error handling is verbose.** Writing correct code requires a try/finally block.

The try/finally pattern solves the safety problem but is cumbersome:

```python
f = open("data.txt", "r", encoding="utf-8")
try:
    content = f.read()
finally:
    f.close()
```

This works, but it is verbose and easy to get wrong. You have to remember to put every file operation inside a try block, and you must close the file in the finally block.

## The `with` statement: a better approach

The `with` statement provides a cleaner, safer way to manage resources:

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
# File is automatically closed here
```

This is better for several reasons:

- The file is guaranteed to be closed, even if an error occurs inside the block
- The code is cleaner and more readable
- You cannot accidentally forget to close the file
- It communicates intent clearly: "I am working with this resource temporarily"

## What happens behind the scenes

The `with` statement uses the **context manager protocol**, which is defined by two special methods:

1. When Python enters the `with` block, it calls `__enter__()` on the object returned by `open()`. The return value is assigned to the variable after `as`.
2. When the `with` block ends -- whether normally or because of an exception -- Python calls `__exit__()`. For file objects, this method closes the file.

Here is a simplified mental model of what the `with` statement does:

```python
# This is what Python does (conceptually)
manager = open("data.txt", "r", encoding="utf-8")
f = manager.__enter__()
try:
    content = f.read()
finally:
    manager.__exit__(None, None, None)
```

You never need to write this yourself -- the `with` statement handles it all automatically.

## When exceptions strike

Consider what happens when an exception occurs inside a `with` block:

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
    result = int(content)  # This might raise ValueError
```

If `int(content)` raises a `ValueError`, here is what happens:

1. The exception is raised
2. Python calls `__exit__()` on the file object, which closes the file
3. The exception propagates up the call stack as normal

Your file is always cleaned up, no matter what goes wrong inside the block. This is the key advantage of context managers.

## Beyond files: where context managers appear

Context managers are not limited to file handling. They are a general pattern for resource management in Python. You will encounter them in many places:

- **Database connections** -- automatically committed or rolled back
- **Network sockets** -- automatically closed
- **Locks and threading** -- automatically released
- **Temporary directories** -- automatically deleted with `tempfile.TemporaryDirectory()`
- **Mocking in tests** -- automatically restored after the test

This consistency is one of the strengths of the pattern. Once you understand how `with` works for files, you understand how it works everywhere.

## The cost of forgetting

What can go wrong if you do not close files properly?

- **Data loss.** When you write to a file, the data may be buffered in memory. If you do not close the file (or flush the buffer), the buffered data may never be written to disc.
- **File locks.** On some operating systems, an open file may be locked, preventing other processes from reading or writing it.
- **Resource exhaustion.** Every open file consumes a file descriptor. If you open enough files without closing them, the operating system will refuse to open more.
- **Corrupted files.** If your program crashes while a file is open for writing, the file may contain only partial data.

## Common misconceptions

**"The garbage collector will close my files."** It might, eventually. When a file object is garbage collected, Python will attempt to close it. However, the timing of garbage collection is unpredictable. In CPython (the standard implementation), objects are usually collected quickly when their reference count drops to zero. But in other implementations (such as PyPy), garbage collection works differently, and files may stay open much longer. You should not rely on this behaviour.

**"I only have one file open, so it does not matter."** Even with a single file, failing to close it properly can cause data loss. Write operations may be buffered, and the buffer is only flushed when the file is closed (or when you call `flush()` explicitly).

**"I can just call `.close()` manually."** You can, but the `with` statement is safer. Manual `close()` calls can be skipped by early returns, exceptions, or simple forgetfulness. The `with` statement removes this entire class of bugs.

## Summary

Context managers, used through the `with` statement, are one of the best features of Python for writing robust, correct file handling code. They solve a real problem -- resource management -- in an elegant and readable way. By using `with` for every file operation, you ensure that files are always closed properly, data is always flushed, and your code communicates its intent clearly.

The rule is simple: if you are opening a file, use a `with` statement.

## See also

- [Tutorials: Reading files](../learn/01-reading-files.ipynb)
- [`open()` function reference](../reference/open-function-reference.md)
- [Official Python documentation on context managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
