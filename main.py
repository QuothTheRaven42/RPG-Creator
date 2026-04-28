"""A Python RPG character system featuring a base Character class with six subclasses —
(Barbarian, Cleric, Wizard, Sorcerer, Fighter, Rogue)
Race-based stat bonuses, leveling, combat, inventory management, and character sheet export."""
from factory_methods import *
from combatant import *


class Barbarian(Character, Combatant):
    def __init__(self, name, race):
        super().__init__(name, race, 12)
        self.strength += 3
        self.constitution += 3
        self.intelligence -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Cleric(Character, Combatant):
    def __init__(self, name, race):
        super().__init__(name, race, 6)
        self.constitution += 3
        self.wisdom += 3
        self.charisma -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Wizard(Character, Combatant):
    def __init__(self, name, race):
        super().__init__(name, race, 8)
        self.intelligence += 3
        self.charisma += 3
        self.max_hp -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Sorcerer(Character, Combatant):
    def __init__(self, name, race):
        super().__init__(name, race, 16)
        self.wisdom += 3
        self.max_hp += 3
        self.dexterity -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Fighter(Character, Combatant):
    def __init__(self, name, race):
        super().__init__(name, race, 20)
        self.strength += 3
        self.charisma += 3
        self.wisdom -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Rogue(Character, Combatant):
    def __init__(self, name, race):
        super().__init__(name, race, 8)
        self.dexterity += 3
        self.intelligence += 3
        self.constitution -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


CLASSES = {'barbarian': Barbarian, 'cleric': Cleric, 'wizard': Wizard, 'sorcerer': Sorcerer, 'fighter': Fighter, 'rogue': Rogue }


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
for num in range(1, amount+1):
    while True:
        class_choice = input(
            f"Which class for player #{num}?\nBarbarian, Cleric, Wizard, Sorcerer, Fighter, or Rogue "
        ).strip()
        if class_choice not in ['barbarian', 'cleric', 'wizard', 'sorcerer', 'fighter', 'rogue']:
            print("Not a valid class option, please try again.\n")
            continue
        character = CLASSES[class_choice].from_prompt()
        players[character.name] = character
        break
print('The party:')
for player in players.values():
    print(f'{player.name} - {player.race} {player.class_name} - level {player.level}')

