"""Create characters from Barbarian, Cleric, Wizard, Sorcerer, Fighter, and Rogue.
Includes stat bonuses for each class"""

from character import Character
from combatant import Combatant


class Barbarian(Character, Combatant):
    def __init__(self, name, race):
        super().__init__(name, race, 20)
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
        self.intelligence += 3
        self.dexterity -= 3
        self.current_hp: int = self.max_hp
        self.display_sheet()


class Fighter(Character, Combatant):
    def __init__(self, name, race):
        super().__init__(name, race, 14)
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
