import time
from database import item_database
import random
import questionary
from colorama import init, Fore, Style

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