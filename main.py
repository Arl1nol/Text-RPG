import random
import time
import questionary
import json
import glob
from colorama import init, Fore, Style
import os
init()

item_database = {
    "apple": {"type": "food", "rarity": "common", "boost": 10, "price": 5},
    "bread": {"type": "food", "rarity": "common", "boost": 15, "price": 8},
    "berries": {"type": "food", "rarity": "common", "boost": 5, "price": 2},
    "dried_fish": {"type": "food", "rarity": "common", "boost": 12, "price": 6},
    "cooked_meat": {"type": "food", "rarity": "uncommon", "boost": 40, "price": 25},
    "stew": {"type": "food", "rarity": "uncommon", "boost": 50, "price": 35},
    "golden_elixir": {"type": "food", "rarity": "rare", "boost": 100, "price": 150},
    "ambrosia": {"type": "food", "rarity": "legendary", "boost": 500, "price": 1000},
    "wooden_lid": {"type": "shield", "rarity": "common", "defense": 10, 'kind': 'overshield', "price": 10},
    "pot_lid": {"type": "shield", "rarity": "common", "defense": 40, 'kind': 'overshield', "price": 30},
    "buckler": {"type": "shield", "rarity": "common", "defense": 100, 'kind': 'overshield', "price": 50},
    "iron_shield": {"type": "shield", "rarity": "uncommon", "defense": 150, 'kind': 'overshield', "price": 200},
    "reinforced_wood": {"type": "shield", "rarity": "uncommon", "defense": 12, 'kind': 'buff', 'durability': 20,
                        "price": 60},
    "knight_shield": {"type": "shield", "rarity": "rare", "defense": 30, 'kind': 'buff', 'durability': 20,
                      "price": 250},
    "dragon_scale_shield": {"type": "shield", "rarity": "rare", 'kind': 'negation', 'durability': 3, "price": 400},
    "aegis_of_light": {"type": "shield", "rarity": "legendary", 'kind': 'negation', 'durability': 5, "price": 1200},
    "rusty_dagger": {"type": "physical", "rarity": "common", "dmg": 8, "durability": 15, "price": 20},
    "stick": {"type": "physical", "rarity": "common", "dmg": 2, "durability": 5, "price": 1},
    "club": {"type": "physical", "rarity": "common", "dmg": 10, "durability": 20, "price": 30},
    "dull_axe": {"type": "physical", "rarity": "common", "dmg": 12, "durability": 10, "price": 25},
    "iron_sword": {"type": "physical", "rarity": "uncommon", "dmg": 20, "durability": 30, "price": 100},
    "spear": {"type": "physical", "rarity": "uncommon", "dmg": 18, "durability": 40, "price": 90},
    "mace": {"type": "physical", "rarity": "uncommon", "dmg": 25, "durability": 25, "price": 120},
    "war_hammer": {"type": "physical", "rarity": "rare", "dmg": 45, "durability": 25, "price": 450},
    "katana": {"type": "physical", "rarity": "rare", "dmg": 40, "durability": 50, "price": 500},
    "dragon_slayer": {"type": "physical", "rarity": "legendary", "dmg": 95, "durability": 100, "price": 2500},
    "wooden_wand": {'dmg': 5, "type": "magic", "rarity": "common", "dmg_multi": 1.10, "mana_boost": 10,
                    "durability": 10, "price": 40, 'mana_regen_bonus': 5},
    "burnt_branch": {'dmg': 8, "type": "magic", "rarity": "common", "dmg_multi": 1.05, "mana_boost": 5, "durability": 5,
                     "price": 5, 'mana_regen_bonus': 8},
    "old_tome": {'dmg': 12, "type": "magic", "rarity": "common", "dmg_multi": 1.08, "mana_boost": 15, "durability": 12,
                 "price": 30, 'mana_regen_bonus': 10},
    "apprentice_staff": {'dmg': 20, "type": "magic", "rarity": "uncommon", "dmg_multi": 1.25, "mana_boost": 30,
                         "durability": 20, "price": 150, 'mana_regen_bonus': 15},
    "crystal_shard": {'dmg': 25, "type": "magic", "rarity": "uncommon", "dmg_multi": 1.30, "mana_boost": 20,
                      "durability": 10, "price": 180, 'mana_regen_bonus': 23},
    "wizard_orb": {'dmg': 32, "rarity": "rare", "type": "magic", "dmg_multi": 1.50, "mana_boost": 60, "durability": 15,
                   "price": 600, 'mana_regen_bonus': 30},
    "runic_blade": {'dmg': 41, "type": "magic", "rarity": "rare", "dmg_multi": 1.45, "mana_boost": 40, "durability": 35,
                    "price": 550, 'mana_regen_bonus': 40},
    "staff_of_eternity": {'dmg': 55, "type": "magic", "rarity": "legendary", "dmg_multi": 2.10, "mana_boost": 150,
                          "durability": 50, "price": 3000, 'mana_regen_bonus': 50}
}

