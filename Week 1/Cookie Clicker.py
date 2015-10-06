"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """   
    def __init__(self):
        self._cookies = 0.0
        self._total_cookies = 0.0
        self._history = [(0.0, None, 0.0, 0.0)]
        self._time = 0.0
        self._cur_cps = 1.0
        
    def __str__(self):
        """
        Return human readable state
        """
        description_str = 	("Total Cookies: " + str(self._total_cookies) + "\n" +
                             "Cookies:       " + str(self._cookies) + "\n" +
                             "Time:          " + str(self._time) + "\n" +
                             "CPS:           " + str(self._cur_cps) + "\n")        
        return "\n" + description_str
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cur_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        cookies_needed = cookies - self._cookies
        if cookies_needed <= 0:
            return 0.0
        else:
            return float(math.ceil(cookies_needed / self._cur_cps)) 
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        self._time += time
        self._cookies += time * self._cur_cps
        self._total_cookies += time * self._cur_cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._cookies:
            self._cookies -= cost
            self._cur_cps += additional_cps
            self._history.append((self._time, item_name, cost, self._total_cookies))

        else:
            return
            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    game = build_info.clone()
    state = ClickerState()
    
    game_clock = 0.0
    
    while (game_clock <= duration):
        next_item = strategy(state.get_cookies(), state.get_cps(), duration - game_clock, game)
        if next_item == None:
            state.wait(duration - game_clock)
            return state
        else:
            cost_next_item = game.get_cost(next_item)
            time_needed = state.time_until(cost_next_item)
            if (time_needed <= duration - game_clock):
                state.wait(time_needed)
                game_clock += time_needed
                additional_cps = game.get_cps(next_item)
                state.buy_item(next_item, cost_next_item, additional_cps)
                game.update_item(next_item)
            else:
                state.wait(duration - game_clock)
                return state
    return state

def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always return cheapest
    """
    game = build_info.clone()
    item_list = game.build_items()
    cheapest = item_list[0]
    for index in range(len(item_list)):
        if game.get_cost(item_list[index]) < game.get_cost(cheapest):
            cheapest = item_list[index]
    if game.get_cost(cheapest) <= (cookies + cps * time_left):
        return cheapest
    else:
        return None

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always return most expensive
    """
    game = build_info.clone()
    item_list = game.build_items()
    affordable_items = []
    most_expensive = None
    for index in range(len(item_list)):
        if game.get_cost(item_list[index]) <= (cookies + cps * time_left):
            affordable_items.append(item_list[index])
    if len(affordable_items) > 0:
        most_expensive = affordable_items[0]
        for index in range(len(affordable_items)):
            if game.get_cost(affordable_items[index]) > game.get_cost(most_expensive):
                most_expensive = affordable_items[index]
    return most_expensive

def strategy_best(cookies, cps, time_left, build_info):
    """ Try to get the most amount of cookies
    """
    game = build_info.clone()
    item_list = game.build_items()
    best_choice = item_list[0]
    for index_i in range(len(item_list)):
        item_cps = game.get_cps(item_list[index_i])
        time_to_get_item = game.get_cost(item_list[index_i]) / cps
        time_to_get_best = game.get_cost(best_choice)/cps
       
        if (item_cps/time_to_get_item) > game.get_cps(best_choice)/time_to_get_best:
            best_choice = item_list[index_i]
    
    return best_choice
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
# run()
