
# game.py
import random
import gamefunctions as gf

# ----------------- STATE ----------------- #
state = {
    "player_name": input("Enter your name: "),
    "player_hp": 30,
    "player_gold": 200,
    "player_inventory": [],
}

gf.print_welcome(state["player_name"], 40)

# ----------------- UI HELPERS ----------------- #
def print_divider():
    print("\n" + "-" * 40)

def print_header(title):
    print_divider()
    print(f"{title:^40}")
    print_divider()

# ----------------- DISPLAY FUNCTIONS ----------------- #
def display_town_status():
    print_header("TOWN")
    print(f"HP: {state['player_hp']} | Gold: {state['player_gold']}")

def show_inventory():
    print_header("INVENTORY")

    if not state["player_inventory"]:
        print("Inventory is empty.")
        return

    for i, item in enumerate(state["player_inventory"]):
        line = f"{i+1}) {item['name']} ({item['type']})"

        if item.get("equipped"):
            line += " [EQUIPPED]"

        if "currentDurability" in item:
            line += f" Durability: {item['currentDurability']}"

        print(line)

# ----------------- INPUT ----------------- #
def get_town_action():
    print("\nChoose an action:")
    print("[1] Fight Monster")
    print("[2] Sleep (5 gold)")
    print("[3] Shop")
    print("[4] Equip Weapon")
    print("[5] Inventory")
    print("[6] Quit")

    choice = input("> ")

    while choice not in ["1", "2", "3", "4", "5", "6"]:
        print("Invalid choice.")
        choice = input("> ")

    return choice

# ----------------- SHOP ----------------- #
def visit_shop():
    print_header("SHOP")

    print("[1] Sword (50g) - +5 damage, limited uses")
    print("[2] Magic Stone (30g) - Instantly defeats monster")
    print("[3] Leave")

    choice = input("> ")

    if choice == "1" and state["player_gold"] >= 50:
        item = {
            "name": "sword",
            "type": "weapon",
            "maxDurability": 5,
            "currentDurability": 5,
            "equipped": False
        }
        state["player_inventory"].append(item)
        state["player_gold"] -= 50
        print("Purchased sword.")

    elif choice == "2" and state["player_gold"] >= 30:
        item = {
            "name": "magic stone",
            "type": "consumable"
        }
        state["player_inventory"].append(item)
        state["player_gold"] -= 30
        print("Purchased magic stone.")

    else:
        print("Invalid choice or not enough gold.")

# ----------------- EQUIP ----------------- #
def equip_weapon():
    weapons = [item for item in state["player_inventory"] if item["type"] == "weapon"]

    if not weapons:
        print("No weapons to equip.")
        return

    print_header("EQUIP WEAPON")

    for i, w in enumerate(weapons):
        print(f"{i+1}) {w['name']} (Durability: {w['currentDurability']})")

    choice = int(input("> ")) - 1

    for w in weapons:
        w["equipped"] = False

    weapons[choice]["equipped"] = True
    print(f"Equipped {weapons[choice]['name']}")

# ----------------- COMBAT ----------------- #
def fight_monster():
    monster = gf.new_random_monster()
    monster_hp = monster['health']

    print_header(f"FIGHT: {monster['name']}")
    print(monster['description'])

    while state["player_hp"] > 0 and monster_hp > 0:
        print(f"\nHP: {state['player_hp']} | {monster['name']} HP: {monster_hp}")
        print("[1] Attack")
        print("[2] Run")
        print("[3] Use Item")

        action = input("> ")

        if action == "1":
            damage_to_monster = random.randint(5, 10)

            # weapon bonus
            for item in state["player_inventory"]:
                if item.get("equipped"):
                    damage_to_monster += 5
                    item["currentDurability"] -= 1

                    if item["currentDurability"] <= 0:
                        print(f"Your {item['name']} broke!")
                        state["player_inventory"].remove(item)
                    break

            damage_to_player = monster['power']

            monster_hp -= damage_to_monster
            state["player_hp"] -= damage_to_player

            print(f"You dealt {damage_to_monster} damage.")
            print(f"The {monster['name']} dealt {damage_to_player} damage!")

        elif action == "2":
            print("You ran away!")
            break

        elif action == "3":
            if not state["player_inventory"]:
                print("No items available.")
                continue

            for i, item in enumerate(state["player_inventory"]):
                print(f"{i+1}) {item['name']}")

            choice = int(input("> ")) - 1
            item = state["player_inventory"][choice]

            if item["name"] == "magic stone":
                print("You used the magic stone! Monster defeated instantly!")
                state["player_inventory"].pop(choice)
                monster_hp = 0

        else:
            print("Invalid action.")

    if state["player_hp"] <= 0:
        print("\nYou passed out... Game Over!")

    elif monster_hp <= 0:
        reward = monster['money']
        state["player_gold"] += reward
        print(f"\nYou defeated the {monster['name']} and earned {reward} gold!")

# ----------------- REST ----------------- #
def sleep_in_town():
    if state["player_gold"] >= 5:
        state["player_hp"] += 10
        state["player_gold"] -= 5
        print(f"\nYou slept and restored 10 HP.")
    else:
        print("\nNot enough gold!")

# ----------------- MAIN LOOP ----------------- #
while True:
    display_town_status()
    choice = get_town_action()

    if choice == "1":
        fight_monster()
        if state["player_hp"] <= 0:
            break
    elif choice == "2":
        sleep_in_town()
    elif choice == "3":
        visit_shop()
    elif choice == "4":
        equip_weapon()
    elif choice == "5":
        show_inventory()
    elif choice == "6":
        print("\nThanks for playing!")
        break