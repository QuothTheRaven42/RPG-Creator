# RPG Creator

`RPG Creator` is a command-line Python project for generating fantasy RPG characters and running a simple party-vs-enemy battle loop. The codebase focuses on a small set of tabletop-style mechanics: randomized stats, race and class bonuses, inventory, combat, experience gain, level-ups, character-sheet export, and character-sheet import.

## Features

- Import a saved character sheet for any number of party members (up to the default maximum of 6).
- Create additional `Barbarian`, `Cleric`, `Wizard`, `Sorcerer`, `Fighter`, or `Rogue` characters interactively.
- Choose from `Human`, `Dwarf`, `Elf`, `Gnome`, and `Halfling`.
- Roll randomized HP and core ability scores, then apply race and class modifiers.
- Fight a chosen enemy type against a chosen enemy count.
- Track damage, pass-out state, inventory use, experience, and level progression.
- Miss chance in combat scales with dexterity for player characters and is fixed per enemy type.
- Experience rewards scale based on enemy difficulty.
- Export character sheets to `.txt` files.

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

1. Ask how many players are in the party.
2. Ask for the filename of a character sheet to import for the first party member.
3. Ask which class each additional player should use.
4. Prompt for each additional character's name and race.
5. Print the party summary.
6. Ask how many enemies are present and which enemy type to spawn.
7. Run the battle until either the party or enemy group is defeated.
8. Offer to export the party's character sheets at the end.

## Playable Classes

| Class | Hit Dice | Adjustments |
| --- | --- | --- |
| Barbarian | `20` | `+3 STR`, `+3 CON`, `-3 INT` |
| Cleric | `6` | `+3 CON`, `+3 WIS`, `-3 CHA` |
| Wizard | `8` | `+3 INT`, `+3 CHA`, `-3 max HP` |
| Sorcerer | `16` | `+3 WIS`, `+3 INT`, `-3 DEX` |
| Fighter | `14` | `+3 STR`, `+3 CHA`, `-3 WIS` |
| Rogue | `8` | `+3 DEX`, `+3 INT`, `-3 CON` |

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

For player characters, miss chance is derived from dexterity using the formula `80 - (dexterity * 5)`. Higher dexterity reduces the chance to miss. With a base dexterity range of `8–16` plus race bonuses, player miss chance typically falls between 30% and 5%.

For enemies, miss chance is a fixed value set per enemy type, as shown in the table above.

## Experience and Leveling

Characters earn experience on every successful hit. The amount scales with the difficulty of the enemy, using the XP multiplier shown in the enemy table. A Dragon kill is worth ten times the experience of a Goblin kill.

Level-up thresholds scale linearly with the current level. On level-up, all stats increase by a percentage of their current value and HP is fully restored.

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

## Current Limitations

- The CLI party flow currently asks about importing characters, imports up to 6 characters, and creates the remaining party members interactively.
- Each encounter supports only one enemy type.
- Character creation is fully randomized; there is no manual stat allocation.
- Exported character sheets are plain text only.

## Example Output

```text
Barbara - Dwarf barbarian - level 1
---------------------------------
Health: 19/20
Strength: 14
Dexterity: 15
Constitution: 19
Intelligence: 2
Wisdom: 6
Charisma: 7
```
