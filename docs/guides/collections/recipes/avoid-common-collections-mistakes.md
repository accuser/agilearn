# Avoid common collections mistakes

**The question.** Something with a `collections` type is behaving oddly — a dict grew keys you only read, items vanished from a deque, a `Counter` dropped a count, a `namedtuple` won't update. You want the short list of traps and the fix for each.

Most of these come from one of two things: `defaultdict` creating keys on access, and the fact that `Counter` arithmetic and `deque(maxlen=...)` quietly discard things by design.

## The answer

| Looks like… | Why it bites | Fix |
| --- | --- | --- |
| A `defaultdict` has keys you only *read* | any access to a missing key runs the factory and inserts | check with `in` or `.get`; convert to `dict` when done building |
| `Counter` subtraction lost negative counts | `-` and `+` discard zero/negative results | use the `.subtract()` method to keep negatives |
| Items disappeared from a `deque` | `maxlen` drops from the far end when full | that's the feature — use no `maxlen` to keep everything |
| A queue is slow | `list.pop(0)`/`insert(0, x)` are O(n) | use `deque` with `popleft`/`appendleft` |
| `point.x = 5` raises `AttributeError` | a `namedtuple` is immutable | `point = point._replace(x=5)` — and keep the result |
| `Counter('hello world')` counts letters | you passed a string, not words | split first: `Counter(text.split())` |
| Using `OrderedDict` just to keep order | plain dicts have kept order since 3.7 | use a plain `dict` unless you need its extra methods |
| `namedtuple('T', ['class'])` raises | fields can't be keywords or start with digits | rename, or pass `rename=True` to auto-fix |
| `dd['k']` raises `KeyError` anyway | a `defaultdict` with no factory (`None`) acts like a dict | pass a factory: `defaultdict(list)` |
| `ChainMap` write didn't reach the defaults | writes only ever touch the *first* mapping | edit the target dict directly, or pick the right layer |
| `extendleft` reversed my items | each item is `appendleft`-ed in turn | `extend` for same order, or reverse first |

Each in turn below.

## Why each one bites

### 1. `defaultdict` creates keys when you read

The factory fires on *any* missing-key access, including a plain lookup — so merely reading `d[key]` inserts it. This silently grows the dict and can change `len`, iteration, and equality:

```python
from collections import defaultdict
d = defaultdict(list)
_ = d['x']             # inserts 'x': []
print('x' in d)        # True — created by the read

# to check without creating:
print(d.get('y'))      # None, nothing added
print('y' in d)        # False
```

### 2. `Counter` arithmetic drops non-positive counts

The `+` and `-` operators are multiset operations: results of zero or below are discarded. If you need the negatives (e.g. tracking a deficit), use the `subtract` method, which mutates in place and keeps them:

```python
from collections import Counter
print(Counter(a=1) - Counter(a=3))   # Counter() — −2 dropped
c = Counter(a=1); c.subtract(a=3)
print(c['a'])                        # -2 — kept
```

### 3. `maxlen` discards silently

A bounded deque drops an item off the far end for every push past `maxlen`. That's exactly what you want for a sliding window, but a surprise if you only meant to cap memory and still needed the old values. If you must keep everything, don't set `maxlen`.

### 4. A `list` as a queue is slow

`list.pop(0)` and `list.insert(0, x)` shift every remaining element, so they're O(n); doing them in a loop is O(n²). For a queue, that's the wrong structure:

```python
from collections import deque
q = deque()
q.append(x)            # O(1)
q.popleft()            # O(1) — vs list.pop(0)'s O(n)
```

### 5. `namedtuple` is immutable

You can't assign to a field. `_replace` gives you a new instance with changes applied — and because it *returns* the new tuple rather than mutating, you must capture the result:

```python
p = Point(1, 2)
p = p._replace(y=9)    # reassign; p._replace(y=9) alone changes nothing
```

### 6. Counting a string instead of its words

`Counter` counts whatever the iterable yields, and iterating a string yields *characters*. To count words, split first:

```python
Counter('the cat the')          # counts letters: {'t': 3, 'h': 2, ...}
Counter('the cat the'.split())  # counts words:   {'the': 2, 'cat': 1}
```

### 7. Reaching for `OrderedDict` out of habit

Since Python 3.7 a plain `dict` preserves insertion order, so you don't need `OrderedDict` just to keep order. Use it only for its extras — `move_to_end`, `popitem(last=False)`, or order-sensitive equality. Otherwise a `dict` is lighter and clearer.

### 8. Invalid `namedtuple` field names

Field names must be valid identifiers, not Python keywords, and can't start with a digit or underscore. `namedtuple('T', ['class', '2nd'])` raises `ValueError`. Pass `rename=True` to auto-rename the offenders to `_0`, `_1`, … positions, or just choose legal names.

### 9. A `defaultdict` with no factory

`defaultdict(None)` (or one constructed without a factory) has no `default_factory`, so missing keys raise `KeyError` exactly like a normal dict. The factory is the whole point — pass one:

```python
from collections import defaultdict
defaultdict(list)      # missing -> []
defaultdict(int)       # missing -> 0
```

### 10. `ChainMap` writes go to the first map only

Assigning to a `ChainMap` key, or deleting one, only ever affects `maps[0]` — the underlying default dicts are never touched. That's intentional (overrides layer on top), but if you meant to change a default, edit that dict directly. Looking up still searches all layers, first to last.

### 11. `extendleft` reverses the input

`deque.extendleft(iterable)` does `appendleft` for each item in turn, so they land in reverse order. Use `extend` to preserve order on the right, or reverse the iterable yourself before `extendleft`.

## The meta-lesson

Two of these containers trade safety for convenience: `defaultdict` mutates on read, and `Counter`/`deque(maxlen=...)` discard by design. Both are features, not bugs — but they mean "just looking" and "just adding" aren't always free. When in doubt, build with the specialised type and convert to a plain `dict`/`list` at the boundary (before returning or comparing), so the surprising behaviour stays contained. The [choosing a container](../concepts/choosing-a-container.md) essay covers picking the right one in the first place.
