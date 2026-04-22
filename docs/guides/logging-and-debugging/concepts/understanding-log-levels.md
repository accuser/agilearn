# Understanding log levels

Log levels are one of the most powerful features of the `logging` module. They give you a simple, universal way to categorise messages by importance and control which ones you actually see. Getting log levels right is the difference between a logging system that helps you and one that buries you in noise.

This article explores when and why to use each level, how to design a logging strategy, and how levels interact with handlers to give you fine-grained control over output.

## The hierarchy of severity

The five standard log levels form a hierarchy, from least severe to most severe:

```
DEBUG (10)  →  INFO (20)  →  WARNING (30)  →  ERROR (40)  →  CRITICAL (50)
```

Think of it like a volume dial. When you set the level to `WARNING`, you are turning down the volume &ndash; you still hear the loud, important things (`WARNING`, `ERROR`, `CRITICAL`), but the quieter background chatter (`DEBUG`, `INFO`) is filtered out.

Setting the level to `DEBUG` turns the volume all the way up: you hear everything. Setting it to `CRITICAL` means only the most urgent messages get through.

## `DEBUG` -- the developer's notebook

**Numeric value:** 10

**When to use it:** For detailed diagnostic information that is useful during development but too verbose for production.

Good `DEBUG` messages help you trace the flow of execution and understand the state of your program at key points:

```python
logger.debug("Entering process_order with %s items", len(items))
logger.debug("Calculated subtotal: %s", subtotal)
logger.debug("Tax rate applied: %s", tax_rate)
logger.debug("Database query returned %s rows in %s ms", row_count, elapsed)
```

### How much is too much?

A common mistake is logging everything at `DEBUG` level. If every variable assignment and function call generates a `DEBUG` message, the output becomes so noisy that it is useless. The key is to log **decisions and boundaries**: entering a function, choosing a code path, receiving external input, producing a result.

Another common mistake is logging too little. If turning on `DEBUG` does not give you enough information to diagnose a problem, your debug logging is not detailed enough. The goal is to be able to understand what happened by reading the debug log, without needing to add more logging and reproduce the issue.

## `INFO` -- the application diary

**Numeric value:** 20

**When to use it:** To confirm that things are working as expected. `INFO` messages record the significant events in the normal operation of your application.

Good `INFO` messages answer the question "what is the application doing right now?":

```python
logger.info("Application started on port %s", port)
logger.info("Loaded configuration from %s", config_path)
logger.info("Processing batch of %s orders", batch_size)
logger.info("User %s authenticated successfully", username)
logger.info("Scheduled task completed: %s records updated", count)
```

`INFO` messages are the ones you would want to see in a production dashboard. They should be meaningful and not too frequent &ndash; if your `INFO` output is more than a few lines per request or operation, some of those messages probably belong at `DEBUG` level.

## `WARNING` -- something unexpected

**Numeric value:** 30

**When to use it:** When something unexpected happened, but the program can still function correctly. A `WARNING` indicates a situation that might cause problems later or that deviates from the expected behaviour.

```python
logger.warning("Configuration file not found, using defaults")
logger.warning("API rate limit approaching: %s of %s requests used", used, limit)
logger.warning("Disk usage at %s%% on volume %s", usage, volume)
logger.warning("Deprecated function called: use new_function() instead")
logger.warning("Retrying failed request (attempt %s of %s)", attempt, max_retries)
```

`WARNING` is the default level for the root logger in Python. If you do not configure logging at all, only `WARNING` and above will appear. This is a sensible default: it means that out of the box, you see things that need attention but not routine operational noise.

### The difference between `WARNING` and `ERROR`

The distinction is whether the current operation succeeded:

- **`WARNING`**: The operation completed, but something was not ideal. "I did what you asked, but you should know about this."
- **`ERROR`**: The operation failed. "I could not do what you asked."

## `ERROR` -- something went wrong

**Numeric value:** 40

**When to use it:** When a specific operation failed but the application can continue running. An `ERROR` means something broke, but the program is still alive and can handle other requests or tasks.

