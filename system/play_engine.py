import random
import questionary
from system.save_manager import save_run
from helpers.three_dots import  tdt
from system.engage_enemy import engage_enemy
from system.merchant import open_merchant

def run_adventure(p1):
    print("You go down the path")
    tdt()
    while True:
        if engage_enemy(p1):
            break
        if random.random() < 0.25:
            open_merchant(p1)
        if questionary.select("Continue?", choices=['Yes', 'No']).ask() == 'No':
            save_run(p1)
            break