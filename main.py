"""A Python RPG character system featuring a base Character class with six subclasses —
(Barbarian, Cleric, Wizard, Sorcerer, Fighter, Rogue)
Race-based stat bonuses, leveling, combat, inventory management, and character sheet export."""

from random import randint


class Character:
    """Parent class for RPG character classes to inherit.

    Initializes character stats before class bonuses and creates the starting inventory.
    Includes methods for resting, causing and taking damage, and handling the inventory.

    Attributes:
        stats (int): Strength, dexterity, constitution, intelligence, wisdom, and charisma.
        passed_out (bool): Life state, with True meaning life_total is 0.
        exp (int): Total experience for the current level, resets on level up.
        char_sheet (str): Name, race, class, level, and stats.
    """

    def __init__(self):
        self.class_name = self.__class__.__name__.lower()
        self.current_hp = 0
        self.name = input(f"What is your {self.class_name}'s name? ").title()
        self.race = input("\nChoose a race:\n--------\nDwarf\nElf\nGnome\nHalfling\nHuman\n").title()

        self.max_hp = randint(8, 20)
        self.strength = randint(5, 15)
        self.dexterity = randint(5, 15)
        self.constitution = randint(5, 15)
        self.intelligence = randint(5, 15)
        self.wisdom = randint(5, 15)
        self.charisma = randint(5, 15)

        self.passed_out = False
        self.level = 1
        self.exp = 0

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

    @property
    def char_sheet(self) -> str:
        char_sheet = f"""\n{self.name} - {self.race} {self.class_name} - level {self.level}
---------------------------------
Health: {self.current_hp}/{self.max_hp}
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

    def gain_exp(self, multiplier: int = 1) -> str | None:
        if self.passed_out == True:
            return f"{self.name} the {self.class_name} is passed out and cannot gain experience."

        experience = 10 * multiplier
        self.exp += experience
        print(
            f"{self.name} the {self.class_name} has gained {experience} experience points and has {self.exp} total."
        )

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

    def take_dmg(self, dmg: int) -> None:
        if self.current_hp > 0:
            self.current_hp -= dmg
        if self.passed_out == True:
            print(f"{self.name} the {self.class_name} is passed out and cannot take damage.")
        elif self.current_hp < 0:
            self.current_hp = 0
            self.passed_out = True
            print(f"{self.name} the {self.class_name} took {dmg} damage and has passed out!\n")
            print(f"Life total: {self.current_hp}/{self.max_hp}")
        else:
            print(f"{self.name} the {self.class_name} has taken {dmg} points of damage!")
            print(f"Remaining life for {self.name}: {self.current_hp}/{self.max_hp}\n")

    def cause_dmg(self, target: Character) -> int:
        if self.passed_out == True:
            print(f"{self.name} the {self.class_name} is passed out and cannot attack.")
            return 0
        elif target.passed_out == True:
            print(f"{self.name} has already won! {target.name} is passed out and cannot be attacked.")
            return 0
        else:
            dmg = Character.roll_dice(6)
            print(f"{self.name} the {self.class_name} attacks for {dmg} hp!")
            target.take_dmg(dmg)
            self.gain_exp()
            return dmg

    def rest(self) -> None:
        print("\nResting up......")
        self.current_hp = self.max_hp
        self.passed_out = False
        print(f"{self.name} the {self.class_name} is rested up and ready to go!")
        print(f"Life total: {self.current_hp}/{self.max_hp}\n")

    def use_item(self, item: str) -> None:
        if item not in self.inventory:
            print(f"{item} is not {self.name}'s inventory.\n")
        elif self.inventory[item] == 1:
            del self.inventory[item]
            print(f"{self.name} the {self.class_name} used {item} from their inventory.")
        else:
            self.inventory[item] -= 1
            print(f"{self.name} the {self.class_name} used {item} from their inventory.")
            print(f"There are {self.inventory[item]} {item} left in the inventory.")

        # healing items
        if item == "small health potion":
            num = Character.roll_dice(6)
            self.current_hp = min(self.current_hp + num, self.max_hp)
            print(f"small health potion used - +{num} health gained!")
            print(f"Life total: {self.current_hp}\n")
            self.passed_out = False

        elif item == "large health potion":
            num = Character.roll_dice(20) + Character.roll_dice(6)
            self.current_hp = min(self.current_hp + num, self.max_hp)
            print(f"large health potion used - +{num} health gained!")
            print(f"Life total: {self.current_hp}\n")
            self.passed_out = False

    def add_item(self, item: str) -> None:
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1
        print(f"{item} added to the inventory.")

    def view_inventory(self) -> None:
        if self.inventory:
            lines = "\n".join(f"{value} {key}" for key, value in self.inventory.items())
            print(f"{self.name}'s inventory:\n{lines}\n")
        else:
            print(f"No items in {self.name}'s inventory.\n")

    @staticmethod
    def roll_dice(d_num: int) -> int:
        return randint(1, d_num)


class Barbarian(Character):
    def __init__(self):
        super().__init__()
        self.strength += 3
        self.constitution += 3
        self.intelligence -= 3
        self.current_hp = self.max_hp
        self.display_sheet()


class Cleric(Character):
    def __init__(self):
        super().__init__()
        self.constitution += 3
        self.wisdom += 3
        self.charisma -= 3
        self.current_hp = self.max_hp
        self.display_sheet()


class Wizard(Character):
    def __init__(self):
        super().__init__()
        self.intelligence += 3
        self.charisma += 3
        self.max_hp -= 3
        self.current_hp = self.max_hp
        self.display_sheet()


class Sorcerer(Character):
    def __init__(self):
        super().__init__()
        self.wisdom += 3
        self.max_hp += 3
        self.dexterity -= 3
        self.current_hp = self.max_hp
        self.display_sheet()


class Fighter(Character):
    def __init__(self):
        super().__init__()
        self.strength += 3
        self.charisma += 3
        self.wisdom -= 3
        self.current_hp = self.max_hp
        self.display_sheet()


class Rogue(Character):
    def __init__(self):
        super().__init__()
        self.dexterity += 3
        self.intelligence += 3
        self.constitution -= 3
        self.current_hp = self.max_hp
        self.display_sheet()
