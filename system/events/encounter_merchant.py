import time
from database import item_database
import random
import questionary
from colorama import init, Fore, Style
from helpers.type_writer import typewriter


def open_merchant(p1):
    time.sleep(1)
    typewriter(f"\nYou have encountered a {Fore.YELLOW}MERCHANT{Style.RESET_ALL}")
    typewriter(f"You have {Fore.YELLOW}{p1.gold} coins{Style.RESET_ALL}")
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
        "None",
        "I want to sell"
    ]

    while True:
        item_bought = questionary.select("Would you like to buy an item: ", choices=items_for_sale).ask()

        if item_bought == 'None':
            break

        if item_bought == 'I want to sell':
            items_to_be_sold = []
            for item in p1.backpack:
                items_to_be_sold.append(item + f" {int(item_database[item]['price'] / 2)} coins")
            items_to_be_sold.append('Leave')

            items_sold_count = 0
            while items_sold_count < 3:
                item_sold = questionary.select("What item do you want to sell (Max 3):", choices=items_to_be_sold).ask()

                if item_sold == "Leave":
                    break

                item_sold_name = item_sold.rsplit(' ', 2)[0]
                p1.backpack.remove(item_sold_name)
                items_to_be_sold.remove(item_sold)

                sold_price = int(item_database[item_sold_name]['price'] / 2)
                p1.gold += sold_price

                typewriter(
                    f"Sold {Fore.MAGENTA}{item_sold_name}{Style.RESET_ALL}. Gained {Fore.YELLOW}{sold_price} coins{Style.RESET_ALL}.")
                items_sold_count += 1

            continue

        # Buying Logic
        item_name_only = item_bought.rsplit(' ', 2)[0]
        item_price = item_database[item_name_only]['price']

        time.sleep(1)
        if p1.gold >= item_price:
            p1.gold -= item_price
            p1.backpack.append(item_name_only)
            if item_bought in items_for_sale:
                items_for_sale.remove(item_bought)
            typewriter("The item has been added to your inventory!")
            typewriter(f"Coins left: {Fore.YELLOW}{p1.gold}{Style.RESET_ALL}")
        else:
            typewriter(f"{Fore.RED}You do not have enough coins!{Style.RESET_ALL}")
        time.sleep(1)