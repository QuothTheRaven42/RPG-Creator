import contextlib
import io
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class MainTests(unittest.TestCase):
    def test_import_character_restores_experience_and_passed_out_state(self) -> None:
        character_sheet = Path(__file__).parent / "fixtures" / "fallen_fighter.txt"

        with patch("builtins.input", return_value=str(character_sheet)):
            player = main.import_character()

        self.assertEqual(player.exp, 40)
        self.assertTrue(player.passed_out)
        self.assertEqual(player.inventory, {"torch": 1, "rations": 2})

    def test_battle_loop_retries_invalid_enemy_count_input(self) -> None:
        responses = iter(
            [
                "1",
                "David_the_Elf_sorcerer_lvl1.txt",
                "barbarian",
                "Bob",
                "Human",
                "x",
                "0",
                "1",
                "goblin",
                "n",
            ]
        )

        def fake_input(prompt: str = "") -> str:
            return next(responses)

        buffer = io.StringIO()
        with (
            patch("builtins.input", side_effect=fake_input),
            patch("character.Character.display_sheet", autospec=True),
            patch("character.randint", return_value=10),
            patch.object(main.time, "sleep", return_value=None),
            patch.object(main, "choice", side_effect=lambda seq: seq[0]),
            patch("combatant.Combatant.roll_dice", side_effect=lambda sides: sides),
            contextlib.redirect_stdout(buffer),
        ):
            main.battle_loop()

        output = buffer.getvalue()
        self.assertIn("Not a number, please try again.", output)
        self.assertIn("Please enter at least 1 enemy.", output)
        self.assertIn("Every enemy has been defeated!", output)


if __name__ == "__main__":
    unittest.main()
