# game.py

import gamefunctions as gf

# Ask for player's name
player_name = input("Enter your name: ")

# Use functions from the module
gf.print_welcome(player_name, 30)
gf.print_shop_menu("Sword", 150, "Shield", 100)

qty, remaining = gf.purchase_item(150, 500, 3)
print(f"You purchased {qty} item(s), money left: {remaining}")

monster = gf.new_random_monster()
print(f"\nEncountered monster: {monster['name']}")
print(f"{monster['description']}")
print(f"Health: {monster['health']}  Power: {monster['power']}  Money: {monster['money']}")