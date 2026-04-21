---
title: timedelta arithmetic patterns
---

# `timedelta` arithmetic patterns

Quick reference for building, comparing, and operating on `timedelta` values. For the underlying concepts see the [datetime basics notebook](../learn/01-datetime-basics.ipynb).

## Construction

```python
from datetime import timedelta

timedelta(seconds=30)
timedelta(minutes=90)
timedelta(hours=8)
timedelta(days=1, hours=6, minutes=30)
timedelta(weeks=2)
timedelta(microseconds=500)
timedelta(milliseconds=250)
```

All keyword arguments are optional and additive. `timedelta(days=1, hours=24)` is `2 days`. Negative values are fine: `timedelta(days=-1)` is a duration of negative one day.

No `months` or `years`: those aren't fixed durations. For calendar shifts use `dateutil.relativedelta` — see the [durations recipe](../recipes/compute-durations-and-ages.ipynb).

## Arithmetic

| Operation | Result |
| --- | --- |
| `datetime + timedelta` | `datetime` (shifted) |
| `datetime - timedelta` | `datetime` (shifted back) |
| `datetime - datetime` | `timedelta` (gap between) |
| `date + timedelta(days=N)` | `date` |
| `date - date` | `timedelta` (days only — no time component) |
| `timedelta + timedelta` | `timedelta` |
| `timedelta - timedelta` | `timedelta` |
| `timedelta * N` | `timedelta` (scaled) |
| `timedelta / N` | `timedelta` (scaled, `N` can be float or int) |
| `timedelta / timedelta` | `float` (ratio) |
| `timedelta // timedelta` | `int` (whole-number quotient) |
| `timedelta % timedelta` | `timedelta` (remainder) |
| `abs(timedelta)` | `timedelta` (non-negative) |
| `-timedelta` | `timedelta` (negated) |

```python
from datetime import datetime, timedelta

start = datetime(2026, 4, 21, 9, 0)
end = datetime(2026, 4, 21, 17, 30)

gap = end - start              # timedelta(hours=8, minutes=30)
print(gap / timedelta(hours=1))        # 8.5 — how many hours?
print(gap // timedelta(minutes=30))    # 17 — how many half-hours?
print(gap % timedelta(hours=1))        # 0:30:00 — leftover after whole hours
```

## Attributes

A `timedelta` is stored internally as `(days, seconds, microseconds)` with seconds in `[0, 86400)` and microseconds in `[0, 1000000)`. Negative deltas have negative `days` and non-negative `seconds`/`microseconds`.

| Attribute | Meaning |
| --- | --- |
| `.days` | Whole days (can be negative) |
| `.seconds` | Leftover seconds (always 0–86399) |
| `.microseconds` | Leftover microseconds (always 0–999999) |
| `.total_seconds()` | Full duration as a float (seconds) |

**Watch out**: `.seconds` is *not* the total number of seconds. For 23 hours, `td.days == 0` and `td.seconds == 82800`; for 25 hours, `td.days == 1` and `td.seconds == 3600`. Use `.total_seconds()` for the single-number version.

## Comparison

All comparison operators work on `timedelta`:

```python
timedelta(hours=1) < timedelta(hours=2)          # True
timedelta(hours=1) == timedelta(minutes=60)      # True
timedelta(0) < timedelta(minutes=1)              # True
```

**You can't compare a `timedelta` to a number.** `timedelta(hours=1) > 30` raises `TypeError`. Convert with `.total_seconds()` first if you need a number, or — better — build a `timedelta` for the threshold:

```python
if gap > timedelta(minutes=30):
    alert()
```

Clearer than the numeric equivalent, and makes units explicit.

## Zero and truthiness

```python
bool(timedelta(0))                # False
bool(timedelta(microseconds=1))   # True
```

Any non-zero `timedelta` is truthy. `timedelta()` with no args is zero.

## Unit conversions

```python
td = timedelta(days=1, hours=6, minutes=30)

seconds = td.total_seconds()              # 109800.0
minutes = td.total_seconds() / 60         # 1830.0
hours   = td.total_seconds() / 3600       # 30.5
days    = td.total_seconds() / 86400      # 1.2708... (NOT td.days)
```

For the common ones, dividing by a named `timedelta` reads better:

```python
td / timedelta(hours=1)           # 30.5 (hours as float)
td / timedelta(minutes=1)         # 1830.0
td // timedelta(days=1)           # 1 (whole days only)
```

## Formatting for display

`str(td)` gives `'1 day, 6:30:00'` — fine for logs, ugly for UI. For a humanised form, roll your own small helper — see the [durations recipe](../recipes/compute-durations-and-ages.ipynb).

`repr(td)` gives `'datetime.timedelta(days=1, seconds=23400)'` — useful in debug output but not for users.

## Limits

Python's `timedelta` accepts durations between `-999999999 days` and `999999999 days` — which is about 2.7 million years, so you'll hit this limit exactly never.
