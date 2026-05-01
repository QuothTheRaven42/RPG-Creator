import unittest

from enemies import Goblin


class CombatantTests(unittest.TestCase):
    def test_exact_lethal_damage_marks_target_passed_out(self) -> None:
        goblin = Goblin()

        goblin.take_dmg(goblin.current_hp)

        self.assertEqual(goblin.current_hp, 0)
        self.assertTrue(goblin.passed_out)


if __name__ == "__main__":
    unittest.main()
