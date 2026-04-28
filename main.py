import time
import questionary
from colorama import init, Fore, Style
from system.save_manager import load_save, saves
from core.player import Player
from system.play_engine import run_adventure
from helpers.type_writer import typewriter
from system.engage.engage_boss import engage_boss
init()

p1 = None
start_floor = 0
if __name__ == '__main__':
    p1 = Player('Mage')
    engage_boss(p1)
if saves:
    if questionary.select("Do you want to load an existing save?", choices=['Yes', "No"]).ask() == 'Yes':
        time.sleep(1)
        chosen_save = questionary.select("Which save do you want to load:", choices=saves).ask()
        data = load_save(chosen_save)

        if data:
            p1 = Player(data['role'])
            p1.level = data['level']
            p1.xp = data['xp']
            p1.xp_to_next_level = data['xp_to_next_level']
            p1.hp = data['hp']
            p1.maxhp = data['maxhp']
            p1.mana = data['mana']
            p1.maxmana = data['maxmana']
            p1.basemaxmana = data['basemaxmana']
            p1.mana_regen = data['mana_regen']
            p1.gold = data['gold']
            p1.backpack = data['backpack']
            p1.physical_multi = data['physical_multi']
            p1.magic_multi = data['magic_multi']
            p1.equipped_weapon = data['equipped_weapon']
            p1.weapon_durability = data['weapon_durability']
            p1.equipped_shield = data['equipped_shield']
            p1.shield_durability = data['shield_durability']
            p1.shield_overshield = data['shield_overshield']
            p1.spelllevel = data['spelllevel']
            p1.spells = data['spells']
            start_floor = data.get('current_floor', 0)

            typewriter(f"{Fore.GREEN}Data has been loaded successfully!{Style.RESET_ALL}")

if p1 is None:
    your_class = questionary.select("What class do you want to be?",
                                    choices=['Warrior', 'Mage', 'Tank', 'Battlemage']).ask()
    p1 = Player(your_class)

run_adventure(p1, start_floor=start_floor)