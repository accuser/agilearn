# How to Avoid Common unittest Mistakes

As you learn unittest, you'll encounter some common pitfalls. This guide helps you recognise and avoid them, saving you debugging time and frustration.

## 1. Forgetting the `test_` Prefix

### The Mistake

```python
import unittest

class TestCalculator(unittest.TestCase):
    def check_addition(self):  # ❌ Won't run!
        self.assertEqual(2 + 2, 4)

    def verify_subtraction(self):  # ❌ Won't run!
        self.assertEqual(5 - 3, 2)
```

### Why It Happens

unittest only discovers and runs methods that start with `test_`. Methods with other names are ignored, even if they're in a TestCase class.

### The Fix

```python
class TestCalculator(unittest.TestCase):
    def test_addition(self):  # ✅ Runs correctly
        self.assertEqual(2 + 2, 4)

    def test_subtraction(self):  # ✅ Runs correctly
        self.assertEqual(5 - 3, 2)
```

### How to Spot It

If you run your tests and see "Ran 0 tests" but you know you have test methods, check that they all start with `test_`.

---

## 2. Forgetting `self` Before Assertions

### The Mistake

```python
class TestCalculator(unittest.TestCase):
    def test_addition(self):
        result = 2 + 2
        assertEqual(result, 4)  # ❌ NameError: name 'assertEqual' is not defined
```

### Why It Happens

Assertion methods like `assertEqual` belong to the TestCase class. You need `self.` to access them.

### The Fix

```python
class TestCalculator(unittest.TestCase):
    def test_addition(self):
        result = 2 + 2
        self.assertEqual(result, 4)  # ✅ Correct
```

### How to Spot It

You'll see `NameError: name 'assertEqual' is not defined` or similar errors. The fix is always to add `self.` before the assertion.

---

## 3. Testing Too Many Things in One Test

### The Mistake

```python
class TestMathOperations(unittest.TestCase):
    def test_all_operations(self):  # ❌ Too much in one test
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(divide(10, 2), 5)
```

### Why it's a problem

When this test fails, you don't immediately know which operation is broken. You have to read the error message carefully to figure it out.

### The Fix

```python
class TestMathOperations(unittest.TestCase):
    def test_addition(self):  # ✅ One behaviour per test
        self.assertEqual(add(2, 3), 5)

    def test_subtraction(self):  # ✅ Clear purpose
        self.assertEqual(subtract(5, 3), 2)

    def test_multiplication(self):  # ✅ Easy to debug
        self.assertEqual(multiply(3, 4), 12)

    def test_division(self):  # ✅ Focused
        self.assertEqual(divide(10, 2), 5)
```

### The Principle

**One test should verify one behaviour.** If a test fails, you should immediately know what's broken just from the test name.

---

## 4. Comparing Floats with `assertEqual`

### The Mistake

```python
class TestFloats(unittest.TestCase):
    def test_decimal_addition(self):
        result = 0.1 + 0.2
        self.assertEqual(result, 0.3)  # ❌ May fail!
```

### Why It Fails

Floating-point arithmetic in computers isn't always exact:

```python
>>> 0.1 + 0.2
0.30000000000000004  # Not exactly 0.3!
```

### The Fix

```python
class TestFloats(unittest.TestCase):
    def test_decimal_addition(self):
        result = 0.1 + 0.2
        self.assertAlmostEqual(result, 0.3, places=7)  # ✅ Correct
```

### When to Use Each

- **`assertEqual`**: For integers, strings, lists, etc.
- **`assertAlmostEqual`**: For floats and decimals

```python
# Integers - use assertEqual
self.assertEqual(5 + 3, 8)  # ✅

# Floats - use assertAlmostEqual
self.assertAlmostEqual(5.1 + 3.2, 8.3, places=1)  # ✅
```

---

## 5. Writing Vague Test Descriptions

### The Mistake

```python
class TestCalculator(unittest.TestCase):
    def test_calculation(self):  # ❌ What calculation?
        """Test calculation."""
        self.assertEqual(calculate_discount(100, 20), 80)

    def test_edge_case(self):  # ❌ Which edge case?
        """Test an edge case."""
        self.assertIsNone(calculate_discount(-10, 20))
```

### Why It's a Problem

When tests fail months later, vague names don't help you understand what broke.

### The Fix

```python
class TestCalculator(unittest.TestCase):
    def test_twenty_percent_discount_on_one_hundred_pounds(self):  # ✅ Clear
        """Test that 20% discount on £100 results in £80."""
        self.assertEqual(calculate_discount(100, 20), 80)

    def test_negative_price_returns_none(self):  # ✅ Specific
        """Test that negative price returns None."""
        self.assertIsNone(calculate_discount(-10, 20))
```

### Naming Pattern

Use this structure: `test_[what]_[scenario]_[expected_result]`

**Good examples:**
- `test_add_positive_numbers_returns_sum`
- `test_divide_by_zero_returns_none`
- `test_empty_list_returns_zero`
- `test_invalid_email_raises_value_error`

**Poor examples:**
- `test1`, `test2`, `test3` (no information)
- `testAddition` (not Python convention, too vague)
- `test_function` (which function? what about it?)

---

## 6. Not Testing Edge Cases

### The Mistake

```python
class TestDivision(unittest.TestCase):
    def test_division(self):  # ❌ Only tests happy path
        self.assertEqual(divide(10, 2), 5)
```

