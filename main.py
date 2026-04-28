"""A Python RPG character system featuring a base Character class with six subclasses —
(Barbarian, Cleric, Wizard, Sorcerer, Fighter, Rogue)
Race-based stat bonuses, leveling, combat, inventory management, and character sheet export."""

from classes import *
from enemies import *

CLASSES = {
    "barbarian": Barbarian,
    "cleric": Cleric,
    "wizard": Wizard,
    "sorcerer": Sorcerer,
    "fighter": Fighter,
    "rogue": Rogue,
}

while True:
    try:
        amount = int(input("How many players? Enter a digit of up to 4. ").strip())
    except TypeError:
        print("Not a number, please try again.\n")
        continue
    if amount <= 0 or amount > 4:
        print("Not a valid amount, please try again.\n")
        continue
    amount = int(amount)
    break

players = {}
for num in range(1, amount + 1):
    while True:
        class_choice = (
            input(
                f"Which class for player #{num}?\nBarbarian, Cleric, Wizard, Sorcerer, Fighter, or Rogue "
            )
            .lower()
            .strip()
        )
        if class_choice not in ["barbarian", "cleric", "wizard", "sorcerer", "fighter", "rogue"]:
            print("Not a valid class option, please try again.\n")
            continue
        character = CLASSES[class_choice].from_prompt()
        players[character.name] = character
        break
print("The party:")
for player in players.values():
    print(f"{player.name} - {player.race} {player.class_name} - level {player.level}")
