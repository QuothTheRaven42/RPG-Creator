"""Combatant class inherited by characters and enemies for battling."""

from __future__ import annotations
from random import randint


class Combatant:
    """Shared combat behavior for player characters and enemies.

    This class centralizes combat rules so both sides of a fight stay
    consistent: same damage flow, same pass-out state, and same dice model.
    """

    def __init__(self, name, class_name, max_hp, hit_dice):
        """Initialize the common combat state for a battler.

        Args:
            name: Display name used in combat messages.
            class_name: Archetype label (e.g., ``fighter`` or ``goblin``).
            max_hp: Starting and maximum health.
            hit_dice: Number of sides on the attack die.
        """
        self.hit_dice = hit_dice
        self.passed_out: bool = False
        self.name = name
        self.class_name = class_name
        self.max_hp = max_hp
        self.current_hp: int = max_hp


    def take_dmg(self, dmg: int) -> None:
        """Apply incoming damage and mark the combatant passed out at zero HP.

        A combatant that is already passed out is treated as fixed at 0 HP so
        repeated damage cannot drive the state lower or produce confusing output.
        """
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
        """Roll attack damage, apply it to the target, and return amount dealt.

        Returns ``0`` when no attack can happen (attacker or target is passed out, or they missed).
        """
        if self.passed_out:
            print(f"{self.name} is passed out and cannot attack.")
            return 0
        elif target.passed_out:
            print(
                f"{self.name} has already won! {target.name} is passed out and cannot be attacked."
            )
            return 0
        else:
            roll = self.roll_dice(100)
            if roll <= self.miss_chance:
                print(f"{self.name} attacked, but they missed {target.name} entirely!\n")
                return 0
            # Damage is intentionally tied to hit_dice so class/enemy identity
            # directly controls average damage output.
            dmg = Combatant.roll_dice(self.hit_dice)
            print(f"{self.name} attacks for {dmg} hp!")
            target.take_dmg(dmg)
            return dmg

    @staticmethod
    def roll_dice(die_sides: int) -> int:
        """Return the result of rolling one die with the given number of sides."""
        return randint(1, die_sides)
