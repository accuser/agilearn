# String constants reference

This page provides a reference for the constants and utility classes available in Python's `string` module. The `string` module contains a collection of predefined string constants and helper classes that are useful for string processing tasks such as character classification, filtering, and template-based substitution.

To use the constants and classes described on this page, import the module:

```python
import string
```

For the official documentation, see the [Python `string` module documentation](https://docs.python.org/3/library/string.html).

---

## String constants

The `string` module provides the following constants. Each constant is a string containing a specific set of characters. These constants are not locale-dependent and do not change.

| Constant | Value | Description |
|---|---|---|
| `string.ascii_letters` | `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ` | Concatenation of `ascii_lowercase` and `ascii_uppercase` |
| `string.ascii_lowercase` | `abcdefghijklmnopqrstuvwxyz` | Lowercase ASCII letters |
| `string.ascii_uppercase` | `ABCDEFGHIJKLMNOPQRSTUVWXYZ` | Uppercase ASCII letters |
| `string.digits` | `0123456789` | Decimal digit characters |
| `string.hexdigits` | `0123456789abcdefABCDEF` | Characters valid in hexadecimal numbers |
| `string.octdigits` | `01234567` | Characters valid in octal numbers |
| `string.punctuation` | ``!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~`` | ASCII punctuation characters |
| `string.printable` | (digits + letters + punctuation + whitespace) | All printable ASCII characters |
| `string.whitespace` | `` \t\n\r\x0b\x0c`` | ASCII whitespace characters (space, tab, newline, carriage return, vertical tab, form feed) |

### Detailed descriptions and example use cases

#### `string.ascii_letters`

Contains all ASCII letters, both lowercase and uppercase. This is the concatenation of `string.ascii_lowercase` and `string.ascii_uppercase`.

```python
>>> import string
>>> string.ascii_letters
'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
>>> len(string.ascii_letters)
52
```

**Example use case:** Generating random identifiers that contain only ASCII letters.

```python
import random
import string

identifier = "".join(random.choices(string.ascii_letters, k=8))
```

#### `string.ascii_lowercase`

Contains all lowercase ASCII letters from `a` to `z`.

```python
>>> string.ascii_lowercase
'abcdefghijklmnopqrstuvwxyz'
```

**Example use case:** Checking whether a character is a lowercase ASCII letter without using locale-dependent methods.

```python
import string

def is_ascii_lower(char: str) -> bool:
    return char in string.ascii_lowercase
```

#### `string.ascii_uppercase`

Contains all uppercase ASCII letters from `A` to `Z`.

```python
>>> string.ascii_uppercase
'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
```

**Example use case:** Creating a Caesar cipher or other letter-based transformations.

```python
import string

def caesar_encrypt(text: str, shift: int) -> str:
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    result = []
    for char in text:
        if char in upper:
            result.append(upper[(upper.index(char) + shift) % 26])
        elif char in lower:
            result.append(lower[(lower.index(char) + shift) % 26])
        else:
            result.append(char)
    return "".join(result)
```

#### `string.digits`

Contains the decimal digit characters `0` through `9`.

```python
>>> string.digits
'0123456789'
```

**Example use case:** Filtering a string to extract only numeric characters.

```python
import string

def extract_digits(text: str) -> str:
    return "".join(c for c in text if c in string.digits)

extract_digits("Order #12345-A")  # "12345"
```

#### `string.hexdigits`

Contains all characters that are valid in hexadecimal numbers: `0`-`9`, `a`-`f`, and `A`-`F`.

```python
>>> string.hexdigits
'0123456789abcdefABCDEF'
```

**Example use case:** Validating whether a string represents a valid hexadecimal value.

```python
import string

def is_valid_hex(text: str) -> bool:
    return all(c in string.hexdigits for c in text) and len(text) > 0

is_valid_hex("1a2B3c")  # True
is_valid_hex("xyz")     # False
```

#### `string.octdigits`

Contains all characters that are valid in octal numbers: `0` through `7`.

```python
>>> string.octdigits
'01234567'
```

**Example use case:** Validating octal permission strings.

```python
import string

def is_valid_octal_permissions(text: str) -> bool:
    return len(text) == 3 and all(c in string.octdigits for c in text)

is_valid_octal_permissions("755")  # True
is_valid_octal_permissions("789")  # False
```

#### `string.punctuation`

Contains all ASCII punctuation characters.

```python
>>> string.punctuation
'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
>>> len(string.punctuation)
32
```

**Example use case:** Removing punctuation from text for natural language processing.

```python
import string

def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))

remove_punctuation("Hello, world!")  # "Hello world"
```

#### `string.printable`

Contains all ASCII characters that are considered printable. This includes digits, letters, punctuation, and whitespace.

```python
>>> len(string.printable)
100
```

**Example use case:** Filtering out non-printable characters from input.

```python
import string

def sanitise_input(text: str) -> str:
    return "".join(c for c in text if c in string.printable)
```

#### `string.whitespace`

Contains ASCII whitespace characters: space (`' '`), tab (`'\t'`), newline (`'\n'`), carriage return (`'\r'`), vertical tab (`'\x0b'`), and form feed (`'\x0c'`).

```python
>>> string.whitespace
' \t\n\r\x0b\x0c'
>>> len(string.whitespace)
6
```

**Example use case:** Replacing all whitespace characters with a single space.

```python
import string

def normalise_whitespace(text: str) -> str:
    result = text
    for ws in string.whitespace:
        result = result.replace(ws, " ")
    # Collapse multiple spaces
    while "  " in result:
        result = result.replace("  ", " ")
    return result.strip()
```

---

## `string.Template`

The `string.Template` class provides a simpler string substitution mechanism than f-strings or `str.format()`. Templates use `$`-based substitutions, which can be useful when working with strings provided by users or external sources where full format string capabilities are not needed or not safe.

### Basic usage

```python
from string import Template

t = Template("Hello, $name! You have $count messages.")
result = t.substitute(name="Alice", count=5)
# "Hello, Alice! You have 5 messages."
```

### Substitution methods

| Method | Description |
|---|---|
| `Template.substitute(**kwargs)` | Perform substitution; raises `KeyError` if a placeholder is missing |
| `Template.safe_substitute(**kwargs)` | Perform substitution; leaves placeholders intact if values are missing |

```python
from string import Template

t = Template("$greeting, $name!")

# substitute raises KeyError for missing placeholders
t.substitute(greeting="Hello")
# KeyError: 'name'

# safe_substitute leaves missing placeholders unchanged
t.safe_substitute(greeting="Hello")
# "Hello, $name!"
```

### Syntax rules

- `$$` is an escape for a literal `$` character.
- `$identifier` names a substitution placeholder matching the regular expression `[_a-z][_a-z0-9]*` (case-insensitive).
- `${identifier}` is equivalent to `$identifier` and is required when the substitution is followed by valid identifier characters.

```python
from string import Template

t = Template("${item}s cost $$$price each")
t.substitute(item="widget", price="9.99")
# "widgets cost $9.99 each"
```

For a practical guide on using `string.Template` for common tasks, see the [Recipes](../recipes/) section.

---

## `string.Formatter`

The `string.Formatter` class implements the same formatting mechanism used by `str.format()`. It is designed to be subclassed by developers who need to create custom formatting behaviour.

The class provides the following primary methods:

| Method | Description |
|---|---|
| `Formatter.format(format_string, *args, **kwargs)` | The main API method; takes a format string and arguments |
| `Formatter.vformat(format_string, args, kwargs)` | The underlying function that does the actual formatting work |
| `Formatter.parse(format_string)` | Iterates over the format string and returns an iterable of tuples |
| `Formatter.get_field(field_name, args, kwargs)` | Given a field name, returns the object to be formatted and the key |
| `Formatter.get_value(key, args, kwargs)` | Retrieves a given field value |
| `Formatter.check_unused_args(used_args, args, kwargs)` | Called after formatting to check for unused arguments |
| `Formatter.format_field(value, format_spec)` | Calls the `format()` built-in on a single field value |
| `Formatter.convert_field(value, conversion)` | Converts the value using the given conversion type (`s`, `r`, or `a`) |

### Example: custom formatter

```python
import string

class UpperFormatter(string.Formatter):
    """A formatter that converts all string values to uppercase."""

    def format_field(self, value, format_spec):
        if isinstance(value, str) and not format_spec:
            return value.upper()
        return super().format_field(value, format_spec)

formatter = UpperFormatter()
formatter.format("Hello, {name}!", name="world")
# "Hello, WORLD!"
```

In most cases, f-strings or `str.format()` are sufficient, and directly subclassing `string.Formatter` is not necessary. This class is primarily useful for applications that need to customise the formatting pipeline, such as template engines or internationalisation frameworks.

---

## Practical examples

### Password generation

Generate a random password containing letters, digits, and punctuation.

```python
import random
import string

def generate_password(length: int = 16) -> str:
    """Generate a random password of the specified length.

    The password contains a mix of uppercase letters, lowercase letters,
    digits, and punctuation characters.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choices(characters, k=length))
    return password

generate_password()  # for example, "aK3!mZ9@pL2#nQ7&"
```

### Character filtering

Remove all non-alphanumeric characters from a string.

```python
import string

def filter_alphanumeric(text: str) -> str:
    """Remove all characters except letters and digits."""
    allowed = string.ascii_letters + string.digits
    return "".join(c for c in text if c in allowed)

filter_alphanumeric("Hello, World! 123")  # "HelloWorld123"
```

### Input validation

Validate that a username contains only permitted characters.

```python
import string

ALLOWED_USERNAME_CHARS = string.ascii_lowercase + string.digits + "_-"

def is_valid_username(username: str) -> bool:
    """Check whether a username contains only lowercase letters, digits,
    underscores, and hyphens.

    Args:
        username: The username to validate.

    Returns:
        True if the username is valid, False otherwise.
    """
    if not username:
        return False
    return all(c in ALLOWED_USERNAME_CHARS for c in username)

is_valid_username("alice_123")   # True
is_valid_username("Alice 123")   # False
is_valid_username("")            # False
```

### Building a character frequency counter

Count the frequency of different character types in a string.

```python
import string

def character_breakdown(text: str) -> dict[str, int]:
    """Categorise and count the characters in a string.

    Returns a dictionary with counts for letters, digits,
    punctuation, whitespace, and other characters.
    """
    counts = {
        "letters": 0,
        "digits": 0,
        "punctuation": 0,
        "whitespace": 0,
        "other": 0,
    }
    for char in text:
        if char in string.ascii_letters:
            counts["letters"] += 1
        elif char in string.digits:
            counts["digits"] += 1
        elif char in string.punctuation:
            counts["punctuation"] += 1
        elif char in string.whitespace:
            counts["whitespace"] += 1
        else:
            counts["other"] += 1
    return counts

character_breakdown("Hello, World! 123")
# {"letters": 10, "digits": 3, "punctuation": 2, "whitespace": 2, "other": 0}
```

---

## See also

- [Python `string` module documentation](https://docs.python.org/3/library/string.html) -- official reference for the `string` module
- [String methods reference](string-methods-reference.md) -- comprehensive reference for all `str` methods
- [String formatting reference](string-formatting-reference.md) -- f-strings, `str.format()`, and the format specification mini-language
- [PEP 292 -- Simpler String Substitutions](https://peps.python.org/pep-0292/) -- the PEP that introduced `string.Template`