enemy_database = {
    "Dragon": {'hp': (500, 600), 'damage': 60, 'coindrop': (100, 120), 'xp': (1000, 1200), 'weakness': 'physical',
               'rarity': 'legendary'},
    "Cyclops": {'hp': (350, 420), 'damage': 10, 'coindrop': (40, 50), 'xp': (300, 400), 'weakness': 'none',
                'rarity': 'rare'},
    "Orc": {'hp': (20, 30), 'damage': 55, 'coindrop': (20, 30), 'xp': (100, 200), 'weakness': 'magic',
            'rarity': 'uncommon'},
    "Goblin": {'hp': (10, 20), 'damage': 7, 'coindrop': (10, 15), 'xp': (20, 40), 'weakness': 'magic',
               'rarity': 'common'},
}

class Player:

    CLASS_STATS = {
        'Warrior': {'hp_mod': 20, 'mana_mod': -30, 'p_multi': 0.5, 'm_multi': -0.2, 'items': ['rusty_dagger'],
                    'start_wep': 'rusty_dagger'},
        'Mage': {'hp_mod': -20, 'mana_mod': 50, 'p_multi': -0.2, 'm_multi': 0.5, 'items': ['wooden_wand'],
                 'start_wep': 'wooden_wand'},
        'Tank': {'hp_mod': 100, 'mana_mod': -50, 'p_multi': 0.1, 'm_multi': -0.4, 'items': ['rusty_dagger'],
                 'start_wep': 'rusty_dagger'},
        'Battlemage': {'hp_mod': 10, 'mana_mod': 10, 'p_multi': 0.1, 'm_multi': 0.1,
                       'items': ['rusty_dagger', 'wooden_wand'], 'start_wep': 'wooden_wand'}
    }

    SPELL_DATABASE = {
        'Fireball': {'mana': 10, 'type': 'fire', 'level': 1, 'output': 15},
        'Fire Breath': {'mana': 20, 'type': 'fire', 'level': 2, 'output': 35},
        'Dragon Inferno': {'mana': 50, 'type': 'fire', 'level': 3, 'output': 70},
        'Heal': {'mana': 10, 'type': 'heal', 'level': 1, 'output': 20},
        'Super Heal': {'mana': 40, 'type': 'heal', 'level': 2, 'output': 60},
        'Complete Recovery': {'mana': 100, 'type': 'heal', 'level': 3, 'output': 9999},
        'Zap': {'mana': 10, 'type': 'electric', 'level': 1, 'output': 10},
        'Lightning': {'mana': 50, 'type': 'electric', 'level': 2, 'output': 25},
        'Thunder Storm': {'mana': 80, 'type': 'electric', 'level': 3, 'output': 55},
        'Time stop': {'mana': 100, 'type': 'Time Stop', 'level': 3},
    }

    def __init__(self, role):
        self.maxhp, self.basemaxmana, self.maxmana, self.gold = 100, 100, 100, 100
        self.physical_multi, self.magic_multi = 1.0, 1.0
        self.mana_regen = 10
        self.backpack = ['apple']
        self.role = role
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100
        stats = self.CLASS_STATS.get(role)
        if stats:
            self.maxhp += stats['hp_mod']
            self.maxmana += stats['mana_mod']
            self.basemaxmana += stats['mana_mod']
            self.physical_multi += stats['p_multi']
            self.magic_multi += stats['m_multi']
            self.backpack.extend(stats['items'])
            self.equipped_weapon = stats['start_wep']
            self.equipped_shield = ''
        else:
            self.role = "Novice"
            self.backpack.append('rusty_dagger')
            print(f'{Fore.RED}Invalid role. Defaulting to Novice stats.{Style.RESET_ALL}')
        self.hp = self.maxhp
        self.mana = self.maxmana
        self.weapon_durability = item_database[self.equipped_weapon]['durability']
        self.shield_overshield = 0
        self.shield_durability = 1
        self.spelllevel = 1
        self.spells = [name for name, data in self.SPELL_DATABASE.items() if data['level'] == self.spelllevel]
        print(f"{Fore.YELLOW}--- Character Summary ---{Style.RESET_ALL}")
        print(f"Role: {Fore.CYAN}{self.role}{Style.RESET_ALL}")
        print(f"HP: {Fore.GREEN}{self.hp}/{self.maxhp}{Style.RESET_ALL}")
        print(f"Mana: {Fore.BLUE}{self.mana}/{self.maxmana}{Style.RESET_ALL}")
        print(f"Backpack: {self.backpack}")
        print(f"Spells: {Fore.MAGENTA}{self.spells}{Style.RESET_ALL}")
        print(f"Equipped Weapon: {self.equipped_weapon}")
        print(f"Physical Multiplier: {self.physical_multi:.2f}")
        print(f"Magic Multiplier: {self.magic_multi:.2f}\n")
        time.sleep(1.5)

    def gain_xp(self, xp):
        self.xp += xp
        time.sleep(0.5)
        print(f"{Fore.YELLOW}You have earned {xp} XP! Current xp: {self.xp}/{self.xp_to_next_level}{Style.RESET_ALL}")
        while self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.xp -= self.xp_to_next_level
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        self.maxhp = int(self.maxhp * 1.1)
        self.basemaxmana = int(self.basemaxmana * 1.1)
        self.maxmana = int(self.maxmana * 1.1)
        self.physical_multi *= 1.1
        self.magic_multi *= 1.1
        self.hp = self.maxhp
        self.mana = self.maxmana
        if self.level == 5:
            self.spelllevel = 2
            self.spells = [name for name, data in self.SPELL_DATABASE.items() if data['level'] == self.spelllevel]
        elif self.level == 10:
            self.spelllevel = 3
            self.spells = [name for name, data in self.SPELL_DATABASE.items() if data['level'] == self.spelllevel]
        time.sleep(1)
        print(f"{Fore.YELLOW}You have leveled up!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}You are now level {self.level}{Style.RESET_ALL}")
        print("Your new stats:")
        print(f"HP: {Fore.GREEN}{self.hp}/{self.maxhp}{Style.RESET_ALL}")
        print(f"Mana: {Fore.BLUE}{self.mana}/{self.maxmana}{Style.RESET_ALL}")
        print(f"Physical Multiplier: {self.physical_multi:.2f}")
        print(f"Magic Multiplier: {self.magic_multi:.2f}\n")
        time.sleep(2)

    def regen_mana(self):
        weapon_data = item_database.get(self.equipped_weapon)
        weapon_mana_regen = weapon_data.get('mana_regen_bonus', 0)
        added_mana = self.mana_regen + weapon_mana_regen
        if self.mana < self.maxmana:
            self.mana += added_mana
            self.mana = min(self.mana, self.maxmana)
            print(f"{Fore.BLUE}You regenerated {added_mana} mana{Style.RESET_ALL}")

    def show_stats(self):
        print(f"Your current health: {Fore.GREEN}{max(int(self.hp), 0)}/{self.maxhp}{Style.RESET_ALL}")
        print(f"Your current mana: {Fore.BLUE}{max(int(self.mana), 0)}/{self.maxmana}{Style.RESET_ALL}")

    def equip_item(self, item):
        item_data = item_database.get(item)
        if not item_data or item not in self.backpack:
            print(f"{Fore.RED}Invalid request.\n{Style.RESET_ALL}")
            return
        if item_data['type'] in ['physical', 'magic']:
            self.equipped_weapon = item
            self.weapon_durability = item_data['durability']
            print(f"You have equipped {Fore.CYAN}{self.equipped_weapon}{Style.RESET_ALL}\n")
            self.maxmana = self.basemaxmana
            if item_data['type'] == 'magic':
                self.maxmana = self.basemaxmana
                self.maxmana += item_data['mana_boost']
                if self.mana > self.maxmana:
                    self.mana = self.maxmana
        elif item_data['type'] == 'shield':
            self.equipped_shield = item
            if item_data['kind'] == 'overshield':
                self.shield_overshield = item_data['defense']
            else:
                self.shield_durability = item_data['durability']
            print(f"You have equipped {Fore.CYAN}{self.equipped_shield}{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}You cannot equip this item!\n{Style.RESET_ALL}")
        time.sleep(0.5)

    def use_heal(self, item):
        item_data = item_database.get(item)
        if not item_data or item not in self.backpack:
            print(f"{Fore.RED}Invalid request.\n{Style.RESET_ALL}")
            return
        if item_data['type'] != 'food':
            print(f"{Fore.RED}You can only eat food!\n{Style.RESET_ALL}")
            return
        if self.hp == self.maxhp:
            print(f"{Fore.RED}Your HP is already full!\n{Style.RESET_ALL}")
            return
        heal = item_data['boost']
        self.hp = min(self.maxhp, self.hp + heal)
        self.backpack.remove(item)
        print(f'{Fore.GREEN}You ate the {item.title()}. Healed {heal}HP. Current HP: {self.hp}/{self.maxhp}\n{Style.RESET_ALL}')
        time.sleep(0.8)

    def filter_backpack(self):
        return [item for item in self.backpack if item_database.get(item)['type'] in ['physical', 'magic']]

    def is_item_broken(self):
        if self.weapon_durability < 1:
            self.backpack.remove(self.equipped_weapon)
            print(f"{Fore.RED}CRACK! Your weapon broke!{Style.RESET_ALL}")
            time.sleep(0.5)
            choices = self.filter_backpack()
            if choices:
                new_weapon = questionary.select("Choose a weapon to equip:", choices=choices).ask()
                self.equip_item(new_weapon)
            else:
                self.equipped_weapon = None
        elif self.shield_durability < 1 and self.equipped_shield != '':
            self.backpack.remove(self.equipped_shield)
            print(f"{Fore.RED}CRACK! Your shield broke!{Style.RESET_ALL}")
            self.equipped_shield = ''

    def attack(self, target):
        if not self.equipped_weapon:
            target.hp -= 2
            print(f"\n{Fore.YELLOW}You dealt 2 damage to the {target.name}!{Style.RESET_ALL}")
            return
        weapon_data = item_database.get(self.equipped_weapon)
        weapon_damage = weapon_data['dmg']
        if weapon_data['type'] == 'physical':
            damage_output = weapon_damage * self.physical_multi
        else:
            damage_output = weapon_damage * self.magic_multi
        if target.weakness == weapon_data['type']:
            damage_output = damage_output * 1.5
            print(f"{Fore.MAGENTA}It's super effective!{Style.RESET_ALL}")
        damage_output = int(damage_output)
        target.hp -= damage_output
        print(f"\n{Fore.YELLOW}You dealt {damage_output} damage to the {target.name}!{Style.RESET_ALL}")
        print(f"{target.name} (HP: {Fore.RED}{max(0, int(target.hp))} / {target.maxhp}{Style.RESET_ALL})")
        if weapon_data['rarity'] != 'common':
            self.weapon_durability -= 1
            self.is_item_broken()

    def after_shield_damage(self, enemy_attack):
        shield_info = item_database.get(self.equipped_shield)
        if not shield_info:
            return enemy_attack
        if shield_info['kind'] == 'overshield':
            defense = min(self.shield_overshield, enemy_attack)
            self.shield_overshield -= defense
            returned_damage = enemy_attack - defense
            print(f"{Fore.CYAN}You blocked {defense} of the damage{Style.RESET_ALL}")
            if self.shield_overshield < 1:
                print(f"{Fore.RED}Your shield broke{Style.RESET_ALL}")
                self.backpack.remove(self.equipped_shield)
                self.equipped_shield = ''
            return max(returned_damage, 0)
        elif shield_info['kind'] == 'buff':
            shield_buff = shield_info['defense'] / 100
            damage_negated = int(enemy_attack * shield_buff)
            enemy_attack -= damage_negated
            self.shield_durability -= 1
            print(f'{Fore.CYAN}Your shield blocked {damage_negated} of the incoming damage!{Style.RESET_ALL}')
            self.is_item_broken()
            return max(0, int(enemy_attack))
        elif shield_info['kind'] == 'negation':
            self.shield_durability -= 1
            print(f'{Fore.CYAN}Your shield blocked all of the incoming damage!{Style.RESET_ALL}')
            self.is_item_broken()
            return 0
        return enemy_attack

    def convert_to_dic(self):
        save_data = {
            "role": self.role,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next_level": self.xp_to_next_level,
            "hp": self.hp,
            "maxhp": self.maxhp,
            "mana": self.mana,
            "maxmana": self.maxmana,
            "basemaxmana": self.basemaxmana,
            "mana_regen": self.mana_regen,
            "gold": self.gold,
            "physical_multi": self.physical_multi,
            "magic_multi": self.magic_multi,
            "backpack": self.backpack,
            "equipped_weapon": self.equipped_weapon,
            "weapon_durability": self.weapon_durability,
            "equipped_shield": self.equipped_shield,
            "shield_durability": self.shield_durability,
            "shield_overshield": self.shield_overshield,
            "spelllevel": self.spelllevel,
            "spells": self.spells
        }
        return save_data

    def take_damage(self, enemy_attack):
        print(f"{Fore.RED}The enemy attacked with {enemy_attack} damage{Style.RESET_ALL}")
        taken_damage = enemy_attack
        if self.equipped_shield:
            taken_damage = self.after_shield_damage(enemy_attack)
        self.hp -= taken_damage
        time.sleep(0.5)
        print(f"Your health: {Fore.GREEN}{max(0, int(self.hp))}/{self.maxhp}{Style.RESET_ALL}\n")

    def cast_spell(self, name, target):
        spell_data = self.SPELL_DATABASE.get(name)
        if spell_data:
            damage = int(spell_data.get('output', 0) * self.magic_multi)
            if spell_data['type'] == 'fire':
                target.is_enemy_burning = True
                target.burn_time = spell_data['level']
            elif spell_data['type'] == 'heal':
                self.hp = min(self.maxhp, self.hp + damage)
                print(f"{Fore.GREEN}You healed {damage}HP!{Style.RESET_ALL}")
                return
            elif spell_data['type'] == 'electric':
                target.is_enemy_debuffed = True
                target.debuff_time = spell_data['level']
            elif spell_data['type'] == 'Time stop':
                target.freeze_time = spell_data['level']
                target.is_enemy_frozen = True
                target.can_i_attack = False
            target.hp -= damage
            print(f"{Fore.YELLOW}{target.name} took {damage} damage!{Style.RESET_ALL}")
            print(f"{target.name} (HP: {Fore.RED}{max(0, int(target.hp))}/{target.maxhp}{Style.RESET_ALL})")
            time.sleep(0.5)


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

