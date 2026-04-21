# Log format reference

A complete reference for format string attributes used with `logging.Formatter` in the `logging` module.

## Format string syntax

Format strings use `%(name)s` style placeholders, where `name` is an attribute of the `logging.LogRecord` object. The letter after the closing parenthesis specifies the type (`s` for string, `d` for integer, `f` for float).

```python
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
```

## `LogRecord` attributes

The following table lists all standard attributes available in format strings.

| Attribute | Format | Description | Example output |
|-----------|--------|-------------|----------------|
| `asctime` | `%(asctime)s` | Human-readable timestamp | `2026-02-09 14:30:00,123` |
| `created` | `%(created)f` | Time as a Unix timestamp (seconds since epoch) | `1707489000.123456` |
| `filename` | `%(filename)s` | Name of the source file | `my_module.py` |
| `funcName` | `%(funcName)s` | Name of the function that logged the message | `process_data` |
| `levelname` | `%(levelname)s` | Text name of the log level | `WARNING` |
| `levelno` | `%(levelno)d` | Numeric value of the log level | `30` |
| `lineno` | `%(lineno)d` | Line number in the source file | `42` |
| `message` | `%(message)s` | The formatted log message | `Disk usage at 85%` |
| `module` | `%(module)s` | Module name (filename without extension) | `my_module` |
| `msecs` | `%(msecs)d` | Millisecond portion of the timestamp | `123` |
| `name` | `%(name)s` | Name of the logger | `my_app.database` |
| `pathname` | `%(pathname)s` | Full path of the source file | `/home/user/app/my_module.py` |
| `process` | `%(process)d` | Process ID | `12345` |
| `processName` | `%(processName)s` | Process name | `MainProcess` |
| `relativeCreated` | `%(relativeCreated)d` | Milliseconds since the `logging` module was loaded | `5432` |
| `thread` | `%(thread)d` | Thread ID | `140234567890` |
| `threadName` | `%(threadName)s` | Thread name | `MainThread` |
| `taskName` | `%(taskName)s` | `asyncio.Task` name (Python 3.12+) | `Task-1` |

## Date formatting

The `datefmt` parameter of `logging.Formatter` controls the format of the `%(asctime)s` attribute. It uses the same directives as `time.strftime()`.

### `strftime` directives

| Directive | Meaning | Example |
|-----------|---------|---------|
| `%d` | Day of the month (zero-padded) | `09` |
| `%m` | Month as a number (zero-padded) | `02` |
| `%Y` | Four-digit year | `2026` |
| `%y` | Two-digit year | `26` |
| `%H` | Hour in 24-hour format (zero-padded) | `14` |
| `%I` | Hour in 12-hour format (zero-padded) | `02` |
| `%M` | Minute (zero-padded) | `30` |
| `%S` | Second (zero-padded) | `05` |
| `%f` | Microsecond (zero-padded to six digits) | `000123` |
| `%p` | AM or PM | `PM` |
| `%A` | Full weekday name | `Monday` |
| `%a` | Abbreviated weekday name | `Mon` |
| `%B` | Full month name | `February` |
| `%b` | Abbreviated month name | `Feb` |
| `%Z` | Time zone name | `UTC` |
| `%%` | Literal `%` character | `%` |

### Example

```python
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
```

Output: `09/02/2026 14:30:05 [WARNING] Disk usage high`

**Note:** When `datefmt` is not specified, the default format is ISO 8601 with milliseconds: `2026-02-09 14:30:05,123`.

## Common format patterns

### Development (verbose)

```python
format = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
```

Output: `2026-02-09 14:30:05,123 - my_app - DEBUG - app.py:42 - Processing started`

### Production (structured)

```python
format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
datefmt = "%d/%m/%Y %H:%M:%S"
```

Output: `09/02/2026 14:30:05 [WARNING] my_app: Disk usage high`

### Minimal

```python
format = "%(levelname)s: %(message)s"
```

Output: `WARNING: Disk usage high`

### With process and thread information

```python
format = "%(asctime)s [%(process)d:%(threadName)s] %(levelname)s %(name)s: %(message)s"
```

Output: `2026-02-09 14:30:05,123 [12345:MainThread] INFO my_app: Request processed`

### File logging (detailed)

```python
format = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-15s | %(message)s"
```

Output: `2026-02-09 14:30:05,123 | WARNING  | my_app.database      | connect         | Connection timeout`

The `-8s` and `-20s` specifiers left-align the value and pad to the given width, producing neatly aligned columns.

## Custom formatting

For advanced formatting needs, subclass `logging.Formatter` and override the `format()` method.

```python
import logging


class BracketFormatter(logging.Formatter):
    """A formatter that wraps the level name in square brackets."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with bracketed level name.

        Args:
            record: The log record to format.

        Returns:
            The formatted log string.
        """
        record.levelname = "[%s]" % record.levelname
        return super().format(record)
```

## Further reading

- [LogRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes) -- official documentation
- [`time.strftime()` directives](https://docs.python.org/3/library/time.html#time.strftime) -- date formatting reference
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html) -- practical examples
