# Understanding Unicode and encodings

Every time you type a character on your keyboard, something remarkable happens behind the scenes. Your computer &ndash; which fundamentally understands nothing but numbers &ndash; must somehow represent the letter "A", the digit "7", the emoji "😊", and the Chinese character "中" as sequences of ones and zeros. How it does this, and why it matters to you as a Python programmer, is the subject of this article.

## A brief history

In the early days of computing, the **ASCII** standard assigned numbers to 128 characters: the English alphabet (uppercase and lowercase), digits, punctuation, and a handful of control characters. ASCII worked well for English text, but it left no room for the accented characters used in French, the umlauts in German, or the thousands of characters in Chinese, Japanese, and Korean.

The solution &ndash; or rather, the many competing solutions &ndash; was a proliferation of **code pages**. Each code page extended ASCII with additional characters for a specific language or region. A file written using one code page would display as garbled nonsense when opened with another. This was the encoding chaos of the 1980s and 1990s.

**Unicode** was created to end this chaos. It is a universal character set that assigns a unique number, called a **code point**, to every character in every writing system &ndash; plus mathematical symbols, musical notation, and yes, emoji. As of 2024, Unicode defines over 149,000 characters.

## What Unicode is (and is not)

A common misconception is that Unicode is an encoding. It is not. Unicode is a **catalogue** -- a mapping from characters to numbers. The letter "A" is assigned code point U+0041. The pound sign "£" is U+00A3. The snowman "☃" is U+2603.

But a code point is just a number. To store or transmit that number, you need an **encoding** -- a set of rules for converting code points into bytes.

## What UTF-8 is

**UTF-8** is the most widely used encoding for Unicode text. It is a variable-length encoding, meaning that different characters use different numbers of bytes:

- ASCII characters (U+0000 to U+007F) use 1 byte
- Characters from U+0080 to U+07FF use 2 bytes
- Characters from U+0800 to U+FFFF use 3 bytes
- Characters from U+10000 to U+10FFFF use 4 bytes

UTF-8 won the encoding war for several reasons:

- **Backwards compatible with ASCII:** Any valid ASCII text is also valid UTF-8. This made adoption painless.
- **Efficient for English text:** Since ASCII characters use only 1 byte, English text in UTF-8 is the same size as in ASCII.
- **Self-synchronising:** You can jump into the middle of a UTF-8 byte stream and find the start of the next character without reading from the beginning.

## Strings and bytes in Python

In Python, there are two distinct types for representing text and raw binary data:

- **`str`** holds Unicode text. Each element is a character.
- **`bytes`** holds raw byte sequences. Each element is an integer from 0 to 255.

The `str.encode()` method converts text to bytes, and the `bytes.decode()` method converts bytes back to text.

```python
# Text to bytes
text = "café"
encoded = text.encode("utf-8")
print(encoded)        # b'caf\xc3\xa9'
print(type(encoded))  # <class 'bytes'>

# Bytes to text
decoded = encoded.decode("utf-8")
print(decoded)        # café
print(type(decoded))  # <class 'str'>
```

Notice that the "é" character, which is outside the ASCII range, takes 2 bytes (`\xc3\xa9`) in UTF-8.

```
Text (str):     c    a    f    é
                |    |    |    |
Code points:   U+63 U+61 U+66 U+E9
                |    |    |    |
UTF-8 bytes:   0x63 0x61 0x66 0xC3 0xA9
```

## The encoding trap

One of the most common sources of errors in Python programs is opening a file without specifying the encoding. On some systems, the default encoding is not UTF-8, which can lead to `UnicodeDecodeError` when reading files that contain non-ASCII characters.

```python
# This may fail on some systems if the file contains non-ASCII characters
# with open("data.txt") as f:
#     content = f.read()

# Always specify the encoding explicitly
with open("data.txt", encoding="utf-8") as f:
    content = f.read()
```

When you encounter a `UnicodeDecodeError`, it usually means one of two things:

1. The file is not encoded in the encoding you specified. Try a different encoding.
2. The file contains corrupted or mixed-encoding data. Use `errors="replace"` or `errors="ignore"` as a last resort.

```python
# Replace undecodable bytes with a replacement character
with open("data.txt", encoding="utf-8", errors="replace") as f:
    content = f.read()
```

## Practical guidelines

Working with Unicode in Python is straightforward if you follow a few simple rules:

- **Always specify `encoding="utf-8"`** when opening files. Do not rely on the system default.
- **Use `str` for text and `bytes` for binary data.** Do not mix them. If you find yourself calling `encode()` and `decode()` frequently, reconsider your data flow.
- **Be explicit about encoding at system boundaries.** Whenever data enters or leaves your program &ndash; through files, network connections, or command-line arguments &ndash; specify the encoding.
- **Use `errors="replace"` or `errors="ignore"` as last resorts.** These options silently lose data. Prefer fixing the root cause instead.
- **Test with international text.** If your code only works with ASCII characters, it will eventually fail in production. Include characters like "é", "ñ", "中", and "😊" in your test data.

## Summary

The key insight is that **text and bytes are fundamentally different things**. Text is a sequence of characters with meaning. Bytes are a sequence of numbers. Encoding is the bridge between them &ndash; the process of converting characters to bytes for storage or transmission, and decoding is the reverse.

Python makes this distinction explicit with the `str` and `bytes` types. By always specifying your encoding (usually UTF-8) and keeping text and bytes separate, you can work confidently with international text and avoid the encoding errors that plague many programs.