def save_adventure(save, saved_stats):
    save_name = save
    saved_stats = saved_stats
    with open(save_name, 'w') as f:
        json.dump(saved_stats, f, indent=4)
    print(f"{Fore.GREEN}Game has been saved to {save_name}{Style.RESET_ALL}")


def tdt():
    for _ in range(3):
        print('.', end='', flush=True)
        time.sleep(0.5)
    print('\n')

saves = glob.glob('*save*')

if saves:
    if questionary.select("Do you want to load an existing save?", choices=['Yes', "No"]).ask() == 'Yes':
        chosen_save = questionary.select("Which save do you want to load:", choices=saves).ask()
        try:
            with open(chosen_save, 'r') as f:
                data = json.load(f)

                p1 = Player(data['role'])

                p1.level = data['level']
                p1.xp = data['xp']
                p1.xp_to_next_level = data['xp_to_next_level']

                p1.hp = data['hp']
                p1.maxhp = data['maxhp']
                p1.mana = data['mana']
                p1.maxmana = data['maxmana']
                p1.basemaxmana = data['basemaxmana']
                p1.mana_regen = data['mana_regen']

                p1.gold = data['gold']
                p1.backpack = data['backpack']

                p1.physical_multi = data['physical_multi']
                p1.magic_multi = data['magic_multi']

                p1.equipped_weapon = data['equipped_weapon']
                p1.weapon_durability = data['weapon_durability']
                p1.equipped_shield = data['equipped_shield']
                p1.shield_durability = data['shield_durability']
                p1.shield_overshield = data['shield_overshield']

                p1.spelllevel = data['spelllevel']
                p1.spells = data['spells']

                print(f"{Fore.GREEN}Data has been loaded{Style.RESET_ALL}")
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("There has been a corruption on the file you want to open")
            try:
                os.remove(chosen_save)
                print("The file has been deleted and you started a new adventure")
            except OSError:
                print("Delete has failed")
            your_class = questionary.select("What class do you want to be?",
                                            choices=['Warrior', 'Mage', 'Tank', 'Battlemage']).ask()
            p1 = Player(your_class)
            saves = glob.glob('*save*')
    else:
        your_class = questionary.select("What class do you want to be?",
                                        choices=['Warrior', 'Mage', 'Tank', 'Battlemage']).ask()
        p1 = Player(your_class)

