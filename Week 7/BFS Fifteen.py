"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""
class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
    
    def legal_moves(self):
        """
        Returns string with legal moves l,r,d,u
        """
        answer = ''
        zero_tile = self.current_position(0,0)
        if zero_tile[0] != 0:
            answer += 'u'
        if zero_tile[1] != 0:
            answer += 'l'
        if zero_tile[0] != self._height -1:
            answer += 'd'
        if zero_tile[1] != self._width -1:
            answer += 'r'
        return answer
        
    def solved(self):
        """
        Check to see if puzzle is solved
        """
        for row in range(self._height):
            for col in range(self._width):
                if (self.current_position(row, col) != (row, col)):
                    return False
        return True

    ##################################################################
    
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        import time
        starttime = time.time()
        # visited will be the set of board states that have already been considered. It uses board
        # strings rather than boards to be sure duplicate boards are recognized as one
        visited = set(str(self))
        # Frontier is the set of visited puzzles whose children have not yet been explored. Frontier
        # stores boards as puzzle items and their originating path
        new_frontier = set([(self, 'x')])  		# Start with 'x' to make redundancy detection easier
        path_length_under_consideration = 0
    
        if self.solved():
            print ('Puzzle was already solved. No moves needed.')
            return ''
        
        while True:
            ### Refresh frontier, move to next solution length
            old_frontier = new_frontier.copy()
            new_frontier = set()
            path_length_under_consideration += 1
            
            ### Running status updates (not operable in CodeSkulptor) 
#            print
#            print 'Just refreshed the frontier.'
#            print '    Running time:',round(time.time()-starttime)
#            print '    Number of boards visited:', len(visited)
#            print '    Length of frontier:', len(old_frontier)
#            print '    Solution length under consideration:', path_length_under_consideration

            for parent_tuple in old_frontier:    # For each board in frontier, determine and consider children boards 
                possible_moves = parent_tuple[0].legal_moves()
                for move in possible_moves:
                    if parent_tuple[1][-1] + move in ('ud', 'du', 'lr', 'rl'):   # Check for move redundancy
                        pass
                    else:
                        child_puzzle = parent_tuple[0].clone()   # Copy parent
                        child_puzzle.update_puzzle(move)         # Make move
                        child_string = str(child_puzzle)         # Make boardstring of new puzzle board
                        if child_string in visited:              # If new board has already been considered, pass
                            pass
                        else:                                    # This board state hasn't been previously visited.
                            if child_puzzle.solved():            # If child board is a solution, dance!
                                print ()
                                print ('WooHoo!')
                                print ('Time taken:', round(time.time() - starttime))
                                print ('Number of board states visited:', len(visited) + 1 )
                                print ('Solution length is', len(parent_tuple[1][1:]) + 1)
                                print ('Solution:',parent_tuple[1][1:] + move)
                                print ()
                                return parent_tuple[1][1:] + move
                            else:                               # Child board is not a solution. Add to visited list and to the new frontier
                                visited.add(child_string)
                                new_frontier.add((child_puzzle, parent_tuple[1] + move))
                                   
    ##################################################################

def scrambled_board(row, height, nummoves):
    """
    Makes new puzzle and makes nummoves random moves.
    """
    import random
    jpuzz = Puzzle(row, height)
    movecount = 0
    movelist = 'x'        # to streamline redundancy check
    while movecount < nummoves:
        while True:
            move = random.choice(['u','d','l','r'])
            if movelist[-1] + move not in ('du','ud','rl','lr'): # Avoid undoing the last move
                break
        try:
            jpuzz.update_puzzle(move)        # If move is legal, make it!
            movelist += move
            movecount += 1
        except:
            pass
    print ('scrambling move count:', movecount)
    print ('scrambling move list: ', movelist[1:])
    return jpuzz
    
                                   
    ##################################################################


puzzle = scrambled_board(3,3,200)                # Start with scrambled board
#poc_fifteen_gui.FifteenGUI(puzzle)


# Pearson challenge from discussion boards:
#puzzle=Puzzle(4,4,[[15,11,8,12],[14,10,9,13],[2,6,1,4],[3,7,5,0]])   # Needs 80 moves
sol=puzzle.solve_puzzle()
print (sol)
print (len(sol))
print (puzzle)

#Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
