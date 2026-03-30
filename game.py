# game.py
import random
import gamefunctions as gf

# ----------------- INITIAL SETUP ----------------- #
player_name = input("Enter your name: ")
player_hp = 30
player_gold = 50

gf.print_welcome(player_name, 40)

# ----------------- HELPER FUNCTIONS ----------------- #
def display_town_status():
    print("\nYou are in town.")
    print(f"Current HP: {player_hp}, Current Gold: {player_gold}")

def get_town_action():
    print("\nWhat would you like to do?")
    print("1) Leave town (Fight Monster)")
    print("2) Sleep (Restore HP for 5 Gold)")
    print("3) Quit")
    choice = input("Enter your choice: ")
    while choice not in ["1", "2", "3"]:
        print("Invalid choice. Try again.")
        choice = input("Enter your choice: ")
    return choice

def fight_monster():
    global player_hp, player_gold
    monster = gf.new_random_monster()
    monster_hp = monster['health']
    print(f"\nYou encountered a {monster['name']}!")
    print(monster['description'])
    
    while player_hp > 0 and monster_hp > 0:
        print(f"\nYour HP: {player_hp}, Monster HP: {monster_hp}")
        print("1) Attack")
        print("2) Run")
        action = input("Choose your action: ")
        
        if action == "1":
            damage_to_monster = random.randint(5, 10)
            damage_to_player = monster['power']
            monster_hp -= damage_to_monster
            player_hp -= damage_to_player
            print(f"You dealt {damage_to_monster} damage.")
            print(f"The {monster['name']} dealt {damage_to_player} damage to you!")
        elif action == "2":
            print("You ran away!")
            break
        else:
            print("Invalid action. Try again.")
    
    if player_hp <= 0:
        print("\nYou passed out... Game Over!")
    elif monster_hp <= 0:
        reward = monster['money']
        player_gold += reward
        print(f"\nYou defeated the {monster['name']} and earned {reward} gold!")

def sleep_in_town():
    global player_hp, player_gold
    if player_gold >= 5:
        player_hp += 10
        player_gold -= 5
        print(f"\nYou slept and restored 10 HP. Current HP: {player_hp}, Gold: {player_gold}")
    else:
        print("\nNot enough gold to sleep!")

# ----------------- MAIN GAME LOOP ----------------- #
while True:
    display_town_status()
    choice = get_town_action()
    
    if choice == "1":
        fight_monster()
        if player_hp <= 0:
            break
    elif choice == "2":
        sleep_in_town()
    elif choice == "3":
        print("\nThanks for playing!")
        break
