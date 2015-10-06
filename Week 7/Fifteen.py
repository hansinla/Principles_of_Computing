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

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        conditions_met = True
        
        # test tile zero is positioned at (target_row, target_col)
        if self.get_number(target_row, target_col) != 0:
            return False
        
        # test all tiles in rows i+1 or below are positioned at their solved location
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self.get_number(row, col) != col + self._width * row:
                    return False
        
        # test all tiles in row i to the right of position (i,j) are positioned at their solved location
        row = target_row
        col = target_col + 1
        while col < self._width:
            if self.get_number(row, col) != col + self._width * row:
                return False
            col += 1
                
        return conditions_met

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        solution = ""
        
        # find current position of target tile
        target_tile = self.current_position(target_row, target_col)
        
        solution += (target_row - target_tile[0]) * 'u'
        if target_col >= target_tile[1]:
            solution += (target_col - target_tile[1]) * 'r'
        else:
            solution += (target_tile[1] - target_col) * 'l'
        
        return solution

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        conditions_met = True
        
        # test tile zero is positioned at (0, target_col)
        if self.get_number(0, target_col) != 0:
            print("FALSE in test 1")
            return False
        
        # test all tiles in rows i+1 or below are positioned at their solved location
        for row in range(2, self._height):
            for col in range(self._width):
                if self.get_number(row, col) != col + self._width * row:
                    print("FALSE in test 2")
                    return False
        
        # test all tiles in row 0 to the right of position (0,j) are positioned at their solved location
        col = target_col + 1
        while col < self._width:
            if self.get_number(0, col) != col:
                print("FALSE in test 3")
                return False
            col += 1
            
        # additional test for (1, target_col)
        if self.get_number(1, target_col) != col + self._width:
            print (1, target_col, self.get_number(1, target_col), col + self._width)
            print("FALSE in test 4")
            return False
                
        return conditions_met


    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        conditions_met = True
        
        # test check whether tile zero is at (1, target_col)
        if self.get_number(1, target_col) != 0:
            return False
        
        # test whether all positions either below or to the right of this position are solved
        for row in range(2, self._height):
            for col in range(self._width):
                if self.get_number(row, col) != col + self._width * row:
                    return False
        
        # test all tiles in row 1 to the right of position (1,j) are positioned at their solved location
        col = target_col + 1
        while col < self._width:
            if self.get_number(1, col) != col + self._width:
                return False
            col += 1
                
        return conditions_met


    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # testing 
        return ""

# Start interactive simulation
test = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])

print(test.row0_invariant(0))


