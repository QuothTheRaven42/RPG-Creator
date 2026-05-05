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
        """Initialize a character with randomized stats and starter items.

        The constructor builds a neutral baseline first, then applies race
        adjustments. This ordering keeps all class/race combinations predictable.
        """
        self.class_name: str = self.__class__.__name__.lower()
        self.name: str = name
        self.race: str = race
        self.max_hp: int = randint(8, 20)
        super().__init__(self.name, self.class_name, self.max_hp, hit_dice)

        self.strength: int = randint(8, 16)
        self.dexterity: int = randint(8, 16)
        self.constitution: int = randint(8, 16)
        self.intelligence: int = randint(8, 16)
        self.wisdom: int = randint(8, 16)
        self.charisma: int = randint(8, 16)

        self.level: int = 1
        self.exp: int = 0

        # Race bonuses are additive so the random baseline still matters.
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

        # Keeping inventory as a dict allows quantity updates without duplicate keys.
        self.inventory: dict = {
            "50 ft rope": 1,
            "small health potion": 4,
            "torch": 2,
            "water": 3,
            "rations": 1,
        }

    def __str__(self) -> str:
        """Return the formatted character sheet."""
        return self.char_sheet

    @classmethod
    def from_prompt(cls):
        """Prompt the user for a name and race, then create a character.

        Input validation loops until a supported race is provided to avoid
        constructing partially invalid character objects.
        """
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
        """Build the formatted character sheet text."""
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
        """Print the current character sheet to the console."""
        print(f"\nYour character sheet for {self.name} the {self.class_name}:")
        print(f"{self.char_sheet}")


    def export_char_sheet(self) -> None:
        """Write the character sheet and inventory to a text file.

        The output format is intentionally plain text and stable so the import
        path can reconstruct a character from this file later.
        """
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

    @property
    def miss_chance(self):
        return 80 - (self.dexterity * 4)

    def rest(self) -> None:
        """Restore the character to full health and clear passed-out state."""
        print("\nResting up......")
        self.current_hp = self.max_hp
        self.passed_out = False
        print(f"{self.name} the {self.class_name} is rested up and ready to go!")
        print(f"Life total: {self.current_hp}/{self.max_hp}\n")


    def cause_dmg(self, target) -> int:
        """Deal damage to a target and award experience on a successful hit.

        Experience is granted only when positive damage is dealt, which prevents
        leveling from failed actions against invalid or passed-out targets.
        """
        dmg = super().cause_dmg(target)
        if dmg > 0:
            self.gain_exp(target.exp_multiplier)
        return dmg


    def use_item(self, item: str) -> None:
        """Consume an inventory item and apply any of its effects.

        The item count is adjusted before applying effects so inventory and
        combat state always remain in sync even if effect logic changes later.
        """
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

        # Healing items are capped at max HP to avoid overheal exploits.
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
        """Add one copy of an item to the inventory."""
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1
        print(f"{item} added to the inventory.")

    def view_inventory(self) -> None:
        """Print the inventory contents."""
        if self.inventory:
            lines: str = "\n".join(f"{value} {key}" for key, value in self.inventory.items())
            print(f"{self.name}'s inventory:\n{lines}\n")
        else:
            print(f"No items in {self.name}'s inventory.\n")

    def gain_exp(self, exp_multiplier: int = 1) -> str | None:
        """Award experience and level up the character when the threshold is met.

        Args:
            exp_multiplier: Scales experience rewards for harder encounters.

        Returns:
            Optional status message when no XP can be granted.
        """
        if self.passed_out:
            return f"{self.name} is passed out and cannot gain experience."

        experience = 10 * exp_multiplier
        self.exp += experience
        print(f"{self.name} has gained {experience} experience points and has {self.exp} total.\n")

        # Level threshold scales linearly with current level.
        if self.exp >= 50 * self.level:
            self.exp = 0
            self.level += 1
            print(f"\n{self.name} has gained a level...")
            print(f"They are now level {self.level}!\n")

            # Growth is percentage-based so stronger stats keep compounding.
            self.max_hp += round(2.5 * (self.constitution * 0.1))
            self.strength += round(1 * (self.strength * 0.08))
            self.dexterity += round(1 * (self.dexterity * 0.08))
            self.constitution += round(1 * (self.constitution * 0.08))
            self.intelligence += round(1 * (self.intelligence * 0.08))
            self.wisdom += round(1 * (self.wisdom * 0.08))
            self.charisma += round(1 * (self.charisma * 0.08))
            self.current_hp = self.max_hp

        return None
