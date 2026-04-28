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
    def __init__(self, name, race, max_hp, hit_dice):
        super().__init__(name, race, max_hp, hit_dice)
        self.constitution += 3
        self.wisdom += 3
        self.charisma -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Wizard(Character, Combatant):
    def __init__(self, name, race, max_hp, hit_dice):
        super().__init__(name, race, max_hp, hit_dice)
        self.intelligence += 3
        self.charisma += 3
        self.max_hp -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Sorcerer(Character, Combatant):
    def __init__(self, name, race, max_hp, hit_dice):
        super().__init__(name, race, max_hp, hit_dice)
        self.wisdom += 3
        self.max_hp += 3
        self.dexterity -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Fighter(Character, Combatant):
    def __init__(self, name, race, max_hp, hit_dice):
        super().__init__(name, race, max_hp, hit_dice)
        self.strength += 3
        self.charisma += 3
        self.wisdom -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Rogue(Character, Combatant):
    def __init__(self, name, race, max_hp, hit_dice):
        super().__init__(name, race, max_hp, hit_dice)
        self.dexterity += 3
        self.intelligence += 3
        self.constitution -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()



jim = Barbarian.from_prompt()

dragon1 = DragonFactory().create()

dragon1.cause_dmg(jim)
