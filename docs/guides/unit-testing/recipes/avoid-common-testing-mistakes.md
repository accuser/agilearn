# How to avoid common unittest mistakes

# What are the most common mistakes when writing `unittest` tests?

Most `unittest` bugs come from a small, well-known set of traps. The really nasty ones are the silent failures — tests that run cleanly, report green, and aren't testing what you think they're testing. This is a quick reference to the patterns to watch for, ordered roughly by how often they catch people.

## The answer

| Trap | What happens | What to do instead |
|---|---|---|
| Test methods don't start with `test_` | `unittest` silently doesn't discover them; "Ran 0 tests" | Always prefix test methods with `test_` |
| Calling `assertEqual(...)` instead of `self.assertEqual(...)` | `NameError: name 'assertEqual' is not defined` | Assertion methods live on `self` |
| Many assertions in one test method | First failure stops the test; you don't see what else is broken | One logical assertion per test, descriptive method name |
| `assertEqual` on floats | Fails on `0.1 + 0.2 != 0.3` (floating-point precision) | `assertAlmostEqual(a, b, places=7)` |
| `try/except` inside a test "to catch the exception" | Test passes silently when the exception *doesn't* fire | `with self.assertRaises(SomeException):` |
| Vague test names like `test_one`, `test_input`, `test_works` | Failure messages don't tell you what broke | `test_returns_zero_for_empty_input`, `test_raises_on_negative_age` |
| Only testing the happy path | Bugs hide in edge cases — empty inputs, zero, negatives, very large values | Add tests for boundary and error inputs explicitly |
| Asserting on private internals (`_cache`, `_buffer`) | Tests break on every refactor, even when behaviour is correct | Test public behaviour and outputs, not internal state |
| Skipping tests because "it's just a small change" | The small change is the one that breaks production | Run the suite before every commit; let CI block merges |

## Why it works

Most of these traps are silent rather than loud — the test doesn't fail, it just doesn't *test* what you wrote it to test. Knowing the failure modes is the only defence.

**The `test_` prefix and `self.` requirements** are the two boilerplate rules new `unittest` users trip over. `unittest` discovers test methods by name pattern; `setUp`, `tearDown`, and helpers are explicitly excluded by being not-`test_`-prefixed. Forget the prefix and your method becomes an inert helper. Forget `self`, and you get a `NameError` because assertion methods are bound to the `TestCase` instance, not module-level functions.

**One assertion per test** is the rule that pays for itself the first time a test fails. With four assertions in one method, the first failure aborts the test and you see one error; the remaining three may also be broken but you won't find out until you've fixed the first. Four small tests with descriptive names tell you, on a single failed run, that two are broken and which two — diagnosis happens in the test runner output, not in your debugger.

**Float comparison.** `0.1 + 0.2` is not `0.3` in IEEE 754 — it's `0.30000000000000004`. `assertAlmostEqual(a, b, places=7)` rounds both values to seven decimal places before comparing, which is enough precision for most calculations and tolerant enough for floating-point error. Use `places` for absolute tolerance and `delta` for an explicit threshold.

**`try/except` instead of `assertRaises`.** This one is dangerous because the test is *green*. A `try/except SomeException: pass` block silently passes when no exception is raised — exactly the case the test exists to catch. `assertRaises` raises an `AssertionError` if the block completes without raising, which is what you want.

**Vague names** matter because tests fail asynchronously to the moment you wrote them. Six months later, "test_one" tells you nothing; "test_login_rejects_blank_password" tells you exactly what regressed. The test name is the failure message you read first.

**Edge cases.** Bugs cluster at boundaries: empty collections, zero, negative numbers, very large numbers, single-element inputs, off-by-one. The happy-path test ("does it work for `[1, 2, 3]`?") catches one class of bug; explicit edge-case tests catch the other ten.

**Testing internals.** When a test reaches into `_cache` or `_buffer`, every refactor that renames or reshapes that internal state breaks the test even though the behaviour is identical. Tests should pin down behaviour ("calling this returns that"), not implementation ("the third element of the internal queue is..."). The test failures will then mean what they say.

## Trade-offs

A few of these rules have edges worth knowing.

"One assertion per test" is a default, not a law. A test that asserts a returned object has the right type *and* the right value is two assertions on one outcome; splitting them is pedantic. The rule is really "one *behaviour* per test" — when a single failure could have multiple causes, split.

`assertAlmostEqual(a, b)` defaults to seven decimal places, which is fine for most arithmetic but too loose for high-precision numerical work and too tight for sums of many floats. Pick a tolerance that matches the calculation, and document why if it isn't obvious.

Testing private internals is sometimes the only practical option — for example, when the public interface only exposes coarse-grained behaviour and you need to assert on a finer-grained intermediate. When you do this, accept that the test is coupled to the implementation and update it deliberately when the implementation changes. Don't pretend it's a behaviour test.

Edge-case coverage isn't free. Every test is code that needs maintaining, and adding a test for every conceivable input is its own form of waste. Aim for the boundaries that matter for the contract — empty, zero, negative, the documented limits — not exhaustive enumeration.

## Related

- [How to test exceptions and error handling](test-exceptions.ipynb) — the right way to write the `assertRaises` tests this guide warns against doing with `try/except`.
- [How to run tests in Jupyter](run-tests-in-jupyter.ipynb) — the `unittest.main(argv=[''], exit=False)` invocation for notebook-based exploration.
- [Test naming conventions](../reference/test-naming-conventions.md) — why descriptive names beat sequential numbers.
- [Assertions reference](../reference/assertions.md) — the full set of `assertX` methods including `assertAlmostEqual`, `assertSetEqual`, and friends.
