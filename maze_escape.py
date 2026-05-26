import pygame
import sys

# --- Game Configuration --- #
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 40
PLAYER_SIZE = 20
PLAYER_SPEED = 5
FPS = 60

WALL_COLOR = (100, 100, 100)
FLOOR_COLOR = (30, 30, 30)
PLAYER_COLOR = (0, 255, 0)
KEY_COLOR = (255, 255, 0)
EXIT_COLOR = (255, 0, 0)

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
floor, walls, key, exit, player = load_level(level_maps[2])

# --- Game Main Loop --- #
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get inputs and update player position
    keys = pygame.key.get_pressed()
    update_player(player, keys, walls)

    # Draw
    screen.fill((0, 0, 0))
    draw(screen, floor, walls, key, exit, player)
    pygame.display.flip()

    # Advance Framee
    clock.tick(60)

pygame.quit()
sys.exit()