import pygame
import random
TILE_SIZE = 32
MAP_SIZE = 10

def create_map_state():
    return {
        "player_pos": [5, 5],
        "town_pos": [0, 0],
        "monster_pos": [7, 7]
    }

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
    x = max(0, min(9, x))
    y = max(0, min(9, y))

    game_state["player_pos"] = [x, y]

    # outcomes
    if [x, y] == game_state["town_pos"]:
        return "returned_to_town"

    if [x, y] == game_state["monster_pos"]:
        return "monster_encounter"

    return "moved"

def run_map_interface(game_state):
    pygame.init()

    screen = pygame.display.set_mode((320, 320))
    clock = pygame.time.Clock()

    while True:
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
                else:
                    result = "moved"

                if result in ["returned_to_town", "monster_encounter"]:
                    pygame.quit()
                    return result, game_state

        # drawing
        screen.fill((0, 0, 0))

        # town
        tx, ty = game_state["town_pos"]
        pygame.draw.circle(screen, (0, 255, 0),
                           (tx * TILE_SIZE + 16, ty * TILE_SIZE + 16), 10)

        # monster
        mx, my = game_state["monster_pos"]
        pygame.draw.circle(screen, (255, 0, 0),
                           (mx * TILE_SIZE + 16, my * TILE_SIZE + 16), 10)

        # player
        px, py = game_state["player_pos"]
        pygame.draw.rect(screen, (255, 255, 255),
                         (px * TILE_SIZE, py * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(30)