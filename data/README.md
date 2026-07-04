# Data

Raw game data inventory, fetched locally — not committed (game data is
Blizzard's property; only the community parsing output's structure is
referenced here).

## d4data

`d4data/` is a sparse slice (~1 GB of the full ~10 GB repo) of
[DiabloTools/d4data](https://github.com/DiabloTools/d4data) (MIT-licensed
parser output): datamined Diablo 4 game files parsed to JSON, updated by the
community each patch.

Fetch or update it with:

```sh
./scripts/fetch-d4data.sh
```

What the slice includes (under `d4data/json/`):

- `base/meta/Power/` + `SkillKit/` — skills: one `.pow.json` per power, with
  mechanics and scaling formulas (~9,900 files)
- `base/meta/Affix/`, `Aspect/`, `SetItemBonus/` — gear affixes and legendary
  aspects
- `base/meta/Item/`, `ItemType/`, `ItemRequirement/` — items, incl. uniques
- `base/meta/Paragon*` — paragon boards, nodes, glyphs, thresholds
- `base/meta/PlayerClass/`, `GenericSkillTree/` — classes and skill trees
- `base/meta/GameBalance/`, `PowerModifier/`, `CollectiblePower/` — balance
  tables and misc powers
- `enUS_Text/meta/StringList/` — English names/tooltips (`.stl.json`), keyed
  by the same identifiers (e.g. `Power_Sorcerer_Fireball.stl.json` pairs with
  `Sorcerer_Fireball.pow.json`)

`d4data/buildVersion.txt` records which game patch the checkout corresponds
to. Internal identifiers (SNO ids) cross-reference between files; the
`StringList` entries carry the human-readable `name`/`desc` for each power,
affix, and item.
