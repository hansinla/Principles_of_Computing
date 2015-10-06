"""
A simple testing suite for 2048
Note that tests are not exhaustive and should be supplemented
"""

import poc_simpletest

def run_test(game_class):
    """
    Some informal testing code
    """

    string = "[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]"
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    # create a game
    game = game_class

    # test the initial configuration of the board using the str method
    suite.run_test(str(game), string, "Test #0: init")

    # set_tile / get_tile test
    game.set_tile(2,2,4)
    suite.run_test(game.get_tile(2,2), 4, "Test 1a: set_tile / get_tile")
    game.set_tile(0,0,4)
    suite.run_test(game.get_tile(0,0), 4, "Test 1b: set_tile / get_tile")
    game.set_tile(3,3,2)
    suite.run_test(game.get_tile(3,3), 2, "Test 1c: set_tile / get_tile")

    # reset test
    game.reset()
    suite.run_test(str(game), string, "Test #2: reset")

    # new_tile test
    for i in range(16):
        game.new_tile()
    count = 0
    for row in range(4):
        for col in range(4):
            if (game.get_tile(row, col) == 0): count += 1
    suite.run_test(count, 0, "Test #3: calling new_tile 16 times fills grid")
   
    # report number of tests and failures
    suite.report_results()
