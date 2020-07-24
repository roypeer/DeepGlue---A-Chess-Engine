PAWN_VALUE = 1
ROOK_VALUE = 5
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
QUEEN_VALUE = 9

letter_to_value_dict = {'P': PAWN_VALUE, 'R': ROOK_VALUE, 'N': KNIGHT_VALUE, 'B': BISHOP_VALUE, 'Q': QUEEN_VALUE,
                        'p': -1*PAWN_VALUE, 'r': -1*ROOK_VALUE, 'n': -1*KNIGHT_VALUE, 'b': -1*BISHOP_VALUE, 'q': -1*QUEEN_VALUE}

def get_board_score(board, is_black = False):
    score = 0
    for char in str(board):
        value = letter_to_value_dict.get(char)
        if value:
            if(is_black):
                value *= -1
            score += value
    return score