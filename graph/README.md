# Graph

Neo4j-backed knowledge graph over [`characters/`](../characters/) and
[`knowledge/`](../knowledge/): builds, skills, items, and mechanics as nodes,
with relationships like `USES`, `REQUIRES`, and `SYNERGIZES_WITH` — queried
with Cypher to answer questions like "which uniques enable a Bone Spear
build?"

Client-side/WASM exploration on GitHub Pages is parked as a future approach —
see [issue #1](https://github.com/Kylixen/diablo4-theory-crafter/issues/1).
For now Neo4j keeps things simple, with the built-in Neo4j Browser as the
query UI for streaming.

## Running

Requires Docker.

```sh
cd graph
docker compose up -d
```

- Neo4j Browser: http://localhost:7474 (login `neo4j` / `theorycraft`)
- Bolt (drivers, cypher-shell): `bolt://localhost:7687`

Data persists in the `neo4j-data` Docker volume across restarts.

## Loading the graph

Cypher scripts live in [`cypher/`](cypher/) and are mounted read-only into
the container at `/cypher`. Run one with:

```sh
docker exec d4-theory-graph cypher-shell -u neo4j -p theorycraft -f /cypher/<script>.cypher
```

Current scripts (see [`ontology.md`](ontology.md) for the model):

- `00-schema.cypher` — uniqueness constraints
- `10-classes-skills.cypher` — classes + active skills, GENERATED from
  `data/d4data` by [`scripts/extract_skills_classes.py`](../scripts/extract_skills_classes.py);
  re-run after each patch's data fetch, don't hand-edit
