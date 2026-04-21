---
title: strftime and strptime format codes
---

# `strftime` and `strptime` format codes

The full table of directives, with examples for each. Both `strftime` (format a datetime as a string) and `strptime` (parse a string into a datetime) use the same set of codes.

Examples are all formatted from this datetime: `datetime(2026, 4, 21, 14, 30, 5)` — a Tuesday, day 112 of the year.

## Year

| Directive | Meaning | Example |
| --- | --- | --- |
| `%Y` | Year, 4 digits, zero-padded | `2026` |
| `%y` | Year, 2 digits, zero-padded | `26` |
| `%G` | ISO week year (4-digit) | `2026` |
| `%C` | Century | `20` |

Prefer `%Y` — `%y` is ambiguous for years spanning centuries.

## Month

| Directive | Meaning | Example |
| --- | --- | --- |
| `%m` | Month as zero-padded number | `04` |
| `%B` | Full month name (English) | `April` |
| `%b` | Abbreviated month name | `Apr` |

## Day

| Directive | Meaning | Example |
| --- | --- | --- |
| `%d` | Day of month, zero-padded | `21` |
| `%e` | Day of month, space-padded | ` 21` (Linux/macOS only) |
| `%j` | Day of year (001–366) | `112` |

## Weekday

| Directive | Meaning | Example |
| --- | --- | --- |
| `%A` | Full weekday name (English) | `Tuesday` |
| `%a` | Abbreviated weekday name | `Tue` |
| `%w` | Weekday as number (Sunday=0) | `2` |
| `%u` | ISO weekday (Monday=1) | `2` |

## Week number

| Directive | Meaning | Example |
| --- | --- | --- |
| `%V` | ISO week number (01–53) | `17` |
| `%U` | Week of year (Sunday first) | `16` |
| `%W` | Week of year (Monday first) | `16` |

`%V` with `%G` and `%u` gives the full ISO week-date (`2026-W17-2`). Don't combine `%V` with `%Y` — they can disagree at year boundaries.

## Time of day

| Directive | Meaning | Example |
| --- | --- | --- |
| `%H` | Hour (00–23) | `14` |
| `%I` | Hour (01–12) | `02` |
| `%p` | `AM` / `PM` | `PM` |
| `%M` | Minute (00–59) | `30` |
| `%S` | Second (00–59) | `05` |
| `%f` | Microsecond (000000–999999) | `000000` |

## Time zone

| Directive | Meaning | Example |
| --- | --- | --- |
| `%z` | UTC offset `±HHMM` or `±HH:MM` | `+0100` |
| `%Z` | Zone name | `BST` |

`%z` in `strftime` is reliable; parsing with `%z` in `strptime` depends on the exact format. `%Z` parsing is unreliable across platforms — prefer `fromisoformat` for zone-aware strings.

## Locale-sensitive (avoid if possible)

| Directive | Meaning | Example |
| --- | --- | --- |
| `%c` | Locale datetime representation | `Tue Apr 21 14:30:05 2026` |
| `%x` | Locale date representation | `04/21/26` |
| `%X` | Locale time representation | `14:30:05` |

Locale-sensitive formatting depends on `LC_TIME`, which is global state. Avoid for machine-readable output — use explicit format strings instead.

## Literal characters

| Directive | Meaning |
| --- | --- |
| `%%` | A literal `%` |

Any other character in the format string is treated as a literal — `%d/%m/%Y` has `/` literals between the directives.

## Common format strings

```python
dt = datetime(2026, 4, 21, 14, 30, 5)

dt.strftime("%Y-%m-%d")                 # 2026-04-21 (ISO date)
dt.strftime("%Y-%m-%dT%H:%M:%S")        # 2026-04-21T14:30:05 (ISO datetime)
dt.strftime("%d/%m/%Y")                 # 21/04/2026 (British)
dt.strftime("%m/%d/%Y")                 # 04/21/2026 (American)
dt.strftime("%A %d %B %Y")              # Tuesday 21 April 2026
dt.strftime("%d %b %Y, %H:%M")          # 21 Apr 2026, 14:30
dt.strftime("%Y-W%V-%u")                # 2026-W17-2 (ISO week-date)
dt.strftime("%Y%m%d")                   # 20260421 (sortable, filename-safe)
dt.strftime("%Y%m%dT%H%M%S")            # 20260421T143005 (basic ISO, filename-safe)
```

`strftime` is the same in every direction — whatever you put in the format string, that's what you get back. The inverse for parsing is `strptime(string, format)` using the same directives.
