# `logging` module quick reference

A comprehensive quick reference for the `logging` module in Python, covering core functions, classes, and configuration options.

## Log levels

| Level | Numeric value | When to use |
|-------|--------------|-------------|
| `logging.DEBUG` | 10 | Detailed diagnostic information for developers |
| `logging.INFO` | 20 | Confirmation that things are working as expected |
| `logging.WARNING` | 30 | Something unexpected happened, but the program still works |
| `logging.ERROR` | 40 | A specific operation failed |
| `logging.CRITICAL` | 50 | The program itself may not be able to continue |

## Module-level convenience functions

These functions log to the root logger. For most applications, use a named logger instead.

### `logging.basicConfig(**kwargs)`

Configure the root logger with a handler, formatter, and level.

```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    filename="app.log",       # Optional: log to a file
    filemode="a",             # Optional: append mode (default)
)
```

**Key parameters:**

| Parameter | Description |
|-----------|-------------|
| `level` | Root logger level (for example, `logging.DEBUG`) |
| `format` | Format string for log messages |
| `datefmt` | Date format string for `%(asctime)s` |
| `filename` | Write to this file instead of the console |
| `filemode` | File mode (`"a"` for append, `"w"` for overwrite) |
| `handlers` | A list of handler instances to attach to the root logger |

**Note:** `basicConfig()` only takes effect the first time it is called. Subsequent calls have no effect unless you pass `force=True` (Python 3.8+).

### `logging.getLogger(name=None)`

Return a logger with the specified name, or the root logger if no name is given.

```python
logger = logging.getLogger("my_module")
logger = logging.getLogger(__name__)  # Recommended convention
```

Calling `getLogger()` with the same name always returns the same logger instance.

### `logging.debug(msg, *args, **kwargs)`

Log a message at `DEBUG` level on the root logger. The same pattern applies to `logging.info()`, `logging.warning()`, `logging.error()`, and `logging.critical()`.

```python
logging.warning("Disk usage at %s%%", 85)
```

## `Logger` class

### Key methods

| Method | Description |
|--------|-------------|
| `logger.setLevel(level)` | Set the minimum log level for this logger |
| `logger.addHandler(handler)` | Add a handler to this logger |
| `logger.removeHandler(handler)` | Remove a handler from this logger |
| `logger.addFilter(filter)` | Add a filter to this logger |
| `logger.debug(msg, *args, **kwargs)` | Log at `DEBUG` level |
| `logger.info(msg, *args, **kwargs)` | Log at `INFO` level |
| `logger.warning(msg, *args, **kwargs)` | Log at `WARNING` level |
| `logger.error(msg, *args, **kwargs)` | Log at `ERROR` level |
| `logger.critical(msg, *args, **kwargs)` | Log at `CRITICAL` level |
| `logger.exception(msg, *args, **kwargs)` | Log at `ERROR` level with exception info |
| `logger.log(level, msg, *args, **kwargs)` | Log at a specific numeric level |

### `logger.exception()`

Log at `ERROR` level and automatically include exception information. Use only inside an `except` block.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Division failed")
```

## Handler classes

### `logging.StreamHandler(stream=None)`

Send log output to a stream (defaults to `sys.stderr`).

```python
handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### `logging.FileHandler(filename, mode="a", encoding=None)`

Write log output to a file.

```python
handler = logging.FileHandler("app.log", encoding="utf-8")
```

| Parameter | Description |
|-----------|-------------|
| `filename` | Path to the log file |
| `mode` | File mode (`"a"` for append, `"w"` for overwrite) |
| `encoding` | File encoding (recommended: `"utf-8"`) |

### `logging.handlers.RotatingFileHandler(filename, maxBytes=0, backupCount=0)`

Rotate log files when they reach a specified size.

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=5_000_000,  # 5 MB
    backupCount=5,
)
```

### `logging.handlers.TimedRotatingFileHandler(filename, when="h", interval=1, backupCount=0)`

Rotate log files at timed intervals.

```python
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler(
    "app.log",
    when="midnight",
    backupCount=7,
)
```

| `when` value | Interval |
|-------------|----------|
| `"S"` | Every second |
| `"M"` | Every minute |
| `"H"` | Every hour |
| `"D"` | Every day |
| `"midnight"` | At midnight |

### `logging.NullHandler()`

A do-nothing handler. Libraries should add this to prevent "No handlers could be found" warnings.

```python
logging.getLogger("my_library").addHandler(logging.NullHandler())
```

## `Formatter` class

### `logging.Formatter(fmt=None, datefmt=None, style="%")`

Create a formatter for log messages.

```python
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
handler.setFormatter(formatter)
```

See the [Log format reference](log-format-reference.md) for a complete list of format attributes.

## `Filter` class

### `logging.Filter(name="")`

Filter log records based on the logger name. Only records from the named logger (and its children) pass through.

```python
# Only allow records from "my_app.database" and its children
filter = logging.Filter("my_app.database")
handler.addFilter(filter)
```

For custom filtering logic, subclass `logging.Filter` and override the `filter()` method.

## Dictionary-based configuration

### `logging.config.dictConfig(config)`

Configure logging using a dictionary. This is the recommended approach for complex configurations.

```python
import logging.config

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}

logging.config.dictConfig(config)
```

## Quick setup recipes

### Minimal console logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Console logging with custom format

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
```

### File and console logging

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
```

## Further reading

- [Python `logging` module documentation](https://docs.python.org/3/library/logging.html)
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
