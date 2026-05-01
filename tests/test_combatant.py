"""Tests for shared combatant damage handling."""

import unittest

from enemies import Goblin


class CombatantTests(unittest.TestCase):
    """Verify shared combat behavior."""

    def test_exact_lethal_damage_marks_target_passed_out(self) -> None:
        """Taking lethal damage equal to current HP should pass the target out."""
        goblin = Goblin()

        goblin.take_dmg(goblin.current_hp)

        self.assertEqual(goblin.current_hp, 0)
        self.assertTrue(goblin.passed_out)


if __name__ == "__main__":
    unittest.main()
