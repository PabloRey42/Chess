from game.constants import *
import pygame
import chess 
import sys
from game.Ia import evaluate_board, get_best_move
from game.save import save_game_pgn, load_game_pgn

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('./sounds/sound.mp3')

board = chess.Board()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu d'Échecs")

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
        promoting_piece = board.piece_at(square)
        if promoting_piece:
            piece_name = piece_types[promoting_piece.piece_type]
            piece_color = "white" if promoting_piece.color == chess.WHITE else "black"
            piece_image = pieces[f"{piece_color}_{piece_name}"]

            row, col = divmod(square, 8)

            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + (7 - row) * CELL_SIZE - CELL_SIZE
            screen.blit(piece_image, (x, y))

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
    undo_button = font.render("Undo", True, (0, 0, 0))
    save_button = font.render("Save", True, (0, 0, 0))
    load_button = font.render("Load", True, (0, 0, 0))

    pygame.draw.rect(screen, (200, 200, 200), (50, 200, 100, 50))
    screen.blit(reset_button, (65, 210))

    pygame.draw.rect(screen, (200, 200, 200), (850, 200, 100, 50))
    screen.blit(quit_button, (865, 210))

    pygame.draw.rect(screen, (200, 200, 200), (50, 300, 100, 50))
    screen.blit(undo_button, (65, 310))

    pygame.draw.rect(screen, (200, 200, 200), (50, 400, 100, 50))
    screen.blit(save_button, (65, 410))

    pygame.draw.rect(screen, (200, 200, 200), (50, 500, 100, 50))
    screen.blit(load_button, (65, 510))


def draw_turn():
    font = pygame.font.Font(None, 36)
    turn_txt = "Turn: White" if board.turn else "Turn: Black"
    turn_render = font.render(turn_txt, True, WHITE)

    text_width = turn_render.get_width()
    text_x = (WINDOW_WIDTH - text_width) // 2  # Center le text
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

def highlight_square_on_check():
    if board.is_check():
        king_square = board.king(board.turn)

        row, col = divmod(king_square, 8)
        x = BOARD_X + col * CELL_SIZE
        y = BOARD_Y + (7 - row) * CELL_SIZE

        border_check = True  # change background color to red else add a red border to cell
        if border_check:
            # Change background to red
            highlight_color = (255, 0, 0, 128)
            highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(highlight_color)
            screen.blit(highlight_surface, (x, y))
        else:
            # Add red border color
            highlight_color = (255, 0, 0)  # Bright red
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, highlight_color, rect, 4)  # 4-pixel border

def show_promotion_menu(x, y, color):
    """
    Displays a horizontal promotion menu with sprites for the player to choose from, asynchronously.
    Args:
        x, y: The position to display the menu.
        color: The color of the pawn being promoted.
    Returns:
        The selected promotion piece (chess.QUEEN, chess.ROOK, etc.)
    """
    options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    sprites = [pieces[f"{color}_queen"], pieces[f"{color}_rook"],
               pieces[f"{color}_bishop"], pieces[f"{color}_knight"]]

    menu_width = CELL_SIZE * 4
    menu_height = CELL_SIZE
    menu_x = x - (menu_width - CELL_SIZE) // 2
    menu_y = y - CELL_SIZE

    selected_piece = None

    pygame.draw.rect(screen, (200, 200, 200), (menu_x, menu_y, menu_width, menu_height))  # Background
    pygame.draw.rect(screen, BLACK, (menu_x, menu_y, menu_width, menu_height), 3)  # Border
    for i, sprite in enumerate(sprites):
        sprite_x = menu_x + i * CELL_SIZE
        sprite_y = menu_y - CELL_SIZE
        screen.blit(sprite, (sprite_x, sprite_y))
    pygame.display.flip()

    while selected_piece is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = pygame.mouse.get_pos()
                # print(f"click_x: {click_x}: click_y {click_y}")
                if not (menu_x <= click_x <= menu_x + menu_width and menu_y <= click_y <= menu_y + menu_height):
                    return None
                for i in range(4):
                    sprite_x = menu_x + i * CELL_SIZE
                    sprite_y = menu_y
                    option_rect = pygame.Rect(sprite_x, sprite_y, CELL_SIZE, CELL_SIZE)
                    if option_rect.collidepoint(click_x, click_y):
                        selected_piece = options[i]
    return selected_piece

def is_promoting(moving_piece, square):
    return (moving_piece.piece_type is chess.PAWN and
            ((moving_piece.color == chess.WHITE and chess.square_rank(square) == 7)
             or (moving_piece.color == chess.BLACK and chess.square_rank(square) == 0)))

def main():
    selected_square = None
    running = True
    global board

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
                elif 50 <= x <= 150 and 300 <= y <= 350:
                    if len(board.move_stack) > 1:
                        board.pop()
                        board.pop()
                        selected_square = None
                elif 50 <= x <= 150 and 400 <= y <= 450:
                    save_game_pgn(board)
                elif 50 <= x <= 150 and 500 <= y <= 550:
                    pgn = load_game_pgn()
                    if pgn is not None:
                        board = pgn
                elif BOARD_X <= x <= BOARD_X + BOARD_SIZE and BOARD_Y <= y <= BOARD_Y + BOARD_SIZE:
                    if board.turn:  # Le joueur humain joue les blancs
                        square = convert_click_to_square(x, y)
                        if selected_square is not None:
                            moving_piece = board.piece_at(selected_square)
                            chosen_promotion = None
                            if is_promoting(moving_piece, square):
                                pawn_x = BOARD_X + (square % 8) * CELL_SIZE
                                pawn_y = BOARD_Y + (7 - (square // 8)) * CELL_SIZE
                                chosen_promotion = show_promotion_menu(pawn_x, pawn_y, "white" if moving_piece.color else "black")
                            move = chess.Move(selected_square, square, promotion=chosen_promotion)
                            if move in board.legal_moves:
                                board.push(move)
                                pygame.mixer.music.play()
                            selected_square = None
                        else:
                            piece = board.piece_at(square)
                            if piece and piece.color == board.turn:
                                selected_square = square

        if not board.turn:  # C'est au tour des noirs (IA)
            ai_move = get_best_move(board, depth=2)  # Profondeur ajustable
            if ai_move:
                board.push(ai_move)
                pygame.mixer.music.play()
            selected_square = None

        screen.fill((50, 50, 50))
        draw_board()
        highlight_square_on_check()
        draw_pieces()
        draw_turn()
        if selected_square is not None:
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
