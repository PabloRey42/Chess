import os
from datetime import datetime

import chess
import chess.pgn

SAVE_FILE = "saves/saved_game.fen"
#
# def save_game(board):
#     """Saves the current board state to a file."""
#     try:
#         with open(SAVE_FILE, "w") as file:
#             file.write(board.fen())
#         print("Game saved successfully.")
#     except Exception as e:
#         print(f"Error saving game: {e}")
#
# def load_game(board):
#     """Loads the board state from a file, if available."""
#     if os.path.exists(SAVE_FILE):
#         try:
#             with open(SAVE_FILE, "r") as file:
#                 fen = file.read().strip()
#                 board.set_fen(fen)
#             print("Game loaded successfully.")
#         except Exception as e:
#             print(f"Error loading game: {e}")
#     else:
#         print("No saved game found.")
#

def save_game_pgn(board: chess.Board):
    """Saves the current board's move history to a PGN file."""
    try:
        with open("saved_game.pgn", "w") as file:
            exporter = chess.pgn.FileExporter(file)
            game = chess.pgn.Game()
            node = game
            for move in board.move_stack:
                node = node.add_variation(move)
            game.headers["Event"] = "Saved Game"
            game.headers["Site"] = "Local"
            game.headers["Date"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            game.headers["Round"] = "1"
            game.headers["White"] = "Player 1"
            game.headers["Black"] = "Player 2"
            game.accept(exporter)
        print("Game saved to PGN successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")


def load_game_pgn() -> chess.Board | None:
    """Loads a game from a PGN file and restores the board state."""
    if not os.path.exists("saved_game.pgn"):
        print("No saved game found.")
        return

    try:
        with open("saved_game.pgn", "r") as file:
            game = chess.pgn.read_game(file)
            if not game:
                print("Error reading PGN file.")
                return

            board = chess.Board()
            for move in game.mainline_moves():
                board.push(move)
        print("Game loaded from PGN successfully.")
        return board
    except Exception as e:
        print(f"Error loading game: {e}")