def engage_enemy(p1):
    e1 = Enemy()
    player_dead = False
    print(f'\n{Fore.RED}You encountered a {e1.name} (HP: {int(e1.hp)}/{e1.maxhp})!{Style.RESET_ALL}')
    while p1.hp > 0 and e1.hp > 0:
        choice = questionary.select("Your move:", choices=["Attack", "Use Item", "Equip Item", "Cast Spell"]).ask()
        time.sleep(0.5)
        if choice == 'Attack':
            p1.attack(e1)
        elif choice == 'Use Item':
            filtered_usables = [item for item in p1.backpack if item_database.get(item)['type'] in ['food']]
            if filtered_usables:
                item = questionary.select("Use what:", choices=filtered_usables).ask()
                p1.use_heal(item)
            else:
                print(f"{Fore.RED}No food in backpack!{Style.RESET_ALL}")
        elif choice == 'Equip Item':
            filtered_equipables = [item for item in p1.backpack if
                                   item_database.get(item)['type'] in ['physical', 'magic', 'shield']]
            if filtered_equipables:
                item = questionary.select("Equip what:", choices=filtered_equipables).ask()
                p1.equip_item(item)
            else:
                print(f"{Fore.RED}Nothing to equip!{Style.RESET_ALL}")
        elif choice == 'Cast Spell':
            spell_choice = questionary.select('What spell do you want to cast: ', choices=p1.spells).ask()
            p1.cast_spell(spell_choice, e1)

        e1.is_burning()
        e1.is_debuffed()
        e1.is_frozen()
        e1.is_dead(p1)

        if not e1.is_alive:
            p1.show_stats()
            break
        if e1.can_i_attack:
            e1.attack(p1)
        p1.show_stats()
        if p1.hp < 1:
            print(f"{Fore.RED}You died!!!{Style.RESET_ALL}")
            player_dead = True
            break
        p1.regen_mana()
    return player_dead

