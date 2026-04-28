"""Create monster combatants using factories."""

from abc import ABC, abstractmethod
from combatant import *


def spawn_enemy(factory):
    enemy = factory.create()
    return enemy


class Enemy(Combatant):
    """Based enemy class to inherit"""

    def __init__(self, name, class_name, max_hp, hit_dice):
        super().__init__(name, class_name, max_hp, hit_dice)
        self.hit_dice: int = hit_dice

    def describe(self):
        return f"{self.name} (attack: {self.hit_dice})"

    def display_sheet(self):
        raise NotImplementedError("Enemies don't have character sheets.")


class EnemyFactory(ABC):
    """Base Factory class to inherit"""

    @abstractmethod
    def create(self):
        pass


class GoblinFactory(EnemyFactory):
    """The factory for the Goblin class"""

    def create(self):
        return Goblin()


class SkeletonFactory(EnemyFactory):
    """The factory for the Skeleton class"""

    def create(self):
        return Skeleton()


class DragonFactory(EnemyFactory):
    """The factory for the Dragon class"""

    def create(self):
        return Dragon()


class Goblin(Enemy):
    """The Goblin class"""

    def __init__(self):
        super().__init__("Goblin", "Goblin", 10, 5)


class Skeleton(Enemy):
    """The Skeleton class"""

    def __init__(self):
        super().__init__("Skeleton", "Skeleton", 15, 10)


class Dragon(Enemy):
    """The Dragon class"""

    def __init__(self):
        super().__init__("Dragon", "Dragon", 100, 30)
