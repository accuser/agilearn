# Avoid common error handling mistakes

**The question.** You're reviewing (or writing) `try`/`except` code and something feels off — a bare `except` that catches Ctrl-C, a silent `pass` that ate a real bug, a try block that wraps half the function. You want the short list of traps and the fix for each.

The short list is below, then each trap in detail.

## The answer

## The answer

| Looks like… | Why it bites | Fix |
| --- | --- | --- |
| `except:` | also catches `KeyboardInterrupt`, `SystemExit` | name the specific type(s), or use `except Exception` |
| `except FileNotFoundError: pass` | silent swallow — debugging is nearly impossible | log, or at minimum add a comment explaining why it's safe |
| `except Exception` everywhere | hides bugs behind an umbrella catch | handle specific types; `Exception` only as a logged safety net |
| EAFP becomes flow control | `try: raise; except` instead of `if` | use `if`/`else` when the 'exception' is routine |
| 30-line `try` block | the wrong line raised your expected exception | shrink the `try`; wrap only the statement that can fail |
| `raise RuntimeError('bad')` inside an `except` | original cause lost | `raise RuntimeError('bad') from exc` |
| `f = open(...); f.read(); f.close()` | file never closed if `read()` raises | `with open(...) as f:` |

Each in detail below.

## Why each one bites

### 1. Bare `except`

A bare `except` clause catches *everything* — including `KeyboardInterrupt` (Ctrl-C) and `SystemExit`. That means users can't interrupt your program and `sys.exit()` silently fails. Use `except Exception` if you really need a wide catch; better still, name the types you actually expect.

```python
# Wrong
try: process_data(data)
except: print('something went wrong')

# Right
try: process_data(data)
except (ValueError, TypeError) as exc: print(f'invalid data: {exc}')
```

### 2. Silent swallow

`except X: pass` is almost always a bug in disguise. If the exception really is safe to ignore, say so in a comment; otherwise log it at minimum. 'An error happened somewhere' is the worst possible debugging clue.

```python
# Usually wrong
try: load_config()
except FileNotFoundError: pass

# Right — fallback is explicit
try:
    config = load_config()
except FileNotFoundError:
    logger.warning('config missing, using defaults')
    config = DEFAULT_CONFIG
```

### 3. Catching too broadly

`except Exception` catches `KeyError`, `TypeError`, `AttributeError`, and every bug you didn't anticipate. If you know exactly which exceptions your code can raise, name them. Reserve `Exception` for a logged safety net at a framework boundary.

### 4. Exceptions as flow control

```python
# Wrong
def is_positive(n):
    try:
        if n <= 0: raise ValueError
        return True
    except ValueError:
        return False

# Right
def is_positive(n):
    return n > 0
```

Python's 'easier to ask forgiveness than permission' (EAFP) style is fine when the exception really is exceptional. It stops being fine when you're raising just so you can catch — that's an `if`, in disguise.

### 5. Oversized `try` blocks

Only wrap the line that might raise the exception you're catching. A 10-line `try` around 'read file, parse it, process it, save result' means a `FileNotFoundError` printed by your except clause might actually be from the parse step, not the read.

### 6. Losing the original cause

When you raise a new exception from inside an `except`, use `from exc`. That attaches the original as `__cause__` and both appear in the traceback — otherwise you're throwing away the most useful debugging clue.

```python
# Wrong
try: int(raw)
except ValueError: raise RuntimeError('bad input')

# Right
try: int(raw)
except ValueError as exc: raise RuntimeError('bad input') from exc
```

### 7. Forgetting cleanup on exception

```python
# Wrong — f.close() never runs if f.read() raises
f = open('data.txt')
data = f.read()
f.close()

# Right — guaranteed cleanup
with open('data.txt') as f:
    data = f.read()
```

Context managers exist precisely for this. Any resource with a lifecycle — files, locks, connections, cursors — should be acquired with `with`.

## When the pattern is fine

Each of these is a *pattern*, not an absolute rule. `except Exception` at a top-level handler that logs and re-raises is fine — it's the framework boundary. Silent `pass` is fine when the exception is genuinely idempotent-and-expected, like 'delete this file, don't care if it already went'. A wider `try` block is fine when the grouping really is a single operation whose failure modes you handle together.

The traps bite when the shortcut is applied out of habit to a case where the defaults don't match the intent.

## Related reading

- [Create custom exceptions](create-custom-exceptions.ipynb) — raising your own types instead of reusing `ValueError`.
- [Handle multiple exceptions](handle-multiple-exceptions.ipynb) — ordering, grouping, and chaining.
- [Use context managers](use-context-managers.ipynb) — the cleanup-on-exception pattern in detail.
- [try/except syntax reference](../reference/try-except-syntax-reference.md) — the full grammar, including `else` and `finally`.
