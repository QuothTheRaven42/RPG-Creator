"""Combatant class inherited by characters and enemies for battling."""

from random import randint


class Combatant:

    def __init__(self, name, class_name, max_hp, hit_dice):
        self.hit_dice = hit_dice
        self.passed_out: bool = False
        self.name = name
        self.class_name = class_name
        self.max_hp = max_hp
        self.current_hp: int = max_hp

    def take_dmg(self, dmg: int) -> None:
        if self.current_hp > 0:
            self.current_hp -= dmg
        if self.passed_out:
            print(f"{self.name} is passed out and cannot take damage.")
        elif self.current_hp < 0:
            self.current_hp = 0
            self.passed_out = True
            print(f"{self.name} took {dmg} damage and has passed out!\n")
            print(f"Life total: {self.current_hp}/{self.max_hp}")
        else:
            print(f"{self.name} has taken {dmg} points of damage!")
            print(f"Remaining life for {self.name}: {self.current_hp}/{self.max_hp}\n")

    def cause_dmg(self, target: Character) -> int:
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
            if hasattr(self, "exp"):
                self.gain_exp()
            return dmg

    def gain_exp(self, multiplier: int = 1) -> str | None:
        if self.passed_out:
            return f"{self.name} is passed out and cannot gain experience."

        experience = 10 * multiplier
        self.exp += experience
        print(f"{self.name} has gained {experience} experience points and has {self.exp} total.")

        if self.exp >= 50 * self.level:
            self.exp: int = 0
            self.level += 1
            print(f"\n{self.name} has gained a level...")
            print(f"They are now level {self.level}!\n")

            self.max_hp += round(2.5 * (self.constitution * 0.1))
            self.strength += round(1 * (self.strength * 0.08))
            self.dexterity += round(1 * (self.dexterity * 0.08))
            self.constitution += round(1 * (self.constitution * 0.08))
            self.intelligence += round(1 * (self.intelligence * 0.08))
            self.wisdom += round(1 * (self.wisdom * 0.08))
            self.charisma += round(1 * (self.charisma * 0.08))
            self.current_hp = self.max_hp

        return None

    @staticmethod
    def roll_dice(d_num: int) -> int:
        return randint(1, d_num)
