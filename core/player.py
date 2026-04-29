import time
import questionary
from colorama import init, Fore, Style
from database import item_database
from helpers.type_writer import typewriter
from core.entity import Entity

init()


class Player(Entity):
    CLASS_STATS = {
        'Warrior': {'hp_mod': 30, 'mana_mod': -20, 'p_multi': 0.35, 'm_multi': -0.1, 'mana_regen_mod': -1,
                    'items': ['rusty_dagger'],
                    'start_wep': 'rusty_dagger'},
        'Mage': {'hp_mod': -15, 'mana_mod': 35, 'p_multi': -0.1, 'm_multi': 0.4, 'mana_regen_mod': 4,
                 'items': ['wooden_wand'],
                 'start_wep': 'wooden_wand'},
        'Tank': {'hp_mod': 55, 'mana_mod': -30, 'p_multi': 0.2, 'm_multi': -0.25, 'mana_regen_mod': -2,
                 'items': ['rusty_dagger'],
                 'start_wep': 'rusty_dagger'},
        'Battlemage': {'hp_mod': 10, 'mana_mod': 15, 'p_multi': 0.15, 'm_multi': 0.15, 'mana_regen_mod': 2,
                       'items': ['rusty_dagger', 'wooden_wand'], 'start_wep': 'wooden_wand'}
    }

    SPELL_DATABASE = {
        'Fireball': {'mana': 10, 'type': 'fire', 'level': 1, 'output': 10},
        'Fire Breath': {'mana': 20, 'type': 'fire', 'level': 2, 'output': 25},
        'Dragon Inferno': {'mana': 50, 'type': 'fire', 'level': 3, 'output': 60},
        'Heal': {'mana': 10, 'type': 'heal', 'level': 1, 'output': 20},
        'Super Heal': {'mana': 40, 'type': 'heal', 'level': 2, 'output': 60},
        'Complete Recovery': {'mana': 100, 'type': 'heal', 'level': 3, 'output': 9999},
        'Zap': {'mana': 15, 'type': 'electric', 'level': 1, 'output': 10},
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
            self.mana_regen += stats.get('mana_regen_mod', 0)
            self.backpack.extend(stats['items'])
            self.equipped_weapon = stats['start_wep']
            self.equipped_shield = ''
        else:
            self.role = "Novice"
            self.backpack.append('rusty_dagger')
            typewriter(f'{Fore.RED}Invalid role. Defaulting to Novice stats.{Style.RESET_ALL}')
        self.hp = self.maxhp
        self.mana = self.maxmana
        self.weapon_durability = item_database[self.equipped_weapon]['durability']
        self.shield_overshield = 0
        self.shield_durability = 1
        self.spelllevel = 1
        self.current_physical_multi = self.physical_multi
        self.current_magic_multi = self.magic_multi
        self.spells = [name for name, data in self.SPELL_DATABASE.items() if data['level'] == self.spelllevel]
        super().__init__(self.role, self.hp, self.maxhp, 0, None)
        

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
                typewriter(f"You took {Fore.RED}{burn_damage} fire damage!{Style.RESET_ALL}")
                time.sleep(0.5)
        if self.burn_time <= 0 and self.is_player_burning:
            self.is_player_burning = False
            typewriter(f"{Fore.LIGHTGREEN_EX}You are no longer on fire{Style.RESET_ALL}")

    def is_debuffed(self):
        if self.debuff_time <= 0 and self.is_player_debuffed:
            self.is_player_debuffed = False
            self.current_physical_multi = self.physical_multi
            self.current_magic_multi = self.magic_multi
            typewriter(f"{Fore.LIGHTGREEN_EX}Your debuff has expired{Style.RESET_ALL}")
        if self.is_player_debuffed:
            if self.current_physical_multi == self.physical_multi:
                self.current_physical_multi -= 0.3
                self.current_magic_multi -= 0.3
            typewriter(f"{Fore.MAGENTA}You are debuffed!{Style.RESET_ALL}")
            self.debuff_time -= 1

    def gain_xp(self, xp):
        self.xp += xp
        time.sleep(0.5)
        typewriter(
            f"You have earned {Fore.GREEN}{xp} XP{Style.RESET_ALL}! Current xp: {Fore.GREEN}{self.xp}/{self.xp_to_next_level}{Style.RESET_ALL}")
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
        self.current_physical_multi = self.physical_multi
        self.current_magic_multi = self.magic_multi
        if self.level == 3:
            self.spelllevel = 2
            self.spells = [name for name, data in self.SPELL_DATABASE.items() if data['level'] <= self.spelllevel]
            added_spells = [name for name, data in self.SPELL_DATABASE.items() if data['level'] == self.spelllevel]
            typewriter(f"The spells {Fore.MAGENTA}{added_spells}{Style.RESET_ALL} have been added to your inventory")
        elif self.level == 7:
            self.spelllevel = 3
            self.spells = [name for name, data in self.SPELL_DATABASE.items() if data['level'] <= self.spelllevel]
            added_spells = [name for name, data in self.SPELL_DATABASE.items() if data['level'] == self.spelllevel]
            typewriter(f"The spells {Fore.MAGENTA}{added_spells}{Style.RESET_ALL} have been added to your inventory")
        time.sleep(1)
        typewriter(f"{Fore.YELLOW}LEVEL UP! You are now level {self.level}{Style.RESET_ALL}")
        print(f"HP: {Fore.GREEN}{self.hp}/{self.maxhp}{Style.RESET_ALL}")
        print(f"Mana: {Fore.BLUE}{self.mana}/{self.maxmana}{Style.RESET_ALL}")
        time.sleep(1)

    def regen_mana(self):
        weapon_data = item_database.get(self.equipped_weapon)
        weapon_mana_regen = weapon_data.get('mana_regen_bonus', 0) if weapon_data else 0
        added_mana = self.mana_regen + weapon_mana_regen
        if self.mana < self.maxmana:
            self.mana = min(self.mana + added_mana, self.maxmana)
            typewriter(f"{Fore.BLUE}You regenerated {added_mana} mana{Style.RESET_ALL}")

    def show_stats(self):
        print(
            f"Health: {Fore.GREEN}{max(int(self.hp), 0)}/{self.maxhp}{Style.RESET_ALL} | Mana: {Fore.BLUE}{max(int(self.mana), 0)}/{self.maxmana}{Style.RESET_ALL}")

    def equip_item(self, item):
        item_data = item_database.get(item)
        if not item_data or item not in self.backpack:
            typewriter(f"{Fore.RED}Invalid request.\n{Style.RESET_ALL}")
            return
        if item_data['type'] in ['physical', 'magic']:
            self.equipped_weapon = item
            self.weapon_durability = item_data['durability']
            typewriter(f"You have equipped {Fore.CYAN}{self.equipped_weapon}{Style.RESET_ALL}\n")
            self.maxmana = self.basemaxmana
            if item_data['type'] == 'magic':
                self.maxmana += item_data['mana_boost']
                self.mana = min(self.mana, self.maxmana)
        elif item_data['type'] == 'shield':
            self.equipped_shield = item
            if item_data['kind'] == 'overshield':
                self.shield_overshield = item_data['defense']
            else:
                self.shield_durability = item_data['durability']
            typewriter(f"You have equipped {Fore.CYAN}{self.equipped_shield}{Style.RESET_ALL}\n")
        time.sleep(0.5)

    def use_heal(self, item):
        item_data = item_database.get(item)
        if not item_data or item not in self.backpack or item_data['type'] != 'food':
            typewriter(f"{Fore.RED}Invalid request.{Style.RESET_ALL}")
            return
        if self.hp == self.maxhp:
            typewriter(f"{Fore.RED}HP already full!{Style.RESET_ALL}")
            return
        heal = item_data['boost']
        self.hp = min(self.maxhp, self.hp + heal)
        self.backpack.remove(item)
        typewriter(f'{Fore.GREEN}Ate {item.title()}. Healed {heal}HP. ({self.hp}/{self.maxhp}){Style.RESET_ALL}')
        time.sleep(0.5)

    def filter_backpack(self):
        return [item for item in self.backpack if item_database.get(item)['type'] in ['physical', 'magic']]

    def is_item_broken(self):
        if self.weapon_durability < 1:
            self.backpack.remove(self.equipped_weapon)
            typewriter(f"{Fore.RED}CRACK! Your weapon broke!{Style.RESET_ALL}")
            choices = self.filter_backpack()
            if choices:
                new_weapon = questionary.select("Choose a weapon to equip:", choices=choices).ask()
                self.equip_item(new_weapon)
            else:
                self.equipped_weapon = None
        elif self.shield_durability < 1 and self.equipped_shield != '':
            self.backpack.remove(self.equipped_shield)
            typewriter(f"{Fore.RED}CRACK! Your shield broke!{Style.RESET_ALL}")
            self.equipped_shield = ''

    def attack(self, target):
        weapon_data = item_database.get(self.equipped_weapon)
        weapon_damage = weapon_data['dmg']
        multi = self.current_physical_multi
        damage_output = int(weapon_damage * multi)

        if target.weakness == 'physical':
            damage_output = int(damage_output * 1.5)
            typewriter(f"{Fore.MAGENTA}It's super effective!{Style.RESET_ALL}")

        if weapon_data['rarity'] != 'common':
            self.weapon_durability -= 1
            self.is_item_broken()

        target.take_damage(damage_output)

    def after_shield_damage(self, enemy_attack):
        shield_info = item_database.get(self.equipped_shield)
        if not shield_info:
            return enemy_attack
        if shield_info['kind'] == 'overshield':
            defense = min(self.shield_overshield, enemy_attack)
            self.shield_overshield -= defense
            typewriter(f"{Fore.CYAN}You blocked {defense} damage with your overshield!{Style.RESET_ALL}")
            if self.shield_overshield < 1:
                typewriter(f"{Fore.RED}Overshield depleted!{Style.RESET_ALL}")
                self.backpack.remove(self.equipped_shield)
                self.equipped_shield = ''
            return max(enemy_attack - defense, 0)
        elif shield_info['kind'] == 'buff':
            shield_buff = shield_info['defense'] / 100
            damage_negated = int(enemy_attack * shield_buff)
            typewriter(f'{Fore.CYAN}Shield blocked {damage_negated} damage!{Style.RESET_ALL}')
            self.shield_durability -= 1
            self.is_item_broken()
            return max(0, enemy_attack - damage_negated)
        elif shield_info['kind'] == 'negation':
            self.shield_durability -= 1
            typewriter(f'{Fore.CYAN}Shield negated all damage!{Style.RESET_ALL}')
            self.is_item_broken()
            return 0
        return enemy_attack

    def convert_to_dic(self):
        return {
            "role": self.role, "level": self.level, "xp": self.xp, "xp_to_next_level": self.xp_to_next_level,
            "hp": self.hp, "maxhp": self.maxhp, "mana": self.mana, "maxmana": self.maxmana,
            "basemaxmana": self.basemaxmana, "mana_regen": self.mana_regen, "gold": self.gold,
            "physical_multi": self.physical_multi, "magic_multi": self.magic_multi, "backpack": self.backpack,
            "equipped_weapon": self.equipped_weapon, "weapon_durability": self.weapon_durability,
            "equipped_shield": self.equipped_shield, "shield_durability": self.shield_durability,
            "shield_overshield": self.shield_overshield, "spelllevel": self.spelllevel, "spells": self.spells
        }

    def take_damage(self, enemy_attack):
        taken_damage = self.after_shield_damage(enemy_attack) if self.equipped_shield else enemy_attack
        super().take_damage(taken_damage)

    def cast_spell(self, name, target):
        added_damage = 1
        is_weakness_hit = False
        spell_data = self.SPELL_DATABASE.get(name)
        if target.weakness == 'magic' and not spell_data['type'] == 'heal':
            added_damage = 1.5
            is_weakness_hit = True
        if not spell_data or self.mana < spell_data['mana']:
            typewriter(f"{Fore.RED}Not enough mana!{Style.RESET_ALL}")
            return

        self.mana -= spell_data['mana']
        damage = int(spell_data.get('output', 0) * self.magic_multi * added_damage)

        if spell_data['type'] == 'fire':
            target.is_enemy_burning = True
            target.burn_time = spell_data['level']
        elif spell_data['type'] == 'heal':
            self.hp = min(self.maxhp, self.hp + damage)
            typewriter(f"{Fore.GREEN}Healed {damage}HP!{Style.RESET_ALL}")
            return
        elif spell_data['type'] == 'electric':
            target.is_enemy_debuffed = True
            target.debuff_time = spell_data['level']
        elif spell_data['type'] == 'Time stop':
            target.freeze_time = spell_data['level']
            target.is_enemy_frozen = True
            target.can_i_attack = False

        if is_weakness_hit:
            typewriter(f"{Fore.MAGENTA}It's super effective!{Style.RESET_ALL}")
        typewriter(f"{Fore.RED}{name}{Style.RESET_ALL} cast!")
        
        target.take_damage(damage)
