"""CLI entry point for party setup, enemy setup, and turn-based combat."""

from __future__ import annotations

import time
from dataclasses import dataclass
from random import choice

from character import Character
from classes import Barbarian, Cleric, Fighter, Rogue, Sorcerer, Wizard
from enemies import (
    DragonFactory,
    Enemy,
    EnemyFactory,
    GoblinFactory,
    SkeletonFactory,
    spawn_enemy,
)

PLAYER_COUNT_PROMPT = "How many players? Enter a digit of up to 6. "
IMPORT_PARTY_PROMPT = "Would you like to import a character sheet? (y/n) "
MORE_IMPORTED_PROMPT = "Do you have another character to import? (y/n) "
CLASS_PROMPT = (
    "Which class for player #{player_number}?\n"
    "Barbarian, Cleric, Wizard, Sorcerer, Fighter, or Rogue "
)
ENEMY_COUNT_PROMPT = "How many enemies are in this group? "
ENEMY_TYPE_PROMPT = "What type of enemy do you have? Choose 1.\nGoblin\nSkeleton\nDragon\n"
MORE_ENEMY_GROUPS_PROMPT = "Add another enemy type? (y/n) "
EXPORT_PROMPT = 'Would you like to export your character sheets? Type "yes" or "y" '

CLASSES: dict[str, type[Character]] = {
    "barbarian": Barbarian,
    "cleric": Cleric,
    "wizard": Wizard,
    "sorcerer": Sorcerer,
    "fighter": Fighter,
    "rogue": Rogue,
}
ENEMY_FACTORIES: dict[str, type[EnemyFactory]] = {
    "goblin": GoblinFactory,
    "skeleton": SkeletonFactory,
    "dragon": DragonFactory,
}


@dataclass(slots=True)
class EnemyGroup:
    """A stack of enemies that share one enemy template."""

    enemy: Enemy
    count: int


@dataclass(slots=True)
class Encounter:
    """A complete enemy encounter made up of one or more enemy groups."""

    groups: list[EnemyGroup]

    def remaining_enemies(self) -> int:
        """Return the total number of enemies still standing."""
        return sum(group.count for group in self.groups)


