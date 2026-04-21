import time
import questionary
from colorama import init, Fore, Style
from database import item_database
init()

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
        'Time stop': {'mana': 100, 'type': 'Time stop', 'level': 3},
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
        self.is_player_burning = False
        self.burn_time = 0
        self.is_player_debuffed = False
        self.debuff_time = 0
        self.current_physical_multi = self.physical_multi
        self.current_magic_multi = self.magic_multi
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

    def is_burning(self):
        if self.is_player_burning:
            if self.hp > 0:
                burn_damage = int(self.maxhp * 0.1)
                self.hp -= burn_damage
                self.burn_time -= 1
                print(f"{Fore.RED}You took {burn_damage} fire damage!{Style.RESET_ALL}")
                time.sleep(0.5)
        if self.burn_time <= 0 and self.is_player_burning == True:
            self.is_player_burning = False
            print(f"{Fore.LIGHTGREEN_EX}You are no longer on fire{Style.RESET_ALL}")

    def is_debuffed(self):
        if self.is_player_debuffed:
            self.current_physical_multi -= 0.3
            self.current_magic_multi -= 0.3
            print(f"{Fore.MAGENTA}You are debuffed!{Style.RESET_ALL}")
            self.debuff_time -= 1
        if self.debuff_time <= 0 and self.is_player_debuffed == True:
            self.is_player_debuffed = False
            self.current_physical_multi = self.physical_multi
            self.current_magic_multi = self.magic_multi
            print(f"{Fore.LIGHTGREEN_EX}Your debuff has expired{Style.RESET_ALL}")

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
            damage_output = weapon_damage * self.current_physical_multi
        else:
            damage_output = weapon_damage * self.current_magic_multi
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