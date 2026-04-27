from WanderingMonster import WanderingMonster
import pygame

TILE_SIZE = 32
MAP_SIZE = 10


# ---------------- MAP STATE ---------------- #
def create_map_state():
    return {
        "player_pos": [5, 5],
        "town_pos": [0, 0],
        "monsters": [
            WanderingMonster.random_spawn([], [], 10, 10)
        ]
    }


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
    for m in game_state["monsters"]:
        if [x, y] == [m.x, m.y]:
            return "monster_encounter"

    return "moved"


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

                if event.key == pygame.K_w:
                    result = move_player(game_state, "up")

                elif event.key == pygame.K_s:
                    result = move_player(game_state, "down")

                elif event.key == pygame.K_a:
                    result = move_player(game_state, "left")

                elif event.key == pygame.K_d:
                    result = move_player(game_state, "right")

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
                    if result in ["returned_to_town", "monster_encounter"]:
                        pygame.quit()
                        return result, game_state

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