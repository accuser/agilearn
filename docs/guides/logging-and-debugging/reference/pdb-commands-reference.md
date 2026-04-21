# `pdb` commands reference

A complete reference for `pdb`, the built-in Python debugger, including all commands for navigation, inspection, breakpoint management, and execution control.

## Starting the debugger

### From within code

```python
# Modern approach (Python 3.7+)
breakpoint()

# Older approach (equivalent)
import pdb; pdb.set_trace()
```

### From the command line

```bash
# Run a script under pdb (stops at the first line)
python -m pdb script.py

# Run with arguments
python -m pdb script.py arg1 arg2
```

### Programmatic usage

```python
import pdb

# Run a statement under the debugger
pdb.run("my_function()")

# Start post-mortem debugging after an exception
pdb.pm()

# Start post-mortem debugging with a specific traceback
pdb.post_mortem(traceback_object)
```

### Disabling breakpoints

Set the `PYTHONBREAKPOINT` environment variable:

```bash
# Disable all breakpoint() calls
PYTHONBREAKPOINT=0 python script.py

# Use a different debugger
PYTHONBREAKPOINT=ipdb.set_trace python script.py
```

## Navigation commands

Commands for controlling the flow of execution.

| Command | Shortcut | Description |
|---------|----------|-------------|
| `next` | `n` | Execute the current line, stepping over function calls |
| `step` | `s` | Execute the current line, stepping into function calls |
| `continue` | `c` or `cont` | Continue execution until the next breakpoint |
| `return` | `r` | Continue execution until the current function returns |
| `until` | `unt` | Continue until a line number greater than the current is reached |
| `until lineno` | `unt lineno` | Continue until the specified line number is reached |
| `jump lineno` | `j lineno` | Jump to the specified line (skipping or re-executing code) |

### `next` versus `step`

- **`next`** executes the current line completely. If the line contains a function call, the entire function runs before stopping.
- **`step`** enters function calls. If the current line calls a function, the debugger stops at the first line of that function.

### `until`

Without an argument, `until` continues until a line with a number greater than the current line is reached. This is useful for getting past the end of a loop without setting a breakpoint.

### `jump`

The `jump` command changes the next line to be executed. It can only be used within the same frame. Use with caution, as it can produce unexpected behaviour.

## Inspection commands

Commands for examining the current state of the program.

| Command | Shortcut | Description |
|---------|----------|-------------|
| `print expr` | `p expr` | Print the value of an expression |
| `pp expr` | | Pretty-print the value of an expression |
| `list` | `l` | Show 11 lines of source code around the current line |
| `list first, last` | `l first, last` | Show source code between the specified line numbers |
| `longlist` | `ll` | Show the entire source code of the current function |
| `where` | `w` | Show the call stack (most recent frame at the bottom) |
| `up` | `u` | Move one frame up in the call stack |
| `down` | `d` | Move one frame down in the call stack |
| `args` | `a` | Print the arguments of the current function |
| `whatis expr` | | Print the type of an expression |
| `source expr` | | Show the source code of an object |
| `display expr` | | Display the value of an expression each time execution stops |
| `undisplay expr` | | Remove an expression from the display list |
| `interact` | | Start an interactive interpreter in the current scope |

### Using `print`

You can evaluate any Python expression at the `(Pdb)` prompt:

```
(Pdb) p my_variable
42
(Pdb) p len(my_list)
5
(Pdb) p [x * 2 for x in range(3)]
[0, 2, 4]
(Pdb) p type(my_variable)
<class 'int'>
```

### Navigating the call stack

Use `where` to see the full call stack, then `up` and `down` to move between frames. This lets you inspect variables in different scopes.

```
(Pdb) w
  /path/to/script.py(20)<module>()
-> result = process(data)
  /path/to/script.py(10)process()
-> return transform(item)
> /path/to/script.py(5)transform()
-> return item["key"]
(Pdb) u
> /path/to/script.py(10)process()
-> return transform(item)
(Pdb) p item
{'name': 'test'}
```

## Breakpoint commands

Commands for managing breakpoints.

| Command | Description |
|---------|-------------|
| `break` or `b` | List all breakpoints |
| `break lineno` or `b lineno` | Set a breakpoint at a line number |
| `break filename:lineno` | Set a breakpoint in a specific file |
| `break function` | Set a breakpoint at the first line of a function |
| `break lineno, condition` | Set a conditional breakpoint |
| `tbreak lineno` | Set a temporary breakpoint (removed after first hit) |
| `clear` or `cl` | Clear all breakpoints (with confirmation) |
| `clear bpnumber` | Clear a specific breakpoint by number |
| `clear filename:lineno` | Clear breakpoints at a specific location |
| `disable bpnumber` | Disable a breakpoint (keep it but do not stop) |
| `enable bpnumber` | Re-enable a disabled breakpoint |
| `ignore bpnumber count` | Ignore a breakpoint for the next `count` hits |
| `condition bpnumber condition` | Set or change the condition on a breakpoint |

### Conditional breakpoints

```
(Pdb) b 15, len(items) > 10
Breakpoint 1 at script.py:15
(Pdb) b 20, name == "error"
Breakpoint 2 at script.py:20
```

The debugger only stops at the breakpoint when the condition evaluates to `True`.

### Temporary breakpoints

```
(Pdb) tbreak 25
Breakpoint 3 at script.py:25
```

A temporary breakpoint is automatically removed after it is hit once.

## Execution commands

| Command | Description |
|---------|-------------|
| `!statement` | Execute a Python statement in the current scope |
| `run [args]` or `restart [args]` | Restart the program |
| `interact` | Start an interactive Python interpreter |

### Executing statements

Prefix a statement with `!` to execute it:

```
(Pdb) !x = 42
(Pdb) p x
42
```

This is useful for modifying variables during a debugging session.

## Other commands

| Command | Description |
|---------|-------------|
| `help` or `h` | List all available commands |
| `help command` | Show help for a specific command |
| `quit` or `q` | Quit the debugger (and stop the program) |
| `alias name command` | Create a command alias |
| `unalias name` | Remove an alias |

## Common workflows

### Debugging a crash

```bash
python -m pdb script.py
```

1. Type `c` to continue until the crash
2. Inspect variables with `p`
3. Navigate the stack with `w`, `u`, and `d`

### Debugging a specific function

1. Add `breakpoint()` at the start of the function
2. Run the program normally
3. Use `n` to step through, `p` to inspect values
4. Use `c` to continue when finished
5. Remove the `breakpoint()` call

### Finding where a value changes

1. Set a breakpoint at the suspected location
2. Use `display variable` to watch the value
3. Use `c` to continue; `pdb` shows the value each time it stops

## Further reading

- [Python `pdb` documentation](https://docs.python.org/3/library/pdb.html)
- [Python Debugging with pdb](https://docs.python.org/3/library/pdb.html#debugger-commands) -- full command reference
- [`breakpoint()` documentation](https://docs.python.org/3/library/functions.html#breakpoint)
