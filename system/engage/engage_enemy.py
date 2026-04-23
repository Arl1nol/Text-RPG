from core.enemy import Enemy
from colorama import init, Fore, Style
import time
import questionary
from database import item_database
from helpers.type_writer import typewriter

init()


def engage_enemy(p1):
    e1 = Enemy(p1)
    player_dead = False

    typewriter(f'\nYou encountered a {e1.name_display} (HP: {int(e1.hp)}/{e1.maxhp})!')

    while p1.hp > 0 and e1.hp > 0:
        choice = questionary.select("Your move:", choices=["Attack", "Use Item", "Equip Item", "Cast Spell"]).ask()
        time.sleep(0.5)

        if choice == 'Attack':
            p1.attack(e1)
        elif choice == 'Use Item':
            filtered_usables = [item for item in p1.backpack if item_database.get(item)['type'] in ['food']]
            if filtered_usables:
                item = questionary.select("Use what:", choices=filtered_usables).ask()
                p1.use_heal(item)
            else:
                typewriter(f"{Fore.RED}No food in backpack!{Style.RESET_ALL}")
        elif choice == 'Equip Item':
            filtered_equipables = [item for item in p1.backpack if
                                   item_database.get(item)['type'] in ['physical', 'magic', 'shield']]
            if filtered_equipables:
                item = questionary.select("Equip what:", choices=filtered_equipables).ask()
                p1.equip_item(item)
            else:
                typewriter(f"{Fore.RED}Nothing to equip!{Style.RESET_ALL}")
        elif choice == 'Cast Spell':
            spell_choice = questionary.select('What spell do you want to cast: ', choices=p1.spells).ask()
            p1.cast_spell(spell_choice, e1)

        e1.is_burning()
        e1.is_debuffed()
        e1.is_frozen()
        e1.is_dead(p1)
        p1.is_burning()
        p1.is_debuffed()
        if e1.is_alive:
            typewriter(f"{e1.name_display} {Fore.RED}HP:{e1.hp}/{e1.maxhp}{Style.RESET_ALL}")
        else:
            p1.show_stats()
            break

        if e1.can_i_attack:
            e1.attack(p1)

        p1.show_stats()

        if p1.hp < 1:
            typewriter(f"{Fore.RED}You died!!!{Style.RESET_ALL}", speed=0.1)
            player_dead = True
            break

        p1.regen_mana()

    return player_dead