import questionary

from helpers.type_writer import typewriter
from colorama import Fore, Style
import random

def encounter_chest(p1):
    typewriter(f"You encountered a {Fore.YELLOW}CHEST{Style.RESET_ALL}")
    if questionary.select("Do you want to open the chest?", choices=['Yes', 'No']).ask() == 'Yes':
        if random.random()<=0.3:
            typewriter(f"The chest was a {Fore.RED}TRAP!!!{Style.RESET_ALL}")
            damage = random.randint(20,30)
            p1.hp -= damage
            typewriter(f"You took {Fore.RED}{damage} damage!{Style.RESET_ALL}")
        else:
            gold_earned = random.randint(30,70)
            p1.gold += gold_earned
            typewriter(f"You opened the chest and gained {Fore.YELLOW}{gold_earned} coins!{Style.RESET_ALL}")
            typewriter(f"You have {Fore.YELLOW}{p1.gold} coins{Style.RESET_ALL}")