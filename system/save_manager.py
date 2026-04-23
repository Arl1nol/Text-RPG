import glob
import questionary
import json
from colorama import init, Fore, Style
from helpers.three_dots import tdt
from helpers.type_writer import typewriter
import os

init()

saves = glob.glob('saves/*.json')


def load_save(save_name):
    try:
        with open(save_name, 'r') as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        typewriter(f"{Fore.RED}There has been a corruption on the file you want to open{Style.RESET_ALL}")
        try:
            os.remove(save_name)
            typewriter(f"{Fore.YELLOW}The corrupted file has been deleted.{Style.RESET_ALL}")
        except OSError:
            typewriter(f"{Fore.RED}Delete has failed{Style.RESET_ALL}")
        return None


def save_adventure(save, saved_stats):
    save_path = f"saves/{save}.json" if not save.endswith('.json') else save
    with open(save_path, 'w') as f:
        json.dump(saved_stats, f, indent=4)
    tdt()
    typewriter(f"{Fore.GREEN}Game has been saved to {save}{Style.RESET_ALL}")


def save_run(p1, current_floor=0):
    if questionary.select("Do you want to save this adventure?", choices=['Yes', 'No']).ask() == 'Yes':
        selected_save = ''
        current_saves = glob.glob('saves/save_*.json')

        if len(current_saves) >= 3:
            if questionary.select("No free slots left. Overwrite a save?", choices=['Yes', 'No']).ask() == 'Yes':
                selected_save = questionary.select("Select save to overwrite:", choices=current_saves).ask()
            else:
                return
        else:
            for i in range(1, 4):
                slot_path = f'saves/save_{i}.json'
                if slot_path not in current_saves:
                    selected_save = f'save_{i}'
                    break

        if selected_save:
            stat_save = p1.convert_to_dic()
            stat_save["current_floor"] = current_floor
            save_adventure(selected_save, stat_save)

    tdt()