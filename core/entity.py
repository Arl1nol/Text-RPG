import random
import time
from colorama import Fore, Style
from helpers.type_writer import typewriter, display_health_damage

class Entity:
    def __init__(self, name, hp, maxhp, base_damage, weakness, is_player):
        self.name = name
        self.hp = hp
        self.maxhp = maxhp
        self.base_damage = base_damage
        self.current_damage = base_damage
        self.weakness = weakness
        self.is_player = is_player
        if self.is_player:
            self.self_text = "You are"
        else:
            self.self_text = f"The {self.name} is"
        
        # Shared States
        self.is_alive = True
        self.is_burning_state = False
        self.is_frozen_state = False
        self.is_debuffed_state = False
        self.burn_time = 0
        self.freeze_time = 0
        self.debuff_time = 0
        self.debuff_applied = False
        self.can_attack = True
        self.damage_negation = 0

    def check_burning(self):
        if self.is_burning_state and self.hp > 0:
            multiplier = 0.04 if hasattr(self, 'special_attack_chance') else 0.1
            burn_damage = int(self.maxhp * multiplier)
            self.take_damage(burn_damage)
            self.burn_time -= 1
            typewriter(f"{self.self_text} burning! Took {Fore.RED}{burn_damage} fire damage!{Style.RESET_ALL}")
            if self.burn_time <= 0:
                self.is_burning_state = False
            time.sleep(0.5)

    def check_frozen(self, immunity_list=None):
        if immunity_list and 'freeze' in immunity_list:
            self.is_frozen_state = False
            
        if self.is_frozen_state:
            self.can_attack = False
            self.freeze_time -= 1
            typewriter(f"{self.self_text} {Fore.CYAN}frozen{Style.RESET_ALL} and cannot move!")
            if self.freeze_time <= 0:
                self.is_frozen_state = False
            return True
        self.can_attack = True
        return False

    def check_debuff(self):
        if self.debuff_time <= 0 and self.is_debuffed_state:
            self.is_debuffed_state = False
            if self.debuff_applied:
                self.current_damage = int(self.current_damage / 0.8)
                self.debuff_applied = False 
            typewriter(f"{self.self_text} regaining strength!")

        if self.is_debuffed_state:
            if not self.debuff_applied:
                self.current_damage = int(self.current_damage * 0.8)
                self.debuff_applied = True          
            typewriter(f"{self.self_text} {Fore.MAGENTA}weakened{Style.RESET_ALL}!")
            self.debuff_time -= 1

    def take_damage(self, damage):
        damage_output = int(damage * (1 - self.damage_negation))
        if self.damage_negation > 0:
            typewriter(f"{Fore.CYAN}The blow is deflected! {int(self.damage_negation * 100)}% reduced.{Style.RESET_ALL}")
        
        display_health_damage(self.hp, self.maxhp, damage_output)
        self.hp = max(0, self.hp - damage_output)
        target_name = "You" if self.is_player else f"the {self.name}"
        typewriter(f"{damage_output} damage dealt to {target_name}!")
        return damage_output