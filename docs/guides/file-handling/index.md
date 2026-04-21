---
title: File handling
---

# File handling

Reading and writing files is where a lot of real Python work happens — logs, spreadsheets, configuration, exported data. The mechanics look simple (`open`, read, write, close) but the interesting part is everything the mechanics protect you from: encodings, partial reads, forgotten closes, paths that only work on one operating system. This guide takes you through the tools Python gives you for all of that, and the concepts behind them.

## Start here

If file I/O is new to you, work through the [**Learn**](learn/) section in order — four short notebooks, around fifteen minutes each. Every code cell can be edited and run in place, directly on the page; no install required.

If you already know the basics and are looking for a specific technique, jump to the [**Recipes**](recipes/) section, or scan the [**Reference**](reference/) for `open` modes and `pathlib` methods.

## What this guide covers

**[Learn](learn/)** — reading files, writing files, `pathlib`, CSV and JSON.

**[Recipes](recipes/)** — processing large files, binary files, temporary files, common mistakes to avoid.

**[Reference](reference/)** — `open()` options, file modes, `pathlib` methods.

**[Concepts](concepts/)** — why context managers matter, and how file encodings shape what you can read.
