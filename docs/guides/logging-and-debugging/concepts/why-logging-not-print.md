# Why logging, not print

Most developers start their Python journey using `print()` to understand what their code is doing. It is simple, immediate, and works everywhere. So why would you bother learning a whole module just to write messages?

This article explores why the `logging` module is a better choice for diagnostic output in real-world applications, and when `print()` is still perfectly fine.

## The appeal of `print()`

There is a reason `print()` is every beginner's first debugging tool. It has genuine advantages:

- **Zero setup.** No imports, no configuration, no learning curve.
- **Immediate feedback.** You see the output right away.
- **Universal.** It works the same way in every Python environment.

For a quick script or a few lines in the REPL, `print()` is hard to beat. There is no shame in using it when it is the right tool for the job.

## Where `print()` falls short

The problems with `print()` emerge as your code grows beyond a single file or starts running in environments you do not directly observe.

### No severity levels

With `print()`, every message looks the same. There is no built-in way to distinguish a routine status update from an urgent error:

```python
print("Starting data processing")      # Is this important?
print("WARNING: 2 items were skipped")  # How important is this?
print("ERROR: Could not save results")  # How do I filter for just errors?
```

You end up inventing your own conventions, and they are never consistent.

### No filtering

Once a `print()` statement is in your code, it always produces output. The only way to silence it is to comment it out or delete it. If you want to see detailed output during development but not in production, you have to manually manage which print statements are active.

The `logging` module solves this with levels. Set the level to `WARNING` in production, and all your `DEBUG` and `INFO` messages silently disappear -- without touching the source code.

### No destinations

`print()` sends everything to standard output. If you want to save output to a file, send errors to a different destination, or forward messages to a monitoring system, you need to build all of that yourself.

With logging, you can attach multiple **handlers** to a single logger. One handler writes to the console, another writes to a file, and a third sends critical errors to an alerting service -- all from the same log statements.

### No context

A bare `print("Something happened")` tells you nothing about when, where, or at what severity it occurred. With logging, every message automatically includes metadata:

```
2026-02-09 14:30:05 - my_app.database - WARNING - Connection pool nearly full
```

Timestamp, module name, severity level, and message -- all without any extra effort from the developer.

### No lazy evaluation

When you write:

```python
print(f"Processing item {expensive_function(item)}")
```

The `expensive_function()` call happens every time, even if you have a flag that says "do not print debug messages." With logging and `%s` formatting:

```python
logger.debug("Processing item %s", expensive_function(item))
```

If `DEBUG` level is disabled, the function call still happens, but the string formatting does not. For truly lazy evaluation, the arguments are only processed if the message will be emitted.

## What the `logging` module offers

The `logging` module addresses every limitation of `print()`:

| Feature | `print()` | `logging` |
|---------|-----------|-----------|
| Severity levels | No | Five levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| Filtering | Manual | Automatic, based on level thresholds |
| Multiple destinations | No | Handlers for console, files, network, email, and more |
| Timestamps | Manual | Built-in with customisable format |
| Source identification | No | Logger names identify the module or component |
| Lazy formatting | No | `%s` style formatting is deferred |
| Thread safety | No | Built-in thread-safe operation |
| Disable without code changes | No | Change the log level in configuration |

## A practical comparison

Consider a function that downloads files from a list of URLs. Here is the `print()` approach:

```python
def download_files(urls: list[str]) -> list[str]:
    """Download files from a list of URLs."""
    print(f"Starting download of {len(urls)} files")
    results = []
    for url in urls:
        print(f"  Downloading: {url}")
        try:
            content = fetch(url)
            results.append(content)
            print(f"  Success: {len(content)} bytes")
        except ConnectionError:
            print(f"  FAILED: {url}")
    print(f"Downloaded {len(results)} of {len(urls)} files")
    return results
```

And here is the same function with logging:

```python
import logging

logger = logging.getLogger(__name__)


def download_files(urls: list[str]) -> list[str]:
    """Download files from a list of URLs."""
    logger.info("Starting download of %s files", len(urls))
    results = []
    for url in urls:
        logger.debug("Downloading: %s", url)
        try:
            content = fetch(url)
            results.append(content)
            logger.debug("Success: %s bytes", len(content))
        except ConnectionError:
            logger.error("Failed to download: %s", url)
    logger.info("Downloaded %s of %s files", len(results), len(urls))
    return results
```

The logging version looks almost the same, but it gives you:

- **Automatic filtering.** Set the level to `ERROR` in production and only failures are reported.
- **Source identification.** The `%(name)s` field shows which module produced each message.
- **Flexible output.** In development, messages go to the console. In production, they go to a file. The function code does not change.

## When `print()` is fine

Not everything needs logging. `print()` is the right choice when:

- **You are writing a quick script** that will run once and be discarded
- **You are exploring in the REPL** or a Jupyter notebook
- **The output is for the user**, not for the developer. Program output (results, reports, formatted data) belongs in `print()`, not in logging.
- **You are debugging a tiny, self-contained issue** and will remove the print statement immediately

The key distinction is this: **`print()` is for program output. `logging` is for diagnostic output.** If a message exists to help a developer understand what the program is doing, it belongs in a log. If it exists to show a result to the user, it belongs in `print()`.

## The real-world difference

In a production environment, the difference between `print()` and `logging` becomes stark:

- **Log rotation.** Log files are automatically rotated when they reach a certain size, preventing disk space issues.
- **Remote collection.** Log messages can be forwarded to centralised logging systems for analysis.
- **Level-based alerting.** Operations teams can set up alerts that trigger only on `ERROR` or `CRITICAL` messages.
- **Structured analysis.** With consistent formatting, log messages can be parsed, searched, and analysed programmatically.
- **Zero-cost disabling.** `DEBUG` messages have virtually no performance impact in production when the level is set higher.

None of this is possible with `print()` without building significant infrastructure around it -- infrastructure that the `logging` module already provides.

## Making the switch

Transitioning from `print()` to `logging` is straightforward:

1. **Import logging** and create a logger at the top of each module:

   ```python
   import logging
   logger = logging.getLogger(__name__)
   ```

2. **Replace `print()` calls** with the appropriate log level:

   - `print("Starting...")` becomes `logger.info("Starting...")`
   - `print("WARNING: ...")` becomes `logger.warning("...")`
   - `print(f"DEBUG: {value}")` becomes `logger.debug("Value: %s", value)`

3. **Configure logging once** in your application entry point:

   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

4. **Keep `print()`** for actual program output that users should see.

The change is small, but the benefits are significant -- and they grow as your project grows.
