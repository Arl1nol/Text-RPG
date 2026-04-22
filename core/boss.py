from database import item_database, boss_database
import random
from colorama import Fore, Style
import time
from helpers.type_writer import typewriter, shake_text, glitch_text


class Boss:
    def __init__(self, p1):
        all_bosses = list(boss_database.keys())
        boss = random.choice(all_bosses)
        boss_stats = boss_database.get(boss)
        level_hp_scale = 1 + max(0, p1.level - 1) * 0.08
        level_damage_scale = 1 + max(0, p1.level - 1) * 0.06

        self.name = boss
        self.maxhp = int(random.randint(*boss_stats['hp']) * level_hp_scale)
        self.hp = self.maxhp
        self.base_damage = int(boss_stats['damage'] * level_damage_scale)
        self.current_damage = self.base_damage
        self.coindrop = random.randint(*boss_stats['coin_drop'])
        self.xpdrop = random.randint(*boss_stats['xp_gain'])
        self.weakness = boss_stats['weakness']
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

    def is_burning(self):
        if self.is_enemy_burning:
            if self.hp > 0:
                burn_damage = int(self.maxhp * 0.04)
                self.hp -= burn_damage
                self.burn_time -= 1
                typewriter(f"{Fore.RED}The {self.name} took {burn_damage} fire damage!{Style.RESET_ALL}")
                time.sleep(0.5)
        if self.burn_time <= 0:
            self.is_enemy_burning = False

    def is_debuffed(self):
        if self.is_enemy_debuffed:
            self.current_damage = int(self.base_damage * 0.8)
            typewriter(f"{Fore.MAGENTA}The {self.name} is debuffed!{Style.RESET_ALL}")
            self.debuff_time -= 1
        if self.debuff_time <= 0:
            self.is_enemy_debuffed = False
            self.current_damage = self.base_damage

    def is_frozen(self):
        if self.is_enemy_frozen:
            self.can_i_attack = False
            self.freeze_time -= 1
            typewriter(f"{Fore.CYAN}The {self.name} can't attack because it's frozen{Style.RESET_ALL}")
            time.sleep(0.5)
        if self.freeze_time <= 0:
            self.can_i_attack = True
            self.is_enemy_frozen = False

    def is_dead(self, player):
        if self.hp < 1:
            self.is_alive = False
            shake_text(f"{Fore.GREEN}The {self.name} has been defeated!!!{Style.RESET_ALL}")
            typewriter(f"You gained {Fore.YELLOW}{self.coindrop} coins\n{Style.RESET_ALL}")
            player.gold += self.coindrop
            player.gain_xp(self.xpdrop)

    def attack(self, target):
        time.sleep(0.5)
        typewriter(f"\n{Fore.BLACK}{Style.BRIGHT}The {self.name} strikes!{Style.RESET_ALL}")
        dealt_damage = int(self.current_damage + self.current_damage * random.uniform(-0.2, 0.2))
        target.take_damage(dealt_damage)

    def activate_special_attack(self):
        self.is_special_attack_active = True

    def special_attack(self, p1):
        if self.name == 'Lich':
            if self.special_attack_counter == 0:
                glitch_text(
                    f"You feel the air gets dryer around you as {Fore.MAGENTA}The Lich{Style.RESET_ALL} prepares a soul-drain...",
                    speed=0.06)
                self.special_attack_counter += 1
            elif self.special_attack_counter == 1:
                damage = int(self.current_damage * 1.25)
                p1.take_damage(damage)
                self.hp += damage
                shake_text(
                    f"{Fore.MAGENTA}The Lich{Style.RESET_ALL} unleashes a {Fore.RED}Bloody Domain!{Style.RESET_ALL}")
                typewriter(
                    f"It deals {Fore.RED}{damage}{Style.RESET_ALL} damage and heals him for {Fore.GREEN}{damage}{Style.RESET_ALL}")
                self.special_attack_counter = 0
                self.is_special_attack_active = False

        elif self.name == "Dark Knight":
            if self.special_attack_counter == 0:
                typewriter(
                    f"{Fore.BLACK}The Dark Knight's{Style.RESET_ALL} sword starts {Fore.MAGENTA}pulsating{Style.RESET_ALL} with dark energy.")
                self.special_attack_counter += 1
            elif self.special_attack_counter == 1:
                shake_text(
                    f"{Fore.BLACK}The Dark Knight{Style.RESET_ALL} raises his sword, the ground begins to crack!")
                self.special_attack_counter += 1
            elif self.special_attack_counter == 2:
                damage = int(self.current_damage * 2.2)
                shake_text(f"{Fore.RED}THE DARK KNIGHT UNLEASHES AN OBLIVION STRIKE!{Style.RESET_ALL}")
                p1.take_damage(damage)
                self.special_attack_counter = 0
                self.is_special_attack_active = False

    def take_turn(self, p1):
        if self.is_special_attack_active:
            self.special_attack(p1)
        elif random.random() <= 0.2:
            self.activate_special_attack()
            self.special_attack(p1)
        else:
            self.attack(p1)