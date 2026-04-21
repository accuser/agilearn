# Test Naming Conventions

Good test names make your test suite self-documenting. When a test fails, a clear name immediately tells you what's broken. This reference provides patterns and examples for naming tests effectively.

## The Golden Rule

**A test name should describe what behaviour is being verified, not how the code works.**

```python
# ❌ Describes implementation
def test_uses_for_loop_to_sum():
    pass

# ✅ Describes behaviour
def test_calculates_total_of_all_items():
    pass
```

## Basic Structure

### Pattern 1: `test_[function]_[scenario]`

Use this pattern for simple, straightforward tests:

```python
def test_add_positive_numbers(self):
    """Test add() with positive numbers."""
    self.assertEqual(add(2, 3), 5)

def test_add_negative_numbers(self):
    """Test add() with negative numbers."""
    self.assertEqual(add(-2, -3), -5)

def test_add_with_zero(self):
    """Test add() with zero as one operand."""
    self.assertEqual(add(5, 0), 5)
```

### Pattern 2: `test_[scenario]_[expected_result]`

Use this when the behaviour is more important than the function:

```python
def test_negative_price_returns_none(self):
    """Test that negative prices are rejected."""
    self.assertIsNone(calculate_discount(-10, 20))

def test_empty_list_returns_zero(self):
    """Test that empty list sums to zero."""
    self.assertEqual(sum_items([]), 0)

def test_invalid_email_raises_valueerror(self):
    """Test that invalid email format raises ValueError."""
    with self.assertRaises(ValueError):
        validate_email("invalid")
```

### Pattern 3: `test_[when]_[then]`

Use this for complex scenarios:

```python
def test_when_user_not_logged_in_then_redirects_to_login(self):
    """Test unauthenticated users are redirected."""
    response = get_profile(user=None)
    self.assertEqual(response.redirect_url, "/login")

def test_when_cart_empty_then_checkout_disabled(self):
    """Test checkout button is disabled for empty cart."""
    cart = ShoppingCart()
    self.assertFalse(cart.can_checkout())
```

## Naming by Test Type

### Testing Normal Behaviour

```python
def test_calculate_discount_with_valid_inputs(self):
    pass

def test_search_returns_matching_results(self):
    pass

def test_user_can_update_profile(self):
    pass
```

### Testing Edge Cases

```python
def test_divide_by_zero_returns_none(self):
    pass

def test_empty_string_returns_empty_list(self):
    pass

def test_maximum_integer_value_handled_correctly(self):
    pass
```

### Testing Error Conditions

```python
def test_negative_age_raises_valueerror(self):
    pass

def test_missing_required_field_raises_keyerror(self):
    pass

def test_duplicate_email_raises_integrity_error(self):
    pass
```

### Testing Boundary Conditions

```python
def test_password_minimum_length_accepted(self):
    pass

def test_password_one_character_too_short_rejected(self):
    pass

def test_list_with_single_item_processed_correctly(self):
    pass
```

## Python Naming Conventions

### Use Snake Case

```python
# ✅ Correct - snake_case
def test_calculate_total_price(self):
    pass

# ❌ Wrong - camelCase
def testCalculateTotalPrice(self):
    pass

# ❌ Wrong - PascalCase
def TestCalculateTotalPrice(self):
    pass
```

### Use Descriptive Words

```python
# ❌ Too abbreviated
def test_calc_tot(self):
    pass

# ✅ Clear and readable
def test_calculate_total(self):
    pass
```

### Avoid Numbers

```python
# ❌ No information
def test1(self):
    pass

def test2(self):
    pass

# ✅ Descriptive names
def test_add_positive_numbers(self):
    pass

def test_add_negative_numbers(self):
    pass
```

## Common Patterns by Scenario

### Testing with Different Inputs

```python
def test_add_two_positive_numbers(self):
    pass

def test_add_positive_and_negative(self):
    pass

def test_add_two_negative_numbers(self):
    pass

def test_add_with_zero(self):
    pass

def test_add_with_floats(self):
    pass
```

### Testing State Changes

```python
def test_deposit_increases_balance(self):
    pass

def test_withdraw_decreases_balance(self):
    pass

def test_overdraft_keeps_balance_unchanged(self):
    pass
```

### Testing Validation

```python
def test_valid_email_accepted(self):
    pass

def test_email_without_at_symbol_rejected(self):
    pass

def test_email_without_domain_rejected(self):
    pass

def test_email_with_spaces_rejected(self):
    pass
```

