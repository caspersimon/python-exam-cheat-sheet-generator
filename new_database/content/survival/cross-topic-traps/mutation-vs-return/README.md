# Mutation vs return value

> [!summary] Summary
> A single place to remember which operations change an object, which return a new value, and which return `None`.

> [!tip] Why this snippet matters
> A large share of wrong options fail because the code forgets that strings are immutable, that `append`/`sort`/`shuffle` mutate in place, or that some expressions return `None`.

## Metadata

- slug: `mutation-vs-return`
- topic: `survival`
- subtopic: `cross-topic-traps`
- course phase: `mixed`
- default priority: `5`
- difficulty: `beginner`
- recurrence: `signature`
- question refs: `6`
- traps: `3`

## Pieces

- `01` **Mutate / return / object after call** — `table` / `core` / default `yes`
- `02` **Minimal reminders** — `example` / `clarifier` / default `no`
- `03` **Fast trap signals** — `rules` / `trap` / default `yes`
