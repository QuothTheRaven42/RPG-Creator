"""Create monsters for an RPG using a factory."""
from abc import ABC, abstractmethod
from character import *


def spawn_enemy(factory):
    enemy = factory.create()
    return enemy


class Enemy(Character):
    """Based enemy class to inherit"""
    def __init__(self, name, race, attack_power):
        super().__init__(name, race)
        self.name = name
        self.attack_power = attack_power

    def describe(self):
        return f'{self.name} (attack: {self.attack_power})'

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
        super().__init__("Goblin", "Goblin", 5)


class Skeleton(Enemy):
    """The Skeleton class"""
    def __init__(self):
        super().__init__("Skeleton", "Skeleton", 10)


class Dragon(Enemy):
    """The Dragon class"""
    def __init__(self):
        super().__init__("Dragon", "Dragon",30)

    def cause_dmg(self, target: Character) -> int:
        if self.passed_out:
            print(f"{self.name} the {self.class_name} is passed out and cannot attack.")
            return 0
        elif target.passed_out:
            print(f"{self.name} has already won! {target.name} is passed out and cannot be attacked.")
            return 0
        else:
            dmg = Character.roll_dice(self.attack_power)
            print(f"{self.name} the {self.class_name} attacks for {dmg} hp!")
            target.take_dmg(dmg)
            self.gain_exp()
            return dmg



d = spawn_enemy(DragonFactory())
print(d.describe())
