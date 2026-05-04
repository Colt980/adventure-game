
# game.py
from WanderingMonster import WanderingMonster
import json
import random
import gamefunctions as gf
import map_interface as mi





# ---------------- SAVE SYSTEM ---------------- #
SAVE_FILE = "savegame.json"

def save_game():
    save_state = state.copy()

    # convert monsters to dicts
    save_state["monsters"] = [m.to_dict() for m in state["monsters"]]

    with open(SAVE_FILE, "w") as f:
        json.dump(save_state, f)

def load_game():
    global state
    try:
        with open(SAVE_FILE, "r") as f:
            loaded = json.load(f)

        # rebuild monsters
        loaded["monsters"] = [WanderingMonster.from_dict(m) for m in loaded["monsters"]]

        state = loaded
        return True

    except FileNotFoundError:
        print("No save file found.")
        return False

# ---------------- START MENU ---------------- #
print("[1] New Game")
print("[2] Load Game")

choice = input("> ")

if choice == "2" and load_game():
    pass
else:
    name = input("Enter your name: ")
    state = {"player_name": name, "player_hp": 30, "player_gold": 200, "player_inventory": [],"monsters": [WanderingMonster.random_spawn([], [], 10, 10)],"map_state": mi.create_map_state()}

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
    print("[6] Explore Codingsville") # added explore option
    print("[7] Save and Quit")
#-------------Changed Quit -> SAVE AND QUIT------------------------#

    choice = input("> ")

    while choice not in ["1", "2", "3", "4", "5", "6","7"]:
        print("Invalid choice.")
        choice = input("> ")

    return choice

#-----------------------------Exploration------------------#


# ----------------- SHOP ----------------- #
def visit_shop():
    print_header("SHOP")

    print("[1] Sword (50g) - +5 damage, limited uses")
    print("[2] Magic Stone (30g) - Instantly defeats monster")
    print("[3] Leave")

    choice = input("> ")

    if choice == "1" and state["player_gold"] >= 50:
        item = {"name": "sword", "type": "weapon", "maxDurability": 5, "currentDurability": 5, "equipped": False}
        state["player_inventory"].append(item)
        state["player_gold"] -= 50
        print("Purchased sword.")

    elif choice == "2" and state["player_gold"] >= 30:
        item = {"name": "magic stone", "type": "consumable"}
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
        print("Combat is now part of exploration. Choose option 6 to explore the map.")
        
    elif choice == "2":
        sleep_in_town()
    elif choice == "3":
        visit_shop()
    elif choice == "4":
        equip_weapon()
    elif choice == "5":
        show_inventory()
    elif choice == "6":

        if "map_state" not in state:
            state["map_state"] = mi.create_map_state()

        result, state["map_state"] = mi.run_map_interface(state["map_state"])

        if result == "combat":
            print("\nCombat triggered!")

        elif result == "returned_to_town":
            print("You returned to town safely.")

        elif result == "quit":
            print("Exited map.")
        
        # ----------------------------
        # HANDLE MAP RESULT
        # ----------------------------

    if result == "combat":
        print("\nYou encountered a monster!")
        print("Entering combat...")

    # HERE is where you'd call a combat loop later
    # for now you can just simulate or pause
    # or eventually: combat.run(state)
    elif result == "returned_to_town":
        print("You returned to town safely.")

    elif result == "quit":
        print("Exited map.")

        # ----------------------------
        # MONSTER MOVEMENT
        # ----------------------------

        occupied = [(m.x, m.y) for m in state["monsters"]]
        player_pos = state["map_state"]["player_pos"]
        town_pos = state["map_state"]["town_pos"]

        for m in state["monsters"]:
            m.move(occupied=occupied, forbidden=[tuple(player_pos), tuple(town_pos)],grid_w=10,grid_h=10)

        # ----------------------------
        # RESPAWN IF EMPTY
        # ----------------------------

        if len(state["monsters"]) == 0:
            state["monsters"] = [WanderingMonster.random_spawn([], [], 10, 10), WanderingMonster.random_spawn([], [], 10, 10)]
        
    elif choice == "7":
        save_game()
        print("\nGame saved. Thanks for playing!")
        break
    #--------CHANGED THANKS FOR PLAYING -> GAME SAVED-----------#