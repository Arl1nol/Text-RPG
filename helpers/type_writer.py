import time
import sys
import random
from colorama import Fore, Style

def typewriter(text, speed=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

def shake_text(text, repeats=5):
    """Prints text that looks like it is vibrating (useful for roar/earthquake)."""
    for _ in range(repeats):
        spaces = " " * random.randint(1, 3)
        sys.stdout.write(f"\r{spaces}{text}")
        sys.stdout.flush()
        time.sleep(0.05)
    print(f"\r{text}") # Final placement

def glitch_text(text, speed=0.05):
    """Randomly changes speed or caps to make a boss sound unstable."""
    for char in text:
        if random.random() > 0.8:
            sys.stdout.write(char.upper())
            time.sleep(speed * 2)
        else:
            sys.stdout.write(char)
            time.sleep(speed)
        sys.stdout.flush()
    print()

def boss_banner(boss_name):
    """Creates a stylized border for a boss entrance."""
    border = "=" * (len(boss_name) + 10)
    print(f"\n{Fore.RED}{border}")
    typewriter(f"     {boss_name.upper()}     ", speed=0.1)
    print(f"{border}{Style.RESET_ALL}\n")

def display_health_damage(hp, maxhp, damage):
    damage = min(hp, damage)
    initial_health = int((hp/maxhp) * 20)
    damaged_health = int(((hp-damage)/maxhp) * 20)
    difference = initial_health - damaged_health
    initial_missing_health = (20 - initial_health)*"_"
    for i in range(difference+1):
        visual_health = (f"{Fore.RED}░{Style.RESET_ALL}" * (max(1,initial_health-i) if not damaged_health == 0 else initial_health-i))
        visual_missing_health = '_'*i + initial_missing_health
        sys.stdout.write(f"\rBoss Health: [{visual_health}{visual_missing_health}]")
        sys.stdout.flush()
        time.sleep(0.3)
    print(f"\rBoss Health: [{visual_health}{visual_missing_health}]")

def display_health_heal(hp, maxhp, heal):
    initial_health = int((hp/maxhp) * 20)
    healed_health = int(((hp+heal)/maxhp) * 20)
    difference = healed_health - initial_health
    initial_missing_health = 20 - initial_health
    for i in range(difference+1):
        visual_health = (f"{Fore.RED}░{Style.RESET_ALL}" * (min(20,max(1,initial_health+i))))
        visual_missing_health = '_'*(initial_missing_health - i)
        sys.stdout.write(f"\rBoss Health: [{visual_health}{visual_missing_health}]")
        sys.stdout.flush()
        time.sleep(0.12)
    print(f"\rBoss Health: [{visual_health}{visual_missing_health}]")