def prompt_int(
    prompt: str,
    *,
    minimum: int | None = None,
    maximum: int | None = None,
    invalid_number_message: str = "Not a number, please try again.\n",
    minimum_message: str = "Not a valid amount, please try again.\n",
    maximum_message: str | None = None,
) -> int:
    """Prompt until the user enters an integer within the requested bounds."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print(invalid_number_message)
            continue

        if minimum is not None and value < minimum:
            print(minimum_message)
            continue
        if maximum is not None and value > maximum:
            print(maximum_message or minimum_message)
            continue
        return value


def prompt_yes_no(prompt: str) -> bool:
    """Return True when the user answers yes, otherwise False."""
    return input(prompt).strip().lower() == "y"


def prompt_player_count() -> int:
    """Prompt for the number of players that will join the battle."""
    return prompt_int(
        PLAYER_COUNT_PROMPT,
        minimum=1,
        maximum=6,
        minimum_message="Not a valid amount, please try again.\n",
        maximum_message="Not a valid amount, please try again.\n",
    )


def _parse_character_sheet(file_list: list[str]) -> tuple[str, str, str, int, int, int, dict[str, str], dict[str, int]]:
    """Parse exported character sheet text into structured data."""
    if not file_list:
        raise ValueError("The file is empty.")

    header = file_list[0].strip().split(" - ")
    if len(header) != 3:
        raise ValueError(
            "Line 1: the header must look like '<name> - <race> <class> - level <N>'."
        )

    name = header[0].strip()
    race_and_class = header[1].split(" ", maxsplit=1)
    if len(race_and_class) != 2:
        raise ValueError("Line 1: the header must include both a race and a class.")

    race = race_and_class[0].strip()
    class_name = race_and_class[1].strip().lower()
    if class_name not in CLASSES:
        raise ValueError(
            f"Line 1: unsupported class '{class_name}'. Expected one of: {', '.join(sorted(CLASSES))}."
        )

    level_bits = header[2].split(" ", maxsplit=1)
    if len(level_bits) != 2 or level_bits[0].lower() != "level":
        raise ValueError("Line 1: the header must include a level number.")

    try:
        level = int(level_bits[1])
    except ValueError as exc:
        raise ValueError("Line 1: the level value must be a whole number.") from exc

    fields: dict[str, str] = {}
    items: dict[str, int] = {}
    in_inventory = False

    for line_number, line in enumerate(file_list[1:], start=2):
        stripped = line.strip()
        if not stripped or set(stripped) == {"-"}:
            continue

        if stripped == "Inventory:":
            in_inventory = True
            continue

        if in_inventory:
            quantity_and_item = stripped.split(" ", maxsplit=1)
            if len(quantity_and_item) != 2:
                raise ValueError(
                    f"Line {line_number}: inventory entry '{stripped}' does not start with a quantity."
                )
            quantity_text, item_name = quantity_and_item
            try:
                quantity = int(quantity_text)
            except ValueError as exc:
                raise ValueError(
                    f"Line {line_number}: inventory entry '{stripped}' does not start with a quantity."
                ) from exc
            items[item_name] = quantity
            continue

        if ": " not in stripped:
            raise ValueError(
                f"Line {line_number}: sheet line '{stripped}' is missing a label/value separator."
            )

        label, value = stripped.split(": ", maxsplit=1)
        fields[label] = value

    required_fields = {
        "Health",
        "Experience",
        "Strength",
        "Dexterity",
        "Constitution",
        "Intelligence",
        "Wisdom",
        "Charisma",
    }
    missing_fields = sorted(required_fields - fields.keys())
    if missing_fields:
        raise ValueError(
            f"Missing required field(s): {', '.join(missing_fields)}. "
            "The sheet is missing one or more expected export lines."
        )

    health_bits = fields["Health"].split("/", maxsplit=1)
    if len(health_bits) != 2:
        raise ValueError("Health line must look like 'current/max'.")

    try:
        current_hp = int(health_bits[0])
        max_hp = int(health_bits[1])
    except ValueError as exc:
        raise ValueError("Health values must be whole numbers.") from exc

    return name, race, class_name, level, current_hp, max_hp, fields, items


def import_character() -> Character | None:
    """Parse a saved character sheet and reconstruct a playable character."""
    filename = input("What is the full filename for this character sheet? ").strip()
    try:
        with open(filename, "r") as file:
            file_list = [line.rstrip("\n") for line in file]
        name, race, class_name, level, current_hp, max_hp, fields, items = _parse_character_sheet(file_list)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except ValueError as exc:
        print(f"Could not import '{filename}': {exc}")
        return None

    # Build the correct subclass, then replace randomized values with saved data.
    player_class = CLASSES[class_name]
    player = player_class(name, race, display=False)
    player.level = level
    player.exp = int(fields["Experience"])
    player.current_hp = current_hp
    player.max_hp = max_hp
    player.passed_out = current_hp <= 0
    player.strength = int(fields["Strength"])
    player.dexterity = int(fields["Dexterity"])
    player.constitution = int(fields["Constitution"])
    player.intelligence = int(fields["Intelligence"])
    player.wisdom = int(fields["Wisdom"])
    player.charisma = int(fields["Charisma"])
    player.inventory = items
    return player


def build_party(amount: int) -> dict[str, Character]:
    """Collect or import enough players to fill the requested party size."""
    players: dict[str, Character] = {}
    if prompt_yes_no(IMPORT_PARTY_PROMPT):
        while len(players) < amount:
            player = import_character()
            if player is not None:
                players[player.name] = player
            if len(players) >= amount:
                break
            if not prompt_yes_no(MORE_IMPORTED_PROMPT):
                break

    for _ in range(amount - len(players)):
        while True:
            class_choice = input(
                CLASS_PROMPT.format(player_number=len(players) + 1)
            ).lower().strip()
            if class_choice not in CLASSES:
                print("Not a valid class option, please try again.\n")
                continue

            character = CLASSES[class_choice].from_prompt()
            players[character.name] = character
            break

    return players


def prompt_enemy_group() -> EnemyGroup:
    """Prompt for one enemy type and count."""
    num_enemies = prompt_int(
        ENEMY_COUNT_PROMPT,
        minimum=1,
        minimum_message="Please enter at least 1 enemy.\n",
        maximum_message="Please enter at least 1 enemy.\n",
    )

    while True:
        enemy_type = input(ENEMY_TYPE_PROMPT).lower().strip()
        if enemy_type not in ENEMY_FACTORIES:
            print("Please choose one of the available enemy types.")
            continue

        enemy = spawn_enemy(ENEMY_FACTORIES[enemy_type]())
        print(f"Spawned {num_enemies} {enemy}\n")
        time.sleep(4)
        return EnemyGroup(enemy=enemy, count=num_enemies)


def setup_encounter() -> Encounter:
    """Prompt for one or more enemy groups and return the encounter."""
    groups = [prompt_enemy_group()]
    while prompt_yes_no(MORE_ENEMY_GROUPS_PROMPT):
        groups.append(prompt_enemy_group())
    return Encounter(groups=groups)


def setup_game() -> tuple[dict[str, Character], Encounter]:
    """Collect all setup input needed before combat starts."""
    amount = prompt_player_count()
    players = build_party(amount)

    print("The party:")
    for player in players.values():
        print(
            f"{player.name} - {player.race} {player.class_name} - level {player.level} - {player.hit_dice} hit dice - {player.max_hp} HP"
        )
    print()

    encounter = setup_encounter()
    return players, encounter


def _all_active_players(players: dict[str, Character]) -> list[Character]:
    """Return the subset of players that can still act."""
    return [player for player in players.values() if player.current_hp > 0]


def combat_loop(players: dict[str, Character], encounter: Encounter) -> None:
    """Run the combat-only battle loop until one side is defeated."""
    while encounter.remaining_enemies() > 0:
        active_players = _all_active_players(players)
        if not active_players:
            print("All of your characters have died!")
            print(f"{encounter.remaining_enemies()} enemies remained.")
            break

        for group in encounter.groups:
            for _ in range(group.count):
                if not group.enemy.passed_out:
                    group.enemy.cause_dmg(choice(active_players))
                    time.sleep(4)

        active_players = _all_active_players(players)
        if not active_players:
            print("All of your characters have died!")
            print(f"{encounter.remaining_enemies()} enemies remained.")
            break

        for player in active_players:
            for group in encounter.groups:
                if group.count <= 0:
                    continue

                if not player.passed_out and not group.enemy.passed_out:
                    player.cause_dmg(group.enemy)
                    time.sleep(4)

                if group.count > 0 and group.enemy.passed_out:
                    group.count -= 1
                    if group.count > 0:
                        group.enemy.passed_out = False
                        group.enemy.current_hp = group.enemy.max_hp
                        print(
                            f"Another {group.enemy.name.lower()} steps forward! "
                            f"{group.count} remain.\n"
                        )
                        time.sleep(4)
                    else:
                        print(f"The last {group.enemy.name.lower()} has fallen!")
                        time.sleep(4)

        if encounter.remaining_enemies() == 0:
            print("Every enemy has been defeated!")
            time.sleep(4)
            for character in active_players:
                character.current_hp = character.max_hp
            break

    export_choice = input(EXPORT_PROMPT).lower().strip()
    if export_choice in {"yes", "y"}:
        for character in players.values():
            character.export_char_sheet()
    else:
        print("Characters not saved. Thanks for playing!")


def battle_loop() -> None:
    """Run the full interactive game flow: setup first, then combat."""
    players, encounter = setup_game()
    combat_loop(players, encounter)


if __name__ == "__main__":
    battle_loop()
