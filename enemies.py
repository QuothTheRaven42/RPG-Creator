"""Create monster combatants using factories."""

from __future__ import annotations

from abc import ABC, abstractmethod

from combatant import Combatant


def spawn_enemy(factory: EnemyFactory) -> Enemy:
    """Create an enemy instance from the supplied factory.

    Using a factory keeps enemy creation decoupled from battle code so
    new enemy types can be added without changing the loop logic.
    """
    enemy = factory.create()
    return enemy


class Enemy(Combatant):
    """Base class for enemy combatants.

    Enemy objects share combat behavior with characters but intentionally omit
    player-only concepts like inventory and persistent character sheets.
    """

    def __init__(self, name, class_name, max_hp, hit_dice):
        """Initialize an enemy combatant."""
        super().__init__(name, class_name, max_hp, hit_dice)
        self.hit_dice: int = hit_dice

    def __str__(self):
        """Return a short summary of the enemy's combat stats."""
        return f"{self.name} - {self.hit_dice} hit dice, {self.current_hp} / {self.max_hp} HP"

    def describe(self):
        """Return a compact enemy description for UI output."""
        return f"{self.name} (attack: {self.hit_dice})"

    def display_sheet(self):
        """Reject character-sheet display for enemies."""
        raise NotImplementedError("Enemies don't have character sheets.")


class EnemyFactory(ABC):
    """Abstract factory for creating enemies.

    The factory interface keeps spawn logic uniform regardless of enemy type.
    """

    @abstractmethod
    def create(self) -> Enemy:
        """Build and return an enemy instance."""
        pass


class GoblinFactory(EnemyFactory):
    """Factory for goblin enemies."""

    def create(self) -> Enemy:
        """Create a goblin enemy."""
        return Goblin()


class SkeletonFactory(EnemyFactory):
    """Factory for skeleton enemies."""

    def create(self) -> Enemy:
        """Create a skeleton enemy."""
        return Skeleton()


class DragonFactory(EnemyFactory):
    """Factory for dragon enemies."""

    def create(self) -> Enemy:
        """Create a dragon enemy."""
        return Dragon()


class Goblin(Enemy):
    """Goblin enemy type."""

    def __init__(self) -> None:
        """Initialize a goblin enemy."""
        super().__init__("Goblin", "Goblin", 10, 5)


class Skeleton(Enemy):
    """Skeleton enemy type."""

    def __init__(self) -> None:
        """Initialize a skeleton enemy."""
        super().__init__("Skeleton", "Skeleton", 15, 10)


class Dragon(Enemy):
    """Dragon enemy type."""

    def __init__(self) -> None:
        """Initialize a dragon enemy."""
        super().__init__("Dragon", "Dragon", 100, 30)
