import pygame
import chess
import sys

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
BOARD_SIZE = 600  
CELL_SIZE = BOARD_SIZE // 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)

BOARD_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BOARD_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2

board = chess.Board()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu d'Échecs")

pieces = {}
for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
    for color in ["white", "black"]:
        image = pygame.image.load(f"images/{color}_{piece}.png")
        pieces[f"{color}_{piece}"] = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE*2))

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(
                screen,
                color,
                (BOARD_X + col * CELL_SIZE, BOARD_Y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

def draw_pieces():
    piece_types = {
        chess.PAWN: "pawn",
        chess.ROOK: "rook",
        chess.KNIGHT: "knight",
        chess.BISHOP: "bishop",
        chess.QUEEN: "queen",
        chess.KING: "king"
    }
    for square in reversed(chess.SQUARES):
        piece = board.piece_at(square)
        if piece:
            piece_name = piece_types[piece.piece_type]
            color = "white" if piece.color == chess.WHITE else "black"
            image = pieces[f"{color}_{piece_name}"]

            row, col = divmod(square, 8)

            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + (7 - row) * CELL_SIZE - CELL_SIZE
            screen.blit(image, (x, y))

def highlight_moves(square):
    moves = list(board.legal_moves)
    for move in moves:
        if move.from_square == square:
            to_square = move.to_square
            row, col = divmod(to_square, 8)

            x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_Y + (7 - row) * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, (x, y), 10)

def draw_buttons():
    font = pygame.font.Font(None, 36)
    reset_button = font.render("Reset", True, (0, 0, 0))
    quit_button = font.render("Quit", True, (0, 0, 0))

    pygame.draw.rect(screen, (200, 200, 200), (50, 200, 100, 50))
    screen.blit(reset_button, (65, 210))

    pygame.draw.rect(screen, (200, 200, 200), (850, 200, 100, 50))
    screen.blit(quit_button, (865, 210))


def draw_turn():
    font = pygame.font.Font(None, 36)
    turn_txt = "Turn: White" if board.turn else "Turn: Black"
    turn_render = font.render(turn_txt, True, WHITE)

    text_width = turn_render.get_width()
    text_x = (WINDOW_WIDTH - text_width) // 2 # Center le text
    text_y = 20
    screen.blit(turn_render, (text_x, text_y))


def convert_click_to_square(x, y):
    col = (x - BOARD_X) // CELL_SIZE
    row = 7 - (y - BOARD_Y) // CELL_SIZE  # Inverser l'axe des y
    return chess.square(col, row)

def animate_victory(winner):
    font = pygame.font.Font(None, 72)
    text = f"{'Les Blancs' if winner == chess.WHITE else 'Les Noirs'} gagnent !"
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    alpha_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    alpha = 0

    while alpha < 150:
        alpha_surface.fill((0, 0, 0, alpha))
        screen.blit(alpha_surface, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(30)
        alpha += 5


def highlight_on_check():
    if board.is_check():
        king_square = board.king(board.turn)

        row, col = divmod(king_square, 8)
        x = BOARD_X + col * CELL_SIZE
        y = BOARD_Y + (7 - row) * CELL_SIZE

        # Change background to red
        highlight_color = (255, 0, 0, 128)
        highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        highlight_surface.fill(highlight_color)
        screen.blit(highlight_surface, (x, y))

        # Add red border color
        # highlight_color = (255, 0, 0)  # Bright red
        # rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        # pygame.draw.rect(screen, highlight_color, rect, 4)  # 4-pixel border

def main():
    selected_square = None
    running = True

    print(board)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if 50 <= x <= 150 and 200 <= y <= 250:  
                    board.reset()
                    selected_square = None
                elif 850 <= x <= 950 and 200 <= y <= 250:  
                    running = False
                elif BOARD_X <= x <= BOARD_X + BOARD_SIZE and BOARD_Y <= y <= BOARD_Y + BOARD_SIZE:
                    square = convert_click_to_square(x, y)
                    if selected_square:
                        move = chess.Move(selected_square, square)
                        if move in board.legal_moves:
                            board.push(move)
                        selected_square = None
                    else:
                        piece = board.piece_at(square)
                        if piece and piece.color == (board.turn == chess.WHITE):
                            selected_square = square


        screen.fill((50, 50, 50))
        draw_board()
        highlight_on_check()
        draw_pieces()
        draw_turn()
        if selected_square:
            highlight_moves(selected_square)
        draw_buttons()

        if board.is_checkmate():
            winner = not board.turn
            animate_victory(winner)
            board.reset()
            selected_square = None

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
