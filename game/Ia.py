import random
from game.constants import *
import pygame
import chess 
import sys

def evaluate_board(board):
    """
    Simple evaluation function for the board.
    Positive value means advantage for white, negative means advantage for black.
    """
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            evaluation += value if piece.color == chess.WHITE else -value
    return evaluation

def get_best_move(board, depth=2):
    """
    Minimax algorithm to find the best move for the current player.
    """
    def minimax(board, depth, maximizing_player):
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = minimax(board, depth - 1, False)
                board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = minimax(board, depth - 1, True)
                board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    best_move = None
    best_value = float('-inf') if board.turn else float('inf')

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, not board.turn)
        board.pop()

        if (board.turn and board_value > best_value) or (not board.turn and board_value < best_value):
            best_value = board_value
            best_move = move

    return best_move
