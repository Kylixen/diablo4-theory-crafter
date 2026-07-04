# Graph ontology

Versioned design for the knowledge graph. v0.1 covers classes and active
skills; items, aspects, paragon, and builds come later.

## v0.1 — Classes & Skills

```
(:Class {name, snoId})
(:Skill {name, internalName, snoId})
(:SkillCategory {name})
(:Tag {name})

(:Class)-[:HAS_SKILL {levelReq}]->(:Skill)
(:Skill)-[:IN_CATEGORY]->(:SkillCategory)
(:Skill)-[:TAGGED]->(:Tag)
```

### Nodes

- **Class** — the 8 playable classes. `snoId` is the game's internal SNO id
  (stable across patches, the join key throughout d4data).
- **Skill** — player-assignable active skills (~198). Sourced from each
  class's SkillKit `arActiveSkillEntries`, which is the curated in-game
  skill list — this sidesteps the ~9,900 raw Power files, most of which are
  monster/item/test powers. `internalName` is the d4data identifier (e.g.
  `Sorcerer_Fireball`); `name` is the localized English name (e.g.
  `Fireball`).
- **SkillCategory** — the skill-tree grouping, from the power's
  `tPrimaryTag` (`Skill_Primary_*`). Shared categories (Basic, Core,
  Defensive, Ultimate) plus class-specific ones (Justice, Valor, Macabre,
  Brawling, …).
- **Tag** — descriptive mechanics/element tags from `arSkillTags`
  (`Skill_Fire`, `Skill_Mobility`, `Skill_Channeled`, `Skill_Shapeshifting`,
  …). Search-only tags (`bSearchOnly: true`) are excluded.

### Relationships

- **HAS_SKILL** — carries `levelReq` (character level the skill unlocks at,
  from `nLevelReq`).
- **IN_CATEGORY** — exactly one per skill (the primary tag).
- **TAGGED** — zero or more per skill.

### Conventions

- Node identity: `snoId` for Class/Skill (game-stable); `name` for
  SkillCategory/Tag (they have no SNO).
- Tag/category names are stored stripped of their prefixes:
  `Skill_Primary_Core` → `Core`, `Skill_Fire` → `Fire`.
- Everything is regenerable from `data/d4data` via
  `scripts/extract_skills_classes.py` — the graph is a projection of the
  data, never hand-edited, so a new patch just means re-fetch + re-extract.

### Example questions this answers

```cypher
// What Fire skills exist, and for which classes?
MATCH (c:Class)-[:HAS_SKILL]->(s:Skill)-[:TAGGED]->(:Tag {name: 'Fire'})
RETURN c.name, s.name;

// Mobility skills unlocked by level 10
MATCH (c:Class)-[h:HAS_SKILL]->(s:Skill)-[:TAGGED]->(:Tag {name: 'Mobility'})
WHERE h.levelReq <= 10
RETURN c.name, s.name, h.levelReq;
```

## Future versions (not yet modeled)

- v0.2: Items, Aspects, Uniques — `(:Aspect)-[:MODIFIES]->(:Skill)`
- v0.3: Paragon boards, nodes, glyphs
- v0.4: Builds/characters from `characters/season-*` —
  `(:Build)-[:USES]->(:Skill)`, snapshots over time
- Passive skills (skill-tree passives referenced by `arNodes`)
- Skill upgrades/enhancements (Enhanced/branch variants)
