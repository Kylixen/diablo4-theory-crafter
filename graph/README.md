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

Any local Neo4j works. Primary setup is [Neo4j Desktop](https://neo4j.com/download/)
with a local DBMS on the default ports; [`docker-compose.yml`](docker-compose.yml)
remains as an alternative for anyone without Desktop (`cd graph && docker
compose up -d`, login `neo4j`/`theorycraft`).

- Neo4j Browser / HTTP: http://localhost:7474
- Bolt: `bolt://localhost:7687`

## Loading the graph

Cypher scripts live in [`cypher/`](cypher/), numbered by load order. Load
them all with:

```sh
python3 scripts/load_graph.py
```

Connection settings come from env vars or a gitignored `.env` in the repo
root (`NEO4J_URL`, `NEO4J_USER`, `NEO4J_PASSWORD` — see the script header).
The loader uses Neo4j's HTTP API, so it works the same against Desktop or
Docker, no `cypher-shell` needed. Scripts are idempotent (`MERGE`-based) —
re-running is safe.

Current scripts (see [`ontology.md`](ontology.md) for the model):

- `00-schema.cypher` — uniqueness constraints
- `10-classes-skills.cypher` — classes + active skills, GENERATED from
  `data/d4data` by [`scripts/extract_skills_classes.py`](../scripts/extract_skills_classes.py);
  re-run after each patch's data fetch, don't hand-edit
