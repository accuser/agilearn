---
title: Dates and times
---

# Dates and times

Every application that logs, schedules, or processes data eventually has to deal with time — and time is a surprisingly large topic. Python's `datetime` module is adequate but lean; most of the footguns come from the interaction between naive and time-zone-aware datetimes, parsing inconsistent inputs, and DST transitions. This guide covers the mechanics, the idioms, and the traps.

## Start here

If you're new to `datetime`, work through the [**Learn**](learn/) section in order — three short notebooks, around fifteen to twenty minutes each. Every code cell can be edited and run in place, directly on the page; no install required.

If you already know the basics and are looking for a specific technique, jump to the [**Recipes**](recipes/) section, or scan the [**Reference**](reference/) for format codes and common patterns.

## What this guide covers

**[Learn](learn/)** — `date`, `time`, `datetime`, and `timedelta`; parsing and formatting with ISO 8601 and `strptime`/`strftime`; time zones with `zoneinfo`.

**[Recipes](recipes/)** — parsing a messy date column, computing durations and ages, converting between time zones, and avoiding common mistakes.

**[Reference](reference/)** — the full table of `strftime`/`strptime` format codes, `timedelta` arithmetic patterns, and `zoneinfo` usage.

**[Concepts](concepts/)** — why naive datetimes are a footgun, and the "UTC everywhere" design rule (and when it doesn't apply).
