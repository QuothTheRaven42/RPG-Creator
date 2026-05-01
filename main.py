"""
A Python RPG system - Main script for the battle loop
"""

import time
from random import choice

from character import Character
from classes import Barbarian, Cleric, Fighter, Rogue, Sorcerer, Wizard
from enemies import DragonFactory, Enemy, GoblinFactory, SkeletonFactory, spawn_enemy

CLASSES: dict = {
    "barbarian": Barbarian,
    "cleric": Cleric,
    "wizard": Wizard,
    "sorcerer": Sorcerer,
    "fighter": Fighter,
    "rogue": Rogue,
}

ENEMIES: dict = {
    "goblin": GoblinFactory,
    "skeleton": SkeletonFactory,
    "dragon": DragonFactory,
}


def import_character():
    """UNDER CONSTRUCTION, NOT IMPLEMENTED"""
    filename: str = input("What is the full filename for this character sheet? ").lower().strip()
    with open(filename, "r") as file:
        for line in file:
            split_line: list[str] = line.strip().split(" - ")
            race_and_class: list[str] = split_line[1].split(" ")
            level_number: str = split_line[2].split(" ")[1]
            break

    print(split_line, race_and_class, level_number)
    name = split_line[0]
    race = race_and_class[0]
    class_name = race_and_class[1]
    level = int(level_number)

    return name, race, class_name, level


def battle_loop():
    """Create characters and enemies; go through a full battle."""
    while True:
        try:
            amount: int = int(input("How many players? Enter a digit of up to 6. ").strip())
        except ValueError:
            print("Not a number, please try again.\n")
            continue
        if amount <= 0 or amount > 6:
            print("Not a valid amount, please try again.\n")
            continue
        break

    # name, race, class_name, level = import_character()

    players = {}
    for num in range(1, amount + 1):
        while True:
            class_choice: str = (
                input(
                    f"Which class for player #{num}?\nBarbarian, Cleric, Wizard, Sorcerer, Fighter, or Rogue "
                )
                .lower()
                .strip()
            )

            if class_choice not in [
                "barbarian",
                "cleric",
                "wizard",
                "sorcerer",
                "fighter",
                "rogue",
            ]:
                print("Not a valid class option, please try again.\n")
                continue

            character: Character = CLASSES[class_choice].from_prompt()
            players[character.name] = character
            break

    print("The party:")
    for player in players.values():
        print(
            f"{player.name} - {player.race} {player.class_name} - level {player.level} - {player.hit_dice} hit dice - {player.max_hp} HP"
        )
    print()

    # enemy factory creation loop
    enemies = {}
    while True:
        try:
            num_enemies = int(input("How many enemies are there? ").strip())
        except ValueError:
            print("Not a number, please try again.\n")
            continue
        if num_enemies <= 0:
            print("Please enter at least 1 enemy.\n")
            continue
        break

    while True:
        enemy_type = (
            input("What type of enemy do you have?\nGoblin\nSkeleton\nDragon\n").lower().strip()
        )
        if enemy_type not in ENEMIES:
            print("Please choose one of the available enemy types.")
            continue

        else:
            enemy: Enemy = spawn_enemy(ENEMIES[enemy_type]())
            enemies[enemy] = num_enemies
            print(f"Spawned {num_enemies} {enemy}\n")
            time.sleep(2)
            break

    # enemy's battle loop
    while enemies[enemy] > 0:
        active_players: list = [p for p in players.values() if p.current_hp > 0]

        if not active_players:
            print("All of your characters have died!")
            print(f"{enemies[enemy]} enemies remained.")
            break

        for _ in range(enemies[enemy]):
            if not enemy.passed_out:
                enemy.cause_dmg(choice(active_players))
                time.sleep(2)

        # players' battle loop
        active_players = [p for p in players.values() if p.current_hp > 0]
        done: bool = False

        for player in active_players:
            for enemy in enemies.keys():
                if not player.passed_out and not enemy.passed_out:
                    player.cause_dmg(enemy)
                    time.sleep(2)

                if enemy.passed_out:
                    enemies[enemy] -= 1

                    if enemies[enemy] > 0:
                        enemy.passed_out = False
                        enemy.current_hp = enemy.max_hp
                        print(
                            f"Another enemy steps forward! {enemies[enemy]} of the enemies remain.\n"
                        )
                        time.sleep(2)

                    else:
                        print(f"Every enemy has been defeated!")
                        time.sleep(2)
                        done = True
                        break
            if done:
                break

    export_choice: str = (
        input('Would you like to export your character sheets? Type "yes" or "y" ').lower().strip()
    )
    if export_choice == "yes" or export_choice == "y":
        for character in players.values():
            character.export_char_sheet()
    else:
        print("Characters not saved. Game over.")


if __name__ == "__main__":
    battle_loop()
