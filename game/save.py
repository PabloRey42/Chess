import os
from datetime import datetime

import chess
import chess.pgn

SAVED_GAME_PGN = "saves/saved_game.pgn"

def save_game_pgn(board: chess.Board):
    """Saves the current board's move history to a PGN file."""
    try:
        with open(SAVED_GAME_PGN, "w") as file:
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
    if not os.path.exists(SAVED_GAME_PGN):
        print("No saved game found.")
        return

    try:
        with open(SAVED_GAME_PGN, "r") as file:
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