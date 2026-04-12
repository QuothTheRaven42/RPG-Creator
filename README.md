# RPG Character Generator

A command-line RPG character creation system built in Python. Choose a class, pick a race, and get a fully generated character sheet with randomized stats, race and class bonuses, and a starting inventory. Includes a full set of interactive methods for combat, leveling, inventory management, and more.

## Features

- 6 playable classes: Barbarian, Cleric, Wizard, Sorcerer, Fighter, Rogue
- 5 playable races: Human, Dwarf, Elf, Gnome, Halfling — each with unique stat bonuses
- Randomized base stats (strength, dexterity, constitution, intelligence, wisdom, charisma)
- Class bonuses applied on top of race bonuses at creation
- Starting inventory with health potions, rope, torches, water, and rations
- Experience and leveling system — stats scale up on level up
- Combat methods for dealing and receiving damage
- Item system with functional healing potions
- Export your character sheet to a `.txt` file

## Requirements

- Python 3.10+
- No external dependencies

## Usage

Import the class you want and instantiate it:

```python
from character import Barbarian, Wizard, Rogue  # etc.

player = Barbarian()
```

You'll be prompted to enter a name and choose a race. Your character sheet is displayed automatically after creation.

## Available Methods

| Method | Description |
|--------|-------------|
| `display_sheet()` | Print the character sheet to the terminal |
| `export_char_sheet()` | Save the character sheet and inventory to a `.txt` file |
| `gain_exp(multiplier)` | Gain experience points; triggers level up at threshold |
| `take_dmg(dmg)` | Receive damage and update HP |
| `cause_dmg(target)` | Attack another Character instance |
| `rest()` | Restore HP to max and recover from passing out |
| `use_item(item)` | Use an item from inventory; healing items restore HP |
| `add_item(item)` | Add an item to inventory |
| `view_inventory()` | Print current inventory to the terminal |
| `roll_dice(d_num)` | Static method — roll a die with the given number of sides |

## Classes and Stat Bonuses

| Class | Bonuses | Penalties |
|-------|---------|-----------|
| Barbarian | +3 STR, +3 CON | -3 INT |
| Cleric | +3 CON, +3 WIS | -3 CHA |
| Wizard | +3 INT, +3 CHA | -3 HP |
| Sorcerer | +3 WIS, +3 HP | -3 DEX |
| Fighter | +3 STR, +3 CHA | -3 WIS |
| Rogue | +3 DEX, +3 INT | -3 CON |

## Races and Stat Bonuses

| Race | Bonuses |
|------|---------|
| Human | +1 STR, CON, INT, WIS, CHA |
| Dwarf | +2 STR, +2 CON, +1 WIS |
| Elf | +2 DEX, +1 INT, +1 WIS, +1 CHA |
| Gnome | +2 DEX, +2 INT, +1 CON |
| Halfling | +2 DEX, +1 CON, +2 CHA |

## Example

```
What is your fighter's name? Aldric
Choose a race: Human

Aldric - Human fighter - level 1
---------------------------------
Health: 15/15
Strength: 14
Dexterity: 9
...
```
