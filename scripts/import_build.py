#!/usr/bin/env python3
"""Import a Maxroll D4Planner build into characters/season-<N>/.

Usage:
    python3 scripts/import_build.py https://maxroll.gg/d4/planner/pv28we0x [--variant N]

Fetches the planner profile from planners.maxroll.gg, decodes numeric ids
(class, skill-tree nodes) via Maxroll's game data file, and writes a
character snapshot JSON. Re-running overwrites the file — git history is
the progression record.
"""

import argparse
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE_URL = "https://planners.maxroll.gg/profiles/d4/{}"
GAME_DATA_URL = "https://assets-ng.maxroll.gg/d4-tools/game/data.min.json"
GAME_DATA_CACHE = ROOT / "data" / "maxroll-data.json"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def game_data():
    if not GAME_DATA_CACHE.exists():
        print("fetching maxroll game data (cached after first run)...")
        GAME_DATA_CACHE.parent.mkdir(exist_ok=True)
        GAME_DATA_CACHE.write_bytes(fetch(GAME_DATA_URL))
    return json.load(open(GAME_DATA_CACHE))


def skill_node_index(gd):
    """node id -> {power, ranks} across all class skill trees."""
    index = {}
    for tree in gd["skillTrees"].values():
        def walk(obj):
            if isinstance(obj, dict):
                if "id" in obj and isinstance(obj.get("reward"), dict):
                    index[obj["id"]] = obj["reward"]
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)
        walk(tree)
    return index


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("planner", help="Maxroll planner URL or id (e.g. pv28we0x)")
    ap.add_argument("--variant", type=int, default=None,
                    help="profile variant index (default: planner's active profile)")
    args = ap.parse_args()

    m = re.search(r"(?:planner/)?([a-z0-9]+)(?:#(\d+))?$", args.planner)
    if not m:
        sys.exit(f"can't parse planner id from: {args.planner}")
    planner_id = m.group(1)
    variant = args.variant if args.variant is not None else (
        int(m.group(2)) - 1 if m.group(2) else None)

    doc = json.loads(fetch(PROFILE_URL.format(planner_id)))
    data = json.loads(doc["data"]) if isinstance(doc["data"], str) else doc["data"]
    idx = variant if variant is not None else data.get("activeProfile", 0)
    try:
        profile = data["profiles"][idx]
    except IndexError:
        sys.exit(f"variant {idx} not found; planner has {len(data['profiles'])} profiles")

    gd = game_data()
    nodes = skill_node_index(gd)
    class_name = gd["classes"].get(str(profile.get("class")), {}).get("nameMale",
                                                                      f"class#{profile.get('class')}")

    # decode skill tree: active step's {nodeId: rank} -> power names
    tree = profile.get("skillTree") or {}
    steps = tree.get("steps") or []
    step = steps[tree.get("position", 0)] if steps else {}
    allocations = []
    for node_id, rank in sorted((step.get("data") or {}).items(), key=lambda kv: int(kv[0])):
        reward = nodes.get(int(node_id), {})
        allocations.append({
            "power": reward.get("power", f"node#{node_id}"),
            "rank": rank,
        })

    snapshot = {
        "source": f"https://maxroll.gg/d4/planner/{planner_id}",
        "variant": profile.get("name"),
        "synced": date.today().isoformat(),
        "plannerName": doc.get("name"),
        "class": class_name,
        "level": profile.get("level"),
        "worldTier": profile.get("worldTier"),
        "season": profile.get("season"),
        "skillBar": profile.get("skillBar") or [],
        "skillTree": allocations,
        # not yet decoded — stored raw so nothing is lost between syncs
        "raw": {
            "items": profile.get("items") or {},
            "paragon": profile.get("paragon") or {},
            "spiritBoons": profile.get("spiritBoons"),
            "mercenary": profile.get("mercenary"),
        },
    }

    season = profile.get("season") or doc.get("season")
    out_dir = ROOT / "characters" / f"season-{season}"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", (doc.get("name") or planner_id).lower()).strip("-")
    out = out_dir / f"{slug}.json"
    out.write_text(json.dumps(snapshot, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)} "
          f"({class_name} lvl {snapshot['level']}, {len(allocations)} tree nodes, "
          f"{len(snapshot['skillBar'])} bar skills)")


if __name__ == "__main__":
    main()
