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
- [`graph/`](graph/) — Neo4j knowledge graph over `characters/` +
  `knowledge/`, queried with Cypher. Runs locally via Docker; the Neo4j
  Browser is the exploration UI.
- [`data/`](data/) — raw game data (skills, items, affixes, paragon) fetched
  locally from [DiabloTools/d4data](https://github.com/DiabloTools/d4data)
  via [`scripts/fetch-d4data.sh`](scripts/fetch-d4data.sh); gitignored, see
  [`data/README.md`](data/README.md).

## Stack

Neo4j (Docker, local) with Cypher queries — chosen for simplicity. A
client-side alternative (a Rust openCypher engine compiled to WASM, so
viewers could run the same queries on a static GitHub Pages site) was spiked
successfully and is parked as a future approach in
[issue #1](https://github.com/Kylixen/diablo4-theory-crafter/issues/1).
