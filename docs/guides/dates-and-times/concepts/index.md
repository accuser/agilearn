---
title: Concepts
---

# Concepts: Dates and times

Short essays on the ideas underneath datetime handling. Read these once and keep coming back to them when a time-related bug shows up — most of those bugs trace back to one of these two topics.

## Essays in this section

- **[Why naive datetimes are a footgun](why-naive-datetimes-are-a-footgun.md)** — the ambiguity in a datetime without a time zone, and why Python refuses to compare them with aware ones.
- **[UTC everywhere](utc-everywhere.md)** — the design rule that prevents most cross-zone bugs, why it works, and the situations where it doesn't apply.
