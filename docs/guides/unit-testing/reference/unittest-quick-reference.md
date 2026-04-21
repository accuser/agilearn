# unittest Quick Reference

A concise reference guide for Python's unittest module. Keep this handy while writing tests.

## Basic Test Structure

```python
import unittest

class TestMyFunction(unittest.TestCase):
    """Tests for my_function."""

    def test_specific_scenario(self):
        """Clear description of what this test checks."""
        # Arrange: Set up test data
        input_value = 42

        # Act: Call the function
        result = my_function(input_value)

        # Assert: Check the result
        self.assertEqual(result, expected_output)

# For Jupyter notebooks
unittest.main(argv=[''], verbosity=2, exit=False)

# For .py files
if __name__ == '__main__':
    unittest.main()
```

## Common Assertions

| Assertion | Checks | Example |
|-----------|--------|---------|
| `assertEqual(a, b)` | a == b | `self.assertEqual(add(2,3), 5)` |
| `assertNotEqual(a, b)` | a != b | `self.assertNotEqual(result, 0)` |
| `assertTrue(x)` | bool(x) is True | `self.assertTrue(len(items) > 0)` |
| `assertFalse(x)` | bool(x) is False | `self.assertFalse(is_empty(data))` |
| `assertIs(a, b)` | a is b | `self.assertIs(result, None)` |
| `assertIsNot(a, b)` | a is not b | `self.assertIsNot(new_obj, old_obj)` |
| `assertIsNone(x)` | x is None | `self.assertIsNone(find_user(''))` |
| `assertIsNotNone(x)` | x is not None | `self.assertIsNotNone(result)` |
| `assertIn(a, b)` | a in b | `self.assertIn('error', message)` |
| `assertNotIn(a, b)` | a not in b | `self.assertNotIn('debug', log)` |
| `assertIsInstance(a, b)` | isinstance(a, b) | `self.assertIsInstance(result, list)` |
| `assertNotIsInstance(a, b)` | not isinstance(a, b) | `self.assertNotIsInstance(x, str)` |

## Numeric Assertions

| Assertion | Use Case | Example |
|-----------|----------|---------|
| `assertAlmostEqual(a, b)` | Floats (7 decimal places) | `self.assertAlmostEqual(0.1+0.2, 0.3)` |
| `assertAlmostEqual(a, b, places=n)` | Floats (n decimal places) | `self.assertAlmostEqual(pi, 3.14, places=2)` |
| `assertNotAlmostEqual(a, b)` | Floats are different | `self.assertNotAlmostEqual(0.1, 0.2)` |
| `assertGreater(a, b)` | a > b | `self.assertGreater(score, 0)` |
| `assertGreaterEqual(a, b)` | a >= b | `self.assertGreaterEqual(count, 1)` |
| `assertLess(a, b)` | a < b | `self.assertLess(error_rate, 0.01)` |
| `assertLessEqual(a, b)` | a <= b | `self.assertLessEqual(age, 120)` |

## Collection Assertions

| Assertion | Checks | Example |
|-----------|--------|---------|
| `assertListEqual(a, b)` | Lists are equal | `self.assertListEqual([1,2], result)` |
| `assertTupleEqual(a, b)` | Tuples are equal | `self.assertTupleEqual((1,2), coords)` |
| `assertSetEqual(a, b)` | Sets are equal | `self.assertSetEqual({1,2}, set(result))` |
| `assertDictEqual(a, b)` | Dicts are equal | `self.assertDictEqual({'a': 1}, result)` |
| `assertCountEqual(a, b)` | Same elements, any order | `self.assertCountEqual([1,2,3], [3,2,1])` |

## Exception and Warning Assertions

### Testing Exceptions

```python
# Method 1: Context manager (recommended)
def test_divide_by_zero_raises_error(self):
    """Test that dividing by zero raises ZeroDivisionError."""
    with self.assertRaises(ZeroDivisionError):
        divide(10, 0)

# Method 2: With exception object
def test_invalid_input_error_message(self):
    """Test that error message is correct."""
    with self.assertRaises(ValueError) as cm:
        parse_age("invalid")

    self.assertEqual(str(cm.exception), "Age must be a number")

# Method 3: Callable form
def test_exception_with_args(self):
    """Test exception with specific arguments."""
    self.assertRaises(ValueError, parse_age, "invalid")
```

### Testing Warnings

```python
def test_deprecated_function_warns(self):
    """Test that deprecated function issues warning."""
    with self.assertWarns(DeprecationWarning):
        old_function()
```

## String Assertions

| Assertion | Checks | Example |
|-----------|--------|---------|
| `assertRegex(text, pattern)` | Regex matches | `self.assertRegex(email, r'.*@.*\.com')` |
| `assertNotRegex(text, pattern)` | Regex doesn't match | `self.assertNotRegex(id, r'[^0-9]')` |
| `assertMultiLineEqual(a, b)` | Multiline strings equal | `self.assertMultiLineEqual(output, expected)` |

