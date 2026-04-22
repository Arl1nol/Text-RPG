import glob
import random
from system.encounter_chest import encounter_chest
from system.encounter_trap import trigger_trap
from system.encounter_merchant import open_merchant

def encounter_event(p1, time_without_event):
    twe = time_without_event
    event_chance = min(35 + (twe * 8), 75)
    if random.randint(1, 100) <= event_chance:
        events = [open_merchant, trigger_trap, encounter_chest]
        event_run = random.choice(events)
        event_run(p1)
        return True
    return False