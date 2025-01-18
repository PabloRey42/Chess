import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)

BOARD_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BOARD_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2

pieces = {}
for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
    for color in ["white", "black"]:
        image = pygame.image.load(f"images/{color}_{piece}.png")
        pieces[f"{color}_{piece}"] = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE * 2))
