"""Tests for the main battle-loop entry points."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class MainTests(unittest.TestCase):
    """Exercise high-level game flow helpers."""

    def test_import_character_restores_experience_and_passed_out_state(self) -> None:
        """Imported character sheets should restore saved combat state."""
        character_sheet = Path(__file__).parent / "fixtures" / "fallen_fighter.txt"

        with patch("builtins.input", return_value=str(character_sheet)):
            player = main.import_character()

        self.assertEqual(player.exp, 40)
        self.assertTrue(player.passed_out)
        self.assertEqual(player.inventory, {"torch": 1, "rations": 2})

    def test_import_character_rejects_malformed_sheet(self) -> None:
        """Malformed character sheets should fail with a readable error."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as tmp:
            tmp.write("Bad header\nInventory:\n1 torch\n")
            malformed_sheet = Path(tmp.name)

        buffer = io.StringIO()
        try:
            with (
                patch("builtins.input", return_value=str(malformed_sheet)),
                contextlib.redirect_stdout(buffer),
            ):
                player = main.import_character()
        finally:
            malformed_sheet.unlink(missing_ok=True)

        self.assertIsNone(player)
        output = buffer.getvalue()
        self.assertIn("Could not import", output)
        self.assertIn("The header must look like", output)

    def test_prompt_player_count_retries_invalid_input(self) -> None:
        """The player-count prompt should keep retrying until input is valid."""
        responses = iter(
            [
                "x",
                "0",
                "1",
            ]
        )

        def fake_input(prompt: str = "") -> str:
            """Return the next canned prompt response for the player-count prompt."""
            return next(responses)

        buffer = io.StringIO()
        with patch("builtins.input", side_effect=fake_input), contextlib.redirect_stdout(buffer):
            amount = main.prompt_player_count()

        output = buffer.getvalue()
        self.assertIn("Not a number, please try again.", output)
        self.assertIn("Not a valid amount, please try again.", output)
        self.assertEqual(amount, 1)

    def test_setup_game_supports_multiple_enemy_groups(self) -> None:
        """Game setup should allow multiple enemy types in one encounter."""
        responses = iter(
            [
                "1",
                "n",
                "barbarian",
                "Bob",
                "Human",
                "1",
                "goblin",
                "y",
                "2",
                "skeleton",
                "n",
            ]
        )

        def fake_input(prompt: str = "") -> str:
            """Return the next canned setup response."""
            return next(responses)

        buffer = io.StringIO()
        with (
            patch("builtins.input", side_effect=fake_input),
            patch("character.Character.display_sheet", autospec=True),
            patch("character.randint", return_value=10),
            patch.object(main.time, "sleep", return_value=None),
            contextlib.redirect_stdout(buffer),
        ):
            players, encounter = main.setup_game()

        self.assertIn("Bob", players)
        self.assertEqual(len(encounter.groups), 2)
        self.assertEqual([group.count for group in encounter.groups], [1, 2])
        self.assertEqual([group.enemy.name for group in encounter.groups], ["Goblin", "Skeleton"])


if __name__ == "__main__":
    unittest.main()
