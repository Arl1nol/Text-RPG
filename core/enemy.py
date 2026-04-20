from database import item_database, enemy_database
import random
from colorama import init, Fore, Style
import time
init()

class Enemy:
    def __init__(self):
        enemy_keys = list(enemy_database.keys())
        enemy_weights = [1, 4, 15, 80]
        enemy = random.choices(enemy_keys, weights=enemy_weights, k=1)[0]
        enemy_stats = enemy_database.get(enemy)
        self.name = enemy
        self.maxhp = random.randint(*enemy_stats['hp'])
        self.hp = self.maxhp
        self.base_damage = enemy_stats['damage']
        self.current_damage = self.base_damage
        self.coindrop = random.randint(*enemy_stats['coindrop'])
        self.xpdrop = random.randint(*enemy_stats['xp'])
        self.weakness = enemy_stats['weakness']
        self.is_enemy_burning = False
        self.is_enemy_frozen = False
        self.is_enemy_debuffed = False
        self.burn_time = 0
        self.freeze_time = 0
        self.debuff_time = 0
        self.can_i_attack = True
        self.is_alive = True

    def is_burning(self):
        if self.is_enemy_burning:
            if self.hp > 0:
                burn_damage = int(self.maxhp * 0.1)
                self.hp -= burn_damage
                self.burn_time -= 1
                print(f"{Fore.RED}The {self.name} took {burn_damage} fire damage!{Style.RESET_ALL}")
                time.sleep(0.5)
        if self.burn_time <= 0:
            self.is_enemy_burning = False

    def is_debuffed(self):
        if self.is_enemy_debuffed:
            self.current_damage = int(self.base_damage * 0.8)
            print(f"{Fore.MAGENTA}The enemy is debuffed!{Style.RESET_ALL}")
            self.debuff_time -= 1
        if self.debuff_time <= 0:
            self.is_enemy_debuffed = False
            self.current_damage = self.base_damage

    def is_frozen(self):
        if self.is_enemy_frozen:
            self.can_i_attack = False
            self.freeze_time -= 1
            print(f"{Fore.CYAN}The {self.name} cant attack because its frozen{Style.RESET_ALL}")
            time.sleep(0.5)
        if self.freeze_time <= 0:
            self.can_i_attack = True
            self.is_enemy_frozen = False

    def is_dead(self, player):
        if self.hp < 1:
            self.is_alive = False
            print(f"{Fore.GREEN}The {self.name} has been defeated!!!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}You gained {self.coindrop} coins\n{Style.RESET_ALL}")
            player.gold += self.coindrop
            player.gain_xp(self.xpdrop)
            dropped_item = self.drop_item()
            player.backpack.append(dropped_item)
            print(f"{Fore.YELLOW}{dropped_item} was found and added to your backpack{Style.RESET_ALL}")

    def attack(self, target):
        time.sleep(0.5)
        print(f"\n{Fore.RED}The {self.name} strikes!{Style.RESET_ALL}")
        dealt_damage = int(self.current_damage + self.current_damage * random.uniform(-0.2, 0.2))
        target.take_damage(dealt_damage)

    def drop_item(self):
        enemy_rarity = enemy_database[self.name]['rarity']
        item_types = list(set(data['type'] for data in item_database.values()))
        chosen_type = random.choice(item_types)
        chosen_drops = {name: data for name, data in item_database.items() if data['type'] == chosen_type}
        rarity_types = ['common', 'uncommon', 'rare', 'legendary']
        if enemy_rarity == 'common':
            weight = [80, 13, 6, 1]
        elif enemy_rarity == 'uncommon':
            weight = [50, 30, 15, 5]
        elif enemy_rarity == 'rare':
            weight = [10, 30, 40, 20]
        else:
            weight = [2, 8, 20, 70]
        chosen_rarity = random.choices(rarity_types, weights=weight, k=1)[0]
        chosen_drop_pool = {name: data for name, data in chosen_drops.items() if data['rarity'] == chosen_rarity}
        if not chosen_drop_pool:
            return "apple"
        return random.choice(list(chosen_drop_pool.keys()))