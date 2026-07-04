#!/usr/bin/env python3
"""Load graph/cypher/*.cypher into Neo4j over the HTTP API, in filename order.

Connection comes from env vars (or a gitignored .env file in the repo root):
  NEO4J_URL      default http://localhost:7474
  NEO4J_USER     default neo4j
  NEO4J_PASSWORD required

Works against any Neo4j (Desktop, Docker, server) — no cypher-shell needed.
"""

import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CYPHER_DIR = ROOT / "graph" / "cypher"
BATCH = 200


def load_env():
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def statements(path):
    """Split a .cypher file into statements: strip // comments, split on ';'."""
    text = "\n".join(
        l for l in path.read_text().splitlines() if not l.lstrip().startswith("//")
    )
    return [s.strip() for s in text.split(";") if s.strip()]


def main():
    load_env()
    url = os.environ.get("NEO4J_URL", "http://localhost:7474")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD")
    if not password:
        sys.exit("Set NEO4J_PASSWORD (env or .env file)")

    auth = base64.b64encode(f"{user}:{password}".encode()).decode()
    endpoint = f"{url}/db/neo4j/tx/commit"

    def post(stmts):
        body = json.dumps(
            {"statements": [{"statement": s} for s in stmts]}
        ).encode()
        req = urllib.request.Request(
            endpoint,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {auth}",
            },
        )
        with urllib.request.urlopen(req) as resp:
            result = json.load(resp)
        if result.get("errors"):
            sys.exit(f"Neo4j error: {result['errors'][0]}")

    for path in sorted(CYPHER_DIR.glob("*.cypher")):
        stmts = statements(path)
        for i in range(0, len(stmts), BATCH):
            post(stmts[i : i + BATCH])
        print(f"loaded {path.name}: {len(stmts)} statements")


if __name__ == "__main__":
    main()
