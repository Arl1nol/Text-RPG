import random
import time
import sys
from colorama import Fore, Style
from database import item_database, boss_database
from helpers.type_writer import typewriter, shake_text, glitch_text, display_health_damage, display_health_heal

class Boss:
    def __init__(self, p1):
        all_bosses = list(boss_database.keys())
        boss = random.choice(all_bosses)
        boss_stats = boss_database.get(boss)
        
        # Scaling Logic
        level_hp_scale = 1 + max(0, p1.level - 1) * 0.08
        level_damage_scale = 1 + max(0, p1.level - 1) * 0.06

        self.name = boss
        self.name_color = boss_stats.get('name_color', 'WHITE').upper()
        self.name_display = f"{getattr(Fore, self.name_color, Fore.WHITE)}{self.name}{Style.RESET_ALL}"
        
        # Stats
        self.maxhp = int(random.randint(*boss_stats['hp']) * level_hp_scale)
        self.hp = self.maxhp
        self.base_damage = int(boss_stats['damage'] * level_damage_scale)
        self.current_damage = self.base_damage
        self.coindrop = random.randint(*boss_stats['coin_drop'])
        self.xpdrop = random.randint(*boss_stats['xp_gain'])
        self.weakness = boss_stats['weakness']
        
        # States & Mechanics
        self.is_enemy_burning = False
        self.is_enemy_frozen = False
        self.is_enemy_debuffed = False
        self.burn_time = 0
        self.freeze_time = 0
        self.debuff_time = 0
        self.can_i_attack = True
        self.is_alive = True
        self.turn_count = 0
        self.is_special_attack_active = False
        self.special_attack_counter = 0
        self.boss_phase = 1
        self.damage_negation = 0
        self.immunity = []
        self.special_attack_chance = 0.2
        self.debuff_applied = False

    def is_burning(self):
        if self.is_enemy_burning:
            if self.hp > 0:
                burn_damage = int(self.maxhp * 0.04)
                self.take_damage(burn_damage)
                self.burn_time -= 1
                typewriter(f"The {self.name_display} sizzles! Took {Fore.RED}{burn_damage} fire damage!{Style.RESET_ALL}")
                time.sleep(0.5)
        if self.burn_time <= 0:
            self.is_enemy_burning = False

    def apply_stat_gain(self, amount):
        """Helper to add damage while respecting active debuffs."""
        if self.is_enemy_debuffed:
            self.current_damage += int(amount * 0.8)
        else:
            self.current_damage += int(amount)

    def is_debuffed(self):
        # 1. Check for expiration first
        if self.debuff_time <= 0 and self.is_enemy_debuffed:
            self.is_enemy_debuffed = False
            if self.debuff_applied:
                self.current_damage = int(self.current_damage / 0.8)
                self.debuff_applied = False 
            typewriter(f"The {self.name_display} regains its strength!")

        # 2. Apply logic if debuffed
        if self.is_enemy_debuffed:
            if not self.debuff_applied:
                self.current_damage = int(self.current_damage * 0.8)
                self.debuff_applied = True          
            typewriter(f"The {self.name_display} is {Fore.MAGENTA}weakened{Style.RESET_ALL}!")
            self.debuff_time -= 1

    def is_frozen(self):
        if 'freeze' in self.immunity:
            self.is_enemy_frozen = False
        if self.is_enemy_frozen:
            self.can_i_attack = False
            self.freeze_time -= 1
            typewriter(f"The {self.name_display} is locked in {Fore.CYAN}glacier ice{Style.RESET_ALL}!")
            time.sleep(0.5)
            if self.freeze_time <= 0:
                self.is_enemy_frozen = False
            return
        self.can_i_attack = True

    def drop_item(self):
        item_types = list(set(data['type'] for data in item_database.values()))
        chosen_type = random.choice(item_types)
        chosen_drops = {name: data for name, data in item_database.items() if data['type'] == chosen_type}
        chosen_drop_pool = {name: data for name, data in chosen_drops.items() if data['rarity'] == 'legendary'}
        if not chosen_drop_pool:
            return "apple"
        return random.choice(list(chosen_drop_pool.keys()))

    def is_dead(self, player):
        if self.hp < 1:
            self.is_alive = False
            shake_text(f"--- {self.name_display} HAS BEEN VANQUISHED ---", repeats=8)
            typewriter(f"{Fore.YELLOW}Loot Found: {self.coindrop} coins{Style.RESET_ALL}")
            player.gold += self.coindrop
            player.gain_xp(self.xpdrop)
            dropped_item = self.drop_item()
            player.backpack.append(dropped_item)
            typewriter(f"{Fore.MAGENTA}{dropped_item}{Style.RESET_ALL} was found and added to your backpack")

    def attack(self, target):
        time.sleep(0.5)
        typewriter(f"\nThe {self.name_display} {Fore.BLACK}{Style.BRIGHT}lunges forward!{Style.RESET_ALL}")
        dealt_damage = int(self.current_damage + self.current_damage * random.uniform(-0.2, 0.2))
        target.take_damage(dealt_damage)

    def activate_special_attack(self):
        self.is_special_attack_active = True

    def take_damage(self, damage):
        damage_output = int(damage * (1 - self.damage_negation))
        if self.damage_negation > 0:
            typewriter(f"{Fore.CYAN}The blow is deflected! {(self.damage_negation) * 100}% damage reduced.{Style.RESET_ALL}")
        
        typewriter(f"{Fore.YELLOW}>>{damage_output} damage dealt to {self.name}!{Style.RESET_ALL}")
        display_health_damage( self.hp,self.maxhp, damage)
        self.hp -= damage_output
        self.hp = max(self.hp, 0)
        self.check_phase_transition()

    def check_phase_transition(self):
        # Calculate standard bonus
        bonus = self.base_damage * 0.3

        if self.name == 'Lich':
            if 0 < self.hp / self.maxhp <= 0.7 and self.boss_phase == 1:
                self.boss_phase = 2
                self.apply_stat_gain(bonus)
                glitch_text(f"\n[{self.name_display}]: 'Your soul has a peculiar flavor. I shall stop playing with my food.'", speed=0.08)
            elif self.hp <= 0 and self.boss_phase == 2:
                self.hp = 0
                self.boss_phase = 3
                display_health_heal(self.hp, self.maxhp, int(self.maxhp * 0.5))
                self.hp = int(self.maxhp * 0.5)
                self.special_attack_counter = 0
                shake_text(f"{Fore.RED}THE LICH REFUSES TO FALL!{Style.RESET_ALL}")
                glitch_text("ERR: LIFE_FORCE_CRITICAL... INITIATING SOUL_DETONATION.", speed=0.1)
                self.special_attack_chance = 1
                
        elif self.name == 'Dark Knight':
            if self.hp / self.maxhp <= 0.5 and self.boss_phase == 1:
                self.boss_phase = 2
                self.damage_negation = 0.4
                self.apply_stat_gain(bonus)
                self.immunity.append('freeze')
                self.special_attack_chance += 0.2
                shake_text(f"The {self.name_display}'s armor shatters, revealing a void of shadow!")
                typewriter(f"{Fore.BLACK}{Style.BRIGHT}Darkness leaks from the cracks, chilling your very blood...{Style.RESET_ALL}")

    def special_attack(self, p1):
        if self.name == 'Lich':
            if self.boss_phase == 1:
                self.attack(p1)
            elif self.boss_phase == 2:
                if self.special_attack_counter == 0:
                    glitch_text(f"{self.name_display} begins chanting in a forgotten, necrotic tongue...", speed=0.07)
                    self.special_attack_counter += 1
                elif self.special_attack_counter == 1:
                    damage = int(self.current_damage * 1.5)
                    shake_text(f"{Fore.RED}BLOODY DOMAIN: ASCENSION{Style.RESET_ALL}")
                    p1.take_damage(damage)
                    self.hp += damage
                    typewriter(f"{Fore.GREEN}Life essence siphoned!{Style.RESET_ALL} The Lich's wounds close.")
                    self.special_attack_counter = 0
                    self.is_special_attack_active = False
            elif self.boss_phase == 3:
                stages = [
                    f"{Fore.RED}The Lich gathers a catastrophic amount of mana...{Style.RESET_ALL}",
                    f"{Fore.RED}The air is vibrating. You cannot breathe.{Style.RESET_ALL}",
                    f"{Fore.RED}REALITY IS TEARING APART.{Style.RESET_ALL}",
                    f"{Fore.WHITE}{Style.BRIGHT}--- FINAL OBLIVION ---{Style.RESET_ALL}"
                ]
                glitch_text(stages[self.special_attack_counter])
                if self.special_attack_counter == 3:
                    shake_text("BOOM!", repeats=15)
                    p1.take_damage(9999)
                else:
                    self.special_attack_counter += 1

        elif self.name == "Dark Knight":
            if self.special_attack_counter == 0:
                typewriter(f"{self.name_display} assumes a low stance. Light itself bends toward his blade.")
                self.special_attack_counter += 1
            elif self.special_attack_counter == 1:
                shake_text(f"The ground beneath you {Fore.RED}SHATTERS{Style.RESET_ALL}!")
                self.special_attack_counter += 1
            elif self.special_attack_counter == 2:
                damage = int(self.current_damage * 2.5)
                shake_text(f"{Fore.BLACK}{Style.BRIGHT}--- OBLIVION STRIKE ---{Style.RESET_ALL}", repeats=12)
                p1.take_damage(damage)
                self.special_attack_counter = 0
                self.is_special_attack_active = False

    def take_turn(self, p1):
        if self.hp <= 0 and not self.boss_phase == 3:
            return 
            
        if self.is_special_attack_active:
            self.special_attack(p1)
        elif random.random() <= self.special_attack_chance:
            self.activate_special_attack()
            self.special_attack(p1)
        else:
            self.attack(p1)