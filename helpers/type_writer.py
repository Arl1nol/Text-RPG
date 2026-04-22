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