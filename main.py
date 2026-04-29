"""A Python RPG character system featuring a base Character class with six subclasses —
(Barbarian, Cleric, Wizard, Sorcerer, Fighter, Rogue)
Race-based stat bonuses, leveling, combat, inventory management, and character sheet export."""

from classes import *
from enemies import *
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


def battle_loop():

    while True:
        try:
            amount = int(input("How many players? Enter a digit of up to 4. ").strip())
        except TypeError:
            print("Not a number, please try again.\n")
            continue

        if amount <= 0 or amount > 4:
            print("Not a valid amount, please try again.\n")
            continue

        amount = int(amount)
        break


    # CHARACTER IMPORT GOES HERE


    players = {}
    for num in range(1, amount + 1):
        while True:
            class_choice = (
                input(
                    f"Which class for player #{num}?\nBarbarian, Cleric, Wizard, Sorcerer, Fighter, or Rogue "
                ).lower().strip()
            )

            if class_choice not in ["barbarian", "cleric", "wizard", "sorcerer", "fighter", "rogue"]:
                print("Not a valid class option, please try again.\n")
                continue

            character = CLASSES[class_choice].from_prompt()
            players[character.name] = character
            break

    print("The party:")
    for player in players.values():
        print(f"{player.name} - {player.race} {player.class_name} - level {player.level} - {player.hit_dice} hit dice - {player.max_hp} HP")
    print()


    # enemy factory creation loop
    enemies = {}
    num_enemies = int(input('How many enemies are there? '))
    while True:
        enemy_type = input('What type of enemy do you have?\nGoblin\nSkeleton\nDragon\n').lower().strip()
        if enemy_type not in ENEMIES:
            print("Please choose one of the available enemy types.")
            continue

        else:
            enemy = spawn_enemy(ENEMIES[enemy_type]())
            enemies[enemy] = num_enemies
            print(f"Spawned {num_enemies} {enemy}\n")
            break


    # enemy's battle loop
    while enemies[enemy] > 0:
        active_players = [p for p in players.values() if p.current_hp > 0]

        if not active_players:
            print('All of your characters have died!')
            print(f'{enemies[enemy]} enemies remained.')
            break

        time.sleep(.5)

        if not enemy.passed_out:
            enemy.cause_dmg(choice(active_players))


    # players' battle loop
    done = False

    for player in players.values():
        for enemy in enemies.keys():
            if not player.passed_out and not enemy.passed_out:
                player.cause_dmg(enemy)

            time.sleep(.5)

            if enemy.passed_out:
                enemies[enemy] -= 1

                if enemies[enemy] > 0:
                    enemy.passed_out = False
                    enemy.current_hp = enemy.max_hp
                    print(f'Another enemy steps forward! {enemies[enemy]} of the enemies remain.\n')

                else:
                    print(f'Every enemy has been defeated!')
                    done = True
                    break

        if done:
            break


if __name__ == "__main__":
    battle_loop()
