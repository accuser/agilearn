# Avoid common datetime mistakes

**The question.** Your datetime code is misbehaving — a subtraction raises `TypeError`, ages are off by a day, a scheduled reminder fires an hour early on the day the clocks change. The cause is almost always one of a small handful of traps; this recipe is the catalogue.

Below is the summary; each trap is explained in detail after.

## The answer

| Looks like… | Why it bites | Fix |
| --- | --- | --- |
| `aware - naive` | `TypeError: can't subtract offset-naive and offset-aware datetimes` | Make everything aware — attach zones on the way in |
| `datetime.utcnow()` | Returns a **naive** datetime — looks UTC, compares wrongly | `datetime.now(tz=ZoneInfo('UTC'))` |
| `(today - dob).days / 365.25` | Approximation; leap years and calendar variation | Subtract years, adjust for whether the birthday's happened |
| `today + timedelta(months=1)` | `TypeError` — `timedelta` has no months | `today + relativedelta(months=1)` |
| Storing `'2026-03-29 01:30'` as local | Doesn't exist (spring forward) or exists twice (fall back) | Store aware UTC; convert for display |
| Naive datetime arithmetic across DST | Clock values wrong by an hour | Attach zone **before** arithmetic |
| `%y` for year in format string | 2-digit, Y2K-ambiguous | Use `%Y` |
| `strptime('04/05/2026', '%d/%m/%Y')` vs `%m/%d/%Y` | Silent ambiguity | Pick one convention; reject if data mixes both |
| `date(...) < datetime(...)` | `TypeError` | Cast one side (`.date()` or `datetime.combine(...)`) |
| `%Z` in `strptime` | Historically unreliable across platforms | Use `fromisoformat` (3.11+) or parse offset separately |
| `datetime.now()` with no arg | Returns **local naive** — depends on machine config | `datetime.now(tz=ZoneInfo(...))` |

Each in turn below.

## Mixing naive and aware datetimes

```python
from datetime import datetime
from zoneinfo import ZoneInfo

aware = datetime(2026, 4, 21, 14, 30, tzinfo=ZoneInfo('UTC'))
naive = datetime(2026, 4, 21, 14, 30)

aware - naive   # TypeError: can't subtract offset-naive and offset-aware datetimes
```

Python refuses because the answer depends on a zone it wasn't told. Fix: make everything aware — attach a zone on the way in. See [UTC everywhere](../concepts/utc-everywhere.md) for the design rule.

## Using `datetime.utcnow()`

`utcnow()` returns a **naive** datetime set to UTC. It looks right, but because the result is naive, Python will happily compare it against a local-zone naive datetime and give nonsense.

```python
# Bad
naive_utc = datetime.utcnow()

# Good
aware_utc = datetime.now(tz=ZoneInfo('UTC'))
```

(`utcnow` is deprecated in 3.12 — if your codebase still has calls to it, now's the time.)

## Computing age with a `timedelta`

```python
# Wrong: 365.25 days is an approximation
age_years = (today - dob).days / 365.25
```

Calendar years aren't a fixed number of days. For the integer number of birthdays someone has had, subtract years and check whether the birthday has happened yet this year — see the [durations recipe](compute-durations-and-ages.ipynb).

## Adding a month with `timedelta`

`timedelta(months=1)` doesn't exist — `timedelta` only supports fixed durations (days, seconds, microseconds). Use `dateutil.relativedelta` for calendar-based shifts.

```python
from dateutil.relativedelta import relativedelta
later = today + relativedelta(months=1)

# End-of-month edge case — relativedelta clamps to the last valid day
date(2026, 1, 31) + relativedelta(months=1)   # 2026-02-28
```

## Storing local times in a database

Storing `'2026-03-29 01:30'` without a zone loses data on DST transitions: that moment either doesn't exist (spring forward) or exists twice (fall back). Convert to aware UTC before persisting, convert back to local for display.

## Arithmetic on naive datetimes across DST

```python
# Naive datetime — no idea we're crossing a DST boundary
naive = datetime(2026, 3, 29, 0, 30)
later = naive + timedelta(hours=2)     # 02:30
# But 02:30 London time doesn't exist on that date!
```

Attach the zone first, then do arithmetic. `zoneinfo`-aware datetimes correctly handle transitions.

## `%Y` vs `%y` in format strings

`%Y` is the 4-digit year (`2026`); `%y` is the 2-digit year (`26`) and is ambiguous (is `26` 1926 or 2026?). Always use `%Y` unless you're deliberately reproducing a legacy format.

## Parsing with the wrong `dayfirst` assumption

`'04/05/2026'` is 4 May in British notation, 5 April in American. `strptime` with `'%d/%m/%Y'` gives the British answer; `'%m/%d/%Y'` gives the American one. There is no way to auto-detect — pick the convention that matches your source and commit to it. In pandas, `pd.to_datetime(s, dayfirst=True)` handles British data cleanly.

## Comparing `date` against `datetime`

```python
date(2026, 4, 21) < datetime(2026, 4, 21, 0, 0)   # TypeError
```

You can't mix the two types in comparisons. Cast one side — `.date()` on the datetime, or `datetime.combine(d, time.min)` on the date — depending which shape the rest of your code uses.

## Relying on `%Z` / `%z` in `strptime`

`strftime` emits zone names and offsets cleanly, but `strptime` parsing of `%Z` is historically unreliable across platforms. For parsing timestamps with zones, prefer `fromisoformat` (Python 3.11+ handles `Z` and offsets) or parse the offset separately.

## Treating `datetime.now()` as UTC

```python
now = datetime.now()    # local time, naive
```

`datetime.now()` with no argument returns the local time without a zone attached. Its value depends on the system's local zone — machine-specific state you almost certainly didn't mean to depend on. Use `datetime.now(tz=ZoneInfo('UTC'))` for current UTC or `datetime.now(tz=ZoneInfo('Europe/London'))` for current local.

## When the shortcut is fine

Naive datetimes are fine inside a single process that never persists or communicates times — unit tests, one-off scripts that just format "now" for a log line. `(today - dob).days / 365.25` is fine when you want average ages, not integer birthdays. `%y` is fine when you're deliberately matching a legacy format.

The traps bite when the shortcut is applied out of habit to a case where the defaults don't match the intent — especially anything that crosses a DST boundary, a zone, or a system boundary.

## Related reading

- [UTC everywhere](../concepts/utc-everywhere.md) — the design essay behind most of these rules.
- [Compute durations and ages](compute-durations-and-ages.ipynb) — the right way to compute calendar ages.
- [Convert between time zones](convert-between-time-zones.ipynb) — the canonical shape for cross-zone work.
