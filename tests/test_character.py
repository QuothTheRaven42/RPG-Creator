"""Tests for character inventory and experience behavior."""

import unittest
from unittest.mock import patch

from character import Character
from classes import Barbarian, Cleric
from enemies import Goblin


class CharacterTests(unittest.TestCase):
    """Exercise character-specific gameplay behavior."""

    def test_missing_potion_does_not_heal(self) -> None:
        """Using an absent potion should not change the character's HP."""
        with (
            patch("character.Character.display_sheet", autospec=True),
            patch("character.randint", return_value=10),
            patch.object(Character, "roll_dice", return_value=1),
        ):
            cleric = Cleric("Test", "Human")
            cleric.current_hp = 1
            cleric.inventory.pop("small health potion", None)

            cleric.use_item("small health potion")

            self.assertEqual(cleric.current_hp, 1)

    def test_cleric_small_potion_bonus_applies(self) -> None:
        """Clerics should receive their healing bonus from small potions."""
        with (
            patch("character.Character.display_sheet", autospec=True),
            patch("character.randint", return_value=10),
            patch.object(Character, "roll_dice", return_value=1),
        ):
            cleric = Cleric("Test", "Human")
            cleric.current_hp = 1
            cleric.inventory["small health potion"] = 1

            cleric.use_item("small health potion")

            self.assertEqual(cleric.current_hp, 6)

    def test_character_attack_grants_experience(self) -> None:
        """Successful attacks should award experience to the attacker."""
        with (
            patch("character.Character.display_sheet", autospec=True),
            patch("character.randint", return_value=10),
            patch("combatant.randint", return_value=2),
        ):
            barbarian = Barbarian("Test", "Human")
            goblin = Goblin()

            barbarian.cause_dmg(goblin)

            self.assertEqual(barbarian.exp, 10)


if __name__ == "__main__":
    unittest.main()
