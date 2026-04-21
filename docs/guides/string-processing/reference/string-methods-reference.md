# String methods reference

This page provides a comprehensive reference for all methods available on Python `str` objects. Each method is grouped by category, with a summary table followed by detailed signatures and descriptions.

For the official documentation, see the [Python `str` type documentation](https://docs.python.org/3/library/stdtypes.html#string-methods).

All string methods return new values. Strings in Python are immutable, so no method modifies the original string in place.

---

## Case conversion

Methods that return a copy of the string with the case of characters changed.

| Method | Description | Example | Result |
|---|---|---|---|
| `str.upper()` | Convert all characters to uppercase | `"hello".upper()` | `"HELLO"` |
| `str.lower()` | Convert all characters to lowercase | `"HELLO".lower()` | `"hello"` |
| `str.capitalize()` | Capitalise the first character, lowercase the rest | `"hello WORLD".capitalize()` | `"Hello world"` |
| `str.title()` | Capitalise the first character of each word | `"hello world".title()` | `"Hello World"` |
| `str.swapcase()` | Swap uppercase to lowercase and vice versa | `"Hello".swapcase()` | `"hELLO"` |
| `str.casefold()` | Aggressive lowercase for caseless matching | `"Straße".casefold()` | `"strasse"` |

### Detailed signatures

#### `str.upper()`

```python
str.upper() -> str
```

Returns a copy of the string with all cased characters converted to uppercase. The method handles Unicode characters, not only ASCII.

```python
>>> "café".upper()
'CAFÉ'
```

#### `str.lower()`

```python
str.lower() -> str
```

Returns a copy of the string with all cased characters converted to lowercase.

```python
>>> "CAFÉ".lower()
'café'
```

#### `str.capitalize()`

```python
str.capitalize() -> str
```

Returns a copy of the string with the first character capitalised and the remainder lowercased.

```python
>>> "hello WORLD".capitalize()
'Hello world'
```

#### `str.title()`

```python
str.title() -> str
```

Returns a titlecased version of the string, where words start with an uppercase character and the remaining characters are lowercase. The algorithm uses a simple word boundary definition: any sequence of characters that are not letters is treated as a word separator. This can produce unexpected results with apostrophes and other punctuation.

```python
>>> "they're bill's friends".title()
"They'Re Bill'S Friends"
```

#### `str.swapcase()`

```python
str.swapcase() -> str
```

Returns a copy of the string with uppercase characters converted to lowercase and vice versa. Note that `s.swapcase().swapcase()` is not necessarily equal to `s` for certain Unicode characters.

```python
>>> "Hello World".swapcase()
'hELLO wORLD'
```

#### `str.casefold()`

```python
str.casefold() -> str
```

Returns a casefolded copy of the string. Casefolding is similar to lowercasing but more aggressive, as it is intended to remove all case distinctions in a string. This is useful for caseless matching. For example, the German lowercase letter `ß` is equivalent to `ss`; since it is already lowercase, `lower()` would do nothing, but `casefold()` converts it to `ss`.

```python
>>> "Straße".casefold()
'strasse'
>>> "HELLO".casefold()
'hello'
```

---

## Search and test

Methods for finding substrings and testing for the presence of content within a string.

| Method | Description | Example | Result |
|---|---|---|---|
| `str.find()` | Find the lowest index of a substring, or `-1` | `"hello".find("ll")` | `2` |
| `str.rfind()` | Find the highest index of a substring, or `-1` | `"hello hello".rfind("hello")` | `6` |
| `str.index()` | Like `find()`, but raises `ValueError` if not found | `"hello".index("ll")` | `2` |
| `str.rindex()` | Like `rfind()`, but raises `ValueError` if not found | `"hello hello".rindex("hello")` | `6` |
| `str.count()` | Count non-overlapping occurrences of a substring | `"banana".count("an")` | `2` |
| `str.startswith()` | Test whether the string starts with a prefix | `"hello".startswith("he")` | `True` |
| `str.endswith()` | Test whether the string ends with a suffix | `"hello".endswith("lo")` | `True` |
| `in` operator | Test whether a substring exists within the string | `"ll" in "hello"` | `True` |

### Detailed signatures

#### `str.find(sub[, start[, end]])`

```python
str.find(sub: str, start: int = 0, end: int = len(str)) -> int
```

Returns the lowest index in the string where substring `sub` is found within the slice `s[start:end]`. Returns `-1` if `sub` is not found.

```python
>>> "hello world".find("world")
6
>>> "hello world".find("python")
-1
>>> "hello world".find("o", 5)
7
```

#### `str.rfind(sub[, start[, end]])`

```python
str.rfind(sub: str, start: int = 0, end: int = len(str)) -> int
```

Returns the highest index in the string where substring `sub` is found within the slice `s[start:end]`. Returns `-1` if `sub` is not found.

```python
>>> "hello hello".rfind("hello")
6
>>> "hello hello".rfind("hello", 0, 5)
0
```

#### `str.index(sub[, start[, end]])`

```python
str.index(sub: str, start: int = 0, end: int = len(str)) -> int
```

Like `find()`, but raises a `ValueError` when the substring is not found.

```python
>>> "hello".index("ll")
2
>>> "hello".index("xyz")
ValueError: substring not found
```

#### `str.rindex(sub[, start[, end]])`

```python
str.rindex(sub: str, start: int = 0, end: int = len(str)) -> int
```

Like `rfind()`, but raises a `ValueError` when the substring is not found.

```python
>>> "hello hello".rindex("hello")
6
```

#### `str.count(sub[, start[, end]])`

```python
str.count(sub: str, start: int = 0, end: int = len(str)) -> int
```

Returns the number of non-overlapping occurrences of substring `sub` in the range `[start, end]`.

```python
>>> "banana".count("an")
2
>>> "aaa".count("aa")
1
```

#### `str.startswith(prefix[, start[, end]])`

```python
str.startswith(prefix: str | tuple[str, ...], start: int = 0, end: int = len(str)) -> bool
```

Returns `True` if the string starts with the specified `prefix`. The `prefix` can also be a tuple of prefixes to test for.

```python
>>> "hello".startswith("he")
True
>>> "hello".startswith(("he", "wo"))
True
>>> "hello".startswith("el", 1)
True
```

#### `str.endswith(suffix[, start[, end]])`

```python
str.endswith(suffix: str | tuple[str, ...], start: int = 0, end: int = len(str)) -> bool
```

Returns `True` if the string ends with the specified `suffix`. The `suffix` can also be a tuple of suffixes to test for.

```python
>>> "hello".endswith("lo")
True
>>> "hello".endswith((".py", ".txt", "lo"))
True
```

#### The `in` operator

```python
sub in s
```

The `in` operator is not a method but a membership test. It returns `True` if `sub` is found anywhere within `s`.

```python
>>> "world" in "hello world"
True
>>> "xyz" in "hello world"
False
```

---

## String testing

Methods that test the content of a string and return a boolean value. All of these methods return `False` for an empty string.

| Method | Description | Example | Result |
|---|---|---|---|
| `str.isalpha()` | All characters are alphabetic | `"hello".isalpha()` | `True` |
| `str.isdigit()` | All characters are digits | `"123".isdigit()` | `True` |
| `str.isalnum()` | All characters are alphanumeric | `"abc123".isalnum()` | `True` |
| `str.isspace()` | All characters are whitespace | `" \t\n".isspace()` | `True` |
| `str.isupper()` | All cased characters are uppercase | `"HELLO".isupper()` | `True` |
| `str.islower()` | All cased characters are lowercase | `"hello".islower()` | `True` |
| `str.istitle()` | String is in titlecase | `"Hello World".istitle()` | `True` |
| `str.isnumeric()` | All characters are numeric | `"½".isnumeric()` | `True` |
| `str.isdecimal()` | All characters are decimal | `"123".isdecimal()` | `True` |
| `str.isidentifier()` | String is a valid Python identifier | `"my_var".isidentifier()` | `True` |
| `str.isprintable()` | All characters are printable | `"hello".isprintable()` | `True` |
| `str.isascii()` | All characters are ASCII | `"hello".isascii()` | `True` |

### Detailed signatures

#### `str.isalpha()`

```python
str.isalpha() -> bool
```

Returns `True` if all characters in the string are alphabetic and there is at least one character. Alphabetic characters are those defined in the Unicode character database as "Letter".

```python
>>> "hello".isalpha()
True
>>> "hello123".isalpha()
False
>>> "café".isalpha()
True
```

#### `str.isdigit()`

```python
str.isdigit() -> bool
```

Returns `True` if all characters in the string are digits and there is at least one character. Digits include decimal characters and digits that need special handling, such as superscript digits.

```python
>>> "123".isdigit()
True
>>> "²".isdigit()
True
>>> "½".isdigit()
False
```

#### `str.isalnum()`

```python
str.isalnum() -> bool
```

Returns `True` if all characters in the string are alphanumeric (alphabetic or digit) and there is at least one character.

```python
>>> "abc123".isalnum()
True
>>> "abc 123".isalnum()
False
```

#### `str.isspace()`

```python
str.isspace() -> bool
```

Returns `True` if all characters in the string are whitespace characters and there is at least one character. Whitespace characters include space, tab, newline, carriage return, form feed, and vertical tab, among other Unicode whitespace characters.

```python
>>> " \t\n".isspace()
True
>>> "".isspace()
False
```

#### `str.isupper()`

```python
str.isupper() -> bool
```

Returns `True` if all cased characters in the string are uppercase and there is at least one cased character. Uncased characters (such as digits and punctuation) are ignored.

```python
>>> "HELLO 123".isupper()
True
>>> "Hello".isupper()
False
```

#### `str.islower()`

```python
str.islower() -> bool
```

Returns `True` if all cased characters in the string are lowercase and there is at least one cased character.

```python
>>> "hello 123".islower()
True
>>> "Hello".islower()
False
```

#### `str.istitle()`

```python
str.istitle() -> bool
```

Returns `True` if the string is titlecased: uppercase characters may only follow uncased characters, and lowercase characters may only follow cased characters.

```python
>>> "Hello World".istitle()
True
>>> "Hello world".istitle()
False
```

#### `str.isnumeric()`

```python
str.isnumeric() -> bool
```

Returns `True` if all characters in the string are numeric characters and there is at least one character. Numeric characters include digit characters and all characters that have the Unicode numeric value property, such as fractions and Roman numerals.

```python
>>> "123".isnumeric()
True
>>> "½".isnumeric()
True
>>> "Ⅳ".isnumeric()
True
```

#### `str.isdecimal()`

```python
str.isdecimal() -> bool
```

Returns `True` if all characters in the string are decimal characters and there is at least one character. Decimal characters are those that can be used to form numbers in base 10. This is a stricter test than `isdigit()`.

```python
>>> "123".isdecimal()
True
>>> "²".isdecimal()
False
```

#### `str.isidentifier()`

```python
str.isidentifier() -> bool
```

Returns `True` if the string is a valid identifier according to the Python language definition. Note that this does not check whether the string is a reserved keyword. Use `keyword.iskeyword()` to test for reserved identifiers.

```python
>>> "my_var".isidentifier()
True
>>> "2fast".isidentifier()
False
>>> "class".isidentifier()
True
```

#### `str.isprintable()`

```python
str.isprintable() -> bool
```

Returns `True` if all characters in the string are printable or the string is empty. Non-printable characters are those defined in the Unicode character database as "Other" or "Separator", with the exception of the ASCII space (`0x20`), which is considered printable.

```python
>>> "hello".isprintable()
True
>>> "hello\n".isprintable()
False
```

#### `str.isascii()`

```python
str.isascii() -> bool
```

Returns `True` if the string is empty or all characters in the string are ASCII (code points in the range U+0000 to U+007F).

```python
>>> "hello".isascii()
True
>>> "café".isascii()
False
>>> "".isascii()
True
```

---

## Transformation

Methods that return transformed copies of the string.

| Method | Description | Example | Result |
|---|---|---|---|
| `str.strip()` | Remove leading and trailing characters | `" hello ".strip()` | `"hello"` |
| `str.lstrip()` | Remove leading characters | `" hello ".lstrip()` | `"hello "` |
| `str.rstrip()` | Remove trailing characters | `" hello ".rstrip()` | `" hello"` |
| `str.replace()` | Replace occurrences of a substring | `"hello".replace("l", "r")` | `"herro"` |
| `str.translate()` | Translate characters using a mapping table | `"abc".translate({97: "A"})` | `"Abc"` |
| `str.maketrans()` | Create a translation table | `str.maketrans("abc", "ABC")` | (mapping) |
| `str.expandtabs()` | Replace tab characters with spaces | `"a\tb".expandtabs(4)` | `"a   b"` |
| `str.removeprefix()` | Remove a prefix if present | `"TestCase".removeprefix("Test")` | `"Case"` |
| `str.removesuffix()` | Remove a suffix if present | `"MixIn".removesuffix("In")` | `"Mix"` |

### Detailed signatures

#### `str.strip([chars])`

```python
str.strip(chars: str | None = None) -> str
```

Returns a copy of the string with leading and trailing characters removed. The `chars` argument is a string specifying the set of characters to remove. If omitted or `None`, whitespace characters are removed. The `chars` argument is not a prefix or suffix; rather, all combinations of its values are stripped.

```python
>>> " hello ".strip()
'hello'
>>> "www.example.com".strip("cmowz.")
'example'
```

#### `str.lstrip([chars])`

```python
str.lstrip(chars: str | None = None) -> str
```

Returns a copy of the string with leading characters removed. Behaves identically to `strip()`, but only removes characters from the left side.

```python
>>> " hello ".lstrip()
'hello '
>>> "###hello".lstrip("#")
'hello'
```

#### `str.rstrip([chars])`

```python
str.rstrip(chars: str | None = None) -> str
```

Returns a copy of the string with trailing characters removed. Behaves identically to `strip()`, but only removes characters from the right side.

```python
>>> " hello ".rstrip()
' hello'
>>> "hello!!!".rstrip("!")
'hello'
```

#### `str.replace(old, new[, count])`

```python
str.replace(old: str, new: str, count: int = -1) -> str
```

Returns a copy of the string with all occurrences of substring `old` replaced by `new`. If the optional argument `count` is given, only the first `count` occurrences are replaced.

```python
>>> "hello world".replace("world", "Python")
'hello Python'
>>> "aaa".replace("a", "b", 2)
'bba'
```

#### `str.translate(table)`

```python
str.translate(table: dict[int, str | int | None]) -> str
```

Returns a copy of the string in which each character has been mapped through the given translation table. The table must be a mapping of Unicode ordinals to Unicode ordinals, strings, or `None`. Characters mapped to `None` are deleted.

```python
>>> table = str.maketrans("aeiou", "AEIOU")
>>> "hello world".translate(table)
'hEllO wOrld'
```

#### `str.maketrans(x[, y[, z]])`

```python
# Single argument form
str.maketrans(mapping: dict[int | str, str | int | None]) -> dict[int, str | int | None]

# Two argument form
str.maketrans(from: str, to: str) -> dict[int, int]

# Three argument form
str.maketrans(from: str, to: str, delete: str) -> dict[int, int | None]
```

This is a static method that returns a translation table suitable for use with `str.translate()`.

With one argument, `mapping` must be a dictionary mapping Unicode ordinals or single characters to Unicode ordinals, strings, or `None`.

With two arguments, `from` and `to` must be strings of equal length, and each character in `from` will be mapped to the character at the same position in `to`.

With three arguments, each character in `delete` will be mapped to `None`.

```python
>>> table = str.maketrans("aeiou", "AEIOU", "xyz")
>>> "the fox".translate(table)
'thE fO'
```

#### `str.expandtabs(tabsize=8)`

```python
str.expandtabs(tabsize: int = 8) -> str
```

Returns a copy of the string where all tab characters are expanded using spaces. The column number is reset to zero at each newline. Tab positions occur every `tabsize` characters.

```python
>>> "01\t012\t0123\t01234".expandtabs(4)
'01  012 0123    01234'
```

#### `str.removeprefix(prefix)`

```python
str.removeprefix(prefix: str) -> str
```

If the string starts with the `prefix` string, returns `string[len(prefix):]`. Otherwise, returns a copy of the original string. Available since Python 3.9.

```python
>>> "TestHook".removeprefix("Test")
'Hook'
>>> "BaseTestCase".removeprefix("Test")
'BaseTestCase'
```

#### `str.removesuffix(suffix)`

```python
str.removesuffix(suffix: str) -> str
```

If the string ends with the `suffix` string and that suffix is not empty, returns `string[:-len(suffix)]`. Otherwise, returns a copy of the original string. Available since Python 3.9.

```python
>>> "MixIn".removesuffix("In")
'Mix'
>>> "Mixin".removesuffix("In")
'Mixin'
```

---

## Split and join

Methods for splitting strings into lists and joining lists into strings.

| Method | Description | Example | Result |
|---|---|---|---|
| `str.split()` | Split by separator (from left) | `"a,b,c".split(",")` | `["a", "b", "c"]` |
| `str.rsplit()` | Split by separator (from right) | `"a,b,c".rsplit(",", 1)` | `["a,b", "c"]` |
| `str.splitlines()` | Split by line boundaries | `"a\nb\n".splitlines()` | `["a", "b"]` |
| `str.partition()` | Split into three parts at first separator | `"a:b:c".partition(":")` | `("a", ":", "b:c")` |
| `str.rpartition()` | Split into three parts at last separator | `"a:b:c".rpartition(":")` | `("a:b", ":", "c")` |
| `str.join()` | Join an iterable with the string as separator | `",".join(["a", "b"])` | `"a,b"` |

### Detailed signatures

#### `str.split(sep=None, maxsplit=-1)`

```python
str.split(sep: str | None = None, maxsplit: int = -1) -> list[str]
```

Returns a list of the words in the string, using `sep` as the delimiter. If `maxsplit` is given, at most `maxsplit` splits are done (resulting in at most `maxsplit + 1` elements).

When `sep` is `None` or not specified, any whitespace string is a separator, and empty strings are removed from the result. Consecutive whitespace is treated as a single separator. When `sep` is specified, consecutive delimiters are not grouped together and produce empty strings.

```python
>>> "hello world".split()
['hello', 'world']
>>> "  hello  world  ".split()
['hello', 'world']
>>> "a,,b,,c".split(",")
['a', '', 'b', '', 'c']
>>> "a,b,c,d".split(",", 2)
['a', 'b', 'c,d']
```

#### `str.rsplit(sep=None, maxsplit=-1)`

```python
str.rsplit(sep: str | None = None, maxsplit: int = -1) -> list[str]
```

Behaves identically to `split()`, except that splits are performed from the right. This only makes a difference when `maxsplit` is specified.

```python
>>> "a,b,c,d".rsplit(",", 2)
['a,b', 'c', 'd']
>>> "a,b,c,d".split(",", 2)
['a', 'b', 'c,d']
```

#### `str.splitlines(keepends=False)`

```python
str.splitlines(keepends: bool = False) -> list[str]
```

Returns a list of the lines in the string, breaking at line boundaries. Line breaks are not included in the resulting list unless `keepends` is `True`. This method recognises a variety of line boundary representations, including `\n`, `\r\n`, `\r`, `\v`, `\f`, `\x1c`, `\x1d`, `\x1e`, `\x85`, `\u2028`, and `\u2029`.

```python
>>> "hello\nworld\n".splitlines()
['hello', 'world']
>>> "hello\nworld\n".splitlines(True)
['hello\n', 'world\n']
>>> "hello\r\nworld".splitlines()
['hello', 'world']
```

#### `str.partition(sep)`

```python
str.partition(sep: str) -> tuple[str, str, str]
```

Splits the string at the first occurrence of `sep` and returns a 3-tuple containing the part before the separator, the separator itself, and the part after the separator. If the separator is not found, returns a 3-tuple containing the original string and two empty strings.

```python
>>> "user@example.com".partition("@")
('user', '@', 'example.com')
>>> "hello".partition("@")
('hello', '', '')
```

#### `str.rpartition(sep)`

```python
str.rpartition(sep: str) -> tuple[str, str, str]
```

Splits the string at the last occurrence of `sep` and returns a 3-tuple. If the separator is not found, returns a 3-tuple containing two empty strings followed by the original string.

```python
>>> "path/to/file.txt".rpartition("/")
('path/to', '/', 'file.txt')
>>> "hello".rpartition("/")
('', '', 'hello')
```

#### `str.join(iterable)`

```python
str.join(iterable: Iterable[str]) -> str
```

Returns a string which is the concatenation of the strings in `iterable`. The string on which `join()` is called serves as the separator between elements. A `TypeError` is raised if any value in the iterable is not a string.

```python
>>> ",".join(["apple", "banana", "cherry"])
'apple,banana,cherry'
>>> " ".join(["hello", "world"])
'hello world'
>>> "\n".join(["line 1", "line 2", "line 3"])
'line 1\nline 2\nline 3'
```

---

## Alignment and padding

Methods for aligning and padding strings to a specified width.

| Method | Description | Example | Result |
|---|---|---|---|
| `str.center()` | Centre the string within a given width | `"hi".center(10)` | `"    hi    "` |
| `str.ljust()` | Left-justify the string within a given width | `"hi".ljust(10)` | `"hi        "` |
| `str.rjust()` | Right-justify the string within a given width | `"hi".rjust(10)` | `"        hi"` |
| `str.zfill()` | Pad with zeros on the left to fill a given width | `"42".zfill(5)` | `"00042"` |

### Detailed signatures

#### `str.center(width[, fillchar])`

```python
str.center(width: int, fillchar: str = " ") -> str
```

Returns the string centred within a string of length `width`. Padding is done using the specified fill character (default is an ASCII space). The original string is returned if `width` is less than or equal to `len(s)`.

```python
>>> "hello".center(11)
'   hello   '
>>> "hello".center(11, "-")
'---hello---'
```

#### `str.ljust(width[, fillchar])`

```python
str.ljust(width: int, fillchar: str = " ") -> str
```

Returns the string left-justified within a string of length `width`. Padding is done using the specified fill character.

```python
>>> "hello".ljust(10)
'hello     '
>>> "hello".ljust(10, ".")
'hello.....'
```

#### `str.rjust(width[, fillchar])`

```python
str.rjust(width: int, fillchar: str = " ") -> str
```

Returns the string right-justified within a string of length `width`. Padding is done using the specified fill character.

```python
>>> "hello".rjust(10)
'     hello'
>>> "hello".rjust(10, ".")
'.....hello'
```

#### `str.zfill(width)`

```python
str.zfill(width: int) -> str
```

Returns a copy of the string left-filled with ASCII `0` digits to make a string of length `width`. A leading sign prefix (`+` or `-`) is handled by inserting the padding after the sign character rather than before. The original string is returned if `width` is less than or equal to `len(s)`.

```python
>>> "42".zfill(5)
'00042'
>>> "-42".zfill(5)
'-0042'
>>> "+42".zfill(5)
'+0042'
```

---

## Encoding

Methods related to encoding strings as bytes.

| Method | Description | Example | Result |
|---|---|---|---|
| `str.encode()` | Encode the string to bytes | `"hello".encode("utf-8")` | `b"hello"` |

### Detailed signatures

#### `str.encode(encoding="utf-8", errors="strict")`

```python
str.encode(encoding: str = "utf-8", errors: str = "strict") -> bytes
```

Returns the string encoded as a `bytes` object using the specified encoding. The `errors` argument specifies the error handling scheme. The default value of `"strict"` causes a `UnicodeEncodeError` to be raised on encoding failures. Other permitted values include `"ignore"`, `"replace"`, `"xmlcharrefreplace"`, `"backslashreplace"`, and any other name registered via `codecs.register_error()`.

```python
>>> "hello".encode()
b'hello'
>>> "café".encode("utf-8")
b'caf\xc3\xa9'
>>> "café".encode("ascii", errors="replace")
b'caf?'
>>> "café".encode("ascii", errors="ignore")
b'caf'
```

---

## See also

- [Python `str` type documentation](https://docs.python.org/3/library/stdtypes.html#string-methods) -- official reference for all string methods
- [String formatting reference](string-formatting-reference.md) -- f-strings, `str.format()`, and the format specification mini-language
- [String constants reference](string-constants-reference.md) -- constants from the `string` module
- [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html) -- working with Unicode in Python
- [Text Sequence Type](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) -- the `str` type itself, including indexing, slicing, and common operations
