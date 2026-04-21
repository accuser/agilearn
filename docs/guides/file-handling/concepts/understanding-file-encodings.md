# Understanding file encodings

## What is an encoding?

Computers store numbers, not letters. An encoding is the mapping between numbers and characters -- a codebook that tells the computer which number corresponds to which letter.

When you save a text file, the characters you typed are converted into a sequence of bytes (numbers between 0 and 255) using an encoding. When you open the file later, those bytes are converted back into characters using the same encoding. If you read the file with a different encoding than the one used to write it, you get garbled text -- sometimes called "mojibake."

## A brief history of character encodings

### ASCII

ASCII (American Standard Code for Information Interchange) was created in the 1960s. It defines 128 characters using 7 bits per character, covering English letters (uppercase and lowercase), digits, punctuation, and some control characters.

The limitation is obvious: ASCII only covers English. Characters from other languages -- accented letters, Cyrillic, Chinese, Arabic, and so on -- are not represented.

### Extended ASCII and code pages

To support more characters, various organisations created extensions to ASCII. Latin-1 (ISO 8859-1) added characters for Western European languages, while other "code pages" covered Eastern European, Greek, Arabic, and other scripts.

The fundamental problem was that different systems used different extensions. A file written on one system might display incorrectly on another, because the same byte value mapped to different characters in different code pages.

### Unicode

Unicode was created to solve this problem once and for all. It assigns a unique number (called a "code point") to every character in every writing system. As of 2024, Unicode covers over 150,000 characters from virtually all human languages, plus mathematical symbols, emoji, and more.

Unicode defines *which* characters exist and *what number* each one has. But it does not define how those numbers are stored as bytes -- that is the job of a Unicode encoding.

### UTF-8

UTF-8 is the most widely used Unicode encoding. It has several properties that make it the default choice for most applications:

- **Variable-length.** It uses 1 to 4 bytes per character. ASCII characters use just one byte, making UTF-8 very efficient for English text.
- **Backwards compatible with ASCII.** Any valid ASCII file is also a valid UTF-8 file with the same content.
- **Self-synchronising.** You can find the start of any character without reading from the beginning of the file.
- **Universal.** It can represent every Unicode character.

UTF-8 is used by the vast majority of web pages, APIs, and modern applications. It is the recommended encoding for Python file handling.

## Why encoding matters in Python

### The platform default problem

When you call `open("file.txt", "r")` without specifying an encoding, Python uses the platform default encoding. This can be:

- **UTF-8** on Linux and macOS (in most configurations)
- **cp1252** or another locale-specific encoding on Windows

This means code that works perfectly on one platform may produce errors or garbled text on another. Consider this example:

```python
# This code is not portable!
with open("file.txt", "r") as f:
    content = f.read()
```

If the file contains non-ASCII characters (such as accented letters or emoji), this code may work on Linux but fail on Windows, or vice versa.

### The solution: always specify encoding

```python
# This code works consistently on all platforms
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

By specifying `encoding="utf-8"` explicitly, you ensure your code behaves the same way regardless of the platform it runs on.

Note that Python 3.15 will make UTF-8 the default encoding. However, specifying it explicitly is still good practice for clarity and for compatibility with earlier versions of Python.

## Common encodings

| Encoding | Description | Common use |
|----------|-------------|------------|
| `utf-8` | Unicode, variable-length (1--4 bytes) | The recommended default for all new files |
| `ascii` | English characters only (128 characters) | Legacy systems, simple data |
| `latin-1` (or `iso-8859-1`) | Western European characters (256 characters) | Older web pages, legacy systems |
| `utf-16` | Unicode, 2 or 4 bytes per character | Some Windows APIs, some XML files |
| `utf-32` | Unicode, 4 bytes per character | Internal processing (rarely used for files) |
| `cp1252` | Windows Western European | Windows default in many Western locales |

## Handling encoding errors

When Python encounters bytes that cannot be decoded (or characters that cannot be encoded) with the specified encoding, it raises an error by default. The `errors` parameter in `open()` lets you control this behaviour.

### Error handling strategies

| Strategy | Description |
|----------|-------------|
| `"strict"` (default) | Raise `UnicodeDecodeError` or `UnicodeEncodeError` |
| `"ignore"` | Silently skip characters that cannot be decoded or encoded |
| `"replace"` | Replace problem characters with `?` (encoding) or `\ufffd` (decoding) |
| `"backslashreplace"` | Replace with Python backslash escape sequences |
| `"xmlcharrefreplace"` | Replace with XML character references (encoding only) |

```python
# Strict (default) -- raises an error for non-ASCII bytes
with open("data.txt", "r", encoding="ascii", errors="strict") as f:
    content = f.read()  # UnicodeDecodeError if non-ASCII found

# Replace -- substitutes problem characters
with open("data.txt", "r", encoding="ascii", errors="replace") as f:
    content = f.read()  # non-ASCII bytes become the replacement character
```

The `"replace"` strategy is useful when you need to read a file but can tolerate some loss of information. The `"strict"` strategy is better when data integrity is critical and you want to know immediately if there is an encoding problem.

## Detecting the encoding of a file

There is no reliable way to detect the encoding of a file automatically. A sequence of bytes can be valid in multiple encodings, and without additional information, Python cannot know which one was intended.

Some approaches to determining the encoding include the following:

- **Check for a BOM** (byte order mark) at the start of the file -- see the next section
- **Use third-party libraries** such as `chardet` or `charset-normalizer`, which analyse byte patterns to make an educated guess
- **Know the encoding in advance** from documentation, file format standards, or conventions -- this is the most reliable approach

## The byte order mark (BOM)

Some files include a byte order mark (BOM) at the very beginning. This is a special sequence of bytes that hints at the encoding:

| Encoding | BOM bytes |
|----------|-----------|
| UTF-8 | `\xef\xbb\xbf` |
| UTF-16 (little-endian) | `\xff\xfe` |
| UTF-16 (big-endian) | `\xfe\xff` |

UTF-8 files do not require a BOM, but some applications (notably Microsoft Excel) add one. To handle UTF-8 files that may or may not have a BOM, use the `"utf-8-sig"` encoding:

```python
with open("bom-file.txt", "r", encoding="utf-8-sig") as f:
    content = f.read()
```

The `"utf-8-sig"` encoding strips the BOM if present and reads normally if it is not.

## Practical tips

1. **Always use UTF-8 as your default encoding.** It covers all Unicode characters and is the most widely supported encoding.
2. **Always specify encoding explicitly when opening files.** Do not rely on the platform default.
3. **Be especially careful with files from other systems.** Files created on Windows may use `cp1252`, files from older systems may use `latin-1`, and files from East Asian systems may use encodings such as `shift_jis` or `gb2312`.
4. **Test with non-ASCII characters during development.** Include accented letters, emoji, or characters from other scripts in your test data.
5. **Use `errors="replace"` when you need to read files with unknown or mixed encodings gracefully.** This prevents crashes at the cost of some data loss.
6. **When writing files that others will read, document the encoding used.** This saves everyone time and frustration.

## Summary

Encoding is one of those concepts that seems invisible until something goes wrong. A file that looks perfect on your machine may display as gibberish on someone else's, or your program may crash with a mysterious `UnicodeDecodeError`.

By understanding how encodings work and always specifying `encoding="utf-8"` explicitly, you can avoid a whole class of subtle bugs. The rule is simple: every time you open a text file, specify the encoding.

## See also

- [`open()` function reference](../reference/open-function-reference.md)
- [Official Python documentation on text encoding](https://docs.python.org/3/library/codecs.html)
