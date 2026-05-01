# RPG Creator

`RPG Creator` is a command-line Python project for generating fantasy RPG characters and running a simple party-vs-enemy battle loop. The codebase focuses on a small set of tabletop-style mechanics: randomized stats, race and class bonuses, inventory, combat, experience gain, level-ups, and character-sheet export.

## Features

- Create a party of `1` to `6` player characters.
- Play as `Barbarian`, `Cleric`, `Wizard`, `Sorcerer`, `Fighter`, or `Rogue`.
- Choose from `Human`, `Dwarf`, `Elf`, `Gnome`, and `Halfling`.
- Roll randomized HP and core ability scores, then apply race and class modifiers.
- Fight a chosen enemy type against a chosen enemy count.
- Track damage, pass-out state, inventory use, experience, and level progression.
- Export character sheets to `.txt` files.

## Project Layout

| File | Purpose |
| --- | --- |
| `main.py` | Interactive entry point and battle loop |
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
2. Ask which class each player should use.
3. Prompt for each character's name and race.
4. Print each generated character sheet.
5. Ask how many enemies are present and which enemy type to spawn.
6. Run the battle until either the party or enemy group is defeated.
7. Offer to export the party's character sheets at the end.

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

| Enemy | HP | Attack Die |
| --- | --- | --- |
| Goblin | `10` | `d5` |
| Skeleton | `15` | `d10` |
| Dragon | `100` | `d30` |

Battles currently use one enemy instance at a time and a counter that tracks how many of that enemy type remain in the encounter.

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

- `import_character()` exists in `main.py`, but it is still unfinished and is not currently wired into `battle_loop()`.
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
