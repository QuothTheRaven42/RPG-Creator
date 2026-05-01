"""The Character class for setting stats, displaying character sheet, and various character actions."""

from random import randint

from combatant import Combatant


class Character(Combatant):
    """Parent class for RPG character classes to inherit.

    Initializes character stats before class bonuses and creates the starting inventory.
    Includes methods for resting, causing and taking damage, and handling the inventory.

    Attributes:
        stats (int): Strength, dexterity, constitution, intelligence, wisdom, and charisma.
        passed_out (bool): Life state, with True meaning life_total is 0.
        exp (int): Total experience for the current level, resets on level up.
        char_sheet (str): Name, race, class, level, and stats.
    """

    def __init__(self, name, race, hit_dice: int = 0):
        self.class_name: str = self.__class__.__name__.lower()
        self.name: str = name
        self.race: str = race
        self.max_hp: int = randint(8, 20)
        super().__init__(self.name, self.class_name, self.max_hp, hit_dice)

        self.strength: int = randint(5, 15)
        self.dexterity: int = randint(5, 15)
        self.constitution: int = randint(5, 15)
        self.intelligence: int = randint(5, 15)
        self.wisdom: int = randint(5, 15)
        self.charisma: int = randint(5, 15)

        self.level: int = 1
        self.exp: int = 0

        # Race bonuses
        if self.race == "Human":
            self.strength += 1
            self.constitution += 1
            self.intelligence += 1
            self.wisdom += 1
            self.charisma += 1
        elif self.race == "Dwarf":
            self.strength += 2
            self.constitution += 2
            self.wisdom += 1
        elif self.race == "Elf":
            self.dexterity += 2
            self.intelligence += 1
            self.wisdom += 1
            self.charisma += 1
        elif self.race == "Gnome":
            self.dexterity += 2
            self.intelligence += 2
            self.constitution += 1
        elif self.race == "Halfling":
            self.dexterity += 2
            self.constitution += 1
            self.charisma += 2

        # Starting inventory
        self.inventory: dict = {
            "50 ft rope": 1,
            "small health potion": 4,
            "torch": 2,
            "water": 3,
            "rations": 1,
        }

    def __str__(self) -> str:
        return self.char_sheet

    @classmethod
    def from_prompt(cls):
        name: str = input(f"What is your {cls.__name__}'s name? ").title()
        while True:
            race: str = input(
                "\nChoose a race:\n--------\nDwarf\nElf\nGnome\nHalfling\nHuman\n"
            ).title()
            print()
            if race not in ["Human", "Dwarf", "Elf", "Gnome", "Halfling"]:
                print(f"{race} is not a valid option, please try again.\n")
                continue
            return cls(name, race)

    @property
    def char_sheet(self) -> str:
        char_sheet: str = f"""{self.name} - {self.race} {self.class_name} - level {self.level}
---------------------------------
Health: {self.current_hp}/{self.max_hp}
Experience: {self.exp}
Strength: {self.strength}
Dexterity: {self.dexterity}
Constitution: {self.constitution}
Intelligence: {self.intelligence}
Wisdom: {self.wisdom}
Charisma: {self.charisma}\n"""

        return char_sheet

    def display_sheet(self) -> None:
        print(f"\nYour character sheet for {self.name} the {self.class_name}:")
        print(f"{self.char_sheet}")

    def cause_dmg(self, target) -> int:
        dmg = super().cause_dmg(target)
        if dmg > 0:
            self.gain_exp()
        return dmg

    def export_char_sheet(self) -> None:
        with open(
            f"{self.name}_the_{self.race}_{self.class_name}_lvl{self.level}.txt", "w"
        ) as file:
            file.write(self.char_sheet)
            file.write("\nInventory:\n")
            lines = "\n".join(f"{value} {key}" for key, value in self.inventory.items())
            file.write(f"{lines}")

        print(
            f"Character sheet for {self.name} the {self.class_name} has been saved as {self.name}_the_{self.race}_{self.class_name}_lvl{self.level}.txt."
        )

    def rest(self) -> None:
        print("\nResting up......")
        self.current_hp = self.max_hp
        self.passed_out = False
        print(f"{self.name} the {self.class_name} is rested up and ready to go!")
        print(f"Life total: {self.current_hp}/{self.max_hp}\n")

    def use_item(self, item: str) -> None:
        if item not in self.inventory:
            print(f"{item} is not in {self.name}'s inventory.\n")
            return
        elif self.inventory[item] == 1:
            del self.inventory[item]
            print(f"{self.name} the {self.class_name} used {item} from their inventory.")
        else:
            self.inventory[item] -= 1
            print(f"{self.name} the {self.class_name} used {item} from their inventory.")
            print(f"There are {self.inventory[item]} {item} left in the inventory.")

        # healing items
        if item == "small health potion":
            num: int = Character.roll_dice(6)
            if self.class_name == "cleric":
                num += 4
            self.current_hp = min(self.current_hp + num, self.max_hp)
            print(f"small health potion used - +{num} health gained!")
            print(f"Life total: {self.current_hp}\n")
            self.passed_out = False
        elif item == "large health potion":
            num = Character.roll_dice(20) + Character.roll_dice(6)
            if self.class_name == "cleric":
                num += 12
            self.current_hp: int = min(self.current_hp + num, self.max_hp)
            print(f"large health potion used - +{num} health gained!")
            print(f"Life total: {self.current_hp}\n")
            self.passed_out: bool = False

    def add_item(self, item: str) -> None:
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1
        print(f"{item} added to the inventory.")

    def view_inventory(self) -> None:
        if self.inventory:
            lines: str = "\n".join(f"{value} {key}" for key, value in self.inventory.items())
            print(f"{self.name}'s inventory:\n{lines}\n")
        else:
            print(f"No items in {self.name}'s inventory.\n")

    def gain_exp(self, multiplier: int = 1) -> str | None:
        if self.passed_out:
            return f"{self.name} is passed out and cannot gain experience."

        experience = 10 * multiplier
        self.exp += experience
        print(f"{self.name} has gained {experience} experience points and has {self.exp} total.\n")

        if self.exp >= 50 * self.level:
            self.exp = 0
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
