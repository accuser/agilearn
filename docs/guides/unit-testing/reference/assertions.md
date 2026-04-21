# unittest assertions reference

A comprehensive reference guide to assertion methods in Python's `unittest` module.

## Contents

- [Overview](#overview)
- [Basic equality assertions](#basic-equality-assertions)
- [Boolean assertions](#boolean-assertions)
- [Membership and container assertions](#membership-and-container-assertions)
- [Numeric assertions](#numeric-assertions)
- [String assertions](#string-assertions)
- [Exception assertions](#exception-assertions)
- [Collection assertions](#collection-assertions)
- [Custom messages](#custom-messages)
- [Choosing the right assertion](#choosing-the-right-assertion)
- [Next steps](#next-steps)

## Overview

Assertions are the foundation of unit testing. They check that your code produces the expected results and report failures with clear, informative messages when expectations aren't met.

All assertion methods are provided by the `unittest.TestCase` class. To use them, your test class must inherit from `TestCase`:

```python
import unittest

class TestExample(unittest.TestCase):
    def test_something(self):
        self.assertEqual(1 + 1, 2)  # ✅ Pass
```

### General principles

- Use the most **specific assertion** available for better error messages
- Assertions stop test execution on first failure (subsequent assertions won't run)
- All assertions accept an optional `msg` parameter for custom failure messages
- Assertion names use `camelCase` to match `unittest` conventions

## Basic equality assertions

### `assertEqual(a, b)`

**Signature:** `assertEqual(first, second, msg=None)`

**Description:** Tests that `a == b`.

**Example:**

```python
def test_addition(self):
    result = 2 + 3
    self.assertEqual(result, 5)
```

**When to use:** For comparing values where `==` comparison makes sense (numbers, strings, lists, dictionaries).

**Common pitfalls:**
- Don't use for floating-point numbers (use `assertAlmostEqual` instead)
- Don't use for checking object identity (use `assertIs` instead)

**Failure message:**
```
AssertionError: 6 != 5
```

---

### `assertNotEqual(a, b)`

**Signature:** `assertNotEqual(first, second, msg=None)`

**Description:** Tests that `a != b`.

**Example:**

```python
def test_different_values(self):
    result = calculate_random()
    self.assertNotEqual(result, 0)  # Ensure result is not zero
```

**When to use:** When you need to verify two values are different.

**Common pitfalls:**
- Less commonly used than `assertEqual`
- Consider if there's a more specific assertion for what you're testing

---

### `assertIs(a, b)`

**Signature:** `assertIs(expr1, expr2, msg=None)`

**Description:** Tests that `a is b` (object identity, not equality).

**Example:**

```python
def test_singleton_pattern(self):
    instance1 = get_database_connection()
    instance2 = get_database_connection()
    self.assertIs(instance1, instance2)  # Same object
```

**When to use:** When you need to verify two references point to the **same object** in memory.

**Common pitfalls:**
- Don't confuse with `assertEqual` – `is` checks identity, `==` checks equality
- Two lists with identical contents are equal (`==`) but not the same object (`is`)

**Understanding `==` vs `is`:**

```python
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = list1

list1 == list2  # True (equal values)
list1 is list2  # False (different objects)
list1 is list3  # True (same object)
```

---

### `assertIsNot(a, b)`

**Signature:** `assertIsNot(expr1, expr2, msg=None)`

**Description:** Tests that `a is not b` (different objects).

**Example:**

```python
def test_creates_new_instance(self):
    obj1 = create_object()
    obj2 = create_object()
    self.assertIsNot(obj1, obj2)  # Different objects
```

**When to use:** When you need to verify two references point to **different objects**.

## Boolean assertions

### `assertTrue(x)`

**Signature:** `assertTrue(expr, msg=None)`

**Description:** Tests that `bool(x) is True`.

**Example:**

```python
def test_validation_passes(self):
    result = validate_email("user@example.com")
    self.assertTrue(result)
```

**When to use:** When you're checking if something is truthy (True, non-empty, non-zero).

**Common pitfalls:**
- Less specific than other assertions – consider `assertEqual(x, True)` if you need to verify exactly `True`
- Remember that many values are truthy (non-empty strings, non-zero numbers, non-empty containers)

---

### `assertFalse(x)`

**Signature:** `assertFalse(expr, msg=None)`

**Description:** Tests that `bool(x) is False`.

**Example:**

```python
def test_validation_fails(self):
    result = validate_email("invalid-email")
    self.assertFalse(result)
```

**When to use:** When you're checking if something is falsy (False, empty, zero, None).

**Common pitfalls:**
- Many values are falsy: `False`, `None`, `0`, `""`, `[]`, `{}`
- Use `assertIsNone` if you specifically want to check for `None`

---

### `assertIsNone(x)`

**Signature:** `assertIsNone(expr, msg=None)`

**Description:** Tests that `x is None`.

**Example:**

```python
def test_not_found_returns_none(self):
    result = find_user("nonexistent")
    self.assertIsNone(result)
```

**When to use:** When you specifically want to check for `None` (common for functions that return `None` on failure).

**Common pitfalls:**
- More specific than `assertFalse` – use this when you specifically expect `None`

**Failure message:**
```
AssertionError: <object> is not None
```

---

### `assertIsNotNone(x)`

**Signature:** `assertIsNotNone(expr, msg=None)`

**Description:** Tests that `x is not None`.

**Example:**

```python
def test_user_found(self):
    result = find_user("alice")
    self.assertIsNotNone(result)
```

**When to use:** When you want to verify something is not `None` before using it.

## Membership and container assertions

### `assertIn(a, b)`

**Signature:** `assertIn(member, container, msg=None)`

**Description:** Tests that `a in b`.

**Example:**

```python
def test_item_in_list(self):
    fruits = ["apple", "banana", "cherry"]
    self.assertIn("banana", fruits)

def test_substring_in_string(self):
    text = "Hello, world!"
    self.assertIn("world", text)

def test_key_in_dict(self):
    user = {"name": "Alice", "age": 30}
    self.assertIn("name", user)
```

**When to use:** For checking membership in sequences, strings, dictionaries (checks keys), or sets.

**Common pitfalls:**
- For dictionaries, checks keys (not values)
- Case-sensitive for strings

---

### `assertNotIn(a, b)`

**Signature:** `assertNotIn(member, container, msg=None)`

**Description:** Tests that `a not in b`.

**Example:**

```python
def test_no_banned_words(self):
    comment = "This is a nice post"
    self.assertNotIn("spam", comment.lower())
```

**When to use:** For verifying something is absent from a container.

---

### `assertIsInstance(obj, cls)`

**Signature:** `assertIsInstance(obj, cls, msg=None)`

**Description:** Tests that `isinstance(obj, cls)` is `True`.

**Example:**

```python
def test_returns_correct_type(self):
    result = calculate_total([10, 20, 30])
    self.assertIsInstance(result, int)

def test_accepts_multiple_types(self):
    value = get_value()
    self.assertIsInstance(value, (int, float))  # Either int or float
```

**When to use:** For type checking in tests, especially when testing functions that should return specific types.

**Common pitfalls:**
- Can check multiple types using a tuple: `(int, float, str)`
- Subclasses pass the test (if `obj` is a subclass of `cls`)

---

### `assertNotIsInstance(obj, cls)`

**Signature:** `assertNotIsInstance(obj, cls, msg=None)`

**Description:** Tests that `isinstance(obj, cls)` is `False`.

**Example:**

```python
def test_sanitizes_input(self):
    result = sanitize_input("<script>alert('XSS')</script>")
    self.assertNotIsInstance(result, bytes)  # Should be string
```

**When to use:** Less common, but useful when you want to ensure a value is not a particular type.

## Numeric assertions

### `assertGreater(a, b)`

**Signature:** `assertGreater(a, b, msg=None)`

**Description:** Tests that `a > b`.

**Example:**

```python
def test_positive_result(self):
    result = calculate_profit(revenue=100, costs=60)
    self.assertGreater(result, 0)
```

**When to use:** When you need to verify a value exceeds a threshold.

---

### `assertGreaterEqual(a, b)`

**Signature:** `assertGreaterEqual(a, b, msg=None)`

**Description:** Tests that `a >= b`.

**Example:**

```python
def test_minimum_score(self):
    score = calculate_score(answers)
    self.assertGreaterEqual(score, 50)  # Must score at least 50
```

**When to use:** When you need to verify a value meets or exceeds a minimum.

---

### `assertLess(a, b)`

**Signature:** `assertLess(a, b, msg=None)`

**Description:** Tests that `a < b`.

**Example:**

```python
def test_within_limit(self):
    file_size = get_file_size("document.pdf")
    self.assertLess(file_size, 10_000_000)  # Less than 10MB
```

**When to use:** When you need to verify a value is below a maximum.

---

### `assertLessEqual(a, b)`

**Signature:** `assertLessEqual(a, b, msg=None)`

**Description:** Tests that `a <= b`.

**Example:**

```python
def test_response_time(self):
    response_time = measure_api_call()
    self.assertLessEqual(response_time, 1.0)  # 1 second or less
```

**When to use:** When you need to verify a value doesn't exceed a maximum.

---

### `assertAlmostEqual(a, b, places=7)`

**Signature:** `assertAlmostEqual(first, second, places=7, msg=None, delta=None)`

**Description:** Tests that `round(a-b, places) == 0`. For floating-point comparisons.

**Example:**

```python
def test_floating_point_calculation(self):
    result = 0.1 + 0.2
    self.assertAlmostEqual(result, 0.3, places=7)

def test_with_delta(self):
    result = measure_temperature()
    self.assertAlmostEqual(result, 20.0, delta=0.5)  # Within ±0.5
```

**When to use:** **Always use this for floating-point comparisons** instead of `assertEqual`.

**Parameters:**
- `places`: Number of decimal places to check (default: 7)
- `delta`: Absolute tolerance (alternative to `places`)

**Why this matters:**

```python
0.1 + 0.2 == 0.3  # False! (0.30000000000000004)
```

Floating-point arithmetic has rounding errors. Use `assertAlmostEqual` to handle this.

**Common pitfalls:**
- Forgetting to use this for floats and using `assertEqual` instead
- Using `delta` when you need it for physical measurements (temperatures, distances)

---

### `assertNotAlmostEqual(a, b, places=7)`

**Signature:** `assertNotAlmostEqual(first, second, places=7, msg=None, delta=None)`

**Description:** Tests that `round(a-b, places) != 0`.

**Example:**

```python
def test_values_significantly_different(self):
    result1 = calculate_with_method_a()
    result2 = calculate_with_method_b()
    self.assertNotAlmostEqual(result1, result2, places=2)
```

**When to use:** Rarely needed, but useful when you want to ensure two floating-point values are sufficiently different.

## String assertions

### `assertRegex(text, regex)`

**Signature:** `assertRegex(text, regex, msg=None)`

**Description:** Tests that `regex` matches `text`.

**Example:**

```python
import re

def test_email_format(self):
    email = generate_email("alice")
    self.assertRegex(email, r'^[\w\.-]+@[\w\.-]+\.\w+$')

def test_log_message_format(self):
    log = get_log_entry()
    self.assertRegex(log, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
```

**When to use:** When you need to verify a string matches a pattern (email addresses, dates, log formats, etc.).

**Common pitfalls:**
- Remember to use raw strings (`r'...'`) for regex patterns
- Test your regex pattern separately to ensure it's correct

---

### `assertNotRegex(text, regex)`

**Signature:** `assertNotRegex(text, regex, msg=None)`

**Description:** Tests that `regex` does not match `text`.

**Example:**

```python
def test_no_special_characters(self):
    username = sanitize_username("alice123")
    self.assertNotRegex(username, r'[^\w]')  # No non-alphanumeric
```

**When to use:** When you need to verify a string doesn't contain certain patterns.

---

### `assertMultiLineEqual(a, b)`

**Signature:** `assertMultiLineEqual(first, second, msg=None)`

**Description:** Tests that multi-line strings are equal. Provides detailed diff output on failure.

**Example:**

```python
def test_generated_config(self):
    config = generate_config()
    expected = """
[database]
host = localhost
port = 5432
    """.strip()
    self.assertMultiLineEqual(config, expected)
```

**When to use:** When comparing multi-line strings (configuration files, generated code, templates).

**Why use this:** Provides a clear, line-by-line diff when strings don't match, making it much easier to spot differences.

**Failure message:**
```
AssertionError: 'line 1\nline 2\nline 3' != 'line 1\nline 2\nline 4'
- line 3
+ line 4
```

## Exception assertions

### `assertRaises(exception)`

**Signature:** `assertRaises(exception, callable, *args, **kwargs)`

**Description:** Tests that `callable(*args, **kwargs)` raises `exception`.

**Example (callable form):**

```python
def test_division_by_zero(self):
    self.assertRaises(ZeroDivisionError, divide, 10, 0)
```

**Example (context manager form):**

```python
def test_invalid_input(self):
    with self.assertRaises(ValueError):
        parse_age("-5")
```

**Example (accessing exception details):**

```python
def test_exception_message(self):
    with self.assertRaises(ValueError) as cm:
        parse_age("-5")

    self.assertEqual(str(cm.exception), "Age must be positive")
```

**When to use:** When testing that your code properly raises exceptions for invalid inputs or error conditions.

**Which form to use:**
- **Context manager (`with`)**: More flexible, allows additional assertions about the exception
- **Callable form**: More concise for simple cases

**Common pitfalls:**
- Don't wrap the assertion in a try/except – let `assertRaises` handle it
- Remember that the test fails if the exception is **not** raised

---

### `assertRaisesRegex(exception, regex)`

**Signature:** `assertRaisesRegex(exception, regex, callable, *args, **kwargs)`

**Description:** Like `assertRaises`, but also checks that the exception message matches `regex`.

**Example:**

```python
def test_error_message_format(self):
    with self.assertRaisesRegex(ValueError, r'Age must be between \d+ and \d+'):
        validate_age(150)
```

**When to use:** When you want to verify both the exception type **and** that the message contains specific information.

---

### `assertWarns(warning)`

**Signature:** `assertWarns(warning, callable, *args, **kwargs)`

**Description:** Tests that `callable(*args, **kwargs)` triggers `warning`.

**Example:**

```python
import warnings

def test_deprecation_warning(self):
    with self.assertWarns(DeprecationWarning):
        old_function()
```

**When to use:** When testing that your code properly issues warnings (deprecation warnings, user warnings, etc.).

## Collection assertions

### `assertCountEqual(a, b)`

**Signature:** `assertCountEqual(first, second, msg=None)`

**Description:** Tests that sequences contain the same elements, **regardless of order**.

**Example:**

```python
def test_same_elements_different_order(self):
    result = get_user_permissions("alice")
    expected = ["read", "write", "delete"]
    self.assertCountEqual(result, expected)  # Order doesn't matter
```

**When to use:** When you care about the **contents** of a sequence but not the **order**.

**Common pitfalls:**
- Name is confusing (doesn't count, checks contents)
- Previously called `assertItemsEqual` in Python 2

---

### `assertListEqual(a, b)`

**Signature:** `assertListEqual(list1, list2, msg=None)`

**Description:** Tests that two lists are equal. Provides detailed diff on failure.

**Example:**

```python
def test_sorted_results(self):
    results = sort_items([3, 1, 2])
    self.assertListEqual(results, [1, 2, 3])
```

**When to use:** When you specifically want to compare lists (not just any sequences).

**Why use this:** Provides a better error message than `assertEqual` when comparing lists.

---

### `assertTupleEqual(a, b)`

**Signature:** `assertTupleEqual(tuple1, tuple2, msg=None)`

**Description:** Tests that two tuples are equal.

**Example:**

```python
def test_coordinates(self):
    point = get_location()
    self.assertTupleEqual(point, (51.5074, -0.1278))  # London
```

**When to use:** When comparing tuples specifically.

---

### `assertSetEqual(a, b)`

**Signature:** `assertSetEqual(set1, set2, msg=None)`

**Description:** Tests that two sets are equal.

**Example:**

```python
def test_unique_values(self):
    tags = extract_tags("python testing unittest")
    self.assertSetEqual(tags, {"python", "testing", "unittest"})
```

**When to use:** When comparing sets (order never matters for sets).

---

### `assertDictEqual(a, b)`

**Signature:** `assertDictEqual(d1, d2, msg=None)`

**Description:** Tests that two dictionaries are equal. Provides detailed diff on failure.

**Example:**

```python
def test_user_data(self):
    user = get_user_data("alice")
    expected = {
        "name": "Alice",
        "email": "alice@example.com",
        "active": True
    }
    self.assertDictEqual(user, expected)
```

**When to use:** When comparing dictionaries.

**Why use this:** Provides a clear diff showing which keys/values differ, making debugging much easier.

**Failure message:**
```
AssertionError: {'name': 'Alice', 'email': 'bob@example.com'} != {'name': 'Alice', 'email': 'alice@example.com'}
- {'email': 'bob@example.com', 'name': 'Alice'}
+ {'email': 'alice@example.com', 'name': 'Alice'}
```

## Custom messages

All assertion methods accept an optional `msg` parameter for custom failure messages:

```python
def test_with_custom_message(self):
    result = calculate_discount(100, 20)
    self.assertEqual(
        result,
        80,
        msg="20% discount on £100 should give £80"
    )
```

**When to use custom messages:**
- When the default failure message isn't clear enough
- When you want to provide context about what the test is checking
- When testing complex conditions

**Example failure with custom message:**
```
AssertionError: 85 != 80 : 20% discount on £100 should give £80
```

## Choosing the right assertion

Use the most **specific** assertion available:

| Instead of | Use |
|------------|-----|
| `assertTrue(x == y)` | `assertEqual(x, y)` |
| `assertTrue(x is None)` | `assertIsNone(x)` |
| `assertTrue(x in y)` | `assertIn(x, y)` |
| `assertTrue(isinstance(x, int))` | `assertIsInstance(x, int)` |
| `assertEqual(x, None)` | `assertIsNone(x)` |

**Why specificity matters:**

```python
# ❌ Less helpful error message
self.assertTrue(result == 5)
# Error: AssertionError: False is not true

# ✅ More helpful error message
self.assertEqual(result, 5)
# Error: AssertionError: 6 != 5
```

The more specific assertion provides better error messages, making debugging faster.

## Quick reference table

| Assertion | Checks | Example |
|-----------|--------|---------|
| `assertEqual(a, b)` | `a == b` | `assertEqual(result, 5)` |
| `assertNotEqual(a, b)` | `a != b` | `assertNotEqual(result, 0)` |
| `assertTrue(x)` | `bool(x) is True` | `assertTrue(is_valid)` |
| `assertFalse(x)` | `bool(x) is False` | `assertFalse(has_errors)` |
| `assertIs(a, b)` | `a is b` | `assertIs(obj1, obj2)` |
| `assertIsNot(a, b)` | `a is not b` | `assertIsNot(obj1, obj2)` |
| `assertIsNone(x)` | `x is None` | `assertIsNone(result)` |
| `assertIsNotNone(x)` | `x is not None` | `assertIsNotNone(user)` |
| `assertIn(a, b)` | `a in b` | `assertIn("test", tags)` |
| `assertNotIn(a, b)` | `a not in b` | `assertNotIn("admin", roles)` |
| `assertIsInstance(a, b)` | `isinstance(a, b)` | `assertIsInstance(result, int)` |
| `assertNotIsInstance(a, b)` | `not isinstance(a, b)` | `assertNotIsInstance(result, str)` |
| `assertGreater(a, b)` | `a > b` | `assertGreater(score, 50)` |
| `assertGreaterEqual(a, b)` | `a >= b` | `assertGreaterEqual(age, 18)` |
| `assertLess(a, b)` | `a < b` | `assertLess(size, limit)` |
| `assertLessEqual(a, b)` | `a <= b` | `assertLessEqual(count, max)` |
| `assertAlmostEqual(a, b)` | `round(a-b, 7) == 0` | `assertAlmostEqual(0.1+0.2, 0.3)` |
| `assertRegex(s, r)` | `re.search(r, s)` | `assertRegex(email, r'@.*\.com')` |
| `assertRaises(E)` | `raises E` | `with assertRaises(ValueError):` |

## Next steps

- Practice using assertions in [Your First Test](../learn/01-your-first-test.ipynb)
- Learn when to use different assertions in [Testing Thoroughly](../learn/02-testing-thoroughly.ipynb)
- Explore [Test Naming Conventions](test-naming-conventions.md) for writing clear test methods
- Review [Common Testing Mistakes](../recipes/avoid-common-testing-mistakes.md)

## References

- [Official Python unittest documentation](https://docs.python.org/3/library/unittest.html#assert-methods)
- [unittest Quick Reference](unittest-quick-reference.md)