def open_merchant(p1):
    time.sleep(1)
    print(f"\nYou have encountered a {Fore.YELLOW}MERCHANT{Style.RESET_ALL}")
    print(f"You have {Fore.YELLOW}{p1.gold} coins{Style.RESET_ALL}")
    time.sleep(1)
    common_item = random.choice([name for name, data in item_database.items() if data.get('rarity') == 'common'])
    uncommon_item = random.choice([name for name, data in item_database.items() if data.get('rarity') == 'uncommon'])
    rare_item = random.choice([name for name, data in item_database.items() if data.get('rarity') == 'rare'])
    legendary_item = random.choice([name for name, data in item_database.items() if data.get('rarity') == 'legendary'])
    items_for_sale = [
        common_item + f" {item_database[common_item]['price']} coins",
        uncommon_item + f" {item_database[uncommon_item]['price']} coins",
        rare_item + f" {item_database[rare_item]['price']} coins",
        legendary_item + f" {item_database[legendary_item]['price']} coins",
        "None"
    ]
    while True:
        item_bought = questionary.select("Would you like to buy an item: ", choices=items_for_sale).ask()
        if item_bought == 'None':
            break
        item_name_only = item_bought.rsplit(' ', 2)[0]
        item_price = item_database[item_name_only]['price']
        time.sleep(1)
        if p1.gold >= item_price:
            p1.gold -= item_price
            p1.backpack.append(item_name_only)
            items_for_sale.remove(item_bought)
            print("The item has been added to your inventory!")
            print(f"Coins left: {p1.gold}")
        else:
            print("You do not have enough coins to buy that weapon")
        time.sleep(1)


def run_adventure():
    print("You go down the path")
    tdt()
    while True:
        if engage_enemy(p1):
            break
        if True: #random.random() < 0.25:
            open_merchant(p1)
        if questionary.select("Continue?", choices=['Yes', 'No']).ask() == 'No':
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
            break

if questionary.select("Are you ready to start?", choices=["Yes", 'No']).ask() == 'Yes':
    run_adventure()

else:
    running = False
    print("You cower away...")

