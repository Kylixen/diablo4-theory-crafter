#!/usr/bin/env bash
# Sparse-clone the theory-crafting-relevant slice of DiabloTools/d4data
# (datamined Diablo 4 game data parsed to JSON, ~9.8 GB in full) into
# data/d4data/. The data is gitignored — game data is Blizzard's property,
# so we fetch it locally rather than commit it.
set -euo pipefail

REPO_URL="https://github.com/DiabloTools/d4data.git"
DEST="$(cd "$(dirname "$0")/.." && pwd)/data/d4data"

# Game-balance & class data used to build the skills/items/paragon inventory,
# plus English string lists for human-readable names and descriptions.
SPARSE_PATHS=(
  json/base/meta/Affix
  json/base/meta/Aspect
  json/base/meta/CollectiblePower
  json/base/meta/GameBalance
  json/base/meta/GenericSkillTree
  json/base/meta/Item
  json/base/meta/ItemRequirement
  json/base/meta/ItemType
  json/base/meta/ParagonBoard
  json/base/meta/ParagonGlyph
  json/base/meta/ParagonGlyphAffix
  json/base/meta/ParagonNode
  json/base/meta/ParagonThreshold
  json/base/meta/PlayerClass
  json/base/meta/Power
  json/base/meta/PowerModifier
  json/base/meta/SetItemBonus
  json/base/meta/SkillKit
  json/enUS_Text/meta/StringList
)

if [ -d "$DEST/.git" ]; then
  echo "Updating existing checkout in $DEST"
  git -C "$DEST" fetch --depth 1 origin master
  git -C "$DEST" reset --hard origin/master
else
  echo "Cloning sparse slice of d4data into $DEST"
  git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$DEST"
  git -C "$DEST" sparse-checkout set "${SPARSE_PATHS[@]}"
fi

echo "Done. Game version: $(cat "$DEST/buildVersion.txt" 2>/dev/null || echo unknown)"
du -sh "$DEST"
