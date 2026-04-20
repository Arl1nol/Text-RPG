import glob
import questionary
import json
from colorama import init, Fore, Style
from helpers.three_dots import tdt
import os
init()

saves = glob.glob('saves/*.json')

def load_save(save_name):
    try:
        with open(save_name, 'r') as f:
            data = json.load(f)
            return data

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("There has been a corruption on the file you want to open")
    try:
        os.remove(save_name)
        print("The file has been deleted and you started a new adventure")
    except OSError:
        print("Delete has failed")


def save_adventure(save, saved_stats):
    save_name = save
    saved_stats = saved_stats
    with open(f"saves/{save_name}.json", 'w') as f:
        json.dump(saved_stats, f, indent=4)
    tdt()
    print(f"{Fore.GREEN}Game has been saved to {save_name}{Style.RESET_ALL}")

def save_run(p1):
    if questionary.select("Do you want to save this adventure?", choices=['Yes', 'No']).ask() == 'Yes':
        selected_save = ''
        if len(saves) > 3:
            if questionary.select("You do not have any free slots left, do you want to overwrite a save?",
                                  choices=['Yes', 'No']).ask() == 'Yes':
                selected_save = questionary.select("Which save do you want to select: ",
                                                   choices=saves).ask()
        for i in range(1, 4):
            slot_name = f'save_{i}'
            if slot_name not in saves:
                selected_save = slot_name
                break
        stat_save = p1.convert_to_dic()
        save_adventure(selected_save, stat_save)
    tdt()
