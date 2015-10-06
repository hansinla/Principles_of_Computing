"""
Monte Carlo Tic-Tac-Toe Player
Hans van Riet 2014
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 200   # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    tries to win a board with random moves from the given position
    """   
    while (board.check_win() == None):
        # randomly pick a empty place on board
        empty_cell_list = board.get_empty_squares()
        coord = random.choice(empty_cell_list)
        board.move(coord[0], coord[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    Score the completed board and update the scores grid.
    """
    winner = board.check_win()
    if winner == provided.DRAW:
        return
    
    dim = board.get_dim()
    for row in range(dim):
        for col in range(dim):
            if board.square(row, col) == provided.EMPTY:
                pass
            elif board.square(row, col) == winner:
                scores[row][col] += MCMATCH
            else:
                scores[row][col] -= MCOTHER

def get_best_move(board, scores):
    """
    The function finds all of the empty squares with the maximum score
    and randomly return one of them as a (row, column) tuple.
    """
    empty_cell_list = board.get_empty_squares()
    if len(empty_cell_list) == 1:
        return empty_cell_list[0]
    
    best_coords = [empty_cell_list[0]]
    best_value = scores[best_coords[0][0]][best_coords[0][1]]
    
    for coord in empty_cell_list:
        if scores[coord[0]][coord[1]] > best_value:
            best_coords = [coord]
            best_value = scores[coord[0]][coord[1]]
        elif scores[coord[0]][coord[1]] == best_value:
            best_coords.append(coord)
            
    if len(best_coords) > 1:
        return random.choice(best_coords)
    else:
        return best_coords[0]

def mc_move(board, player, trials):
    """
    The function uses the Monte Carlo simulation to return a move
    for the machine player in the form of a (row, column) tuple.
    """
    dim = board.get_dim()
    score_board = init_board(dim)
    
    # Execute num trials
    for dummy_i in range(trials):
        board_copy = board.clone()
        mc_trial(board_copy, player)
        mc_update_scores(score_board, board_copy, player)
       
    return get_best_move(board, score_board)

def init_board(dim):
    """
    Initializes a board with zeros
    """
    return [[0 for dummy_x in range(dim)] for dummy_y in range(dim)]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
