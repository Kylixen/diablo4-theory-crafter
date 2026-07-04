# Characters & Builds

One directory per season: `season-14/`, `season-15/`, etc. Each holds the
characters/builds played that season.

Convention:

- Starting a new season: copy forward whichever builds carry over from the
  prior season's directory, then edit in place as the build evolves.
- Builds that don't carry over just don't get copied — no need to delete
  anything retroactively, the old season directory stays as history.
- Season directories are what the graph in [`graph/`](../graph/) ingests, so
  keep file naming/structure consistent across seasons (see whatever
  convention the first populated season settles on).

## Syncing from Maxroll

Builds are maintained in the [Maxroll D4Planner](https://maxroll.gg/d4/planner)
and synced here manually:

```sh
python3 scripts/import_build.py https://maxroll.gg/d4/planner/<id>
```

This writes `season-<N>/<planner-name>.json` (skill bar and skill tree
decoded to the game's internal power names — the same `internalName` ids the
graph uses; items/paragon kept raw for now). Re-running overwrites the
snapshot, so git history is the progression record: sync, commit, repeat.
