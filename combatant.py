"""Combatant class inherited by characters and enemies for battling."""

from __future__ import annotations
from random import randint


class Combatant:
    """Shared combat behavior for player characters and enemies."""

    def __init__(self, name, class_name, max_hp, hit_dice):
        """Initialize the common combat state for a battler."""
        self.hit_dice = hit_dice
        self.passed_out: bool = False
        self.name = name
        self.class_name = class_name
        self.max_hp = max_hp
        self.current_hp: int = max_hp

    def take_dmg(self, dmg: int) -> None:
        """Apply incoming damage and mark the combatant passed out at zero HP."""
        if self.passed_out or self.current_hp <= 0:
            self.current_hp = 0
            self.passed_out = True
            print(f"{self.name} is passed out and cannot take damage.")
            return

        self.current_hp -= dmg
        if self.current_hp <= 0:
            self.current_hp = 0
            self.passed_out = True
            print(f"{self.name} took {dmg} damage and has passed out!\n")
        else:
            print(f"{self.name} has taken {dmg} points of damage!")
            print(f"Remaining life for {self.name}: {self.current_hp}/{self.max_hp}\n")

    def cause_dmg(self, target) -> int:
        """Roll attack damage, apply it to the target, and return the amount dealt."""
        if self.passed_out:
            print(f"{self.name} is passed out and cannot attack.")
            return 0
        elif target.passed_out:
            print(
                f"{self.name} has already won! {target.name} is passed out and cannot be attacked."
            )
            return 0
        else:
            dmg = Combatant.roll_dice(self.hit_dice)
            print(f"{self.name} attacks for {dmg} hp!")
            target.take_dmg(dmg)
            return dmg

    @staticmethod
    def roll_dice(d_num: int) -> int:
        """Return the result of rolling one die with the given number of sides."""
        return randint(1, d_num)
