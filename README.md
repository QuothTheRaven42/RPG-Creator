# RPG Character Generator
A command-line RPG character creation and combat system built in Python. Choose a class, pick a race, and get a fully generated character sheet with randomized stats, race and class bonuses, and a starting inventory. Includes a full set of interactive methods for combat, leveling, inventory management, and more.

The project also includes an enemy spawning system built with the Factory Method design pattern, with a shared combat base class used by both player characters and enemies.

## Project Structure
| File | Description |
|------|-------------|
| `character.py` | Player character base class and all playable subclasses |
| `classes.py` | Character classes for player characters.
| `combatant.py` | Shared base class for combat behavior — used by both characters and enemies |
| `enemies.py` | Enemy classes and factories built with the Factory Method pattern |
| `main.py` | Entry point for running the project |

## Features
- 6 playable classes: Barbarian, Cleric, Wizard, Sorcerer, Fighter, Rogue
- 5 playable races: Human, Dwarf, Elf, Gnome, Halfling — each with unique stat bonuses
- Randomized base stats (strength, dexterity, constitution, intelligence, wisdom, charisma)
- Class and race bonuses applied at character creation
- Starting inventory with health potions, rope, torches, water, and rations
- Experience and leveling system — stats scale on level up
- Shared combat system via `Combatant` base class
- Enemy spawning via Factory Method pattern
- 3 enemy types: Goblin, Skeleton, Dragon — each with fixed HP and hit dice
- Export character sheet to a `.txt` file

## Requirements
- Python 3.10+
- No external dependencies

## Usage

**Player characters** — instantiate using `from_prompt()` to be guided through name and race selection:
```python
from character import Barbarian

jim = Barbarian.from_prompt()
```

**Enemies** — use a factory to spawn an enemy instance:
```python
from factory_methods import DragonFactory, spawn_enemy

dragon = spawn_enemy(DragonFactory())
```

**Combat:**
```python
dragon.cause_dmg(jim)
jim.cause_dmg(dragon)
```

## Available Methods

### Player Characters
| Method | Description |
|--------|-------------|
| `display_sheet()` | Print the character sheet to the terminal |
| `export_char_sheet()` | Save the character sheet and inventory to a `.txt` file |
| `rest()` | Restore HP to max and recover from passing out |
| `use_item(item)` | Use an item from inventory; healing items restore HP |
| `add_item(item)` | Add an item to inventory |
| `view_inventory()` | Print current inventory to the terminal |

### All Combatants (Characters and Enemies)
| Method | Description |
|--------|-------------|
| `cause_dmg(target)` | Attack another Combatant instance |
| `take_dmg(dmg)` | Receive damage and update HP |
| `gain_exp(multiplier)` | Gain experience points; triggers level up at threshold (characters only) |
| `roll_dice(d_num)` | Static method — roll a die with the given number of sides |

## Playable Classes and Stat Bonuses
| Class | Bonuses | Penalties |
|-------|---------|-----------|
| Barbarian | +3 STR, +3 CON | -3 INT |
| Cleric | +3 CON, +3 WIS | -3 CHA |
| Wizard | +3 INT, +3 CHA | -3 HP |
| Sorcerer | +3 WIS, +3 HP | -3 DEX |
| Fighter | +3 STR, +3 CHA | -3 WIS |
| Rogue | +3 DEX, +3 INT | -3 CON |

## Playable Races and Stat Bonuses
| Race | Bonuses |
|------|---------|
| Human | +1 STR, CON, INT, WIS, CHA |
| Dwarf | +2 STR, +2 CON, +1 WIS |
| Elf | +2 DEX, +1 INT, +1 WIS, +1 CHA |
| Gnome | +2 DEX, +2 INT, +1 CON |
| Halfling | +2 DEX, +1 CON, +2 CHA |

## Enemies
| Enemy | HP | Hit Dice |
|-------|----|----------|
| Goblin | 10 | d5 |
| Skeleton | 15 | d10 |
| Dragon | 100 | d30 |

## Example
```
What is your Barbarian's name? Jim
Choose a race: Human

Jim - Human barbarian - level 1
---------------------------------
Health: 17/17
Strength: 16
Dexterity: 9
Constitution: 14
Intelligence: 5
Wisdom: 10
Charisma: 10
```
