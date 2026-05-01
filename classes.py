"""Playable RPG character classes and their class-specific stat adjustments."""

from character import Character
from combatant import Combatant


class Barbarian(Character, Combatant):
    """Player character class focused on strength and constitution."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a barbarian and optionally print its character sheet."""
        super().__init__(name, race, 20)
        self.strength += 3
        self.constitution += 3
        self.intelligence -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Cleric(Character, Combatant):
    """Player character class focused on constitution and wisdom."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a cleric and optionally print its character sheet."""
        super().__init__(name, race, 6)
        self.constitution += 3
        self.wisdom += 3
        self.charisma -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Wizard(Character, Combatant):
    """Player character class focused on intelligence and charisma."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a wizard and optionally print its character sheet."""
        super().__init__(name, race, 8)
        self.intelligence += 3
        self.charisma += 3
        self.max_hp -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Sorcerer(Character, Combatant):
    """Player character class focused on wisdom and intelligence."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a sorcerer and optionally print its character sheet."""
        super().__init__(name, race, 16)
        self.wisdom += 3
        self.intelligence += 3
        self.dexterity -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Fighter(Character, Combatant):
    """Player character class focused on strength and charisma."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a fighter and optionally print its character sheet."""
        super().__init__(name, race, 14)
        self.strength += 3
        self.charisma += 3
        self.wisdom -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Rogue(Character, Combatant):
    """Player character class focused on dexterity and intelligence."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a rogue and optionally print its character sheet."""
        super().__init__(name, race, 8)
        self.dexterity += 3
        self.intelligence += 3
        self.constitution -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()
