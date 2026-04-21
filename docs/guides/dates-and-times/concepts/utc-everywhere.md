---
title: UTC everywhere
---

# UTC everywhere

There's a design rule that prevents most cross-zone datetime bugs. It's one sentence long:

> Store all datetimes in UTC. Convert to local time only at the display layer.

This essay is about why that rule works and when it doesn't apply.

## The rule

Every datetime inside your system — in memory, in the database, in logs, in serialised payloads sent between services — is aware and in UTC. The only places local time zones appear are:

1. **On input**, when a user types `"09:00"` meaning local time: attach their zone, then convert to UTC.
2. **On output**, when displaying a UTC timestamp to a human: convert to their local zone for the render.

Between those two boundaries, everything is UTC. No arithmetic on local times, no storage of local times, no comparison between different zones.

## Why it works

The problems with time zones come from *mixing* them. Two events stored in two different zones are hard to compare — you have to convert one of them before the comparison is meaningful. Ten events in ten zones are harder still. The cost is combinatorial, and as soon as one event is naive (no zone), everything breaks.

UTC everywhere collapses that. Every stored datetime shares a common reference frame. Comparison, arithmetic, sorting — all of it just works, because they're all in the same zone.

It's the same argument as ISO 8601 for date strings: picking a single canonical form, even if it's not the one humans want to see, makes everything downstream simpler.

## Why specifically UTC?

UTC has two properties that matter:

- **No DST.** A UTC hour is a UTC hour, always, with no "spring forward" or "fall back" edge cases.
- **No political changes.** National time zones occasionally shift (countries abolish DST, change their offset, redraw boundaries). UTC is defined by atomic clocks, not governments.

You could pick any fixed-offset zone and get most of the benefit. UTC is the conventional choice — it's the one every tool, library, and protocol assumes by default.

## The conversion rules

| Direction | Pattern |
| --- | --- |
| Local input → UTC storage | `user_time.replace(tzinfo=user_zone).astimezone(utc)` — if the input is naive and you know which zone it represents |
| UTC storage → local display | `stored.astimezone(user_zone)` |
| UTC arithmetic | Do it on UTC-aware datetimes. Never on local times — DST silently changes the answer. |

The `replace(tzinfo=...)` call is doing something subtle: it's *attaching* a zone to a naive datetime without changing the clock values. Use `astimezone` to convert; use `replace` to tag.

## DST and why this rule matters

DST is the reason this rule exists. Local-time arithmetic across a DST boundary is broken: adding 24 hours to `10:00 on spring-forward day` could give you `10:00 the next day` (what humans expect) or `11:00 the next day` (what the physical clock does). Both are correct for different definitions of "24 hours later". The ambiguity is baked into local time.

UTC has no DST. `10:00 UTC + 24 hours = 10:00 UTC the next day`, full stop. Convert to local only at render time, and the DST edge cases become a rendering problem, not a data problem.

## When the rule doesn't apply

A few cases where UTC everywhere is the wrong answer:

- **Wall-clock scheduling.** "Send this at 09:00 local each day" is a recurring local event, not a UTC instant. Each day, 09:00 London is a different UTC time (DST shifts the offset twice a year). The right model here is "zone + wall-clock time", with the UTC instant computed per occurrence.
- **Calendar-day reporting.** "How many users signed up on 21 April 2026" isn't a UTC-instant question — it's a calendar-day question, and the answer depends on whose calendar you're using. Store the timestamp in UTC as usual, but compute the calendar-day in the relevant zone (the user's, or the company's, or the report's) at query time.
- **Historical data.** Some databases store timestamps in "the server's local time" with no zone information. You inherit that naivety. Either convert to UTC on read (if you know what zone the data came from) or keep it naive and handle the caveats.

## Relationship to types

The rule maps cleanly onto types:

- At the boundary (parsing, user input, deserialisation): construct aware UTC datetimes immediately.
- Internal function signatures accept and return aware datetimes.
- At render: convert to the user's local zone and format.

If you lint `datetime` values with type-checkers, a naive one inside your system is a bug — an API somewhere didn't apply the rule. In practice this works well: most of the bugs come from *inconsistency*, and the rule is a way to enforce consistency structurally.

## The summary

The rule is three lines:

1. On input: attach the source zone, convert to UTC.
2. Inside the system: everything is UTC.
3. On output: convert to the user's local zone.

Every cross-zone datetime bug you've ever seen is a violation of one of those three. Apply them consistently and most of the category of bugs disappears.
