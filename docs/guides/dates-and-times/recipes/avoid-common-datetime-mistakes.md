---
title: Avoid common datetime mistakes
---

# Avoid common datetime mistakes

A short catalogue of traps that catch people out — and the shape of the fix for each. If you hit a datetime bug, it's probably one of these.

## Mixing naive and aware datetimes

```python
from datetime import datetime
from zoneinfo import ZoneInfo

aware = datetime(2026, 4, 21, 14, 30, tzinfo=ZoneInfo("UTC"))
naive = datetime(2026, 4, 21, 14, 30)

aware - naive   # TypeError: can't subtract offset-naive and offset-aware datetimes
```

Python refuses because the answer depends on a time zone it wasn't told. The fix is to make everything aware — attach a zone on the way in and you never have to worry about it again. See the [UTC everywhere essay](../concepts/utc-everywhere.md) for the design rule.

## Using `datetime.utcnow()`

`utcnow()` returns a **naive** datetime set to UTC. It looks like it's doing the right thing, but because the result is naive Python will happily compare it against a local-zone naive datetime and give you nonsense. Don't use it.

```python
# Bad
from datetime import datetime
naive_utc = datetime.utcnow()   # naive! no tzinfo

# Good
from zoneinfo import ZoneInfo
aware_utc = datetime.now(tz=ZoneInfo("UTC"))
```

The pattern `datetime.now(tz=ZoneInfo("UTC"))` is always the right answer for "current UTC".

## Computing \"age\" with a `timedelta`

```python
# Wrong: 365.25 days is an approximation
age_years = (today - dob).days / 365.25
```

Calendar years aren't a fixed number of days — leap years, DST shifts, even the definition of \"year\" varies. For an integer number of birthdays, subtract years and check whether the birthday has happened yet this year (see the [durations recipe](compute-durations-and-ages.ipynb)).

## Adding a month with `timedelta`

`timedelta(months=1)` doesn't exist — `timedelta` only supports fixed durations (days, seconds, microseconds). For calendar-based shifts, reach for `dateutil.relativedelta` or compute the target date directly.

```python
# Wrong
from datetime import timedelta
later = today + timedelta(months=1)    # TypeError

# Right
from dateutil.relativedelta import relativedelta
later = today + relativedelta(months=1)
```

Note the end-of-month edge case: `date(2026, 1, 31) + relativedelta(months=1)` is `2026-02-28`, not `2026-03-03`. `relativedelta` clamps to the last valid day — usually what you want.

## Storing local times in a database

Storing `"2026-03-29 01:30"` in a database with no zone information means losing data on DST transitions: that moment either doesn't exist (spring forward) or exists twice (fall back). Convert to aware UTC before persisting, convert back to local time for display.

See the [UTC everywhere essay](../concepts/utc-everywhere.md) for the full argument.

## Doing arithmetic on naive datetimes across DST

```python
# Naive datetime; no idea we're crossing a DST boundary
naive = datetime(2026, 3, 29, 0, 30)
later = naive + timedelta(hours=2)     # 02:30
# But 02:30 London time doesn't exist on that date!
```

Attach the zone first, then do arithmetic. `zoneinfo`-aware datetimes correctly handle transitions.

## Using `%Y` vs `%y` in format strings

`%Y` is the 4-digit year (`2026`), `%y` is the 2-digit year (`26`). Always use `%Y` — `%y` is ambiguous (is `26` 1926 or 2026?) and the source of many a Y2K-style bug.

## Parsing with the wrong `dayfirst` assumption

`"04/05/2026"` is 4 May in British notation, 5 April in American. `strptime` with `"%d/%m/%Y"` gives the British answer; `"%m/%d/%Y"` gives the American one. There is no way to auto-detect — pick the convention that matches your data source and commit to it.

In pandas, `pd.to_datetime(s, dayfirst=True)` handles this for British-convention data.

## Comparing `date` against `datetime`

```python
date(2026, 4, 21) < datetime(2026, 4, 21, 0, 0)   # TypeError
```

You can't mix the two types in comparisons. Either call `.date()` on the datetime or build a datetime from the date — depends which one is the right shape for what you're doing.

## Relying on `%Z` / `%z` in `strptime`

`strftime` emits zone names and offsets cleanly, but `strptime` parsing of `%Z` is historically unreliable across platforms. For parsing timestamps with zones, prefer `fromisoformat` (Python 3.11+ handles `Z` and offsets) or parse the offset separately.

## Treating `datetime.now()` as UTC

```python
now = datetime.now()    # local time, naive
```

`datetime.now()` with no argument returns the local time, without a zone attached. It's naive, and its value depends on the system's local time zone — which is machine-specific state you probably didn't want to depend on. Use `datetime.now(tz=ZoneInfo("UTC"))` for current UTC, or `datetime.now(tz=ZoneInfo("Europe/London"))` for current local.
