# Diablo 4 Theory Crafter

Tracking Diablo 4 theory-crafting season over season: characters, builds, and
the underlying game knowledge that informs them. Built to stream — the goal
is to show the progression and reasoning behind builds over time, not just
the end result.

## Layout

- [`knowledge/`](knowledge/) — evergreen reference data (mechanics, items,
  skills). Not season-partitioned; edited in place, with git history as the
  record of what changed and when.
- [`characters/`](characters/) — builds and characters, one directory per
  season (e.g. `season-14/`). See [`characters/README.md`](characters/README.md)
  for the season-over-season convention.
- [`graph/`](graph/) — Rust workspace that turns `characters/` + `knowledge/`
  into a queryable graph, compiled to WASM so it can run client-side.
- [`site/`](site/) — static frontend, published via GitHub Pages, that loads
  the WASM graph module so viewers can explore builds the same way I do.

## Stack

The knowledge graph runs as SQLite queried live in the browser via
[`sqlite-wasm-rs`](https://crates.io/crates/sqlite-wasm-rs) (Rust compiled to
`wasm32-unknown-unknown`), rather than a hosted graph database like Neo4j —
that keeps the whole thing deployable as a static GitHub Pages site with no
backend to run or pay for.
