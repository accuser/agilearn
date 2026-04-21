# Why functions matter

Functions are arguably the most important building block in programming. They let you take a piece of logic, give it a name, and reuse it wherever you need it. But their value runs much deeper than simple reuse. Understanding why functions matter will shape how you think about writing, organising, and maintaining code.

## The DRY principle

"Do not Repeat Yourself" is one of the most widely cited principles in software development. The idea is simple: every piece of knowledge should have a single, authoritative representation in your codebase. When you find yourself copying and pasting the same block of code, that is a strong signal that a function is waiting to be written.

Consider a programme that calculates discounted prices in several places. Without a function, every calculation is a separate copy. If the discount formula changes, you have to find and update every copy. Miss one, and you have a bug. With a function, the formula lives in exactly one place:

```python
def apply_discount(price: float, discount: float) -> float:
    """Return the price after applying the discount percentage."""
    return price * (1 - discount / 100)
```

Now every part of your programme calls `apply_discount()`, and changing the formula means changing one function.

## Abstraction: hiding complexity behind a clear interface

Functions create layers of abstraction. When you call `sorted()`, you do not need to know which sorting algorithm Python uses. You only need to know what it accepts and what it returns. This is the power of a well-designed function: it hides the complexity of *how* something works behind a clear description of *what* it does.

Good functions are like well-labelled boxes. You know what goes in, you know what comes out, and you do not need to open the box to use it. This allows you to think at a higher level, assembling your programme from meaningful operations rather than low-level details.

## Code organisation and readability

A long, unbroken script is difficult to read and even harder to modify. Functions give your code structure. Each function is a named, self-contained unit of logic with a clear purpose. When you read a well-organised programme, the function names alone tell you the story:

```python
data = load_data("sales.csv")
cleaned = remove_duplicates(data)
summary = calculate_totals(cleaned)
save_report(summary, "report.pdf")
```

Even without seeing the implementation of each function, you understand the overall flow. Functions turn a wall of code into a narrative.

## Testing: functions as testable units

One of the most practical reasons to write functions is testability. A function with clear inputs and a clear return value is straightforward to test:

```python
import unittest

class TestDiscount(unittest.TestCase):
    def test_apply_ten_percent_discount(self):
        result = apply_discount(100.0, 10)
        self.assertEqual(result, 90.0)
```

Testing code that is tangled up in a long script, with dependencies on global variables and side effects, is far more difficult. Functions create natural boundaries for testing. Each function is a unit, and testing it in isolation is what unit testing is all about.

## Reusability across projects

Once you have written a well-designed function, it is not tied to one programme. A function that validates email addresses, formats dates, or calculates distances can be moved to a module and imported into any project that needs it. Over time, you build a personal library of reliable, tested functions that accelerate your work.

## The evolution from scripts to functions to modules

Most programmers follow a natural progression. You start by writing scripts: sequential code that runs from top to bottom. As your scripts grow, you notice repetition and extract functions. As your collection of functions grows, you organise them into modules. This is not just about tidiness. It reflects a deepening understanding of how to decompose problems into manageable, reusable pieces.

```
Script          ->  Functions        ->  Modules
(one long file)     (named blocks)       (organised collections)
```

Each step up the ladder brings clearer code, easier testing, and better collaboration with other programmers.

## The recipe analogy

Think of a function as a recipe. A recipe has a name ("Victoria sponge"), a list of ingredients (parameters), a set of instructions (the function body), and a finished product (the return value). You do not rewrite the entire recipe every time you bake a cake. You follow it. And if you want to adjust the recipe, you change it in one place.

Just as a head chef organises recipes into categories (starters, mains, desserts), a programmer organises functions into modules. And just as a recipe can be shared between kitchens, a function can be shared between projects.

## When not to create a function

Functions are powerful, but over-abstraction is a real risk. Not every three lines of code need to become a function. Here are some signs that a function might be unnecessary:

- **It is called only once and is unlikely to be reused.** If the code is clear and short, inlining it may be more readable.
- **The function name does not add meaning.** If you cannot think of a name that is clearer than the code itself, the abstraction may not be helping.
- **It creates unnecessary indirection.** If a reader has to jump through five function calls to understand a simple operation, the code has become harder to follow, not easier.
- **The function has too many parameters.** A function with 10 parameters is probably doing too much. Consider whether it should be broken into smaller functions or whether the parameters should be grouped into a data structure.

The goal is clarity. Functions should make your code easier to read, easier to test, and easier to change. When they start doing the opposite, it is time to step back and reconsider.

## Summary

Functions matter because they are the fundamental tool for managing complexity. They let you name things, reuse things, test things, and organise things. They transform sprawling scripts into readable, maintainable programmes. Learning to write good functions is not just a technical skill. It is a way of thinking about problems clearly and solving them well.
