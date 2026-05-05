## Low effort — passive combat modifiers

Strength → bonus to physical attack damage or hit chance 

Dexterity → initiative order, dodge/evasion chance, or crit chance

Intelligence → spell damage multiplier or mana pool size

Wisdom → healing effectiveness, resist debuffs, or mana regen

Charisma → flee success rate, or a "intimidate" that reduces enemy attack

## Medium effort — derived stats
Rather than stats acting directly, you compute secondary values from them at character creation/load time:

max_hp partially scales with Strength or Wisdom

crit_chance derived from Dexterity

spell_power derived from Intelligence

This keeps combat code clean — it just reads self.crit_chance, not raw stat values.

Medium effort — class-specific stat gating

Each class already exists in your hierarchy. You could make certain abilities only trigger above a stat threshold — a Wizard's big spell only fires if Intelligence ≥ X, a Barbarian rage only if Strength ≥ Y. Rewards building characters intentionally.

## Higher effort — skill checks outside combat
A text-based RPG classically uses stats for non-combat moments: a Charisma check to talk your way past a guard, a Wisdom check to notice a trap, Intelligence to decipher something. This would require adding an event/encounter layer beyond the battle loop, but it's a natural next step if you want the system to feel like a real RPG.

The derived stats approach is probably the cleanest architectural move — it gives every stat a purpose without tangling the combat logic. What's the current shape of your Character class where these stats live? That'd help narrow down which approach fits most naturally.
