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
        swapped_color = "black" if color == "white" else "white"
        image = pygame.image.load(f"{swapped_color}_{piece}.png")
        pieces[f"{color}_{piece}"] = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

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
    #AAAAAAAAAAAAAAAAAAAAAAAA je vais me tabasser !
    piece_types = {
        chess.PAWN: "pawn",
        chess.ROOK: "rook",
        chess.KNIGHT: "knight",
        chess.BISHOP: "bishop",
        chess.QUEEN: "queen",
        chess.KING: "king"
    }
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_name = piece_types[piece.piece_type]
            color = "white" if piece.color == chess.WHITE else "black"
            image = pieces[f"{color}_{piece_name}"]

            row, col = divmod(square, 8)

            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + row * CELL_SIZE
            screen.blit(image, (x, y))

def highlight_moves(square):
    moves = list(board.legal_moves)
    for move in moves:
        if move.from_square == square:
            to_square = move.to_square
            row, col = divmod(to_square, 8)

            x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, (x, y), 10)

def draw_buttons():
    font = pygame.font.Font(None, 36)
    reset_button = font.render("Reset", True, (0, 0, 0))
    quit_button = font.render("Quit", True, (0, 0, 0))

    pygame.draw.rect(screen, (200, 200, 200), (50, 200, 100, 50))
    screen.blit(reset_button, (65, 210))

    pygame.draw.rect(screen, (200, 200, 200), (850, 200, 100, 50))
    screen.blit(quit_button, (865, 210))

def convert_click_to_square(x, y):
    col = (x - BOARD_X) // CELL_SIZE
    row = (y - BOARD_Y) // CELL_SIZE

    return chess.square(col, row)

def main():
    selected_square = None
    runningjeparlepasdelacourseapiedsmaisjustesilaboucletourneencoreoupas = True

    print(board)  
    while runningjeparlepasdelacourseapiedsmaisjustesilaboucletourneencoreoupas:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningjeparlepasdelacourseapiedsmaisjustesilaboucletourneencoreoupas = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if 50 <= x <= 150 and 200 <= y <= 250:  
                    board.reset()
                    selected_square = None
                elif 850 <= x <= 950 and 200 <= y <= 250:  
                    runningjeparlepasdelacourseapiedsmaisjustesilaboucletourneencoreoupas(jeparlepasdelacourseapiedsmaisjustesilaboucletourneencofreoupas) = False
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
        draw_pieces()
        if selected_square:
            highlight_moves(selected_square)
        draw_buttons()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
