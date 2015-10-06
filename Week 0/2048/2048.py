"""
Clone of 2048 game.
"""
import poc_2048_gui
from random import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # Control variable to limit additions to one occurence only
    control = 5 * [True]
    
    # copy the line to return_line with zeros
    length = len(line)
    return_line = line[:]

    # remove zeroes
    while (0 in return_line):
        return_line.remove(0)
    while (len(return_line) < length):
        return_line.append(0)

    # Start addition proces                        
    for index_i in range(length - 1):
        if return_line[index_i] != 0 and return_line[index_i] == return_line[index_i + 1] and control[index_i]:
            return_line[index_i] = 2 * return_line[index_i];
            control[index_i] = False
            for index_l in range(index_i + 1, length - 1):
                return_line[index_l] = return_line[index_l + 1]
            return_line[-1] = 0

    return return_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """init
        """
        self.rows = grid_height
        self.cols = grid_width
        self.reset()
        
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = [[0 for dummy_x in range(self.cols)] for dummy_y in range(self.rows)]
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self.grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.rows
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.cols
                            
    def move(self, direction):
            """
            Move all tiles in the given direction and add
            a new tile if any tiles moved.
            """
            # copy the current grid
            self.old_grid = [list(inner_list) for inner_list in self.grid]

            if (direction == UP):
                self.move_up()
            elif (direction == DOWN):
                self.move_down()
            elif (direction == LEFT):
                self.move_left()
            else:
                self.move_right()

            # if the grid has changed, add a new tile
            if (self.old_grid != self.grid):
                self.new_tile()

    def move_up(self):
        """
        Move all tiles up
        """
        for columns in range(0, self.cols, 1):
            temp_list = []
            for rows in range(0, self.rows, 1):
                temp_list.append(self.grid[rows][columns])
            # we have our list, let's merge
            new_list = merge(temp_list)
            # now put our new list back in grid
            for rows in range(0, self.rows, 1):
                self.grid[rows][columns] = new_list[rows]

    def move_down(self):
        """
        Move all tiles down
        """
        for columns in range(0, self.cols, 1):
            temp_list = []
            for rows in range(self.rows - 1, -1, -1):
                temp_list.append(self.grid[rows][columns])
            # we have our list, let's merge
            new_list = merge(temp_list)
            # now put our new list back in grid
            for rows in range(self.rows - 1, -1, -1):
                self.grid[rows][columns] = new_list[self.rows - 1 - rows]

    def move_left(self):
        """
        Move all tiles left
        """
        for rows in range(0, self.rows, 1):
            temp_list = []
            for columns in range(0, self.cols, 1):
                temp_list.append(self.grid[rows][columns])
            # we have our list, let's merge
            new_list = merge(temp_list)
            # now put our new list back in grid
            for columns in range(0, self.cols, 1):
                self.grid[rows][columns] = new_list[columns]

    def move_right(self):
        """
        Move all tiles right
        """
        for rows in range(0, self.rows, 1):
            temp_list = []
            for columns in range(self.cols - 1, -1, -1):
                temp_list.append(self.grid[rows][columns])
            # we have our list, let's merge
            new_list = merge(temp_list)
            # now put our new list back in grid
            for columns in range(self.cols - 1, -1, -1):
                self.grid[rows][columns] = new_list[self.cols - 1 - columns]        

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_spot_found = False
        
        # check if there's an empty spot left
        for list in self.grid:
            if 0 in list:
                empty_spot_found = True

        while empty_spot_found:
            # generate tile value
            if random() < 0.9:
                new_tile = 2
            else:
                new_tile = 4

            # randomly pick a empty place on board
            row = int(random() * self.rows)
            col = int(random() * self.cols)
            if self.grid[row][col] == 0:
                self.grid[row][col] = new_tile
                break
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.grid[row][col]
 
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
