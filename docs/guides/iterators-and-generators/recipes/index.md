---
title: Recipes
---

# Recipes: Iterators and generators

Task-focused how-tos. If you know what you want to do but aren't sure how to build it, this is the section to skim.

## Recipes in this section

- **[Process a large file lazily](process-a-large-file-lazily.ipynb)** — streaming a file line by line (or record by record) without loading it all into memory. The pattern that lets you process multi-gigabyte inputs on a laptop.
- **[Chain and group iterables](chain-and-group-iterables.ipynb)** — `itertools.chain` for concatenation, `groupby` for runs of adjacent equal values, `zip` and `zip_longest` for parallel iteration.
- **[Combine generators into a pipeline](combine-generators.ipynb)** — stacking `filter → transform → window → aggregate` as generators that feed each other. The functional-pipeline style for data processing.
- **[Avoid common iterator mistakes](avoid-common-iterator-mistakes.md)** — a catalogue of the gotchas: once-consumed iterators, mutating during iteration, generator-inside-a-try, late binding in generator expressions.
