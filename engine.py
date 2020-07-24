import chess
import copy
import random
import chess.svg
from chess_auxiliary_functions import get_board_score

'''
See also - Jupyter notebook...
'''


class ChessBoardTreeNode:
    def __init__(self, board):
        self.board = board
        self.children_nodes = []
        self.score = get_board_score(board)

    def generate_next_moves(self):
        for move in list(self.board.legal_moves):
            new_board = copy.deepcopy(self.board)
            new_board.push(move)
            self.children_nodes.append(ChessBoardTreeNode(new_board))


class MiniMaxer:
    def __init__(self, curr_board_node, n_moves_forward):
        self.board_node = curr_board_node
        self.n_moves_forward = n_moves_forward
        self.trackers = []

    # n_moves_forward_left should initially be self.n_moves_forward
    def construct_minimax_tree(self, curr_node, n_moves_forward_left):
        if (n_moves_forward_left == 0):
            return
        curr_node.generate_next_moves()

        for child in curr_node.children_nodes:
            self.construct_minimax_tree(child, n_moves_forward_left - 1)

    def find_score_recursive(self, curr_node, is_my_move = True):
        # Break condition - leaf
        if curr_node.children_nodes == []:
            return curr_node.score
        if is_my_move :
            return max(curr_node.children_nodes, key = lambda child: self.find_score_recursive(child, not is_my_move)).score
        if not is_my_move:
            return min(curr_node.children_nodes, key=lambda child: self.find_score_recursive(child, not is_my_move)).score

    def find_best_move(self):
        return max(self.board_node.children_nodes, key= lambda child: self.find_score_recursive(child, is_my_move = False))

# Assumes I am white and it is my turn
def roy_engine(board, n_moves_forward):
    minimax = MiniMaxer(ChessBoardTreeNode(board), n_moves_forward)
    minimax.construct_minimax_tree(minimax.board_node, minimax.n_moves_forward)
    best_move = minimax.find_best_move()
    return best_move.board

def random_engine(board):
    new_board = copy.deepcopy(board)
    moves = new_board.legal_moves
    new_board.push(random.choice(list(moves)))
    return new_board


if __name__ == "__main__":
    # Let's play a game
    board = chess.Board()
    print(board)
    print("----------\n\n")
    ROY_MOVES_FORWARD = 3

    for turns in range(10):
        board = roy_engine(board, ROY_MOVES_FORWARD)
        print("ROY'S MOVE: \n")
        print(board)
        print("----------\n\n")

        board = random_engine(board)
        print("RANDOM'S MOVE: \n")
        print(board)
        print("----------\n\n")

