import pygame
import sys

# --- Game Configuration --- #
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 40
FPS = 60

WALL_COLOR = (100, 100, 100)
FLOOR_COLOR = (30, 30, 30)

# --- Utility Functions --- #
def verify_level(level):
    max_rows = HEIGHT // TILE_SIZE
    max_cols = WIDTH // TILE_SIZE
    assert len(level) <= max_rows, "LEVEL MAP TOO LARGE"
    assert len(level) <= max_cols, "LEVEL MAP TOO LARGE"
    expected_cols = len(level[0])
    for row in level:
        assert len(row) == expected_cols, "ROWS MUST BE SAME LENGTH"

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
        "W.WWWW...W",
        "W....W...W",
        "W..K.W.E.W",
        "WWWWWWWWWW",
    ],
    2 : [
        "WWWWWWWWWW",
        "WP.......W",
        "W.WWWW...W",
        "W....W...W",
        "W..K.W.E.W",
        "WWWWWWWWWW",
    ],
}
for i, level in level_maps.items():
    print(f"Validating level {i}")
    verify_level(level)

# --- Game Main Loop --- #
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()