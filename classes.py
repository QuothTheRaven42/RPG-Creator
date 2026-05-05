"""Playable RPG classes and their class-specific stat adjustments.

Each subclass applies a lightweight archetype identity (stat boosts/penalties)
on top of :class:`Character` so gameplay differences are easy to reason about.

Guards against stats going below 7 so they grow on level up.
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
        if self.intelligence < 7:
            self.intelligence = 7
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
        if self.charisma < 7:
            self.charisma = 7
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Wizard(Character, Combatant):
    """Caster class with high mental stats and lower durability."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a wizard and optionally print its character sheet."""
        super().__init__(name, race, hit_dice=8)
        # Tradeoff model: stronger spell potential for reduced survivability.
        self.intelligence += 3
        self.charisma += 3
        self.max_hp -= 3
        if self.max_hp < 7:
            self.max_hp = 7
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Sorcerer(Character, Combatant):
    """Magic class with strong mental stats and weaker agility."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a sorcerer and optionally print its character sheet."""
        super().__init__(name, race, hit_dice=16)
        # Tradeoff model: elevated casting stats at the cost of dexterity.
        self.wisdom += 3
        self.intelligence += 3
        self.dexterity -= 3
        if self.dexterity < 7:
            self.dexterity = 7
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Fighter(Character, Combatant):
    """Balanced martial class with strong offense."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a fighter and optionally print its character sheet."""
        super().__init__(name, race, hit_dice=14)
        # Tradeoff model: better offense/leadership, lower wisdom checks.
        self.strength += 3
        self.charisma += 3
        self.wisdom -= 3
        if self.wisdom < 7:
            self.wisdom = 7
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()


class Rogue(Character, Combatant):
    """Skirmisher class emphasizing precision and cleverness."""

    def __init__(self, name, race, display: bool = True):
        """Initialize a rogue and optionally print its character sheet."""
        super().__init__(name, race, hit_dice=8)
        # Tradeoff model: mobility and utility at the cost of raw toughness.
        self.dexterity += 3
        self.intelligence += 3
        self.constitution -= 3
        if self.constitution < 7:
            self.constitution = 7
        self.current_hp: int = self.max_hp
        if display:
            self.display_sheet()
