import time
import random
from colorama import Fore, Style
from database import trap_database
from helpers.three_dots import tdt
from helpers.type_writer import typewriter
def trigger_trap(p1):
    tdt()

    all_traps = list(trap_database.keys())
    trap_name = random.choice(all_traps)
    trap_data = trap_database.get(trap_name)
    trap_type = trap_data['type']

    print(f"{Fore.RED}!!! TRAP TRIGGERED: {trap_name} !!!{Style.RESET_ALL}")

    raw_damage = random.randint(*trap_data['damage'])
    time.sleep(0.8)

    if trap_type == 'physical':
        actual_loss = min(max(0, p1.hp), raw_damage)
        p1.hp -= raw_damage
        typewriter(f"{Fore.YELLOW}Crunch! You took {actual_loss} physical damage.{Style.RESET_ALL}")

    elif trap_type == 'fire':
        actual_loss = min(max(0, p1.hp), raw_damage)
        p1.hp -= raw_damage
        p1.is_player_burning = True
        p1.burn_time = 3
        typewriter(f"{Fore.RED}Sizzle! You took {actual_loss} fire damage and are BURNING!{Style.RESET_ALL}")

    elif trap_type == 'coin':
        actual_loss = min(p1.gold, raw_damage)
        p1.gold -= actual_loss
        typewriter(f"{Fore.YELLOW}A thief! You lost {actual_loss} gold coins!{Style.RESET_ALL}")

    elif trap_type == 'debuff':
        actual_loss = min(max(0, p1.hp), raw_damage)
        p1.hp -= raw_damage
        p1.is_player_debuffed = True
        p1.debuff_time = 3
        typewriter(
            f"{Fore.MAGENTA}Cursed! You took {actual_loss} damage and feel your strength fading...{Style.RESET_ALL}")

    time.sleep(1)