### Testing Collections

```python
def test_empty_list_returns_zero(self):
    pass

def test_single_item_list_returns_item_value(self):
    pass

def test_multiple_items_returns_sum(self):
    pass

def test_list_with_none_values_skips_none(self):
    pass
```

## Test Class Naming

### Pattern: `Test[ClassName]` or `Test[FunctionName]`

```python
# Testing a class
class TestShoppingCart(unittest.TestCase):
    pass

# Testing a function
class TestCalculateDiscount(unittest.TestCase):
    pass

# Testing a module feature
class TestUserAuthentication(unittest.TestCase):
    pass
```

### Group Related Tests

```python
# All discount calculation tests together
class TestDiscountCalculation(unittest.TestCase):
    def test_ten_percent_discount(self):
        pass

    def test_fifty_percent_discount(self):
        pass

    def test_one_hundred_percent_discount(self):
        pass

# All validation tests together
class TestInputValidation(unittest.TestCase):
    def test_valid_input_accepted(self):
        pass

    def test_empty_input_rejected(self):
        pass

    def test_too_long_input_rejected(self):
        pass
```

## Docstring Best Practices

Test docstrings should complement the test name:

```python
def test_calculate_discount_with_twenty_percent(self):
    """Test that 20% discount on £100 results in £80."""
    self.assertEqual(calculate_discount(100, 20), 80.0)
```

### Good Docstrings

```python
"""Test that negative prices return None."""

"""Verify user can update profile with valid data."""

"""Check that empty cart disables checkout button."""
```

### Poor Docstrings

```python
"""Test discount calculation."""  # Too vague

"""Test function."""  # No information

"""This test tests the thing."""  # Redundant
```

## Real-World Examples

### E-commerce System

```python
class TestShoppingCart(unittest.TestCase):
    def test_add_item_increases_cart_count(self):
        pass

    def test_remove_item_decreases_cart_count(self):
        pass

    def test_clear_cart_removes_all_items(self):
        pass

    def test_calculate_total_sums_all_item_prices(self):
        pass

    def test_apply_discount_code_reduces_total(self):
        pass

    def test_invalid_discount_code_ignored(self):
        pass
```

### User Authentication

```python
class TestUserLogin(unittest.TestCase):
    def test_valid_credentials_grants_access(self):
        pass

    def test_invalid_password_denies_access(self):
        pass

    def test_nonexistent_user_denies_access(self):
        pass

    def test_locked_account_denies_access(self):
        pass

    def test_successful_login_creates_session(self):
        pass
```

### Data Processing

```python
class TestDataParser(unittest.TestCase):
    def test_valid_json_parsed_correctly(self):
        pass

    def test_malformed_json_raises_parse_error(self):
        pass

    def test_empty_file_returns_empty_list(self):
        pass

    def test_missing_required_field_raises_keyerror(self):
        pass

    def test_unicode_characters_handled_correctly(self):
        pass
```

## Anti-Patterns to Avoid

### ❌ Too Vague

```python
def test_function(self):
    pass

def test_calculation(self):
    pass

def test_validation(self):
    pass
```

### ❌ Implementation Details

```python
def test_uses_list_comprehension(self):
    pass

def test_calls_helper_function(self):
    pass

def test_iterates_with_for_loop(self):
    pass
```

### ❌ Non-Descriptive Numbers

```python
def test1(self):
    pass

def test2(self):
    pass

def test_case_3(self):
    pass
```

## Quick Decision Tree

When naming a test, ask yourself:

1. **What function/method am I testing?** → Include it in the name
2. **What scenario am I testing?** → Describe the input/state
3. **What should happen?** → Describe the expected outcome

**Formula**: `test_[what]_[scenario]_[outcome]`

**Example**: `test_divide_by_zero_returns_none`
- **What**: divide
- **Scenario**: by zero
- **Outcome**: returns none

## Summary

**Good test names:**
- Are descriptive and specific
- Use snake_case
- Start with `test_`
- Describe behaviour, not implementation
- Make failures immediately understandable

**Pattern**: `test_[function]_[scenario]_[expected_result]`

**Remember**: If you can't think of a good name, your test might be trying to do too much. Consider splitting it into multiple tests.

## Next Steps

- Practice naming tests in [Your First Test Tutorial](../learn/01-your-first-test.ipynb)
- Review [Common Testing Mistakes](../recipes/avoid-common-testing-mistakes.md)
- Check [unittest Quick Reference](unittest-quick-reference.md)
