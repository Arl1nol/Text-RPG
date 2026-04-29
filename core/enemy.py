from database import item_database, enemy_database
import random
from colorama import init, Fore, Style
import time
from helpers.type_writer import typewriter
from core.entity import Entity

init()

class Enemy(Entity):
    def __init__(self, p1):
        enemy_keys = list(enemy_database.keys())
        enemy_weights = []
        if p1.level <= 3:
            enemy_weights = [1, 8, 26, 65]
        elif p1.level <= 5:
            enemy_weights = [5, 18, 42, 35]
        else:
            enemy_weights = [12, 34, 34, 20]
        enemy = random.choices(enemy_keys, weights=enemy_weights, k=1)[0]
        enemy_stats = enemy_database.get(enemy)
        self.name = enemy
        rarity_hp_scale = {'common': 0.95, 'uncommon': 1.0, 'rare': 1.08, 'legendary': 1.16}
        rarity_damage_scale = {'common': 0.95, 'uncommon': 1.0, 'rare': 1.1, 'legendary': 1.2}
        level_hp_scale = 1 + max(0, p1.level - 1) * 0.09
        level_damage_scale = 1 + max(0, p1.level - 1) * 0.06
        rarity = enemy_stats['rarity']
        self.name_color = enemy_stats.get('name_color', 'WHITE').upper()
        self.name_display = f"{getattr(Fore, self.name_color, Fore.WHITE)}{self.name}{Style.RESET_ALL}"
        self.maxhp = int(random.randint(*enemy_stats['hp']) * level_hp_scale * rarity_hp_scale[rarity])
        self.hp = self.maxhp
        self.base_damage = int(enemy_stats['damage'] * level_damage_scale * rarity_damage_scale[rarity])
        self.current_damage = self.base_damage
        self.coindrop = random.randint(*enemy_stats['coindrop'])
        self.xpdrop = random.randint(*enemy_stats['xp'])
        self.weakness = enemy_stats['weakness']
        super().__init__(self.name, self.hp, self.maxhp, self.base_damage, self.weakness, False)

    def apply_stat_gain(self, amount):
        """Standardizes how damage is added, even for regular enemies."""
        if self.is_enemy_debuffed:
            self.current_damage += int(amount * 0.8)
        else:
            self.current_damage += int(amount)

    def is_dead(self, player):
        if self.hp < 1:
            self.is_alive = False
            typewriter(f"The {self.name_display} has been {Fore.GREEN}defeated{Style.RESET_ALL}!!!")
            typewriter(f"You gained {Fore.YELLOW}{self.coindrop} coins\n{Style.RESET_ALL}")
            player.gold += self.coindrop
            player.gain_xp(self.xpdrop)
            dropped_item = self.drop_item()
            player.backpack.append(dropped_item)
            typewriter(f"{Fore.MAGENTA}{dropped_item}{Style.RESET_ALL} was found and added to your backpack")

    def attack(self, target):
        time.sleep(0.5)
        typewriter(f"\nThe {self.name_display} {Fore.RED}strikes{Style.RESET_ALL}!")
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