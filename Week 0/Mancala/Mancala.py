"""
Class to run the game logic for solitaire mancala
TO BE RUN INSIDE CODESKULPTOR
"""
import poc_mancala_gui


class SolitaireMancala:
    """ Class definition
    """

    def __init__(self):
        """(board) -> NoneType
        """       
        self.board = [0]

    def set_board(self, configuration):
        """(list) -> list
        """
        self.board = [0]
        self.board[0] = configuration[0]
        for i in range (1, len(configuration)):
            self.board.append(configuration[i])
        
    def __str__(self):
        """ None -> str
        returns a description of the game board
        """
        result = "["
        for i in range (len(self.board)):
           result += str(self.board[len(self.board) -1 - i]) 
           if i < len(self.board) -1:
               result += ", "
        result += "]"
        return result

    def get_num_seeds(self, house_num):
        """int -> int
        """
        return self.board[house_num]

    def is_legal_move(self, house_num):
        """int -> Boolean
        """
        if (house_num == 0):
            return False
        elif (house_num == self.board[house_num]):
            return True
        else:
            return False

    def apply_move(self, house_num):
        """int -> NoneType
        """
        if (self.is_legal_move(house_num)):
            self.board[house_num] =0
            for i in range(house_num - 1, -1, -1):
                self.board[i] += 1

    def choose_move(self):
        """ NoneType -> int
        return best legal move
        """
        for i in range(len(self.board)):
            if (self.is_legal_move(i)):
                return i
        return 0

    def is_game_won(self):
        """ returns true if game is won
        """
        for i in range(1, len(self.board)):
            if (self.board[i] != 0):
                return False
        return True

    def plan_moves(self):
        """ NoneType -> list
        Completes a list with legal moves
        """
        test_board = SolitaireMancala()
        test_board.set_board(self.board)
        moves = []

        while True:
            move = test_board.choose_move()
            if move == 0:
                return moves
            test_board.apply_move(move)
            moves.append(move)
            if (test_board.is_game_won()):
                return moves

poc_mancala_gui.run_gui(SolitaireMancala())