```python
logger.error("Failed to connect to database at %s", db_host)
logger.error("Could not parse configuration file: %s", filepath)
logger.error("Payment processing failed for order %s", order_id)
```

When logging exceptions, use `logger.exception()` (which logs at `ERROR` level with a traceback) or pass `exc_info=True`:

```python
try:
    result = process(data)
except ValueError:
    logger.exception("Failed to process data")
```

This automatically includes the full traceback, which is invaluable for diagnosing the problem later.

## `CRITICAL` -- the system is failing

**Numeric value:** 50

**When to use it:** For serious errors that may prevent the program from continuing. `CRITICAL` should be reserved for situations where the application is in real trouble.

```python
logger.critical("Database connection pool exhausted, cannot serve requests")
logger.critical("Out of disk space on %s", volume)
logger.critical("Unrecoverable error in main loop, shutting down")
```

In many applications, `CRITICAL` messages trigger immediate alerts to the operations team. Use this level sparingly &ndash; if every error is critical, then nothing is truly critical.

## Choosing the right level

When you are about to write a log statement, ask yourself these questions:

1. **Did something fail?**
   - Yes, and the application may not recover → `CRITICAL`
   - Yes, but the application continues → `ERROR`
   - No → continue to question 2

2. **Is something unexpected or potentially problematic?**
   - Yes → `WARNING`
   - No → continue to question 3

3. **Is this a significant event in normal operation?**
   - Yes → `INFO`
   - No → `DEBUG`

### Common mistakes in level selection

- **Using `WARNING` for errors.** If an operation failed, that is an `ERROR`, not a `WARNING`.
- **Logging everything at `DEBUG`.** If your debug output is thousands of lines per second, it is hard to find anything useful in it.
- **Using `INFO` for detailed diagnostics.** If you would not want to see the message in a production dashboard, it belongs at `DEBUG`.
- **Never using `CRITICAL`.** Some applications genuinely never have critical failures. That is fine. Do not force it.

## Designing a logging strategy

Before adding logging to a project, consider three questions:

### Who is the audience?

- **Developers** need `DEBUG` and `INFO` to understand code behaviour during development.
- **Operators** need `WARNING`, `ERROR`, and `CRITICAL` to monitor system health.
- **Analysts** may need structured `INFO` messages to track business metrics.

Different audiences need different levels, which is exactly what the logging system provides.

### What is the environment?

- **Development**: Show everything (`DEBUG` and above). Use a simple console format.
- **Staging**: Show `INFO` and above. Use the same format as production to catch formatting issues.
- **Production**: Show `WARNING` and above on the console, `INFO` and above in files, and send `ERROR` and above to an alerting system.

### What is the volume?

Think about how many messages each level will produce under normal operation. In production, `DEBUG` messages might generate thousands of lines per second. That is fine &ndash; they should be disabled by default. `INFO` messages should be at a manageable rate. `WARNING` and above should be rare events.

## How levels interact with handlers

This is where the level system becomes truly powerful. The logger level and handler levels work together as two independent gates:

1. **The logger level** is the first gate. If a message does not pass the logger level, it is discarded immediately and never reaches any handler.

2. **The handler level** is the second gate. Each handler can have its own level, allowing different destinations to show different amounts of detail.

For example:

```python
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)  # Logger accepts everything

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Console shows WARNING+

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)  # File captures everything
```

In this configuration:

- `DEBUG` and `INFO` messages go to the file only
- `WARNING`, `ERROR`, and `CRITICAL` go to both the file and the console

The result is a clean console that only shows things that need attention, alongside a detailed file log for later analysis. This is a common and effective production pattern.

## Summary

Log levels are not just labels &ndash; they are a filtering mechanism that lets you control the verbosity of your application without changing the code. Use them thoughtfully:

- **`DEBUG`** for detailed diagnostics during development
- **`INFO`** for significant events in normal operation
- **`WARNING`** for unexpected but non-fatal situations
- **`ERROR`** for failed operations
- **`CRITICAL`** for potentially fatal problems

The right logging strategy balances detail with readability: enough information to diagnose problems, but not so much that the important messages are lost in noise.
