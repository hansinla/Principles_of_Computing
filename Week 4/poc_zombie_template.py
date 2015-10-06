"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        return (zombie for zombie in self._zombie_list)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        return (human for human in self._human_list)
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        grid_height = self.get_grid_height()
        grid_width  = self.get_grid_width()
        distance_field = [[grid_height * grid_width for dummy_col in range(grid_width)] for dummy_row in range(grid_height)]
        visited = poc_grid.Grid(grid_height, grid_width)
        for dummy_row in range(grid_height):
            for dummy_col in range(grid_width):
                if not self.is_empty(dummy_row, dummy_col):
                    visited.set_full(dummy_row, dummy_col)
        
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for cell in self._human_list:
                boundary.enqueue((cell[0], cell[1]))
        elif entity_type == ZOMBIE:
            for cell in self._zombie_list:
                boundary.enqueue((cell[0], cell[1]))
        for cell in boundary:
            distance_field[cell[0]][cell[1]] = 0
            visited.set_full(cell[0], cell[1])
            
        while boundary.__len__() > 0:
            cell = boundary.dequeue()
            distance = distance_field[cell[0]][cell[1]] + 1
            
            all_neighbors = self.four_neighbors(cell[0], cell[1])
                        
            for cell in all_neighbors:
                row = cell[0]
                col = cell[1]
                if visited.is_empty(row, col):
                    boundary.enqueue((row, col))
                    if distance_field[row][col] > distance:
                        distance_field[row][col] = distance
                    visited.set_full(row, col)           
        return distance_field
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        temp_humans = []
        for human in self._human_list:
            distance = zombie_distance[human[0]][human[1]]
            best_cell = human
            all_neighbors = self.eight_neighbors(human[0], human[1])
            for cell in all_neighbors:
                if zombie_distance[cell[0]][cell[1]] > distance and self.is_empty(cell[0], cell[1]):
                    best_cell = cell
                    distance = zombie_distance[cell[0]][cell[1]]
            temp_humans.append(best_cell)
        self._human_list = []
        for human in temp_humans:
            self._human_list.append(human)
        
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        temp_zombies = []
        for zombie in self._zombie_list:
            distance = human_distance[zombie[0]][zombie[1]]
            best_cell = zombie
            all_neighbors = self.four_neighbors(zombie[0], zombie[1])
            for cell in all_neighbors:
                if human_distance[cell[0]][cell[1]] < distance and self.is_empty(cell[0], cell[1]):
                    best_cell = cell
                    distance = human_distance[cell[0]][cell[1]]
            temp_zombies.append(best_cell)
        self._zombie_list = []
        for zombie in temp_zombies:
            self._zombie_list.append(zombie)


# start up gui for simulation
poc_zombie_gui.run_gui(Zombie(30, 40))
