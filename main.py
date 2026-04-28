"""A Python RPG character system featuring a base Character class with six subclasses —
(Barbarian, Cleric, Wizard, Sorcerer, Fighter, Rogue)
Race-based stat bonuses, leveling, combat, inventory management, and character sheet export."""
from factory_methods import *
from character import *


class Barbarian(Character):
    def __init__(self, name, race):
        super().__init__(name, race)
        self.strength += 3
        self.constitution += 3
        self.intelligence -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Cleric(Character):
    def __init__(self, name, race):
        super().__init__()
        self.constitution += 3
        self.wisdom += 3
        self.charisma -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Wizard(Character):
    def __init__(self, name, race):
        super().__init__()
        self.intelligence += 3
        self.charisma += 3
        self.max_hp -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Sorcerer(Character):
    def __init__(self, name, race):
        super().__init__()
        self.wisdom += 3
        self.max_hp += 3
        self.dexterity -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Fighter(Character):
    def __init__(self, name, race):
        super().__init__()
        self.strength += 3
        self.charisma += 3
        self.wisdom -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Rogue(Character):
    def __init__(self, name, race):
        super().__init__()
        self.dexterity += 3
        self.intelligence += 3
        self.constitution -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()



jim = Barbarian.from_prompt()
dragon1 = DragonFactory().create()
# character = Barbarian()
#
# character.display_sheet()
#
dragon1.cause_dmg(jim)
#
# character.display_sheet()