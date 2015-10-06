"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    state = board.check_win()
    if state != None:
        return SCORES[state], (-1, -1)
    else:
        empty_list = board.get_empty_squares()
        best_score = None
        best_move = ()

        for square in empty_list:           
            copy_board = board.clone()
            copy_board.move(square[0], square[1], player)
            score, dummy_position = mm_move(copy_board, provided.switch_player(player))
            
            if score * SCORES[player] == 1:
                return score, square
            else:
                if player == provided.PLAYERX:
                    if best_score == None or score > best_score:
                        best_score = score
                        best_move = square
                else:
                    if best_score == None or score < best_score:
                        best_score = score
                        best_move = square
                           
        return best_score, best_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


