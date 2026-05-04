from WanderingMonster import WanderingMonster
import pygame

TILE_SIZE = 32
MAP_SIZE = 10


# ---------------- MAP STATE ---------------- #
def create_map_state():
    return {"mode": "explore","player_pos": [5, 5],"town_pos": [0, 0],"monsters": [WanderingMonster.random_spawn([], [], 10, 10)],"active_monster": None}


# ---------------- PLAYER MOVEMENT ---------------- #
def move_player(game_state, direction):
    x, y = game_state["player_pos"]

    if direction == "up":
        y -= 1
    elif direction == "down":
        y += 1
    elif direction == "left":
        x -= 1
    elif direction == "right":
        x += 1

    # boundaries
    x = max(0, min(MAP_SIZE - 1, x))
    y = max(0, min(MAP_SIZE - 1, y))

    game_state["player_pos"] = [x, y]

    # check town
    if [x, y] == game_state["town_pos"]:
        return "returned_to_town"

    # check monster encounter
    # check monster collision (FORCED COMBAT)
    for m in game_state["monsters"]:
        if [x, y] == [m.x, m.y]:
            game_state["active_monster"] = m
            game_state["mode"] = "combat"
            return "combat"

    return "moved"

# Combat system
def handle_combat_input(game_state, key):
    monster = game_state["active_monster"]
    player = game_state.get("player", {"hp": 20})

    if key == pygame.K_1:
        # attack
        monster.hp -= 5

        if monster.hp <= 0:
            game_state["monsters"].remove(monster)
            game_state["mode"] = "explore"
            game_state["active_monster"] = None
            return "victory"

        # monster counterattack
        player["hp"] -= monster.attack
        game_state["player"] = player

    elif key == pygame.K_2:
        # run away
        game_state["mode"] = "explore"
        game_state["active_monster"] = None
        return "escaped"

    return "combat"

occupied = [(m.x, m.y) for m in state["monsters"]]
player_pos = state["map_state"]["player_pos"]
town_pos = state["map_state"]["town_pos"]

for m in state["monsters"]:
    m.move(occupied=occupied, forbidden=[tuple(player_pos), tuple(town_pos)],grid_w=10,grid_h=10)

# ---------------- MAP LOOP ---------------- #
def run_map_interface(game_state):
    pygame.init()

    screen = pygame.display.set_mode((320, 320))
    clock = pygame.time.Clock()

    while True:

        result = None

        # ---------------- EVENTS ---------------- #
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit", game_state

            if event.type == pygame.KEYDOWN:

                if game_state["mode"] != "explore":
                    continue  # ignore movement during combat

                
                if event.key == pygame.K_w:
                    result = move_player(game_state, "up")

                elif event.key == pygame.K_s:
                    result = move_player(game_state, "down")

                elif event.key == pygame.K_a:
                    result = move_player(game_state, "left")

                elif event.key == pygame.K_d:
                    result = move_player(game_state, "right")

                if game_state["mode"] == "combat":

                    if event.key in [pygame.K_1, pygame.K_2]:
                        handle_combat_input(game_state, event.key)

                # ---------------- MONSTER MOVEMENT (ONLY ON INPUT) ---------------- #
                if result is not None:
                    occupied = [(m.x, m.y) for m in game_state["monsters"]]
                    player_pos = game_state["player_pos"]
                    town_pos = game_state["town_pos"]

                    for m in game_state["monsters"]:
                        m.move(
                            occupied=occupied,
                            forbidden=[tuple(player_pos), tuple(town_pos)],
                            grid_w=MAP_SIZE,
                            grid_h=MAP_SIZE
                        )

                    # exit conditions
                    if result == "returned_to_town":
                        pygame.quit()
                        return result, game_state

                    if result == "combat":
                        return "combat", game_state
                    
        # ---------------- DRAW ---------------- #
        screen.fill((0, 0, 0))

        # town
        tx, ty = game_state["town_pos"]
        pygame.draw.circle(screen,(0, 255, 0),(tx * TILE_SIZE + 16, ty * TILE_SIZE + 16),10)

        # monsters
        for m in game_state["monsters"]:
            pygame.draw.circle(screen,(255, 0, 0),(m.x * TILE_SIZE + 16, m.y * TILE_SIZE + 16),10)

        # player
        px, py = game_state["player_pos"]
        pygame.draw.rect(screen,(255, 255, 255),(px * TILE_SIZE, py * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(30)