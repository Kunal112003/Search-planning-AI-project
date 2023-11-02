import random
import unittest 
from connect4 import Board
from math import inf
def alpha_beta(board, player, alpha, beta, ply):
    """
    Function receives an instance of the Board class, the player who is to act at this state (either X or O),
    the value of alpha, beta, and the maximum search depth given by the variable ply.

    The function returns three values: 
    1. the score of the optimal move for the player who is to act;
    2. the optimal move
    3. the total number of nodes expanded to find the optimal move 
    """
	
	
    # Check if we've reached the maximum search depth or the game is over
    if ply == 0 or board.is_terminal():
        return evaluate_game(board, player), None, 1

    # Initialize best move and number of nodes expanded
    best_move = None
    nodes_expanded = 1

    # Determine whether the current player is maximizing or minimizing
    if player == "X":
        maximizing_player = True
    else:
        maximizing_player = False

    # Initialize alpha and beta values
    if maximizing_player:
        best_score = float("-inf")
        value = float("-inf")
    else:
        best_score = float("inf")
        value = float("inf")
    num_nodes = 0
    # Loop through all possible moves
    for move in board.available_moves():

        # Make the move on the board
        board.perform_move(move,player)

        # Increment nodes expanded count
        
        # Recursively call alpha_beta function on the new board state
        score, _, num_nodes = alpha_beta(board, get_opponent(player), alpha, beta, ply - 1)
        
        board.undo_move(move)
        nodes_expanded += num_nodes

        # Update best score and best move if necessary
        if maximizing_player and score > best_score:
            best_score = score
            best_move = move
        elif not maximizing_player and score < best_score:
            best_score = score
            best_move = move

        # Update alpha or beta values
        if maximizing_player:
            value = max(value, score)
            alpha = max(alpha, value)
            
        else:
            value = min(value, score)
            beta = min(beta, value)
            

        # Check if we can prune the remaining nodes
        if beta <= alpha:
            
            break
        
        

    if best_move == None:
        return 0, None, 1
    else:
        
        return best_score, best_move, nodes_expanded




def evaluate_game(board, player):
    """
    Given a board and a player, returns a heuristic evaluation of the board state for that player.
    """
    
    if board.has_winner():
        
        if board.get_winner() == player:
            
            if player == 'X':
                return 1
            if player == 'O':
                return -1
        else:
            return 1 if player == 'O' else -1
    else:
        return 0
    
    


def get_opponent(player):
    """
    Given a player, returns the opponent player.
    """
    if player == 'X':
        return 'O'
    else:
        return 'X'


class TestMinMaxDepth1(unittest.TestCase):

	def test_depth1a(self):
		b = Board()
		player = b.create_board('010101')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 0)

	def test_depth1b(self): 
		b = Board() 
		player = b.create_board('001122')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)

	def test_depth1c(self): 
		b = Board() 
		player = b.create_board('335566')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 4)

	def test_depth1d(self):
		b = Board() 
		player = b.create_board('3445655606')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 6)

	def test_depth1e(self):
		b = Board() 
		player = b.create_board('34232210101')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 1)

	def test_depth1f(self):
		b = Board() 
		player = b.create_board('23445655606')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 6)

	def test_depth1g(self): 
		b = Board() 
		player = b.create_board('33425614156')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 1)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 2)

class TestMinMaxDepth3(unittest.TestCase):

	def test_depth3a(self):
		b = Board()
		player = b.create_board('303111426551')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 2)

	def test_depth3b(self): 
		b = Board() 
		player = b.create_board('23343566520605001')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 6)

	def test_depth3c(self): 
		b = Board() 
		player = b.create_board('10322104046663')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 0)

	def test_depth3d(self):
		b = Board() 
		player = b.create_board('00224460026466')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)

	def test_depth3e(self):
		b = Board() 
		player = b.create_board('102455500041526')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 1)

	def test_depth3f(self):
		b = Board() 
		player = b.create_board('01114253335255')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 2)

	def test_depth3g(self): 
		b = Board() 
		player = b.create_board('0325450636643')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 3)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 5)

class TestMinMaxDepth5(unittest.TestCase):
	def test_depth5a(self):
		b = Board()
		player = b.create_board('430265511116')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)
		
	def test_depth5b(self):
		b = Board()
		player = b.create_board('536432111330')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 5)

	def test_depth5c(self):
		b = Board()
		player = b.create_board('322411004326')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)

	def test_depth5d(self):
		b = Board()
		player = b.create_board('3541226000220')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 4)

	def test_depth5e(self):
		b = Board()
		player = b.create_board('43231033655')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
		self.assertEqual(bestScore, -1)
		self.assertEqual(bestMove, 1)

	def test_depth5f(self):
		b = Board()
		player = b.create_board('345641411335')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 5)

	def test_depth5g(self):
		b = Board()
		player = b.create_board('336604464463')
		bestScore, bestMove, expansions = alpha_beta(b, player, -inf, inf, 5)
		print(bestScore, bestMove, expansions)

		self.assertEqual(bestScore, 1)
		self.assertEqual(bestMove, 3)			


if __name__ == '__main__':
    unittest.main()
    