---
title: zoneinfo reference
---

# `zoneinfo` reference

Quick reference for the `zoneinfo` module (Python 3.9+). For the underlying concepts see the [time zones notebook](../learn/03-time-zones-with-zoneinfo.ipynb).

## Importing

```python
from zoneinfo import ZoneInfo, available_timezones
```

`ZoneInfo` is the class you attach to datetimes. `available_timezones()` returns the full set of IANA zone names as a `set[str]`.

## Building a `ZoneInfo`

```python
ZoneInfo("UTC")
ZoneInfo("Europe/London")
ZoneInfo("America/New_York")
ZoneInfo("Asia/Tokyo")
ZoneInfo("Australia/Sydney")
ZoneInfo("Pacific/Auckland")
```

Names use the IANA `Continent/City` form. The list of valid names is platform-dependent — it comes from your system's `tzdata` database (or the `tzdata` pip package as a fallback on Windows).

## Common zone names

| Region | Name |
| --- | --- |
| UTC | `UTC` |
| London (and most of UK/Ireland) | `Europe/London` |
| Paris/Berlin/Madrid | `Europe/Paris`, `Europe/Berlin`, `Europe/Madrid` |
| New York | `America/New_York` |
| Los Angeles | `America/Los_Angeles` |
| Chicago | `America/Chicago` |
| Toronto | `America/Toronto` |
| São Paulo | `America/Sao_Paulo` |
| Tokyo | `Asia/Tokyo` |
| Shanghai/Beijing | `Asia/Shanghai` |
| Singapore | `Asia/Singapore` |
| Kolkata (India) | `Asia/Kolkata` |
| Dubai | `Asia/Dubai` |
| Sydney | `Australia/Sydney` |
| Auckland | `Pacific/Auckland` |
| Johannesburg | `Africa/Johannesburg` |
| Cairo | `Africa/Cairo` |

Never use abbreviations like `"EST"`, `"PST"`, `"BST"` — they're ambiguous (`EST` means something different in the US and Australia, for instance).

## Attaching to a datetime

```python
from datetime import datetime
from zoneinfo import ZoneInfo

london = ZoneInfo("Europe/London")

# At construction
dt = datetime(2026, 4, 21, 14, 30, tzinfo=london)

# Or attach to a naive datetime (assumes the naive value is *already* in that zone)
naive = datetime(2026, 4, 21, 14, 30)
aware = naive.replace(tzinfo=london)
```

`replace(tzinfo=...)` attaches the zone **without** changing the wall-clock values — use it when the value is already in the target zone and just lacks the metadata. Use `.astimezone(target)` to *convert* between zones.

## Converting between zones

```python
utc = ZoneInfo("UTC")
tokyo = ZoneInfo("Asia/Tokyo")

moment = datetime(2026, 4, 21, 14, 30, tzinfo=utc)
print(moment.astimezone(tokyo))   # 2026-04-21 23:30:00+09:00
```

`.astimezone(target)` preserves the absolute instant — only the wall-clock representation changes.

## Getting the current time

```python
datetime.now(tz=ZoneInfo("UTC"))               # aware, UTC
datetime.now(tz=ZoneInfo("Europe/London"))     # aware, London
```

Never `datetime.now()` (naive, local) or `datetime.utcnow()` (naive but UTC — the worst of both worlds).

## Inspecting a zone

Given a `ZoneInfo` and an aware datetime:

```python
dt = datetime(2026, 7, 15, 12, 0, tzinfo=ZoneInfo("Europe/London"))

dt.utcoffset()       # timedelta(seconds=3600)  — BST in July
dt.tzname()          # 'BST'
dt.dst()             # timedelta(seconds=3600)  — 1 hour of DST in effect
```

Same inspection in January would give `0:00:00`, `'GMT'`, and `0:00:00`.

## Enumerating all zones

```python
from zoneinfo import available_timezones

all_zones = available_timezones()
print(len(all_zones))               # ~600 typically
print(sorted(all_zones)[:10])       # sample
```

Useful for dropdowns or validation. Filter by prefix (`Europe/`, `America/`) if you want a region-specific list.

## DST transitions — the `fold` attribute

For ambiguous wall-clock times (the hour that happens twice in autumn), the `fold` attribute disambiguates: `fold=0` picks the first occurrence, `fold=1` picks the second.

```python
london = ZoneInfo("Europe/London")

# 2026-10-25 01:30 happens twice
before = datetime(2026, 10, 25, 1, 30, fold=0, tzinfo=london)   # BST
after  = datetime(2026, 10, 25, 1, 30, fold=1, tzinfo=london)   # GMT

print(before.utcoffset())    # 1:00:00
print(after.utcoffset())     # 0:00:00
```

For non-existent times (the spring-forward gap), `zoneinfo` returns whatever the system would show for that moment — `fold` picks between the two possible offset choices. Most application code doesn't care; if yours does, the Python docs have more detail.

## `ZoneInfo` versus `datetime.timezone`

`datetime.timezone(timedelta(hours=1))` gives a fixed-offset zone — no DST, no zone name, just `"+01:00"`. Useful for representing an ISO 8601 offset without a full IANA zone, but not a replacement for `ZoneInfo` when DST matters.

```python
from datetime import timezone, timedelta

fixed = timezone(timedelta(hours=1))      # UTC+01:00, no DST rules
```

`ZoneInfo("UTC")` and `timezone.utc` are functionally equivalent for UTC.

## Errors

| Error | Cause |
| --- | --- |
| `ZoneInfoNotFoundError` | Name isn't in the tzdata database (typo, or missing `tzdata` package on Windows) |
| `ValueError: fold must be 0 or 1` | Passed something else to `fold` |

Catch `ZoneInfoNotFoundError` if you're parsing zone names from user input.
