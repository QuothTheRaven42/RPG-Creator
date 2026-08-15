## Low Effort - Passive Combat Modifiers

- Strength: bonus damage or hit chance
- Dexterity: initiative, evasion, or crit chance
- Intelligence: spell damage or mana
- Wisdom: healing, resist, or mana regen
- Charisma: flee chance or intimidate

## Medium Effort - Derived Stats

- Derive `max_hp` from Strength or Wisdom
- Derive `crit_chance` from Dexterity
- Derive `spell_power` from Intelligence

## Medium Effort - Class Gating

- Gate big Wizard spells behind Intelligence
- Gate Barbarian rage behind Strength

## Higher Effort - Skill Checks

- Add non-combat Charisma checks
- Add non-combat Wisdom checks
- Add non-combat Intelligence checks

## Nice To Have - Test Mode

- Add `--no-sleep` or `--test-mode` to skip combat delays during tests and quick runs
