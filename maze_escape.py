import pygame
import sys

# --- Game Configuration --- #
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 40
PLAYER_SIZE = 20
PLAYER_SPEED = 5
TIME_SECONDS = 20
FPS = 60

WALL_COLOR = (100, 100, 100)
FLOOR_COLOR = (30, 30, 30)
PLAYER_COLOR = (0, 255, 0)
KEY_COLOR = (255, 255, 0)
EXIT_COLOR = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- Utility Functions --- #
def verify_level(level):
    max_rows = HEIGHT // TILE_SIZE
    max_cols = WIDTH // TILE_SIZE
    assert len(level) <= max_rows, "LEVEL MAP TOO LARGE"
    assert len(level) <= max_cols, "LEVEL MAP TOO LARGE"
    expected_cols = len(level[0])
    P = 0
    K = 0
    E = 0
    for row in level:
        assert len(row) == expected_cols, "ROWS MUST BE SAME LENGTH"
        for c in row:
            assert c in "WPKE.", "UNEXPECTED CHARACTER IN LEVEL MAP"
            if c == "P":
                P += 1
            if c == "K":
                K += 1
            if c == "E":
                E += 1
    assert P == 1, "ONLY ONE PLAYER ALLOWED"
    assert E == 1, "ONLY ONE EXIT ALLOWED"
    assert K == 1, "ONLY ONE KEY ALLOWED"

def load_level(level_map):
    walls = []
    key = None
    exit = None
    player = None
    N = len(level_map)
    M = len(level_map[0])
    floor = pygame.Rect(0, 0, M*TILE_SIZE, N*TILE_SIZE)

    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            offset = (TILE_SIZE - PLAYER_SIZE) / 2
            if tile == "W":
                walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile == "K":
                key = pygame.Rect(x + offset, y + offset, PLAYER_SIZE, PLAYER_SIZE)
            elif tile == "P":
                player = pygame.Rect(x + offset, y + offset, PLAYER_SIZE, PLAYER_SIZE)
            elif tile == "E":
                exit = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    return floor, walls, key, exit, player

def draw(screen, floor, walls, key, exit, player):
    pygame.draw.rect(screen, FLOOR_COLOR, floor)
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)
    if key:
        pygame.draw.rect(screen, KEY_COLOR, key)
    pygame.draw.rect(screen, EXIT_COLOR, exit)
    pygame.draw.rect(screen, PLAYER_COLOR, player)

def update_player(player, keys, walls):
    player_x = player.x
    player_y = player.y
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player.y += PLAYER_SPEED

    # Check for collision with walls
    for wall in walls:
        if wall.colliderect(player):
            player.x = player_x
            player.y = player_y
            return

def draw_win_message(screen):
        font = pygame.font.SysFont(None, 36)
        game_over_text = font.render("YOU WIN", True, GREEN)
        restart_text = font.render("Press R to play again.", True, WHITE)

        screen.blit(game_over_text, (WIDTH // 2 - 90, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - 140, HEIGHT // 2 + 10))

def draw_hud(screen, has_key, level, message, t):
    font = pygame.font.SysFont(None, 30)
    hud_text = font.render(f"Get the key! Find the Exit!   Key: {has_key}  Level: {level}  Time: {t:.1f}", True, WHITE)
    screen.blit(hud_text, (10, 10))

    hud_text = font.render(message, True, WHITE)
    screen.blit(hud_text, (10, HEIGHT - 40))

def reset_game(level):
    global floor, walls, key, exit, player, has_key, game_state, message, timer
    floor, walls, key, exit, player = load_level(level_maps[level])
    has_key = False
    game_state = "playing"
    message = ""
    timer = TIME_SECONDS

# --- Game Initialization --- #
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Level Maps --- #
level_maps = { 
    0 : [
        "WWWWWWWWWW",
        "WP.......W",
        "W.WWWW...W",
        "W....W...W",
        "W..K.W.E.W",
        "WWWWWWWWWW",
    ],
    1 : [
        "WWWWWWWWWW",
        "WP.......W",
        "WWWWWWWW.W",
        "W........W",
        "W...KW..EW",
        "WWWWWWWWWW",
    ],
    2 : [
        "WWWWWWWWWWWWWWWWWWWW",
        "WP.................W",
        "W.WWWW.............W",
        "W....W.............W",
        "W..K.W.............W",
        "W..................W",
        "W..................W",
        "W..................W",
        "W..................W",
        "W..................W",
        "W..................W",
        "W..................W",
        "W..................W",
        "W.................EW",
        "WWWWWWWWWWWWWWWWWWWW",
    ],
}
for i, level in level_maps.items():
    print(f"Validating level {i}")
    verify_level(level)

# --- Load --- #
level = 0
floor, walls, key, exit, player = load_level(level_maps[0])
has_key = False
game_state = "playing"
number_of_levels = len(level_maps)
message = ""
timer = TIME_SECONDS

# --- Game Main Loop --- #
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "win" and event.key == pygame.K_r:
                level = 0
                reset_game(level)

    # Get inputs and update player position
    keys = pygame.key.get_pressed()

    if game_state == "playing":
        update_player(player, keys, walls)

        # Check for key
        if not has_key and player.colliderect(key):
            has_key = True

        # Check win condition
        if player.colliderect(exit):
            if has_key:
                level += 1
                if level >= number_of_levels:
                    game_state = "win"
                else:
                    reset_game(level)

            else:
                message = "Find the key first"

        # Draw
        screen.fill((0, 0, 0))
        draw(screen, floor, walls,
            key if not has_key else None,
            exit, player
        )
        draw_hud(screen, has_key, level, message, timer)
    elif game_state == "win":
        screen.fill((0, 0, 0))
        draw_win_message(screen)
    pygame.display.flip()

    # Advance Frame
    clock.tick(60)
    timer -= 1/60

    # Check timer, restart level
    if timer <= 0.0:
        reset_game(level)

pygame.quit()
sys.exit()