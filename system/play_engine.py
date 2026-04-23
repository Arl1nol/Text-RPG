import questionary
from system.events.event_handler import encounter_event
from system.save_manager import save_run
from helpers.three_dots import tdt
from system.engage.engage_enemy import engage_enemy
from helpers.type_writer import typewriter
from system.engage.engage_boss import engage_boss


def run_adventure(p1, start_floor=0):
    typewriter("You go down the path")
    tdt()
    time_without_event = 0
    current_floor = max(0, start_floor)
    while True:
        current_floor += 1

        if not current_floor % 10 == 0:
            if engage_enemy(p1):
                break
        else:
            if engage_boss(p1):
                break

        if encounter_event(p1,time_without_event):
            time_without_event = 0
        else:
            time_without_event += 1

        if p1.hp <= 0:
            break

        choice = questionary.select("Continue?", choices=['Yes', 'No']).ask()
        if choice == 'No':
            save_run(p1, current_floor)
            break

        typewriter("Moving deeper into the dungeon...")
        tdt()