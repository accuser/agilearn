# String formatting reference

This page provides a complete reference for string formatting in Python, covering f-strings, the `str.format()` method, the format specification mini-language, and the older `%` formatting operator.

For the official documentation, see the [Python Format String Syntax](https://docs.python.org/3/library/string.html#formatstrings) and the [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#format-specification-mini-language).

---

## f-string syntax

Formatted string literals, commonly known as f-strings, were introduced in Python 3.6 (PEP 498). An f-string is a string literal prefixed with `f` or `F` that can contain expressions inside curly braces `{}`. These expressions are evaluated at runtime and formatted using the format specification mini-language.

### Basic syntax

```python
f"{expression}"
f"{expression:format_spec}"
f"{expression!conversion}"
f"{expression!conversion:format_spec}"
```

### Expressions

Any valid Python expression can appear inside the curly braces.

```python
>>> name = "world"
>>> f"Hello, {name}!"
'Hello, world!'

>>> f"The sum of 2 + 3 is {2 + 3}."
'The sum of 2 + 3 is 5.'

>>> items = ["apple", "banana", "cherry"]
>>> f"First item: {items[0]}"
'First item: apple'

>>> f"Uppercase: {name.upper()}"
'Uppercase: WORLD'
```

### Conversions

A conversion field causes type coercion before formatting. Three conversion flags are supported:

| Flag | Meaning | Equivalent |
|---|---|---|
| `!s` | Calls `str()` on the value | `str(value)` |
| `!r` | Calls `repr()` on the value | `repr(value)` |
| `!a` | Calls `ascii()` on the value | `ascii(value)` |

```python
>>> value = "café"
>>> f"{value!s}"
'café'
>>> f"{value!r}"
"'café'"
>>> f"{value!a}"
"'caf\\xe9'"
```

### Nesting and self-documenting expressions

F-strings support nested expressions and, since Python 3.8, self-documenting expressions using the `=` specifier.

```python
>>> width = 10
>>> precision = 4
>>> value = 12.34567
>>> f"{value:{width}.{precision}}"
'     12.35'

>>> x = 42
>>> f"{x = }"
'x = 42'
>>> f"{x = :05d}"
'x = 00042'
```

### Escaping braces

To include a literal brace character in an f-string, double it.

```python
>>> f"{{literal braces}}"
'{literal braces}'
```

### Multi-line f-strings

F-strings can span multiple lines when used inside parentheses or with triple quotes.

```python
>>> name = "Alice"
>>> age = 30
>>> message = (
...     f"Name: {name}\n"
...     f"Age: {age}"
... )
>>> print(message)
Name: Alice
Age: 30
```

---

## `str.format()` syntax

The `str.format()` method performs string formatting by replacing replacement fields delimited by curly braces `{}` with the arguments passed to the method.

### Basic syntax

```python
"text {field} text".format(value)
"text {field:format_spec} text".format(value)
```

### Positional and keyword arguments

```python
>>> "{0}, {1}, {2}".format("a", "b", "c")
'a, b, c'

>>> "{}, {}, {}".format("a", "b", "c")
'a, b, c'

>>> "{name} is {age}".format(name="Alice", age=30)
'Alice is 30'

>>> "{0} is {age}".format("Alice", age=30)
'Alice is 30'
```

### Accessing attributes and items

```python
>>> import datetime
>>> d = datetime.date(2024, 1, 15)
>>> "The date is {0.day}/{0.month}/{0.year}".format(d)
'The date is 15/1/2024'

>>> data = {"name": "Alice", "role": "developer"}
>>> "{name} is a {role}".format(**data)
'Alice is a developer'

>>> items = ["zero", "one", "two"]
>>> "Item: {0[1]}".format(items)
'Item: one'
```

### Escaping braces

As with f-strings, double the braces to include literal brace characters.

```python
>>> "Use {{}} for placeholders in format strings".format()
'Use {} for placeholders in format strings'
```

---

## Format specification mini-language

The format specification mini-language defines how individual values are presented. It is used by f-strings, `str.format()`, and the built-in `format()` function.

### Full syntax

```
[[fill]align][sign][z][#][0][width][grouping_option][.precision][type]
```

Each component is optional. The components must appear in the order shown above.

### Alignment options

The `align` character specifies how the value is aligned within the available width. An optional `fill` character (which can be any character except `{` or `}`) precedes the alignment character.

| Align | Meaning | Applicable to |
|---|---|---|
| `<` | Left-align within the available space | All types |
| `>` | Right-align within the available space | All types (default for numbers) |
| `^` | Centre within the available space | All types |
| `=` | Place padding after the sign but before the digits | Numeric types only |

```python
>>> f"{'hello':<10}"
'hello     '
>>> f"{'hello':>10}"
'     hello'
>>> f"{'hello':^10}"
'  hello   '
>>> f"{'hello':*^10}"
'**hello***'
>>> f"{-42:=10}"
'-       42'
>>> f"{-42:0=10}"
'-000000042'
```

If no alignment is specified, strings default to left-aligned and numbers default to right-aligned.

### Sign options

The `sign` option is only valid for numeric types.

| Sign | Meaning |
|---|---|
| `+` | Use a sign for both positive and negative numbers |
| `-` | Use a sign only for negative numbers (default behaviour) |
| (space) | Use a leading space for positive numbers, a minus sign for negative numbers |

```python
>>> f"{42:+d}"
'+42'
>>> f"{-42:+d}"
'-42'
>>> f"{42:-d}"
'42'
>>> f"{42: d}"
' 42'
>>> f"{-42: d}"
'-42'
```

### The `z` option

Available since Python 3.11. When used with a numeric presentation type, this option coerces negative zero floating-point values to positive zero after rounding.

```python
>>> x = -0.0001
>>> f"{x:z.1f}"
'0.0'
>>> f"{x:.1f}"
'-0.0'
```

### The `#` option

The `#` option causes the "alternate form" to be used for the conversion. For integers, this adds the prefix `0b`, `0o`, `0x`, or `0X` for binary, octal, hexadecimal, and upper-case hexadecimal output respectively. For floats, the decimal point is always present even if no digits follow it.

```python
>>> f"{42:#b}"
'0b101010'
>>> f"{42:#o}"
'0o52'
>>> f"{42:#x}"
'0x2a'
>>> f"{1.0:#.0f}"
'1.'
```

### The `0` option

When no explicit alignment is given, preceding the `width` field with a zero character enables sign-aware zero-padding for numeric types. This is equivalent to a fill character of `0` with an alignment type of `=`.

```python
>>> f"{42:05d}"
'00042'
>>> f"{-42:05d}"
'-0042'
```

### Width

The `width` is a decimal integer defining the minimum total field width, including any prefixes, separators, and other formatting characters. If not specified, the field width is determined by the content.

```python
>>> f"{'hello':10}"
'hello     '
>>> f"{42:10}"
'        42'
```

### Grouping options

The grouping option inserts a separator between digit groups for readability.

| Option | Meaning |
|---|---|
| `,` | Use a comma as the thousands separator |
| `_` | Use an underscore as the thousands separator |

For integer presentation types `b`, `o`, `x`, and `X`, underscores are inserted every 4 digits rather than every 3.

```python
>>> f"{1234567:,}"
'1,234,567'
>>> f"{1234567:_}"
'1_234_567'
>>> f"{1234567890.12:,.2f}"
'1,234,567,890.12'
>>> f"{0xDEADBEEF:#_x}"
'0xdead_beef'
```

### Precision

The `precision` is a decimal number preceded by a dot `.`.

- For floating-point types formatted with `f` or `F`, it specifies the number of digits after the decimal point.
- For floating-point types formatted with `g` or `G`, it specifies the total number of significant digits.
- For non-numeric types, it specifies the maximum field size (the number of characters used from the content).
- Precision is not permitted for integer presentation types.

```python
>>> import math
>>> f"{math.pi:.4f}"
'3.1416'
>>> f"{math.pi:.4g}"
'3.142'
>>> f"{'hello world':.5}"
'hello'
```

### Integer type codes

| Type | Meaning | Example | Result |
|---|---|---|---|
| `b` | Binary format | `f"{42:b}"` | `"101010"` |
| `c` | Character (converts integer to corresponding Unicode character) | `f"{65:c}"` | `"A"` |
| `d` | Decimal integer (default for integers) | `f"{42:d}"` | `"42"` |
| `o` | Octal format | `f"{42:o}"` | `"52"` |
| `x` | Hexadecimal format (lowercase) | `f"{255:x}"` | `"ff"` |
| `X` | Hexadecimal format (uppercase) | `f"{255:X}"` | `"FF"` |
| `n` | Number, same as `d` but uses the current locale setting for the number separator | `f"{1234:n}"` | `"1234"` (locale-dependent) |

```python
>>> f"{42:b}"
'101010'
>>> f"{42:08b}"
'00101010'
>>> f"{255:x}"
'ff'
>>> f"{255:#X}"
'0XFF'
>>> f"{65:c}"
'A'
```

### Float type codes

| Type | Meaning | Example | Result |
|---|---|---|---|
| `e` | Scientific notation (lowercase `e`) | `f"{1234.5:e}"` | `"1.234500e+03"` |
| `E` | Scientific notation (uppercase `E`) | `f"{1234.5:E}"` | `"1.234500E+03"` |
| `f` | Fixed-point notation (default precision is 6) | `f"{3.14159:f}"` | `"3.141590"` |
| `F` | Fixed-point notation (same as `f`, but `nan` becomes `NAN` and `inf` becomes `INF`) | `f"{float('nan'):F}"` | `"NAN"` |
| `g` | General format (uses `e` for large or small numbers, otherwise `f`; default for floats) | `f"{1234.5:g}"` | `"1234.5"` |
| `G` | General format (uses `E` instead of `e`) | `f"{1234567.0:G}"` | `"1.23457E+06"` |
| `n` | Number, same as `g` but uses the current locale setting for the number separator | `f"{1234.5:n}"` | `"1234.5"` (locale-dependent) |
| `%` | Percentage (multiplies by 100 and displays with a percent sign) | `f"{0.75:%}"` | `"75.000000%"` |

```python
>>> f"{0.001234:e}"
'1.234000e-03'
>>> f"{3.14159:.2f}"
'3.14'
>>> f"{0.75:.1%}"
'75.0%'
>>> f"{1234567.89:,.2f}"
'1,234,567.89'
>>> f"{float('inf'):f}"
'inf'
>>> f"{float('inf'):F}"
'INF'
```

### String type code

| Type | Meaning | Example | Result |
|---|---|---|---|
| `s` | String format (default for strings) | `f"{'hello':s}"` | `"hello"` |

The `s` type is the default presentation type for strings and is rarely specified explicitly.

---

## Common formatting patterns

The following table shows frequently used formatting patterns for quick reference.

| Pattern | Description | Example | Result |
|---|---|---|---|
| `{:.2f}` | Two decimal places | `f"{3.14159:.2f}"` | `"3.14"` |
| `{:,}` | Thousands separator | `f"{1000000:,}"` | `"1,000,000"` |
| `{:,.2f}` | Thousands separator with two decimal places | `f"{1234567.89:,.2f}"` | `"1,234,567.89"` |
| `{:.1%}` | Percentage with one decimal place | `f"{0.856:.1%}"` | `"85.6%"` |
| `{:>10}` | Right-align in 10-character field | `f"{'hi':>10}"` | `"        hi"` |
| `{:<10}` | Left-align in 10-character field | `f"{'hi':<10}"` | `"hi        "` |
| `{:^10}` | Centre in 10-character field | `f"{'hi':^10}"` | `"    hi    "` |
| `{:0>5}` | Pad with zeros (left) | `f"{'42':0>5}"` | `"00042"` |
| `{:05d}` | Zero-padded integer | `f"{42:05d}"` | `"00042"` |
| `{:+.2f}` | Always show sign | `f"{3.14:+.2f}"` | `"+3.14"` |
| `{:#010x}` | Hexadecimal with prefix and padding | `f"{255:#010x}"` | `"0x000000ff"` |
| `{:08b}` | Binary with zero padding | `f"{42:08b}"` | `"00101010"` |
| `{:.5}` | Truncate string to 5 characters | `f"{'hello world':.5}"` | `"hello"` |
| `{:*^20}` | Centre with custom fill character | `f"{'title':*^20}"` | `"*******title********"` |

---

## `%` formatting (legacy)

The `%` operator (sometimes called printf-style formatting) is the oldest string formatting mechanism in Python. While it is still fully supported, f-strings and `str.format()` are preferred for new code because they are more readable and more capable.

### Basic syntax

```python
"format string" % values
```

### Common conversion specifiers

| Specifier | Meaning | Example | Result |
|---|---|---|---|
| `%s` | String | `"%s" % "hello"` | `"hello"` |
| `%d` | Decimal integer | `"%d" % 42` | `"42"` |
| `%f` | Floating-point number | `"%f" % 3.14` | `"3.140000"` |
| `%x` | Hexadecimal (lowercase) | `"%x" % 255` | `"ff"` |
| `%X` | Hexadecimal (uppercase) | `"%X" % 255` | `"FF"` |
| `%o` | Octal | `"%o" % 42` | `"52"` |
| `%e` | Scientific notation | `"%e" % 1234.5` | `"1.234500e+03"` |
| `%%` | Literal `%` character | `"100%%"` | `"100%"` |

### Width and precision

```python
>>> "%10d" % 42
'        42'
>>> "%-10d" % 42
'42        '
>>> "%05d" % 42
'00042'
>>> "%.2f" % 3.14159
'3.14'
>>> "%10.2f" % 3.14159
'      3.14'
```

### Multiple values

When formatting multiple values, pass them as a tuple.

```python
>>> "Name: %s, Age: %d" % ("Alice", 30)
'Name: Alice, Age: 30'
```

### Dictionary-based formatting

```python
>>> "%(name)s is %(age)d" % {"name": "Alice", "age": 30}
'Alice is 30'
```

### Limitations

The `%` formatting approach has several limitations compared with f-strings and `str.format()`:

- It does not support accessing object attributes or dictionary keys with dot or bracket notation in the format string itself.
- It cannot call methods or use arbitrary expressions.
- It has limited support for custom formatting.
- Using a single value that happens to be a tuple requires wrapping it in another tuple.

---

## See also

- [Format String Syntax](https://docs.python.org/3/library/string.html#formatstrings) -- official Python documentation for `str.format()` syntax
- [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#format-specification-mini-language) -- official reference for the format spec
- [PEP 498 -- Literal String Interpolation](https://peps.python.org/pep-0498/) -- the PEP that introduced f-strings
- [PEP 701 -- Syntactic formalization of f-strings](https://peps.python.org/pep-0701/) -- relaxed restrictions on f-strings in Python 3.12
- [String methods reference](string-methods-reference.md) -- comprehensive reference for all `str` methods
- [String constants reference](string-constants-reference.md) -- constants from the `string` module
- [printf-style String Formatting](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting) -- official documentation for `%` formatting
