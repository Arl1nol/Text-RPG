from core.player import Player
from system.engage.engage_boss import engage_boss

p1 = Player('Mage')
p1.maxhp = 1000
p1.hp = 1000
p1.maxmana = 10000
p1.mana = 10000
p1.spells.append("Dragon Inferno")


engage_boss(p1)