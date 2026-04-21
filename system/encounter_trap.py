import time

from database import trap_database
from colorama import init, Fore, Style
from helpers.three_dots import tdt
import random

def trigger_trap(p1):
    tdt()
    all_traps = list(trap_database.keys())
    trap = random.choice(all_traps)
    trap_data = trap_database.get(trap)
    trap_type = trap_data['type']
    print(f"{Fore.RED}You encountered a {trap} trap!!!{Style.RESET_ALL}")
    damage = random.randint(*trap_data['damage'])
    time.sleep(1)
    if trap_type == 'physical':
        p1.hp -= damage
        print(f"You took {min(p1.gold, damage)} damage!")
    elif trap_type == 'fire':
        p1.hp -= damage
        p1.is_player_burning = True
        p1.burn_time = 3
        print(f"You took {min(p1.hp, damage)} damage!")
        print(f"{Fore.RED}You have been set on fire for 3 rounds!{Style.RESET_ALL}")
    elif trap_type == 'coin':
        p1.gold -= min(p1.gold,damage)
        print(f"You lost {damage} gold!")
    elif trap_type == 'debuff':
        p1.hp -= damage
        print(f"You took {min(p1.hp, damage)} damage!")
        p1.is_player_debuffed = True
        p1.debuff_time = 3
        print(f"{Fore.MAGENTA}You have been debuffed for 3 rounds!{Style.RESET_ALL}")