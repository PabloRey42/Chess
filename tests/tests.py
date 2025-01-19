import unittest
import chess
from game.Ia import evaluate_board, get_best_move

class TestIa(unittest.TestCase):

    def test_evaluate_board_initial(self):
        """
        Test l'évaluation d'un échiquier au début du jeu.
        """
        board = chess.Board()  # Échiquier initial
        evaluation = evaluate_board(board)
        self.assertEqual(evaluation, 0, "L'évaluation initiale doit être 0 car le jeu est équilibré.")

    def test_evaluate_board_white_advantage(self):
        """
        Test l'évaluation lorsque les blancs ont un avantage matériel.
        """
        board = chess.Board()
        board.set_board_fen("8/8/8/8/8/8/4P3/8 w - - 0 1")  # Un pion blanc en plus
        evaluation = evaluate_board(board)
        self.assertGreater(evaluation, 0, "Les blancs ont un avantage, donc l'évaluation doit être positive.")

    def test_evaluate_board_black_advantage(self):
        """
        Test l'évaluation lorsque les noirs ont un avantage matériel.
        """
        board = chess.Board()
        board.set_board_fen("8/8/8/8/8/8/8/4p3 w - - 0 1")  # Un pion noir en plus
        evaluation = evaluate_board(board)
        self.assertLess(evaluation, 0, "Les noirs ont un avantage, donc l'évaluation doit être négative.")

    def test_get_best_move_initial(self):
        """
        Teste que l'IA génère un mouvement valide au début du jeu.
        """
        board = chess.Board()  # Échiquier initial
        best_move = get_best_move(board, depth=1)
        self.assertIn(best_move, board.legal_moves, "Le mouvement généré par l'IA doit être valide.")

    def test_get_best_move_checkmate(self):
        """
        Teste que l'IA choisit un coup de mat lorsqu'il est disponible.
        """
        board = chess.Board()
        board.set_board_fen("8/8/8/8/8/8/5k2/R6K w - - 0 1")  # Les blancs peuvent mater en un coup
        best_move = get_best_move(board, depth=1)
        self.assertEqual(str(best_move), "a1a8", "L'IA doit jouer le coup gagnant pour mater.")

if __name__ == "__main__":
    unittest.main()