## Test Fixtures

### setUp and tearDown

```python
class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Runs before each test method."""
        self.db = create_test_database()
        self.db.connect()

    def tearDown(self):
        """Runs after each test method."""
        self.db.disconnect()
        self.db.delete()

    def test_insert(self):
        """self.db is available here."""
        self.db.insert("data")
        self.assertEqual(self.db.count(), 1)
```

### setUpClass and tearDownClass

```python
class TestExpensiveSetup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests in the class."""
        cls.shared_resource = create_expensive_resource()

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests in the class."""
        cls.shared_resource.cleanup()

    def test_something(self):
        """Can access self.shared_resource."""
        result = self.shared_resource.process()
        self.assertIsNotNone(result)
```

## Test Discovery

### Running Tests

```bash
# Run all tests in current directory
python -m unittest discover

# Run all tests in specific directory
python -m unittest discover -s tests

# Run all tests with verbose output
python -m unittest discover -v

# Run specific test file
python -m unittest test_calculator

# Run specific test class
python -m unittest test_calculator.TestAddition

# Run specific test method
python -m unittest test_calculator.TestAddition.test_positive_numbers
```

## Skipping Tests

```python
import unittest

class TestFeature(unittest.TestCase):
    @unittest.skip("Not implemented yet")
    def test_future_feature(self):
        pass

    @unittest.skipIf(sys.version_info < (3, 10), "Requires Python 3.10+")
    def test_new_syntax(self):
        pass

    @unittest.skipUnless(has_database(), "Requires database")
    def test_database_operation(self):
        pass
```

## Subtest

For testing multiple related scenarios:

```python
def test_multiple_inputs(self):
    """Test function with various inputs."""
    test_cases = [
        (2, 3, 5),
        (10, 5, 15),
        (-1, 1, 0),
    ]

    for a, b, expected in test_cases:
        with self.subTest(a=a, b=b):
            result = add(a, b)
            self.assertEqual(result, expected)
```

## Custom Failure Messages

```python
def test_with_custom_message(self):
    """Test with helpful failure message."""
    result = calculate(10, 20)
    self.assertEqual(
        result,
        30,
        f"Expected 30 but got {result} when adding 10 and 20"
    )
```

## Assertion Aliases

Some assertions have multiple names:

| Primary | Aliases |
|---------|---------|
| `assertEqual` | `assertEquals` (deprecated) |
| `assertNotEqual` | `assertNotEquals` (deprecated) |
| `assertRaises` | `assertRaisesRegex` (with regex) |

**Note**: Use the non-deprecated forms (without 's' at the end).

## Test Naming Convention

```
test_[what_you're_testing]_[scenario]_[expected_result]
```

**Examples:**
- `test_add_positive_numbers_returns_sum`
- `test_divide_by_zero_returns_none`
- `test_empty_input_raises_valueerror`

## Golden Rules

1. **Test methods must start with `test_`** or they won't run
2. **Use `self.` before all assertions** (e.g., `self.assertEqual`)
3. **One test should test one behaviour**
4. **Use `assertAlmostEqual` for floats**, not `assertEqual`
5. **Write descriptive test names and docstrings**
6. **Test edge cases**: zero, negative, empty, None, boundaries
7. **Every test should pass, every time**

## Common Patterns

### Arrange-Act-Assert

```python
def test_withdrawal(self):
    """Test bank account withdrawal."""
    # Arrange
    account = BankAccount(balance=100)

    # Act
    account.withdraw(30)

    # Assert
    self.assertEqual(account.balance, 70)
```

### Testing with Mock Data

```python
def test_process_user(self):
    """Test user processing with sample data."""
    user = {
        'name': 'Test User',
        'email': 'test@example.com',
        'age': 25
    }

    result = process_user(user)

    self.assertTrue(result['verified'])
    self.assertEqual(result['status'], 'active')
```

## Debugging Failed Tests

When a test fails, check:

1. **Read the assertion error** - it tells you what went wrong
2. **Check the test name and docstring** - ensure you're testing what you think
3. **Verify test data** - are inputs correct?
4. **Run the test in isolation** - does it still fail?
5. **Add print statements** - see what values you're getting
6. **Use a debugger** - step through the code

## Next Steps

- [Your First Test Tutorial](../learn/01-your-first-test.ipynb)
- [Test Naming Conventions](test-naming-conventions.md)
- [Avoiding Common Mistakes](../recipes/avoid-common-testing-mistakes.md)
- [Understanding Test Structure](../concepts/understanding-test-structure.md)

## External Resources

- [Official unittest documentation](https://docs.python.org/3/library/unittest.html)
- [Python Testing with unittest, nose, pytest](https://realpython.com/python-testing/)
