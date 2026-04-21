---
title: Why naive datetimes are a footgun
---

# Why naive datetimes are a footgun

A *naive* datetime is one without a time zone attached — no `tzinfo`. The string `"2026-04-21 14:30"`, parsed into a `datetime`, is naive: it carries the wall-clock values but nothing about which wall they came off.

That sounds harmless. It isn't. Here's why.

## The ambiguity is real

If I tell you it's 14:30, you need to know *where* before that's a useful statement. 14:30 in London is 09:30 in New York and 23:30 in Tokyo — three different moments in time. A naive datetime is any of them; the object doesn't know. Worse, it doesn't know that it doesn't know.

```python
from datetime import datetime

event = datetime(2026, 4, 21, 14, 30)
# Happens when? London 14:30? UTC 14:30? The server's local time?
# The object can't tell you.
```

That's the footgun. A naive datetime looks complete — it has a year, a month, a day, a time — but it's missing the one piece of information needed to pin it to a moment.

## Where the bugs come in

Naive datetimes work fine *within* a single zone. A batch job running on a server in London, reading timestamps from a database populated by applications in London, displaying results to users in London — naive works. Everyone implicitly agrees on the zone.

The bugs start the moment that invariant breaks. A user travels. A server moves to a new data centre. The app gets deployed to a second region. A dataset from another team lands in your pipeline. At that point:

- Your 09:00 meeting now happens an hour late, or an hour early.
- Scheduled jobs fire at the wrong moment twice a year (DST).
- Timestamps from different sources can't be compared — and nothing warns you, because they're all naive and Python happily subtracts them.

The common thread: there's no machine-checkable signal that a naive datetime belongs to a particular zone. It's a human convention, documented (maybe) in a comment somewhere, unverified by the type system.

## What Python does to save you

Python refuses to mix naive and aware datetimes:

```python
from zoneinfo import ZoneInfo
aware = datetime(2026, 4, 21, 14, 30, tzinfo=ZoneInfo("UTC"))
naive = datetime(2026, 4, 21, 14, 30)

aware - naive   # TypeError: can't subtract offset-naive and offset-aware datetimes
aware < naive   # TypeError: can't compare offset-naive and offset-aware datetimes
```

This is a feature. The answer genuinely depends on which zone `naive` is in, and Python refuses to guess. In codebases that mix the two, this error is annoying — but every one of those errors is a bug caught early.

The worse failure mode is the one where *everything* is naive and you get a number back that looks plausible but was computed by treating two zones as if they were the same.

## The fix

Make everything aware — attach a zone on the way in and you never have to worry about it again. `zoneinfo.ZoneInfo("Europe/London")` (or `UTC`) turns a naive datetime into an aware one. Do it at the boundary: parsing, reading from the database, building from user input. The interior of your program is then all aware, all internally consistent.

The [UTC everywhere](utc-everywhere.md) essay goes further: store everything in UTC, convert only at the display layer. That's a design rule, not just a defensive habit — and it's the one that makes cross-zone bugs structurally impossible rather than merely unlikely.

## The exceptions

Two places where naive is fine:

- **You genuinely don't care about zones.** A `date` (just year/month/day, no time) is inherently zone-less — what you mean by "21 April 2026" doesn't need disambiguation, as long as you accept that "the calendar day" is different in different zones anyway. For birthdays, anniversaries, calendar-day reporting, naive `date` is the right shape.
- **Wall-clock scheduling.** "Send this at 09:00 local" isn't a single moment — it's a different moment in every zone. A naive `datetime(9, 0, ...)` combined with per-user zone metadata is sometimes cleaner than trying to pre-compute aware instants.

Everything else: attach a zone. Python's type system is trying to help; let it.
