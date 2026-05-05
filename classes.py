"""Playable RPG classes and their class-specific stat adjustments.

Each subclass applies a lightweight archetype identity (stat boosts/penalties)
on top of :class:`Character` so gameplay differences are easy to reason about.
"""

from character import Character
from combatant import Combatant


class Barbarian(Character, Combatant):
    """Frontline class with high strength and durability."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a barbarian and optionally print its character sheet."""
        super().__init__(name, race, 20)
        # Tradeoff model: stronger melee and survivability, weaker caster aptitude.
        self.strength += 3
        self.constitution += 3
        self.intelligence -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Cleric(Character, Combatant):
    """Support class emphasizing wisdom and toughness."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a cleric and optionally print its character sheet."""
        super().__init__(name, race, 6)
        # Tradeoff model: improved sustain and utility, lower social pressure stat.
        self.constitution += 3
        self.wisdom += 3
        self.charisma -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Wizard(Character, Combatant):
    """Caster class with high mental stats and lower durability."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a wizard and optionally print its character sheet."""
        super().__init__(name, race, 8)
        # Tradeoff model: stronger spell potential for reduced survivability.
        self.intelligence += 3
        self.charisma += 3
        self.max_hp -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Sorcerer(Character, Combatant):
    """Magic class with strong mental stats and weaker agility."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a sorcerer and optionally print its character sheet."""
        super().__init__(name, race, 16)
        # Tradeoff model: elevated casting stats at the cost of dexterity.
        self.wisdom += 3
        self.intelligence += 3
        self.dexterity -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Fighter(Character, Combatant):
    """Balanced martial class with strong offense."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a fighter and optionally print its character sheet."""
        super().__init__(name, race, 14)
        # Tradeoff model: better offense/leadership, lower wisdom checks.
        self.strength += 3
        self.charisma += 3
        self.wisdom -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Rogue(Character, Combatant):
    """Skirmisher class emphasizing precision and cleverness."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a rogue and optionally print its character sheet."""
        super().__init__(name, race, 8)
        # Tradeoff model: mobility and utility at the cost of raw toughness.
        self.dexterity += 3
        self.intelligence += 3
        self.constitution -= 3
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()
