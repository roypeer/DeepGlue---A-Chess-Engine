import chess
import copy
import random
import chess.svg

'''
See also - Jupyter notebook...
'''

PAWN_VALUE = 1
ROOK_VALUE = 5
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
QUEEN_VALUE = 9

letter_to_value_dict = {'P': PAWN_VALUE, 'R': ROOK_VALUE, 'N': KNIGHT_VALUE, 'B': BISHOP_VALUE, 'Q': QUEEN_VALUE,
                        'p': -1*PAWN_VALUE, 'r': -1*ROOK_VALUE, 'n': -1*KNIGHT_VALUE, 'b': -1*BISHOP_VALUE, 'q': -1*QUEEN_VALUE}

def get_board_score(board, is_white = True):
    score = 0
    for char in str(board):
        value = letter_to_value_dict.get(char)
        if value:
            score += value
    return score


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
        # self.construct_minimax_tree_and_trackers(self.n_moves_forward, self.n_moves_forward)

    # n_moves_forward_left should initially be self.n_moves_forward
    def construct_minimax_tree_and_trackers(self, curr_node, n_moves_forward_left):
        if (n_moves_forward_left == 0):
            return
        curr_node.generate_next_moves()

        curr_depth = self.n_moves_forward - n_moves_forward_left
        for child in curr_node.children_nodes:
            if len(self.trackers) <= curr_depth:
                # self.trackers[curr_depth] = []
                self.trackers.append([])
            self.trackers[curr_depth].append(child)
            self.construct_minimax_tree_and_trackers(child, n_moves_forward_left - 1)

    # Should be called after construct_minimax_tree
    def DEPRACATED_find_best_next_move(self):
        looking_at_level = self.n_moves_forward - 2 # 1
        my_move = looking_at_level % 2 == 1

        for i in range(looking_at_level, -1, -1):
            # Find best move

            for state in self.trackers[looking_at_level]:
                if my_move:
                    state.score = max([child.score for child in state.children_nodes])
                else:
                    state.score = min([child.score for child in state.children_nodes])

            my_move = not my_move

        # Return best move
        return max(self.board_node.children_nodes, key=lambda child: child.score)

    def find_score_recursive(self, curr_node, is_my_move = True):
        # Using recursion
        if(curr_node.children_nodes == []):
            return curr_node.score
        if(is_my_move):
            return max(curr_node.children_nodes, key = lambda child: self.find_score_recursive(child, not is_my_move)).score
        if(not is_my_move):
            return min(curr_node.children_nodes, key=lambda child: self.find_score_recursive(child, not is_my_move)).score

    def find_best_move(self):
        return max(self.board_node.children_nodes, key= lambda child: self.find_score_recursive(child, is_my_move = False))

# Assumes I am white and it is my turn
def roy_engine(board, n_moves_forward):
    minimax = MiniMaxer(ChessBoardTreeNode(board), n_moves_forward)
    minimax.construct_minimax_tree_and_trackers(minimax.board_node, minimax.n_moves_forward)

    # COMPARE BEFORE THIS LINE!
    # best_move = minimax.find_best_next_move()
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

