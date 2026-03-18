"""
gamefunctions.py

This module provides basic game functionality for a simple RPG-like game.
It includes functions for printing welcome messages, displaying a shop
menu, purchasing items, and generating random monsters.

Dependencies:
    - random

Functions:
    - print_welcome(name, width)
    - print_shop_menu(item1Name, item1Price, item2Name, item2Price)
    - purchase_item(itemPrice, startingMoney, quantityToPurchase=1)
    - new_random_monster()

This module can be imported and used by other Python files or run
directly to test the functions.
"""

import random

# ---------------- FUNCTIONS ---------------- #

def print_welcome(name, width):
    """
    Prints a centered welcome message.

    Parameters:
        name (str): Player's name to display.
        width (int): Total width for centering the text.

    Returns:
        None

    Example:
        >>> print_welcome("Jeff", 20)
        '    Hello, Jeff!    '
    """
    print(f"{('Hello, ' + name + '!'):^{width}}")


def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints a formatted shop menu with two items.

    Parameters:
        item1Name (str): Name of first item.
        item1Price (float): Price of first item.
        item2Name (str): Name of second item.
        item2Price (float): Price of second item.

    Returns:
        None
    """
    print("/----------------------\\")
    print(f"| {item1Name:<12} ${item1Price:>6.2f} |")
    print(f"| {item2Name:<12} ${item2Price:>6.2f} |")
    print("\\----------------------/")


def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """
    Determines how many items can be purchased and remaining money.

    Parameters:
        itemPrice (int): Price of one item.
        startingMoney (int): Total money available.
        quantityToPurchase (int, optional): Desired quantity to buy. Default is 1.

    Returns:
        tuple: (quantity purchased, remaining money)
    """
    max_affordable = startingMoney // itemPrice
    quantity_purchased = min(quantityToPurchase, max_affordable)
    leftover_money = startingMoney - (quantity_purchased * itemPrice)
    return quantity_purchased, leftover_money


def new_random_monster():
    """
    Generates a random monster with stats.

    Returns:
        dict: Monster data with keys 'name', 'description', 'health',
              'power', and 'money'.
    """
    monsters = ["Goblin", "Reaper Horse", "Slime"]
    monster = random.choice(monsters)

    if monster == "Goblin":
        description = "Cunning creature. Easily distracted by shiny objects. Small and green."
        health = random.randint(10, 30)
        power = random.randint(5, 10)
        money = random.randint(10, 50)
    elif monster == "Reaper Horse":
        description = "Horse composed of only its skeletal structure. Leaves tracks of fire in its wake."
        health = random.randint(30, 60)
        power = random.randint(10, 20)
        money = random.randint(50, 150)
    else:  # Slime
        description = "Creature resembling gelatin. Harmless unless provoked."
        health = random.randint(5, 20)
        power = random.randint(2, 8)
        money = random.randint(5, 25)

    return {
        "name": monster,
        "description": description,
        "health": health,
        "power": power,
        "money": money
    }


def test_functions():
    """Test all functions in the module."""
    print("=== Welcome Tests ===")
    print_welcome("Jeff", 20)
    print_welcome("Audrey", 30)
    print_welcome("Maxx", 25)

    print("\n=== Shop Menu Tests ===")
    print_shop_menu("Apple", 31, "Pear", 1.234)
    print_shop_menu("Egg", 0.23, "Bag of Oats", 12.34)
    print_shop_menu("Golden Apple", 100.69, "Bean Stalk", 3.33)

    print("\n=== Purchase Tests ===")
    print(purchase_item(123, 1000, 3))
    print(purchase_item(123, 201, 3))
    print(purchase_item(341, 2112))

    print("\n=== Monster Tests ===")
    for _ in range(3):
        monster = new_random_monster()
        print(f"{monster['name']} (Health: {monster['health']}, Power: {monster['power']}, Money: {monster['money']})")
        print(f"{monster['description']}\n")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    test_functions()