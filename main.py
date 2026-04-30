"""
A Python RPG system
Main script for the battle loop
"""

from classes import *
from enemies import *
from character import *
from random import choice
import time

CLASSES = {
    "barbarian": Barbarian,
    "cleric": Cleric,
    "wizard": Wizard,
    "sorcerer": Sorcerer,
    "fighter": Fighter,
    "rogue": Rogue,
}

ENEMIES = {
    "goblin": GoblinFactory,
    "skeleton": SkeletonFactory,
    "dragon": DragonFactory,
}


def import_character():
    filename = input('What is the full filename for this character sheet? ').lower().strip()
    with open(filename, "r") as file:
        for line in file:
            split_line = (line.strip().split(' - '))
            split_line[1] = split_line[1].split(' ')
            split_line[2] = split_line[2].split(' ')[1]
            break

    name = split_line[0]
    race = split_line[1][0]
    class_name = split_line[1][1]
    level = int(split_line[2][0])

    return name, race, class_name, level


def battle_loop():
    while True:
        try:
            amount = int(input("How many players? Enter a digit of up to 4. ").strip())
        except TypeError:
            print("Not a number, please try again.\n")
            continue

        if amount <= 0 or amount > 6:
            print("Not a valid amount, please try again.\n")
            continue

        amount = int(amount)
        break


    name, race, class_name, level = import_character()


    players = {}
    for num in range(1, amount + 1):
        while True:
            class_choice = (
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

            character = CLASSES[class_choice].from_prompt()
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
    num_enemies = int(input("How many enemies are there? "))
    while True:
        enemy_type = (
            input("What type of enemy do you have?\nGoblin\nSkeleton\nDragon\n").lower().strip()
        )
        if enemy_type not in ENEMIES:
            print("Please choose one of the available enemy types.")
            continue

        else:
            enemy = spawn_enemy(ENEMIES[enemy_type]())
            enemies[enemy] = num_enemies
            print(f"Spawned {num_enemies} {enemy}\n")
            time.sleep(2)
            break

    # enemy's battle loop
    while enemies[enemy] > 0:
        active_players = [p for p in players.values() if p.current_hp > 0]

        if not active_players:
            print("All of your characters have died!")
            print(f"{enemies[enemy]} enemies remained.")
            break

        for _ in range(enemies[enemy]):
            if not enemy.passed_out:
                enemy.cause_dmg(choice(active_players))
                time.sleep(1.5)

        # players' battle loop
        active_players = [p for p in players.values() if p.current_hp > 0]
        done = False

        for player in active_players:
            for enemy in enemies.keys():
                if not player.passed_out and not enemy.passed_out:
                    player.cause_dmg(enemy)
                    time.sleep(1.5)

                if enemy.passed_out:
                    enemies[enemy] -= 1

                    if enemies[enemy] > 0:
                        enemy.passed_out = False
                        enemy.current_hp = enemy.max_hp
                        print(
                            f"Another enemy steps forward! {enemies[enemy]} of the enemies remain.\n"
                        )
                        time.sleep(1.5)

                    else:
                        print(f"Every enemy has been defeated!")
                        time.sleep(1.5)
                        done = True
                        break

            if done:
                break

    export_choice = input('Would you like to export your character sheets? Type "yes" or "y" ').lower().strip()
    if export_choice == 'yes' or export_choice == 'y':
        for character in players.values():
            character.export_char_sheet()
    else:
        print('Characters not saved. Game over.')

if __name__ == "__main__":
    battle_loop()
