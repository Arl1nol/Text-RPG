from core.boss import Boss
from colorama import init, Fore, Style
import time
import questionary
from database import item_database
from helpers.type_writer import typewriter, boss_banner, shake_text, glitch_text
from helpers.three_dots import tdt

init()


def engage_boss(p1):
    p1.is_burning()
    p1.is_debuffed()
    e1 = Boss(p1)
    player_dead = False

    boss_banner(e1.name_display)
    tdt()

    if e1.name == 'Lich':
        typewriter(f'\nYou open the gates to the {Fore.BLACK}{Style.BRIGHT}Underground Crypt...{Style.RESET_ALL}')
        time.sleep(1)
        glitch_text(f'"{Fore.LIGHTBLACK_EX}Mortals have no place in the halls of the eternal...{Style.RESET_ALL}"',
                    speed=0.08)
        tdt()

    elif e1.name == 'Dark Knight':
        shake_text(f'\nYou step into a {Fore.RED}blood-stained arena...{Style.RESET_ALL}')
        time.sleep(1)
        typewriter(f'The sound of heavy iron scraping against stone echoes through the room.')
        typewriter(f'A towering warrior in black plate armor draws a massive Greatsword.')
        tdt()

    while p1.hp > 0 and e1.hp > 0:
        while True:
            choice = questionary.select("Your move:", choices=["Attack", "Use Item", "Equip Item", "Cast Spell"]).ask()
            time.sleep(0.5)

            if choice == 'Attack':
                p1.attack(e1)
                break
            
            elif choice == 'Use Item':
                filtered_usables = [item for item in p1.backpack if item_database.get(item)['type'] in ['food']]
                if filtered_usables:
                    choices = filtered_usables + ["Back"]
                    item = questionary.select("Use what:", choices=choices).ask()
                    if item == "Back":
                        continue
                    p1.use_heal(item)
                    break
                else:
                    typewriter(f"{Fore.RED}No food in backpack!{Style.RESET_ALL}")
                    
            elif choice == 'Equip Item':
                filtered_equipables = [item for item in p1.backpack if item_database.get(item)['type'] in ['physical', 'magic', 'shield']]
                if filtered_equipables:
                    choices = filtered_equipables + ["Back"]
                    item = questionary.select("Equip what:", choices=choices).ask()
                    if item == "Back":
                        continue
                    p1.equip_item(item)
                    break
                else:
                    typewriter(f"{Fore.RED}Nothing to equip!{Style.RESET_ALL}")
                    
            elif choice == 'Cast Spell':
                if p1.spells:
                    choices = p1.spells + ["Back"]
                    spell_choice = questionary.select('What spell do you want to cast: ', choices=choices).ask()
                    if spell_choice == "Back":
                        continue
                    p1.cast_spell(spell_choice, e1)
                    break
                else:
                    typewriter(f"{Fore.RED}You know no spells!{Style.RESET_ALL}")

        e1.is_burning()
        e1.is_debuffed()
        e1.is_frozen()
        e1.is_dead(p1)

        if not e1.is_alive:
            p1.show_stats()
            break

        typewriter(f"\n{e1.name_display} {Fore.RED}HP:{e1.hp}/{e1.maxhp}{Style.RESET_ALL}")

        if e1.can_i_attack:
            e1.take_turn(p1)

        p1.show_stats()

        if p1.hp < 1:
            shake_text(f"{Fore.RED}YOU DIED!!!{Style.RESET_ALL}")
            player_dead = True
            break

        p1.regen_mana()

    return player_dead