### The Problem

This test only checks that division works with normal inputs. It doesn't test:
- What happens with zero?
- What happens with negative numbers?
- What happens with division resulting in decimals?

### The Fix

```python
class TestDivision(unittest.TestCase):
    def test_divide_positive_numbers(self):  # ✅ Normal case
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero_raises_error(self):  # ✅ Edge case
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_divide_negative_numbers(self):  # ✅ Edge case
        self.assertEqual(divide(-10, 2), -5)

    def test_divide_results_in_float(self):  # ✅ Edge case
        self.assertAlmostEqual(divide(5, 2), 2.5)
```

### Edge Cases to Consider

- **Zero**: Often special
- **Negative numbers**: May behave differently
- **Empty collections**: Lists, strings, dictionaries
- **Boundary values**: Maximum/minimum values
- **None/null values**: Missing data
- **Invalid input**: Wrong types, out-of-range values

---

## 7. Not Running Tests After Writing Them

### The Mistake

```python
# Write test
class TestNewFeature(unittest.TestCase):
    def test_new_feature(self):
        self.assertEqual(new_feature(), expected_result)

# Oops, forgot to run unittest.main()!
```

### Why It's a Problem

You think you've written tests, but they've never actually executed. The bugs they would have caught go unnoticed.

### The Fix

**Always run your tests immediately after writing them:**

```python
class TestNewFeature(unittest.TestCase):
    def test_new_feature(self):
        self.assertEqual(new_feature(), expected_result)

# Run the tests!
unittest.main(argv=[''], verbosity=2, exit=False)
```

### Make It a Habit

1. Write a test
2. Run it and watch it fail (if testing new code)
3. Write/fix the code
4. Run the test again and watch it pass

This is the essence of Test-Driven Development (TDD).

---

## 8. Ignoring Test Failures

### The Mistake

```
test_calculate_discount ... FAIL
test_validate_email ... FAIL
test_process_order ... ok

======================================================================
FAIL: test_calculate_discount
AssertionError: 85.0 != 80.0
```

**Response**: "Oh well, 2 out of 3 passed, that's good enough."  # ❌

### Why It's Dangerous

Every failing test represents a bug or misunderstanding. Ignoring failures means bugs make it to production.

### The Fix

**Every test should pass, every time.**

When a test fails:
1. **Read the error message carefully**
2. **Understand what it's telling you**
3. **Fix either the code or the test**
4. **Run again until it passes**

### When Tests Fail

Test failures mean one of three things:

1. **Your code is buggy** → Fix the code
2. **Your test is wrong** → Fix the test
3. **Your understanding is wrong** → Learn, then fix accordingly

---

## 9. Testing Implementation Details

### The Mistake

```python
def calculate_total(items):
    # Implementation uses a temporary variable
    temp_sum = 0
    for item in items:
        temp_sum += item.price
    return temp_sum

class TestTotal(unittest.TestCase):
    def test_uses_temp_sum_variable(self):  # ❌ Testing implementation
        # This test checks HOW it works, not WHAT it does
        pass
```

### Why It's a Problem

Tests should verify **what** your code does, not **how** it does it. If you refactor the implementation, tests shouldn't need to change.

### The Fix

```python
class TestTotal(unittest.TestCase):
    def test_calculates_total_price(self):  # ✅ Tests behaviour
        """Test that total price is sum of all item prices."""
        items = [Item(10), Item(20), Item(30)]
        self.assertEqual(calculate_total(items), 60)
```

### The Principle

Test the **interface** (inputs and outputs), not the **implementation** (internal details).

---

## 10. Not Using Descriptive Assertion Messages

### The Mistake

```python
class TestValidation(unittest.TestCase):
    def test_email_validation(self):
        self.assertTrue(is_valid_email("test@example.com"))  # ❌ Vague
```

When this fails:
```
FAIL: test_email_validation
AssertionError: False is not true
```

You have no idea why it failed!

### The Fix

```python
class TestValidation(unittest.TestCase):
    def test_email_validation(self):
        email = "test@example.com"
        self.assertTrue(
            is_valid_email(email),
            f"Expected {email} to be valid, but it was rejected"  # ✅ Helpful
        )
```

When this fails:
```
FAIL: test_email_validation
AssertionError: False is not true : Expected test@example.com to be valid, but it was rejected
```

Now you know exactly what went wrong!

---

## Quick Checklist

Before you finish writing tests, check:

- [ ] All test methods start with `test_`
- [ ] All assertions use `self.`
- [ ] Each test checks one behaviour
- [ ] Float comparisons use `assertAlmostEqual`
- [ ] Test names are descriptive
- [ ] Edge cases are tested
- [ ] Tests have been run and pass
- [ ] No failing tests are ignored
- [ ] Tests check behaviour, not implementation
- [ ] Assertion messages are helpful

## Summary

The most common mistakes are:
1. Forgetting `test_` prefix
2. Forgetting `self` before assertions
3. Testing too much in one test
4. Using `assertEqual` for floats
5. Vague test descriptions

Avoid these, and you'll write better, more maintainable tests!

## Next Steps

- Practice with [Your First Test Tutorial](../learn/01-your-first-test.ipynb)
- Learn [Test Naming Conventions](../reference/test-naming-conventions.md)
- Review [unittest Quick Reference](../reference/unittest-quick-reference.md)
