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
    "Dragon": {
        'hp': (220, 300),
        'damage': 24,
        'coindrop': (80, 130),
        'xp': (420, 560),
        'weakness': 'physical',
        'rarity': 'legendary',
        'name_color': 'RED'
    },
    "Cyclops": {
        'hp': (140, 190),
        'damage': 18,
        'coindrop': (45, 70),
        'xp': (220, 320),
        'weakness': 'magic',
        'rarity': 'rare',
        'name_color': 'GREEN'
    },
    "Orc": {
        'hp': (70, 100),
        'damage': 12,
        'coindrop': (20, 35),
        'xp': (90, 140),
        'weakness': 'magic',
        'rarity': 'uncommon',
        'name_color': 'LIGHTBLACK_EX'
    },
    "Goblin": {
        'hp': (30, 50),
        'damage': 7,
        'coindrop': (6, 16),
        'xp': (25, 45),
        'weakness': 'physical',
        'rarity': 'common',
        'name_color': 'GREEN'
    }
}

trap_database = {
    'Spike': {'damage': (15,25), 'type': 'physical'},
    'Fire': {'damage': (10, 20), 'type': 'fire'},
    'Coin': {'damage': (15,25), 'type': 'coin'},
    'Debuff': {'damage': (5, 10), 'type': 'debuff'}
}

boss_database = {
    'Lich': {
        'hp': (420, 560),
        'damage': 26,
        'coin_drop': (900, 1200),
        'xp_gain': (650, 900),
        'rarity': 'boss',
        'weakness': 'physical',
        'name_color': 'MAGENTA'
    },
    'Dark Knight': {
        'hp': (520, 700),
        'damage': 22,
        'coin_drop': (1050, 1400),
        'xp_gain': (750, 1050),
        'rarity': 'boss',
        'weakness': 'magic',
        'name_color': 'BLACK'
    }
}