# RPG Creator

`RPG Creator` is a command-line Python project for generating fantasy RPG characters and running a simple party-vs-enemy battle loop. The codebase focuses on a small set of tabletop-style mechanics: randomized stats, race and class bonuses, inventory, combat, experience gain, level-ups, character-sheet export, and character-sheet import.

## Features

- Import saved character sheets for zero to all party members (up to 6 total), then create any remaining members interactively.
- Create `Barbarian`, `Cleric`, `Wizard`, `Sorcerer`, `Fighter`, or `Rogue` characters interactively.
- Choose from `Human`, `Dwarf`, `Elf`, `Gnome`, and `Halfling`.
- Roll randomized HP and core ability scores, then apply race and class modifiers.
- Fight a chosen enemy type against a chosen enemy count.
- Track damage, pass-out state, inventory use, experience, and level progression.
- Miss chance in combat scales with dexterity for player characters and is fixed per enemy type.
- Experience rewards scale based on enemy difficulty.
- Export character sheets to `.txt` files and import them back into active play.

## Project Layout

| File | Purpose |
| --- | --- |
| `main.py` | Interactive entry point, import flow, and battle loop |
| `character.py` | Base character behavior, stats, inventory, XP, and export logic |
| `classes.py` | Playable classes and their stat adjustments |
| `combatant.py` | Shared combat behavior for characters and enemies |
| `enemies.py` | Enemy classes and factory helpers |
| `tests/` | Automated unit tests |
| `*_lvl*.txt` | Example exported character sheets |

Folders such as `.idea`, `.venv`, `.mypy_cache`, and `__pycache__` are development or runtime artifacts and are not required to understand the project itself.

## Requirements

- Python `3.10+`
- No third-party runtime dependencies

## Run

From the project folder:

```powershell
python main.py
```

## Run Tests

```powershell
python -m unittest discover -s tests -q
```

## Gameplay Flow

When you run `main.py`, the game will:

1. Ask how many players are in the party (1-6).
2. Ask whether to import character sheets.
3. If importing, repeatedly prompt for sheet filenames until you stop.
4. Create any remaining party members by choosing class, then entering name and race.
5. Print the party summary.
6. Ask how many enemies are present and which enemy type to spawn.
7. Run combat rounds (enemies attack first, then active players) until one side is defeated.
8. Offer to export the party's character sheets at the end.

## Playable Classes

| Class | Base Hit Dice | Extra Hit Dice Rule | Adjustments |
| --- | --- | --- | --- |
| Barbarian | `14` | `+ STR // 2` | `+3 STR`, `+3 CON`, `-3 INT` |
| Cleric | `8` | `+ CON // 2` | `+3 CON`, `+3 WIS`, `-3 CHA` |
| Wizard | `12` | `+ WIS // 2` | `+3 INT`, `+3 CHA`, `-3 STR` |
| Sorcerer | `14` | `+ INT // 2` | `+3 WIS`, `+3 INT`, `-3 DEX` |
| Fighter | `10` | `+ CHA // 2` | `+3 STR`, `+3 CHA`, `-3 WIS` |
| Rogue | `10` | `+ DEX // 2` | `+3 DEX`, `+3 INT`, `-3 CON` |

## Playable Races

| Race | Adjustments |
| --- | --- |
| Human | `+1 STR`, `+1 CON`, `+1 INT`, `+1 WIS`, `+1 CHA` |
| Dwarf | `+2 STR`, `+2 CON`, `+1 WIS` |
| Elf | `+2 DEX`, `+1 INT`, `+1 WIS`, `+1 CHA` |
| Gnome | `+2 DEX`, `+2 INT`, `+1 CON` |
| Halfling | `+2 DEX`, `+1 CON`, `+2 CHA` |

## Enemy Types

| Enemy | HP | Attack Die | Miss Chance | XP Multiplier |
| --- | --- | --- | --- | --- |
| Goblin | `10` | `d5` | `30%` | `1x` |
| Skeleton | `15` | `d10` | `20%` | `2x` |
| Dragon | `100` | `d30` | `10%` | `5x` |

## Miss Chance

Miss chance is checked at the start of every attack. A miss deals no damage and awards no experience.

For player characters, miss chance is derived from dexterity using the formula `80 - (dexterity * 4)`. Higher dexterity reduces the chance to miss. With a typical dexterity range of 7-18 across race/class outcomes, player miss chance is usually around 52% down to 8%.

For enemies, miss chance is a fixed value set per enemy type, as shown in the table above.

## Experience and Leveling

Characters earn experience on every successful hit. The amount scales with the difficulty of the enemy, using the XP multiplier shown in the enemy table.

Level-up thresholds scale linearly with current level (`50 * level`). On level-up, XP resets to `0`, core stats increase by a percentage of their current values, max HP increases based on constitution, and HP is fully restored.

## Creating Characters in Code

You can create characters directly without using the interactive prompts:

```python
from classes import Barbarian, Wizard

barbara = Barbarian("Barbara", "Dwarf")
david = Wizard("David", "Elf")
```

Or prompt interactively for a specific class:

```python
from classes import Rogue

player = Rogue.from_prompt()
```

## Character Export

Exported files use this naming pattern:

```text
Name_the_Race_class_lvl<level>.txt
```

Example:

```text
Barbara_the_Dwarf_barbarian_lvl1.txt
```

Each exported file contains the character sheet followed by the inventory list.

## Testing

This repository includes automated `unittest` coverage for core behavior such as:

- combat damage and experience gain
- item usage
- input validation in the main battle loop
- import reconstruction of saved state (inventory, experience, passed-out status)

## Current Limitations

- The import flow assumes the file matches this project's export format and does not currently handle malformed files with friendly errors.
- Imported class names are parsed from the file header and expected to match current class keys (lowercase names such as `fighter`, `rogue`, etc.).
- Each encounter supports only one enemy type.
- Character creation is fully randomized; there is no manual stat allocation.
- Exported character sheets are plain text only.

## Example Output

```text
Barbara - Dwarf barbarian - level 1
---------------------------------
Health: 19/20
Experience: 40
Strength: 14
Dexterity: 15
Constitution: 19
Intelligence: 7
Wisdom: 6
Charisma: 7
```
